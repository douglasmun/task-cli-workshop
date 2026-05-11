"""
Lab B — Multi-Agent CTI Pipeline

Goal: build a three-stage pipeline that reads raw threat intelligence from
lab-b-samples/mock-threat-intel.json, normalises it, and produces a structured
summary report. Each stage maps to one agent role from the course:

    Collector  →  Perceive  (validate + normalise raw input)
    Extractor  →  Reason    (cast to typed objects, derive metadata)
    Reporter   →  Act       (produce the human-readable output)

Run from the repo root:
    python labs/lab-b-skeleton/pipeline_skeleton.py

Expected output (based on the 10-IOC sample dataset):
    === CTI Pipeline Report ===
    Total IOCs: 10
    By type: ip: 3, domain: 4, hash: 2, url: 1
    By confidence: HIGH: 5, MODERATE: 3, LOW: 2
    Tags seen: c2, ransomware, ironlock, healthcare-targeting, supply-chain,
               exfil, npm-compromise, ta-phantom, phishing, apt-sg41,
               jade-cicada, silkthread, financial-sector, dropper,
               suspected-loader, unconfirmed, suspected-proxy,
               residential-proxy, credential-stuffing
    Highest-confidence indicator: 198.51.100.42
"""

from __future__ import annotations

import json
from collections import Counter
from typing import TypedDict


# ---------------------------------------------------------------------------
# Types
# ---------------------------------------------------------------------------

class IOC(TypedDict):
    type: str        # "ip" | "domain" | "hash" | "url"
    value: str       # the raw indicator string
    confidence: str  # "HIGH" | "MODERATE" | "LOW"
    tags: list[str]  # free-form labels, e.g. ["c2", "ransomware"]


class EnrichedIOC(TypedDict):
    type: str
    value: str
    confidence: str
    tags: list[str]
    severity: int    # derived: HIGH=3, MODERATE=2, LOW=1


REQUIRED_KEYS: frozenset[str] = frozenset({"type", "value", "confidence", "tags"})
CONFIDENCE_RANK: dict[str, int] = {"HIGH": 3, "MODERATE": 2, "LOW": 1}


# ---------------------------------------------------------------------------
# Stage 1 — Collector: validate and normalise raw input
# ---------------------------------------------------------------------------

def collector(raw_data: list[dict]) -> list[dict]:
    """Validate and normalise raw IOC dicts from an untrusted data source.

    Accepts a list of arbitrary dicts (e.g. parsed from JSON) and returns
    only the entries that have all required keys. Partial or malformed entries
    are silently dropped — in production you would log them.

    Normalisation rules:
      - confidence is uppercased ("high" → "HIGH")
      - tags is guaranteed to be a list (if the source sends a string, wrap it)
      - type is lowercased ("IP" → "ip")

    Args:
        raw_data: A list of dicts from an untrusted source.

    Returns:
        A list of dicts that all satisfy REQUIRED_KEYS, with fields normalised.
        Ordering matches the input (minus dropped entries).

    Example:
        >>> good = {"type": "ip", "value": "1.2.3.4", "confidence": "high", "tags": ["c2"]}
        >>> bad  = {"type": "ip", "value": "1.2.3.4"}  # missing confidence and tags
        >>> result = collector([good, bad])
        >>> len(result)
        1
        >>> result[0]["confidence"]
        'HIGH'

    Implementation hint:
        Iterate raw_data. For each entry, check REQUIRED_KEYS.issubset(entry).
        If it passes, normalise the three fields listed above and append to output.
    """
    # TODO: filter raw_data — keep only entries where all REQUIRED_KEYS are present
    # TODO: normalise confidence to uppercase
    # TODO: normalise type to lowercase
    # TODO: ensure tags is a list (if str, wrap in [])
    # TODO: return the cleaned list
    raise NotImplementedError


# ---------------------------------------------------------------------------
# Stage 2 — Extractor: cast to typed objects
# ---------------------------------------------------------------------------

def extractor(iocs: list[dict]) -> list[IOC]:
    """Cast normalised dicts to IOC TypedDicts.

    At this stage all entries have already been validated by collector().
    The extractor's job is to ensure the Python type system can rely on
    the shape of each record downstream.

    Args:
        iocs: Output of collector().

    Returns:
        A list of IOC TypedDicts in the same order as the input.

    Example:
        >>> raw = [{"type": "ip", "value": "1.2.3.4", "confidence": "HIGH", "tags": ["c2"]}]
        >>> typed = extractor(raw)
        >>> typed[0]["type"]
        'ip'
        >>> isinstance(typed[0]["tags"], list)
        True

    Implementation hint:
        TypedDict construction is just a dict cast: IOC(**entry) or
        IOC(type=..., value=..., confidence=..., tags=...).
        Python does not enforce TypedDict at runtime, so this is mainly
        for static analysis and documentation purposes.
    """
    # TODO: for each dict in iocs, construct and append an IOC TypedDict
    # TODO: return the list
    raise NotImplementedError


