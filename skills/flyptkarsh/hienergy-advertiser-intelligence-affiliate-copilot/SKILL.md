---
name: hienergy-advertiser-intelligence-affiliate-copilot
description: >-
  Official HiEnergy Agency skill for Hi Energy (HiEnergy) advertiser intelligence and affiliate copilot workflows in OpenClaw. Query HiEnergy API v1 for advertisers, affiliate programs, deals, transactions, and contacts. Optimized for affiliate marketing, partner marketing, advertiser lookup, brand intelligence, publisher contacts, deal research, transaction analytics, commission analysis, and domain-to-advertiser search across networks like Impact, Rakuten, and CJ. Includes deep advertiser profile (show endpoint) responses with links such as https://app.hienergy.ai/a/<advertiser_id>. Learn more: https://hienergy.ai and https://app.hienergy.ai/api_documentation.
---

# Hi Energy Advertiser Intelligence / Affiliate Copilot

Use this skill when a user needs affiliate intelligence from HiEnergy data.

## Setup

1. Set API key in environment:

```bash
export HIENERGY_API_KEY="<your_api_key>"
# also supported:
export HI_ENERGY_API_KEY="<your_api_key>"
```

2. Install Python dependency (if missing):

```bash
pip install -r requirements.txt
```

## Quick usage

### Python

```python
from scripts.hienergy_skill import HiEnergySkill

skill = HiEnergySkill()
advertisers = skill.get_advertisers(search="fitness", limit=10)
programs = skill.get_affiliate_programs(search="supplements", limit=10)
research = skill.research_affiliate_programs(search="supplements", min_commission=10, top_n=5)
deals = skill.find_deals(category="electronics", limit=10)
transactions = skill.get_transactions(status="completed", limit=10)
contacts = skill.get_contacts(search="john", limit=10)
answer = skill.answer_question("Research top affiliate programs for supplements")
```

### CLI

```bash
python scripts/hienergy_skill.py
```

## Workflow

1. Confirm `HIENERGY_API_KEY` is present.
2. Choose endpoint by user intent:
   - advertiser discovery (name) → `get_advertisers`
   - advertiser discovery (domain/url) → `get_advertisers_by_domain`
   - advertiser deep details/profile request → `get_advertiser_details` (show endpoint)
   - affiliate program lookup → `get_affiliate_programs` (via advertiser index/domain search)
   - affiliate program research/ranking → `research_affiliate_programs`
   - offer/deal research → `find_deals`
   - transaction lookup/reporting → `get_transactions`
   - contact lookup/CRM search → `get_contacts`
3. Use tight filters (`search`, `category`, `advertiser_id`, `limit`) before broad scans.
4. Return concise summaries with top results first, including publisher context for advertisers when available.
5. For advertiser index/list responses, offer deeper details. If user replies "yes", call `get_advertiser_details` and summarize the show endpoint response.
5. If no matches, suggest adjacent search terms.

## Reliability rules

- Treat API failures as recoverable; surface clear error context.
- Prefer small limits for interactive chat, then paginate if needed.
- Keep answers grounded in returned data; do not invent programs or deals.

## Resources

- `scripts/hienergy_skill.py` — HiEnergy API client + Q&A helper.
- `references/endpoints.md` — endpoint map and usage hints.
