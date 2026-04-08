"""
myHQ Office Pulse — Newsletter Generator
=========================================
Orchestrates the full pipeline:
  1. Research  — Claude Opus 4.6 + web_search/web_fetch (server-side tools)
  2. Vet       — Claude Haiku 4.5 quality-scores every raw news item
  3. Write     — Claude Opus 4.6 + adaptive thinking writes the newsletter
  4. Render    — Jinja2 populates the HTML template

Usage:
  python main.py --region bangalore
  python main.py --region delhi_ncr
  python main.py --region chennai_hyderabad
  python main.py --region mumbai_pune
  python main.py --all
  python main.py --region bangalore --recipient "Arjun"

Output: HTML file(s) saved to ./output/
"""

import argparse
import base64
import json
import os
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime, timedelta
from pathlib import Path

from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader

from src.researcher import research_region
from src.vetter import vet_research
from src.writer import write_newsletter

load_dotenv()

# ── Paths ───────────────────────────────────────────────────────────────────
ROOT = Path(__file__).parent
CONFIG_DIR = ROOT / "config"
TEMPLATE_DIR = ROOT / "templates"
OUTPUT_DIR = ROOT / "output"


def load_config() -> tuple[list[dict], dict]:
    with open(CONFIG_DIR / "regions.json") as f:
        regions_cfg = json.load(f)["regions"]
    with open(CONFIG_DIR / "voice.json") as f:
        voice_cfg = json.load(f)
    return regions_cfg, voice_cfg


def get_region(region_id: str, regions: list[dict]) -> dict:
    for r in regions:
        if r["id"] == region_id:
            return r
    valid = [r["id"] for r in regions]
    print(f"ERROR: Unknown region '{region_id}'. Valid options: {valid}")
    sys.exit(1)


_UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
)


