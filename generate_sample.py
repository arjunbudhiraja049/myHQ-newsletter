"""
Generate a sample newsletter for Arjun Budhiraja — Bangalore / HSR Layout.

Runs the full research → vet → write → image-fetch → render pipeline
so every piece of news is real, sourced, and linked.

Usage:
    python generate_sample.py

Requires: ANTHROPIC_API_KEY in .env or environment.
Output:   output/bangalore_office_pulse_<date>.html
"""

import os
import sys
from pathlib import Path

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT))

from dotenv import load_dotenv
load_dotenv()

if not os.getenv("ANTHROPIC_API_KEY"):
    print("ERROR: ANTHROPIC_API_KEY not set.")
    print("  Copy .env.example → .env and add your API key, then re-run.")
    sys.exit(1)

from main import generate_for_region, load_config, get_region


def main():
    regions, voice = load_config()
    region = get_region("bangalore", regions)
    generate_for_region(region, voice, recipient_name="Arjun")


if __name__ == "__main__":
    main()
