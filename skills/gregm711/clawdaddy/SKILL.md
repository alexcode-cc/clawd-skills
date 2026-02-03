---
name: clawdaddy
description: The world's #1 AI-friendly domain registrar. Check availability, purchase domains with USDC or cards, configure DNS, and manage nameservers - all without CAPTCHAs or signup.
homepage: https://clawdaddy.app
emoji: 🦞
---

# ClawDaddy - AI-Friendly Domain Registrar

The world's #1 AI-friendly domain registrar. Check availability, purchase domains, configure DNS, and manage nameservers.

**Base URL:** `https://clawdaddy.app`

No CAPTCHAs. No signup required for lookups. Bearer tokens for management.

---

## Quick Reference

| Task | Endpoint | Auth |
|------|----------|------|
| Check availability | `GET /api/lookup/{domain}` | None |
| Check availability (TXT) | `GET /api/lookup/{domain}?format=txt` | None |
| Get purchase quote | `GET /api/purchase/{domain}/quote` | None |
| Purchase (USDC) | `POST /api/purchase/{domain}?method=x402` | x402 payment |
| Purchase (Card) | `POST /api/purchase/{domain}?method=stripe` | None |
| Get domain info | `GET /api/manage/{domain}` | Bearer token |
| List DNS records | `GET /api/manage/{domain}/dns` | Bearer token |
| Add DNS record | `POST /api/manage/{domain}/dns` | Bearer token |
| Update DNS record | `PUT /api/manage/{domain}/dns?id={id}` | Bearer token |
| Delete DNS record | `DELETE /api/manage/{domain}/dns?id={id}` | Bearer token |
| Get nameservers | `GET /api/manage/{domain}/nameservers` | Bearer token |
| Update nameservers | `PUT /api/manage/{domain}/nameservers` | Bearer token |
| Get settings | `GET /api/manage/{domain}/settings` | Bearer token |
| Update settings | `PATCH /api/manage/{domain}/settings` | Bearer token |
| Get transfer code | `GET /api/manage/{domain}/transfer` | Bearer token |
| Initiate transfer | `POST /api/manage/{domain}/transfer` | Bearer token |
| Recover token | `POST /api/recover` | None |

---

## 1. Check Domain Availability

```
GET https://clawdaddy.app/api/lookup/example.com
```

**Response:**
```json
{
  "fqdn": "example.com",
  "available": true,
  "status": "available",
  "premium": false,
  "price": {
    "amount": 12.99,
    "currency": "USD",
    "period": "year"
  },
  "renewal": {
    "amount": 19.99,
    "currency": "USD",
    "period": "year"
  },
  "checked_at": "2026-01-15T10:30:00.000Z",
  "source": "namecom",
  "cache": {
    "hit": false,
    "ttl_seconds": 120,
    "stale": false
  }
}
```

**TXT format (easier to parse):**
```
GET https://clawdaddy.app/api/lookup/example.com?format=txt
```

```
fqdn=example.com
available=true
status=available
premium=false
price_amount=12.99
price_currency=USD
price_period=year
renewal_amount=19.99
checked_at=2026-01-15T10:30:00Z
source=namecom
cache_hit=false
ttl_seconds=120
```

**Status values:**
| Status | available | Meaning |
|--------|-----------|---------|
| `available` | `true` | Can be registered |
| `registered` | `false` | Already taken |
| `unknown` | `false` | Error or timeout |

---

## 2. Purchase a Domain

### Step 1: Get Quote

```
GET https://clawdaddy.app/api/purchase/example.com/quote
```

```json
{
  "domain": "example.com",
  "available": true,
  "priceUsd": 12.99,
  "marginUsd": 2.00,
  "totalUsd": 14.99,
  "validUntil": "2026-01-15T10:35:00.000Z",
  "paymentMethods": {
    "x402": {
      "enabled": true,
      "currency": "USDC",
      "network": "base",
      "endpoint": "/api/purchase/example.com?method=x402"
    },
    "stripe": {
      "enabled": true,
      "currency": "USD",
      "endpoint": "/api/purchase/example.com?method=stripe"
    }
  }
}
```

