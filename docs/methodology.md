# Scoring Methodology

MATCHIQ Football Tools uses a simple editorial confidence score to help decide how a football report should be treated before publication.

The score is not a prediction of whether a story is true.

For example, a score of 90 does **not** mean there is a 90% chance that the report is correct. It only means the report currently meets a high level of confidence based on the source and the reported status.

## How the score works

The current score uses two inputs:

- Source reliability: 65%
- Report status: 35%

The calculation is:

```text
Confidence Score =
(Source Score × 0.65) +
(Status Score × 0.35)
