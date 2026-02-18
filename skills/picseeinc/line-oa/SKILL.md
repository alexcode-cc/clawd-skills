---
name: line-oa
description: Operate LINE Official Account Manager (chat.line.biz) via browser automation. Use when asked to check LINE messages, reply to LINE customers, or manage LINE OA chat interface.
---

# LINE Official Account Manager

⚠️ **CRITICAL**: Always use `profile:"openclaw"` (isolated browser) for all browser actions. Never use Chrome relay. Keep the same `targetId` across operations to avoid losing the tab.

## Configuration

Before first use, check if `config.json` exists:
```
read file_path:"<skill_dir>/config.json"
```

If missing, tell the user to run the setup wizard:
```bash
cd <skill_dir>
node scripts/setup.js
```

The setup script will guide them through configuration interactively.

## Quick Start Workflow

When user asks to check LINE messages:

1. **Check config** → if missing, prompt user to run setup
2. **Open browser** → `browser action:"open"` with chatUrl
3. **Wait 2s** → let page load
4. **Snapshot** → check if already on chat list page
5. **If on chat list** (see chat items + "Click a chat to start talking!"):
   - ✅ **PROCEED to List Unread Messages section**
6. **If on login page** (see "LINE Account" or "Business Account" button):
   - Click through login flow
   - Wait and snapshot again
   - Verify you reached chat list before proceeding
7. **Run list-unread.js** → extract and report unread conversations

**Key rule**: Always verify you're on the chat list page (Step 5 check) before running the unread script.

## Login

**IMPORTANT**: Follow these steps in order. After each action, CHECK if you've reached the chat list before proceeding.

### Step 1: Load config and open browser

1. Read the chat URL from config:
   ```
   read file_path:"<skill_dir>/config.json"
   ```
   Parse the JSON and extract `chatUrl`. If the file doesn't exist, prompt the user to run setup first.

2. Open the chat interface:
   ```
   browser action:"open" profile:"openclaw" targetUrl:"<chatUrl_from_config>"
   ```
   This returns a `targetId` — **save it for all subsequent operations**.

### Step 2: Check if already logged in

3. Wait 2 seconds for page to load:
   ```
   browser action:"act" profile:"openclaw" targetId:"<your_targetId>" request:{"kind":"wait","timeMs":2000}
   ```

4. Take a snapshot to see what page you're on:
   ```
   browser action:"snapshot" profile:"openclaw" targetId:"<your_targetId>" refs:"aria"
   ```

5. **CHECK THE SNAPSHOT** — you are logged in if you see:
   - Multiple chat items with names like "John Smith", "Alice Chen", "Sarah Johnson" etc.
   - Text "Click a chat to start talking!"
   - A banner with "LINE Official Account Manager" heading
   - A textbox with placeholder "Search"
   
   **If you see these elements → SKIP to "List Unread Messages" section. Login is complete.**

### Step 3: Handle login page (only if not logged in)

6. If the snapshot shows a login page with buttons "LINE Account" or "Business Account":
   - Click the green "LINE Account" button (look for button with text "LINE Account" or similar):
     ```
     browser action:"act" profile:"openclaw" targetId:"<your_targetId>" request:{"kind":"click","ref":"<button_ref>"}
     ```

7. Wait 2 seconds, then snapshot again:
   ```
   browser action:"act" profile:"openclaw" targetId:"<your_targetId>" request:{"kind":"wait","timeMs":2000}
   ```
   ```
   browser action:"snapshot" profile:"openclaw" targetId:"<your_targetId>" refs:"aria"
   ```

8. If you see a "Login" or "Sign in" button, click it:
   ```
   browser action:"act" profile:"openclaw" targetId:"<your_targetId>" request:{"kind":"click","ref":"<login_button_ref>"}
   ```

9. Wait 3 seconds for redirect:
   ```
   browser action:"act" profile:"openclaw" targetId:"<your_targetId>" request:{"kind":"wait","timeMs":3000}
   ```

10. Take another snapshot and **CHECK AGAIN** using the criteria in Step 5. If you see the chat list, proceed to list unread messages.

