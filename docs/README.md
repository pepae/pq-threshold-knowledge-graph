# Demo media

`demo.mp4` is an 80-second tour of the webapp. `demo.gif` is a 7-second loop of
the whole-graph view at 640px, sped up 2x, used inline in the top-level README and
for social posts. It is deliberately a thumbnail: node labels are not legible at
that size, and the mp4 and the live site are where the detail lives.

Both are recorded from the real site, not mocked up. To regenerate after a UI
change:

```bash
pip install playwright imageio-ffmpeg && python3 -m playwright install chromium
python3 scripts/build_webapp.py
python3 -m http.server 8770 -d dist &

python3 scripts/record_demo.py            # writes docs/demo.mp4 and docs/demo.gif
```

The tour script drives every pan, zoom and hover in many small steps, because the
app deliberately has no animated transitions: the layout is solved to convergence
before the first frame so it cannot jitter. All the motion in the video is camera
work, not the graph settling.

Node positions in the script are taken from a reference render at 1512x950. The
layout is deterministic and seeded per view, so the same viewport reproduces the
same positions and the scripted hovers land on the intended nodes. If you change
the viewport, the layout parameters or the node set, re-check the coordinates in
`WHOLE` at the top of the script.
