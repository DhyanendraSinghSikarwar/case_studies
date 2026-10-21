# Book 1 Part 07 review

Questions reviewed: 49. Header (49 Qs; 15/21/13 stars) verified correct. No ANSWER_PENDING. CRLF preserved.

## Code
- 14 python blocks extracted and run standalone (Q1, 6, 7, 12, 13, 16, 19, 21, 22, 26, 32, 35, 36, 46). 12 ran and matched quoted numbers as-is.
- Q32 and Q46 were fragments (not standalone): made standalone. Q32 original setup could not be reconstructed, so I set up my own illustrative simulation; all quoted numbers updated (true 0.0918, IPS 0.0942, clip 0.0629, SNIPS 0.095, DR 0.0949, ESS ~16,100). Q46 lambdas [0.215 -0.16 0.015 -0.074 0.004] reproduced exactly.
- Q19 LightGBM already had n_jobs=1; runs ~37 s; added note. Outputs 0.902 / 0.372 match.
- Q36 sparse-mask claim corrected (15% mask: val 1.08 vs train 0.44 at 60 epochs, was "about 1.0 vs 0.4").

## Fixes
- Q6, Q13, Q19: added missing Example field.
- Q9: latency figures labelled illustrative. Q20: example labelled back-of-envelope; HNSW "would not fit" softened.
- Q31: BERT4Rec claim rewritten (Petrov & Macdonald 2022 replicability study; SASRec with softmax loss competitive) - from memory, not web-checked.
- Q38: TIGER (Rajput et al. 2023) cited, flagged as research result.
- Q27: interleaving "10-100x fewer queries" softened.
- Q11, Q24, Q27, Q39, Q40, Q49: examples labelled illustrative.

## Unresolved / not verified
- No web verification done (citations from memory: Petrov & Macdonald 2022, Rajput 2023, Hu 2019, Yi 2019, Beutel 2018, Hu-Koren-Volinsky). Netflix Prize non-deployment claim (Q17) unverified here.
- Q43 "80% of gain at 1/50th cost" already labelled illustrative target.
