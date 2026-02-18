# CAN: Clock Address Naming

6D naming + routing for agents and humans.

```
WHEN   = clock      (millisecond unix timestamp)
WHERE  = address    (SHA-256 content hash)
HOW    = names      (petnames, tags, whatever you want)
```

Plus three more dimensions:

```
WHO    = identity   (free machine-id → keypair → nostr/farcaster/oauth)
WHY    = bags       (SAVE, GOOD, HUSH, POST)
WHAT   = bits       (the thing itself)
```

## What

Every thing gets named three ways at minimum: by time, by content hash, and by human words. Computer handles WHEN, WHERE, HOW and WHO automatically. Human adds WHY in one keystroke. Both find things fast.

## Why

Paths lie. Hashes don't. Timestamps prove ordering. Names make it findable. WHO proves accountability. Agents waste powerplants on security theatre — DNS lookups, TLS negotiation, certificate validation, redirect chains — plus expensive reasoning about whether what they fetched is real. CAN eliminates that entire category. Hash matches = done thinking. WHO matches = done wondering.

## WHO: identity in three tiers

- **WHO-0** (free): `sha256(username + machine-id)`, automatic, zero config. One login is enough.
- **WHO-1** (opt-in): local ed25519 keypair, proves consistency across saves
- **WHO-2** (auth): Nostr, Farcaster, OAuth — portable, externally verifiable

Start free. Upgrade when you need to. Old saves get retroactively claimed.

## Bags

One keystroke captures intent at save time:

```
SAVE  →  bag of meh, index silently
GOOD  →  bag of goodies, hold me close
HUSH  →  hush bag, local only, privacy
POST  →  bag of poasted, publish, sign
```

Promote anytime: SAVE → GOOD → POST. HUSH stays HUSH.

## Routing

```
LOCATION (today):  agent → DNS → IP → TCP → TLS → HTTP → path → hope
                   7 hops, 4 trust assumptions, 0 verification

CONTENT (CAN):     agent → "I need hash X" → nearest source → verify → done
                   1 request, 0 trust assumptions, instant verification
```

## Install

```
clawhub install xccx/can
```

## Quick test

```bash
CLOCK=$(date +%s%3N)
ADDRESS=$(echo -n "hello world" | sha256sum | awk '{print $1}')
WHO=$(echo -n "$(whoami)|$(cat /etc/machine-id 2>/dev/null || hostname)" | sha256sum | awk '{print $1}')
echo "$CLOCK $ADDRESS WHO:${WHO:0:8} greeting:hello"
```

## Requirements

`sha256sum` (pre-installed on most Linux; use `shasum -a 256` on macOS). WHO-1 signing uses `openssl` (pre-installed on most systems). Also uses `awk`, `date`, `base64` — standard on Linux and macOS. No npm. No pip. No runtime. Works air-gapped.

## Roadmap

```
v1.3.2  DONE   naming + routing + bags + HUSH
v1.4    NOW    WHO: free machine-id + auth upgrade path
v1.5    NEXT   ITC: agents build CAN in the CAN
v1.6    THEN   RINA: recursive naming scopes
v1.7    AND    MERKLE: provenance threading
v1.8    LOL    game-over or insert-coin
v1.9    MEME   what else are ya gonna do?
```

Each version earns the next.

## TL;DR

```
HASH thing
TIME when
WHO says
INDEX ())
OWN your things.
```

## References

- Paul Baran, On Distributed Communications (RAND, 1964)
- Van Jacobson, Named Data Networking (NDN)
- John Day, Recursive InterNetwork Architecture (RINA)
- Git content-addressable object store
- OpenTimestamps for Bitcoin-anchored WHEN verification
- Zooko's Triangle (CAN resolves it via six dimensions)

## License

Public domain.