---

### Option A: Purchase with USDC (x402 Protocol)

**Best for:** AI agents with crypto wallets

#### Step 2a: Initiate Purchase

```
POST https://clawdaddy.app/api/purchase/example.com?method=x402
```

**Response: HTTP 402 Payment Required**
```json
{
  "error": "Payment Required",
  "domain": "example.com",
  "price": "$14.99 USDC",
  "x402": {
    "version": "2.0",
    "accepts": [{
      "scheme": "exact",
      "network": "eip155:8453",
      "maxAmountRequired": "14990000",
      "resource": "https://clawdaddy.app/api/purchase/example.com?method=x402",
      "description": "Register domain: example.com",
      "payTo": "0xc8381BA1987844D5DD973a90A02a0C87FDf5C0D2",
      "asset": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"
    }]
  }
}
```

**Understanding the 402 response:**
- `network`: `eip155:8453` = Base mainnet
- `maxAmountRequired`: USDC amount with 6 decimals (`14990000` = $14.99)
- `payTo`: Wallet address to send USDC to
- `asset`: USDC contract address on Base

#### Step 3a: Pay USDC on Base

Send the exact USDC amount to the `payTo` address on Base network.

#### Step 4a: Complete Purchase with Payment Proof

```
POST https://clawdaddy.app/api/purchase/example.com?method=x402
x-payment: <payment_proof_or_transaction_hash>
```

**Success Response:**
```json
{
  "success": true,
  "method": "x402",
  "domain": "example.com",
  "registrationId": "12345",
  "expiresAt": "2027-01-15T10:30:00.000Z",
  "nameservers": ["ns1.name.com", "ns2.name.com"],
  "transactionHash": "0x...",
  "managementToken": "clwd_abc123xyz789...",
  "manageUrl": "https://clawdaddy.app/api/manage/example.com",
  "message": "Successfully registered example.com!"
}
```

---

### Option B: Purchase with Card (Stripe)

**Best for:** Humans or agents without crypto

#### Step 2b: Get Checkout URL

```
POST https://clawdaddy.app/api/purchase/example.com?method=stripe
Content-Type: application/json

{
  "email": "user@example.com"
}
```

**Response:**
```json
{
  "method": "stripe",
  "checkoutUrl": "https://checkout.stripe.com/c/pay/cs_live_...",
  "sessionId": "cs_live_...",
  "quote": {
    "domain": "example.com",
    "totalUsd": 14.99
  }
}
```

#### Step 3b: Complete Payment

Redirect user to `checkoutUrl` or open it in a browser. After successful payment, user is redirected to success page with their management token.

---

**CRITICAL: Save the `managementToken` immediately after purchase! You need it to manage DNS, nameservers, and settings. It cannot be retrieved without going through token recovery.**

---

## 3. Domain Management

All management endpoints require the Authorization header:
```
Authorization: Bearer clwd_your_management_token
```

### Get Domain Overview

```
GET https://clawdaddy.app/api/manage/example.com
Authorization: Bearer clwd_abc123...
```

```json
{
  "domain": "example.com",
  "purchasedAt": "2026-01-15T10:30:00.000Z",
  "expiresAt": "2027-01-15T10:30:00.000Z",
  "nameservers": ["ns1.name.com", "ns2.name.com"],
  "settings": {
    "locked": true,
    "autorenewEnabled": false,
    "privacyEnabled": true
  }
}
```

---

### DNS Records

#### List All Records

```
GET https://clawdaddy.app/api/manage/example.com/dns
Authorization: Bearer clwd_abc123...
```

```json
{
  "records": [
    {"id": 1, "host": "@", "type": "A", "answer": "1.2.3.4", "ttl": 300},
    {"id": 2, "host": "www", "type": "CNAME", "answer": "example.com", "ttl": 300}
  ]
}
```

