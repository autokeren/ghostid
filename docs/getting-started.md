# Getting started with Ghostid — the honest guide

*Written by a user, for users. I set this up on a Galaxy S22 Ultra and a Z Fold5, hit every wall, and wrote down everything I wish someone had told me first.*

---

## What you need

- An Android phone (Android 11+, API 30+)
- **Wi-Fi** (yes, really — even if your phone has mobile data)
- Ghostid installed — [Google Play](https://play.google.com/store/apps/details?id=com.autokeren.ghostid)
- An AI agent that speaks MCP (Claude Desktop, Cursor, or your own)

---

## Step 1 — Install and start the tunnel

1. Install Ghostid.
2. Open it. You'll see a **status card** (Device, Server, ADB, Tunnel, License, Quota, Screens, A11y engine).
3. Tap **Start Tunnel**. Wait ~10 seconds.
4. The **Public URL** card fills in with something like
   `https://YOUR-TUNNEL.trycloudflare.com`.
5. Copy the URL and the **Token** below it.

> ⚠️ The URL **changes every time the tunnel restarts**. If your agent suddenly can't connect, copy the new URL.

## Step 2 — Connect your agent

Point your MCP client at the tunnel:

```json
{
  "mcpServers": {
    "ghostid": {
      "type": "http",
      "url": "https://YOUR-TUNNEL.trycloudflare.com/mcp",
      "headers": { "Authorization": "Bearer YOUR-TOKEN" }
    }
  }
}
```

Ask your agent: *"Take a screenshot and tell me what's on screen."* If it answers, you're in.

---

## Step 3 — Enable Accessibility (2 taps)

This is what lets your agent **read the screen and tap**.

1. In Ghostid, tap **Accessibility**.
2. Read the disclosure — it explains exactly what the service does and that screen data goes only to *your* agent.
3. Tap **Open Settings**.
4. In Settings → Accessibility → Installed apps → **Ghostid** → toggle **ON**.

The status card now shows `A11y engine: On`.

> 🔒 Samsung tip: Android hides the USB/Wireless debugging toggles from the accessibility tree on purpose. That means your *agent* cannot flip them — you have to. That's a security feature, not a bug.

## Step 4 — Enable Screenshots (1 system prompt)

This lets your agent **see** the screen without ADB.

1. Tap **Screenshots**.
2. A pre-dialog explains the next screen. Tap **Continue**.
3. The Android dialog appears. **This is the part everyone gets stuck on:**
   - Tap **"Share one app"** (it's a row, not a button — tapping it reveals the options)
   - Choose **"Share entire screen"**
   - Tap **"Share screen"**
4. Status card: `Screens: On`.

> ⚠️ The permission dies when the app process restarts (reboot, force-stop, update). Just tap **Screenshots** again.

---

## Step 5 — Optional: ADB wireless (power users)

ADB gives you shell, file access, and app control. It needs **Developer options** + **Wireless debugging**. This is the part that trips everyone up, so follow it exactly:

### 5a. Turn on Developer options
1. Settings → About phone
2. Tap **Build number** 7 times
3. Enter your PIN

### 5b. Turn on Wireless debugging
1. Settings → Developer options → **Wireless debugging** (tap the row, not the toggle)
2. Toggle **Wireless debugging ON**
3. A prompt appears: **"Allow wireless debugging on this device?"** → check **"Always allow on this network"** → tap **Allow**

> ⚠️ **Wi-Fi must be connected.** If Wi-Fi is off, the page says `Unavailable (Not allowed)` and every pairing row is disabled. Connect Wi-Fi first.
>
> ⚠️ **If you just connected Wi-Fi**, the page can be stale. Toggle Wireless debugging **off and on** to refresh it.

### 5c. Get the pairing code
1. On the Wireless debugging page, **scroll down**
2. Below "IP address & Port" you'll find **"Pair device with pairing code"** (subtitle: *six-digit code*)
3. Tap it — Android shows a **6-digit code** and an IP:port

> ⚠️ **Keep this dialog open.** The pairing service only runs while it's visible.

### 5d. Pair in Ghostid
1. Open Ghostid → tap **Pair ADB**
2. Type the 6-digit code
3. If auto-discovery fails, also enter the **port** from the dialog (e.g. `38851`) — mDNS can be blocked on some devices
4. Tap **Pair**

Ghostid pairs and connects. Status card: `ADB: Connected`.

> 💡 Pairing is stored forever. You only do this once per phone.

### 5e. Faster path (optional, USB once)
If you have a USB cable, `adb tcpip 5555` from a PC enables the legacy port permanently.
Ghostid can then connect to `127.0.0.1:5555` — no pairing code needed. (This is what the
cookbook demos use.)

---

## Step 6 — The rest of the toolbox

| Button | What it does |
|---|---|
| **Screenshots** | MediaProjection capture (no ADB) |
| **Unlock PIN** | Store your lock-screen PIN encrypted so the agent can unlock (see below) |
| **Pair ADB** | Wireless debugging pairing |
| **Accessibility** | The a11y engine toggle |

### Agent Unlock PIN

1. Tap **Unlock PIN** → type your lock-screen PIN → **Save**
2. The PIN is encrypted with the Android Keystore — **it never leaves the phone**
3. Your agent calls `GET /unlock` → the app unlocks the screen itself
4. Remove it anytime with **Clear**

### Files, screen recording, clipboard

These work through the API (see [docs/mcp-tools.md](mcp-tools.md)):

- `GET /file/fetch?url=...&path=...` — download a URL directly on the phone
- `GET /file/get?path=...` / `POST /file/put?path=...` — read/write files
- `GET /screenrecord?action=start&seconds=15` → `action=stop` — screen recording
- `GET /clipboard?action=get|set&text=...` — clipboard
- `GET /a11y/longpress` / `GET /a11y/pinch` — extra gestures

---

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `ADB: Not connected` | Wireless debugging off or Wi-Fi off | Enable Wi-Fi, then Wireless debugging |
| Wireless debugging page says `Unavailable (Not allowed)` | Wi-Fi disconnected or page stale | Connect Wi-Fi, toggle Wireless debugging off/on |
| Pairing rows greyed out | Wi-Fi just connected / stale page | Toggle Wireless debugging off/on |
| No "Pair device with pairing code" row | You're not scrolled down | Scroll below "IP address & Port" |
| Pair fails | Pairing dialog closed too early | Keep the 6-digit dialog open while pairing |
| Screenshot returns black | Projection died (app restart) | Tap Screenshots → grant again |
| Agent can't tap Settings items | Samsung hides developer toggles from a11y | Tap those yourself |
| Agent can't connect | Tunnel URL changed | Copy the new URL from the app |
| Agent's taps land on the wrong element in Gemini/TikTok | Compose apps return stale a11y trees | Use `uiautomator dump` + `input tap` (see cookbook) |

## FAQ

**Do I need a cable?**
No. Everything above is wireless. (A cable is only useful for sideloading the APK.)

**Do I need root?**
No.

**Does my data go to Ghostid servers?**
No. Screen data goes only to the agent *you* connect, over your own tunnel. Ghostid never receives it.

**Why does the tunnel URL change?**
It's an ephemeral Cloudflare quick tunnel. Copy the new URL after each restart.

**Why can't my agent flip the Wireless debugging toggle?**
Android hides developer options from accessibility on purpose. You tap those; your agent does everything after.

**Does the free tier work?**
Yes — 1,000 calls/day, all tools. Pro (100,000/day) is in the Google Play version.

**Tested on**
- Samsung Galaxy S22 Ultra (SM-S908E, Android 16)
- Samsung Galaxy Z Fold5 (SM-F946B, Android 16)

*Got a device that behaves differently? Open an issue with your model + Android version.*