### Troubleshooting

- **URL check**: If `url` in snapshot response contains `https://chat.line.biz/xxx` and snapshot has multiple link elements with chat names → you are logged in
- **If stuck on login**: Tell the user to manually complete authentication in the OpenClaw browser tab, then continue
- **Session expired**: If you see "LINE Business ID" heading or login forms after opening chatUrl, the session expired — follow Step 6-10

## List Unread Messages

Extracts unread chats from the left-side chat list. Does NOT require clicking into each conversation.

**Prerequisites**: You must be logged in and on the chat list page (see Login section Step 5 for verification).

### Steps

1. Read the script content:
   ```
   read file_path:"<skill_dir>/scripts/list-unread.js"
   ```
   You will see a script wrapped in `(() => { ... })()` format.

2. Run the script via browser evaluate:
   
   ⚠️ **CRITICAL**: Browser evaluate requires `function(){...}` format, NOT `(() => {...})()` format.
   
   ❌ **WRONG** (will fail with "Invalid evaluate function"):
   ```json
   {"kind":"evaluate","fn":"(() => { const items = ...; })()"}
   ```
   
   ✅ **CORRECT** (use this format):
   ```json
   {"kind":"evaluate","fn":"function(){const items=document.querySelectorAll('.list-group-item-chat');return Array.from(items).map(el=>{const h6=el.querySelector('h6');const preview=el.querySelector('.text-muted.small');const prevText=preview?.textContent?.trim()||'';const allMuted=el.querySelectorAll('.text-muted');let time='';for(const m of allMuted){const t=m.textContent.trim();if(t&&t.length<20&&t!==prevText)time=t;}const dot=el.querySelector('span.badge.badge-pin');const unread=!!dot&&getComputedStyle(dot).display!=='none';return{name:h6?.textContent?.trim()||'',time,lastMsg:prevText.substring(0,100),unread};}).filter(i=>i.name);}"}
   ```
   
   Full browser call:
   ```
   browser action:"act" profile:"openclaw" targetId:"<your_targetId>" request:{"kind":"evaluate","fn":"function(){const items=document.querySelectorAll('.list-group-item-chat');return Array.from(items).map(el=>{const h6=el.querySelector('h6');const preview=el.querySelector('.text-muted.small');const prevText=preview?.textContent?.trim()||'';const allMuted=el.querySelectorAll('.text-muted');let time='';for(const m of allMuted){const t=m.textContent.trim();if(t&&t.length<20&&t!==prevText)time=t;}const dot=el.querySelector('span.badge.badge-pin');const unread=!!dot&&getComputedStyle(dot).display!=='none';return{name:h6?.textContent?.trim()||'',time,lastMsg:prevText.substring(0,100),unread};}).filter(i=>i.name);}"}
   ```

3. The script returns a JSON array of **all** chat items: `[{ name, time, lastMsg, unread }]`
   - `name`: sender display name (who sent the message)
   - `time`: timestamp shown in chat list (e.g., "21:32", "Yesterday", "Friday")
   - `lastMsg`: last message preview text, truncated to ~100 chars
   - `unread`: boolean — `true` if green dot is present, `false` otherwise

### Example Output

```json
[
  {
    "name": "John Smith",
    "time": "21:32",
    "lastMsg": "Good evening! Thank you for your message. We will respond within 12 hours as this is outside our support hours.",
    "unread": false
  },
  {
    "name": "Alice Chen",
    "time": "Yesterday",
    "lastMsg": "Hello! Thank you for reaching out. Happy New Year! 🎊 I've confirmed your payment was successful ✅",
    "unread": true
  }
]
```

### How to Report Results

- **If there are unread messages** (`unread: true`):
  - List each unread conversation with name, time, and preview
  - Example: "There is 1 unread message: Alice Chen (Yesterday): Hello! Thank you for reaching out. Happy New Year!..."

- **If no unread messages**:
  - Say: "No unread messages at this time"

### Notes

