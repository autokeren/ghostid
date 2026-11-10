# Read and summarize notifications

**Goal:** Read the notification shade and summarize what needs attention.

## Prerequisites

- Notification access granted to the agent's shell (default for `dumpsys`)

## Steps

1. `shell` — `dumpsys notification --noredact`
2. Parse `NotificationRecord` entries: package, title, text
3. Summarize: app → one-line summary, sorted by priority
4. Report actionable items only (skip ongoing/media notifications)

## Prompt

See [prompt.md](prompt.md).

## Failure modes

| Symptom | Recovery |
|---|---|
| Empty output | Open the shade first: `shell` with `cmd statusbar expand-notifications` |
| Redacted text | Some apps hide content — report "content hidden" |
| Too many entries | Summarize the newest 10 only |
