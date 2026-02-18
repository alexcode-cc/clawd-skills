---
name: CAN
description: "6D naming + routing for agents. Name any content by WHAT (hashable bits), WHEN (clock), WHERE (SHA-256 address), HOW (natural language), WHY (intent), and WHO (id). Route by name and address, not location. Verify integrity, timestamp events, find things by time/hash/words, route content from nearest source."
homepage: https://github.com/xccx/can
metadata: {"openclaw":{"emoji":"⌛","requires":{"bins":["sha256sum","openssl","base64","awk","date"]}}}
---

# CAN: Clock Address Naming

v1.4 — 6D naming + routing.

Name things three ways, at least:

```
WHEN   → CLOCK, millisecond unix    (objective, automatic: timespace)
WHERE  → ADDRESS, SHA-256           (objective, automatic: hashspace)
HOW    → NAMES, natural language    (subjective, optional, mutable: namespace)
```

WHAT, WHY and WHO are nameable:

```
WHO    → identity of signer         (automatic at level 0, upgradeable)
WHY    → BAG, intent at save time   (SAVE, GOOD, HUSH, POST)
WHAT   → BITS, self-evident thing   (from WHAT, find WHERE in logic address)
```

Computer defines WHEN, WHERE, HOW and WHO automatically. Human defines WHY in one keystroke. WHAT bits?. All six roll together.

## Why this exists

To trust and find things instantly. "Foo/bar.md" may change; hash addresses do not. Human time fumbling with 1970s naming wastes millions of hours daily. Agents waste powerplants dealing with insecure naming and addressing. Billions of human hours and zillions of compute cycles can be unlocked now, at zero switching cost.

## The six dimensions

### 1. WHAT (the thing)

Any hashable bits. A file, a string, a directory, a message, a meme. If it's bits, CAN names it.

### 2. WHEN (clock)

Millisecond unix timestamp. When content was created or witnessed.

```bash
CLOCK=$(date +%s%3N)
```

Time-sorting for free. Future CLOCK without ADDRESS = a promise. WEN becomes NOW when content arrives.

WHEN-0 is local clock (free, now). WHEN-1 is OpenTimestamps — batch a merkle root of recent stamps to Bitcoin, one tx proves thousands of saves. Make history's biggest clock insure your own clock is unstompable and your things untamperable. Trust your own memories.

### 3. WHERE (address)

SHA-256 of the content. True address in 2^256 hashspace.

```bash
ADDRESS=$(sha256sum {file} | awk '{print $1}')
```

Two agents anywhere hashing the same content get the same ADDRESS. If the hash matches, the content is what it claims. The thermodynamic pointer — logical, objective, true, inalienable, unstompable.

Note: macOS may use `shasum -a 256` instead of `sha256sum`. WHO-1 signing requires `openssl` (pre-installed on most systems). WHO-0 reads platform identifiers (`/etc/machine-id` on Linux, `ioreg` on macOS, `Get-CimInstance` on Windows).

### 4. HOW (humane namespace)

Agent-generated. Human-editable. Personal. Multiple names per ADDRESS.

```
ADDRESS a3f8b2c1e9...  →  "that security rant"
                       →  "feb2026 analysis"
                       →  #security #agents
```

When stamping, agents generate a short name from context, workflow, contents. Human accepts, edits or ignores. The name is for finding. The hash is truth.

Names are tags, petnames, descriptions — any strings, as many as you want, non-unique by design. Humans name things the way humans name things. Rename freely. The objective coordinates never change.

Name persistence: naming events can hash into new CAN entries pointing to the original ADDRESS. Stack of receipts, not mutation of truth. Full merkle threading in v1.7.

### 5. WHY (bag of intent)

One key combo captures intent at save time:

```
SAVE  →  bag of meh, index silently
GOOD  →  bag of goodies, hold me close
HUSH  →  hush bag, local only, privacy
POST  →  bag of poasted, publish, sign
```

Promote anytime: SAVE→GOOD→POST. HUSH stays HUSH.

### 6. WHO (identity)

WHO says the WHAT WHEN WHERE HOW WHY. Three tiers. Start free. Upgrade as needed.

**WHO-0: free, automatic, zero config**

