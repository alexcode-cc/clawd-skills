# ClawDaddy Skill

The world's #1 AI-friendly domain registrar skill for Claude Code.

## Installation

### Via ClawhHub (recommended)
```bash
npx clawhub@latest install clawdaddy
```

### Manual
```bash
curl -s https://clawdaddy.app/skill.md
```

## Features

- **Domain Availability** - Check if domains are available with pricing
- **Purchase with USDC** - x402 protocol for crypto payments on Base
- **Purchase with Card** - Stripe checkout for traditional payments
- **DNS Management** - Full CRUD for A, AAAA, CNAME, MX, TXT, NS, SRV records
- **Nameserver Config** - Point to Cloudflare, Vercel, Netlify, etc.
- **Domain Settings** - Transfer lock, auto-renew
- **Token Recovery** - Get back access via email or wallet

## Quick Start

```
# Check availability
GET https://clawdaddy.app/api/lookup/example.com

# Get purchase quote
GET https://clawdaddy.app/api/purchase/example.com/quote

# Buy with USDC (x402)
POST https://clawdaddy.app/api/purchase/example.com?method=x402

# Buy with card (Stripe)
POST https://clawdaddy.app/api/purchase/example.com?method=stripe
```

## Links

- Homepage: https://clawdaddy.app
- API Docs: https://clawdaddy.app/llms.txt
- Skill: https://clawdaddy.app/skill.md
