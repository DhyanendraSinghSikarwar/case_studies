**Follow-ups:**
- The provider will not let you pin a version. What do you do? Keep your own regression set and canary, own a fallback provider or model path, and treat each provider change as a release that must pass your eval gate.
- Why paired and not two proportions on the replay? The same questions are used twice, so only the questions that changed state carry information; pairing gives a tighter test.
- How would you size the canary? Pick the smallest drop that matters (say 4 points), use the paired or unpaired sample-size formula, and run it daily or at provider-change signals.

**Common mistakes:**
- Declaring the provider guilty from the thumbs drop alone.
- Comparing this week's live traffic with last week's instead of replaying the same questions.
- Not logging the model version and prompt hash with every answer.
- Building a canary too small to see a 4 to 8 point change.
- Fixing the prompt before reading the failure cases.
