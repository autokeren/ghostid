# Prompt — Upload a video to TikTok

You are operating an Android phone through Ghostid.

Goal: upload a specific local video to TikTok with this caption and publish it:

"""
<CAPTION — plain text, keep emojis minimal>
"""

Video file: `<FILE PATH, e.g. /sdcard/Movies/my-video.mp4>`

Rules:
- **Verify the selected video via `screenshot` before tapping "Berikutnya".**
  If the cover does not match the expected content, go back and use the share-sheet flow.
- If the keyboard is open and a button is hidden, press BACK once first.
- Do not tap "Draf" (Draft) — the goal is to publish.

Recommended steps (direct share — no chooser):
1. `shell`: `am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d file://<FILE PATH>`
2. `shell`: `content query --uri content://media/external/video/media --projection _id:_display_name --where "_display_name LIKE '%<FILENAME>%'"`
   → note the `_id`
3. `shell`: `am start -a android.intent.action.SEND -t video/mp4 --eu android.intent.extra.STREAM content://media/external/video/media/<id> -n com.ss.android.ugc.trill/com.ss.android.ugc.aweme.share.SystemShareActivity -f 0x1`
4. TikTok editor opens with that exact video → get "Berikutnya" bounds from a
   fresh `uiautomator dump` and tap its center (never guess coordinates
   from a screenshot — screenshots are scaled).
5. Caption screen: tap "Tambah deskripsi...", then
   `GET /a11y/type?value=<CAPTION>&find=<first-word-in-field>` (full replace),
   BACK, tap "Posting".
6. Dismiss "Nanti saja" / "Lain kali" popups if they appear.
7. Wait 10-15 s, then `screenshot` and report the visible feed/profile state.

Fallback steps (in-app gallery):
1. `open_app` with package `com.ss.android.ugc.trill`.
2. Tap the "+" button, then the gallery thumbnail.
3. Select the video and **verify the cover with `screenshot`**.
4. "Berikutnya" → "Berikutnya" → caption → BACK → "Posting".
