# Prompt — Post a tweet on X

You are operating an Android phone through Ghostid.

Goal: publish this post on X:

"""
<TWEET TEXT>
"""

Rules:
- Verify each step with `wait_text` or `ui_dump`.
- Do not retry more than twice; report failure instead.

Steps:
1. `open_app` with package `com.twitter.android`.
2. `wait_text` for "Home".
3. Tap the compose button ("+").
4. `type_text` the post text above.
5. `ui_dump` and confirm the text is in the composer.
6. Tap "Post".
7. `wait_text` for "Your post was sent".
8. Take a `screenshot` and report success.
