---
name: x-api-poster
version: 1.0.0
description: Post tweets to X (Twitter) via API v2 with OAuth 1.0a authentication. Supports text posts, image attachments, replies, and thread creation. Use when user says "tweet", "post to X", "post to Twitter", or "ツイート".
---

# X API Poster

Post to X (Twitter) using the official API v2 with OAuth 1.0a authentication.

## Features

- **Text tweets** — Post plain text tweets
- **Image attachments** — Upload and attach images (v1.1 media upload)
- **Replies & threads** — Reply to tweets or create thread chains
- **Pure Python** — No external OAuth libraries needed (manual HMAC-SHA1 signing)

## Quick Start

```bash
# Post a tweet
python3 {skill_dir}/post.py "Hello from OpenClaw!"

# Post with image
python3 {skill_dir}/post.py "Check this out" /path/to/image.png

# Reply to a tweet (thread)
python3 {skill_dir}/post.py "Reply text" 1234567890123456789

# Reply with image
python3 {skill_dir}/post.py "Reply with pic" 1234567890123456789 /path/to/image.png
```

## Configuration

Set these environment variables (or they fall back to hardcoded defaults in the script):

| Variable | Description |
|----------|-------------|
| `X_CONSUMER_KEY` | Twitter API Consumer Key (API Key) |
| `X_CONSUMER_SECRET` | Twitter API Consumer Secret |
| `X_ACCESS_TOKEN` | OAuth 1.0a Access Token |
| `X_ACCESS_TOKEN_SECRET` | OAuth 1.0a Access Token Secret |

### Getting API Keys

1. Go to [developer.x.com](https://developer.x.com/)
2. Create a project and app
3. Enable OAuth 1.0a with Read and Write permissions
4. Generate Consumer Keys and Access Tokens
5. Set them as environment variables or in `~/.openclaw/secrets.env`

## Requirements

- Python 3.8+
- `requests` library (`pip install requests`)

## Usage from Agent

When the user asks to post a tweet:

```bash
python3 {skill_dir}/post.py "Tweet content here"
```

For image posts, generate or locate the image first, then:

```bash
python3 {skill_dir}/post.py "Tweet with image" /path/to/image.png
```

## API Details

- **Post endpoint**: `POST https://api.twitter.com/2/tweets` (v2)
- **Media upload**: `POST https://upload.twitter.com/1.1/media/upload.json` (v1.1)
- **Auth**: OAuth 1.0a with HMAC-SHA1 signature
