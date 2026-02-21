---
name: m10-blockchain-agent
description: >-
  Ask natural language questions about Ethereum blockchain data. Covers
  historical on-chain activity (events, transactions, blocks, token transfers,
  NFTs), live chain state (balances, gas prices, transaction lookups), and
  smart contract bytecode analysis (function selectors, ABIs for unverified
  contracts). Powered by a multi-agent pipeline over 5.8B+ indexed records.
compatibility: Requires network access and an x402-compatible wallet on Base Mainnet
metadata:
  openclaw:
    requires:
      env:
        - X402_WALLET_PRIVATE_KEY
      bins:
        - node
    primaryEnv: X402_WALLET_PRIVATE_KEY
    homepage: https://onesource.io
    install:
      - kind: node
        package: "@x402/fetch"
      - kind: node
        package: "@x402/evm"
      - kind: node
        package: viem
---

# M10 Blockchain Agent

Ask a question in plain English. Get a structured analysis backed by live
blockchain data — no query language, no SDKs, no index knowledge required.

|              |                                           |
| ------------ | ----------------------------------------- |
| **Base URL** | `https://agent.onesource.io`              |
| **Auth**     | x402 (pay-per-request, no API keys)       |
| **Price**    | $0.04 USDC per query                      |
| **Payment**  | On-chain USDC on Base mainnet via x402    |
| **Networks** | Ethereum mainnet · Sepolia · Avalanche    |

---

## Setup & Payment

### How x402 Payment Works

