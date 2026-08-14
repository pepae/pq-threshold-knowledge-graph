"""Record a scripted tour of the KB webapp.

Deliberately slow and smooth: every pan, zoom and hover is driven in many small
steps so the recording reads as motion rather than as jump cuts. The app itself
has no transitions, which is on purpose (see the layout notes), so all the motion
here comes from the camera.
"""
import pathlib, shutil, sys
from playwright.sync_api import sync_playwright

OUT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "/tmp/kb-tour-raw")
URL = "http://localhost:8770/"
W, H = 1512, 950
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"

if OUT.exists():
    shutil.rmtree(OUT)
OUT.mkdir(parents=True)

# world coordinates lifted from a reference render at this exact viewport; the
# layout is deterministic, so they land on the same nodes every run
WHOLE = {
    "beat_mev":   (858, 595),
    "tacet":      (934, 606),
    "d14":        (876, 384),
    "start_here": (708, 281),
    "blt":        (1090, 740),
    "schemes":    (1010, 640),
    "assumptions": (350, 480),
    "attacks":    (520, 750),
}


def glide(pg, a, b, steps=45):
    pg.mouse.move(*a)
    pg.mouse.move(*b, steps=steps)


def zoom(pg, at, ticks, dy=-110, pause=16):
    pg.mouse.move(*at)
    for _ in range(ticks):
        pg.mouse.wheel(0, dy)
        pg.wait_for_timeout(pause)


with sync_playwright() as p:
    b = p.chromium.launch(executable_path=CHROME)
    ctx = b.new_context(viewport={"width": W, "height": H},
                        record_video_dir=str(OUT),
                        record_video_size={"width": W, "height": H},
                        device_scale_factor=1)
    pg = ctx.new_page()
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto(URL, wait_until="networkidle")
    pg.wait_for_timeout(2600)

    # 1. the landing guide, read a little
    pg.mouse.move(430, 500)
    for _ in range(7):
        pg.mouse.wheel(0, 150)
        pg.wait_for_timeout(120)
    pg.wait_for_timeout(700)
    for _ in range(5):
        pg.mouse.wheel(0, -180)
        pg.wait_for_timeout(90)
    pg.wait_for_timeout(500)

    # 2. search, and land on a scheme
    pg.click("#search")
    pg.type("#search", "epoch-free", delay=105)
    pg.wait_for_timeout(1500)
    pg.keyboard.press("Escape")
    pg.click("#search")
    pg.type("#search", "BEAT-MEV", delay=100)
    pg.wait_for_timeout(1400)
    pg.keyboard.press("Enter")
    pg.wait_for_timeout(2400)

    # 3. hover the neighbourhood: isolation + tooltips
    glide(pg, (1150, 470), (1180, 520), 30)
    pg.wait_for_timeout(900)
    glide(pg, (1180, 520), (1060, 640), 40)
    pg.wait_for_timeout(900)
    glide(pg, (1060, 640), (1250, 380), 45)
    pg.wait_for_timeout(1000)

    # 4. widen the context to 2 hops
    pg.select_option("#hops", "2")
    pg.wait_for_timeout(2600)
    glide(pg, (1100, 500), (1000, 600), 40)
    pg.wait_for_timeout(1100)

    # 5. jump to a guide, showing the narrative layer
    pg.select_option("#guides", "the-problems")
    pg.wait_for_timeout(2500)
    pg.mouse.move(430, 520)
    for _ in range(6):
        pg.mouse.wheel(0, 170)
        pg.wait_for_timeout(110)
    pg.wait_for_timeout(900)

    # 6. the whole graph, full screen
    pg.select_option("#hops", "1")
    pg.wait_for_timeout(600)
    pg.click("#expand")
    pg.wait_for_timeout(900)
    pg.click("#global")
    pg.wait_for_timeout(3400)

    # 7. fly over it
    zoom(pg, WHOLE["schemes"], 7)
    pg.wait_for_timeout(1200)
    glide(pg, WHOLE["schemes"], WHOLE["assumptions"], 70)
    pg.wait_for_timeout(1000)
    zoom(pg, WHOLE["assumptions"], 5, dy=110)
    pg.wait_for_timeout(900)
    pg.click("#refit")
    pg.wait_for_timeout(1600)

    # 8. one hub, isolated: cross-cluster traffic
    pg.mouse.move(*WHOLE["beat_mev"], steps=1)
    pg.wait_for_timeout(2000)
    glide(pg, WHOLE["beat_mev"], WHOLE["d14"], 40)
    pg.wait_for_timeout(1700)
    glide(pg, WHOLE["d14"], WHOLE["blt"], 45)
    pg.wait_for_timeout(1700)
    pg.mouse.move(760, 130)
    pg.wait_for_timeout(900)

    # 9. reveal the 63 people: the full wealth, 178 nodes
    pg.click('#legend button[data-t="person"]')
    pg.wait_for_timeout(4200)
    zoom(pg, (760, 500), 4)
    pg.wait_for_timeout(1400)
    pg.click("#refit")
    pg.wait_for_timeout(1600)
    pg.click('#legend button[data-t="person"]')
    pg.wait_for_timeout(3000)

    # 10. narrow it down: post-quantum only, then one desideratum
    pg.click("#pqonly")
    pg.wait_for_timeout(2800)
    pg.mouse.move(700, 480)
    pg.wait_for_timeout(1300)
    pg.click("#pqonly")
    pg.wait_for_timeout(2400)
    pg.select_option("#dfilter", "D14")
    pg.wait_for_timeout(2800)
    glide(pg, (700, 450), (820, 520), 35)
    pg.wait_for_timeout(1600)
    pg.select_option("#dfilter", "")
    pg.wait_for_timeout(2200)

    # 11. back to two panes, rebalance them
    pg.click("#expand")
    pg.wait_for_timeout(1400)
    g = pg.eval_on_selector("#gutter",
        "e=>{const r=e.getBoundingClientRect();return[r.x+r.width/2,r.y+r.height/2]}")
    pg.mouse.move(g[0], g[1])
    pg.mouse.down()
    pg.mouse.move(g[0] - 300, g[1], steps=40)
    pg.wait_for_timeout(500)
    pg.mouse.move(g[0] + 60, g[1], steps=40)
    pg.mouse.up()
    pg.wait_for_timeout(1200)

    # 12. end where a reader starts
    pg.click("#search")
    pg.type("#search", "start here", delay=95)
    pg.wait_for_timeout(1100)
    pg.keyboard.press("Enter")
    pg.wait_for_timeout(2600)

    print("page errors:", errs[:5] if errs else "none")
    path = pg.video.path()
    ctx.close()
    b.close()
    print("raw video:", path)

