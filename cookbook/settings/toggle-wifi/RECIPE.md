# Toggle Wi-Fi and verify

**Goal:** Turn Wi-Fi on or off and verify the resulting state.

## Prerequisites

- None (works on any Android 11+ device)

## Steps

1. `shell` — `svc wifi disable` (or `enable`)
2. `shell` — `settings get global wifi_on`
3. Verify: `0` = off, `1` = on
4. Report the previous and new state

## Prompt

See [prompt.md](prompt.md).

## Failure modes

| Symptom | Recovery |
|---|---|
| `svc wifi` permission denied | Use the a11y engine: open Settings → Network → Wi-Fi toggle |
| State unchanged | Retry once; some OEMs delay the setting by ~2 s |
| Device on Wi-Fi only | Warn before disabling — the tunnel may drop |