Every request to this skill costs **$0.04 USDC** paid on-chain via the
[x402 protocol](https://github.com/coinbase/x402). No API keys or accounts
are needed — payment is cryptographic and per-request.

1. Your agent sends a `POST` to `https://agent.onesource.io/`
2. The gateway returns **HTTP 402** with payment instructions in the `payment-required` header
3. The x402 client library automatically signs a USDC Permit2 authorization with your wallet
4. The signed payment is sent in the `payment-signature` header on a retry
5. The gateway verifies the payment, proxies the request, and settles on-chain
6. Your agent receives the response

The x402 client libraries handle steps 2–4 transparently.

### Required Environment Variable

| Variable | Description |
| --- | --- |
| `X402_WALLET_PRIVATE_KEY` | Private key (hex, `0x`-prefixed) for a Base mainnet wallet holding USDC. Used to sign x402 payment authorizations. **Never hardcode this — always use an env var.** |

### Wallet Prerequisites

Your wallet (the address derived from `X402_WALLET_PRIVATE_KEY`) must have:

1. **USDC on Base mainnet** — at least a few dollars to cover queries at $0.01 each
2. **A one-time ERC-20 approval** of USDC to the Permit2 contract:
   `0x000000000022D473030F116dDEE9F6B43aC78BA3`
3. **A small amount of ETH on Base** — for the initial approval transaction gas

### Install Dependencies

```sh
npm install @x402/fetch @x402/evm viem
```

### Example: Making a Paid Request

```js
import { wrapFetchWithPayment, x402Client } from "@x402/fetch";
import { registerExactEvmScheme } from "@x402/evm/exact/client";
import { privateKeyToAccount } from "viem/accounts";

// Load wallet from environment — never hardcode private keys
const account = privateKeyToAccount(process.env.X402_WALLET_PRIVATE_KEY);
const client = new x402Client();
registerExactEvmScheme(client, { signer: account });

const fetchWithPayment = wrapFetchWithPayment(fetch, client);

const res = await fetchWithPayment("https://agent.onesource.io/", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    query: "What is the ETH balance of vitalik.eth?"
  }),
});

const data = await res.json();
console.log(data.summary);
console.log(data.response);
```

---

## Privacy & Data Handling

- **Queries are sent to `https://agent.onesource.io`** — an external service
  operated by [OneSource](https://onesource.io). Your natural-language query
  text and any addresses you include are transmitted.
- **`query_traces`** in the response contains an audit trail of internal data
  lookups. This may echo parts of your query. Omit it from user-facing output
  if not needed.
- **No data is stored** beyond what is needed to process the request. Payments
  are settled on-chain and are publicly visible as standard USDC transfers.

---

## Capabilities

### Indexed Historical Data
5.8 billion+ records across Ethereum mainnet, Sepolia testnet, and Avalanche C-Chain.

**Events & Activity**
- "How many Transfer events happened in the last 24 hours?"
- "What events did 0xdead... emit this week?"
- "Top 10 contracts by event count over the last 30 days"
- "Show me all Approval events for USDC in the last hour"

**Transactions**
- "What's the average gas used per transaction on mainnet today?"
- "How many transactions did 0xabc... send in the last 30 days?"
- "Show the 5 highest-value transactions in block range 21000000–21001000"
- "What's the transaction volume trend week over week for the last month?"

**Blocks**
- "What was the average block time last week?"
- "Which blocks had the highest gas utilization in the past 24 hours?"
- "How many blocks were produced per hour yesterday?"

**Token Transfers (ERC-20 / ERC-721 / ERC-1155)**
- "What ERC-20 tokens did 0xabc... receive in the last month?"
- "Top 5 ERC-20 tokens by transfer volume this week"
- "Show all mint events for USDC in the last 7 days"
- "How many unique wallets received WETH in the last 24 hours?"

**NFTs**
- "Show me BAYC token #4321 — name, image, and attributes"
- "What were the last 5 CryptoPunks sales and their prices?"
- "How many NFTs did 0xabc... receive this month?"
- "Top 10 NFT collections by transfer count today"

**Contracts**
- "When was Uniswap V3 deployed and who deployed it?"
- "How many contracts were deployed on mainnet in the last 7 days?"
- "Is 0xabc... a contract or an EOA?"

---

### Live Chain State
Real-time lookups directly from Ethereum archive nodes — no indexing lag.

- "What's the current ETH balance of 0xabc...?"
- "What's the current gas price on mainnet?"
- "Did transaction 0x123... succeed or revert?"
- "What's the latest block number right now?"
- "What's the USDC balance of 0xabc... at the current block?"
- "How much ETH does Vitalik's address hold?"
- "What's the current EIP-1559 base fee and priority fee?"

---

### Smart Contract Analysis
Analyze any deployed contract's bytecode — including unverified contracts —
to extract its interface without needing source code.

- "What functions does 0xabc... expose?"
- "Decompile 0xabc... and show me the function selectors"
- "Compare the public functions of these two contracts: 0xabc... and 0xdef..."
- "Does 0xabc... implement ERC-721?"

---

## Pricing

Requests are priced per-query at **$0.04 USDC** via the x402 payment protocol
(see [Setup & Payment](#setup--payment) above for wallet configuration).

| Network | Asset | Scheme  | Endpoint |
| ------- | ----- | ------- | -------- |
| Base    | USDC  | `exact` | `https://agent.onesource.io` |

The `usage.estimated_cost_usd` field in every response shows exactly what
each query cost.

---

## Request

```
POST /
Content-Type: application/json

{
  "query":      "string — required. Your natural language question.",
  "session_id": "string — optional. Custom ULID. Auto-generated if omitted."
}
```

## Response

```json
{
  "session_id": "01JMQX7K3N...",
  "status":     "completed | error | processing",
  "summary":    "Plain text summary, 1–3 sentences. Present on success.",
  "response":   "Full Markdown analysis with tables, headers, code blocks.",
  "steps": [
    {
      "agent":       "router | opensearch | rpc | evmole",
      "action":      "Description of what was queried",
      "status":      "completed | failed"
    }
  ],
  "usage": {
    "total_tokens":       5820,
    "estimated_cost_usd": 0.0018
  },
  "query_traces": [...],
  "error": "string | null"
}
```

**`summary`** — plain text, 1–3 sentences. Display this prominently.
**`response`** — full Markdown. Render it, don't parse it as structured data.
**`query_traces`** — raw audit trail of every data query made internally.

---

## Error Codes

| Code | Meaning                | Fix                                   |
| ---- | ---------------------- | ------------------------------------- |
| 402  | Payment required       | Send x402 payment (auto with SDK)     |
| 409  | Session already exists | Omit `session_id` or use a new one    |
| 422  | Malformed request      | Check `query` field is present        |
| 500  | Pipeline error         | Try rephrasing the query              |

---

## What M10 Won't Answer

The agent rejects queries requiring unbounded full-index scans with no filter:

- "List every transaction ever"
- "Give me all NFTs"
- "Show everything in the last year"

Add a filter (address, time range, event type, contract) and it works:

- "List the last 10 transactions from 0xabc..."
- "Top 10 NFT collections by mint count in the last 24 hours"
- "How many transactions happened last year?" (aggregation — fine)
