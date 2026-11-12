# Review G1: Guide Sections 1, 2, 2b (Guide_S1_S2_S2b.md)

Items checked: about 150 numbers/claims (all lines read). Edits applied: 22 targeted Edits. No FAQ files touched.

## Number audit (summary table; every row source-checked by grep)
| Claim | Source | Result |
|---|---|---|
| Pooled table, 20 skills (75/73/60/54/44/40/33/32/23/18/14/13/10/10/9/8/5/4/4/3 %) and class labels | MS Addendum (counts re-divided by 186) | OK |
| n=186 = 40+47+42+32+25 | MS Addendum | OK |
| MIS: Excel 72, SQL 44, Python 16 | jd_sample_mis_people Sec 4 (n=32) | OK number; label corrected (was "pooled, +/-7", now n=32, about +/-17) |
| Python 30/40/40 by sample | MS Addendum per-sample | OK; label corrected (per-sample n=47/42/25, +/-15-20; first sample 35%) |
| Stakeholder "about 60% Bengaluru and GCC" | MS Addendum (64/60/60; first 15, MIS 19) | OK; context added (Hyd 64, first/MIS low) |
| Excel/SQL only above 50%; 4 must-haves | MS Addendum | OK |
| "Python rising in Bengaluru/GCC" | none | corrected (rising unsupported; now 40 vs 30) |
| "Cloud, Snowflake... 5% or fewer to 10%" | MS Addendum | corrected wording (10, 5, 4, 4, 3) |
| SQL 98 / Python 80 (vendor) | MS Section 7 (ownyourcareer.in) | OK; source named |
| About 25 postings 3+ yrs | MS Section 3 (first sample only) | OK; "in the first sample" added |
| Interview table (19/15/14/14/10/8/7/6/6/5 of about 20) | IP Section 4 | OK |
| Flipkart, PhonePe, Meesho hardest SQL | IP 2.4, Section 3 | OK |
| Infosys Hyderabad Mar 2026, 1 report | IP Section 4 | OK |
| GenAI 14% pooled, 20% first sample | MS Addendum, MS Sec 3 | OK |
| Pay: 8 posted rows (8 of 40), TMI 160-180K | MS Section 4 | OK |
| Pay shown: 7/47, 7/42, 9/32, 0/25 | jd_sample_* pay sections | added (about 31 of 186) |
| Honhr 4.8 (x4), 6.0 (x1) | jd_sample_mis_people rows 1-5 | OK |
| Secondary snippets (5-12, 5.5-10, 6-10, 3.5-9, 4-12, 7.5, 3.5-6) | MS Sec 4, B0S | OK |
| Entry MIS/BA Rs 3-6 LPA | MS Addendum | OK |
| Example postings and experience labels (Tata Play, KPMG, HPE, EXL 2-5, TMI 2+, Quess, Hackett, TriNet, Gartner 0-2, C&W, Rocket 2-4, Syneos 3+, Unisys 4-6, Unisys OCM 0-2, Netcom 1-3, Easyship) | MS App A | OK; Easyship "2+" added |
| Worksheet arithmetic 8.0+0.5-5.5=3.0; 3.0/12=Rs 25,000 | arithmetic | OK (labelled illustrative) |

## Fixes
| Location | Problem | Fix |
|---|---|---|
| Intro | "0-2 years or entry level" and no sample sizes | states real inclusion rule and 40/47/42/32/25 |
| 1.2 MIS row, 1.3, 1.6 | MIS % labelled as pooled n=186 +/-7 | relabelled n=32, about +/-17 |
| 1.2 DA and BA rows, 2.9 | +/-7 applied to per-sample figures | per-sample n and wider error given |
| 1.3 | "rising" Python unsupported | rewritten with numbers |
| 1.4, 2b.6 | Conflict MS Sec 6 (DB Workday "Entry") vs Addendum (Workday roles 3+) not stated | conflict stated explicitly in both places |
| 1.4, 2.8 | "LinkedIn not accessible" contradicts Hyderabad sample (LinkedIn public pages used) | corrected |
| 2.2 | tail range wording wrong | corrected |
| 2b.1-2b.3, 2b.9 | pay table used only the first sample; omitted Rs 1.8-3, 3-5, 4-8 and 12-30 posted figures; "GCC reachable" without noting no GCC JD showed pay | added second table, counts, and honest evidence note for Rs 6-10 |
| 2b.5 worksheet | F in months but H in rupees; G (months to offer) cost logic wrong if applying while employed | F in rupees, G = months without income, H redefined |
| 2b.1 | "evidence says reachable" overstated | softened |

## Claims still unverified
- All vendor/blog pay figures (2b.4) remain unverified by design; DB Workday role experience level unresolved; "switcher-friendliness" ratings are judgement, labelled so.
- MS Addendum counts are sub-agent tallies (some keyword-matched, +/-2), not re-derived by me.

## Could not check
- Original postings (live pages) and the 3+ year observation (impression only). Pointers are by Book number only; none use Part numbers, so no plan.md part-table mismatches. Book 8 as "case-style thinking" and Books 7/8 mapping match plan.md.
