# Features

Everything Ghostid can do, and which engine makes it work.

## Engines

| Engine | Setup | What it gives you |
|---|---|---|
| **Accessibility** | 2 taps (disclosure → Settings) | Read the UI tree, tap, type, scroll, gestures, launch apps, intents |
| **ADB (wireless)** | Developer options + pairing code | Everything above + raw shell, files, app control, `dumpsys` |
| **MediaProjection** | 1 system prompt | Screenshots (no ADB needed) |

Most agents only need the Accessibility + MediaProjection engines. ADB is for power users.

## Tools (26)

### Screen & UI

| Tool | Engine | What it does |
|---|---|---|
| `screenshot` | MediaProjection / ADB | PNG of the screen |
| `ui_dump` | ADB | uiautomator XML tree |
| `a11y_dump` | Accessibility | UI tree from all windows (richer on some apps) |
| `a11y_xsearch` | Accessibility | Cross-window text search |
| `a11y_debugall` | Accessibility | Dump every window (debugging) |

### Interaction

| Tool | Engine | What it does |
|---|---|---|
| `tap` / `swipe` | ADB | Touch injection |
| `a11y_tap` / `a11y_swipe` | Accessibility | Gesture-based touch (works when overlays block ADB) |
| `a11y_click` | Accessibility | Click a node by text/desc |
| `a11y_clickat` | Accessibility | Click at coordinates via a11y |
| `a11y_longpress` | Accessibility | Long-press (600 ms+) |
| `a11y_pinch` | Accessibility | Two-finger pinch in/out |
| `a11y_scroll` / `a11y_scrolldown` / `a11y_scrolllist` | Accessibility | Scrolling variants |
| `type_text` / `a11y_type` | ADB / Accessibility | Type into the focused field |
| `keyevent` | ADB | HOME, BACK, ENTER, MENU… |

### Apps

| Tool | Engine | What it does |
|---|---|---|
| `open_app` / `a11y_app` | Accessibility | Launch by package name |
| `a11y_intent` | Accessibility | Fire an ACTION_VIEW intent (deep links) |
| `tap_text` / `wait_text` | ADB | Find/tap/wait by text |
| `uncast` | ADB | Kill Samsung Flow/Smart View overlays |

### Files & media

| Tool | Engine | What it does |
|---|---|---|
| `file_get` | ADB | Read a file (base64, up to ~9 MB) |
| `file_put` | ADB | Write a file (base64) |
| `file_fetch` | App | Download a URL directly on the phone |
| `file_list` / `file_rm` | ADB | List / delete |
| `screenrecord` | ADB | Record the screen (start → stop returns mp4) |
| `clipboard` | App | Read/write the clipboard |

### Device

| Tool | Engine | What it does |
|---|---|---|
| `unlock` | App + Accessibility | Unlock with the stored Agent PIN (encrypted, never leaves the device) |
| `shell` | ADB | Raw shell command |

## Security model

- Every request needs the **bearer token** shown in the app (rotate anytime)
- The tunnel is public but unauthenticated requests are rejected
- The **Agent PIN** is stored with AES-GCM in the Android Keystore — the agent never sees it
- Screen data goes only to the agent *you* connect — never to Ghostid servers

## Limits

| Tier | Calls per day |
|---|---|
| Free (all builds) | 1,000 |
| Pro (Google Play) | 100,000 |

The quota resets daily using server time (synced from `ghostid-api.autokeren.com`).
