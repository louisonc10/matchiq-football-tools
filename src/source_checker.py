from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
import argparse
import json


VERSION = "0.1.1"

DEFAULT_SOURCE = "Fabrizio Romano"
DEFAULT_STATUS = "here we go"

SOURCE_WEIGHT = 0.65
STATUS_WEIGHT = 0.35


STATUS_SCORES = {
    "official": 100,
    "here we go": 90,
    "confirmed": 85,
    "reported": 70,
    "rumour": 40,
    "unknown": 25,
}


STATUS_ALIASES = {
    "herewego": "here we go",
    "here-we-go": "here we go",
    "rumor": "rumour",
}


@dataclass
class CheckResult:
    source: str
    source_tier: str
    source_score: int
    status: str
    status_score: int
    confidence: int
    verdict: str
    recommendation: str


def get_project_root() -> Path:
    if "__file__" in globals():
        return Path(__file__).resolve().parents[1]

    return Path.cwd()


@lru_cache(maxsize=1)
def load_source_scores() -> dict:
    config_path = (
        get_project_root()
        / "config"
        / "sources.json"
    )

    if not config_path.exists():
        raise FileNotFoundError(
            f"Source config not found: {config_path}"
        )

    with config_path.open(
        "r",
        encoding="utf-8",
    ) as file:
        data = json.load(file)

    if not isinstance(data, dict):
        raise ValueError(
            "sources.json must contain a JSON object."
        )

    return data


def normalize_status(status: str) -> str:
    normalized = " ".join(
        status.strip().lower().split()
    )

    normalized = STATUS_ALIASES.get(
        normalized,
        normalized,
    )

    if normalized not in STATUS_SCORES:
        valid = ", ".join(STATUS_SCORES)

        raise ValueError(
            f"Unknown status '{status}'. "
            f"Valid statuses: {valid}"
        )

    return normalized


def get_source_score(
    source: str,
) -> tuple[int, str]:

    normalized = " ".join(
        source.strip().lower().split()
    )

    if not normalized:
        raise ValueError(
            "Source cannot be empty."
        )

    if "official" in normalized:
        return 100, "Official source"

    source_scores = load_source_scores()

    source_data = source_scores.get(
        normalized
    )

    if source_data is None:
        return 40, "Unrated"

    score = source_data.get("score")
    tier = source_data.get("tier")

    if not isinstance(score, int):
        raise ValueError(
            f"Invalid score for source: {source}"
        )

    if not isinstance(tier, str):
        raise ValueError(
            f"Invalid tier for source: {source}"
        )

    return score, tier


def get_verdict(
    confidence: int,
    status: str,
) -> tuple[str, str]:

    if status == "official":
        return (
            "OFFICIAL",
            (
                "Official confirmation. "
                "Publish with a link to the original source."
            ),
        )

    if confidence >= 88:
        return (
            "VERY HIGH CONFIDENCE",
            (
                "Strong enough to publish with clear sourcing. "
                "Do not label it official."
            ),
        )

    if confidence >= 75:
        return (
            "HIGH CONFIDENCE",
            (
                "Publish with clear sourcing and "
                "make the report status clear."
            ),
        )

    if confidence >= 55:
        return (
            "MONITOR",
            (
                "Wait for stronger confirmation before "
                "treating it as verified."
            ),
        )

    return (
        "LOW CONFIDENCE",
        "Do not publish as verified news.",
    )


def check_source(
    source: str,
    status: str,
) -> CheckResult:

    normalized_status = normalize_status(
        status
    )

    source_score, source_tier = (
        get_source_score(source)
    )

    status_score = STATUS_SCORES[
        normalized_status
    ]

    confidence = round(
        (source_score * SOURCE_WEIGHT)
        + (status_score * STATUS_WEIGHT)
    )

    verdict, recommendation = (
        get_verdict(
            confidence,
            normalized_status,
        )
    )

    return CheckResult(
        source=source.strip(),
        source_tier=source_tier,
        source_score=source_score,
        status=normalized_status,
        status_score=status_score,
        confidence=confidence,
        verdict=verdict,
        recommendation=recommendation,
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "MATCHIQ Football Source Checker - "
            "a simple editorial confidence checker."
        )
    )

    parser.add_argument(
        "--source",
        help="Source name, for example: BBC Sport",
    )

    parser.add_argument(
        "--status",
        help=(
            "official, here we go, confirmed, "
            "reported, rumour, or unknown"
        ),
    )

    args = parser.parse_args()

    source = args.source or DEFAULT_SOURCE
    status = args.status or DEFAULT_STATUS

    try:
        result = check_source(
            source,
            status,
        )

    except (
        ValueError,
        FileNotFoundError,
        json.JSONDecodeError,
    ) as exc:
        print(f"Error: {exc}")
        return

    print(
        f"MATCHIQ Football Source Checker "
        f"v{VERSION}"
    )

    print("-" * 40)

    print(f"Source:         {result.source}")
    print(f"Source tier:    {result.source_tier}")
    print(
        f"Source score:   "
        f"{result.source_score}/100"
    )
    print(f"Status:         {result.status}")
    print(
        f"Status score:   "
        f"{result.status_score}/100"
    )
    print(
        "Weighting:      "
        f"Source {int(SOURCE_WEIGHT * 100)}% + "
        f"Status {int(STATUS_WEIGHT * 100)}%"
    )
    print(
        "Calculation:    "
        f"({result.source_score} * {SOURCE_WEIGHT}) + "
        f"({result.status_score} * {STATUS_WEIGHT}) = "
        f"{result.confidence}"
    )
    print(
        f"Confidence:     "
        f"{result.confidence}/100"
    )
    print(f"Verdict:        {result.verdict}")
    print(
        f"Recommendation: "
        f"{result.recommendation}"
    )


if __name__ == "__main__":
    main()
