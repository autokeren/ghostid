# Ghostid MCP Tools

Full reference for the 26 tools exposed by Ghostid at `POST /mcp` (and as REST endpoints).

Base URL: the tunnel URL shown in the app, e.g. `https://your-tunnel.trycloudflare.com`
Auth: `Authorization: Bearer <token>` — the token is shown in the Ghostid app.

## Discovery

| Endpoint | Description |
|---|---|
| `GET /status` | Health check (no auth) |
| `GET /skill.md` | Agent skill document |
| `GET /tools.json` | Machine-readable tool catalog |
| `GET /openapi.json` | OpenAPI 3.0 spec |

## Core tools

| Tool | Params | Description |
|---|---|---|
| `screenshot` | — | PNG screenshot of the screen |
| `ui_dump` | — | uiautomator XML: text, content-desc, bounds |
| `tap` | `x`, `y` | Tap coordinates |
| `swipe` | `x1`, `y1`, `x2`, `y2`, `ms` | Swipe gesture |
| `type_text` | `text` | Type into the focused field |
| `keyevent` | `key` | 3=HOME, 4=BACK, 66=ENTER, 82=MENU |
| `open_app` | `package` | Launch app by package name |
| `tap_text` | `text`, `exact` | Find element by text/desc and tap |
| `wait_text` | `text`, `timeout`, `exact` | Wait until text appears |
| `uncast` | — | Kill Samsung Flow/Smart View overlay |
| `shell` | `command` | Raw ADB shell command |

## Accessibility engine

The a11y engine works even when touch injection is blocked by overlays.

| Tool | Params | Description |
|---|---|---|
| `a11y_dump` | — | Dump UI tree via accessibility (all windows) |
| `a11y_click` | `text`, `index`, `exact` | Click node by text/desc |
| `a11y_clickat` | `x`, `y` | Accessibility click at coordinates |
| `a11y_type` | `text` | Set text via accessibility |
| `a11y_scroll` | `direction` | Scroll forward/backward |
| `a11y_scrolldown` | `text` | Scroll until text is found |
| `a11y_scrolllist` | — | Scroll list containers |
| `a11y_swipe` | `x1`, `y1`, `x2`, `y2` | Gesture via accessibility |
| `a11y_tap` | `x`, `y` | Gesture tap |
| `a11y_app` | `package` | Launch app |
| `a11y_intent` | `intent` | Fire an intent |
| `a11y_findtext` | `text` | Find text node |
| `a11y_clickid` | `id` | Click by resource-id |
| `a11y_debugall` | — | Dump all windows (debugging) |
| `a11y_xsearch` | `query` | Cross-window search |

## Files, media and device

| Endpoint | Params | Description |
|---|---|---|
| `GET /file/get` | `path` | Read a file (base64, up to ~9 MB) |
| `POST /file/put` | `path`, body=base64 | Write a file (up to ~9 MB) |
| `GET /file/fetch` | `url`, `path` | Download a URL directly on the phone |
| `GET /file/list` | `path` | Directory listing |
| `GET /file/rm` | `path` | Delete a file |
| `GET /screenrecord` | `action=start|stop`, `seconds`, `kbps` | Screen recording (start returns immediately; stop returns the mp4 base64) |
| `GET /clipboard` | `action=get|set`, `text` | Read/write the clipboard |
| `GET /unlock` | � | Unlock the lock screen with the stored Agent PIN (never leaves the device) |
| `GET /unlock/status` | � | Whether an Agent PIN is configured |
| `GET /a11y/longpress` | `x`, `y`, `ms` | Long-press gesture |
| `GET /a11y/pinch` | `in=1|0`, `x`, `y`, `spread` | Pinch zoom in/out |

> Large downloads: use `/file/fetch` (phone downloads the URL itself) instead of `/file/put`
> (the ADB shell command line cannot carry multi-MB base64 payloads).

## App endpoints

| Endpoint | Description |
|---|---|
| `GET /tunnel?action=start` | Start the Cloudflare tunnel |
| `GET /tunnel?action=stop` | Stop the tunnel |
| `GET /quota` | Current usage and daily limit |
| `GET /license?key=…` | Install a Pro license key |
| `GET /pair?code=…` | Pair Wireless Debugging (SPAKE2) |
| `GET /connect` | Connect Wireless Debugging (TLS, auto mDNS) |
| `GET /mdns` | Discover wireless debugging services |
