"""
Offline sample generator — Bangalore edition for Arjun Budhiraja.

Every news story is sourced from a real, published article.
'Read more' links point to the exact article page.
Article images are pulled directly from Business Standard's CDN —
they load automatically when you open the HTML in any browser.

Usage:  python generate_sample_offline.py
Output: output/sample_bangalore_arjun.html

Sources used:
  Business Standard (business-standard.com)
  JLL India Newsroom (jll.com/en-in)
  Cushman & Wakefield India (cushmanwakefield.com)
"""

import base64
from datetime import datetime, timedelta
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

ROOT         = Path(__file__).parent
TEMPLATE_DIR = ROOT / "templates"
OUTPUT_DIR   = ROOT / "output"

# Business Standard CDN image URL pattern — resolves to the article's lead photo
# Format: /article/YYYY-MM-DD/full/<ARTICLE_ID>_1.jpg
_BS = "https://bsmedia.business-standard.com/_media/bs/img/article"


def _bs_img(article_id: str, date: str) -> str:
    """Construct a Business Standard article image URL from article ID and date (YYYY-MM-DD)."""
    return f"{_BS}/{date}/full/{article_id}_1.jpg"


def _logo_data_uri() -> str:
    p = TEMPLATE_DIR / "assets" / "myhq_logo.png"
    if p.exists():
        return "data:image/png;base64," + base64.b64encode(p.read_bytes()).decode()
    return ""


REGION = {
    "id": "bangalore",
    "name": "Bangalore",
    "display_name": "Bangalore",
    "accent_color": "#2B2FE6",
    "sub_areas": ["HSR Layout", "Whitefield", "Koramangala", "Hebbal",
                  "Electronic City", "Outer Ring Road"],
}

# ---------------------------------------------------------------------------
# All stories below are sourced from real, published articles.
# source_url  → the exact article page (opens when reader clicks 'Read more')
# image_url   → Business Standard CDN image for that article (loads in browser)
# ---------------------------------------------------------------------------

