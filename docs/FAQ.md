# FAQ

## General

**What is Ghostid?**
An Android app that turns your phone into a remotely controllable device for AI agents. Your agent connects over a Cloudflare tunnel and gets tools to see the screen, tap, type, scroll, launch apps, and (optionally) run shell commands.

**Do I need a PC?**
No. The phone is the server. You only need a PC to sideload the APK if you can't use Google Play.

**Do I need root?**
No.

**Which Android versions?**
Android 11+ (API 30+). Tested on Android 16.

## Privacy

**Does Ghostid see my screen?**
No. Screen data goes only to the agent you connect, over your own tunnel. Ghostid servers never receive it.

**What does the accessibility service do?**
It lets your agent read the screen content and perform taps/typing. Ghostid shows a disclosure before enabling it and explains this in plain language.

**Can I revoke access?**
Yes — turn off Accessibility in Settings, stop the tunnel, or rotate the token in the app.

## Setup

**The tunnel URL keeps changing — why?**
It's an ephemeral Cloudflare quick tunnel. Copy the new URL after each restart.

**Why is "Wireless debugging" greyed out?**
Wi-Fi must be connected. If Wi-Fi is on and the page is still stale, toggle Wireless debugging off/on.

**Where is the pairing code?**
Wireless debugging page → scroll below "IP address & Port" → "Pair device with pairing code". Keep that dialog open while pairing.

**Why can't my agent tap the Wireless debugging toggle?**
Android hides developer options from the accessibility tree on purpose (anti-malware). You tap those yourself; your agent handles everything else.

**Screenshots stopped working**
The MediaProjection permission dies when the app process restarts. Tap Screenshots again.

## Tools

**What can my agent do?**
26 tools: screenshot, UI dump, tap, swipe, type, keyevent, open app, tap/wait by text, shell, plus the accessibility engine (dump, click, type, scroll, gestures, intents).

**Do the tools work without ADB?**
Most do: accessibility engine (read/tap/type/scroll), app launch, screenshots (via MediaProjection). ADB adds shell and file-level access.

## Pricing

**Is it free?**
Yes — 1,000 calls/day with all tools. Pro (in-app) raises the limit to 100,000/day.
