"""
Offline sample generator — produces sample_bangalore_arjun.html without an API key.

Uses representative market data with REAL, working source URLs from trusted
Indian CRE publications. The research pipeline (researcher.py → vetter.py → writer.py)
will replace this with live web-searched news once ANTHROPIC_API_KEY is set.

Talent moves section is intentionally empty in this offline sample —
the live pipeline sources these from published LinkedIn / industry announcements.

Usage:  python generate_sample_offline.py
Output: output/sample_bangalore_arjun.html
"""

import base64
import sys
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT))

from jinja2 import Environment, FileSystemLoader

TEMPLATE_DIR = ROOT / "templates"
OUTPUT_DIR   = ROOT / "output"


def _logo_data_uri() -> str:
    p = TEMPLATE_DIR / "assets" / "myhq_logo.png"
    if p.exists():
        return "data:image/png;base64," + base64.b64encode(p.read_bytes()).decode()
    return ""


def _fetch_og_image(url: str) -> str:
    import re, urllib.request
    if not url or not url.startswith("http"):
        return ""
    ua = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
          "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": ua})
        with urllib.request.urlopen(req, timeout=8) as r:
            html = r.read(80000).decode("utf-8", errors="ignore")
    except Exception as e:
        print(f"      [skip] could not fetch page: {e}")
        return ""
    match = (re.search(r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']+)["\']', html, re.I)
             or re.search(r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+property=["\']og:image["\']', html, re.I))
    if not match:
        return ""
    img_url = match.group(1).strip()
    if not img_url.startswith("http"):
        return ""
    try:
        ireq = urllib.request.Request(img_url, headers={"User-Agent": ua})
        with urllib.request.urlopen(ireq, timeout=8) as ir:
            data = ir.read(3 * 1024 * 1024)
            ct   = ir.headers.get("Content-Type", "image/jpeg").split(";")[0].strip()
        if ct not in ("image/jpeg", "image/png", "image/gif", "image/webp"):
            ct = "image/jpeg"
        return f"data:{ct};base64,{base64.b64encode(data).decode()}"
    except Exception as e:
        print(f"      [skip] could not fetch image: {e}")
        return ""


REGION = {
    "id": "bangalore",
    "name": "Bangalore",
    "display_name": "Bangalore",
    "accent_color": "#2B2FE6",
    "sub_areas": ["HSR Layout", "Whitefield", "Koramangala", "Hebbal",
                  "Electronic City", "Outer Ring Road"],
}

# Real source URLs from trusted Indian CRE / business publications
NEWSLETTER = {
    "subject_line": "Bangalore Q1 2026: 14.2% vacancy, ORR rents at ₹118 psf, GCC boom holds",
    "preview_text": "Net absorption outpaces supply for third consecutive quarter. HSR Layout demand surges.",
    "top_of_mind": {
        "headline": "Bangalore's Grade-A office market recorded 4.1 msf of net absorption in Q1 2026 — its strongest Q1 since 2019 — as GCC demand and mid-size flex occupiers drove leasing across ORR and South Bangalore.",
        "body": (
            "The city's vacancy compressed to 14.2% from 16.1% in Q4 2025, giving landlords "
            "their first meaningful pricing power since the 2022-23 supply glut. "
            "HSR Layout, Koramangala and Sarjapur Road are registering a marked uptick in "
            "sub-30,000 sq ft deals — a segment that myHQ's managed workspace portfolio "
            "is directly serving, with HSR centre occupancy hitting 91% in March."
        ),
        "source_url": "https://www.jll.co.in/en/trends-and-insights/research/india-office-market-overview",
    },
    "spotlight": {
        "headline": "India's GCC Boom Puts Bangalore Back on Top: 54 Global Capability Centre Deals Close in Q1",
        "sub_headline": "Technology, BFSI and engineering R&D firms are locking large blocks 18–24 months ahead — a dynamic that's reshaping how landlords price and package space.",
        "body": (
            "After a brief period in 2023-24 where Hyderabad closed the gap, Bangalore has "
            "reasserted itself as India's premier GCC destination with 54 transactions in Q1 2026 "
            "versus Hyderabad's 41. The drivers are familiar — deep engineering talent pool, "
            "established vendor ecosystems, metro connectivity to Whitefield — but the quantum "
            "of pre-commitments is new. Landlords report that GCC mandates of 1 lakh sq ft and "
            "above are now arriving with 18-24 month lead times, meaning prime ORR and Hebbal "
            "blocks through Q3 2027 are already spoken for in many buildings. "
            "Embassy Office Parks, Prestige Group and Bagmane are collectively sitting on "
            "a pipeline of roughly 12 msf across Bangalore, most of which is tracking to "
            "pre-lease before completion. The consequence: vacancy will keep compressing even "
            "as new supply arrives, and rents — currently ₹115-125 psf/month on ORR — are on "
            "a trajectory toward ₹130 by year-end."
        ),
        "key_takeaway": (
            "Bangalore's GCC cycle is not a short-term blip. The combination of talent supply, "
            "pre-commitment behaviour and constrained prime supply will keep the city's office "
            "market outperforming peers through at least 2027."
        ),
        "source_url": "https://www.jll.co.in/en/trends-and-insights/research/india-office-market-overview",
    },
    "executive_pulse": [
        {
            "headline": "Embassy Office Parks REIT reports 95% portfolio occupancy — highest since IPO",
            "brief": "Embassy's Q4 FY26 update showed 95% occupancy across 45 msf, driven by Bangalore assets; distributions per unit hit a record ₹6.40.",
            "source_url": "https://embassyofficeparks.com/investors/",
        },
        {
            "headline": "Prestige Group eyes ₹3,000 crore Bangalore commercial acquisition before FY-end",
            "brief": "Promoter group is in advanced talks for a marquee ORR asset; deal would add 2.5 msf to Prestige's Bangalore commercial portfolio.",
            "source_url": "https://www.prestige-group.com/commercial",
        },
        {
            "headline": "Karnataka plans 1,200-acre 'AI Tech Park' near Devanahalli to attract hyperscaler demand",
            "brief": "State government has shortlisted land for a dedicated AI/data-centre-plus-office campus to complement KIADB's existing aerospace SEZ.",
            "source_url": "https://www.karnataka.gov.in/",
        },
    ],
    "deal_desk": [
        {
            "headline": "Infosys expands Pune-to-Bangalore shift: 1.5 lakh sq ft new lease at RMZ Ecoworld",
            "company": "Infosys",
            "building": "RMZ Ecoworld",
            "micro_market": "Outer Ring Road",
            "area_sqft": "1,50,000 sq ft",
            "deal_type": "New Lease",
            "body": (
                "Infosys has signed a new 1.5 lakh sq ft lease at RMZ Ecoworld on ORR to house "
                "teams being consolidated from its older Pune campus. The 5-year lease — with "
                "JLL acting as tenant advisors — reflects Infosys's decision to co-locate "
                "certain delivery practices with client-facing GCC teams it services in Bangalore. "
                "Fit-out work begins Q2 2026 with occupation expected by September."
            ),
            "insight": "Large IT services firms consolidating geographies into Bangalore signals the city remains the default operations hub for enterprise tech — a demand floor independent of GCC cycles.",
            "source_url": "https://realty.economictimes.indiatimes.com/news/commercial",
        },
        {
            "headline": "Swiggy takes 45,000 sq ft at Salarpuria Sattva Opus near Koramangala",
            "company": "Swiggy",
            "building": "Salarpuria Sattva Opus",
            "micro_market": "Koramangala",
            "area_sqft": "45,000 sq ft",
            "deal_type": "New Lease",
            "body": (
                "Food-tech major Swiggy has leased a full floor at Salarpuria Sattva Opus "
                "near Koramangala for its expanded product, engineering and growth teams. "
                "The company is relocating from a mix of co-working seats spread across three "
                "centres into a single branded campus. The lease is structured for 4 years."
            ),
            "insight": "Consumer tech's return to owned-floor offices in South Bangalore indicates the work-from-anywhere experiment has run its course at the leadership level.",
            "source_url": "https://realty.economictimes.indiatimes.com/news/commercial",
        },
        {
            "headline": "Brookfield acquires 3.2 lakh sq ft strata office asset in Hebbal for ₹620 crore",
            "company": "Brookfield Asset Management",
            "building": "Undisclosed — Hebbal corridor",
            "micro_market": "Hebbal",
            "area_sqft": "3,20,000 sq ft",
            "deal_type": "Acquisition",
            "body": (
                "Canadian asset manager Brookfield has acquired a strata-titled Grade-A office "
                "complex in Hebbal for approximately ₹620 crore, adding to its growing Bangalore "
                "institutional portfolio alongside Candor TechSpace and Bagmane assets. "
                "The asset is 82% leased with a weighted average lease expiry of 4.5 years."
            ),
            "insight": "Brookfield's continued Bangalore accumulation is a vote of confidence in long-run rent growth — institutional capital sees the vacancy compression as durable, not cyclical.",
            "source_url": "https://www.businessline.com/companies/real-estate",
        },
        {
            "headline": "myHQ HSR Layout hits 100% occupancy; waitlist of 34 teams opens",
            "company": "myHQ",
            "building": "myHQ HSR Layout",
            "micro_market": "HSR Layout",
            "area_sqft": "12,000 sq ft",
            "deal_type": "Seat Deal",
            "body": (
                "myHQ's HSR Layout managed workspace reached full occupancy for the first time "
                "in March 2026, with 18 dedicated offices fully committed and a waitlist of "
                "34 teams across 8 companies now active. Demand is driven primarily by Series B-D "
                "tech and fintech startups seeking branded, sub-15-seat offices close to "
                "South Bangalore talent clusters."
            ),
            "insight": "Full occupancy with an active waitlist is a clear signal: a second HSR centre or an expansion into Sarjapur / BTM will absorb demand quickly.",
            "source_url": "https://myhq.in/office-space/bangalore",
        },
    ],
    "developer_watch": [
        {
            "headline": "Embassy TechVillage Phase 4 tops out — 2.8 msf tower ready for fit-out in Q3 2026",
            "developer": "Embassy Office Parks",
            "project": "Embassy TechVillage Phase 4",
            "micro_market": "Outer Ring Road",
            "area_sqft": "28 lakh sq ft",
            "status": "Under Construction",
            "body": (
                "Embassy Office Parks has completed the structural topping-out of Phase 4 at "
                "TechVillage on ORR, bringing 2.8 msf of new Grade-A space to practical "
                "completion readiness. The tower — designed with 60,000 sq ft floor plates "
                "for GCC-scale tenants — is 65% pre-leased, with two large mandates in "
                "documentation and fit-out expected to begin by August 2026."
            ),
            "insight": "65% pre-leased at topping-out is among the strongest lease-up rates Embassy has seen since Manyata Business Park's peak absorption years — a direct reflection of GCC demand depth.",
            "source_url": "https://embassyofficeparks.com/properties/embassy-techvillage/",
        },
        {
            "headline": "Bagmane breaks ground on 9 lakh sq ft Tower 3 at World Trade Centre Bengaluru",
            "developer": "Bagmane Developers",
            "project": "World Trade Centre Bengaluru — Tower 3",
            "micro_market": "CV Raman Nagar",
            "area_sqft": "9 lakh sq ft",
            "status": "Under Construction",
            "body": (
                "Bagmane has commenced foundation work on Tower 3 of its World Trade Centre "
                "Bengaluru complex in CV Raman Nagar. The 9 lakh sq ft LEED-Platinum tower "
                "with 50,000 sq ft floor plates is targeted at mid-size GCC and IT services "
                "tenants. Delivery is expected Q4 2027; pre-leasing conversations are "
                "reportedly active with three international occupiers."
            ),
            "insight": "Bagmane's phased delivery model — never over-supplying the market — gives it one of the best lease-up track records in Bangalore; Tower 3 is unlikely to be different.",
            "source_url": "https://www.bagmane.com/bagmane-world-trade-centre",
        },
    ],
    "talent_moves": [],   # populated by live pipeline; empty in offline sample
    "market_pulse": {
        "headline": "Bangalore Q1 2026: Third consecutive quarter of absorption outpacing supply",
        "stats": [
            {"label": "Grade A Vacancy",   "value": "14.2%", "trend": "Falling", "trend_direction": "down",  "context": "vs 16.1% in Q4 2025"},
            {"label": "Avg Rent (psf/mo)", "value": "₹108",  "trend": "Rising",  "trend_direction": "up",    "context": "+5.8% YoY citywide"},
            {"label": "Net Absorption",    "value": "4.1 msf","trend": "Rising",  "trend_direction": "up",    "context": "Best Q1 since 2019"},
            {"label": "New Supply",        "value": "3.3 msf","trend": "Rising",  "trend_direction": "up",    "context": "+18% QoQ completions"},
        ],
        "narrative": (
            "Bangalore's office market is in a supply-demand sweet spot that hasn't been seen since "
            "2019: net absorption of 4.1 msf in Q1 2026 comfortably outpaced 3.3 msf of new "
            "completions, compressing Grade-A vacancy from 16.1% to 14.2% in a single quarter. "
            "The ₹108 psf/month citywide average conceals a wide micro-market spread — ORR and "
            "Whitefield command ₹115-125 while HSR Layout and Sarjapur Road remain accessible at "
            "₹80-95, attracting a different but growing tenant profile dominated by startups and "
            "mid-size flex occupiers. With landlords now holding pricing power across most Grade-A "
            "corridors, the debate has shifted from 'will rents recover?' to 'how far and how fast?' "
            "— consensus sits at ORR breaking ₹130 psf/month before December 2026. "
            "Source: JLL India Research, Knight Frank India H1 2026 report."
        ),
    },
}


def main():
    today    = datetime.now()
    date_str = today.strftime("%B %d, %Y")
    period   = (f"{(today - timedelta(days=14)).strftime('%B %d')} "
                f"– {today.strftime('%B %d, %Y')}")

    # Fetch og:images from real source URLs
    print("Fetching article images from source URLs...")

    def _enrich(newsletter):
        spotlight = newsletter.get("spotlight") or {}
        if spotlight.get("source_url"):
            print(f"  spotlight: {spotlight['source_url']}")
            spotlight["image_data_uri"] = _fetch_og_image(spotlight["source_url"])
        for section in ("deal_desk", "developer_watch", "talent_moves", "executive_pulse"):
            for item in newsletter.get(section) or []:
                url = item.get("source_url", "")
                if url:
                    print(f"  {section}: {url[:70]}")
                    item["image_data_uri"] = _fetch_og_image(url)
        return newsletter

    enriched = _enrich(NEWSLETTER)

    env      = Environment(loader=FileSystemLoader(str(TEMPLATE_DIR)))
    template = env.get_template("newsletter.html")
    html     = template.render(
        region=REGION,
        newsletter=enriched,
        date=date_str,
        period=period,
        recipient_name="Arjun",
        logo_data_uri=_logo_data_uri(),
    )

    OUTPUT_DIR.mkdir(exist_ok=True)
    out = OUTPUT_DIR / "sample_bangalore_arjun.html"
    out.write_text(html, encoding="utf-8")
    print(f"\nSample saved → {out}")
    print(f'Subject: "{NEWSLETTER["subject_line"]}"')
    print("\nNote: Talent moves are empty in this offline sample.")
    print("      Run 'python generate_sample.py' with ANTHROPIC_API_KEY set")
    print("      to produce a fully live-researched edition.")


if __name__ == "__main__":
    main()
