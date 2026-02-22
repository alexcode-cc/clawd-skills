---
name: ngrok-preview
description: High-utility ngrok preview skill for AI agents to share local artifacts (HTML, images, web apps) via temporary public URLs. Use when OpenClaw runs locally but users need mobile access (Telegram/mobile browser) where localhost links are unreachable.
---

# 🌐 Ngrok Preview Skill

A high-utility skill for AI agents to share local artifacts (HTML, images, web apps) with users via temporary, secure public URLs.

This skill is designed to bridge the gap between a local development environment and a mobile-first user experience (Telegram or mobile browsers), where `localhost` links are inaccessible.

## 🚀 Why use this?

- **Mobile-friendly workflows**: Preview agent-generated web content on your phone while the agent runs locally.
- **OpenClaw integration**: Works smoothly with the OpenClaw local gateway. Instead of local file paths or long text dumps, the agent can return a clickable ngrok link.
- **Zero-config sharing flow**: Handles short-lived preview session creation and cleanup through one script.

## 🛠 Installation

Install via the skills.sh ecosystem:

```bash
npx skills add https://github.com/wynnsu/skills-ngrok-preview --skill ngrok-preview
```

## ⚙️ Prerequisites

- `ngrok` CLI installed locally.
- ngrok authenticated with your account token:

```bash
ngrok config add-authtoken "$NGROK_AUTHTOKEN"
ngrok config check
```

## 📖 How it works

When the agent generates a local artifact (visualization, mockup, report, generated page), this skill can:

1. Start a local HTTP server scoped to the artifact directory.
2. Tunnel that local server through ngrok.
3. Return a temporary public URL back to the user through OpenClaw.

## Default agent workflow

Create a preview session:

```bash
python3 scripts/ngrok_preview.py up \
  --title "<task title>" \
  --session-id "<task-id>" \
  --ttl-minutes 120 \
  --source "<artifact-path-1>" \
  --source "<artifact-path-2>"
```

The script returns JSON with:

- `public_url`
- `expires_at`
- `session_id`
- `stop_command`

Stop and clean up when done:

```bash
python3 scripts/ngrok_preview.py down --session-id "<task-id>" --delete-session-dir
```

List sessions:

```bash
python3 scripts/ngrok_preview.py status
```

Clean expired sessions:

```bash
python3 scripts/ngrok_preview.py cleanup
```

## Skill structure

- `SKILL.md`: Skill metadata + operational guidance.
- `scripts/ngrok_preview.py`: Core Python logic for tunnel/session management.
- `references/troubleshooting.md`: Common fixes for ngrok auth, tunnel timeout, and stale sessions.

## 🤝 Compatibility

Optimized for:

- **Gateway**: OpenClaw
- **Ecosystem**: skills.sh
- **Platforms**: Telegram and web-based agent UIs

## Safety boundaries

- Publish only task-specific outputs (never broad directories like workspace root).
- Keep TTL short and explicit.
- Treat every link as temporary access, not persistent hosting.
- Always stop/delete sessions after task completion.

## Troubleshooting

If preview creation fails, follow:

- `references/troubleshooting.md`
