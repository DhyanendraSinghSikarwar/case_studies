# Chapter 6 answer key: Valid, Invalid and Sound Arguments

Every verdict below was checked by computer: if-then shapes by full truth table; "all/some/no" arguments by testing every small group (up to 3 people, with every combination of properties), a counterexample being a group where all premises hold and the conclusion fails.

## Self-check answers

1. **No.** This is the invalid shape "If P then Q, Q, so P". Counterexample: the shop is closed but someone left the lights on. Both premises true, conclusion false.
2. **Yes.** If true premises and a true conclusion are connected by an invalid shape, the argument is still invalid (for example, "If 15 is divisible by 5 then 15 is odd; 15 is odd; so 15 is divisible by 5").
3. Valid means the conclusion must follow if the premises are true; sound means it is valid **and** the premises really are true.

## Practice answers

**Q1** **Valid** (modus ponens: If P then Q; P; so Q). Whenever both premises are true, the dashboard must not load.

**Q2** **Invalid.** Shape "If P then Q, Q, so P". Counterexample: today is the day before a festival, the branch is crowded, but it is not salary day. Both premises hold, conclusion false.

**Q3** **Invalid.** Shape "All A are B, x is B, so x is A". Counterexample: Sita is an office cashier who wears a helmet when riding her scooter to work; she is not warehouse staff. Premise 1 can still be true (all warehouse staff wear helmets) and premise 2 is true, yet the conclusion is false.

**Q4** **Valid.** "All A are B; x is A; so x is B". If every drawer pen is blue and this pen is from the drawer, it must be blue.

**Q5** **Yes.** Validity only says "if the premises are true then the conclusion is true". With a false premise the conclusion can be false. Example: "All fish can fly. A salmon is a fish. So a salmon can fly." Valid (structure is fine), conclusion false, because premise 1 is false.

**Q6** **Valid** (All A are B; x is A; so x is B). **Unsound**, because the first premise "All birds can fly" is false (penguins cannot). Its conclusion "penguins can fly" is also false, which shows a valid argument with a false premise can give a false conclusion.

**Q7** **Valid** (same shape) and **sound**: both premises are true (every prime greater than 2 is odd; 7 is a prime greater than 2), so the conclusion "7 is odd" is guaranteed true.

**Q8** **Valid** (modus tollens: If P then Q; not Q; so not P). If approval always brings a signature, no signature means it cannot have been approved.

**Q9** **Invalid** (denying the condition: If P then Q; not P; so not Q). Counterexample: Priya was given a long-service award at 3 years because of an exceptional contribution. The policy says 5 years leads to an award; it does not say nothing else can. Both premises true, conclusion false.

**Q10** **Valid** (the chain: If P then Q; if Q then R; so if P then R). Truth-table check: no combination makes both premises true while "if P then R" is false.

**Q11** **Invalid** ("P or Q, P, so not Q" wrongly rules out the other). Counterexample: both Arun and Bela approved the order. "Arun or Bela approved" is true (inclusive or), "Arun approved" is true, "Bela did not approve" is false.

**Q12** **Invalid.** Counterexample: Asha is an analyst and a manager but is never late; Basu is a manager and a late-comer but not an analyst. Premise 1: some analysts are managers (Asha). Premise 2: some managers are late-comers (Basu). Conclusion: some analysts are late-comers. Asha is the only analyst, and she is not late, so it is false.

**Q13** **Invalid.** Counterexample: Raj is an intern with no admin access, but he can delete records because his team lead granted him a delete permission directly. Take also one admin holder, Lata, who can delete. Premise 1: no intern has admin access (Raj has none). Premise 2: all admin holders can delete (Lata can). Conclusion "no intern can delete records" is false (Raj can). The second premise says what admin holders can do, not that only they can.

**Q14** Many answers work. One: A = dogs, B = pets, C = cats. Premise 1: all dogs are pets (true). Premise 2: some pets are cats (true). Conclusion: some dogs are cats (false). Another: A = cars, B = vehicles, C = bicycles. Computer check: this shape is invalid, so a counterexample always exists.

**Q15**
- (a) **(1) valid and sound.** All multiples of 4 are even (true), 12 is a multiple of 4 (true).
- (b) **(2) valid but unsound.** Structure "All A are B; x is A; so x is B" is fine, but premise 1 is false (10 is even but not a multiple of 4, so "all even numbers are multiples of 4" fails). The conclusion "10 is a multiple of 4" is false.
- (c) **(3) invalid.** Shape "All A are B; x is B; so x is A". Premises true, conclusion false (6 is not a multiple of 4).
- (d) **(3) invalid.** Shape "If P then Q; Q; so P". All three statements happen to be true, yet the shape does not guarantee it. The same shape with another number shows it can fail: "If 9 is divisible by 5 then 9 is odd" is true (its if-part is false, so nothing can break it); "9 is odd" is true; but "9 is divisible by 5" is false.

**Q16** **Valid** (All A are B; no B is C; so no A is C). Reason: a supervisor is a trained staff member; no trained staff member is on probation; so no supervisor can be on probation. Checked: no group makes both premises true and the conclusion false.

**Q17** **Invalid.** Both premises true and R true but P false occurs in exactly **2** combinations (P, Q, R):
- P false, Q false, R true: "if P then Q" is true (P false), "if Q then R" is true, R true, conclusion P false.
- P false, Q true, R true: both ifs true, R true, P false.

Other combinations fail either a premise or already make P true. A concrete reading: the candidate got feedback (R) without clearing aptitude (P false).

**Q18** **(a)**. With "Everyone who gets a raise has been promoted", "Dev got a raise" gives "Dev was promoted", a valid chain. (b), (c) and (d) say nothing linking raises to promotions; a computer search found a case for each where all premises are true and Dev was not promoted, so they leave the argument invalid.

**Q19** **Valid, but unsound.** The two premises contradict each other (all encrypted, yet one is not), so they can never be true together. Therefore there is no situation with true premises and a false conclusion, which is the definition of valid (called valid "by emptiness"). It is **not sound**, because at least one premise is always false. It also shows that validity alone proves nothing: from contradictory premises any conclusion is "valid".

**Q20**
(a) Replace premise 2 with **"Only admin-access holders can delete records"** (that is, everyone who can delete records holds admin access). Then: no intern has admin access, so no intern can delete records. Checked valid.
(b) Keep the premises and write the conclusion **"No admin-access holder is an intern."** Checked valid: it is the original first premise turned around. Any conclusion that must hold in every case where the premises hold works.
