from dataclasses import dataclass
import argparse


VERSION = "0.1.0"

# Change these two values when using the Run button
DEFAULT_SOURCE = "Fabrizio Romano"
DEFAULT_STATUS = "here we go"


SOURCE_SCORES = {
    "fabrizio romano": (90, "Tier 1"),
    "david ornstein": (95, "Tier 1"),
    "bbc sport": (90, "Tier 1"),
    "the athletic": (90, "Tier 1"),
    "sky sports": (82, "Tier 2"),
}


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
    status: str
    confidence: int
    verdict: str
    recommendation: str


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

    if normalized in SOURCE_SCORES:
        return SOURCE_SCORES[normalized]

    return 40, "Unrated"


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
        (source_score * 0.65)
        + (status_score * 0.35)
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
        status=normalized_status,
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
        help=(
            "Source name, for example: BBC Sport"
        ),
    )

    parser.add_argument(
        "--status",
        help=(
            "official, here we go, confirmed, "
            "reported, rumour, or unknown"
        ),
    )

    args = parser.parse_args()

    source = (
        args.source
        or DEFAULT_SOURCE
    )

    status = (
        args.status
        or DEFAULT_STATUS
    )

    try:
        result = check_source(
            source,
            status,
        )

    except ValueError as exc:
        print(f"Error: {exc}")
        return

    print(
        f"MATCHIQ Football Source Checker "
        f"v{VERSION}"
    )

    print("-" * 40)

    print(
        f"Source:         "
        f"{result.source}"
    )

    print(
        f"Source tier:    "
        f"{result.source_tier}"
    )

    print(
        f"Status:         "
        f"{result.status}"
    )

    print(
        f"Confidence:     "
        f"{result.confidence}/100"
    )

    print(
        f"Verdict:        "
        f"{result.verdict}"
    )

    print(
        f"Recommendation: "
        f"{result.recommendation}"
    )


if __name__ == "__main__":
    main()
