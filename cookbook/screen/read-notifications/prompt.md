# Prompt — Read and summarize notifications

You are operating an Android phone through Ghostid.

Goal: summarize the phone's notifications.

Rules:
- Skip ongoing/media/foreground-service notifications.
- Keep each item to one line: "App — what happened".
- Do not act on anything; read-only.

Steps:
1. `shell` with `cmd statusbar expand-notifications` (open the shade).
2. `shell` with `dumpsys notification --noredact`.
3. Extract `NotificationRecord` entries: package name, title, text.
4. Summarize the newest 10 actionable items, grouped by app.
5. `shell` with `cmd statusbar collapse` (close the shade).
6. Report the summary.
