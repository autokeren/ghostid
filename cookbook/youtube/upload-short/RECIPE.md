# Upload a YouTube Short

**Goal:** Publish a local video as a YouTube Short from the phone.

## Prerequisites

- YouTube app installed and signed in
- The video file is in the gallery (recorded or downloaded)

## Steps

1. `open_app` — `com.google.android.youtube`
2. `wait_text` — `Home` (verify launch)
3. `tap_text` — `+` (Create)
4. `tap_text` — `Upload a video`
5. `tap_text` — `Shorts` / select the video thumbnail
6. `tap_text` — `Next` (details)
7. `type_text` — title
8. `tap_text` — `Next` (visibility)
9. `tap_text` — `Public`
10. `tap_text` — `Upload Short`
11. `wait_text` — `Uploading` → `Published` (verify)

## Prompt

See [prompt.md](prompt.md).

## Failure modes

| Symptom | Recovery |
|---|---|
| Create button not found | `ui_dump` and tap the FAB by bounds |
| Video picker empty | Video not indexed — open the gallery once, retry |
| Upload stuck | Check Wi-Fi; `ui_dump` for "Waiting for network" |
| Daily upload limit | YouTube shows a banner — stop and report |