# encode the two deliverables next to the repo's docs/
import subprocess
try:
    import imageio_ffmpeg
    ff = imageio_ffmpeg.get_ffmpeg_exe()
except ImportError:
    sys.exit("pip install imageio-ffmpeg to encode; raw webm is at " + str(path))

docs = pathlib.Path(__file__).resolve().parent.parent / "docs"
docs.mkdir(exist_ok=True)
subprocess.run([ff, "-hide_banner", "-loglevel", "error", "-i", path,
                "-vf", "fps=24,scale=1280:-2", "-c:v", "libx264", "-pix_fmt", "yuv420p",
                "-crf", "29", "-preset", "veryslow", "-movflags", "+faststart", "-an",
                str(docs / "demo.mp4"), "-y"], check=True)
# The GIF is a thumbnail, not a document: short, small and sped up 2x so it
# loops before a reader scrolls past. Labels are illegible at 640px by design;
# the mp4 and the live site carry the detail.
subprocess.run([ff, "-hide_banner", "-loglevel", "error", "-ss", "44", "-t", "14",
                "-i", path, "-vf",
                "setpts=PTS/2.0,fps=11,scale=640:-2:flags=lanczos,split[a][b];"
                "[a]palettegen=max_colors=48:stats_mode=diff[p];"
                "[b][p]paletteuse=dither=bayer:bayer_scale=5:diff_mode=rectangle",
                "-loop", "0", str(docs / "demo.gif"), "-y"], check=True)
print("wrote docs/demo.mp4 and docs/demo.gif")