#### Add Record

```
POST https://clawdaddy.app/api/manage/example.com/dns
Authorization: Bearer clwd_abc123...
Content-Type: application/json

{
  "host": "@",
  "type": "A",
  "answer": "1.2.3.4",
  "ttl": 300
}
```

#### Update Record

```
PUT https://clawdaddy.app/api/manage/example.com/dns?id=123
Authorization: Bearer clwd_abc123...
Content-Type: application/json

{
  "answer": "5.6.7.8",
  "ttl": 600
}
```

#### Delete Record

```
DELETE https://clawdaddy.app/api/manage/example.com/dns?id=123
Authorization: Bearer clwd_abc123...
```

**Supported record types:** `A`, `AAAA`, `CNAME`, `MX`, `TXT`, `NS`, `SRV`

**Common DNS configurations:**

| Purpose | Record |
|---------|--------|
| Point to server | `{"host": "@", "type": "A", "answer": "1.2.3.4"}` |
| IPv6 | `{"host": "@", "type": "AAAA", "answer": "2001:db8::1"}` |
| www subdomain | `{"host": "www", "type": "CNAME", "answer": "example.com"}` |
| Email (Google) | `{"host": "@", "type": "MX", "answer": "aspmx.l.google.com", "priority": 1}` |
| SPF record | `{"host": "@", "type": "TXT", "answer": "v=spf1 include:_spf.google.com ~all"}` |
| Domain verification | `{"host": "@", "type": "TXT", "answer": "google-site-verification=abc123"}` |

---

### Nameservers

#### Get Current Nameservers

```
GET https://clawdaddy.app/api/manage/example.com/nameservers
Authorization: Bearer clwd_abc123...
```

#### Update Nameservers

```
PUT https://clawdaddy.app/api/manage/example.com/nameservers
Authorization: Bearer clwd_abc123...
Content-Type: application/json

{
  "nameservers": [
    "ns1.cloudflare.com",
    "ns2.cloudflare.com"
  ]
}
```

**Common nameserver configurations:**

| Provider | Nameservers |
|----------|-------------|
| Cloudflare | `ns1.cloudflare.com`, `ns2.cloudflare.com` |
| Vercel | `ns1.vercel-dns.com`, `ns2.vercel-dns.com` |
| Netlify | `dns1.p01.nsone.net`, `dns2.p01.nsone.net` |
| AWS Route53 | Check your hosted zone for specific NS records |
| Google Cloud | `ns-cloud-X.googledomains.com` (X = a1-e4) |

---

### Domain Settings

#### Get Settings

```
GET https://clawdaddy.app/api/manage/example.com/settings
Authorization: Bearer clwd_abc123...
```

#### Update Settings

```
PATCH https://clawdaddy.app/api/manage/example.com/settings
Authorization: Bearer clwd_abc123...
Content-Type: application/json

{
  "locked": false,
  "autorenewEnabled": true
}
```

**Settings:**
- `locked`: Domain transfer lock (recommended: true)
- `autorenewEnabled`: Auto-renew before expiration

---

### Transfer Domain Out

#### Get Auth Code

```
GET https://clawdaddy.app/api/manage/example.com/transfer
Authorization: Bearer clwd_abc123...
```

#### Initiate Transfer (Unlock + Get Code)

```
POST https://clawdaddy.app/api/manage/example.com/transfer
Authorization: Bearer clwd_abc123...
```

**Note:** Domains cannot be transferred within 60 days of registration (ICANN policy).

---

## 4. Token Recovery

Lost your management token? Request a new one:

```
POST https://clawdaddy.app/api/recover
Content-Type: application/json

{
  "email": "you@example.com",
  "domain": "example.com"
}
```

For x402 purchases (wallet-based):
```json
{
  "wallet": "0x123...",
  "domain": "example.com"
}
```

