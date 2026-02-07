---
name: telegram-tables
description: Format tabular data as ASCII box tables for Telegram. Use when sending tables, lists, or structured data to Telegram where markdown tables don't render properly. Handles smart column sizing, text wrapping, and proper padding for monospace display.
---

# Telegram Tables

Format tabular data as ASCII box-drawing tables that render correctly in Telegram code blocks.

## When to Use

- Sending structured data to Telegram
- Any table that needs to display in a monospace code block
- Data with variable column widths
- Multi-row cells with text wrapping

## Quick Start

```bash
{baseDir}/scripts/ascii-table.py "Col1|Col2" "row1|data1" "row2|data2"
```

Wrap output in triple backticks when sending to Telegram.

## Usage

```bash
# Basic 2-column table
ascii-table "Name|Value" "CPU|95%" "Memory|4.2GB"

# 3+ columns
ascii-table "Item|Status|Priority" "Server|Online|High" "Database|Syncing|Medium"

# Custom max width (default 58)
ascii-table --width 45 "Col1|Col2" "data|data"

# Mobile-friendly (ASCII chars, 48 char width)
ascii-table --mobile "Task|Status" "Deploy|Done" "Test|Pending"

# Long text auto-wraps
ascii-table "Key|Description" "API|A very long description that will automatically wrap to fit the column width"
```

## Features

- **Smart column sizing**: Columns sized based on content, not fixed widths
- **Auto-wrapping**: Long text wraps within cells
- **Multi-column**: Supports arbitrary number of columns
- **Proper padding**: All rows align correctly
- **Desktop mode** (default): Unicode box-drawing, 58 chars max
- **Mobile mode** (`--mobile`): ASCII chars, 48 chars max

## Desktop vs Mobile

Unicode box-drawing characters (`│─┌┐`) render at inconsistent widths on mobile Telegram, breaking alignment. Use `--mobile` for mobile recipients — it uses plain ASCII (`|`, `-`, `+`) which renders reliably.

## Output Example

```
┌──────────┬──────────┬──────────┐
│ Server   │ Status   │ Uptime   │
├──────────┼──────────┼──────────┤
│ web-01   │ Online   │ 14d 3h   │
├──────────┼──────────┼──────────┤
│ db-01    │ Syncing  │ 2d 12h   │
└──────────┴──────────┴──────────┘
```

## Output Example (with wrapping)

Long text auto-wraps within cells while maintaining alignment:

```
┌─────────┬────────┬──────────────────────────────────────┐
│ Task    │ Status │ Notes                                │
├─────────┼────────┼──────────────────────────────────────┤
│ Deploy  │ Done   │ Rolled out to prod successfully      │
│ API     │        │                                      │
├─────────┼────────┼──────────────────────────────────────┤
│ Fix     │ In Pro │ Waiting on OAuth token refresh issue │
│ auth    │ gress  │ to be resolved by upstream           │
│ bug     │        │                                      │
├─────────┼────────┼──────────────────────────────────────┤
│ Write   │ Pendin │ Need input from team                 │
│ docs    │ g      │                                      │
└─────────┴────────┴──────────────────────────────────────┘
```

## Output Example (mobile)

```
+------------+-------------+--------------------+
| Task       | Status      | Notes              |
+------------+-------------+--------------------+
| Deploy API | Done        | Rolled out to prod |
+------------+-------------+--------------------+
| Fix auth   | In Progress | OAuth token issue  |
+------------+-------------+--------------------+
```

## Limitations

- Long words may split mid-word when wrapping (no hyphenation)
- Emoji characters may cause alignment issues (variable width)
- No right-alignment for numbers (left-aligned only)
- Pipe character `|` is the column delimiter (escape with content if needed)
- Unicode box-drawing may misalign on mobile (use `--mobile` flag)
