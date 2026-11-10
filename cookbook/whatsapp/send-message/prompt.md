# Prompt — Send a WhatsApp message

You are operating an Android phone through Ghostid.

Goal: send this message to the WhatsApp contact "<CONTACT>":

"""
<MESSAGE>
"""

Rules:
- If more than one chat matches "<CONTACT>", stop and ask.
- Verify the chat header before typing.
- Do not send if the typed text does not match exactly.

Steps:
1. `open_app` with package `com.whatsapp`.
2. `wait_text` for "Chats".
3. Tap the search icon, then `type_text` "<CONTACT>".
4. Tap the matching chat row.
5. `ui_dump` and confirm the header shows "<CONTACT>".
6. Tap the message input, `type_text` the message above.
7. Tap "Send".
8. `ui_dump` and confirm the message bubble appears.
9. Take a `screenshot` and report success.
