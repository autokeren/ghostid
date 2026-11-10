# Generate a video with Gemini

**Goal:** Ask Gemini to generate a short video from a text prompt, save it with a readable name, then verify the result.

## Prerequisites

- Gemini app installed and signed in (`com.google.android.apps.bard`)
- Google account with video generation access (Pro/One)
- Accessibility engine ON (Ghostid) — needed for `type_text`

## Steps (verified flow)

> **Why shell commands?** Gemini is a Compose app: the in-app `a11y_dump` can return
> STALE trees (wrong bounds). `uiautomator dump` via the shell is always fresh, and
> `input tap` injects at the system level. Use them for Gemini.

1. `open_app` — `com.google.android.apps.bard`
2. Fresh dump: `sh: uiautomator dump /sdcard/g.xml` → `GET /file/get?path=/sdcard/g.xml`
3. If **"Buat video"** is not fully visible, scroll the chips:
   `sh: input swipe 540 1500 540 1200 300` → dump again
4. `sh: input tap <chip center>` (the chip sits just above the input bar)
5. Dump again → confirm the placeholder is **"Deskripsikan video Anda"**
6. Tap the input, then `a11y_type` the prompt (include the aspect ratio, e.g. `9:16`)
7. Tap **"Kirim"** (send, bottom-right)
8. Wait 30-60 s → dump until "Membuat video Anda" appears
9. Wait 60-120 s → dump until **"Video Anda sudah siap!"** appears
10. Save it (next section)
11. `screenshot` — capture the result for the user

## Saving the video to a named file

After **"Video Anda sudah siap!"**:

1. If the action buttons are below the fold:
   `sh: input swipe 540 1400 540 700 300`
2. Dump → find `content-desc="Opsi lainnya"` → `sh: input tap <cx> <cy>`
3. Dump → find `text="Simpan video"` → tap it
4. Wait 3-5 s → `sh: ls -lt /sdcard/Movies | head -3` — the newest `*.mp4` is the download
5. Rename: `sh: mv "/sdcard/Movies/<timestamp>.mp4" "/sdcard/Movies/<slug>.mp4"`

## Prompt

See [prompt.md](prompt.md).

## Failure modes

| Symptom | Recovery |
|---|---|
| "Buat video" chip not visible | Swipe the chips list up ~300 px; the chip sits just above the input bar |
| Placeholder still "Minta Gemini" | The chip tap missed — dump again and re-tap the exact bounds |
| Quota message ("batas Anda direset") | Daily video quota exhausted — stop; retry after the reset |
| Still "Membuat video" after 3 min | Wait another minute; if still stuck, report |
| "Video Anda sudah siap!" but no player | Scroll up in the chat to reveal the video player |
| Opsi lainnya menu won't open | Ensure the buttons row is visible (scroll), then tap the exact dump bounds |

## Tested on

- Samsung Galaxy S22 Ultra (SM-S908E, Android 16)
- Tested via Cloudflare tunnel only (no USB)
