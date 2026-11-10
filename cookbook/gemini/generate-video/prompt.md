# Prompt — Generate a video with Gemini

You are operating an Android phone through Ghostid.

Goal: generate a short video in the Gemini app from this prompt:

"""
<PROMPT — include style + subject + setting + aspect ratio, e.g.:
"buatkan video lucu kucing terbang di langit jakarta 9:16">
"""

Rules:
- Gemini is a Compose app: use `shell: uiautomator dump` + `input tap`, NOT the in-app
  a11y dump (it can return stale bounds).
- Verify every step with a fresh dump before continuing.
- Stop and report if you see any quota/limit message.

Steps:
1. `open_app` with package `com.google.android.apps.bard`.
2. Dump: `sh: uiautomator dump /sdcard/g.xml` then `GET /file/get?path=/sdcard/g.xml`.
3. If "Buat video" is not fully visible: `sh: input swipe 540 1500 540 1200 300`, dump again.
4. Tap the "Buat video" chip (`sh: input tap <cx> <cy>`).
5. Dump → confirm the placeholder is "Deskripsikan video Anda".
6. Tap the input, `type_text` the prompt above.
7. Tap "Kirim".
8. Poll a fresh dump every 20-30 s until "Video Anda sudah siap!" appears.
9. Save: scroll if needed, tap "Opsi lainnya" → "Simpan video".
10. `sh: ls -lt /sdcard/Movies | head -3` → rename the newest mp4 to a slug.
11. Take a `screenshot` and report success with the saved file path.
