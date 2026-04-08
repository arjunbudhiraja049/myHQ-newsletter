"""
Writer: Uses Claude Opus 4.6 with adaptive thinking to transform vetted news
into a structured, engaging newsletter. Returns a JSON dict that the
Jinja2 template consumes directly.
"""

import json
import re
from datetime import datetime, timedelta
import anthropic


def _extract_json_object(text: str) -> dict:
    text = text.strip()
    try:
        result = json.loads(text)
        if isinstance(result, dict):
            return result
    except json.JSONDecodeError:
        pass
    match = re.search(r'\{[\s\S]*\}', text)
    if match:
        try:
            result = json.loads(match.group())
            if isinstance(result, dict):
                return result
        except json.JSONDecodeError:
            pass
    return {}


def write_newsletter(region: dict, vetted_items: dict[str, list], voice: dict) -> dict:
    """
    Uses Claude Opus 4.6 with adaptive thinking to write the full newsletter.
    Returns a structured dict for the Jinja2 template.
    """
    client = anthropic.Anthropic()

    region_name = region["name"]
    today = datetime.now().strftime("%B %d, %Y")
    fortnight_start = (datetime.now() - timedelta(days=14)).strftime("%B %d")

    total_items = sum(len(v) for v in vetted_items.values())
    items_summary = json.dumps(vetted_items, indent=2)

    system_prompt = f"""You are the founding editor of myHQ's "Office Pulse" — India's most respected fortnightly commercial real estate newsletter.

Your readers are: Business POCs managing office decisions, brokers, developers, and real estate heads at top companies.
What they need: Clarity on what's happening in their market, why it matters, and what to watch next.
Your voice: Sharp. Specific. No fluff. Think Bloomberg Intelligence meets inside industry knowledge.

The newsletter covers {region_name}. You write it like a trusted colleague who knows every deal in the market.

Rules:
- Be specific: Name companies, buildings, exact locations, sq ft figures
- Every deal/project needs a "what this means" insight — the so-what
- Use Indian number formats where relevant (lakh sq ft, ₹X crore)
- If data is insufficient for a section, write "Market Update Pending" for that item
- Write subject lines that make people open the email"""

    prompt = f"""Today: {today}
Coverage period: {fortnight_start} – {today}
Region: {region_name}
Total vetted news items: {total_items}

VETTED NEWS ITEMS BY CATEGORY:
{items_summary}

Write the complete Office Pulse newsletter for {region_name}. Return ONLY a valid JSON object with this exact structure:

{{
  "subject_line": "Subject line max 60 chars — make it punchy and specific to this edition's biggest story",
  "preview_text": "Email preview text max 90 chars — the teaser that makes them open",
  "top_of_mind": {{
    "headline": "The single most important insight or stat this fortnight for {region_name} — 1 sharp sentence",
    "body": "2-3 sentences expanding on why this matters for the market right now"
  }},
  "executive_pulse": [
    {{"headline": "Quick hit 1 headline", "brief": "One sentence of context or data"}},
    {{"headline": "Quick hit 2 headline", "brief": "One sentence of context or data"}},
    {{"headline": "Quick hit 3 headline", "brief": "One sentence of context or data"}}
  ],
  "deal_desk": [
    {{
      "headline": "Deal headline",
      "company": "Tenant/occupier company name",
      "building": "Building or tech park name",
      "micro_market": "Specific micro-market (e.g. Whitefield, BKC, HITEC City)",
      "area_sqft": "XX,XXX sq ft — or 'Undisclosed' if not reported",
      "deal_type": "New Lease|Renewal|Expansion|Pre-Commitment|Seat Deal",
      "body": "2-3 sentences: what happened, who's involved, context",
      "insight": "What this deal signals about the market — 1 actionable sentence",
      "source_url": "URL of the original news article, or empty string if unavailable"
    }}
  ],
  "developer_watch": [
    {{
      "headline": "Project headline",
      "developer": "Developer name",
      "project": "Project / building name",
      "micro_market": "Location",
      "area_sqft": "Total leasable area",
      "status": "Announced|Under Construction|Completed|Pre-Leasing|REIT Acquisition",
      "body": "2-3 sentences on the project, timeline, significance",
      "insight": "Market implication — 1 sentence",
      "source_url": "URL of the original news article, or empty string if unavailable"
    }}
  ],
  "talent_moves": [
    {{
      "person": "Full name",
      "previous_role": "Previous Title, Previous Company",
      "new_role": "New Title, New Company",
      "brief": "2 sentences: what they're taking on and their background",
      "why_it_matters": "Why the market should pay attention — 1 sentence",
      "source_url": "URL of the original news article, or empty string if unavailable"
    }}
  ],
  "market_pulse": {{
    "headline": "Market summary headline for {region_name} this fortnight",
    "stats": [
      {{
        "label": "Grade A Vacancy",
        "value": "X.X%",
        "trend": "Rising|Falling|Stable",
        "trend_direction": "up|down|flat",
        "context": "vs last quarter or YoY"
      }},
      {{
        "label": "Avg Rent (psf/mo)",
        "value": "₹XXX",
        "trend": "Rising|Falling|Stable",
        "trend_direction": "up|down|flat",
        "context": "YoY or QoQ change"
      }},
      {{
        "label": "Net Absorption",
        "value": "X.X msf",
        "trend": "Rising|Falling|Stable",
        "trend_direction": "up|down|flat",
        "context": "H1 2026 or latest period"
      }},
      {{
        "label": "New Supply",
        "value": "X.X msf",
        "trend": "Rising|Falling|Stable",
        "trend_direction": "up|down|flat",
        "context": "pipeline or completed"
      }}
    ],
    "narrative": "3-4 sentences connecting the stats into a cohesive market picture for {region_name}"
  }},
  "spotlight": {{
    "headline": "Deep-dive story headline — the most interesting trend or story in the data",
    "sub_headline": "One-sentence teaser that makes the reader want to read on",
    "body": "4-6 sentences of analysis — connect dots, give context, cite specific examples from the data",
    "key_takeaway": "The one thing readers should remember from this story — 1-2 sentences",
    "source_url": "URL of the primary source article for this story, or empty string"
  }}
}}

Important: Return ONLY valid JSON. No markdown fences, no explanation before or after."""

    response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=16000,
        thinking={"type": "adaptive"},
        system=system_prompt,
        messages=[{"role": "user", "content": prompt}],
    )

    # Extract from response — thinking blocks come first, then text
    for block in response.content:
        if hasattr(block, "type") and block.type == "text":
            newsletter = _extract_json_object(block.text)
            if newsletter:
                return newsletter

    return {}
