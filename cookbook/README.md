# The Ghostid Cookbook

**Recipes that make agents useful on Android.**

Each recipe is a tested tool sequence + a copy-paste prompt. Cooking = turning an intent into a repeatable recipe.

## Recipes

| App | Recipe | Difficulty | Time |
|---|---|---|---|
| YouTube | [Upload a Short](youtube/upload-short/) | medium | 2-4 min |
| X | [Post a tweet](x/post-tweet/) | easy | 30-60 s |
| WhatsApp | [Send a message](whatsapp/send-message/) | easy | 30-60 s |
| Settings | [Toggle Wi-Fi](settings/toggle-wifi/) | easy | 5-10 s |
| Screen | [Read notifications](screen/read-notifications/) | easy | 10-20 s |
| Gemini | [Generate a video](gemini/generate-video/) | easy | 2-3 min |
| TikTok | [Upload a video](tiktok/upload-video/) | medium | 1-2 min |

## Full chain example

Two recipes chain together into one end-to-end automation:

```
gemini/generate-video   ->  /sdcard/Movies/<slug>.mp4
tiktok/upload-video     ->  posted with a caption
```

1. Generate a video in Gemini and save it with a readable name.
2. Upload that exact file to TikTok via the share sheet.
3. Verify the post in the profile grid.

Tested end-to-end on a Galaxy S22 Ultra through a Cloudflare tunnel only.

## Anatomy of a recipe

```
cookbook/<app>/<action>/
├── RECIPE.md      # goal, steps, failure modes
├── recipe.yaml    # metadata + tool list
└── prompt.md      # copy-paste prompt
```

See [spec/RECIPE-FORMAT.md](../spec/RECIPE-FORMAT.md) for the standard.

## Contributing

1. Pick an app + action nobody has covered
2. Test it on a real device through Ghostid
3. Follow the format, add `tested_on`
4. Open a PR — one recipe per PR

No recipe is too small. The best ones are boring and reliable.

## Share your cooking

Post your recipes and results in the [Ghostid Discord](https://discord.gg/krANeUdpB) `#showcase` channel � the best ones get featured.