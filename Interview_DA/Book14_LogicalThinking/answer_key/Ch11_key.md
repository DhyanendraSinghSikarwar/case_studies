# Chapter 11 answer key

Flowcharts are written as text outlines (see Chapter 11 for how to read them). Every chart below was run by code against its rule on every combination of test values listed in the notes, with no mismatches, and checked so that every box is reachable and every path ends at an End.

## Self-check answers

1. A **diamond** is the shape for a question. A yes/no question has **two exits**, one labelled Yes and one labelled No.
2. 800 is not over 1000, so the answer to the question is No. The order follows the No arrow to 'Add delivery fee of 50'. The result is a fee of 50.
3. The person following the chart cannot tell which answer sends them along that arrow, so two readers could choose different paths. Every exit of a question must be labelled.

## Practice answers

### Q1: Free delivery

**How to build it.** One question with two exits is all this needs. The test is 'at least 999', so exactly 999 goes to the Yes arrow: this is the boundary case that people get wrong.

**Flowchart (text outline):**

```text
S (Start) Start
-> D1 <Question> Is the order total 999 or more?
    Yes: E1 (End) Delivery fee 0
    No: E2 (End) Delivery fee 49
```

**Trace of the test cases:**

| Input | Path through the chart | Result |
|---|---|---|
| order total 998 | `S > D1(No) > E2` | Delivery fee 49 |
| order total 999 | `S > D1(Yes) > E1` | Delivery fee 0 |
| order total 2500 | `S > D1(Yes) > E1` | Delivery fee 0 |

### Q2: Attendance marking

**How to build it.** Two questions in a row. The 'is there a record' question must come first because you cannot compare a time that does not exist. Then 09:30 exactly belongs to On time because the rule says '09:30 or earlier'.

**Flowchart (text outline):**

```text
S (Start) Start
-> D1 <Question> Is there a swipe-in record?
    Yes: D2 <Question> Is the swipe-in time 9:30 or earlier?
        Yes: E2 (End) On time
        No: E3 (End) Late
    No: E1 (End) Absent
```

**Trace of the test cases:**

| Input | Path through the chart | Result |
|---|---|---|
| no swipe record | `S > D1(No) > E1` | Absent |
| swipe at 09:30 | `S > D1(Yes) > D2(Yes) > E2` | On time |
| swipe at 09:31 | `S > D1(Yes) > D2(No) > E3` | Late |

### Q3: Refund approval

**How to build it.** Both conditions must hold for approval, so approval sits at the end of a chain: a No at either question exits to a rejection. The order of the questions matters here because the text asks for the 'too late' reason first.

**Flowchart (text outline):**

```text
S (Start) Start
-> D1 <Question> Is the request within 7 days of purchase?
    Yes: D2 <Question> Is the item unused?
        Yes: E3 (End) Approve refund
        No: E2 (End) Reject: item used
    No: E1 (End) Reject: too late
```

**Trace of the test cases:**

| Input | Path through the chart | Result |
|---|---|---|
| 7 days, item unused | `S > D1(Yes) > D2(Yes) > E3` | Approve refund |
| 3 days, item used | `S > D1(Yes) > D2(No) > E2` | Reject: item used |
| 9 days, item unused | `S > D1(No) > E1` | Reject: too late |

### Q4: Leave approval

**How to build it.** The balance check comes first because it can end the process before any approval is needed. Then the days split into three bands with two chained questions. The manager question appears twice (once on the 3 to 5 band, once on the 6 or more band); drawing it twice keeps the chart a simple tree. HR is asked only after the manager says yes.

**Flowchart (text outline):**

```text
S (Start) Start
-> D1 <Question> Are the days asked more than the leave balance?
    Yes: E1 (End) Reject: balance too low
    No: D2 <Question> Are the days asked 2 or fewer?
        Yes: E2 (End) Auto-approve
        No: D3 <Question> Are the days asked 5 or fewer?
            Yes: D4 <Question> Does the manager approve?
                Yes: E3 (End) Approve
                No: E4 (End) Reject by manager
            No: D5 <Question> Does the manager approve?
                Yes: D6 <Question> Does HR approve?
                    Yes: continue at E3 (shown above)
                    No: E5 (End) Reject by HR
                No: continue at E4 (shown above)
```

**Trace of the test cases:**

| Input | Path through the chart | Result |
|---|---|---|
| 4 days asked, balance 3 | `S > D1(Yes) > E1` | Reject: balance too low |
| 2 days asked, balance 10 | `S > D1(No) > D2(Yes) > E2` | Auto-approve |
| 4 days asked, balance 10, manager says yes | `S > D1(No) > D2(No) > D3(Yes) > D4(Yes) > E3` | Approve |
| 8 days asked, balance 10, manager yes, HR no | `S > D1(No) > D2(No) > D3(No) > D5(Yes) > D6(No) > E5` | Reject by HR |
| 8 days asked, balance 10, manager no | `S > D1(No) > D2(No) > D3(No) > D5(No) > E4` | Reject by manager |