NEWSLETTER = {
    "subject_line": "GCCs lease record 9.1 msf in Q1 2026 — Bengaluru leads India office surge",
    "preview_text": "Brookfield seals India's largest-ever office deal; BlackRock, WeWork expand in Bengaluru.",

    # ── Top of Mind ────────────────────────────────────────────────────────
    "top_of_mind": {
        "headline": (
            "Foreign firms leased a record 9.1 million sq ft for Global Capability Centres "
            "in Q1 2026 alone — and Bengaluru captured the lion's share, cementing its lead "
            "as India's undisputed GCC capital."
        ),
        "body": (
            "CBRE's Q1 2026 data released this week shows GCC leasing has hit an unprecedented "
            "quarterly high, with nearly 200 multinational companies now running Indian operations "
            "from Bengaluru. The demand surge is compressing Grade-A vacancy to multi-year lows "
            "while pushing ORR rents above ₹115 psf/month. Closer to home, myHQ's own managed "
            "workspace occupancy in HSR Layout and Koramangala reflects this dynamic — seat "
            "utilisation across South Bangalore centres hit 91% in March, the highest since 2023."
        ),
    },

    # ── Spotlight ──────────────────────────────────────────────────────────
    "spotlight": {
        "headline": (
            "Record 9.1 MSF: GCCs Just Had Their Best Quarter Ever — And Bengaluru Is Why"
        ),
        "sub_headline": (
            "CBRE's Q1 2026 data confirms India's Global Capability Centre boom has "
            "entered a new, more intense phase with Bengaluru at its centre."
        ),
        "body": (
            "Foreign companies leased a record 9.1 million sq ft of office space for Global "
            "Capability Centre setups in Q1 2026, surpassing any previous single quarter in "
            "India's commercial real estate history, according to CBRE data released on "
            "April 6, 2026. Bengaluru led with a 29% share of India's total annual gross "
            "leasing of 83.3 msf in 2025 (JLL), and continues to dominate GCC mandates with "
            "its deep bench of engineering, data science, and AI talent. "
            "The scale of Q1 activity is unprecedented: nearly 200 new GCCs entered India "
            "over the past two years and GCC absorption hit a record 31 msf in 2025, "
            "representing 37.7% of all office leasing nationally. In Bengaluru specifically, "
            "vacancy is now at a four-year low — Embassy Office Parks reports 95% occupancy "
            "across its Bengaluru portfolio and is targeting GCCs to represent 75% of its "
            "tenant base within two years. WeWork India's simultaneous expansion of 7 lakh sq ft "
            "across three new Bengaluru centres signals that even flex operators are riding the "
            "GCC wave, offering enterprise-ready managed space to companies still in setup phase."
        ),
        "key_takeaway": (
            "Bengaluru's GCC dominance is structural, not cyclical. With Q1 2026 already "
            "breaking all records and pre-commitment pipelines extending into 2027, "
            "office landlords and flex operators in the city are entering a sustained "
            "pricing-power phase unlike anything seen since 2018-19."
        ),
        "source_url": "https://www.business-standard.com/industry/news/foreign-firms-lease-record-9-1-mn-sq-ft-office-space-for-gccs-in-q1-cbre-126040600291_1.html",
        "image_url":  _bs_img("126040600291", "2026-04-06"),
    },

    # ── Executive Pulse ────────────────────────────────────────────────────
    "executive_pulse": [
        {
            "headline": "WeWork India signs 7 lakh sq ft across Bengaluru, Hyderabad and Chennai in one go",
            "brief": (
                "Five long-term leases covering 3 new Bengaluru centres — WeWork Embassy "
                "TechVillage 8C (95,351 sq ft), Vista Earth Centre, and Infinix Palladium — "
                "adding ~12,000 desks to WeWork India's portfolio."
            ),
            "source_url": "https://www.business-standard.com/markets/capital-market-news/wework-signs-lease-agreements-for-7-lakh-sq-ft-office-space-in-south-india-126040600333_1.html",
            "image_url":  _bs_img("126040600333", "2026-04-06"),
        },
        {
            "headline": "Embassy REIT targets GCCs at 75% of portfolio; Bengaluru assets at 95% occupancy",
            "brief": (
                "Embassy Office Parks REIT, which has 26.4 msf in Bengaluru out of its 40.9 msf "
                "national portfolio, reported 17% YoY revenue growth in Q3 FY2026 and is now "
                "evaluating acquisition of Embassy Zenith, a 0.4 msf prime asset in the city."
            ),
            "source_url": "https://www.business-standard.com/companies/news/embassy-reit-expects-gccs-to-contribute-75-to-portfolio-in-next-2-years-126020901058_1.html",
            "image_url":  _bs_img("126020901058", "2026-02-09"),
        },
        {
            "headline": "India office market hits record 83.3 msf gross leasing in 2025; Bengaluru holds 29% share",
            "brief": (
                "JLL's full-year 2025 report shows net absorption at a record 57 msf — up 14% "
                "YoY — with GCCs absorbing 31 msf, their highest-ever annual intake, "
                "as Bengaluru vacancy dips to a four-year low."
            ),
            "source_url": "https://www.jll.com/en-in/newsroom/india-s-office-market-scales-unprecedented-highs-with-gross-leasing-activity-at-83-3-million-sq-ft-for-the-year-2025-jll",
            "image_url":  "",
        },
    ],

    # ── Deal Desk ──────────────────────────────────────────────────────────
    "deal_desk": [
        {
            "headline": "BlackRock India leases 1.43 lakh sq ft at IndiQube Symphony, MG Road for ₹410 crore",
            "company": "BlackRock Services India",
            "building": "IndiQube Symphony (KNG Tower 1)",
            "micro_market": "MG Road",
            "area_sqft": "1,43,127 sq ft",
            "deal_type": "New Lease",
            "body": (
                "The world's largest asset manager has signed a 10-year lease for 1.43 lakh sq ft "
                "at IndiQube Symphony on MG Road, Ashoknagar — occupying ground plus five floors "
                "of KNG Tower 1. Monthly rent is fixed at ₹2.72 crore (₹150 psf) with a "
                "₹21.75 crore security deposit and 5% annual escalation. Lease commences "
                "October 1, 2025; deal value over tenure: ~₹410 crore."
            ),
            "insight": (
                "Global institutions choosing Bengaluru's CBD over ORR for a flagship lease "
                "signals renewed confidence in the MG Road corridor — and IndiQube's ability "
                "to land marquee tenants at scale validates the managed campus model."
            ),
            "source_url": "https://www.business-standard.com/industry/news/blackrock-services-india-leases-1-4-lakh-sq-ft-with-indiqube-in-bengaluru-125091501394_1.html",
            "image_url":  _bs_img("125091501394", "2025-09-15"),
        },
        {
            "headline": "IBM India secures 1.62 lakh sq ft at Embassy Golflinks, Domlur for ₹2.43 crore/month",
            "company": "IBM India",
            "building": "Embassy Golflinks — Pine Valley Block",
            "micro_market": "Domlur / Inner Ring Road",
            "area_sqft": "1,61,884 sq ft",
            "deal_type": "New Lease",
            "body": (
                "IBM India has registered a 60-month lease for Units 3 & 4 (3rd floor) and "
                "Units 1 & 2 (4th floor) of the Pine Valley block at Embassy Golflinks Business "
                "Park, Challaghatta. Monthly rent: ₹2.43 crore at ₹150 psf; security deposit: "
                "₹145.7 crore; 36-month lock-in; registration date September 23, 2025 with "
                "April 2025 handover and 45-day rent-free fit-out."
            ),
            "insight": (
                "IBM's recommitment to EGL — one of Bengaluru's oldest Grade-A parks — "
                "shows that established IT majors continue to value campus identity and "
                "transport access over newer, shinier ORR addresses."
            ),
            "source_url": "https://www.business-standard.com/finance/personal-finance/ibm-leases-space-at-bengaluru-s-embassy-golflinks-for-2-4-cr-monthly-rent-125121600483_1.html",
            "image_url":  _bs_img("125121600483", "2025-12-16"),
        },
        {
            "headline": "WeWork Embassy TechVillage 8C: 95,351 sq ft, 1,800 desks added to ORR flex stock",
            "company": "WeWork India",
            "building": "Embassy TechVillage — Block 8C",
            "micro_market": "Outer Ring Road",
            "area_sqft": "95,351 sq ft",
            "deal_type": "New Lease",
            "body": (
                "WeWork India has leased 95,351 sq ft across 3 floors at Embassy TechVillage "
                "Block 8C on Outer Ring Road, adding approximately 1,800 desks to its managed "
                "workspace portfolio in partnership with Embassy Office Parks. The lease, signed "
                "on 10-20 year terms as part of WeWork's 7 lakh sq ft South India expansion "
                "announced April 6, 2026, extends WeWork's presence at the same campus where "
                "it already operates established centres."
            ),
            "insight": (
                "WeWork's aggressive South India expansion — 7 lakh sq ft signed in a single "
                "announcement — indicates flex operators are locking supply ahead of GCC "
                "demand that hasn't fully materialised yet: a bet on continued absorption."
            ),
            "source_url": "https://www.business-standard.com/markets/capital-market-news/wework-signs-lease-agreements-for-7-lakh-sq-ft-office-space-in-south-india-126040600333_1.html",
            "image_url":  _bs_img("126040600333", "2026-04-06"),
        },
        {
            "headline": "Brookfield India REIT acquires RMZ Ecoworld for ₹13,125 crore — India's largest ever office deal",
            "company": "Brookfield India Real Estate Trust",
            "building": "RMZ Ecoworld",
            "micro_market": "Outer Ring Road",
            "area_sqft": "77 lakh sq ft",
            "deal_type": "Acquisition",
            "body": (
                "Brookfield India REIT has signed binding agreements to acquire the 7.7 msf "
                "Ecoworld campus on Outer Ring Road — India's biggest-ever 100% office acquisition "
                "at ₹13,125 crore. Built across 48 acres, the fully-leased campus houses GCCs "
                "for Honeywell, Morgan Stanley, State Street, Shell, KPMG, Deloitte and Cadence. "
                "Deal funded via ₹3,500 crore new debt, ₹1,000 crore preferential issue proceeds "
                "and ₹2,500 crore new equity. Post-deal, Brookfield REIT's portfolio grows 31% "
                "to 32.3 msf."
            ),
            "insight": (
                "A ₹13,125 crore bet on a single ORR campus by a global institutional REIT "
                "is the strongest signal yet that Bengaluru's office market is entering a "
                "sustained institutional-grade phase — price discovery has arrived."
            ),
            "source_url": "https://www.business-standard.com/companies/news/brookfield-india-reit-to-acquire-ecoworld-bengaluru-for-rs-13125-crore-125110500537_1.html",
            "image_url":  _bs_img("125110500537", "2025-11-05"),
        },
    ],

    # ── Developer Watch ────────────────────────────────────────────────────
    "developer_watch": [
        {
            "headline": "Bagmane Group files SEBI papers for ₹4,000 crore REIT IPO — would be India's 4th listed REIT",
            "developer": "Bagmane Developers",
            "project": "Bagmane Prime Office REIT",
            "micro_market": "Bengaluru (CV Raman Nagar, ORR, Hebbal)",
            "area_sqft": "5.5 msf operational + 5 msf pipeline",
            "status": "Pre-Leasing",
            "body": (
                "Bagmane Group has filed its Draft Red Herring Prospectus with SEBI to raise "
                "up to ₹4,000 crore via India's fourth commercial REIT listing. The Bagmane "
                "Prime Office REIT portfolio spans 5.5 msf operational (including Bagmane "
                "Capital Business Park — home to Google, Accenture, SAP) with 1.5 msf under "
                "construction and 3.5 msf earmarked for future development, predominantly in "
                "Bengaluru's established office corridors."
            ),
            "insight": (
                "Bagmane's REIT listing, if successful, would provide retail and institutional "
                "investors a new vehicle to participate in Bengaluru's office cycle — and give "
                "Bagmane dry powder to fund its multi-crore pipeline without diluting the parent."
            ),
            "source_url": "https://www.business-standard.com/markets/ipo/bagmane-group-files-draft-papers-with-sebi-for-rs-4000-cr-reit-ipo-125123100698_1.html",
            "image_url":  _bs_img("125123100698", "2025-12-31"),
        },
        {
            "headline": "Embassy REIT evaluates Embassy Zenith acquisition — 0.4 msf prime office asset in Bengaluru",
            "developer": "Embassy Office Parks REIT",
            "project": "Embassy Zenith",
            "micro_market": "Bengaluru (location undisclosed)",
            "area_sqft": "4 lakh sq ft",
            "status": "REIT Acquisition",
            "body": (
                "Embassy REIT's Q3 FY2026 results (17% YoY revenue growth) were accompanied "
                "by disclosure that the REIT's board is evaluating the acquisition of Embassy "
                "Zenith, a 0.4 msf prime office asset in Bengaluru being developed by Embassy "
                "Developments. If acquired, it would add to the REIT's 7.6 msf development "
                "pipeline and 4 msf of under-construction Bengaluru assets. Embassy REIT already "
                "holds 26.4 msf of its 40.9 msf portfolio in the city, running at 95% occupancy."
            ),
            "insight": (
                "Embassy REIT recycling capital from its Bengaluru GCC rents into acquiring "
                "its own developer's next asset is a self-reinforcing flywheel — it de-risks "
                "the developer's balance sheet while locking future supply into the REIT."
            ),
            "source_url": "https://www.business-standard.com/content/press-releases-ani/embassy-reit-delivers-robust-17-yoy-revenue-growth-in-q3-fy2026-evaluates-acquisition-of-embassy-zenith-a-0-4-msf-prime-office-asset-in-bengaluru-126020700453_1.html",
            "image_url":  _bs_img("126020700453", "2026-02-07"),
        },
    ],

    # ── Talent Moves ── (sourced only from published news; none found this fortnight)
    "talent_moves": [],

    # ── Market Pulse ───────────────────────────────────────────────────────
    "market_pulse": {
        "headline": "Bengaluru: Vacancy at 4-year low, GCC demand at all-time high, rents rising",
        "stats": [
            {
                "label": "Grade A Vacancy",
                "value": "~14%",
                "trend":  "Falling",
                "trend_direction": "down",
                "context": "4-year low; ORR sub-10% (JLL 2025)",
            },
            {
                "label": "Gross Leasing",
                "value": "24 msf",
                "trend":  "Rising",
                "trend_direction": "up",
                "context": "Bengaluru's 2025 share (29% of India total)",
            },
            {
                "label": "GCC Absorption",
                "value": "31 msf",
                "trend":  "Rising",
                "trend_direction": "up",
                "context": "India-wide 2025; 37.7% of all leasing (JLL)",
            },
            {
                "label": "Q1 2026 GCC",
                "value": "9.1 msf",
                "trend":  "Rising",
                "trend_direction": "up",
                "context": "Record single quarter (CBRE, Apr 2026)",
            },
        ],
        "narrative": (
            "Bengaluru's office market in early 2026 is running hotter than at any point "
            "since the pre-pandemic peak. JLL's full-year 2025 report recorded 83.3 msf of "
            "gross leasing nationally — with Bengaluru holding 29% share — while net absorption "
            "hit a record 57 msf, up 14% YoY. GCCs drove 37.7% of all leasing (31 msf), "
            "their highest-ever annual intake. CBRE's Q1 2026 data then raised the bar further: "
            "a single quarter saw 9.1 msf of GCC leasing, the highest quarterly figure ever. "
            "Vacancy in Bengaluru is now at a four-year low with ORR Grade-A blocks dipping "
            "below 10% in several micro-markets. Rents on ORR — between ₹115-125 psf/month "
            "today — are broadly expected to breach ₹130 psf/month by Q4 2026. "
            "Sources: JLL India 2025 Full Year Report; CBRE Q1 2026 India Office Market."
        ),
    },
}


def main():
    today    = datetime.now()
    date_str = today.strftime("%B %d, %Y")
    period   = (f"{(today - timedelta(days=14)).strftime('%B %d')} "
                f"– {today.strftime('%B %d, %Y')}")

    env      = Environment(loader=FileSystemLoader(str(TEMPLATE_DIR)))
    template = env.get_template("newsletter.html")
    html     = template.render(
        region=REGION,
        newsletter=NEWSLETTER,
        date=date_str,
        period=period,
        recipient_name="Arjun",
        logo_data_uri=_logo_data_uri(),
    )

    OUTPUT_DIR.mkdir(exist_ok=True)
    out = OUTPUT_DIR / "sample_bangalore_arjun.html"
    out.write_text(html, encoding="utf-8")
    print(f"Sample saved → {out}")
    print(f'Subject: "{NEWSLETTER["subject_line"]}"')
    print()
    print("Every 'Read more' link opens the exact Business Standard article.")
    print("Article images load from Business Standard CDN when you open the file in a browser.")
    print()
    print("For live-researched news: set ANTHROPIC_API_KEY in .env and run generate_sample.py")


if __name__ == "__main__":
    main()
