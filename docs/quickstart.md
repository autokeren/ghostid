# Quickstart — connect your agent in 60 seconds

## 1. Install Ghostid

[Google Play → Ghostid](https://play.google.com/store/apps/details?id=com.autokeren.ghostid)

## 2. Start the tunnel

Open the app → tap **Start Tunnel**. Wait for the URL card:

```
https://your-tunnel.trycloudflare.com
```

Copy the URL and the **token** below it.

## 3. Connect your MCP client

### Claude Desktop / Claude Code

`claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "ghostid": {
      "type": "http",
      "url": "https://YOUR-TUNNEL.trycloudflare.com/mcp",
      "headers": {
        "Authorization": "Bearer YOUR-TOKEN"
      }
    }
  }
}
```

### Cursor

`.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "ghostid": {
      "url": "https://YOUR-TUNNEL.trycloudflare.com/mcp",
      "headers": { "Authorization": "Bearer YOUR-TOKEN" }
    }
  }
}
```

### Raw REST (curl)

```bash
curl -H "Authorization: Bearer $TOKEN" "$URL/status"
curl -H "Authorization: Bearer $TOKEN" "$URL/ui"
curl -H "Authorization: Bearer $TOKEN" "$URL/screen"
```

## 4. Verify

Ask your agent:

> Take a screenshot of the phone and tell me what app is open.

If it answers, you're live. Next: pick a recipe from the [cookbook](../cookbook/).

## Troubleshooting

| Symptom | Fix |
|---|---|
| 401 Unauthorized | Token mismatch — copy again from the app |
| Tunnel URL dead | Restart tunnel in the app (URLs are ephemeral) |
| Taps do nothing | Samsung Flow/Smart View overlay — call `uncast`, or use the a11y engine |
| UI dump empty | Enable the Accessibility engine in the app, then retry |
