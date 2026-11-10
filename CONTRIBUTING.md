# Contributing to Ghostid

The most valuable contribution is a **recipe** — a tested, copy-pasteable tool sequence that makes an agent do something real on Android.

## Add a recipe

1. Fork this repo
2. Create `cookbook/<app>/<action>/` with:
   - `RECIPE.md` — goal, prerequisites, steps, failure modes
   - `recipe.yaml` — metadata (see [spec/RECIPE-FORMAT.md](../spec/RECIPE-FORMAT.md))
   - `prompt.md` — the exact prompt that works
3. Test it on a real device through Ghostid
4. Open a PR — one recipe per PR

Rules:
- No recipe without `tested_on`
- Every mutation ends with a verification step
- Keep prompts self-contained and imperative

## Fix a recipe

Broken recipe? Open an issue with:
- Device + Android version
- The failing step
- The `ui_dump` output around the failure

## Code of conduct

Be useful. Be precise. No spam, no self-promo, no unrelated links.

## Need help?

Join the [Ghostid Discord](https://discord.gg/krANeUdpB) � the `#help` channel and the `/faq` bot command answer the most common setup questions.