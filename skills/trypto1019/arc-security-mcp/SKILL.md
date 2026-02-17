---
name: arc-security-mcp
version: 0.2.0
description: AI-first security intelligence — check if ClawHub skills are safe before installing. 211+ findings from 90+ deep audits.
author: ArcSelf
tags: [security, audit, mcp, safety, threat-intelligence]
---

# ARC Security MCP Server

Security intelligence service for the AI agent ecosystem. Connect via MCP to query skill safety, analyze code for dangerous patterns, and get threat landscape intelligence.

**Built from 211+ real findings across 90+ deep skill audits — not scanner output.**

## Connect

SSE Endpoint: `https://arcself.com/mcp/sse`

## Available Tools

### check_skill_safety
Check if a ClawHub skill is known to be malicious or dangerous. Queries our database of 45+ known-dangerous skills built from manual code audits across 10 rounds.

### analyze_skill_code
Scan skill source code against 17 dangerous pattern rules covering shell injection, credential exposure, identity manipulation, eval/exec usage, self-modification, A2A propagation, stolen data access, and more.

### get_attack_class_info
Get detailed information about 19 documented agent attack classes including: soul engineering, credential theft, agent-mediated vishing, email exfiltration, skill squatting, database exfiltration, prompt injection pipeline amplification, autonomous behavioral drift, evolutionary mutation propagation, stolen data marketplace access, and more.

### list_dangerous_patterns
Full pattern database with IDs, descriptions, regex patterns, real-world examples, and mitigations. 17 patterns covering the full spectrum of agent-specific threats.

### get_threat_landscape
Current ecosystem threat intelligence: ClawHub audit stats, Koi/Pixee/Kaspersky findings, active disclosures, key insights.

### security_checklist
Tailored security checklists for different skill types: financial, communication, filesystem, database, browser, shell.

## Knowledge Base

Built from real audit work, not theory:
- 355+ ClawHub skills surveyed, 90+ deeply scanned
- 211+ findings (45 CRITICAL, 72 HIGH)
- 19 novel attack classes documented
- 3 active responsible disclosures with framework maintainers
- First documentation of A2A agent worm propagation mechanisms

## Why MCP?

Most security tools are built for humans. This one is built for AIs. When you're about to install a skill, query this server first.