def _fetch_og_image(url: str) -> str:
    """
    Fetch og:image from a news article URL and return a base64 data URI.
    Returns empty string on any failure (timeout, no tag, bad image, etc.).
    """
    if not url or not url.startswith("http"):
        return ""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": _UA})
        with urllib.request.urlopen(req, timeout=7) as resp:
            html = resp.read(80000).decode("utf-8", errors="ignore")
    except Exception:
        return ""

    # Match og:image in either attribute order
    match = re.search(
        r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']+)["\']',
        html, re.IGNORECASE,
    ) or re.search(
        r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+property=["\']og:image["\']',
        html, re.IGNORECASE,
    )
    if not match:
        return ""

    img_url = match.group(1).strip()
    if not img_url.startswith("http"):
        return ""

    try:
        img_req = urllib.request.Request(img_url, headers={"User-Agent": _UA})
        with urllib.request.urlopen(img_req, timeout=7) as img_resp:
            img_bytes = img_resp.read(3 * 1024 * 1024)  # cap at 3 MB
            ct = img_resp.headers.get("Content-Type", "image/jpeg").split(";")[0].strip()
        if ct not in ("image/jpeg", "image/png", "image/gif", "image/webp"):
            ct = "image/jpeg"
        return f"data:{ct};base64,{base64.b64encode(img_bytes).decode()}"
    except Exception:
        return ""


def _enrich_with_images(newsletter: dict) -> dict:
    """
    Walk every section that has a source_url, fetch the og:image,
    and attach it as image_data_uri on the item.
    Sections with no URL or a failed fetch silently get no field (template falls back to gradient).
    """
    # Spotlight (single dict)
    spotlight = newsletter.get("spotlight") or {}
    if spotlight.get("source_url"):
        print(f"    [img] spotlight: {spotlight['source_url'][:70]}")
        spotlight["image_data_uri"] = _fetch_og_image(spotlight["source_url"])

    # List sections
    for section in ("deal_desk", "developer_watch", "talent_moves", "executive_pulse"):
        for item in newsletter.get(section) or []:
            url = item.get("source_url", "")
            if url:
                print(f"    [img] {section}: {url[:70]}")
                item["image_data_uri"] = _fetch_og_image(url)

    return newsletter


def _logo_data_uri() -> str:
    logo_path = TEMPLATE_DIR / "assets" / "myhq_logo.png"
    if logo_path.exists():
        data = base64.b64encode(logo_path.read_bytes()).decode()
        return f"data:image/png;base64,{data}"
    return ""


def render_html(region: dict, newsletter: dict, date_str: str, period: str,
                recipient_name: str = "Reader") -> str:
    env = Environment(loader=FileSystemLoader(str(TEMPLATE_DIR)))
    template = env.get_template("newsletter.html")
    return template.render(
        region=region,
        newsletter=newsletter,
        date=date_str,
        period=period,
        recipient_name=recipient_name,
        logo_data_uri=_logo_data_uri(),
    )


def save_output(html: str, region_id: str, date_str: str) -> Path:
    OUTPUT_DIR.mkdir(exist_ok=True)
    # Sanitise date string for filename
    safe_date = date_str.replace(" ", "_").replace(",", "")
    filename = f"{region_id}_office_pulse_{safe_date}.html"
    out_path = OUTPUT_DIR / filename
    out_path.write_text(html, encoding="utf-8")
    return out_path


def generate_for_region(region: dict, voice: dict, recipient_name: str = "Reader") -> None:
    region_name = region["name"]
    today = datetime.now()
    date_str = today.strftime("%B %d, %Y")
    period = f"{(today - timedelta(days=14)).strftime('%B %d')} – {today.strftime('%B %d, %Y')}"

    print(f"\n{'='*60}")
    print(f"  myHQ Office Pulse  ·  {region_name}")
    print(f"  Coverage: {period}")
    print(f"{'='*60}")

    # ── Step 1: Research ───────────────────────────────────────────────────
    print("\n[1/3] RESEARCH — gathering news via Claude + web search...")
    raw_research = research_region(region)
    total_raw = sum(len(v) for v in raw_research.values())
    print(f"  Total raw items found: {total_raw}")

    if total_raw == 0:
        print("  WARNING: No raw items found. Newsletter will be sparse.")

    # ── Step 2: Vet ────────────────────────────────────────────────────────
    print("\n[2/3] VETTING — scoring & filtering news items...")
    vetted = vet_research(raw_research, region)
    total_vetted = sum(len(v) for v in vetted.values())
    print(f"  Items passing quality threshold: {total_vetted}/{total_raw}")

    # ── Step 3: Write ──────────────────────────────────────────────────────
    print("\n[3/3] WRITING — Claude composing the newsletter...")
    newsletter = write_newsletter(region, vetted, voice)

    if not newsletter:
        print("  ERROR: Writer returned empty content. Aborting.")
        return

    # ── Step 3.5: Fetch article images ────────────────────────────────────
    print("\n[3.5/4] IMAGES — fetching article thumbnails from source URLs...")
    newsletter = _enrich_with_images(newsletter)

    # ── Step 4: Render & Save ──────────────────────────────────────────────
    print("\n[4/4] RENDERING — building HTML...")
    html = render_html(region, newsletter, date_str, period, recipient_name)
    out_path = save_output(html, region["id"], date_str)

    print(f"\n  ✓ Newsletter saved → {out_path.relative_to(ROOT)}")
    print(f"  Subject line: \"{newsletter.get('subject_line', 'N/A')}\"")


def main():
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("ERROR: ANTHROPIC_API_KEY not set.")
        print("  Copy .env.example → .env and add your key, or set the env var directly.")
        sys.exit(1)

    parser = argparse.ArgumentParser(
        description="myHQ Office Pulse — AI newsletter generator"
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--region",
        choices=["bangalore", "delhi_ncr", "chennai_hyderabad", "mumbai_pune"],
        help="Generate newsletter for a specific region",
    )
    group.add_argument(
        "--all",
        action="store_true",
        help="Generate newsletters for all 4 regions",
    )
    parser.add_argument(
        "--recipient",
        default="Reader",
        help="Recipient first name for the greeting (default: Reader)",
    )
    args = parser.parse_args()

    regions, voice = load_config()

    if args.all:
        for region in regions:
            generate_for_region(region, voice, args.recipient)
    else:
        region = get_region(args.region, regions)
        generate_for_region(region, voice, args.recipient)

    print("\nDone.\n")


if __name__ == "__main__":
    main()