### Q5: Hiring flow

**How to build it.** Each stage is a gate: a No exits to its own rejection, a Yes moves to the next gate. Four gates in a row make a straight line of questions with one exit per gate.

**Flowchart (text outline):**

```text
S (Start) Start
-> D1 <Question> Is the resume shortlisted?
    Yes: D2 <Question> Is the test score 60 or more?
        Yes: D3 <Question> Did the candidate pass the interview?
            Yes: D4 <Question> Is the background check clear?
                Yes: E5 (End) Make offer
                No: E4 (End) Offer withdrawn
            No: E3 (End) Reject after interview
        No: E2 (End) Reject after test
    No: E1 (End) Reject at screening
```

**Trace of the test cases:**

| Input | Path through the chart | Result |
|---|---|---|
| shortlisted, test 59 | `S > D1(Yes) > D2(No) > E2` | Reject after test |
| shortlisted, test 60, interview passed, background clear | `S > D1(Yes) > D2(Yes) > D3(Yes) > D4(Yes) > E5` | Make offer |
| shortlisted, test 85, interview passed, background not clear | `S > D1(Yes) > D2(Yes) > D3(Yes) > D4(No) > E4` | Offer withdrawn |
| not shortlisted | `S > D1(No) > E1` | Reject at screening |

### Q6: Login with 3 tries

**How to build it.** This chart needs a loop: an action 'read the password and add 1 to tries' that can be visited up to 3 times. The counter is set to 0 once, before the loop, and the 'have 3 tries been used' question sits on the No branch of the password check, so a correct password never reaches it.

**Flowchart (text outline):**

```text
S (Start) Start
-> P0 [Action] Set tries = 0
-> P1 [Action] Read the password entered; add 1 to tries
-> D1 <Question> Is the password correct?
    Yes: E1 (End) Logged in
    No: D2 <Question> Have 3 tries been used?
        Yes: E2 (End) Account locked
        No: continue at P1 (shown above)
```

**Trace of the test cases:**

| Input | Path through the chart | Result |
|---|---|---|
| wrong, wrong, right | `S > P0 > P1 > D1(No) > D2(No) > P1 > D1(No) > D2(No) > P1 > D1(Yes) > E1` | Logged in |
| wrong, wrong, wrong | `S > P0 > P1 > D1(No) > D2(No) > P1 > D1(No) > D2(No) > P1 > D1(No) > D2(Yes) > E2` | Account locked |
| right on the first try | `S > P0 > P1 > D1(Yes) > E1` | Logged in |

### Q7: Expense claim

**How to build it.** The receipt rule applies only above 500, so the first question splits on the amount. The second split (5000) happens for every claim that survives the receipt rule, including small ones, so both branches of the first question join at the same node. Joining branches is allowed: many arrows may enter one node.

**Flowchart (text outline):**

```text
S (Start) Start
-> D1 <Question> Is the amount more than 500?
    Yes: D2 <Question> Is a receipt attached?
        Yes: D3 <Question> Is the amount 5000 or less?
            Yes: E2 (End) Approve by manager
            No: D4 <Question> Does the finance head approve?
                Yes: E3 (End) Approve by finance head
                No: E4 (End) Reject by finance head
        No: E1 (End) Reject: receipt missing
    No: continue at D3 (shown above)
```

**Trace of the test cases:**

| Input | Path through the chart | Result |
|---|---|---|
| amount 500, no receipt | `S > D1(No) > D3(Yes) > E2` | Approve by manager |
| amount 501, no receipt | `S > D1(Yes) > D2(No) > E1` | Reject: receipt missing |
| amount 5000, receipt attached | `S > D1(Yes) > D2(Yes) > D3(Yes) > E2` | Approve by manager |
| amount 5001, receipt attached, finance head says no | `S > D1(Yes) > D2(Yes) > D3(No) > D4(No) > E4` | Reject by finance head |
| amount 9000, receipt attached, finance head says yes | `S > D1(Yes) > D2(Yes) > D3(No) > D4(Yes) > E3` | Approve by finance head |

### Q8: Complaint ticket

**How to build it.** Urgency chooses the target (two actions), then both branches join at the same action 'agent works, read reply, add 1 to rounds'. The loop returns to that join action. Escalation happens on the third No, which is why the count is checked after a No only.

**Flowchart (text outline):**

