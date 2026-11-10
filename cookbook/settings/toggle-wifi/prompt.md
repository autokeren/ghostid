# Prompt — Toggle Wi-Fi and verify

You are operating an Android phone through Ghostid.

Goal: turn Wi-Fi <on|off> and report the verified result.

Rules:
- Always read the state before and after.
- If the tunnel is Wi-Fi-dependent, warn before disabling.

Steps:
1. `shell` with `settings get global wifi_on` — record the previous state.
2. `shell` with `svc wifi <enable|disable>`.
3. Wait 2 seconds.
4. `shell` with `settings get global wifi_on` — record the new state.
5. Report: previous → new (0 = off, 1 = on).
