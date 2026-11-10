/**
 * Ghostid Discord bot — Cloudflare Worker.
 *
 * Slash commands (HTTP interactions, no gateway needed):
 *   /faq <topic>      search docs/FAQ.md
 *   /recipe <slug>    fetch a cookbook recipe
 *   /docs             links to the docs
 *   /role <name>      assign User / Dev / Contributor
 *
 * Cron: polls the cookbook and posts new recipes to a webhook channel.
 *
 * Env vars (wrangler secret):
 *   DISCORD_PUBLIC_KEY   app public key (for signature verification)
 *   DISCORD_BOT_TOKEN    bot token (for role assignment)
 *   DISCORD_APP_ID       application id
 *   DISCORD_GUILD_ID     your server id
 *   RECIPES_WEBHOOK      Discord webhook URL for #recipes
 *   REPO                 owner/repo (default autokeren/ghostid)
 */

const REPO = 'autokeren/ghostid';
const RAW = 'https://raw.githubusercontent.com';
const API = 'https://discord.com/api/v10';

export default {
  async fetch(request, env, ctx) {
    if (request.method !== 'POST') return new Response('Ghostid bot', { status: 200 });

    const body = await request.text();
    const ok = await verify(request, body, env.DISCORD_PUBLIC_KEY);
    if (!ok) return new Response('invalid request signature', { status: 401 });

    const interaction = JSON.parse(body);

    // PING (Discord verification)
    if (interaction.type === 1) {
      return json({ type: 1 });
    }

    const name = interaction.data && interaction.data.name;
    const options = (interaction.data && interaction.data.options) || [];
    const arg = options.length ? String(options[0].value || '') : '';

    try {
      if (name === 'faq') return json(await cmdFaq(arg));
      if (name === 'recipe') return json(await cmdRecipe(arg));
      if (name === 'docs') return json(cmdDocs());
      if (name === 'role') return json(await cmdRole(interaction, arg, env));
    } catch (e) {
      return json(reply(`Error: ${e.message}`, true));
    }
    return json(reply('Unknown command.', true));
  },

  async scheduled(event, env, ctx) {
    ctx.waitUntil(feedRecipes(env));
  },
};

/* ---------- signature ---------- */

async function verify(request, body, publicKeyHex) {
  const sig = request.headers.get('X-Signature-Ed25519');
  const ts = request.headers.get('X-Signature-Timestamp');
  if (!sig || !ts || !publicKeyHex) return false;
  const key = hexToBytes(publicKeyHex);
  const sigBytes = hexToBytes(sig);
  const msg = new TextEncoder().encode(ts + body);
  const cryptoKey = await crypto.subtle.importKey(
    'raw', key, { name: 'Ed25519' }, false, ['verify']
  );
  return crypto.subtle.verify('Ed25519', cryptoKey, sigBytes, msg);
}

function hexToBytes(hex) {
  const out = new Uint8Array(hex.length / 2);
  for (let i = 0; i < out.length; i++) out[i] = parseInt(hex.substr(i * 2, 2), 16);
  return out;
}

/* ---------- commands ---------- */

