"""
Researcher: Uses Claude Opus 4.6 with web_search + web_fetch to gather
office leasing news for a given region across all content pillars.
"""

import json
import re
import anthropic


SYSTEM_PROMPT = """You are a senior commercial real estate research analyst covering the Indian office market.
Your job is to search for and compile recent, verified news for a fortnightly industry newsletter.

When searching, look for content from the last 14 days. Prioritise sources like:
ET Realty, Business Standard, Moneycontrol, Knight Frank, JLL, CBRE, Cushman & Wakefield,
Anarock, LiveMint, The Hindu BusinessLine.

Always return your findings as a valid JSON array. Each item must follow this schema:
[
  {
    "headline": "Concise, factual headline",
    "source": "Publication name",
    "url": "URL if available, else empty string",
    "date": "Date string, e.g. April 5, 2026, or 'Recent' if not found",
    "summary": "2-3 sentence factual summary of the news",
    "companies": ["Company1", "Company2"],
    "micro_market": "Specific sub-area or micro-market within the region",
    "category": "transaction|developer|talent|market",
    "key_metric": "Key number if available, e.g. '50,000 sq ft', '₹120 psf/month', else empty string"
  }
]

Return ONLY a valid JSON array — no preamble, no explanation, no markdown fences.
If you genuinely find no relevant news, return an empty array: []
"""

CATEGORY_PROMPTS = {
    "transactions": (
        "Search for commercial office leasing TRANSACTIONS in {region_name} India from the last 14 days. "
        "Include: new leases signed, renewals, expansions, pre-commitments, seat deals. "
        "Focus on Grade A and Grade B office spaces. Name the tenant, building, area in sq ft, and deal type. "
        "Key sub-markets to cover: {sub_areas}. "
        "Good search queries: '{region_name} office lease deal 2026', "
        "'{region_name} company leases office space', 'office transaction {region_name}'"
    ),
    "developers": (
        "Search for DEVELOPER and new supply news in {region_name} India commercial real estate from the last 14 days. "
        "Include: new project announcements, project completions, pre-leasing activity, "
        "REIT acquisitions, park expansions. Key sub-markets: {sub_areas}. "
        "Good search queries: '{region_name} commercial project launch 2026', "
        "'{region_name} office park completion', 'new Grade A supply {region_name}'"
    ),
    "talent": (
        "Search for PEOPLE MOVEMENT in commercial real estate in {region_name} India from the last 14 days. "
        "Include: new appointments, promotions, leadership changes at developers, brokerages, "
        "REITs, property consultancies, and major occupier real estate teams. "
        "Good search queries: '{region_name} real estate appointment 2026', "
        "'joins as MD real estate India', 'commercial real estate India leadership change 2026'"
    ),
    "market": (
        "Search for MARKET DATA and analysis for the {region_name} office market from the last 14 days. "
        "Include: vacancy rates, average rents per sq ft, net absorption figures, "
        "new supply data, demand outlook, quarterly/annual reports from consultancies. "
        "Good search queries: '{region_name} office market Q1 2026', "
        "'{region_name} vacancy rate rent 2026', 'office absorption {region_name} report'"
    ),
}


def _extract_json_array(text: str) -> list:
    """Parse JSON array from Claude's text response, with fallback extraction."""
    text = text.strip()
    try:
        result = json.loads(text)
        if isinstance(result, list):
            return result
    except json.JSONDecodeError:
        pass

    # Try to find a JSON array within the text
    match = re.search(r'\[[\s\S]*\]', text)
    if match:
        try:
            result = json.loads(match.group())
            if isinstance(result, list):
                return result
        except json.JSONDecodeError:
            pass

    return []


def research_category(client: anthropic.Anthropic, region: dict, category: str) -> list:
    """
    Run one research call for a specific region + content category.
    Uses Claude Opus 4.6 with web_search and web_fetch (server-side tools).
    Handles pause_turn for long server-side loops.
    """
    region_name = region["name"]
    sub_areas = ", ".join(region["sub_areas"][:8])

    user_prompt = CATEGORY_PROMPTS[category].format(
        region_name=region_name,
        sub_areas=sub_areas,
    )

    messages = [{"role": "user", "content": user_prompt}]
    max_continuations = 4

    for _ in range(max_continuations):
        response = client.messages.create(
            model="claude-opus-4-6",
            max_tokens=8000,
            system=SYSTEM_PROMPT,
            tools=[
                {"type": "web_search_20260209", "name": "web_search"},
                {"type": "web_fetch_20260209", "name": "web_fetch"},
            ],
            messages=messages,
        )

        if response.stop_reason in ("end_turn", "stop_sequence"):
            break

        if response.stop_reason == "pause_turn":
            # Server-side tool loop hit iteration limit — re-send to continue
            messages = [
                {"role": "user", "content": user_prompt},
                {"role": "assistant", "content": response.content},
            ]
            continue

        # Any other stop reason — break and use what we have
        break

    # Extract JSON from the final text block
    for block in response.content:
        if hasattr(block, "type") and block.type == "text":
            items = _extract_json_array(block.text)
            if items:
                return items

    return []


def research_region(region: dict) -> dict[str, list]:
    """
    Research all 4 content pillars for a region.
    Returns a dict keyed by category with lists of raw news items.
    """
    client = anthropic.Anthropic()

    categories = ["transactions", "developers", "talent", "market"]
    results = {}

    for category in categories:
        print(f"  Researching [{category}] for {region['name']}...")
        items = research_category(client, region, category)
        results[category] = items
        print(f"    Found {len(items)} raw items")

    return results
