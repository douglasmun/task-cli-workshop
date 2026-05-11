# Lab B Skeleton — multi-agent CTI pipeline

import json
from typing import TypedDict


class IOC(TypedDict):
    type: str        # e.g. "ip", "domain", "hash"
    value: str       # the raw indicator value
    confidence: str  # "HIGH", "MODERATE", or "LOW"
    tags: list[str]  # e.g. ["c2", "ransomware"]


def collector(raw_data: list[dict]) -> list[dict]:
    """Validate and normalize raw IOC dicts.

    Accepts a list of arbitrary dicts (e.g. loaded from JSON) and returns
    only the dicts that contain the required keys: type, value, confidence,
    tags. Drop or skip any entry missing a required field.

    Returns a list of normalized dicts ready for the extractor.
    """
    # TODO: filter raw_data to only include dicts with all required keys
    # TODO: normalise confidence to uppercase (e.g. "high" -> "HIGH")
    pass


def extractor(iocs: list[dict]) -> list[IOC]:
    """Convert dicts to typed IOC objects.

    Takes the output of collector() and casts each dict to an IOC TypedDict.
    Returns a list of IOC objects.
    """
    # TODO: cast each dict to an IOC TypedDict and return the list
    pass


def reporter(iocs: list[IOC]) -> str:
    """Return a 5-line plain-text summary of the IOC set.

    The summary must include:
      Line 1: total IOC count
      Line 2: breakdown by type (e.g. "ip: 1, domain: 1")
      Line 3: breakdown by confidence level
      Line 4: all unique tags seen across all IOCs
      Line 5: highest-confidence indicator (value only)

    Returns a single string with newline-separated lines.
    """
    # TODO: compute the stats and format them into exactly 5 lines
    pass


def run_pipeline(raw_data: list[dict]) -> str:
    collected = collector(raw_data)
    extracted = extractor(collected)
    # TODO: add a mapper stage here (stretch goal)
    # mapper should accept list[IOC] and return list[IOC] with severity added
    return reporter(extracted)


def main():
    with open("labs/lab-b-samples/mock-threat-intel.json") as f:
        raw = json.load(f)
    result = run_pipeline(raw)
    print(result)


if __name__ == "__main__":
    main()


# Expected output (based on mock-threat-intel.json with 2 IOCs):
# Total IOCs: 2
# By type: ip: 1, domain: 1
# By confidence: HIGH: 1, MODERATE: 1
# Tags: c2, ransomware, phishing, ta-phantom
# Highest confidence: 198.51.100.42
