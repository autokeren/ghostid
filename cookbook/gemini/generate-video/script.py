#!/usr/bin/env python3
"""
Generate a video with Gemini on an Android phone via Ghostid.

The phone drives itself - this script only talks to the Ghostid REST API
through your Cloudflare tunnel. No ADB, no USB.

Usage:
  set GHOSTID_URL=https://YOUR-TUNNEL.trycloudflare.com
  set GHOSTID_TOKEN=your-token
  python script.py "buatkan video lucu kucing terbang di langit jakarta 9:16"

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

GEMINI_PKG = "com.google.android.apps.bard"


def call(path, **params):
    r = requests.get(f"{BASE}{path}", params=params, headers=HEADERS, timeout=60)
    r.raise_for_status()
    return r.json()


def dump():
    return call("/a11y/dump")


def texts(d):
    return [(n.get("text") or "").strip() for n in d.get("nodes", [])]


def find_node(d, needle, exact=False):
    """Match text OR content-desc (labels often live in desc)."""
    for n in d.get("nodes", []):
        for field in ("text", "desc"):
            t = (n.get(field) or "").strip()
            if not t:
                continue
            if (t == needle) if exact else (needle.lower() in t.lower()):
                return n
    return None


def tap_node(n):
    b = n["bounds"]  # "[x1,y1][x2,y2]"
    m = re.match(r"\[(\d+),(\d+)\]\[(\d+),(\d+)\]", b)
    x = (int(m.group(1)) + int(m.group(3))) // 2
    y = (int(m.group(2)) + int(m.group(4))) // 2
    return call("/a11y/tap", x=x, y=y)


def slugify(text, maxlen=40):
    s = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return (s[:maxlen].rstrip("-") or "gemini-video")


def newest_movie():
    """Return the newest mp4 filename in /sdcard/Movies."""
    r = call("/sh", cmd="ls -lt /sdcard/Movies/*.mp4 2>/dev/null | head -1")
    out = r.get("result") or ""
    m = re.search(r"(\d+)\s+\S+\s+\S+\s+\S+\s+\S+\s+([^\\n]+\.mp4)", out)
    if not m:
        return None
    return m.group(2).strip()


def save_video(prompt):
    """Tap the player -> Download Video -> rename the newest mp4."""
    d = dump()
    player = None
    for n in d.get("nodes", []):
        if "Pemutar Video" in (n.get("desc") or ""):
            player = n
            break
    if player:
        print("7) open player")
        print(tap_node(player))
        time.sleep(2)

    d = dump()
    dl = find_node(d, "Download Video")
    if not dl:
        print("WARN: Download Video button not found - skipping save")
        return
    print("8) download video")
    print(tap_node(dl))
    time.sleep(6)

    newest = newest_movie()
    if not newest:
        print("WARN: no mp4 found in /sdcard/Movies")
        return
    slug = slugify(prompt)
    dest = f"/sdcard/Movies/{slug}.mp4"
    print("9) rename ->", dest)
    print(call("/sh", cmd=f'mv "/sdcard/Movies/{newest}" "{dest}"'))
    print("SAVED:", dest)

def main():
    prompt = sys.argv[1] if len(sys.argv) > 1 else (
        "buatkan video lucu kucing terbang di langit jakarta 9:16"
    )

    print("1) open Gemini")
    print(call("/a11y/app", pkg=GEMINI_PKG))
    time.sleep(4)

    d = dump()
    print("   screen:", d.get("pkg"))

    # Gemini may reopen the last chat - go back to home until the chips are visible
    for _ in range(3):
        if find_node(d, "Buat video"):
            break
        print("2) not on home - pressing BACK")
        call("/key", k="4")
        time.sleep(2)
        d = dump()

    # Always scroll the chip list up so "Buat video" is fully visible above the input bar
    print("2) scroll chips up")
    print(call("/a11y/swipe", x1=540, y1=1500, x2=540, y2=1150))
    time.sleep(2)
    d = dump()

    chip = find_node(d, "Buat video")
    if not chip:
        print("ERR: 'Buat video' chip not found")
        return 1

    # The chip bounds are clipped by the input bar; after the scroll its real
    # center sits at ~67% of screen height. Try a few offsets until video mode is on.
    print("3) tap Buat video")
    in_video = False
    for y in (1557, 1520, 1600, 1480):
        print(call("/a11y/tap", x=239, y=y))
        time.sleep(2)
        d = dump()
        ts = texts(d)
        if any("Deskripsikan video" in t for t in ts):
            in_video = True
            break
        # video tool chip active in the toolbar also means video mode
        if find_node(d, "video") and any("Kirim" in (n.get("desc") or "") for n in d.get("nodes", [])):
            in_video = True
            break
    if not in_video:
        print("WARN: could not confirm video mode")

    print("4) type prompt")
    print(call("/a11y/type", value=prompt))
    time.sleep(1)

    d = dump()
    send = find_node(d, "Kirim") or find_node(d, "Send")
    if not send:
        print("ERR: send button not found")
        return 1

    print("5) send")
    print(tap_node(send))

    print("6) waiting for generation (max 3 min)")
    deadline = time.time() + 180
    while time.time() < deadline:
        time.sleep(20)
        d = dump()
        ts = texts(d)
        if any(t.strip() == "Video Anda sudah siap!" for t in ts):
            print("DONE: video ready")
            save_video(prompt)
            shot = call("/screen")
            if shot.get("png_b64"):
                with open("gemini_video.png", "wb") as f:
                    f.write(base64.b64decode(shot["png_b64"]))
                print("screenshot saved: gemini_video.png")
            return 0
        if any("Membuat video" in t for t in ts):
            print("   still generating...")
        if any("batas Anda direset" in t for t in ts):
            print("LIMIT: Gemini video quota exhausted - try again after the reset")
            return 2
    print("TIMEOUT: video not ready after 3 minutes")
    return 1


if __name__ == "__main__":
    sys.exit(main())
