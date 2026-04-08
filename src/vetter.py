"""
Vetter: Uses Claude Haiku to score and filter raw news items.
Each item is scored on relevance, recency, geographic specificity,
business impact, and source credibility. Items below threshold are dropped.
"""

import json
import re
import anthropic


SCORE_THRESHOLD = 6.0  # Items with average score below this are dropped


def _extract_json_array(text: str) -> list:
    text = text.strip()
    try:
        result = json.loads(text)
        if isinstance(result, list):
            return result
    except json.JSONDecodeError:
        pass
    match = re.search(r'\[[\s\S]*\]', text)
    if match:
        try:
            result = json.loads(match.group())
            if isinstance(result, list):
                return result
        except json.JSONDecodeError:
            pass
    return []


def vet_category(client: anthropic.Anthropic, items: list, region: dict, category: str) -> list:
    """
    Score and filter news items for a single category using Claude Haiku.
    Returns only items that pass the quality threshold.
    """
    if not items:
        return []

    region_name = region["name"]
    sub_areas_str = ", ".join(region["sub_areas"][:6])
    items_json = json.dumps(items, indent=2)

    prompt = f"""You are a data quality analyst for the myHQ Office Pulse newsletter.

Region: {region_name}
Key sub-markets: {sub_areas_str}
Category: {category}

Review these raw news items and score each one. Be strict — we only want high-quality, relevant items.

ITEMS TO VET:
{items_json}

Score each item (1-10) on five dimensions:
1. relevance: Is this directly about commercial office real estate in India? (Not residential, not retail, not unrelated sector)
2. recency: Is this clearly recent (last 14 days)? Score 8-10 if date confirmed recent, 5-6 if "recent" but unclear, 1-3 if old.
3. geographic: Is this specifically about {region_name} and its sub-markets? Not just India in general?
4. impact: How significant is this for an office occupier, property manager, or broker in {region_name}?
5. credibility: Is the source a credible real estate or business publication?

Return ONLY a valid JSON array with each original item enriched with these new fields:
- "scores": {{"relevance": X, "recency": X, "geographic": X, "impact": X, "credibility": X}}
- "average_score": calculated float average of the 5 scores
- "include": true if average_score >= {SCORE_THRESHOLD}, false otherwise
- "vetter_note": one sentence explaining the include/exclude decision

Do NOT remove or change any original fields. Return ALL items (included and excluded) with scores.
Return ONLY valid JSON — no markdown, no explanation."""

    response = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=8000,
        messages=[{"role": "user", "content": prompt}],
    )

    for block in response.content:
        if hasattr(block, "type") and block.type == "text":
            vetted = _extract_json_array(block.text)
            if vetted:
                included = [item for item in vetted if item.get("include", False)]
                return included

    # Fallback: return all original items if vetting parse failed
    return items


def vet_research(raw_research: dict[str, list], region: dict) -> dict[str, list]:
    """
    Vet all categories for a region.
    Returns filtered dict with only high-quality items per category.
    """
    client = anthropic.Anthropic()
    vetted = {}

    for category, items in raw_research.items():
        print(f"  Vetting [{category}]: {len(items)} raw → ", end="", flush=True)
        passed = vet_category(client, items, region, category)
        vetted[category] = passed
        print(f"{len(passed)} passed")

    return vetted
