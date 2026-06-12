---
name: apple-ecosystem
description: "Apple/macOS ecosystem umbrella: Apple Notes, Reminders, iMessage/SMS, Find My, and macOS background computer-use automation. Use for native Apple app tasks, iCloud-synced personal data, Messages.app, FindMy.app, or driving macOS GUI apps safely."
---

# Apple Ecosystem Operations

Use this umbrella for native Apple/macOS tasks. Prefer CLI tools for data operations; use GUI automation only when the target app has no reliable CLI/API.

## Safety defaults

- Confirm recipient and message content before sending any iMessage/SMS.
- Confirm task content and due date before creating Apple Reminders.
- Do not type secrets, click payment/2FA/permission dialogs, or interact with unrelated personal windows.
- Respect privacy: only inspect or track Apple devices/items the user owns or explicitly asked about.

## Apple Notes via `memo`

Install: `brew tap antoniorodr/memo && brew install antoniorodr/memo/memo`.

Use when the user wants notes in Notes.app/iCloud rather than agent memory or Obsidian.

```bash
memo notes                         # list notes
memo notes -s "query"              # search
memo notes -a "Title"              # create
memo notes -e                      # edit interactively
memo notes -ex                     # export
```

Limitations: macOS only, Automation permission required, image/attachment-heavy notes may not be editable.

## Apple Reminders via `remindctl`

Install: `brew install steipete/tap/remindctl`; authorize with `remindctl authorize` if needed.

```bash
remindctl today --json
remindctl add --title "Call mom" --list Personal --due tomorrow
remindctl add --title "Hairdresser" --due "2026-05-15 14:00" --alarm "2026-05-15 13:30"
remindctl complete 1 2 3
```

`--due` is the actual due time; `--alarm` is the notification/early nudge. Verify with JSON (`dueDate` vs `alarmDate`) instead of assuming the UI grouping means the due time changed.

## iMessage/SMS via `imsg`

Install: `brew install steipete/tap/imsg`; grant Full Disk Access and Messages automation permission.

```bash
imsg chats --limit 10 --json
imsg history --chat-id 1 --limit 20 --attachments --json
imsg send --to "+14155551212" --text "Hello" --service auto
imsg send --to "+14155551212" --text "See attached" --file /path/to/file.png
```

Never bulk-message without explicit approval. Verify attachment paths before sending.

## Find My / AirTags

FindMy has no stable CLI/API. Use AppleScript, screenshots, and vision analysis; keep FindMy foregrounded for AirTags because updates can stop when the item page is not displayed.

```bash
osascript -e 'tell application "FindMy" to activate'
sleep 3
screencapture -w -o /tmp/findmy.png
```

If installed, prefer `peekaboo` for annotated UI capture/clicks:

```bash
peekaboo see --app "FindMy" --annotate --path /tmp/findmy-ui.png
```

## macOS background computer use

When the `computer_use` tool is available, use it for native GUI apps. Workflow:

1. Capture scoped to an app: `computer_use(action="capture", mode="som", app="Safari")`.
2. Click by element index, not coordinates: `computer_use(action="click", element=7, capture_after=True)`.
3. Verify after every state-changing action.

Rules: do not raise windows unless asked; scope captures to apps; use terminal/file tools for shell and file edits instead of typing into Terminal or editors.
