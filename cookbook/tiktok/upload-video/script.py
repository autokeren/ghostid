#!/usr/bin/env python3
"""
Upload a specific video file to TikTok via Ghostid — no chooser, no guessing.

Battle-tested flow (Nov 2026, Galaxy S22 Ultra, via Cloudflare tunnel only):

  1. MediaStore scan + lookup the file's content:// id
  2. Fire ACTION_SEND *directly* at TikTok's share activity
     (com.ss.android.ugc.trill/com.ss.android.ugc.aweme.share.SystemShareActivity)
     with FLAG_GRANT_READ_URI_PERMISSION — the system share sheet never appears,
     so you can never tap the wrong target.
  3. Tap "Berikutnya" using bounds from a fresh uiautomator dump
     (NEVER guess coordinates from a screenshot — the preview image is scaled).
  4. Set the caption with /a11y/type (full-field replace, avoids the
     `input text` %23 double-encoding trap for '#').
  5. Tap "Posting", dismiss the "Tautkan email" / "Aktifkan notifikasi?"
     popups ("Nanti saja" / "Lain kali"), verify on the feed.

The phone drives itself - this script only talks to the Ghostid REST API
through your Cloudflare tunnel. No ADB, no USB.

Usage:
  set GHOSTID_URL=https://YOUR-TUNNEL.trycloudflare.com
  set GHOSTID_TOKEN=your-device-token
  python script.py "/sdcard/Movies/my-video.mp4" "My caption #hashtag"

Requirements: requests (pip install requests)
"""

import base64
import os
import re
import sys
import time

import requests

BASE = os.environ["GHOSTID_URL"].rstrip("/")
TOKEN = os.environ["GHOSTID_TOKEN"]
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

TIKTOK_PKG = "com.ss.android.ugc.trill"
TIKTOK_SHARE = TIKTOK_PKG + "/com.ss.android.ugc.aweme.share.SystemShareActivity"


def call(endpoint, **params):
    r = requests.get(f"{BASE}{endpoint}", params=params, headers=HEADERS, timeout=120)
    r.raise_for_status()
    return r.json()


def shell(cmd):
    return call("/sh", cmd=cmd)


def ui_dump():
    """Fresh uiautomator dump -> list of (text, desc, bounds-tuple)."""
    shell("uiautomator dump /sdcard/ui.xml")
    r = call("/file/get", path="/sdcard/ui.xml")
    raw = base64.b64decode(r.get("b64") or "").decode("utf-8", "replace")
    nodes = []
    for m in re.finditer(r"<node[^>]*>", raw):
        tag = m.group(0)

        def attr(name):
            mm = re.search(name + r'="([^"]*)"', tag)
            return mm.group(1) if mm else ""

        b = re.search(r'bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"', tag)
        if not b:
            continue
        nodes.append((attr("text"), attr("content-desc"), tuple(map(int, b.groups()))))
    return nodes


def find(nodes, needle):
    for t, d, b in nodes:
        for v in (t, d):
            if v and needle.lower() in v.lower():
                return (t, d, b)
    return None


def tap_node(n):
    x1, y1, x2, y2 = n[2]
    return call("/a11y/tap", x=(x1 + x2) // 2, y=(y1 + y2) // 2)


def wait_for(needle, timeout=30):
    end = time.time() + timeout
    while time.time() < end:
        n = find(ui_dump(), needle)
        if n:
            return n
        time.sleep(2)
    return None


def screenshot(name):
    shot = call("/screen")
    if shot.get("png_b64"):
        with open(name, "wb") as f:
            f.write(base64.b64decode(shot["png_b64"]))
        print("   screenshot saved:", name)


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "/sdcard/Movies/my-video.mp4"
    caption = sys.argv[2] if len(sys.argv) > 2 else "Video baru! #FYP"
    name = os.path.basename(path)

    print("1) wake the screen (keep it on while this runs)")
    shell("input keyevent KEYCODE_WAKEUP")
    time.sleep(1)

    print("2) media scan:", name)
    shell(f"am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d file://{path}")
    time.sleep(2)

    print("3) lookup media id")
    r = shell(
        "content query --uri content://media/external/video/media "
        "--projection _id:_display_name "
        f"--where \"_display_name LIKE '%{name}%'\""
    )
    m = re.search(r"_id=(\d+)", r.get("result") or "")
    if not m:
        print("ERR: file not indexed in MediaStore")
        return 1
    media_id = m.group(1)
    print("   media id:", media_id)

    print("4) direct share into the TikTok editor (no chooser)")
    shell(
        "am start -a android.intent.action.SEND -t video/mp4 "
        f"--eu android.intent.extra.STREAM content://media/external/video/media/{media_id} "
        f"-n {TIKTOK_SHARE} -f 0x1"
    )

    print("5) wait for the editor, tap Berikutnya")
    ed = wait_for("Berikutnya", 60)
    if not ed:
        print("ERR: editor did not open")
        return 1
    tap_node(ed)
    time.sleep(5)

    print("6) caption (full-field replace via /a11y/type)")
    cap = wait_for("Tambah deskripsi", 20)
    if cap:
        tap_node(cap)
        time.sleep(1)
        # find= matches the field's current text (or its hint on first use)
        cur = cap[0] or cap[1]
        first_word = (cur.split() or ["deskripsi"])[0]
        call("/a11y/type", value=caption, find=first_word)
        time.sleep(1)
        shell("input keyevent 4")  # close keyboard
        time.sleep(1)
    else:
        print("WARN: caption field not found - posting without caption")

    print("7) tap Posting")
    post = wait_for("Posting", 15)
    if not post:
        print("ERR: Posting button not found")
        return 1
    tap_node(post)
    time.sleep(12)

    print("8) dismiss post-upload popups")
    for needle in ("Nanti saja", "Lain kali"):
        n = wait_for(needle, 8)
        if n:
            tap_node(n)
            time.sleep(3)

    print("9) verify")
    screenshot("tiktok_post.png")
    print("DONE: confirm the new post at the top of the profile video grid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
