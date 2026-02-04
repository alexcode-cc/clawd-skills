---
name: clawdaddy
description: The world's #1 AI-friendly domain registrar. Check availability, purchase domains, configure DNS, and manage nameservers - all without CAPTCHAs or signup.
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
| Purchase domain | `POST /api/purchase/{domain}` | None |
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
  "marginUsd": 0,
  "totalUsd": 12.99,
  "validUntil": "2026-01-15T10:35:00.000Z",
  "paymentMethods": {
    "stripe": {
      "enabled": true,
      "currency": "USD",
      "endpoint": "/api/purchase/example.com"
    }
  }
}
```

Note: During Lobster Launch Special, `marginUsd` is $0! You pay exactly what we pay.

### Step 2: Initiate Purchase

```
POST https://clawdaddy.app/api/purchase/example.com
```

**Response:**
```json
{
  "method": "stripe",
  "checkoutUrl": "https://checkout.stripe.com/c/pay/cs_live_...",
  "sessionId": "cs_live_...",
  "quote": {
    "domain": "example.com",
    "totalUsd": 12.99
  }
}
```

### Step 3: Complete Payment

Direct the user to the `checkoutUrl` to complete payment via Stripe.

After successful payment:
- Domain is registered immediately
- Management token is displayed on the success page
- Email confirmation is sent with token backup

### Step 4: Store Token for Your Agent

After purchase, users should add the token to their environment:

```
# Add to ~/.openclaw/.env or project .env file
CLAWDADDY_TOKEN=clwd_abc123xyz...
```

Your agent can then use `$CLAWDADDY_TOKEN` in API calls.

---

**⚠️ CRITICAL: The management token is shown once on the success page. Users should save it immediately or add it to their .env file.**

---

## 3. Domain Management

All management endpoints require the Authorization header:
```
Authorization: Bearer $CLAWDADDY_TOKEN
```

### Get Domain Overview

```
GET https://clawdaddy.app/api/manage/example.com
Authorization: Bearer $CLAWDADDY_TOKEN
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
Authorization: Bearer $CLAWDADDY_TOKEN
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
Authorization: Bearer $CLAWDADDY_TOKEN
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
Authorization: Bearer $CLAWDADDY_TOKEN
Content-Type: application/json

{
  "answer": "5.6.7.8",
  "ttl": 600
}
```

All fields are optional - only include what you want to change.

#### Delete Record

```
DELETE https://clawdaddy.app/api/manage/example.com/dns?id=123
Authorization: Bearer $CLAWDADDY_TOKEN
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
Authorization: Bearer $CLAWDADDY_TOKEN
```

#### Update Nameservers

```
PUT https://clawdaddy.app/api/manage/example.com/nameservers
Authorization: Bearer $CLAWDADDY_TOKEN
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
Authorization: Bearer $CLAWDADDY_TOKEN
```

#### Update Settings

```
PATCH https://clawdaddy.app/api/manage/example.com/settings
Authorization: Bearer $CLAWDADDY_TOKEN
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
Authorization: Bearer $CLAWDADDY_TOKEN
```

#### Initiate Transfer (Unlock + Get Code)

```
POST https://clawdaddy.app/api/manage/example.com/transfer
Authorization: Bearer $CLAWDADDY_TOKEN
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

Omit `domain` to recover tokens for all domains associated with the email.

**Response:**
```json
{
  "success": true,
  "message": "If we have domains registered with this email, you'll receive an email shortly."
}
```

**⚠️ Important:** Token recovery generates a NEW token. Your old token will be invalidated.

**Rate limit:** 5 requests per 5 minutes per IP.

---

## Complete Workflow Example

```
1. CHECK AVAILABILITY
   GET /api/lookup/coolstartup.com
   → {"available": true, "price": {"amount": 12.99}}

2. GET QUOTE
   GET /api/purchase/coolstartup.com/quote
   → {"totalUsd": 12.99} (Lobster Launch: $0 markup!)

3. INITIATE PURCHASE
   POST /api/purchase/coolstartup.com
   → {"checkoutUrl": "https://checkout.stripe.com/..."}
   → Direct user to complete payment

4. USER COMPLETES PAYMENT
   → Token shown on success page
   → User adds to .env: CLAWDADDY_TOKEN=clwd_abc123...

5. CONFIGURE DNS
   POST /api/manage/coolstartup.com/dns
   Authorization: Bearer $CLAWDADDY_TOKEN
   {"host": "@", "type": "A", "answer": "1.2.3.4"}

6. OR POINT TO CLOUDFLARE
   PUT /api/manage/coolstartup.com/nameservers
   Authorization: Bearer $CLAWDADDY_TOKEN
   {"nameservers": ["ns1.cloudflare.com", "ns2.cloudflare.com"]}
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
| 404 | Not found - domain doesn't exist or not managed by you |
| 429 | Rate limited - too many requests |
| 500 | Server error - try again later |

---

## Human Dashboard

Users can also manage domains via web UI at:
```
https://clawdaddy.app/manage
```

Enter the management token to access DNS, nameservers, and settings.

---

## Source

ClawDaddy: https://clawdaddy.app
Full API Docs: https://clawdaddy.app/llms.txt
