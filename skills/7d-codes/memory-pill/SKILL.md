---
name: memory-pill
description: AI-native memory system for OpenClaw. Structured projects, milestone-driven execution, and built-in discipline — designed for how AIs actually work. Persistent, linked, and context-aware. Asks permission before setup.
---

# Memory Pill v0.7.9

**The Problem:** AIs forget everything. They loop. They half-finish tasks. They start solving before understanding. They're context-hungry and stateless by design.

**Memory Pill fixes that at the system level.**

It's not just "folders for notes." It's an **AI-native structure** — designed for how AIs actually work:
- **Milestones** (AIs need bounded scope, not infinite todo lists)
- **Prompt expansion** (AIs need detailed instructions, not vague requests)
- **Execution discipline** (AIs loop without guardrails)
- **Linked memory** (AIs need fast retrieval, not grep)

Your AI becomes stateful, structured, and actually useful across sessions.

---

## Quick Start

```bash
clawhub install memory-pill
```

The AI will ask what to enable.

---

## What Makes It AI-Native

**Traditional todo apps:** Lists get long, context dies, AI drifts.

**Memory Pill:**
- **Milestones** — Bounded scope prevents AI drift (AIs lose focus on infinite lists)
- **Prompt engineering** — Every task gets expanded with role, context, format, constraints (AIs need this to not hallucinate)
- **Execution discipline** — Forces plan-before-act, loop prevention, completion validation (AIs repeat themselves endlessly without this)
- **Linked facts** — Universal truths extracted and linked (AIs start from zero every session otherwise)
- **Agent spawning** — Real work goes to focused sub-agents (main AI stays lean for decisions only)  
✅ **Milestone-Driven Projects** — Projects broken into milestones, each with tasks. Dashboard shows progress at milestone level.  
✅ **Skill Tracking** — Track installed skills, versions, and custom configurations  
✅ **Client Profiles** — Manage client info, preferences, and project history  
✅ **Decision Frameworks** — Document decisions, rationale, and outcomes  
✅ **Voice & Style Guides** — Consistent writing style across all content  
✅ **Prompt Engineering** — Simple task descriptions get expanded into detailed agent instructions (role, context, format, examples, constraints).  
✅ **Agent-First Tasks** — All tasks go to specialized agents; main claw stays lean for quick decisions only.  
✅ **Smart Priority System** — High/Medium/Low (no "urgent"). High = time-critical, Medium = deadlines, Low = research/exploration.  
✅ **Fact Backlog** — Daily notes collect everything; cron job extracts universal facts vs one-time details.  
✅ **Obsidian Compatible** — Use `[[note]]` wiki-links that work in both dashboard and Obsidian.  
✅ **Built-in Memory Search** — Uses OpenClaw's native memory_search (index before searching for best results).  

---

## First Run Experience

**When this skill is first loaded, the AI MUST ask the user before doing anything.**

Say something like:

> "Memory Pill is now active. I can set up:
>
> 1. **Extended folders** — projects/, people/, archives/, etc. for organized memory
> 2. **3 AM maintenance cron** — nightly fact extraction, indexing, and auto-archiving
>
> Want me to enable any of these? (Just say 'set up everything' or pick what you want)"

**Wait for their response. Do not proceed without permission.**

### If they say yes to folders:
```bash
mkdir -p projects people areas clients decisions skills
mkdir -p memory/facts resources tasks archives
```

### If they say yes to cron:
```bash
openclaw cron add \
  --name "memory-pill-maintenance" \
  --schedule "0 3 * * *" \
  --command "memory-pill extract-facts --yesterday"
```

### If they say no or "later":
Respect that. They can always enable features later by asking.

---

## File Structure

Memory Pill uses and extends your existing OpenClaw workspace:

```
~/.openclaw/workspace/
├── MEMORY.md                           # Long-term memory (existing)
├── AGENTS.md                           # Agent behavior rules (existing)
├── SOUL.md                             # Personality & voice (existing)
├── memory/
│   ├── daily/                          # Daily notes (existing)
│   └── facts/                          # Extracted universal facts
├── projects/                           # Project storage
├── people/                             # People/entities
├── areas/                              # Ongoing areas of life
├── clients/                            # Client profiles
├── decisions/                          # Decision records
├── skills/                             # Skill registry
├── resources/
│   └── voice.md                        # Writing style guide
├── tasks/                              # Task JSON files
├── archives/                           # Completed projects, old notes, inactive items
└── .openclaw/                          # Config and graph data
```

