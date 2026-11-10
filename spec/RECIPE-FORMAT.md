# Recipe Format

A recipe is the smallest reusable unit of agent behavior: **an intent, a tool sequence, and a prompt that works**.

Recipes live in `cookbook/<app>/<action>/` and follow this structure:

```
cookbook/
└── youtube/
    └── upload-short/
        ├── RECIPE.md      # human-readable: goal, steps, failure modes
        ├── recipe.yaml    # machine-readable: metadata + tool list
        └── prompt.md      # copy-paste prompt for the agent
```

## Slug rules

- `<app>/<action>` — lowercase, hyphenated
- `<app>` = the target app or surface: `youtube`, `x`, `whatsapp`, `settings`, `screen`, `camera`
- `<action>` = what the agent accomplishes: `upload-short`, `post-tweet`, `toggle-wifi`

## recipe.yaml

```yaml
slug: youtube/upload-short
title: Upload a YouTube Short
goal: Publish a local video as a YouTube Short from the phone.
difficulty: medium            # easy | medium | hard
time: 2-4 min                 # typical wall time
tools:                        # Ghostid MCP tools used, in order
  - open_app
  - ui_dump
  - tap_text
  - type_text
  - wait_text
requires:                     # environment assumptions
  - YouTube app installed and signed in
tested_on:
  - Samsung Galaxy S22 Ultra (Android 16)
```

## RECIPE.md

Must contain, in order:

1. **Goal** — one sentence
2. **Prerequisites** — apps, accounts, permissions
3. **Steps** — numbered, each naming the tool used
4. **Prompt** — the exact prompt that works
5. **Failure modes** — what breaks and how the agent recovers

## prompt.md

The prompt must be:

- **Self-contained** — assume the agent sees only this file
- **Imperative** — "Open the YouTube app", not "You could open…"
- **Verification-first** — every mutation ends with a `ui_dump`/`wait_text` check
- **Bounded** — state the success condition explicitly

## Compatibility

Recipes are tested against the listed device. Android UI varies across OEMs — if a recipe fails, open an issue with your device, Android version, and the failing step.
