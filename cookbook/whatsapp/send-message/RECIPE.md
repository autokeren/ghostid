# Send a WhatsApp message

**Goal:** Send a text message to a contact on WhatsApp.

## Prerequisites

- WhatsApp installed and signed in
- Contact name known

## Steps

1. `open_app` — `com.whatsapp`
2. `wait_text` — `Chats`
3. `tap_text` — search icon
4. `type_text` — contact name
5. `tap_text` — the matching chat row
6. `ui_dump` — confirm the chat opened (contact name in header)
7. `tap_text` — message input box
8. `type_text` — message
9. `tap_text` — send button (`Send`)
10. `ui_dump` — confirm the message bubble appears

## Prompt

See [prompt.md](prompt.md).

## Failure modes

| Symptom | Recovery |
|---|---|
| Multiple matches | Stop and ask which contact |
| Input box not found | `ui_dump`, tap the `com.whatsapp:id/entry` bounds |
| Send disabled | Empty text — retype and verify |
