"""
HiEnergy API Skill - Open Claw Skill for querying advertisers, affiliate programs, and deals.
"""

import os
import json
from typing import Dict, List, Optional, Any
import requests


class HiEnergySkill:
    """
    A skill for interacting with the HiEnergy API to answer questions about
    advertisers, affiliate programs, deals, transactions, and contacts.
    """
    
    BASE_URL = "https://app.hienergy.ai"
    MAX_SEARCH_TERMS = 3  # Maximum number of keywords to extract from questions
    MAX_DISPLAY_ITEMS = 5  # Maximum number of items to display in formatted answers
    MAX_PAGE_SIZE = 500  # API-documented max
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the HiEnergy API skill.
        
        Args:
            api_key: The API key for HiEnergy API. If not provided, will try to read
                    from HIENERGY_API_KEY environment variable.
        """
        self.api_key = (
            api_key
            or os.environ.get('HIENERGY_API_KEY')
            or os.environ.get('HI_ENERGY_API_KEY')
        )
        if not self.api_key:
            raise ValueError(
                "API key is required. Provide it as a parameter or set HIENERGY_API_KEY "
                "(or HI_ENERGY_API_KEY) environment variable. "
                "Get your key at https://app.hienergy.ai/api_documentation/api_key "
                "(login: https://app.hienergy.ai/sign_in)."
            )
        
        self.headers = {
            'X-Api-Key': self.api_key,
            'Content-Type': 'application/json',
            'User-Agent': 'openclaw-hi-energy-affiliate-copilot/1.0'
        }
    
    def _clamp_page_size(self, value: int) -> int:
        """Clamp page size to API-safe bounds."""
        if value is None:
            return 20
        return max(1, min(int(value), self.MAX_PAGE_SIZE))

    def _make_request(self, endpoint: str, method: str = 'GET',
                      params: Optional[Dict] = None, data: Optional[Dict] = None) -> Dict:
        """
        Make a request to the HiEnergy API.
        
        Args:
            endpoint: The API endpoint to call
            method: HTTP method (GET, POST, etc.)
            params: Query parameters
            data: Request body data
            
        Returns:
            Response data as dictionary
            
        Raises:
            requests.exceptions.RequestException: If the request fails
        """
        url = f"{self.BASE_URL}/api/v1/{endpoint.lstrip('/')}"
        
        try:
            response = requests.request(
                method=method,
                url=url,
                headers=self.headers,
                params=params,
                json=data,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            status = e.response.status_code if e.response is not None else 'unknown'
            body_preview = ''
            if e.response is not None:
                body_preview = (e.response.text or '')[:300]
            raise Exception(f"API request failed (HTTP {status}): {body_preview}")
        except requests.exceptions.RequestException as e:
            raise Exception(f"API request failed: {str(e)}")
    
    def _normalize_item(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """Flatten JSON:API-style objects while preserving top-level keys."""
        if not isinstance(item, dict):
            return {}

        attrs = item.get('attributes')
        if isinstance(attrs, dict):
            merged = dict(attrs)
            if 'id' not in merged and item.get('id') is not None:
                merged['id'] = item.get('id')
            if item.get('type') is not None:
                merged['type'] = item.get('type')
            return merged

        return item

    def _extract_list_data(self, response: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract list payloads across flat and JSON:API response formats."""
        data = response.get('data', []) if isinstance(response, dict) else []
        if isinstance(data, list):
            return [self._normalize_item(item) for item in data]
        if isinstance(data, dict):
            return [self._normalize_item(data)]
        return []

    def _extract_single_data(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """Extract single payloads across flat and JSON:API response formats."""
        items = self._extract_list_data(response)
        return items[0] if items else {}

    def get_advertisers_by_domain(self, domain_or_url: str, limit: int = 200) -> List[Dict]:
        """
        Search advertisers by domain or URL.

        Args:
            domain_or_url: Domain or URL (e.g., amazon.com or https://amazon.com)
            limit: Maximum number of results to return

        Returns:
            List of advertiser dictionaries
        """
        params: Dict[str, Any] = {
            'domain': domain_or_url,
            'limit': self._clamp_page_size(limit)
        }

        results: List[Dict[str, Any]] = []

        # Primary endpoint from docs.
        try:
            response = self._make_request('advertisers/search_by_domain', params=params)
            results = self._extract_list_data(response)
        except Exception:
            results = []

        # Some backends accept `url` instead of `domain`.
        if not results:
            try:
                url_params: Dict[str, Any] = {
                    'url': domain_or_url,
                    'limit': self._clamp_page_size(limit)
                }
                url_response = self._make_request('advertisers/search_by_domain', params=url_params)
                results = self._extract_list_data(url_response)
            except Exception:
                results = []

        # Fallback: use advertisers index filters when domain endpoint is unstable.
        if not results:
            try:
                idx_response = self._make_request('advertisers', params={
                    'domain': domain_or_url,
                    'limit': self._clamp_page_size(limit)
                })
                results = self._extract_list_data(idx_response)
            except Exception:
                results = []

        if not results:
            try:
                idx_response = self._make_request('advertisers', params={
                    'name': domain_or_url,
                    'limit': self._clamp_page_size(limit)
                })
                results = self._extract_list_data(idx_response)
            except Exception:
                results = []

        return results

    def get_advertisers(self, search: Optional[str] = None,
                       limit: int = 200, offset: int = 0) -> List[Dict]:
        """
        Get advertisers from the HiEnergy API.

        Args:
            search: Optional name/search term to filter advertisers
            limit: Maximum number of results to return
            offset: Offset for pagination

        Returns:
            List of advertiser dictionaries
        """
        params = {
            'limit': self._clamp_page_size(limit),
            'offset': offset
        }

        # Prefer domain endpoint for domain/URL-like queries.
        if search and ('.' in search or search.startswith('http://') or search.startswith('https://')):
            domain_results = self.get_advertisers_by_domain(search, limit=limit)
            if domain_results:
                return domain_results

        if search:
            params['name'] = search

        response = self._make_request('advertisers', params=params)
        results = self._extract_list_data(response)

        # Smart fallback: if a multi-word query returns no rows, retry by tokens and merge.
        if search and not results and ' ' in search.strip():
            merged: List[Dict[str, Any]] = []
            seen_ids = set()
            for token in [t.strip() for t in search.split() if t.strip()]:
                token_params = {
                    'limit': self._clamp_page_size(limit),
                    'offset': offset,
                    'name': token
                }
                token_response = self._make_request('advertisers', params=token_params)
                for item in self._extract_list_data(token_response):
                    item_id = str(item.get('id'))
                    if item_id not in seen_ids:
                        seen_ids.add(item_id)
                        merged.append(item)
            results = merged

        return results
    
    def get_affiliate_programs(self, advertiser_id: Optional[str] = None,
                              search: Optional[str] = None,
                              limit: int = 200, offset: int = 0) -> List[Dict]:
        """
        Get affiliate program matches via advertiser endpoints.

        Note: HiEnergy does not expose a dedicated /affiliate_programs endpoint.
        Program discovery is performed via:
        - /advertisers/search_by_domain (for domain/url-like queries)
        - /advertisers index search (for name/text queries)

        Args:
            advertiser_id: Optional advertiser ID to filter results
            search: Optional search term or domain/url
            limit: Maximum number of results to return
            offset: Offset for pagination

        Returns:
            List of advertiser/program dictionaries
        """
        try:
            programs = self.get_advertisers(search=search, limit=limit, offset=offset)
        except Exception:
            programs = []

        # Improve matching for spaced brand names (e.g., "all birds" -> "allbirds").
        if search and ' ' in search.strip():
            merged = {str(p.get('id')): p for p in programs if p.get('id') is not None}
            compact_variants = [
                ''.join(search.split()),
                '-'.join(search.split()),
            ]
            for variant in compact_variants:
                if not variant:
                    continue
                try:
                    extra = self.get_advertisers(search=variant, limit=limit, offset=offset)
                    for p in extra:
                        pid = str(p.get('id'))
                        if pid and pid not in merged:
                            merged[pid] = p
                except Exception:
                    continue
            programs = list(merged.values())

        # Re-rank by closeness to query string to surface strongest brand match first.
        if search:
            q = search.lower().strip()
            q_compact = ''.join(q.split())

            def score(item: Dict[str, Any]) -> int:
                name = str(item.get('name', '')).lower()
                name_compact = ''.join(name.split())
                s = 0
                if q == name:
                    s += 100
                if q in name:
                    s += 50
                if q_compact and q_compact == name_compact:
                    s += 80
                if q_compact and q_compact in name_compact:
                    s += 40
                return s

            programs = sorted(programs, key=score, reverse=True)

        if advertiser_id:
            advertiser_id_str = str(advertiser_id)
            programs = [
                p for p in programs
                if str(p.get('id')) == advertiser_id_str or str(p.get('advertiser_id')) == advertiser_id_str
            ]

        return programs
    
    def _parse_commission_value(self, program: Dict[str, Any]) -> float:
        """Best-effort numeric commission extraction for ranking/filtering."""
        candidates = [
            program.get('commission_rate'),
            program.get('avg_commission_rate'),
            program.get('commission_amount'),
        ]
        for value in candidates:
            if value is None:
                continue
            if isinstance(value, (int, float)):
                return float(value)
            if isinstance(value, str):
                cleaned = value.strip().replace('%', '').replace('$', '').replace(',', '')
                try:
                    return float(cleaned)
                except ValueError:
                    continue
        return 0.0

    def research_affiliate_programs(self,
                                    search: Optional[str] = None,
                                    advertiser_id: Optional[str] = None,
                                    min_commission: Optional[float] = None,
                                    network_slug: Optional[str] = None,
                                    status: Optional[str] = None,
                                    country: Optional[str] = None,
                                    limit: int = 200,
                                    top_n: int = 10) -> Dict[str, Any]:
        """
        Research affiliate programs with ranking and summary stats.

        Returns a dict with:
        - summary: aggregate counts + average commission
        - programs: filtered + ranked program list
        """
        programs = self.get_affiliate_programs(
            advertiser_id=advertiser_id,
            search=search,
            limit=limit,
        )

        filtered: List[Dict[str, Any]] = []
        for program in programs:
            commission_value = self._parse_commission_value(program)

            if min_commission is not None and commission_value < float(min_commission):
                continue

            if network_slug:
                network_value = str(
                    program.get('network_slug')
                    or (program.get('network') or {}).get('slug')
                    or ''
                ).lower()
                if network_slug.lower() not in network_value:
                    continue

            if status:
                status_value = str(program.get('status') or program.get('program_status') or '').lower()
                if status.lower() != status_value:
                    continue

            if country:
                country_value = ' '.join([
                    str(program.get('country', '')),
                    str(program.get('country_code', '')),
                    ' '.join(program.get('countries', []) if isinstance(program.get('countries'), list) else []),
                ]).lower()
                if country.lower() not in country_value:
                    continue

            enriched = dict(program)
            enriched['_commission_value'] = commission_value
            filtered.append(enriched)

        ranked = sorted(
            filtered,
            key=lambda p: (p.get('_commission_value', 0.0), p.get('transactions_count', 0) or 0),
            reverse=True,
        )

        top_programs = ranked[:max(1, int(top_n))]
        avg_commission = (
            sum([p.get('_commission_value', 0.0) for p in ranked]) / len(ranked)
            if ranked else 0.0
        )

        return {
            'summary': {
                'query': search,
                'total_programs_scanned': len(programs),
                'total_programs_matched': len(ranked),
                'average_commission': round(avg_commission, 2),
                'filters': {
                    'advertiser_id': advertiser_id,
                    'min_commission': min_commission,
                    'network_slug': network_slug,
                    'status': status,
                    'country': country,
                },
            },
            'programs': top_programs,
        }

    def find_deals(self, search: Optional[str] = None,
                   category: Optional[str] = None,
                   advertiser_id: Optional[str] = None,
                   min_commission: Optional[float] = None,
                   limit: int = 200, offset: int = 0,
                   cursor: Optional[str] = None,
                   page: Optional[int] = None,
                   per_page: Optional[int] = None,
                   network_slug: Optional[str] = None,
                   start_date: Optional[str] = None,
                   end_date: Optional[str] = None,
                   sort_by: Optional[str] = None,
                   sort_order: Optional[str] = None) -> List[Dict]:
        """
        Find deals from the HiEnergy API.

        Args:
            search: Optional search term to filter deals
            category: Optional category to filter deals
            advertiser_id: Optional advertiser ID/slug to filter deals
            min_commission: Optional minimum commission rate
            limit: Maximum number of results to return
            offset: Offset for pagination (legacy)
            cursor: Cursor pagination token
            page: Offset pagination page number
            per_page: Offset pagination page size
            network_slug: Optional network slug filter
            start_date: Optional start date filter (YYYY-MM-DD)
            end_date: Optional end date filter (YYYY-MM-DD)
            sort_by: Optional sort field
            sort_order: Optional sort direction (asc/desc)

        Returns:
            List of deal dictionaries
        """
        params: Dict[str, Any] = {
            'limit': self._clamp_page_size(limit),
            'offset': offset
        }
        if search:
            params['name'] = search
        if category:
            params['category'] = category
        if advertiser_id:
            params['advertiser_id'] = advertiser_id
        if min_commission is not None:
            params['min_commission'] = min_commission
        if cursor:
            params['cursor'] = cursor
        if page is not None:
            params['page'] = page
        if per_page is not None:
            params['per_page'] = self._clamp_page_size(per_page)
        if network_slug:
            params['network_slug'] = network_slug
        if start_date:
            params['start_date'] = start_date
        if end_date:
            params['end_date'] = end_date
        if sort_by:
            params['sort_by'] = sort_by
        if sort_order:
            params['sort_order'] = sort_order

        response = self._make_request('deals', params=params)
        results = self._extract_list_data(response)

        # Fallback 1: some endpoints still expect `search` instead of `name`.
        if search and not results:
            fallback_params = dict(params)
            fallback_params.pop('name', None)
            fallback_params['search'] = search
            fallback_response = self._make_request('deals', params=fallback_params)
            results = self._extract_list_data(fallback_response)

        # Fallback 2: multi-word token search with de-dup if exact phrase misses.
        if search and not results and ' ' in search.strip():
            merged: List[Dict[str, Any]] = []
            seen_ids = set()
            for token in [t.strip() for t in search.split() if t.strip()]:
                token_params = dict(params)
                token_params['name'] = token
                token_response = self._make_request('deals', params=token_params)
                token_results = self._extract_list_data(token_response)
                if not token_results:
                    token_params.pop('name', None)
                    token_params['search'] = token
                    token_response = self._make_request('deals', params=token_params)
                    token_results = self._extract_list_data(token_response)

                for item in token_results:
                    item_id = str(item.get('id'))
                    if item_id not in seen_ids:
                        seen_ids.add(item_id)
                        merged.append(item)
            results = merged

        return results
    
    def get_transactions(self, search: Optional[str] = None,
                         advertiser_id: Optional[str] = None,
                         network_id: Optional[str] = None,
                         start_date: Optional[str] = None,
                         end_date: Optional[str] = None,
                         currency: Optional[str] = None,
                         sort_by: Optional[str] = None,
                         sort_order: Optional[str] = None,
                         limit: int = 200,
                         offset: int = 0,
                         cursor: Optional[str] = None,
                         page: Optional[int] = None,
                         per_page: Optional[int] = None,
                         advertiser_slug: Optional[str] = None,
                         network_slug: Optional[str] = None,
                         status: Optional[str] = None,
                         contact_id: Optional[str] = None) -> List[Dict]:
        """
        Get transactions from the HiEnergy API.

        Args:
            search: Optional broad search text (client-assisted)
            advertiser_id: Filter by advertiser id/slug
            network_id: Filter by network id/slug
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            currency: Currency code filter (USD/EUR/...)
            sort_by: Sort field (transaction_date|commission_amount|sale_amount)
            sort_order: Sort direction (asc|desc)
            limit: Maximum number of results to return
            offset: Offset for pagination (legacy)
            cursor: Cursor pagination token
            page: Offset pagination page number
            per_page: Offset pagination page size
            advertiser_slug: Legacy alias for advertiser_id
            network_slug: Legacy alias for network_id
            status: Optional status filter (best-effort; if supported)
            contact_id: Optional contact filter (best-effort; if supported)

        Returns:
            List of transaction dictionaries
        """
        params: Dict[str, Any] = {
            'limit': self._clamp_page_size(limit),
            'offset': offset
        }

        if advertiser_id:
            params['advertiser_id'] = advertiser_id
        if advertiser_slug:
            params['advertiser_slug'] = advertiser_slug
        if network_id:
            params['network_id'] = network_id
        if network_slug:
            params['network_slug'] = network_slug
        if start_date:
            params['start_date'] = start_date
        if end_date:
            params['end_date'] = end_date
        if currency:
            params['currency'] = currency
        if sort_by:
            params['sort_by'] = sort_by
        if sort_order:
            params['sort_order'] = sort_order
        if cursor:
            params['cursor'] = cursor
        if page is not None:
            params['page'] = page
        if per_page is not None:
            params['per_page'] = self._clamp_page_size(per_page)
        if status:
            params['status'] = status
        if contact_id:
            params['contact_id'] = contact_id

        # If search is provided, try server-side targeted filters first.
        if search and not any([advertiser_id, advertiser_slug, network_id, network_slug]):
            candidate_filters = [
                {'advertiser_id': search},
                {'advertiser_slug': search},
                {'network_id': search},
                {'network_slug': search},
            ]

            for candidate in candidate_filters:
                try_params = dict(params)
                try_params.update(candidate)
                try:
                    response = self._make_request('transactions', params=try_params)
                    items = self._extract_list_data(response)
                    if items:
                        return items
                except Exception:
                    # Some candidate filters may not be accepted by backend for a given value.
                    continue

        response = self._make_request('transactions', params=params)
        results = self._extract_list_data(response)

        # Client-side fallback for broad text search when API has no generic text param.
        if search:
            query = search.lower().strip()
            if query:
                filtered: List[Dict[str, Any]] = []
                for tx in results:
                    advertiser = tx.get('advertiser') if isinstance(tx.get('advertiser'), dict) else {}
                    network = tx.get('network') if isinstance(tx.get('network'), dict) else {}
                    haystack = ' '.join([
                        str(tx.get('id', '')),
                        str(tx.get('transaction_id', '')),
                        str(tx.get('order_id', '')),
                        str(tx.get('status', '')),
                        str(tx.get('currency', '')),
                        str(tx.get('advertiser_id', '')),
                        str(tx.get('advertiser_slug', '')),
                        str(advertiser.get('id', '')),
                        str(advertiser.get('name', '')),
                        str(advertiser.get('slug', '')),
                        str(network.get('id', '')),
                        str(network.get('name', '')),
                        str(network.get('slug', '')),
                    ]).lower()
                    if query in haystack:
                        filtered.append(tx)
                results = filtered

        return results

    def get_contacts(self, search: Optional[str] = None,
                     email: Optional[str] = None,
                     phone: Optional[str] = None,
                     limit: int = 200, offset: int = 0) -> List[Dict]:
        """
        Get contacts from the HiEnergy API.

        Args:
            search: Optional search term to filter contacts
            email: Optional email filter
            phone: Optional phone filter
            limit: Maximum number of results to return
            offset: Offset for pagination

        Returns:
            List of contact dictionaries
        """
        params = {
            'limit': self._clamp_page_size(limit),
            'offset': offset
        }
        if search:
            params['name'] = search
        if email:
            params['email'] = email
        if phone:
            params['phone'] = phone

        response = self._make_request('contacts', params=params)
        return self._extract_list_data(response)

    def get_advertiser_details(self, advertiser_id: str) -> Dict:
        """
        Get detailed information about a specific advertiser.
        
        Args:
            advertiser_id: The ID of the advertiser
            
        Returns:
            Advertiser details dictionary
        """
        response = self._make_request(f'advertisers/{advertiser_id}')
        return self._extract_single_data(response)
    
    def get_program_details(self, program_id: str) -> Dict:
        """
        Get detailed information about a specific affiliate program.
        
        Args:
            program_id: The ID of the affiliate program
            
        Returns:
            Program details dictionary
        """
        response = self._make_request(f'affiliate_programs/{program_id}')
        return self._extract_single_data(response)
    
    def get_deal_details(self, deal_id: str) -> Dict:
        """
        Get detailed information about a specific deal.
        
        Args:
            deal_id: The ID of the deal
            
        Returns:
            Deal details dictionary
        """
        response = self._make_request(f'deals/{deal_id}')
        return self._extract_single_data(response)
    
    def get_transaction_details(self, transaction_id: str) -> Dict:
        """
        Get detailed information about a specific transaction.

        Args:
            transaction_id: The ID of the transaction

        Returns:
            Transaction details dictionary
        """
        response = self._make_request(f'transactions/{transaction_id}')
        return self._extract_single_data(response)

    def get_contact_details(self, contact_id: str) -> Dict:
        """
        Get detailed information about a specific contact.

        Args:
            contact_id: The ID of the contact

        Returns:
            Contact details dictionary
        """
        response = self._make_request(f'contacts/{contact_id}')
        return self._extract_single_data(response)

    def _looks_like_domain_or_url(self, text: str) -> bool:
        t = (text or '').strip().lower()
        return '.' in t or t.startswith('http://') or t.startswith('https://')

    def _is_detail_request(self, question_lower: str) -> bool:
        detail_terms = ['more detail', 'details', 'detail', 'profile', 'show endpoint', 'full info', 'deep dive']
        return any(term in question_lower for term in detail_terms)

    def _is_yes_reply(self, question_lower: str) -> bool:
        yes_tokens = {'yes', 'y', 'yeah', 'yep', 'sure', 'ok', 'okay', 'please do'}
        cleaned = question_lower.strip()
        return cleaned in yes_tokens

    def answer_question(self, question: str, context: Optional[Dict] = None) -> str:
        """
        Answer a question about advertisers, affiliate programs, or deals.
        
        This method analyzes the question and queries the appropriate endpoints
        to provide an answer.
        
        Args:
            question: The question to answer
            context: Optional context to help answer the question
            
        Returns:
            Answer string
        """
        question_lower = question.lower()

        # Follow-up flow: user replied "yes" to detail offer from advertiser index results.
        if context and self._is_yes_reply(question_lower):
            last_adv_id = context.get('last_advertiser_id') if isinstance(context, dict) else None
            if last_adv_id:
                details = self.get_advertiser_details(str(last_adv_id))
                return self._format_advertiser_details_answer(details)

        search_term = self._extract_search_term(question)

        # Determine the type of question
        if any(term in question_lower for term in ['advertiser', 'company', 'brand', 'merchant']) or self._looks_like_domain_or_url(search_term):
            # Question about advertisers
            advertisers = self.get_advertisers(search=search_term)
            if advertisers:
                if self._is_detail_request(question_lower):
                    first = advertisers[0]
                    adv_id = first.get('id')
                    if adv_id:
                        details = self.get_advertiser_details(str(adv_id))
                        return self._format_advertiser_details_answer(details)
                return self._format_advertisers_answer(advertisers, question)
            else:
                return "I couldn't find any advertisers matching your query."

        elif any(term in question_lower for term in ['program', 'affiliate program', 'partnership']):
            # Question about affiliate programs
            if 'research' in question_lower or 'best' in question_lower or 'top' in question_lower:
                report = self.research_affiliate_programs(search=self._extract_search_term(question), top_n=5)
                if report.get('programs'):
                    return self._format_program_research_answer(report)
                return "I couldn't find any affiliate programs matching your query."

            programs = self.get_affiliate_programs(search=self._extract_search_term(question))
            if programs:
                answer = self._format_programs_answer(programs, question)
                if len(programs) > 1:
                    answer += "\nThere are multiple matches. Do you want a specific publisher or network?"
                return answer
            else:
                return "I couldn't find any affiliate programs matching your query."
        
        elif any(term in question_lower for term in ['deal', 'offer', 'discount', 'promotion', 'coupon']):
            # Question about deals
            deals = self.find_deals(search=self._extract_search_term(question))
            if deals:
                return self._format_deals_answer(deals, question)
            else:
                return "I couldn't find any deals matching your query."

        elif any(term in question_lower for term in ['transaction', 'payment', 'sale', 'order', 'invoice']):
            # Question about transactions
            transactions = self.get_transactions(search=self._extract_search_term(question))
            if transactions:
                return self._format_transactions_answer(transactions, question)
            else:
                return "I couldn't find any transactions matching your query."

        elif any(term in question_lower for term in ['contact', 'customer', 'lead', 'client', 'prospect']):
            # Question about contacts
            contacts = self.get_contacts(search=self._extract_search_term(question))
            if contacts:
                return self._format_contacts_answer(contacts, question)
            else:
                return "I couldn't find any contacts matching your query."

        else:
            # General search across all
            return self._general_search(question)
    
    def _extract_search_term(self, question: str) -> str:
        """Extract the main search term from a question."""
        # Remove common question words
        stop_words = ['what', 'are', 'the', 'is', 'about', 'tell', 'me', 'show',
                      'find', 'get', 'list', 'any', 'which', 'who', 'how',
                      'search', 'for', 'advertiser', 'advertisers', 'affiliate',
                      'program', 'programs']
        words = question.lower().split()
        filtered_words = [w.strip('?.,!') for w in words if w.lower() not in stop_words]
        # Return first few keywords to keep search focused
        return ' '.join(filtered_words[:self.MAX_SEARCH_TERMS]) if filtered_words else question
    
    def _extract_advertiser_id(self, item: Dict[str, Any]) -> Optional[str]:
        """Best-effort advertiser id extraction from mixed response shapes."""
        if not isinstance(item, dict):
            return None

        advertiser_obj = item.get('advertiser') if isinstance(item.get('advertiser'), dict) else {}

        candidates = [
            item.get('advertiser_id'),
            advertiser_obj.get('id'),
            item.get('id'),
        ]

        for candidate in candidates:
            if candidate is None:
                continue
            text = str(candidate).strip()
            if text:
                return text
        return None

    def _advertiser_link(self, advertiser_id: Optional[str]) -> str:
        """Build the canonical advertiser details link."""
        if not advertiser_id:
            return 'N/A'
        return f"https://app.hienergy.ai/a/{advertiser_id}"

    def _format_advertisers_answer(self, advertisers: List[Dict], question: str) -> str:
        """Format advertisers data into an answer (including publisher context)."""
        if len(advertisers) == 1:
            adv = advertisers[0]
            publisher = adv.get('publisher_name') or adv.get('agency_name') or adv.get('publisher_id') or 'Unknown'
            network = adv.get('network_name') or 'Unknown'
            adv_id = self._extract_advertiser_id(adv)
            link = self._advertiser_link(adv_id)
            return (
                f"Found advertiser: {adv.get('name', 'Unknown')} "
                f"(publisher: {publisher}, network: {network}) - "
                f"{adv.get('description', 'No description available')}\n"
                f"More info: {link}\n"
                f"Want a deeper summary from the advertiser profile? Reply 'yes'."
            )
        else:
            rows = []
            for adv in advertisers[:self.MAX_DISPLAY_ITEMS]:
                publisher = adv.get('publisher_name') or adv.get('agency_name') or adv.get('publisher_id') or 'Unknown'
                link = self._advertiser_link(self._extract_advertiser_id(adv))
                rows.append(f"{adv.get('name', 'Unknown')} [publisher: {publisher}] ({link})")
            return (
                f"Found {len(advertisers)} advertisers: {', '.join(rows)}\n"
                f"Want a deeper summary for the top match from the advertiser profile? Reply 'yes'."
            )

    def _format_advertiser_details_answer(self, advertiser: Dict[str, Any]) -> str:
        """Format advertiser show-endpoint details."""
        if not advertiser:
            return "I couldn't load advertiser details."

        name = advertiser.get('name', 'Unknown')
        advertiser_id = advertiser.get('id', 'Unknown')
        domain = advertiser.get('domain', 'N/A')
        url = advertiser.get('url', 'N/A')
        status = advertiser.get('status') or advertiser.get('program_status') or 'N/A'
        publisher = advertiser.get('publisher_name') or advertiser.get('agency_name') or advertiser.get('publisher_id') or 'Unknown'
        network = advertiser.get('network_name') or 'Unknown'
        commission = advertiser.get('commission_rate') or advertiser.get('avg_commission_rate') or 'N/A'

        return (
            f"Advertiser details: {name} (id: {advertiser_id})\n"
            f"- Domain: {domain}\n"
            f"- URL: {url}\n"
            f"- Status: {status}\n"
            f"- Publisher: {publisher}\n"
            f"- Network: {network}\n"
            f"- Commission: {commission}\n"
            f"- More info: {self._advertiser_link(str(advertiser_id))}"
        )
    
    def _format_programs_answer(self, programs: List[Dict], question: str) -> str:
        """Format affiliate program matches (backed by advertiser endpoints)."""
        if len(programs) == 1:
            prog = programs[0]
            link = self._advertiser_link(self._extract_advertiser_id(prog))
            network = prog.get('network_name') or 'Unknown'
            publisher = prog.get('publisher_name') or prog.get('agency_name') or prog.get('publisher_id') or 'Unknown'
            return (
                f"Found affiliate program: {prog.get('name', 'Unknown')} "
                f"(network: {network}, publisher: {publisher})\n"
                f"Related advertiser: {link}"
            )

        rows = []
        for prog in programs:
            link = self._advertiser_link(self._extract_advertiser_id(prog))
            network = prog.get('network_name') or 'Unknown'
            publisher = prog.get('publisher_name') or prog.get('agency_name') or prog.get('publisher_id') or 'Unknown'
            rows.append(f"{prog.get('name', 'Unknown')} [network: {network}, publisher: {publisher}] ({link})")
        return f"Found {len(programs)} affiliate programs: {', '.join(rows)}"
    
    def _format_deals_answer(self, deals: List[Dict], question: str) -> str:
        """Format deals data into an answer."""
        if len(deals) == 1:
            deal = deals[0]
            link = self._advertiser_link(self._extract_advertiser_id(deal))
            return (
                f"Found deal: {deal.get('title', 'Unknown')} - {deal.get('description', 'No description')}\n"
                f"Related advertiser: {link}"
            )
        else:
            titles = []
            for deal in deals[:self.MAX_DISPLAY_ITEMS]:
                link = self._advertiser_link(self._extract_advertiser_id(deal))
                titles.append(f"{deal.get('title', 'Unknown')} ({link})")
            return f"Found {len(deals)} deals: {', '.join(titles)}"

    def _format_program_research_answer(self, report: Dict[str, Any]) -> str:
        """Format affiliate program research report."""
        summary = report.get('summary', {})
        programs = report.get('programs', [])
        if not programs:
            return "No affiliate programs matched your research filters."

        lines = [
            (
                f"Program research: {summary.get('total_programs_matched', 0)} matches "
                f"(avg commission {summary.get('average_commission', 0)})."
            )
        ]
        for p in programs[:self.MAX_DISPLAY_ITEMS]:
            name = p.get('name', 'Unknown')
            commission = p.get('commission_rate', p.get('_commission_value', 'N/A'))
            link = self._advertiser_link(self._extract_advertiser_id(p))
            lines.append(f"- {name} (commission: {commission}) | advertiser: {link}")
        return '\n'.join(lines)

    def _format_transactions_answer(self, transactions: List[Dict], question: str) -> str:
        """Format transactions data into an answer."""
        if len(transactions) == 1:
            tx = transactions[0]
            amount = tx.get('amount', tx.get('sale_amount', 'N/A'))
            status = tx.get('status', 'unknown')
            link = self._advertiser_link(self._extract_advertiser_id(tx))
            return (
                f"Found transaction: {tx.get('id', 'Unknown')} - Amount: {amount}, Status: {status}\n"
                f"Related advertiser: {link}"
            )
        else:
            tx_rows = []
            for tx in transactions[:self.MAX_DISPLAY_ITEMS]:
                link = self._advertiser_link(self._extract_advertiser_id(tx))
                tx_rows.append(f"{str(tx.get('id', 'Unknown'))} ({link})")
            return f"Found {len(transactions)} transactions: {', '.join(tx_rows)}"

    def _format_contacts_answer(self, contacts: List[Dict], question: str) -> str:
        """Format contacts data into an answer."""
        if len(contacts) == 1:
            contact = contacts[0]
            name = contact.get('name') or contact.get('full_name') or 'Unknown'
            email = contact.get('email', 'N/A')
            return f"Found contact: {name} - Email: {email}"
        else:
            names = [
                (c.get('name') or c.get('full_name') or 'Unknown')
                for c in contacts[:self.MAX_DISPLAY_ITEMS]
            ]
            return f"Found {len(contacts)} contacts: {', '.join(names)}"
    
    def _general_search(self, question: str) -> str:
        """Perform a general search when question type is unclear."""
        search_term = self._extract_search_term(question)
        
        # Try all endpoints
        advertisers = self.get_advertisers(search=search_term, limit=3)
        programs = self.get_affiliate_programs(search=search_term, limit=3)
        deals = self.find_deals(search=search_term, limit=3)
        transactions = self.get_transactions(search=search_term, limit=3)
        contacts = self.get_contacts(search=search_term, limit=3)
        
        results = []
        if advertisers:
            results.append(f"Advertisers: {', '.join([a.get('name', 'Unknown') for a in advertisers])}")
        if programs:
            results.append(f"Programs: {', '.join([p.get('name', 'Unknown') for p in programs])}")
        if deals:
            results.append(f"Deals: {', '.join([d.get('title', 'Unknown') for d in deals])}")
        if transactions:
            results.append(f"Transactions: {', '.join([str(t.get('id', 'Unknown')) for t in transactions])}")
        if contacts:
            results.append(
                f"Contacts: {', '.join([(c.get('name') or c.get('full_name') or 'Unknown') for c in contacts])}"
            )
        
        if results:
            return "Found the following:\n" + "\n".join(results)
        else:
            return "I couldn't find any results for your question."


def main():
    """Example usage of the HiEnergy skill."""
    import sys
    
    # Check if API key is provided
    if len(sys.argv) > 1:
        api_key = sys.argv[1]
    else:
        api_key = os.environ.get('HIENERGY_API_KEY')
    
    if not api_key:
        print("Usage: python hienergy_skill.py <api_key>")
        print("Or set HIENERGY_API_KEY environment variable")
        sys.exit(1)
    
    # Create skill instance
    skill = HiEnergySkill(api_key=api_key)
    
    # Example queries
    print("=" * 60)
    print("HiEnergy API Skill - Example Usage")
    print("=" * 60)
    
    try:
        # Get advertisers
        print("\n1. Getting advertisers:")
        advertisers = skill.get_advertisers(limit=5)
        print(f"   Found {len(advertisers)} advertisers")
        
        # Get affiliate programs
        print("\n2. Getting affiliate programs:")
        programs = skill.get_affiliate_programs(limit=5)
        print(f"   Found {len(programs)} programs")
        
        # Find deals
        print("\n3. Finding deals:")
        deals = skill.find_deals(limit=5)
        print(f"   Found {len(deals)} deals")
        
        # Get transactions
        print("\n4. Getting transactions:")
        transactions = skill.get_transactions(limit=5)
        print(f"   Found {len(transactions)} transactions")

        # Get contacts
        print("\n5. Getting contacts:")
        contacts = skill.get_contacts(limit=5)
        print(f"   Found {len(contacts)} contacts")

        # Answer a question
        print("\n6. Answering questions:")
        question = "What transactions were recently created?"
        answer = skill.answer_question(question)
        print(f"   Q: {question}")
        print(f"   A: {answer}")
        
    except Exception as e:
        print(f"\nError: {e}")
        print("\nNote: This is a mock implementation. The actual API endpoints may differ.")
        print("Please refer to https://app.hienergy.ai/api_documentation for details.")


if __name__ == '__main__':
    main()
