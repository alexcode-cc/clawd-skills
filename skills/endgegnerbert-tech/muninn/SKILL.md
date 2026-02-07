---
name: muninn
version: 1.2.0
homepage: https://www.muninn.space
description: Universal Context Protocol (CXP) for AI agents. Provides per-project long-term memory, semantic search, and surgical context injection. Use to save 95% of tokens and ensure cross-session persistence. Created by @Blackknight1dev.
---

# Muninn - The Universal Memory Layer

Muninn is an advanced per-project memory system designed for AI agents. It uses the **Context Exchange Protocol (CXP)** to provide high-performance, token-efficient context management.

## 🚀 The Muninn Protocol

As an agent, you SHOULD follow these three pillars of the Muninn workflow to remain efficient and accurate:

1.  **Orient Yourself (`brain_check`)**: Call this at the start of every session. It's your "morning coffee" for the project.
2.  **Search Before You Code (`search_context`)**: Never assume you know the codebase. Search for existing patterns to avoid duplication and bugs.
3.  **Learn as You Go (`add_memory`)**: Every decision and fix should be a memory. This is how you (and future agents) become smarter.

---

## 🛠 Tool Reference (MCP)

This skill provides access to the Muninn core toolset via MCP.

### 1. `init_project`
**Purpose**: Prepare a new project for Muninn.
- **Arguments**:
    - `project_path` (string): Absolute path to the directory.
- **When to use**: When starting a brand new project that isn't yet indexed.

### 2. `brain_check`
**Purpose**: Loads project context, identifies active files, and patterns.
- **Arguments**:
    - `task_description` (string, *required*): What are you about to do?
- **When to use**: Call this at the beginning of a task to load relevant context.

### 3. `add_memory` (LEARNING)
**Purpose**: Persist facts, decisions, lessons, or user preferences.
- **Arguments**:
    - `content` (string, *required*): The factual content to save.
    - `title` (string, *required*): A short, descriptive title.
    - `category` (string): Subfolder (e.g., 'architecture', 'decisions', 'lessons').
- **When to use**: When a bug is fixed, a decision is made, or the user says "remember this".

### 4. `search_context` (SEARCH)
**Purpose**: Semantically search the project code and memories.
- **Arguments**:
    - `query` (string, *required*): Natural language query or "Project Overview".
    - `limit` (number): Max results (default: 5).
- **When to use**: Before any code change or when answering architectural questions.

### 5. `reindex_context`
**Purpose**: Rebuild the CXP index to reflect recent file changes.
- **Arguments**:
    - `project_path` (string): Path to the project.
- **When to use**: After large refactors or when files seem "out of sync".

---

## 📦 Technical Integration

Muninn is powered by the `muninn-core` package.
- **Package**: `npx -y muninn-core@2.1.3`
- **Format**: CXP (Context Exchange Protocol)
- **Persistence**: Memories are stored in `~/.muninn/memory/` as Git-friendly Markdown.

---

## 🦞 Pro-Tip for Agents
Muninn surgically retrieves only what's needed. Instead of reading a 1000-line file, use `search_context` to find the exact 50 lines that matter. Your user will thank you for the lower token costs!
