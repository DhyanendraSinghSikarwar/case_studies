### Q17 ⭐⭐⭐ 🔴 Conversation logs store full prompts for 400 days, and a scan of 500,000 stored conversations finds phone numbers or emails in 2% of them, which is 10,000 conversations. Support staff and an analytics vendor can read the logs. What do you do now, what do you change in the logging design, and how do you handle the 10,000 existing conversations?
**Asked at:** PII and compliance material (tianpan, Kunal Ganglani, Gravitee and barkingiguana pages on logs, retention, redaction and data residency, and a vendor piece on DPDP readiness for LLM traffic); vendor and practitioner pages, not regulator guidance or an interview bank; commonly reported in public guides for data scientist, ML engineer and GenAI engineer loops; search snippets only, not opened
**Say this first (1 line):** I would stop the exposure now by limiting who can read the logs and masking PII before storage, then shorten retention and clean the 10,000 existing conversations, with legal deciding on any notification duty.

**Clarifying questions:**
- Did the scan cover all 500,000 conversations or a sample, and how was PII detected? Why it matters: a regex misses some PII, so 10,000 is probably a floor.
- What do support staff and the vendor need? Why it matters: least access can often replace full access.
- What does the vendor contract and data-processing agreement say? Why it matters: sets what the vendor may keep and train on.
- Why 400 days? Why it matters: the retention need decides how much to keep.
- Where are the logs stored (region, backups)? Why it matters: copies and residency add scope.

**Approach:**
1. Now: restrict log access to named roles, turn on access auditing, and check who has already read or exported them. Pause the vendor feed or redact it first.
2. Tell privacy and legal today. Whether this is a reportable incident and what notice is due is their decision; I do not make legal claims here.
3. Fix at the source: redact before write (detect phone numbers, emails, ids and replace with typed tokens like PHONE), keep raw prompts out of logs by default, and store only what debugging needs.
4. Split storage: raw (short retention, tight access) and redacted (longer retention, wider access). Encrypt both.
5. Cut retention to what is justified. If volume and PII rate are constant, 30 days keeps about 37,500 conversations with about 750 containing PII, against 10,000 at 400 days.
6. Backfill: run the redaction job over the 10,000 flagged conversations, plus a second, different detector to catch what the first missed. Keep a record of what was changed.
7. Verify: sample 1,000 after redaction. Zero hits means an upper bound near 0.30% (rule of three), not zero.
8. Deletion path: be able to find and delete a person's conversations on request.

**Metrics:**
- PII rate = conversations with detected PII / conversations scanned (2.0%).
- Detector recall = PII items found / PII items present, estimated on a hand-labelled sample.
- Reader count = distinct people or systems with access to raw logs.
- Residual rate after redaction with its upper bound.
- Guardrails: debugging resolution time, no redaction that breaks the logs' usefulness.

**Risks:**
- Redaction that is incomplete (names, addresses, free-text ids).
- The vendor already holds copies.
- Over-redaction that makes logs useless, so teams bypass the system.
- Deleting evidence needed for the review.

**What the interviewer scores:**
- Strong: stop the exposure first, involve legal, fix design, handle the backlog, verify with a bounded claim.
- Strong: notes the detector's recall limit.
- Weak: "delete everything" or "ignore, 2% is small".
- Weak: claims legal conclusions.

**Example:** Illustrative. Weak: "Run a regex and delete the matches." Strong: "I would cut vendor and support access to a named few today, mask on write from the next deploy, redact the 10,000 with two detectors, and report the residual as less than about 0.3% at 95% on a 1,000 sample. Legal decides on notification."

**Code:**
```python
import math
stored, hit_rate = 500_000, 0.02
n_pii = int(stored * hit_rate)
print(f"conversations with PII: {n_pii:,}")
assert n_pii == 10_000
# Steady-state effect of shorter retention (assumes constant volume and constant PII rate).
for days in (400, 90, 30):
    kept = stored * days / 400
    print(f"retention {days:>3} days: ~{kept:,.0f} stored, ~{kept*hit_rate:,.0f} with PII")
assert stored * 30 / 400 * hit_rate == 750
# After redaction at write, check a random sample; zero hits is not zero risk.
n = 1000
rule3 = 3 / n
exact = 1 - 0.05 ** (1 / n)
print(f"0 PII hits in {n} sampled: 95% upper bound ~{rule3:.2%} (rule of three), exact {exact:.3%}")
assert round(rule3, 4) == 0.003 and round(exact, 5) == 0.00299
# A regex scan has recall below 100%: if it finds 10,000 at recall 80%, the true count is higher.
for recall in (1.0, 0.8, 0.6):
    print(f"detector recall {recall:.0%}: implied true PII conversations ~{n_pii/recall:,.0f}")
assert round(n_pii / 0.8) == 12_500
```

**Output (my run):**
```
conversations with PII: 10,000
retention 400 days: ~500,000 stored, ~10,000 with PII
retention  90 days: ~112,500 stored, ~2,250 with PII
retention  30 days: ~37,500 stored, ~750 with PII
0 PII hits in 1000 sampled: 95% upper bound ~0.30% (rule of three), exact 0.299%
detector recall 100%: implied true PII conversations ~10,000
detector recall 80%: implied true PII conversations ~12,500
detector recall 60%: implied true PII conversations ~16,667
```

**Follow-ups:**
- Can you keep raw prompts for debugging? Yes, briefly, with restricted access and automatic expiry.
- What about the vendor's copy? Check the contract, ask for deletion or confirm retention, and stop sending raw data.
- How do you prove it is fixed? Scheduled scans with a labelled recall check and an access-audit report.

**Common mistakes:**
- Trusting a regex scan as complete.
- Redacting new logs and forgetting the backlog.
- Giving legal conclusions in the interview.
- Wide access "for convenience".

