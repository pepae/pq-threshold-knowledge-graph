---
id: pq-threshold
type: implementation
title: pq-threshold (TACET reference implementation)
repo: https://github.com/pepae/pq-threshold
url: https://github.com/pepae/pq-threshold
language: [Python, Rust, Coq]
runnable: true
source_depth: repo
measured: "self-reported scorecard of 10 PASS / 5 PARTIAL / 0 FAIL against D1-D15, checked by runtime tests, measurements and named artifacts"
implements: [tacet, tacet-silent]
uses: [zero-sharing-masks, vector-commitments, replicated-secret-sharing, low-norm-secret-sharing, wee-matrix-commitment]
---

The reference implementation of [[tacet]] and [[tacet-silent]]: a Python reference,
a constant-time Rust core, Coq proofs of the security composition and noise budget,
and a compiled paper.

## Caveat first

Unpublished and unreviewed. The scorecard below is the project's own assessment of
its own scheme, executed by its own test suite. That is more evidence than a paper
claim alone, and less than external review.

## What is actually checked

`bench/ef_requirements.py` evaluates each of D1-D15 end to end, with a runtime test
where testable, a measurement where quantitative, and a structural statement naming
the supporting artifact otherwise. This file is also the source of the canonical
D1-D15 numbering used throughout this KB, which is why the KB and this project agree
on what D14 means.

Result: 10 pass, 5 partial, 0 fail. The partials are the lattice tax on ciphertext
and share size, the static-corruption relaxation, the committee-size cost, and silent
setup.

Two checks are worth singling out because they test properties rather than
performance. The [[D9]] check runs an actual harvesting attempt: it builds partial
decryptions under one anchor and under a competing fork's anchor, combines half from
each, and asserts the mixed combination fails while the consistent one succeeds. The
[[D14]] check asserts both that every included position opens and that no epoch
parameter exists in the parameter set.

## Why the KB cites it

For the measurements and the audit log. See [[tacet]] for the corrections that
building it produced, two of which are recorded as their own nodes:
[[linear-route-opening-impossibility]] and
[[flooding-underestimate-ring-setting]].