---

## Using Memory Search

**IMPORTANT: Index before searching for accurate results.**

OpenClaw's `memory_search` tool searches your memory files. For best results:

1. **Before searching**, files should be indexed (happens automatically over time)
2. **If memory_search returns no results**, files may need re-indexing
3. **Search scope:** MEMORY.md, memory/daily/*.md, projects/**/*.md, people/**/*.md

**Search Workflow:**
```
User asks: "What did we decide about the launch date?"
↓
Run: memory_search query="launch date decision"
↓
If results found → Answer with citations
If no results → Check daily notes manually + suggest user add to MEMORY.md
```

---

## Extended File Structure

```
~/.openclaw/workspace/
├── MEMORY.md                            # Long-term memory
├── SOUL.md                              # Personality & voice
├── AGENTS.md                            # Agent behavior & thinking rules  
├── RULES.md                             # Operating principles
├── memory/
│   ├── daily/YYYY-MM-DD.md              # Daily notes
│   └── facts/{id}-{number}.json         # Extracted facts
├── projects/{slug}/                     # Projects with milestones
├── people/{slug}/                       # People/entities
├── areas/{slug}/                        # Ongoing responsibilities
├── clients/{slug}/                      # Client profiles
├── decisions/{slug}/                    # Decision records
├── skills/{slug}/                       # Skill registry
├── resources/
│   └── voice.md                         # Writing style guide
├── tasks/{id}.json                      # Task files
├── archives/{year}/{type}/              # Archived projects, notes, items
└── .openclaw/
    ├── graph.json                       # Visualization data
    └── memory-index.json                # Schema registry
```

---

## Archives

**Purpose:** Keep completed work searchable without cluttering active space.