# ---------------------------------------------------------------------------
# Stage 3 — Mapper: enrich with derived fields (stretch goal)
# ---------------------------------------------------------------------------

def mapper(iocs: list[IOC]) -> list[EnrichedIOC]:
    """Enrich each IOC with a numeric severity score derived from confidence.

    This is the stretch-goal stage. The mapper transforms typed IOC records
    into EnrichedIOC records by adding a severity integer field.

    Severity mapping:
        HIGH     → 3
        MODERATE → 2
        LOW      → 1
        unknown  → 0

    Args:
        iocs: Output of extractor().

    Returns:
        A list of EnrichedIOC TypedDicts, same length and order as input.

    Example:
        >>> ioc = IOC(type="ip", value="1.2.3.4", confidence="HIGH", tags=[])
        >>> enriched = mapper([ioc])
        >>> enriched[0]["severity"]
        3

    Implementation hint:
        Use CONFIDENCE_RANK.get(ioc["confidence"], 0) for the lookup.
        Construct each EnrichedIOC by spreading the existing IOC fields
        and adding the severity key.
    """
    # TODO: for each IOC, look up severity from CONFIDENCE_RANK
    # TODO: construct an EnrichedIOC with all IOC fields plus severity
    # TODO: return the list
    raise NotImplementedError


# ---------------------------------------------------------------------------
# Stage 4 — Reporter: produce the human-readable summary
# ---------------------------------------------------------------------------

def reporter(iocs: list[IOC]) -> str:
    """Produce a structured plain-text summary of the IOC dataset.

    Args:
        iocs: Output of extractor() (or mapper() if you completed the stretch goal).

    Returns:
        A multi-line string. The exact format must match the lines below so
        that the pipeline's output is deterministic and testable:

        Line 1:  "Total IOCs: <n>"
        Line 2:  "By type: ip: <n>, domain: <n>, ..."  (sorted alphabetically by type)
        Line 3:  "By confidence: HIGH: <n>, MODERATE: <n>, LOW: <n>"
        Line 4:  "Tags seen: <tag1>, <tag2>, ..."       (sorted alphabetically)
        Line 5:  "Highest-confidence indicator: <value>" (first HIGH, else first MODERATE)

    Example (based on the two-IOC mini-dataset):
        >>> mini = [
        ...     IOC(type="ip",     value="1.2.3.4",       confidence="HIGH",     tags=["c2"]),
        ...     IOC(type="domain", value="evil.example",  confidence="MODERATE", tags=["phishing"]),
        ... ]
        >>> print(reporter(mini))
        Total IOCs: 2
        By type: domain: 1, ip: 1
        By confidence: HIGH: 1, MODERATE: 1, LOW: 0
        Tags seen: c2, phishing
        Highest-confidence indicator: 1.2.3.4

    Implementation hint:
        Use collections.Counter for type and confidence tallies.
        For tags, flatten all tag lists with itertools.chain or a list comprehension,
        then deduplicate with sorted(set(...)).
        For highest-confidence, filter by "HIGH" first, fall back to "MODERATE".
    """
    # TODO: count IOCs by type using Counter
    # TODO: count IOCs by confidence level
    # TODO: collect all unique tags across all IOCs
    # TODO: find the highest-confidence indicator value
    # TODO: format and return the five-line string
    raise NotImplementedError


# ---------------------------------------------------------------------------
# Pipeline runner
# ---------------------------------------------------------------------------

def run_pipeline(raw_data: list[dict]) -> str:
    """Run the full collector → extractor → (mapper) → reporter pipeline.

    Args:
        raw_data: Raw list of dicts, typically loaded from JSON.

    Returns:
        The reporter's output string.
    """
    collected = collector(raw_data)
    extracted = extractor(collected)
    # Uncomment after completing the mapper stretch goal:
    # enriched = mapper(extracted)
    # return reporter(enriched)
    return reporter(extracted)


def main() -> None:
    data_path = "labs/lab-b-samples/mock-threat-intel.json"
    with open(data_path, encoding="utf-8") as f:
        raw = json.load(f)

    print(f"Loaded {len(raw)} raw records from {data_path}\n")
    result = run_pipeline(raw)
    print("=== CTI Pipeline Report ===")
    print(result)


if __name__ == "__main__":
    main()
