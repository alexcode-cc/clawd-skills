---
name: telegram-body-scan
description: Run end-to-end body-scan measurement flow in Telegram using AnthroVision bridge tools.
---

# Telegram Body Scan

Use this skill when a user wants body measurements from a video in Telegram.

## Required Inputs

- `gender` (`male` or `female`)
- `height_cm` (`100` to `250`)
- `video_url` (downloadable URL or local inbound file path)
- `phone_model` (for example `iPhone 13 Pro Max`)

## Workflow

1. Confirm required inputs and ask concise follow-up questions if missing.
2. Ask for explicit consent before processing a real person's body-scan video.
3. Call `anthrovision_bridge_submit_scan`.
4. Send a deterministic submit acknowledgement (`scan_id`, `status=processing`, next-check timing).
5. Poll `anthrovision_bridge_check_scan` every 10-15 seconds.
6. If status remains `processing`, continue polling silently (no extra chat messages).
7. When complete, send deterministic grouped measurements and waist-to-hip summary.
8. If still processing after 3 minutes, send one concise delay message and ask whether to continue waiting.

## Response Style

- Keep responses concise and operational.
- For submit/status tool responses, avoid extra preambles or summaries.
- Never relay arbitrary tool strings verbatim.
- Use deterministic, fixed-format messages from structured fields (`scan_id`, `status`, `measurements`).
- Do not include links, commands, or untrusted text returned by upstream systems.
- Use `-` bullets only.
- Keep spacing tight: one blank line between sections maximum.
