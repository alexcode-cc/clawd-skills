---
name: repliz
description: Repliz social media management API integration. Use when working with Repliz to: (1) Get connected social media accounts, (2) View or create post schedules, (3) Manage comment queues and replies, (4) Delete scheduled posts. Requires Access Key and Secret Key for Basic authentication.
---

# Repliz API Skill

## Authentication

All API requests require **Basic Authentication** in the header:
- **Username**: Access Key
- **Password**: Secret Key
- **Base URL**: `https://api.repliz.com`

## API Endpoints

### Accounts

**GET /public/account**
- Query params: `page` (default 1), `limit` (default 10), `search` (optional)
- Returns list of connected social media accounts
- Fields: `_id`, `generatedId`, `name`, `username`, `picture`, `isConnected`, `type` (instagram/threads/tiktok/etc), `userId`, `createdAt`, `updatedAt`

**GET /public/account/{_id}**
- Get account details by ID (use `_id` field from account list)
- Returns full account info including `token.access` for posting

---

### Schedules

**GET /public/schedule**
- Query params: `page`, `limit`, `accountIds` (can be repeated)
- Returns scheduled posts

**GET /public/schedule/{_id}**
- Get schedule details by ID

**POST /public/schedule**
- Create new scheduled post. Request body varies by type:

Text post (Facebook, Threads):
```json
{
  "title": "",
  "description": "Your post text",
  "type": "text",
  "medias": [],
  "scheduleAt": "2026-02-14T10:35:09.658Z",
  "accountId": "680affa5ce12f2f72916f67e"
}
```

Image post (Facebook, Instagram, Threads, TikTok, LinkedIn):
```json
{
  "title": "",
  "description": "Caption",
  "type": "image",
  "medias": [{"type": "image", "thumbnail": "url", "url": "url", "alt": "description"}],
  "scheduleAt": "2026-02-14T10:35:09.658Z",
  "accountId": "680affa5ce12f2f72916f67e"
}
```

Nested/Thread post (Threads):
```json
{
  "title": "",
  "description": "First Post",
  "type": "text",
  "medias": [],
  "scheduleAt": "2026-02-14T10:35:09.658Z",
  "accountId": "680affa5ce12f2f72916f67e",
  "replies": [
    {"title": "", "description": "Second Post reply First Post", "type": "text", "medias": []},
    {"title": "", "description": "Third Post reply Second Post", "type": "text", "medias": []}
  ]
}
```

**DELETE /public/schedule/{_id}**
- Delete scheduled post (cannot be recovered)

---

### Comment Queue

**GET /public/queue**
- Query params: `page`, `limit`, `search`, `status` (pending/resolved/ignored), `accountIds` (can be repeated)
- Returns comment queue from social media

**GET /public/queue/{_id}**
- Get queue item details

**POST /public/queue/{_id}**
- Reply to comment (automatically marks as resolved)
```json
{
  "text": "Your reply"
}
```

---

## Error Handling

- `401`: Invalid authorization header
- `404`: Not found
- `500`: Internal server error

## Notes

- `accountId` for posting comes from `_id` field in account list
- `scheduleAt` uses ISO 8601 format with timezone (e.g., `2026-02-14T10:35:09.658Z`)
- Queue status can be: pending, resolved, ignored