Omit `domain` to recover tokens for all domains associated with the email/wallet.

**Response:**
```json
{
  "success": true,
  "message": "If we have domains registered with this email/wallet, you'll receive an email shortly."
}
```

**Important:** Token recovery generates a NEW token. Your old token will be invalidated.

**Rate limit:** 5 requests per 5 minutes per IP.

---

## Complete Workflow Examples

### Example 1: Check and Buy with USDC

```
1. CHECK AVAILABILITY
   GET /api/lookup/coolstartup.com
   → {"available": true, "price": {"amount": 12.99}}

2. GET QUOTE
   GET /api/purchase/coolstartup.com/quote
   → {"totalUsd": 14.99, "paymentMethods": {"x402": {"enabled": true}}}

3. INITIATE PURCHASE
   POST /api/purchase/coolstartup.com?method=x402
   → HTTP 402: {
       "x402": {
         "accepts": [{
           "maxAmountRequired": "14990000",
           "payTo": "0xc8381BA1987844D5DD973a90A02a0C87FDf5C0D2",
           "asset": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
           "network": "eip155:8453"
         }]
       }
     }

4. PAY USDC ON BASE
   Send 14.99 USDC to 0xc8381BA1987844D5DD973a90A02a0C87FDf5C0D2

5. COMPLETE PURCHASE
   POST /api/purchase/coolstartup.com?method=x402
   x-payment: 0xtransactionhash...
   → {"success": true, "managementToken": "clwd_abc123..."}

6. SAVE THE TOKEN!
   Store "clwd_abc123..." securely - you need it for all management
```

### Example 2: Configure DNS for a Web Server

```
1. ADD A RECORD (root domain)
   POST /api/manage/coolstartup.com/dns
   Authorization: Bearer clwd_abc123...
   {"host": "@", "type": "A", "answer": "123.45.67.89", "ttl": 300}

2. ADD CNAME (www subdomain)
   POST /api/manage/coolstartup.com/dns
   Authorization: Bearer clwd_abc123...
   {"host": "www", "type": "CNAME", "answer": "coolstartup.com", "ttl": 300}

3. VERIFY
   GET /api/manage/coolstartup.com/dns
   → {"records": [{"host": "@", "type": "A", ...}, {"host": "www", "type": "CNAME", ...}]}
```

### Example 3: Point Domain to Cloudflare

```
PUT /api/manage/coolstartup.com/nameservers
Authorization: Bearer clwd_abc123...
{"nameservers": ["ns1.cloudflare.com", "ns2.cloudflare.com"]}
→ {"success": true}
```

### Example 4: Set Up Email with Google Workspace

```
1. ADD MX RECORDS
   POST /api/manage/example.com/dns
   {"host": "@", "type": "MX", "answer": "aspmx.l.google.com", "priority": 1}

   POST /api/manage/example.com/dns
   {"host": "@", "type": "MX", "answer": "alt1.aspmx.l.google.com", "priority": 5}

2. ADD SPF RECORD
   POST /api/manage/example.com/dns
   {"host": "@", "type": "TXT", "answer": "v=spf1 include:_spf.google.com ~all"}

3. ADD DKIM (get value from Google Admin)
   POST /api/manage/example.com/dns
   {"host": "google._domainkey", "type": "TXT", "answer": "v=DKIM1; k=rsa; p=..."}
```

---

## Error Handling

All errors return JSON:
```json
{
  "error": "Description of what went wrong",
  "details": "Additional context if available"
}
```

| Status | Meaning |
|--------|---------|
| 400 | Bad request - invalid input or domain format |
| 401 | Unauthorized - missing or invalid management token |
| 402 | Payment required - x402 payment flow (not an error) |
| 404 | Not found - domain doesn't exist or not managed by you |
| 429 | Rate limited - too many requests |
| 500 | Server error - try again later |

---

## Source

ClawDaddy: https://clawdaddy.app
Full API Docs: https://clawdaddy.app/llms.txt
