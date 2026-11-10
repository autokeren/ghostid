# Post a tweet on X

**Goal:** Publish a text post on X from the phone.

## Prerequisites

- X app installed and signed in
- Network available

## Steps

1. `open_app` — `com.twitter.android`
2. `wait_text` — `Home`
3. `tap_text` — compose FAB (`+`)
4. `type_text` — the tweet text
5. `ui_dump` — verify the text landed
6. `tap_text` — `Post`
7. `wait_text` — `Your post was sent` (verify)

## Prompt

See [prompt.md](prompt.md).

## Failure modes

| Symptom | Recovery |
|---|---|
| Compose FAB not found | `ui_dump`, tap the floating button by bounds |
| Text truncated | X limit reached — split the text |
| Draft dialog appears | Tap "Discard" only if intended; else stop |