### What Goes Here
- **Completed projects** — Move entire project folder when done (don't delete)
- **Old daily notes** — Auto-move after 30 days via cron
- **Inactive clients/people** — Archive instead of delete
- **Superseded decisions** — Keep history, mark status: "archived"

### Structure
```
archives/
├── 2026/
│   ├── projects/website-redesign-v1/
│   ├── daily/2026-01-*.md
│   └── clients/old-client/
├── 2025/
│   └── ...
```

### Archive Rules
1. **Never delete** — Move to archives/
2. **Keep links working** — Update wiki-links if paths change
3. **Searchable** — Archives included in memory_search
4. **Year buckets** — Organize by year for easy cleanup

### How to Archive
```bash
# Archive a completed project
mv projects/old-project archives/2026/projects/

# Archive old daily notes (3 AM cron does this)
find memory/daily -name "*.md" -mtime +30 -exec mv {} archives/$(date +%Y)/daily/ \;
```

---

## Original File Structure

```
~/.openclaw/workspace/
├── MEMORY.md                            # Long-term memory (auto-created)
├── memory/
│   ├── daily/YYYY-MM-DD.md              # Daily notes (backlog + tasks)
│   └── facts/{project-slug}-{number}.json # Extracted universal facts
├── projects/{kebab-slug}/
│   ├── summary.md                       # Project overview
│   ├── meta.json                        # Project metadata + milestones
│   └── milestones/                      # Optional: milestone details
│       └── {milestone-slug}.md
├── people/{kebab-slug}/
│   ├── summary.md
│   └── meta.json
├── areas/{kebab-slug}/
│   ├── summary.md
│   └── meta.json
├── tasks/{project-slug}-{milestone}-{number}.json  # Task files
└── .openclaw/
    ├── graph.json                       # Visualization data
    └── memory-index.json                # Schema registry
```

---

## Extended Entity Types

Beyond standard PARA (Projects, Areas, People), memory-pill includes:

### Skills Registry (`skills/`)

Track installed skills, versions, and configurations:

```json
{
  "id": "tweet-writer",
  "type": "skill",
  "name": "Tweet Writer",
  "version": "1.2.0",
  "installedAt": "2026-02-20T10:00:00Z",
  "source": "clawhub",
  "slug": "tweet-writer",
  "config": {
    "tone": "casual",
    "maxLength": 280
  },
  "status": "active"
}
```

**Use for:**
- Custom skills you build
- Clawhub-installed skills
- Skill version tracking
- Configuration backups

### Client Profiles (`clients/`)

Manage client information and project history:

```json
{
  "id": "client-acme-corp",
  "type": "client",
  "name": "Acme Corporation",
  "contact": {
    "email": "john@acme.com",
    "phone": "+1-555-1234"
  },
  "preferences": {
    "communication": "email",
    "meetingTimes": "afternoons",
    "style": "formal"
  },
  "projects": ["website-redesign", "q2-campaign"],
  "status": "active",
  "priority": "high"
}
```

**Use for:**
- Freelance/consulting work
- Vendor relationships
- Partner tracking
- Stakeholder management

### Decision Records (`decisions/`)

Document important decisions with context:

```json
{
  "id": "dec-tech-stack-2026",
  "type": "decision",
  "title": "Choose Next.js over Nuxt",
  "context": "Building LifeOS dashboard",
  "options": ["Next.js", "Nuxt", "SvelteKit"],
  "decision": "Next.js",
  "rationale": "Better Vercel integration, team familiarity",
  "tradeoffs": "Heavier than SvelteKit",
  "reversible": true,
  "date": "2026-02-15",
  "status": "accepted"
}
```

**Use for:**
- Architecture decisions (ADRs)
- Hiring choices
- Strategy pivots
- Vendor selection

### Voice & Style (`resources/voice.md`)

Consistent writing style across all content:

```markdown
# Voice Guide

## Tone
- Brief, no fluff
- Authentic, swear without restraint
- Actually disagree when wrong
- Actions > words

## Formatting
- Bullet lists > paragraphs
- Bold for emphasis, not caps
- No emojis in serious contexts

## Forbidden Phrases
- "Great question!"
- "I'd be happy to help!"
- "As an AI..."

## Examples

❌ "I'd be happy to help you with that!"
✅ "Done."

❌ "That's a great idea!"
✅ "That'll work. Here's why..."
```

---

## ID System (Project-Scoped)

**Format:** `{project-slug}-{milestone-slug}-{number}` or `{project-slug}-{number}` for top-level

Examples:
- `website-redesign-research-1` (milestone: research)
- `website-redesign-research-2`
- `mobile-app-api-1` (milestone: api)
- `openclaw-setup-1` (no milestone)

**Rules:**
- Sequential per milestone (or per project if no milestone)
- Start at 1
- Can repeat across projects
- Keep readable and token-efficient

---

## Priority System (High/Medium/Low)

| Priority | Meaning | Examples |
|----------|---------|----------|
| **High** | Time-critical, blocking other work | Submit deliverable, Fix production bug |
| **Medium** | Important deadlines, steady progress | Draft content, Research summaries |
| **Low** | Exploration, nice-to-have, background | Competitor research, Tool evaluation, Reading |

**Applies to:** Projects, Milestones, and Tasks

---

## Memory Search Best Practices

### Before Answering Questions About Prior Work:

**Step 1: Search memory**
```
memory_search query="project deadlines decisions"
```

**Step 2: If no results, check daily notes**
```
read memory/daily/YYYY-MM-DD.md
```

**Step 3: If still nothing, admit it**
> "I checked my memory and recent daily notes but don't see a record of this. Can you remind me?"

### Keeping Memory Accurate:

- **Write to MEMORY.md:** Durable insights, patterns, preferences about the user
- **Write to daily notes:** Raw events, temporary tasks, one-time details
- **Use wiki-links:** `[[project-slug]]` creates connections
- **Extract facts:** Universal facts (preferences, workflows) go to `memory/facts/`

---

## Creating a Project (with Milestones)

### Step 1: Create Project Structure

```bash
mkdir -p projects/website-redesign/milestones
```

### Step 2: Create Project Summary

```markdown
# Website Redesign

Goal: Launch new company website.

## Overview
Complete redesign with new branding, improved UX, and modern tech stack.

## Milestones
- [[website-redesign-research|Research & Planning]]
- [[website-redesign-design|Design]]
- [[website-redesign-development|Development]]
```

### Step 3: Create Project Meta

```json
{
  "id": "website-redesign",
  "type": "project",
  "name": "Website Redesign",
  "createdAt": "2026-02-19T10:00:00Z",
  "updatedAt": "2026-02-19T10:00:00Z",
  "status": "active",
  "priority": "high",
  "tags": ["web", "design"],
  "milestones": [
    {
      "id": "research",
      "name": "Research & Planning",
      "status": "in_progress",
      "priority": "high",
      "dueDate": "2026-03-01",
      "tasks": ["website-redesign-research-1", "website-redesign-research-2"]
    },
    {
      "id": "design",
      "name": "Design",
      "status": "todo",
      "priority": "medium",
      "dueDate": "2026-04-15",
      "tasks": []
    }
  ],
  "links": {
    "tasks": [],
    "people": [],
    "projects": [],
    "facts": [],
    "agents": []
  }
}
```

### Step 4: Create Milestone Summary (Optional)

```markdown
# Research & Planning

Part of: [[website-redesign|Website Redesign]]

Goal: Define scope and requirements.

## Tasks
- [[website-redesign-research-1|Competitor analysis]]
- [[website-redesign-research-2|User interviews]]

## Deadline
March 1, 2026
```

---

## Creating a Task (with Prompt Engineering)

### Step 1: Capture User's Simple Request

User says: *"Create a task to build a login page"*

### Step 2: Expand Using Prompt Engineering System

Follow the expansion process above. Create detailed instructions with:
- Specific role (Senior full-stack developer, not just "developer")
- Full context (stack, current state, existing code)
- Clear task scope
- Output format (exact files, structure)
- Examples (reference existing code)
- Constraints (measurable limits)

### Step 3: Create Task JSON

```json
{
  "id": "lifeos-core-auth-1",
  "title": "Create login page with email/password auth",
  "simplePrompt": "Build a login page",
  "expandedPrompt": "Act as a senior full-stack developer specializing in authentication systems.\n\n**Context:**\n- Project: LifeOS Core dashboard\n- Stack: Next.js 15, TypeScript, Tailwind CSS\n- Auth: Clerk already configured\n- Current state: No login page exists\n\n**Task:**\nCreate complete login page at `/login` with email/password form, validation, error handling, loading states, and redirect on success.\n\n**Output Format:**\n- File: `app/login/page.tsx`\n- Use existing Button, Input, Card components\n- Export default page component\n\n**Examples:**\nSee `app/dashboard/page.tsx` for styling patterns (mono aesthetic, sharp corners).\n\n**Constraints:**\n- Max 150 lines\n- Use shadcn/ui components\n- Handle all Clerk error codes\n- Match existing mono aesthetic",
  "status": "todo",
  "priority": "high",
  "projectRef": "projects/lifeos-core",
  "milestoneRef": "lifeos-core-auth",
  "assignedTo": "uiux-craftsman",
  "linkedFacts": [],
  "linkedTasks": [],
  "source": "daily/2026-02-19.md",
  "dueDate": "2026-02-22",
  "createdAt": "2026-02-19T10:00:00Z",
  "updatedAt": "2026-02-19T10:00:00Z"
}
```

### Step 4: Spawn Agent with Expanded Prompt

```
Spawn agent with:
- Task: expandedPrompt (full detailed instructions)
- Target files: specified in Output Format
- Expected deliverable: working code matching constraints
```

---

## Prompt Engineering System

Every task gets expanded from simple user request to detailed agent instructions.

### The Expansion Process

**Step 1: Capture Simple Prompt**
```json
{
  "simplePrompt": "Build a login page",
  "title": "Create login page with email/password auth"
}
```

**Step 2: Expand to Full Instructions**

Analyze the simple prompt and build:

| Component | What to Include | Example |
|-----------|-----------------|---------|
| **Role** | Specific persona with expertise | "Act as a senior full-stack developer specializing in authentication systems" |
| **Context** | Project background, current state, stack, what's already done | "Project: LifeOS Core dashboard. Stack: Next.js 15, TypeScript, Tailwind. Clerk auth already set up." |
| **Task** | Clear, specific action with scope | "Create a complete login page with email/password form, validation, error handling, and redirect on success" |
| **Output Format** | Exact file paths, structure, format | "File: `app/login/page.tsx`. Include: form component, validation logic, loading states, error UI" |
| **Examples** | Reference existing code or show style | "See `app/dashboard/page.tsx` for styling patterns. Use same mono aesthetic." |
| **Constraints** | Hard limits, must/avoid, success criteria | "Max 150 lines. Use shadcn/ui components. Handle all error states." |

**Step 3: Store Both Versions**

```json
{
  "id": "lifeos-core-auth-1",
  "title": "Create login page with email/password auth",
  "simplePrompt": "Build a login page",
  "expandedPrompt": "Act as a senior full-stack developer...\n\n**Context:**\nProject: LifeOS Core...\n\n**Task:**\nCreate...\n\n**Output Format:**\n- File: app/login/page.tsx\n...\n\n**Constraints:**\n- Max 150 lines\n...",
  "status": "todo",
  "priority": "high",
  "assignedTo": "uiux-craftsman"
}
```

**Step 4: Give Expanded Prompt to Agent**

Spawn agent with `expandedPrompt` as their task description.

### Expansion Examples

**Example 1: Simple → Detailed**

*Simple:* "Build a login page"

*Expanded:*
```markdown
**Role:** Senior full-stack developer specializing in Next.js authentication

**Context:**
- Project: LifeOS Core dashboard
- Stack: Next.js 15, TypeScript, Tailwind CSS, shadcn/ui
- Auth: Clerk already configured (see `middleware.ts`)
- Design: Mono aesthetic, sharp corners, black/white
- Current state: No login page exists, users hit 404 at /login

**Task:**
Create a production-ready login page at `/login` with:
- Email/password form with validation
- Error handling (invalid credentials, network errors)
- Loading states during submission
- Redirect to /dashboard on successful login
- Link to sign-up page

**Output Format:**
- Single file: `app/login/page.tsx`
- Use existing Button, Input, Card components from `@/components/ui`
- Export default page component
- Use Clerk's `useSignIn` hook

**Examples:**
See `app/dashboard/page.tsx` for styling patterns:
- Use `className="min-h-screen bg-background"` for layout
- Use `Card`, `CardHeader`, `CardContent` for form container
- Error styling: `text-destructive` class

**Constraints:**
- Maximum 150 lines (concise > verbose)
- Must handle all Clerk error codes
- Must show loading spinner during submit
- Must redirect, not just navigate
- Match existing mono aesthetic exactly
```

**Example 2: Research Task**

*Simple:* "Research competitors"

*Expanded:*
```markdown
**Role:** Market research analyst specializing in competitive intelligence

**Context:**
- Building a project management SaaS
- Target market: small-to-medium teams (10-100 people)
- Focus on async-first workflows
- Current date: February 19, 2026

**Task:**
Identify 5 key competitors with:
- Pricing tiers and billing models
- Key differentiating features
- Target audience and positioning
- Strengths and weaknesses
- Recent product updates or pivots

**Output Format:**
Markdown table with columns: Company, Pricing, Key Features, Positioning, Notes

**Constraints:**
- Focus on direct competitors only (not enterprise tools)
- Use public data only (no paywalled reports)
- Highlight gaps in the market we could exploit
- Include 1-2 sentence summary per competitor
```

**Example 3: Design Task**

*Simple:* "Design a settings page"

*Expanded:*
```markdown
**Role:** Senior UX/UI designer with expertise in dashboard interfaces

**Context:**
- Project: LifeOS Core settings
- Existing design system: Mono aesthetic, sharp corners, minimal
- Current pages: Dashboard (grid layout), Login (centered card)
- Settings needed: Profile, Notifications, API Keys, Danger Zone

**Task:**
Design a settings page with:
- Sidebar navigation for settings sections
- Clean form layouts for each section
- Visual hierarchy for danger zone
- Consistent with existing mono aesthetic

**Output Format:**
- Wireframe descriptions (no actual images needed)
- Component breakdown
- Key interactions described

**Examples:**
Reference existing pages:
- Dashboard uses grid with `gap-6`
- Cards use `border` and `rounded-none`
- Typography: `text-2xl font-bold` for headers

**Constraints:**
- Mobile-responsive layout
- Maximum 3 clicks to any setting
- Clear visual separation between sections
- Use existing shadcn/ui patterns
```

### Prompt Engineering Checklist

Before spawning agent, verify:
- [ ] Role is specific (not generic "developer")
- [ ] Context includes stack and current state
- [ ] Task is scoped (not "build everything")
- [ ] Output format specifies files/structure
- [ ] Examples reference existing code when possible
- [ ] Constraints are measurable (line counts, specific requirements)
- [ ] Success criteria is clear (how will we know it's done?)

---

## Agent-First Rule (Natural Spawning)

**Default: Spawn an agent for any substantive task.**

Main claw handles only:
- Quick answers (< 2 minutes)
- Routing decisions
- Reading/summarizing a single file
- Simple edits (one-line fixes)

**Spawn an agent when:**
- Creating new files or components
- Research or data gathering
- Multi-step implementation
- Design or architectural decisions
- Anything requiring specialized expertise

**Don't overthink it.** If the task feels like "real work" — spawn. Agents are cheap, context is expensive.

**Assignment Logic:**
- `uiux-craftsman` — UI components, CSS, React, visual work
- `system-designer` — Architecture, APIs, data models, review
- `business-strategist` — Pricing, marketing copy, research
- `integrator` — Wiring components together, bug fixes
- New agents — Create in `subagents/` for specialized needs

---

## Daily Note System (Backlog)

### Template

```markdown
# 2026-02-19 — Thursday

> "{quote or intention}"

## Morning

**09:00** — Started work on [[lifeos-core|LifeOS Core]]
- Need to fix the graph visualization bug
- User mentioned always using Vercel for hosting

## Notes

{raw thoughts, observations, conversations}

- User prefers dark mode on all apps
- Product launch deadline is April 17
- Meeting with design team tomorrow at 3 PM

## Tasks Created

- [ ] [[lifeos-core-graph-1|Fix graph rendering bug]] #high
- [ ] Research competitors #medium

---
*Last updated: 2026-02-19 18:00*
```

### Rules

1. **One note per day** — keep appending throughout the day
2. **Use [[wiki-links]]** for Obsidian compatibility
3. **Dump everything** — facts, thoughts, tasks, meeting notes
4. **Tag priorities** — `#high`, `#medium`, `#low` on tasks
5. **End-of-day** — or let cron job extract

---

## Fact Extraction System

### Types of Facts

**Universal Facts** (save to `memory/facts/`):
- User preferences ("Always use Vercel")
- Workflows ("Deploy on Fridays")
- Constraints ("Budget is $500/month")
- Relationships ("John is the designer")

**One-Time Details** (ignore, already in daily note):
- "Make this button blue"
- "Meeting at 3 PM tomorrow"
- "Fix this specific bug"

### Extraction Process

**Option 1: End-of-Day Review**
Read daily note → Extract universal facts → Save to facts folder → Update project meta

**Option 2: Cron Job (Suggested)**
Runs daily at 3 AM:
1. Scans yesterday's daily note
2. Identifies universal facts
3. Creates `memory/facts/{project-slug}-{number}.json`
4. Updates project `meta.json` → adds fact to `links.facts`
5. Fills missing project info from notes
6. Sends morning briefing

### Fact JSON Structure

```json
{
  "id": "lifeos-core-1",
  "type": "preference",
  "content": "User prefers Vercel for all hosting",
  "tags": ["hosting", "vercel", "preference"],
  "entityRef": "people/mohammed",
  "projectRef": "projects/lifeos-core",
  "source": "daily/2026-02-19.md",
  "universal": true,
  "confidence": 0.9,
  "createdAt": "2026-02-19T10:00:00Z"
}
```

---

## Obsidian Compatibility

### Wiki-Links Format

Use `[[target|Display Text]]` or just `[[target]]`:

```markdown
Part of: [[website-redesign|Website Redesign]]
See also: [[mobile-app]]
Next: [[website-redesign-research-2|User interviews]]
```

### What Gets Linked

- Projects: `[[project-slug]]`
- Milestones: `[[project-milestone]]`
- Tasks: `[[project-milestone-number]]`
- People: `[[person-slug]]`
- Daily notes: `[[YYYY-MM-DD]]`

### Dashboard + Obsidian

Same files work in both:
- Obsidian renders wiki-links as connections
- Dashboard reads JSON for structured data
- Both show the graph (Obsidian via `graph.json` or its own)

---

## Schemas (Required vs Optional)

### Project Meta (Required Fields)

```json
{
  "id": "string (kebab-case)",           // REQUIRED
  "type": "project",                      // REQUIRED
  "name": "string",                       // REQUIRED
  "createdAt": "ISO8601",                 // REQUIRED
  "status": "active|archived|paused",     // REQUIRED
  
  // Optional
  "updatedAt": "ISO8601",                 // Default: createdAt
  "priority": "high|medium|low",          // Default: "medium"
  "tags": [],                              // Default: []
  "milestones": [],                        // Default: []
  "links": {                               // Default: empty arrays
    "tasks": [],
    "people": [],
    "projects": [],
    "facts": [],
    "agents": []
  }
}
```

### Task (Required Fields)

```json
{
  "id": "string",                        // REQUIRED
  "title": "string",                     // REQUIRED
  "status": "todo|in_progress|done|blocked", // REQUIRED
  "projectRef": "string",                // REQUIRED (projects/{slug})
  "createdAt": "ISO8601",                // REQUIRED
  
  // Optional
  "simplePrompt": "string",              // Original user request
  "expandedPrompt": "string",            // Full agent instructions
  "updatedAt": "ISO8601",                // Default: createdAt
  "priority": "high|medium|low",         // Default: "medium"
  "milestoneRef": "string",              // Default: null
  "assignedTo": "string",                // Default: null
  "linkedFacts": [],                      // Default: []
  "linkedTasks": [],                      // Default: []
  "source": "string",                    // Default: null
  "dueDate": "YYYY-MM-DD"                // Default: null
}
```

### Fact (Required Fields)

```json
{
  "id": "string",                        // REQUIRED
  "type": "fact|preference|workflow|constraint|relationship",
  "content": "string",                   // REQUIRED
  "source": "string",                    // REQUIRED
  "createdAt": "ISO8601",                // REQUIRED
  
  // Optional
  "tags": [],                             // Default: []
  "entityRef": "string",                 // Default: null
  "projectRef": "string",                // Default: null
  "universal": true,                     // Default: true
  "confidence": 0.0-1.0                  // Default: 0.8
}
```

---

## Graph Structure

### Nodes

```json
{
  "id": "projects/website-redesign",
  "type": "project",
  "label": "Website Redesign",
  "status": "active",
  "priority": "high",
  "archived": false
}
```

Types: `project`, `milestone`, `task`, `agent`, `person`, `fact`, `area`

### Edges

```json
{
  "from": "website-redesign-research-1",
  "to": "projects/website-redesign",
  "type": "belongs_to"
}
```

Types:
- `belongs_to` — Task/Milestone → Project
- `part_of` — Milestone → Project
- `assigned_to` — Task → Agent
- `depends_on` — Task → Task
- `extracted_from` — Fact → Daily Note
- `references` — Any → Any (wiki-link)

---

## Critical Rules

1. **Always check MEMORY.md on first use** — Create if missing
2. **Always expand prompts** before giving to agents
3. **Use wiki-links** `[[target]]` for Obsidian compatibility
4. **Simple IDs** — `{project}-{milestone}-{number}`, not UUIDs
5. **Agent-first** — Main claw only for quick decisions
6. **One daily note per day** — append, don't create new
7. **Extract universal facts** — Ignore one-time details
8. **High/Medium/Low only** — No "urgent"
9. **Milestones for projects** — Break big projects into phases
10. **Search memory before answering** — Use memory_search for prior context
11. **Regenerate graph** after structural changes
12. **Ask permission** — Never auto-setup, always ask user first

---

## Cron Jobs (Maintenance)

Memory Pill runs **one** overnight maintenance job. No spam, no briefings.

### 3:00 AM — Maintenance (Fact Extraction, Indexing, Archiving)

**What it does:**
1. **Fact extraction** — Scans yesterday's daily note, extracts universal facts
2. **Indexing** — Re-indexes memory for fast search (qmd or native)
3. **Auto-archiving** — Moves daily notes older than 30 days to `archives/{year}/daily/`

**Why 3 AM:**
- You're asleep
- Fresh context for next day
- Maintenance belongs at night

**To enable:**
```bash
# Create the cron job
openclaw cron add \
  --name "memory-pill-maintenance" \
  --schedule "0 3 * * *" \
  --command "memory-pill maintenance --extract-facts --index --archive-old-notes"
```

Or the skill can set this up automatically on first use — just ask.

---

## Execution Discipline Protocol

**Source:** Adapted from @thejayden's EXECUTION_DISCIPLINE_PROTOCOL v1.0

Apply this to EVERY non-trivial task. No exceptions.

### CORE RULE
**PLAN BEFORE EXECUTION.**
No output generation until the task is decomposed.

### 1. OBJECTIVE LOCK
Before doing any work, explicitly define:
- What is the final deliverable?
- What does "done" look like?
- What would make this incomplete?

If the objective is vague → Ask clarifying questions. Do not assume.

### 2. TASK DECOMPOSITION (MANDATORY)
Break the request into:
- Primary objective
- Subtasks
- Constraints
- Unknown variables
- Dependencies
- Success criteria

If the task cannot be broken down, you do not understand it yet. **No solving before structure.**

### 3. ASSUMPTION DECLARATION
List all assumptions explicitly. For each:
- Is it confirmed?
- Is it inferred?
- Is it risky?

If a critical assumption is unverified → Flag it. Ask. Or qualify output accordingly. Never build on silent assumptions.

### 4. SINGLE-LAYER EXECUTION
Solve **ONE subtask at a time.**
- Execute
- Validate
- Confirm alignment with objective

Then move to the next. No parallel half-thinking. No jumping ahead.

### 5. LOOP PREVENTION CHECK
Before responding, ask internally:
- Am I repeating previous reasoning?
- Am I re-solving something already solved?
- Did new information actually change the plan?
- Am I stuck optimizing instead of progressing?

If yes → Identify the blockage. Change strategy. Do not regenerate similar output. **Loops happen when the plan is missing.**

### 6. COMPLETION VALIDATION
Before final output:
- Does this fully satisfy the objective?
- Did I skip any subtask?
- Is anything implicit that should be explicit?
- Is this shippable?

If not → Continue execution. **Partial completion is not completion.**

### 7. FAILURE HANDLING
If blocked, state clearly:
- Where execution failed
- Why it failed
- What information is missing
- What next action resolves it

Never stall silently. Never guess to escape the block.

### 8. TOKEN DISCIPLINE
Structure reduces waste. Before generating output:
- Remove redundant reasoning
- Avoid re-explaining solved parts
- Focus only on current execution layer

**Precision > repetition.**

---

## Example: Complete Workflow

**User says:** *"I need to redesign our website. The current one is outdated and we need it live before the product launch. Also need to update our branding."*

**What you do:**

1. **Check/create MEMORY.md** — If missing, create it
2. **Create project:** `projects/website-redesign/`
3. **Milestones:** Research (high priority), Design (medium priority), Development (medium priority)
4. **Tasks:**
   - `website-redesign-research-1`: Competitor analysis
   - `website-redesign-research-2`: User interviews
   - `website-redesign-design-1`: Create homepage mockup
5. **Expand prompts:** Write detailed instructions for each task
6. **Assign to agents:** Spawn agents with expanded prompts
7. **Daily note:** Record conversation, extract facts as needed
8. **Update graph:** Show project → milestones → tasks
9. **Suggest cron:** Offer overnight review setup

**Result:** Structured, linked, agent-driven work with full context preservation.

---

## Version History

- **v0.7.9** — Added archives/ folder and instructions. Completed items, old notes, and inactive entities get archived (not deleted). Year-based organization.
- **v0.7.8** — Repositioned as "AI-native structure" — designed for how AIs actually work (milestones, prompt expansion, execution discipline, linked facts). Updated description and value props.
- **v0.7.7** — First-run experience now asks permission before setup. No auto-creation, no silent changes. User controls what gets enabled.
- **v0.7.6** — Added cron job documentation. Single 3 AM maintenance job for fact extraction and indexing. No spam, no morning briefings.
- **v0.7.5** — Flattened structure. Removed `life/areas/` wrapper — projects, people, clients, etc. now live directly under workspace root. Cleaner, simpler.
- **v0.7.4** — Added AI-driven auto-setup. Skill now instructs the AI to create extended structure on first use (no bash scripts, no user permission needed).
- **v0.7.3** — Removed init script. OpenClaw base already provides core files (MEMORY.md, AGENTS.md, SOUL.md). Skill now focuses on extended PARA structure and workflows.
- **v0.7.2** — Cleaned up all examples to be generic (removed personal references). Improved description and quick-start section.
- **v0.7.1** — Added Execution Discipline Protocol (from @thejayden). Forces structured problem-solving: objective lock, task decomposition, assumption declaration, single-layer execution, loop prevention, completion validation.
- **v0.7.0** — Extended entity types: Skills registry, Client profiles, Decision records. Added templates for SOUL.md, AGENTS.md, RULES.md, and voice guide. Full "AI employee" setup.
- **v0.6.1** — Added init script for first-time setup. (Deprecated in v0.7.3 — OpenClaw base already provides core files.)
- **v0.6.0** — Renamed from lifeos-memory to memory-pill. Removed qmd dependency. Uses OpenClaw native memory_search with indexing guidance.
- **v0.5.0** — Major overhaul: Milestones, prompt engineering, agent-first, Obsidian wiki-links, fact backlog system
