# MATCHIQ Football Tools

A small open-source toolkit for checking football news and transfer reports before they are published.

I started this project because football news moves quickly and the line between a confirmed report, a strong source and a normal rumour is often unclear.

The idea is simple: give each report a consistent confidence check before treating it as verified news.

## Current tools

### Source Checker

Checks a report using two things:

- who the source is
- how far the story has progressed

It then gives the report a confidence score and a simple publishing recommendation.

## Quick start

Python 3.10+ is recommended.

```bash
python src/source_checker.py --source "BBC Sport" --status reported
