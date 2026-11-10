# Upload a video to TikTok

**Goal:** Upload a local video file to TikTok with a caption and publish it.

## Prerequisites

- TikTok installed and signed in (`com.ss.android.ugc.trill`)
- The video file exists on the phone (e.g. `/sdcard/Movies/<name>.mp4`)
- Accessibility engine ON (Ghostid)

## Recommended flow — direct share (most reliable)

This path targets a **specific file** and skips the system share sheet
entirely, so you can never tap the wrong target.

1. If the file was downloaded remotely, fetch it on the phone:
   `GET /file/fetch?url=<https-url>&path=/sdcard/Movies/<name>.mp4`
2. Index it in MediaStore (otherwise the share target can't read it):
   `sh: am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d file:///sdcard/Movies/<name>.mp4`
3. Get the media id:
   `sh: content query --uri content://media/external/video/media --projection _id:_display_name --where "_display_name LIKE '%<name>%'"`
4. Fire ACTION_SEND **directly** at TikTok's share activity (no chooser):
   `sh: am start -a android.intent.action.SEND -t video/mp4 --eu android.intent.extra.STREAM content://media/external/video/media/<id> -n com.ss.android.ugc.trill/com.ss.android.ugc.aweme.share.SystemShareActivity -f 0x1`
   (find this component with `dumpsys package <tiktok-pkg> | grep -A2 'android.intent.action.SEND:'` if TikTok ever renames it)
5. TikTok opens in the editor with that video → tap **"Berikutnya"**.
6. On the caption screen: tap **"Tambah deskripsi..."**, then set the
   caption with `GET /a11y/type?value=<caption>&find=<first-word-of-field>`
   (full-field replace — avoids the `input text` `%23` double-encoding trap
   for `#`), press BACK to close the keyboard, then tap **"Posting"**.
7. Wait 10-15 s — the app returns to the feed.
8. Dismiss the popups: **"Nanti saja"** (link email) and **"Lain kali"**
   (notifications).
9. Verify in the profile grid (video tab) that the new post appears.

## Alternative flow — in-app gallery

Faster, but you must verify the selected video (the gallery sorts by date added).

1. `a11y_app` — `com.ss.android.ugc.trill`
2. If the app opens on the feed, tap the **"+"** (create) button.
3. On the camera screen, tap the **gallery thumbnail** (right of the shutter).
4. Select the video — **verify the cover via `screenshot` before continuing**.
5. Tap **"Berikutnya"** (preview) → **"Berikutnya"** (editor).
6. Caption → BACK → **"Posting"**.

## Prompt

See [prompt.md](prompt.md).

## Failure modes

| Symptom | Recovery |
|---|---|
| Wrong video selected | The gallery's first item is not always the target. Verify the cover via `screenshot`; if wrong, go back and use the share-sheet flow |
| File not in gallery/share sheet | MediaStore not indexed — run the MEDIA_SCANNER_SCAN_FILE broadcast |
| "Dipilih 1" stuck in the picker | Exit the picker, use the share-sheet flow instead |
| "Berikutnya" does nothing | Keyboard may be open — press BACK once, re-tap |
| Caption emojis garbled | The a11y `set-text` path can mangle emoji — use plain text |
| Caption shows literal `%23` | You double-encoded `#` through `input text` — use `/a11y/type?value=` instead |
| Taps land but nothing happens | You guessed coordinates from a screenshot — screenshots are scaled. Always take tap coordinates from a fresh `uiautomator dump` bounds |
| Screen black / Smart View idle | Screen timed out mid-run — wake it (`input keyevent KEYCODE_WAKEUP`), keep the screen-on timeout long while automating |
| Post button hidden by keyboard | Press BACK to close the keyboard, then tap "Posting" |
| Upload stuck | Check network; wait 30 s; if still stuck, report |

## Tested on

- Samsung Galaxy S22 Ultra (SM-S908E, Android 16)
- Tested via Cloudflare tunnel only (no USB)