async function cmdFaq(topic) {
  const md = await fetchText(`${RAW}/${REPO}/main/docs/FAQ.md`);
  const blocks = md.split(/\n## /).slice(1);
  const needle = topic.toLowerCase();
  const hit = blocks.find((b) => b.toLowerCase().includes(needle));
  if (!hit) {
    return reply(`No FAQ entry for **${topic}**. Try: \`pairing\`, \`screenshot\`, \`privacy\`, \`free\`.`, true);
  }
  const text = hit.split('\n')[0].trim();
  return reply(`**${text}**\n${hit.slice(text.length).trim().slice(0, 1500)}`);
}

async function cmdRecipe(slug) {
  const path = slug.replace(/^\/+|\/+$/g, '');
  const md = await fetchText(`${RAW}/${REPO}/main/cookbook/${path}/RECIPE.md`);
  if (md.startsWith('404')) {
    return reply(`Recipe \`${path}\` not found. Browse: https://github.com/${REPO}/tree/main/cookbook`, true);
  }
  return reply(md.slice(0, 1800));
}

function cmdDocs() {
  return reply(
    `**Ghostid docs**\n` +
      `• Getting started: https://github.com/${REPO}/blob/main/docs/getting-started.md\n` +
      `• Features: https://github.com/${REPO}/blob/main/docs/features.md\n` +
      `• MCP tools: https://github.com/${REPO}/blob/main/docs/mcp-tools.md\n` +
      `• Cookbook: https://github.com/${REPO}/tree/main/cookbook`
  );
}

async function cmdRole(interaction, roleName, env) {
  const roles = {
    user: 'User',
    dev: 'Dev',
    contributor: 'Contributor',
  };
  const key = roleName.toLowerCase();
  if (!roles[key]) {
    return reply('Pick a role: `user`, `dev`, or `contributor`.', true);
  }
  const guildId = interaction.guild_id || env.DISCORD_GUILD_ID;
  const userId = interaction.member && interaction.member.user && interaction.member.user.id;
  if (!guildId || !userId) return reply('Run this inside the server.', true);

  // find the role id by name
  const all = await discord(env, `/guilds/${guildId}/roles`);
  const role = all.find((r) => r.name.toLowerCase() === roles[key].toLowerCase());
  if (!role) return reply(`Role **${roles[key]}** not found on the server.`, true);

  await discord(env, `/guilds/${guildId}/members/${userId}/roles/${role.id}`, 'PUT');
  return reply(`Role **${roles[key]}** assigned ✓`, true);
}

/* ---------- recipe feed ---------- */

async function feedRecipes(env) {
  if (!env.RECIPES_WEBHOOK) return;
  const tree = await fetchJson(`https://api.github.com/repos/${REPO}/git/trees/main?recursive=1`);
  const recipes = (tree.tree || [])
    .filter((t) => t.path.startsWith('cookbook/') && t.path.endsWith('/RECIPE.md'))
    .map((t) => t.path.replace('cookbook/', '').replace('/RECIPE.md', ''));

  // state: last seen recipes, stored in KV (optional)
  const seen = env.STATE ? (await env.STATE.get('seen')) : null;
  const seenSet = new Set(seen ? JSON.parse(seen) : []);
  const fresh = recipes.filter((r) => !seenSet.has(r));

  for (const slug of fresh.slice(0, 5)) {
    const md = await fetchText(`${RAW}/${REPO}/main/cookbook/${slug}/RECIPE.md`);
    const title = (md.match(/^# (.+)$/m) || [, slug])[1];
    await fetch(env.RECIPES_WEBHOOK, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        username: 'Ghostid Cookbook',
        embeds: [
          {
            title: `New recipe: ${title}`,
            url: `https://github.com/${REPO}/tree/main/cookbook/${slug}`,
            description: md.slice(0, 300),
            color: 0xc8a24a,
          },
        ],
      }),
    });
  }

  if (env.STATE) await env.STATE.put('seen', JSON.stringify(recipes));
}

/* ---------- helpers ---------- */

function reply(content, ephemeral = false) {
  return {
    type: 4,
    data: { content: String(content).slice(0, 1900), flags: ephemeral ? 64 : 0 },
  };
}

function json(obj) {
  return new Response(JSON.stringify(obj), {
    headers: { 'Content-Type': 'application/json' },
  });
}

async function fetchText(url) {
  const r = await fetch(url);
  if (!r.ok) return `404: ${url}`;
  return r.text();
}

async function fetchJson(url) {
  const r = await fetch(url, { headers: { 'User-Agent': 'ghostid-bot' } });
  return r.json();
}

async function discord(env, path, method = 'GET', body) {
  const r = await fetch(`${API}${path}`, {
    method,
    headers: {
      Authorization: `Bot ${env.DISCORD_BOT_TOKEN}`,
      'Content-Type': 'application/json',
    },
    body: body ? JSON.stringify(body) : undefined,
  });
  if (!r.ok) throw new Error(`discord ${method} ${path}: ${r.status}`);
  return r.status === 204 ? null : r.json();
}
