# Ghostid Discord bot

A Cloudflare Worker that powers the Ghostid community server.

## What it does

| Command | Description |
|---|---|
| `/faq <topic>` | Search `docs/FAQ.md` |
| `/recipe <slug>` | Show a cookbook recipe (e.g. `tiktok/upload-video`) |
| `/docs` | Links to the docs |
| `/role <name>` | Assign User / Dev / Contributor |

Plus a **cron feed**: every 6 hours it checks the cookbook and posts new recipes to a
Discord webhook channel (#recipes).

> No gateway needed — the bot is pure HTTP interactions, so it runs on the Cloudflare
> free tier. A 24/7 "online" bot needs a small VPS (gateway), but nothing here requires it.

## Setup (10 minutes)

### 1. Create the Discord app

1. https://discord.com/developers/applications → **New Application** → name it `Ghostid`
2. **General Information** → copy **Application ID** and **Public Key**
3. **Bot** → **Reset Token** → copy the **bot token** (keep it secret)

### 2. Invite the bot

**OAuth2 → URL Generator** → scopes: `bot` + `applications.commands`
Permissions: `Manage Roles`, `Send Messages`, `Embed Links`
Open the generated URL and add it to your server.

### 3. Create the channels

```
#welcome        (welcome text + how to use /role)
#announcements  (release updates)
#recipes        (bot feed — create a webhook here: Channel settings → Integrations → Webhooks)
#showcase       (users post their cooking results)
#help           (FAQ + support)
#dev            (technical discussion)
```

Create the roles **User**, **Dev**, **Contributor** (server settings → Roles).

### 4. Deploy the Worker

```bash
cd community/discord-bot
npm install -g wrangler        # if needed
wrangler login

wrangler deploy

wrangler secret put DISCORD_PUBLIC_KEY
wrangler secret put DISCORD_BOT_TOKEN
wrangler secret put DISCORD_APP_ID
wrangler secret put DISCORD_GUILD_ID
wrangler secret put RECIPES_WEBHOOK   # the #recipes webhook URL
```

### 5. Point Discord at the Worker

1. Copy the Worker URL (e.g. `https://ghostid-discord-bot.xxx.workers.dev`)
2. Discord → **General Information → Interactions Endpoint URL** → paste → **Save**
   (Discord sends a PING; the Worker verifies the signature and answers automatically)

### 6. Register the commands

```bash
set DISCORD_APP_ID=...
set DISCORD_BOT_TOKEN=...
set DISCORD_GUILD_ID=...
node register-commands.js
```

Done — try `/faq pairing` in your server.

## Optional: KV for the recipe feed state

Without KV the feed re-posts the latest recipes every run. To track what was already
posted:

```bash
wrangler kv namespace create STATE
# add the returned id to wrangler.json → kv_namespaces
```

## Community playbook

- **#showcase** — ask users to post their cooked recipes (video/screenshot + the prompt).
  Repost the best ones to X/TikTok with credit.
- **#recipes** — the cron feed keeps the channel alive without manual posting.
- **#help** — the `/faq` command answers the top questions (pairing, screenshots, privacy).
- **Onboarding** — pin a message in #welcome: install → tunnel → `/role user`.