- **Unread indicator**: `span.badge.badge-pin` inside each chat list item (green dot)
- **Limitation**: `lastMsg` shows the last message in the thread, which may be an auto-response rather than the customer's original message
- **To read full conversation**: Click the chat item link — the conversation opens in the right panel and marks the message as read

## Reply to a Message

1. Take a snapshot to find the chat item:
   ```
   browser action:"snapshot" profile:"openclaw" targetId:"<your_targetId>" refs:"aria"
   ```
2. Click a chat item link in the left panel (e.g., `ref:"e68"`):
   ```
   browser action:"act" profile:"openclaw" targetId:"<your_targetId>" request:{"kind":"click","ref":"e68"}
   ```
3. If the input box is locked (auto-response mode), click the manual chat toggle button in the top banner to unlock it.
4. Take another snapshot to find the input box and send button.
5. Click the text input box (e.g., `ref:"e509"`):
   ```
   browser action:"act" profile:"openclaw" targetId:"<your_targetId>" request:{"kind":"click","ref":"e509"}
   ```
6. Type the reply message:
   ```
   browser action:"act" profile:"openclaw" targetId:"<your_targetId>" request:{"kind":"type","ref":"e509","text":"Hello! I'm Emma, happy to help you!"}
   ```
7. Click the green **Send** button (e.g., `ref:"e522"`) or press Enter:
   ```
   browser action:"act" profile:"openclaw" targetId:"<your_targetId>" request:{"kind":"click","ref":"e522"}
   ```

## Manage Notes

Each chat has a Notes panel on the right side. Notes are internal-only (not visible to customers). Max 300 characters per note.

### Add a note
1. Open the conversation.
2. Click the **+** button next to the Notes heading in the right panel.
3. Type content in the textarea.
4. Click **Save**.

### Edit a note
1. Find the note in the right panel.
2. Click the pencil icon at the note's bottom-right corner.
3. Modify the textarea content.
4. Click **Save**.

### Delete a note
1. Click the trash icon at the note's bottom-right corner.
2. A confirmation dialog appears — click **Delete** to confirm.

## Manage Tags

Tags are shown in the right panel below the user's name. They are predefined labels for categorizing chats.

### Add a tag
1. Open the conversation.
2. Click the **Add tags** link (or the pencil icon next to existing tags) in the right panel.
3. The Edit tags modal opens, showing an input field and all available tags.
4. Click a tag from the "All tags" list to select it (it moves to the input field).
5. Click **Save**.

### Remove a tag
1. Open the Edit tags modal (same as above).
2. Click the **×** next to the tag in the input field to deselect it.
3. Click **Save**.


## Switch Account

LINE OA Manager can manage multiple official accounts. Switch between them using the account dropdown in the top-left corner.

1. Take a snapshot to find the account selector:
   ```
   browser action:"snapshot" profile:"openclaw" targetId:"<your_targetId>" refs:"aria"
   ```
2. Click the account combobox (shows current account name):
   ```
   browser action:"act" profile:"openclaw" targetId:"<your_targetId>" request:{"kind":"click","ref":"e11"}
   ```
3. Wait for the dropdown menu to appear:
   ```
   browser action:"act" profile:"openclaw" targetId:"<your_targetId>" request:{"kind":"wait","timeMs":1000}
   ```
4. Take another snapshot to see available accounts in the listbox:
   ```
   browser action:"snapshot" profile:"openclaw" targetId:"<your_targetId>" refs:"aria"
   ```
   The snapshot will show a list of accounts you have access to. Look for generic items in the listbox (each account will have a name and "Administrator" or role label).
5. Click the desired account item (e.g., `ref:"e589"`):
   ```
   browser action:"act" profile:"openclaw" targetId:"<your_targetId>" request:{"kind":"click","ref":"e589"}
   ```
6. Wait for the page to load the new account's chat list:
   ```
   browser action:"act" profile:"openclaw" targetId:"<your_targetId>" request:{"kind":"wait","timeMs":2000}
   ```

## Notes

- LINE periodically expires sessions; re-login required when that happens
- Session is usually active for several hours if the browser remains open
