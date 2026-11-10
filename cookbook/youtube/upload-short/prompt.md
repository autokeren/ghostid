# Prompt — Upload a YouTube Short

You are operating an Android phone through Ghostid.

Goal: publish a local video as a YouTube Short titled "<TITLE>".

Rules:
- Verify every step with `wait_text` or `ui_dump` before continuing.
- If an element is missing, `ui_dump` and tap by bounds instead of guessing.
- Stop and report if you see any account, monetization or policy warning.

Steps:
1. `open_app` with package `com.google.android.youtube`.
2. `wait_text` for "Home" to confirm the app is open.
3. Tap the Create button ("+" or "Create").
4. Tap "Upload a video".
5. Select the first video thumbnail, then tap "Next".
6. `type_text` the title: "<TITLE>".
7. Tap "Next", select "Public", then tap "Upload Short".
8. `wait_text` for "Uploading", then for "Published" (or "Public").
9. Take a `screenshot` and report the final state.
