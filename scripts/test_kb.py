#!/usr/bin/env python3
"""Self-tests for the vault parser and graph builder.

These exist so a green CI run means something on an empty or near-empty vault:
they assert that the checks actually fire on malformed input.

    python3 scripts/test_kb.py
"""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

from kb import build_graph, collect_notes, dump_graph, load_schema

SCHEMA = load_schema()


def write(vault: Path, subdir: str, name: str, frontmatter: str, body: str = "") -> None:
    target = vault / subdir
    target.mkdir(parents=True, exist_ok=True)
    (target / f"{name}.md").write_text(
        f"---\n{frontmatter.strip()}\n---\n\n{body}\n", encoding="utf-8"
    )


DESIDERATUM = """
id: D1
type: desideratum
title: 'D1: No trusted setup'
short_name: No trusted setup
"""

ASSUMPTION = """
id: ddh
type: assumption
title: DDH
"""


def minimal_scheme(node_id: str = "demo", extra: str = "") -> str:
    return f"""
id: {node_id}
type: scheme
title: Demo
status: preprint
eprint: "2024/263"
assumptions: [ddh]
satisfies: [D1]
{extra}
"""


class VaultCase(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.vault = Path(self._tmp.name) / "vault"
        self.vault.mkdir(parents=True)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def load(self):
        notes, issues = collect_notes(SCHEMA, self.vault)
        graph, edge_issues = build_graph(notes, SCHEMA)
        return notes, graph, issues + edge_issues

    def assertMessage(self, issues, needle: str) -> None:
        joined = "\n".join(str(i) for i in issues)
        self.assertIn(needle, joined, f"expected {needle!r} in:\n{joined}")

    def seed_valid(self) -> None:
        write(self.vault, "desiderata", "D1", DESIDERATUM)
        write(self.vault, "concepts", "ddh", ASSUMPTION)
        write(self.vault, "schemes", "demo", minimal_scheme())


class TestHappyPath(VaultCase):
    def test_empty_vault_is_valid(self):
        notes, graph, issues = self.load()
        self.assertEqual(issues, [])
        self.assertEqual(graph["metadata"]["node_count"], 0)
        self.assertEqual(graph["metadata"]["edge_count"], 0)

    def test_valid_vault_builds_expected_edges(self):
        self.seed_valid()
        notes, graph, issues = self.load()
        self.assertEqual(issues, [])
        self.assertEqual(len(notes), 3)
        triples = {(e["source"], e["type"], e["target"]) for e in graph["edges"]}
        self.assertIn(("demo", "assumes", "ddh"), triples)
        self.assertIn(("demo", "satisfies", "D1"), triples)

    def test_output_is_deterministic(self):
        self.seed_valid()
        _, first, _ = self.load()
        _, second, _ = self.load()
        self.assertEqual(dump_graph(first), dump_graph(second))
        self.assertNotIn("timestamp", dump_graph(first))

    def test_edge_fields_are_not_copied_into_node_attrs(self):
        self.seed_valid()
        notes, graph, _ = self.load()
        demo = next(n for n in graph["nodes"] if n["id"] == "demo")
        self.assertNotIn("assumptions", demo["attrs"])
        self.assertNotIn("satisfies", demo["attrs"])
        self.assertEqual(demo["attrs"]["eprint"], "2024/263")


class TestReverseEdges(VaultCase):
    def test_superseded_by_becomes_a_forward_supersedes_edge(self):
        self.seed_valid()
        write(self.vault, "schemes", "demo2", minimal_scheme("demo2"))
        path = self.vault / "schemes" / "demo.md"
        path.write_text(
            path.read_text(encoding="utf-8").replace(
                "satisfies: [D1]", "satisfies: [D1]\nsuperseded_by: [demo2]"
            ),
            encoding="utf-8",
        )
        _, graph, issues = self.load()
        self.assertEqual(issues, [])
        triples = {(e["source"], e["type"], e["target"]) for e in graph["edges"]}
        self.assertIn(("demo2", "supersedes", "demo"), triples)
        self.assertNotIn(("demo", "supersedes", "demo2"), triples)

    def test_authors_becomes_a_person_authored_edge(self):
        self.seed_valid()
        write(self.vault, "people", "ada", "id: ada\ntype: person\ntitle: Ada")
        path = self.vault / "schemes" / "demo.md"
        path.write_text(
            path.read_text(encoding="utf-8").replace(
                "satisfies: [D1]", "satisfies: [D1]\nauthors: [ada]"
            ),
            encoding="utf-8",
        )
        _, graph, issues = self.load()
        self.assertEqual(issues, [])
        triples = {(e["source"], e["type"], e["target"]) for e in graph["edges"]}
        self.assertIn(("ada", "authored", "demo"), triples)


class TestHardFailures(VaultCase):
    def test_edge_to_nonexistent_node(self):
        self.seed_valid()
        path = self.vault / "schemes" / "demo.md"
        path.write_text(
            path.read_text(encoding="utf-8").replace("[ddh]", "[ddh, no-such-thing]"),
            encoding="utf-8",
        )
        _, _, issues = self.load()
        self.assertMessage(issues, "unknown id 'no-such-thing'")

    def test_unknown_node_type(self):
        write(self.vault, "schemes", "weird", "id: weird\ntype: gadget\ntitle: W")
        _, _, issues = self.load()
        self.assertMessage(issues, "unknown type 'gadget'")

    def test_missing_required_field(self):
        write(self.vault, "schemes", "nostatus", "id: nostatus\ntype: scheme\ntitle: N")
        _, _, issues = self.load()
        self.assertMessage(issues, "requires field 'status'")

    def test_unknown_frontmatter_field_is_rejected(self):
        self.seed_valid()
        write(
            self.vault,
            "schemes",
            "typo",
            minimal_scheme("typo", extra="assumption: [ddh]"),
        )
        _, _, issues = self.load()
        self.assertMessage(issues, "unknown field 'assumption'")

    def test_id_must_match_filename(self):
        write(
            self.vault,
            "schemes",
            "wrong-name",
            "id: right-name\ntype: scheme\ntitle: X\nstatus: preprint",
        )
        _, _, issues = self.load()
        self.assertMessage(issues, "must equal id 'right-name'")

    def test_type_must_live_in_its_directory(self):
        write(self.vault, "papers", "misfiled", minimal_scheme("misfiled"))
        _, _, issues = self.load()
        self.assertMessage(issues, "must live in vault/schemes/")

    def test_duplicate_id(self):
        write(self.vault, "concepts", "dup", "id: dup\ntype: assumption\ntitle: A")
        write(self.vault, "attacks", "dup", "id: dup\ntype: attack\ntitle: A\nstatus: published")
        _, _, issues = self.load()
        self.assertMessage(issues, "duplicate id 'dup'")

    def test_domain_violation(self):
        """A person cannot satisfy a desideratum."""
        write(self.vault, "desiderata", "D1", DESIDERATUM)
        write(
            self.vault,
            "people",
            "ada",
            "id: ada\ntype: person\ntitle: Ada\nsatisfies: [D1]",
        )
        _, _, issues = self.load()
        self.assertMessage(issues, "unknown field 'satisfies'")

    def test_range_violation(self):
        """assumptions: must point at an assumption, not a technique."""
        self.seed_valid()
        write(self.vault, "concepts", "shamir", "id: shamir\ntype: technique\ntitle: Shamir")
        path = self.vault / "schemes" / "demo.md"
        path.write_text(
            path.read_text(encoding="utf-8").replace("[ddh]", "[shamir]"),
            encoding="utf-8",
        )
        _, _, issues = self.load()
        self.assertMessage(issues, "not in range")

    def test_bad_enum_value(self):
        self.seed_valid()
        path = self.vault / "schemes" / "demo.md"
        path.write_text(
            path.read_text(encoding="utf-8").replace("status: preprint", "status: vibes"),
            encoding="utf-8",
        )
        _, _, issues = self.load()
        self.assertMessage(issues, "must be one of")

    def test_unquoted_eprint_still_parses_as_a_string(self):
        """YAML reads 2024/263 as a string, so the vault convention of quoting
        it is for humans. Document that, so nobody 'fixes' it later."""
        self.seed_valid()
        path = self.vault / "schemes" / "demo.md"
        path.write_text(
            path.read_text(encoding="utf-8").replace('"2024/263"', "2024/263"),
            encoding="utf-8",
        )
        notes, _, issues = self.load()
        self.assertEqual(issues, [])
        self.assertEqual(notes["demo"].fields["eprint"], "2024/263")

    def test_non_string_eprint_is_rejected(self):
        self.seed_valid()
        path = self.vault / "schemes" / "demo.md"
        path.write_text(
            path.read_text(encoding="utf-8").replace('"2024/263"', "2024"),
            encoding="utf-8",
        )
        _, _, issues = self.load()
        self.assertMessage(issues, "field 'eprint' must be a string")

    def test_quoted_year_is_rejected(self):
        self.seed_valid()
        path = self.vault / "schemes" / "demo.md"
        path.write_text(
            path.read_text(encoding="utf-8").replace(
                "status: preprint", 'status: preprint\nyear: "2024"'
            ),
            encoding="utf-8",
        )
        _, _, issues = self.load()
        self.assertMessage(issues, "field 'year' must be an integer")

    def test_non_boolean_pq_is_rejected(self):
        self.seed_valid()
        path = self.vault / "schemes" / "demo.md"
        path.write_text(
            path.read_text(encoding="utf-8").replace(
                "status: preprint", 'status: preprint\npq: "false"'
            ),
            encoding="utf-8",
        )
        _, _, issues = self.load()
        self.assertMessage(issues, "field 'pq' must be a boolean")

    def test_desideratum_id_must_use_the_canonical_D_form(self):
        write(
            self.vault,
            "desiderata",
            "d1",
            "id: d1\ntype: desideratum\ntitle: X\nshort_name: X",
        )
        _, _, issues = self.load()
        self.assertMessage(issues, "must match ^D([1-9]|1[0-5])$")

    def test_desideratum_id_out_of_range_is_rejected(self):
        write(
            self.vault,
            "desiderata",
            "D16",
            "id: D16\ntype: desideratum\ntitle: X\nshort_name: X",
        )
        _, _, issues = self.load()
        self.assertMessage(issues, "must match ^D([1-9]|1[0-5])$")

    def test_non_desideratum_cannot_use_the_D_form(self):
        write(self.vault, "concepts", "D3", "id: D3\ntype: technique\ntitle: X")
        _, _, issues = self.load()
        self.assertMessage(issues, "must match ^[a-z0-9][a-z0-9-]*$")

    def test_missing_frontmatter(self):
        (self.vault / "schemes").mkdir(parents=True, exist_ok=True)
        (self.vault / "schemes" / "bare.md").write_text("no frontmatter\n", encoding="utf-8")
        _, _, issues = self.load()
        self.assertMessage(issues, "missing YAML frontmatter")

    def test_self_edge(self):
        self.seed_valid()
        path = self.vault / "schemes" / "demo.md"
        path.write_text(
            path.read_text(encoding="utf-8").replace(
                "satisfies: [D1]", "satisfies: [D1]\nbuilds_on: [demo]"
            ),
            encoding="utf-8",
        )
        _, _, issues = self.load()
        self.assertMessage(issues, "self-edge")


class TestValidateChecks(VaultCase):
    def test_unresolved_wikilink_is_reported(self):
        import validate

        self.seed_valid()
        path = self.vault / "schemes" / "demo.md"
        path.write_text(
            path.read_text(encoding="utf-8") + "\nSee [[Nonexistent Note]].\n",
            encoding="utf-8",
        )
        notes, _, issues = self.load()
        self.assertEqual(issues, [])
        found = validate.check_wikilinks(notes)
        self.assertMessage(found, "[[Nonexistent Note]] does not resolve")

    def test_wikilink_resolves_by_title_and_alias(self):
        import validate

        self.seed_valid()
        path = self.vault / "concepts" / "ddh.md"
        path.write_text(
            path.read_text(encoding="utf-8").replace(
                "title: DDH", "title: DDH\naliases: [Decisional Diffie-Hellman]"
            ),
            encoding="utf-8",
        )
        demo = self.vault / "schemes" / "demo.md"
        demo.write_text(
            demo.read_text(encoding="utf-8")
            + "\nUses [[ddh]], [[DDH]] and [[Decisional Diffie-Hellman]].\n",
            encoding="utf-8",
        )
        notes, _, _ = self.load()
        self.assertEqual(validate.check_wikilinks(notes), [])

    def test_quality_bar_requires_assumption_and_desideratum(self):
        import validate

        write(self.vault, "papers", "p", "id: p\ntype: paper\ntitle: P\nstatus: published")
        write(
            self.vault,
            "schemes",
            "thin",
            "id: thin\ntype: scheme\ntitle: Thin\nstatus: preprint\nbuilds_on: [p]",
        )
        notes, graph, issues = self.load()
        self.assertEqual(issues, [])
        found = validate.check_quality_bar(notes, graph["edges"], SCHEMA)
        self.assertMessage(found, "no assumption edge")
        self.assertMessage(found, "no desideratum edge")

    def test_malformed_eprint_is_an_error(self):
        import validate

        self.seed_valid()
        path = self.vault / "schemes" / "demo.md"
        path.write_text(
            path.read_text(encoding="utf-8").replace('"2024/263"', '"263/2024x"'),
            encoding="utf-8",
        )
        notes, _, _ = self.load()
        errors, _ = validate.check_citations(notes)
        self.assertMessage(errors, "is not of the form YYYY/NNN")

    def test_unsourced_record_warns_unless_declared(self):
        import validate

        write(
            self.vault,
            "papers",
            "hearsay",
            "id: hearsay\ntype: paper\ntitle: Hearsay\nstatus: preprint",
        )
        notes, _, _ = self.load()
        _, warnings = validate.check_citations(notes)
        self.assertMessage(warnings, "set `unverified: true`")

        path = self.vault / "papers" / "hearsay.md"
        path.write_text(
            path.read_text(encoding="utf-8").replace(
                "status: preprint", "status: preprint\nunverified: true"
            ),
            encoding="utf-8",
        )
        notes, _, _ = self.load()
        _, warnings = validate.check_citations(notes)
        self.assertEqual(warnings, [])

    def test_orphan_and_unreferenced_desideratum_are_reported(self):
        import validate

        write(self.vault, "desiderata", "D1", DESIDERATUM)
        write(self.vault, "concepts", "lonely", "id: lonely\ntype: technique\ntitle: Lonely")
        notes, graph, _ = self.load()
        self.assertMessage(validate.check_orphans(notes, graph["edges"]), "orphan node 'lonely'")
        self.assertMessage(
            validate.check_unreferenced_desiderata(notes, graph["edges"]),
            "desideratum 'D1' has no incoming",
        )


if __name__ == "__main__":
    unittest.main(verbosity=2, buffer=True)
