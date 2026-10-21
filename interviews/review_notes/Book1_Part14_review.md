# Book 1 Part 14 review (Wave C)

Questions reviewed: 62 (19 three-star, 26 two-star, 17 one-star). No ANSWER_PENDING.

## Code
- 52 python blocks extracted and run standalone: 52 ran without error.
- 7 printed numbers did not match the text and were fixed (Q37, Q40, Q44, Q48, Q51; Q42 print format; Q46 added a Monte Carlo line, matches 0.555/0.556/0.556).
- Re-run after edits: Q37, Q42, Q44, Q46, Q48, Q51 all match the text and the in-block output comments.

## Fixes (Q, what, why)
- Header: three-star count 20 -> 19; removed stale "star counts may be stale" remark.
- Q10: Gauss-Markov "first five" -> "first six rows" (table has six non-normality rows).
- Q11: clearer HC0-HC3 wording.
- Q9: rewrote muddled follow-up on why rejection is needed for 7 outcomes.
- Q27, Q28, Q29, Q30, Q31, Q42: added the missing **Example** field (Q31's example was buried in a bullet; moved out). Q27/Q28/Q30 examples are hand-built and labelled illustrative.
- Q29: removed incorrect claim that the 12-month window biases the estimate (gap 11.77 vs 11.82 is sampling noise).
- Q30: "converges at rate d, ~30 iterations for 1e-10" was wrong as a general statement; now worst case ~140, this graph 31 (second eigenvalue 0.5).
- Q31: 1 - p/2 follow-up rewritten (one-sided p equals P(B>A) here by flat-prior/large-n coincidence, not an identity).
- Q35: VIF 158 -> about 196 (computed).
- Q36: reworded exp(prediction) follow-up (median, not mean).
- Q37: text numbers (DW 0.69, SE 0.261/0.402) did not match code (0.59, 0.287, 0.597). Updated; added 500-dataset results (true SD 0.685, mean naive SE 0.274, mean HAC10 0.52) and output comments in code. HAC is still short here; stated honestly.
- Q40: simulated variance 67,903 -> 68,378.
- Q42: sample size 2,700 -> about 2,600 (computed 2,626 with unpooled variance, two-sided 5%, 80% power); formula shown; paired caveat; print format cleaned.
- Q44: ridge/OLS coefficient numbers in text and comment did not match run; corrected.
- Q46: added Monte Carlo check (title asks for simulation).
- Q47: Say-this-first now states 0.20% with SF and 0.1965% excluding SF; verified 3,744 full houses, 5,108 flushes, P(ace)=0.3412, exactly-one-ace 0.2995.
- Q48: code used grid index 500 (f=0.4955); at f=0.5 growth is -0.0889, not -0.0865/-0.087. Fixed code and text.
- Q51: leverage of planted point 0.621 -> 0.571 (text and comment).
- Q57: confidence-sequence width rate softened (log log n is the lower bound, not the mixture rate).
- Q58: naive MC needs about 100/p draws for 10% relative error, not "1/p hits".
- Q62: HC1 scales the variance (not SE) by n/(n-p).

## Verified analytically and by simulation (no change)
Q1 (E=2, 1/4), Q2 (23, 50.7%, 57 -> 99.0%), Q3 (16.7%, sim 16.6%), Q4 (2/3), Q5 (14.7), Q7 (HH 6, HT 4), Q8 (1/3, 1/2), Q13/14 (Wilson and Beta intervals), Q18 table (all 12 cells), Q19, Q20 (EV -3.33, var 1388), Q21, Q24 (161/36, 5.820 for n=10), Q25, Q26, Q34 (naive 12.6%, Pocock 2.36, OBF 4.05/2.86/2.34/2.02), Q38 (1/4), Q39, Q41 (prior Beta(16.7,150.2), top-5 n and rates), Q45 (14, 10), Q53-Q56, Q57-Q61, Q62 (HC0 0.2368 etc.).

## Unresolved / not verified
- Citations: Johari et al. mSPRT/Optimizely attribution in Q57 kept (well known) but not web-checked.
- Q42 paired-test power gain depends on correlation of model errors; stated qualitatively only.
- Q37 and Q60/Q61 simulation numbers are seed-dependent illustrations.
