"""
Generate a sample newsletter for Arjun Budhiraja — Bangalore / HSR Layout.
Uses hardcoded realistic data so no API key is required.

Usage:
  python generate_sample.py
"""

import base64
import json
from datetime import datetime, timedelta
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

ROOT = Path(__file__).parent
TEMPLATE_DIR = ROOT / "templates"
OUTPUT_DIR = ROOT / "output"


def _logo_data_uri() -> str:
    logo_path = TEMPLATE_DIR / "assets" / "myhq_logo.png"
    if logo_path.exists():
        data = base64.b64encode(logo_path.read_bytes()).decode()
        return f"data:image/png;base64,{data}"
    return ""


REGION = {
    "id": "bangalore",
    "name": "Bangalore",
    "display_name": "Bangalore",
    "accent_color": "#2B2FE6",
    "sub_areas": ["HSR Layout", "Whitefield", "Koramangala", "Hebbal", "Electronic City", "Outer Ring Road"],
}

NEWSLETTER = {
    "subject_line": "Bangalore absorbs 4.1 msf in Q1 — HSR Layout leads boutique deals",
    "preview_text": "Whitefield vacancy tightens, two GCC mandates close, and a key CBRE exec moves.",
    "top_of_mind": {
        "headline": "Bangalore's office market posts its strongest Q1 net absorption since 2019 at 4.1 msf, driven by GCC expansions and a return of mid-size flex demand.",
        "body": (
            "Tech and BFSI occupiers led the charge this fortnight, with three lease closures above 1 lakh sq ft. "
            "The Outer Ring Road micro-market continues to attract large-format leases, while HSR Layout is quietly "
            "emerging as the go-to corridor for sub-30,000 sq ft boutique office deals — a trend myHQ is seeing "
            "first-hand across its managed workspace portfolio. Developers are responding: new supply this quarter "
            "is up 18% QoQ, yet vacancy has compressed to 14.2%, the lowest since mid-2022."
        ),
    },
    "spotlight": {
        "headline": "HSR Layout's Boutique Office Boom: Why Sub-30K Sq Ft Deals Are Driving Bangalore's Next Leasing Cycle",
        "sub_headline": "A new breed of mid-market tenant is bypassing Whitefield for the flexibility and talent density of South Bangalore.",
        "body": (
            "For the past 18 months, most of Bangalore's leasing headlines have been written in Whitefield and Hebbal — "
            "large GCC mandates, 2-5 lakh sq ft blocks, multi-year leases. But a quieter story is playing out in HSR "
            "Layout, Koramangala, and Sarjapur Road: a surge in sub-30,000 sq ft deals from Series B-D startups, "
            "Indian IT services firms right-sizing after work-from-home sprawl, and new-age BFSI companies that need "
            "campus-lite offices near talent pools. "
            "Data from JLL and Anarock shows HSR Layout recorded 47 transactions below 20,000 sq ft in Q1 2026 — up "
            "64% year-on-year. Average deal size in the micro-market: 11,400 sq ft. That's a profile that suits "
            "managed workspace operators and boutique Grade-A buildings far better than it does the large IT parks. "
            "myHQ's own occupancy data across HSR and Koramangala centres corroborates the trend: seat utilisation "
            "in dedicated cabin clusters hit 91% in March, the highest since January 2023. Landlords who held out "
            "for large tenants in 2023-24 are now reconsidering floor-plate flexibility."
        ),
        "key_takeaway": (
            "HSR Layout is no longer just an overflow market — it's the primary address for Bangalore's mid-market "
            "office demand. Brokers and landlords ignoring sub-30K sq ft mandates here are leaving money on the table."
        ),
        "source_url": "https://www.jll.co.in/en/trends-and-insights/research/india-office-market-overview",
    },
    "executive_pulse": [
        {
            "headline": "Bengaluru overtakes Hyderabad in Q1 GCC leasing count for first time since 2021",
            "brief": "54 GCC transactions closed in Bangalore vs 41 in Hyderabad — talent depth and metro connectivity cited as key differentiators.",
        },
        {
            "headline": "Outer Ring Road vacancy dips below 10% as Prestige and Embassy hold back new completions",
            "brief": "With ORR vacancy at 9.8%, rents are nudging ₹115-120 psf/month — a 6% uplift from December 2025 levels.",
        },
        {
            "headline": "Karnataka govt fast-tracks IT corridor extension to Attibele — 3 msf of new supply expected by 2028",
            "brief": "The move is aimed at decongesting Whitefield and Electronic City; site allocation notifications expected by June.",
        },
    ],
    "deal_desk": [
        {
            "headline": "Walmart Global Tech inks 2.2 lakh sq ft pre-commitment at Embassy TechVillage Phase 4",
            "company": "Walmart Global Tech",
            "building": "Embassy TechVillage Phase 4",
            "micro_market": "Outer Ring Road",
            "area_sqft": "2,20,000 sq ft",
            "deal_type": "Pre-Commitment",
            "body": (
                "Walmart Global Tech has signed a pre-commitment for 2.2 lakh sq ft at Embassy TechVillage's upcoming "
                "Phase 4 tower on ORR, with fit-out slated to begin Q3 2026. The deal consolidates two existing Walmart "
                "offices in Bellandur into a single campus. CBRE acted for the occupier; Embassy handled in-house."
            ),
            "insight": "Pre-commitments at this scale signal that large tech GCCs are locking supply 18-24 months ahead — a landlord-friendly dynamic that will keep ORR rents elevated through 2027.",
            "source_url": "https://economictimes.indiatimes.com/industry/services/property-/-cstruction/walmart-global-tech-leases-office-space-bangalore/articleshow/sample.cms",
        },
        {
            "headline": "PhonePe expands footprint with 85,000 sq ft new lease at Salarpuria Sattva Knowledge City",
            "company": "PhonePe",
            "building": "Salarpuria Sattva Knowledge City",
            "micro_market": "Whitefield",
            "area_sqft": "85,000 sq ft",
            "deal_type": "Expansion",
            "body": (
                "PhonePe has taken an additional 85,000 sq ft floor at Salarpuria Sattva Knowledge City to house its "
                "growing payments infrastructure and risk engineering teams. The fintech now occupies approximately "
                "2.1 lakh sq ft across the complex. Lease tenure is 5 years with a 15% escalation clause at year 3."
            ),
            "insight": "Fintech's office footprint in Bangalore continues to punch above its sector weight — PhonePe's expansion is the third BFSI-adjacent deal in Whitefield this fortnight.",
            "source_url": "https://www.livemint.com/companies/phonepe-office-space-bangalore-whitefield/sample",
        },
        {
            "headline": "Meesho signs 55,000 sq ft lease in Koramangala's RMZ Ecospace annex",
            "company": "Meesho",
            "building": "RMZ Ecospace Annex",
            "micro_market": "Koramangala",
            "area_sqft": "55,000 sq ft",
            "deal_type": "New Lease",
            "body": (
                "Social commerce platform Meesho has leased a full floor at RMZ Ecospace's recently completed annex "
                "block in Koramangala. The company is consolidating product and design teams from a co-working setup "
                "into a branded office. Deal structured as a 3-year lease with two 1-year renewal options."
            ),
            "insight": "Meesho's shift from flex to owned-feel office reflects a broader D2C/e-commerce trend: hypergrowth-phase companies graduating into mid-size leases as they mature.",
            "source_url": "",
        },
        {
            "headline": "myHQ HSR Layout centre reaches 100% occupancy; waitlist opens for first time",
            "company": "myHQ",
            "building": "myHQ HSR Layout",
            "micro_market": "HSR Layout",
            "area_sqft": "12,000 sq ft",
            "deal_type": "Seat Deal",
            "body": (
                "myHQ's HSR Layout managed workspace — a 12,000 sq ft centre near Agara Lake — hit full occupancy "
                "for the first time in March 2026, with a waitlist of 34 teams across 8 companies now active. "
                "The centre houses 18 dedicated offices ranging from 4-seat cabins to 40-seat suites."
            ),
            "insight": "Full occupancy with an active waitlist is a leading indicator: a second myHQ HSR centre or an adjacent micro-market expansion (Sarjapur, BTM) looks increasingly justified.",
            "source_url": "",
        },
    ],
    "developer_watch": [
        {
            "headline": "Prestige Group launches 'Prestige Technocrat' — 1.8 msf Grade-A campus in Hebbal",
            "developer": "Prestige Group",
            "project": "Prestige Technocrat",
            "micro_market": "Hebbal",
            "area_sqft": "18 lakh sq ft",
            "status": "Announced",
            "body": (
                "Prestige Group has officially announced Prestige Technocrat, a 1.8 msf mixed-use office campus in "
                "Hebbal adjacent to its existing Prestige Tech Park North. The project comprises three towers with "
                "floor plates of 40,000-60,000 sq ft, targeting GCC and BFSI tenants. Completion expected H2 2028. "
                "Pre-leasing conversations are reportedly underway with two US-headquartered GCCs."
            ),
            "insight": "Prestige doubling down on Hebbal — already home to Manyata Tech Park — will intensify competition for north Bangalore GCC mandates and may create a true multi-landlord corridor to rival ORR.",
            "source_url": "https://www.businessline.com/companies/prestige-group-hebbal-office-campus/sample",
        },
        {
            "headline": "Bagmane Developers breaks ground on World Trade Centre Bengaluru Tower 3 in CV Raman Nagar",
            "developer": "Bagmane Developers",
            "project": "World Trade Centre Bengaluru — Tower 3",
            "micro_market": "CV Raman Nagar",
            "area_sqft": "9 lakh sq ft",
            "status": "Under Construction",
            "body": (
                "Bagmane has commenced construction on the third tower of its World Trade Centre Bengaluru complex, "
                "adding 9 lakh sq ft of Grade-A space to a campus that already houses Accenture, Capgemini, and SAP. "
                "Tower 3 is designed to LEED Platinum standards with 50,000 sq ft floor plates. Delivery expected Q4 2027."
            ),
            "insight": "Tower 3 will test whether CV Raman Nagar can absorb another large block outside of ORR — Bagmane's track record of deep tenant relationships reduces lease-up risk significantly.",
            "source_url": "",
        },
    ],
    "talent_moves": [
        {
            "person": "Rahul Arora",
            "previous_role": "Managing Director — Occupier Services, CBRE South Asia",
            "new_role": "Chief Business Officer, Smartworks Co-working",
            "brief": (
                "Rahul Arora, who built CBRE's occupier advisory practice across South Asia over 11 years, has joined "
                "Smartworks as CBO to lead enterprise sales, market expansion, and product-market fit for managed "
                "campuses. He takes charge with immediate effect and will be based in Bangalore."
            ),
            "why_it_matters": "Senior talent moving from transactional brokerage to flex operators signals growing conviction in the managed workspace model at the enterprise level.",
            "source_url": "https://www.linkedin.com/in/rahularora-cre/",
        },
        {
            "person": "Deepa Nair",
            "previous_role": "Head of Real Estate, India — Flipkart",
            "new_role": "VP Real Estate & Workplace, Zepto",
            "brief": (
                "Deepa Nair, who oversaw Flipkart's 3.5 msf office and fulfilment-centre portfolio for 5 years, "
                "has joined Zepto as VP Real Estate & Workplace to lead the quick-commerce company's rapid dark store "
                "and HQ expansion. She joins a team that has added 12 lakh sq ft of space in 14 months."
            ),
            "why_it_matters": "Zepto's aggressive real estate hiring signals that Q-commerce is entering a phase where operational excellence in space — not just speed — will differentiate winners.",
            "source_url": "",
        },
    ],
    "market_pulse": {
        "headline": "Bangalore Q1 2026: Absorption outpaces supply for third consecutive quarter",
        "stats": [
            {
                "label": "Grade A Vacancy",
                "value": "14.2%",
                "trend": "Falling",
                "trend_direction": "down",
                "context": "vs 16.1% in Q4 2025",
            },
            {
                "label": "Avg Rent (psf/mo)",
                "value": "₹108",
                "trend": "Rising",
                "trend_direction": "up",
                "context": "+5.8% YoY citywide",
            },
            {
                "label": "Net Absorption",
                "value": "4.1 msf",
                "trend": "Rising",
                "trend_direction": "up",
                "context": "Best Q1 since 2019",
            },
            {
                "label": "New Supply",
                "value": "3.3 msf",
                "trend": "Rising",
                "trend_direction": "up",
                "context": "+18% QoQ completions",
            },
        ],
        "narrative": (
            "Bangalore's office market is in a supply-demand sweet spot: absorption continues to outpace new completions "
            "for the third consecutive quarter, compressing Grade-A vacancy from 16.1% to 14.2% in just 90 days. "
            "The ₹108 psf/month average rent masks wide micro-market divergence — ORR and Whitefield command ₹115-125, "
            "while HSR Layout and Sarjapur Road remain accessible at ₹80-95, attracting a different but growing tenant "
            "profile. With 3.3 msf of new supply completing in Q1 being absorbed in near real-time, landlords across "
            "Bangalore have regained pricing power they lost in 2022-23. Watch for a re-rating of secondary corridors "
            "as ORR rents push toward ₹130 psf/month through the year."
        ),
    },
}


def main():
    today = datetime.now()
    date_str = today.strftime("%B %d, %Y")
    period = f"{(today - timedelta(days=14)).strftime('%B %d')} – {today.strftime('%B %d, %Y')}"

    env = Environment(loader=FileSystemLoader(str(TEMPLATE_DIR)))
    template = env.get_template("newsletter.html")

    html = template.render(
        region=REGION,
        newsletter=NEWSLETTER,
        date=date_str,
        period=period,
        recipient_name="Arjun",
        logo_data_uri=_logo_data_uri(),
    )

    OUTPUT_DIR.mkdir(exist_ok=True)
    out_path = OUTPUT_DIR / "sample_bangalore_arjun.html"
    out_path.write_text(html, encoding="utf-8")
    print(f"Sample newsletter saved → {out_path}")
    print(f'Subject: "{NEWSLETTER["subject_line"]}"')


if __name__ == "__main__":
    main()
