# Post-mortem: <short title>            (blameless: describe systems and decisions, not people)
Date of incident: <start - end>   Severity: <S1-S3>   Author: <name>   Status: <draft/final>

## Summary (3 lines)
What broke, who was affected, how it ended.

## Impact
Decisions affected (count, value), customers or teams, how long, what we could not undo.

## Timeline (from the event log, in UTC or IST, say which)
| time | event | source |

## Key times
Time to notice (any human) / time to detect (ML team) / time to mitigate / time to resolve.

## Root cause
- Trigger: the change that started it.
- Amplifier: what made it worse or bigger (for example no input check, auto-retrain used the bad data).
- Concealer: what hid it (for example the dashboard averaged it away, labels arrive in 30 days).

## What went well / what was lucky

## Monitoring gaps and action items
| gap | action | owner | due | how we will know it works |

## Lessons for the runbook