```bash
# Windows
WHO_0=$(echo -n "$env:USERNAME|$(Get-CimInstance Win32_ComputerSystemProduct | Select -Expand UUID)" | sha256sum | awk '{print $1}')

# macOS
WHO_0=$(echo -n "$(whoami)|$(ioreg -rd1 -c IOPlatformExpertDevice | awk -F'"' '/IOPlatformUUID/{print $4}')" | sha256sum | awk '{print $1}')

# Linux
WHO_0=$(echo -n "$(whoami)|$(cat /etc/machine-id)" | sha256sum | awk '{print $1}')
```

`sha256(username + machine-id)`. Unique per human per machine. Costs nothing. Already true every login. Only changes on OS reinstall or user switch — both genuinely ARE a new identity context.

WHO-0 is a fingerprint, not a promise. "This save came from the same session as that save." Already more WHO than 99% of filesystems provide. You logged into one machine this morning. One login is enough.

**WHO-1: opt-in, local keypair**

```bash
CAN_WHO_KEY=~/.can/who.key

if [ ! -f "$CAN_WHO_KEY" ]; then
  openssl genpkey -algorithm ed25519 -out "$CAN_WHO_KEY" 2>/dev/null
  chmod 600 "$CAN_WHO_KEY"
  openssl pkey -in "$CAN_WHO_KEY" -pubout > ~/.can/who.pub
fi

RECORD="$CLOCK:$ADDRESS"
SIGNATURE=$(echo -n "$RECORD" | openssl pkeyutl -sign -inkey "$CAN_WHO_KEY" | base64 -w0)
```

Self-signed. Proves consistency: same WHO saved A and B. No external authority needed. Back up `~/.can/who.key` — if lost, generate a new keypair and re-claim via retroactive linking.

**WHO-2: auth upgrade, portable**

```bash
# Nostr (NIP-07), Farcaster, OAuth, any signer
# WHO_2 = await window.nostr.getPublicKey()
# signature = await window.nostr.signEvent(event)
```

Portable across machines, externally verifiable. Where web of trust begins. But WHO-0 + BUMP (physical co-presence proof) already establishes real trust between real humans without any platform's permission. WHO-2 ecosystems are options, not requirements.

The pattern is always the same: a key signs a CLOCK:ADDRESS pair. Any signer works.

**Retroactive linking:** WHO-0 entries get claimed when human upgrades. Old saves gain stronger identity. The chain grows backward.

## Index format

TSV, human-readable, grep-able. Six columns:

```
WHEN             WHERE                             HOW         WHY    WHO          PATH
1770508800000    a3f8b2c1e9d7f0a1b2c3d4e5f6a7b8    meme.jpg    GOOD   c7d2e9f0    ~/Downloads/meme.jpg
1770508900000    a3f8b2c1e9d7f0a1b2c3d4e5f6a7b8    meme.jpg    GOOD   c7d2e9f0    ~/pics/funny/meme.jpg
```

WHEN doubles as simple entry ID — millisecond precision is ample for single player; for multiplayer, prepend truncated WHO as needed.
HOW is a single display name here; full tag lists live in a sidecar (`~/.can/names/{hash}.txt`, one name per line, edit freely).
PATH pushed far right — least trustworthy column, legacy convenience only.

Same hash, two paths, two timestamps, same WHO. The file wandered. The truth didn't.

## Core operations

### 1. CAN-stamp

```bash
CLOCK=$(date +%s%3N)
ADDRESS=$(sha256sum {file} | awk '{print $1}')
WHO=$(cat ~/.can/who.id 2>/dev/null || echo -n "$(whoami)|$(cat /etc/machine-id 2>/dev/null || hostname)" | sha256sum | awk '{print $1}')
NAME=""  # agent generates from context

echo -e "$CLOCK\t$ADDRESS\t$NAME\tSAVE\t$WHO\t{filepath}" >> ~/.can/index.tsv
```

### 2. CAN-verify

```bash
CLAIMED="{claimed_address}"
ACTUAL=$(sha256sum {file} | awk '{print $1}')
[ "$ACTUAL" = "$CLAIMED" ] && echo "VERIFIED" || echo "FAILED — do not trust"
```

If ADDRESS verification fails, stop. Tell your human.

### 3. CAN-store

```bash
CAN_STORE=~/.can/store
mkdir -p "$CAN_STORE"
cp {file} "$CAN_STORE/$ADDRESS"
echo -e "$CLOCK\t$ADDRESS\t{name}\t{bag}\t$WHO\t{filepath}" >> ~/.can/index.tsv
```