```text
S (Start) Start
-> D1 <Question> Is the ticket urgent?
    Yes: P1 [Action] Assign to a senior agent, target 4 hours
    -> P3 [Action] Agent works on the ticket; read the customer reply; add 1 to rounds
    -> D2 <Question> Did the customer confirm it is solved?
        Yes: E1 (End) Closed
        No: D3 <Question> Have 3 rounds been used?
            Yes: E2 (End) Escalated to manager
            No: continue at P3 (shown above)
    No: P2 [Action] Assign to a normal agent, target 24 hours
    -> continue at P3 (shown above)
```

**Trace of the test cases:**

| Input | Path through the chart | Result |
|---|---|---|
| urgent; customer replies: not solved, solved | `S > D1(Yes) > P1 > P3 > D2(No) > D3(No) > P3 > D2(Yes) > E1` | Closed |
| not urgent; replies: not solved, not solved, not solved | `S > D1(No) > P2 > P3 > D2(No) > D3(No) > P3 > D2(No) > D3(No) > P3 > D2(No) > D3(Yes) > E2` | Escalated to manager |
| not urgent; replies: solved | `S > D1(No) > P2 > P3 > D2(Yes) > E1` | Closed |

### Q9: Bonus decision

**How to build it.** This is a decision tree: no loops, six outcomes drawn as three end boxes reused by several arrows. Check warnings first because it overrides everything else. Then split on rating (4 or 5, exactly 3, other) and then on tenure inside each branch.

**Flowchart (text outline):**

```text
S (Start) Start
-> D1 <Question> Does the employee have any warnings?
    Yes: E3 (End) No bonus
    No: D2 <Question> Is the rating 4 or 5?
        Yes: D3 <Question> Is tenure 2 years or more?
            Yes: E1 (End) Full bonus
            No: E2 (End) Half bonus
        No: D4 <Question> Is the rating exactly 3?
            Yes: D5 <Question> Is tenure 5 years or more?
                Yes: continue at E2 (shown above)
                No: continue at E3 (shown above)
            No: continue at E3 (shown above)
```

**Trace of the test cases:**

| Input | Path through the chart | Result |
|---|---|---|
| rating 4, tenure 2, no warnings | `S > D1(No) > D2(Yes) > D3(Yes) > E1` | Full bonus |
| rating 4, tenure 1, no warnings | `S > D1(No) > D2(Yes) > D3(No) > E2` | Half bonus |
| rating 3, tenure 5, no warnings | `S > D1(No) > D2(No) > D4(Yes) > D5(Yes) > E2` | Half bonus |
| rating 5, tenure 10, one warning | `S > D1(Yes) > E3` | No bonus |
| rating 3, tenure 4, no warnings | `S > D1(No) > D2(No) > D4(Yes) > D5(No) > E3` | No bonus |

### Q10: Order fulfilment

**How to build it.** Two gates before the payment loop (stock) and one question after it (express). The loop retries the payment action; the count is checked only after a failure. Note that the end boxes for 'express' and 'standard' sit after the payment succeeded, so they can only be reached through the Yes arrow of 'did the payment go through'.

**Flowchart (text outline):**

```text
S (Start) Start
-> D1 <Question> Are all items in stock?
    Yes: P0 [Action] Set attempts = 0
    -> P1 [Action] Take the payment; add 1 to attempts
    -> D2 <Question> Did the payment go through?
        Yes: D4 <Question> Did the customer choose express delivery?
            Yes: E3 (End) Ship express
            No: E4 (End) Ship standard
        No: D3 <Question> Have 3 attempts been used?
            Yes: E2 (End) Order cancelled
            No: continue at P1 (shown above)
    No: E1 (End) Backorder
```

**Trace of the test cases:**

| Input | Path through the chart | Result |
|---|---|---|
| an item is out of stock | `S > D1(No) > E1` | Backorder |
| in stock; payments: fail, fail, fail | `S > D1(Yes) > P0 > P1 > D2(No) > D3(No) > P1 > D2(No) > D3(No) > P1 > D2(No) > D3(Yes) > E2` | Order cancelled |
| in stock; payments: fail, success; express chosen | `S > D1(Yes) > P0 > P1 > D2(No) > D3(No) > P1 > D2(Yes) > D4(Yes) > E3` | Ship express |
| in stock; payment succeeds first time; express not chosen | `S > D1(Yes) > P0 > P1 > D2(Yes) > D4(No) > E4` | Ship standard |

## Notes on verification

Each flowchart was coded as a small graph and run on the following numbers of input combinations, comparing the outcome with a direct if/else version of the written rule: Q1 6, Q2 5, Q3 8, Q4 72, Q5 24, Q6 8, Q7 24, Q8 16, Q9 60, Q10 32. Worked examples and scenarios were checked the same way.
