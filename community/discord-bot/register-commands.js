/**
 * Register the slash commands for the Ghostid bot (one-time).
 *
 * Usage:
 *   set DISCORD_APP_ID=...
 *   set DISCORD_BOT_TOKEN=...
 *   set DISCORD_GUILD_ID=...
 *   node register-commands.js
 */

const APP = process.env.DISCORD_APP_ID;
const TOKEN = process.env.DISCORD_BOT_TOKEN;
const GUILD = process.env.DISCORD_GUILD_ID;

if (!APP || !TOKEN || !GUILD) {
  console.error('Set DISCORD_APP_ID, DISCORD_BOT_TOKEN and DISCORD_GUILD_ID first.');
  process.exit(1);
}

const commands = [
  {
    name: 'faq',
    description: 'Search the Ghostid FAQ',
    options: [
      { name: 'topic', description: 'e.g. pairing, screenshot, privacy', type: 3, required: true },
    ],
  },
  {
    name: 'recipe',
    description: 'Show a cookbook recipe',
    options: [
      { name: 'slug', description: 'e.g. tiktok/upload-video', type: 3, required: true },
    ],
  },
  { name: 'docs', description: 'Links to the Ghostid docs' },
  {
    name: 'role',
    description: 'Assign yourself a role',
    options: [
      {
        name: 'name',
        description: 'user | dev | contributor',
        type: 3,
        required: true,
        choices: [
          { name: 'User', value: 'user' },
          { name: 'Dev', value: 'dev' },
          { name: 'Contributor', value: 'contributor' },
        ],
      },
    ],
  },
];

const res = await fetch(`https://discord.com/api/v10/applications/${APP}/guilds/${GUILD}/commands`, {
  method: 'PUT',
  headers: {
    Authorization: `Bot ${TOKEN}`,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify(commands),
});

console.log(res.status, await res.text());