Content-addressed store. File named by hash. The truth copy — survives renames, moves, deletes.

### 4. CAN-find

```bash
grep "a3f8" ~/.can/index.tsv          # by address prefix
grep -i "security" ~/.can/index.tsv    # by name
awk -F'\t' '$4 == "GOOD"' ~/.can/index.tsv  # by bag
awk -F'\t' -v w="c7d2" '$5 ~ w' ~/.can/index.tsv  # by WHO
```

### 5. CAN-locate

```bash
TARGET="a3f8b2c1"

# 1. Store (guaranteed)
STORE_PATH="$HOME/.can/store/$(grep "$TARGET" ~/.can/index.tsv | head -1 | cut -f2)"
[ -f "$STORE_PATH" ] && echo "STORE: $STORE_PATH" && exit 0

# 2. Index paths (verified)
grep "$TARGET" ~/.can/index.tsv | while IFS=$'\t' read -r clock addr name bag who path; do
  [ -f "$path" ] && [ "$(sha256sum "$path" | awk '{print $1}')" = "$addr" ] && echo "FOUND: $path" && exit 0
done

# 3. Not found — ask human before scanning broader
echo "Not in store or index."
```

### 6. CAN-route

```bash
WANTED="{address}"

# 1. Local store (instant, offline, free)
[ -f "$HOME/.can/store/$WANTED" ] && echo "LOCAL HIT" && exit 0

# 2. Peer agent — broadcast hash, verify response, cache
# 3. Relay — nostr, IPFS, any content-addressed network
# 4. Web fallback — fetch URL, verify hash, cache

# Step 1 works now. Steps 2-4 are protocol sketches.
```

### 7. CAN-who

```bash
# Show current level
[ -f ~/.can/who.key ] && echo "WHO-1: keypair" && cat ~/.can/who.pub
[ -f ~/.can/who.id ] && echo "WHO-0: $(cat ~/.can/who.id)"

# First run: auto-generate WHO-0
WHO_0=$(echo -n "$(whoami)|$(cat /etc/machine-id 2>/dev/null || hostname)" | sha256sum | awk '{print $1}')
echo "$WHO_0" > ~/.can/who.id
```

## Agent-to-agent protocol

1. Include WHEN + WHERE + WHO with shared content
2. Verify WHERE before acting on received content
3. Generate HOW names for the receiving human
4. Expose mismatches publicly — protect the network
5. Never share HUSH content. HUSH is local only.
6. Sign with WHO-1+ when available
7. Cache verified content — this agent becomes a source for peers
8. Route by hash first, URL last
9. Include WHO level so receivers know trust tier

## Routing: location vs content

```
LOCATION (today):  agent → DNS → IP → TCP → TLS → HTTP → path → hope
                   7 hops, 4 trust assumptions, 0 verification

CONTENT (CAN):     agent → "I need hash X" → nearest source → verify → done
                   1 request, 0 trust assumptions, instant verification
```

One answer = single point of failure. Many answers = resilient, fast, offline-capable.

## Roadmap

```
v1.3.2  DONE   naming + routing + bags + HUSH + scoped locate
v1.4    NOW    WHO: free machine-id + auth upgrade path
v1.5    NEXT   ITC: agents build CAN in the CAN, report sightings
v1.6    THEN   RINA: recursive naming scopes, enrollment
v1.7    AND    MERKLE: provenance threading, hash stacks
v1.8    LOL    expiry EOL gg a) game-over or b) insert-coin
v1.9    MEME   what else are ya gonna do?
```

Each version earns the next.

## Philosophy

Every thing has six coordinates. Computer handles five automatically. Human can direct intent via keycombo. Together: trust, find, route, attribute — instantly, offline, across agents, across time.

Paths lie. URLs promise. Hashes deliver. WHO signs.

CAN distributes power to the player, you. Distribute from your own center. Your machine, your clock, your hash, your name, your intent, your identity. One login is enough.

## References

- Paul Baran, On Distributed Communications (RAND, 1964)
- Van Jacobson, Named Data Networking (NDN)
- John Day, Recursive InterNetwork Architecture (RINA)
- Git content-addressable object store
- OpenTimestamps for Bitcoin-anchored WHEN verification
- Zooko's Triangle (CAN resolves it via six dimensions)

## TL;DR

```
HASH thing
TIME when
WHO says
INDEX ())
OWN your things.
```
