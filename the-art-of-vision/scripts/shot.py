#!/usr/bin/env python3
"""shot.py: chụp từng màn hình (đúng kích thước viewport) để tự xem lại thiết kế trong vòng đánh bóng.

  shot.py <file.html|URL> [--viewports 1440x900,375x812] [--screens 8] [--out polish/<tên>/round-N] [--wait 800]

Thứ tự thử: Playwright (Python) → Chrome/Chromium headless. Ảnh ghi ra <out>/<WxH>/screen-01.png …
Không có Playwright thì Chrome chụp một ảnh dài bằng N màn hình; có Pillow thì cắt ra từng màn hình.
In ra danh sách đường dẫn ảnh. Mở và xem TỪNG ảnh gốc, đừng xem ảnh thu nhỏ.
"""
import argparse, glob, os, shutil, subprocess, sys, tempfile


def to_url(target):
    if "://" in target:
        return target
    return "file://" + os.path.abspath(target)


def next_round(base):
    n = 1
    while os.path.exists(os.path.join(base, "round-%d" % n)):
        n += 1
    return os.path.join(base, "round-%d" % n)


def with_playwright(url, vps, screens, out, wait):
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        return None
    paths = []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for w, h in vps:
            page = browser.new_page(viewport={"width": w, "height": h})
            page.goto(url, wait_until="networkidle")
            page.wait_for_timeout(wait)
            total = page.evaluate("document.documentElement.scrollHeight")
            d = os.path.join(out, "%dx%d" % (w, h)); os.makedirs(d, exist_ok=True)
            for i in range(min(screens, max(1, -(-total // h)))):
                page.evaluate("window.scrollTo(0, %d)" % (i * h))
                page.wait_for_timeout(150)
                path = os.path.join(d, "screen-%02d.png" % (i + 1))
                page.screenshot(path=path)
                paths.append(path)
            page.close()
        browser.close()
    return paths


def find_chrome():
    """-> (đường dẫn, là headless_shell?) của trình duyệt chạy được thật, hoặc (None, False)."""
    cands = []
    for pat in ("~/.cache/ms-playwright/chromium-*/chrome-linux/chrome",
                "~/.cache/ms-playwright/chromium_headless_shell-*/chrome-linux/headless_shell"):
        cands += sorted(glob.glob(os.path.expanduser(pat)), reverse=True)
    for name in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "chrome"):
        if shutil.which(name):
            cands.append(shutil.which(name))
    for c in cands:
        try:
            ok = subprocess.run([c, "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=20).returncode == 0
        except (OSError, subprocess.TimeoutExpired):
            ok = False
        if ok:
            return c, c.endswith("headless_shell")
    return None, False


def with_chrome(url, vps, screens, out, wait):
    chrome, shell = find_chrome()
    if not chrome:
        return None
    paths = []
    for w, h in vps:
        d = os.path.join(out, "%dx%d" % (w, h)); os.makedirs(d, exist_ok=True)
        tall = os.path.join(d, "tall.png")
        with tempfile.TemporaryDirectory() as prof:
            subprocess.run([chrome] + ([] if shell else ["--headless=new"]) + ["--disable-gpu", "--no-sandbox", "--hide-scrollbars",
                            "--user-data-dir=" + prof, "--virtual-time-budget=%d" % wait,
                            "--window-size=%d,%d" % (w, h * screens), "--screenshot=" + tall, url],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=120)
        if not os.path.exists(tall):
            continue
        try:
            from PIL import Image
        except ImportError:
            paths.append(tall)  # không có Pillow: để nguyên ảnh dài
            continue
        img = Image.open(tall)
        for i in range(screens):
            box = img.crop((0, i * h, w, (i + 1) * h))
            if box.convert("L").getextrema()[0] == box.convert("L").getextrema()[1] and i > 0:
                break  # màn hình trống trơn (đã hết trang)
            path = os.path.join(d, "screen-%02d.png" % (i + 1))
            box.save(path)
            paths.append(path)
    return paths


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("target")
    ap.add_argument("--viewports", default="1440x900,375x812")
    ap.add_argument("--screens", type=int, default=8)
    ap.add_argument("--out")
    ap.add_argument("--wait", type=int, default=800)
    a = ap.parse_args()
    vps = [tuple(int(x) for x in v.split("x")) for v in a.viewports.split(",")]
    name = os.path.splitext(os.path.basename(a.target.rstrip("/")))[0] or "page"
    out = a.out or next_round(os.path.join("polish", name))
    url = to_url(a.target)
    paths = with_playwright(url, vps, a.screens, out, a.wait)
    engine = "playwright"
    if paths is None:
        paths, engine = with_chrome(url, vps, a.screens, out, a.wait), "chrome"
    if not paths:
        sys.exit("Không chụp được: cài `pip install playwright && playwright install chromium`, hoặc cài Chrome/Chromium.")
    print("# %s: %d ảnh trong %s" % (engine, len(paths), out))
    for p in paths:
        print(p)


if __name__ == "__main__":
    main()
