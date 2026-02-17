---
name: mailgun-simple
description: Send outbound emails via the Mailgun API. Supports EU and US regions. Clean, environment-driven implementation.
---

# Mailgun Simple

Send outbound emails using the official Mailgun JS SDK. 

## 🚨 Security & Setup

This skill is designed to be secure and environment-driven. It does **not** load external .env files and relies strictly on the environment variables provided by the caller.

### Environment Variables
- `MAILGUN_API_KEY`: Your private Mailgun API key. **REQUIRED.**
- `MAILGUN_DOMAIN`: Your verified sending domain (default: `aicommander.dev`).
- `MAILGUN_REGION`: The API region, either `US` or `EU` (default: `EU`).
- `MAILGUN_FROM`: Optional default sender address.

## Tools

### Send Email
Sends a plain text email to a recipient.
```bash
MAILGUN_API_KEY=xxx node scripts/send_email.js <to> <subject> <text> [from]
```

## Runtime Requirements
Requires: `mailgun.js`, `form-data`, and `node`.
