# MATCHIQ Football Tools

[![Tests](https://github.com/louisonc10/matchiq-football-tools/actions/workflows/tests.yml/badge.svg)](https://github.com/louisonc10/matchiq-football-tools/actions/workflows/tests.yml)

A small open-source toolkit for checking football news and transfer reports before publication.

I started this project because football news moves quickly, and the line between an official announcement, a strong report and a normal rumour is often unclear.

The goal is simple: apply the same basic confidence check to every report before treating it as verified news.

## Current tool

### Football Source Checker

The Source Checker looks at two things:

- the reliability of the source
- the current status of the report

It then returns:

- source tier
- report status
- confidence score
- editorial verdict
- publishing recommendation

Example:

```text
Source:         Fabrizio Romano
Source tier:    Tier 1
Status:         here we go
Confidence:     90/100
Verdict:        VERY HIGH CONFIDENCE
Recommendation: Strong enough to publish with clear sourcing. Do not label it official.
