**Say this first (1 line):** Pick a resolution rule that matches the stakes (majority vote for cheap independent checks, supervisor or judge for reasoned disputes, confidence weighting when scores are calibrated, human escalation for high-risk or split decisions), and remember that agents built on the same base model make correlated mistakes, so adding more voters helps far less than the maths for independent voters suggests.

**Then explain (mechanisms listed by the DEV guide):**
- **Voting:** N agents answer, take the majority. Simple and parallel (it is the voting form of parallelisation in Q3). Works best on questions with a short, comparable answer.
- **Supervisor adjudication:** a lead agent reads the conflicting outputs and decides. Handles free text, but the supervisor can be wrong or biased towards the first or longest answer.
- **Debate with a judge:** agents argue, a judge picks. Surfaces reasoning, costs many calls, and the judge has its own biases (position, verbosity, preferring its own style; see Part 9 on LLM-as-judge).
- **Confidence weighting:** weight by stated confidence. Only useful if confidence is calibrated; model self-reported confidence often is not (Part 3 on calibration ideas, Part 9 for evaluation).
- **Human escalation:** if votes split or confidence is low, route to a person. Define the threshold and the queue before launch.
- **What goes wrong:** (1) correlated errors: agents on one model share blind spots, so they agree on the same wrong answer; (2) convergence and sycophancy: in a debate agents drift towards the most confident or most recent claim; (3) judge bias; (4) cost growth with little gain. Mitigate with diversity (different models, prompts, retrieval sources, tools), an independent verifier that checks evidence not opinion, and ground-truth checks where possible.

**Example:** (synthetic, my simulation, not real model data) each agent is right 70% of the time. With independent errors, a 15-agent majority reaches 0.95. If half the questions are ones where all agents share one draw (rho = 0.5), 15 agents reach only 0.83; at rho = 0.9 they reach 0.725, barely above one agent, and going from 9 to 15 agents adds almost nothing. So buy diversity before you buy more voters.

**Code:** (run; SYNTHETIC; the correlation model is a simple assumption I chose)
@@CODE@@

**Follow-ups:**
- *How do you get diversity?* Different models or providers, different prompts and evidence, tools that return ground truth; temperature alone gives little.
- *Vote or judge?* Vote when answers are short and checkable; judge when answers are long, and calibrate the judge against labelled examples.
- *When to escalate to a human?* Split votes, low evidence, or irreversible actions (Part 5 Q39 for approval design).

**Common mistakes:** assuming independent errors; using the same model as voters and as judge; trusting self-reported confidence; letting debates run until agents agree; never measuring whether the vote beat a single agent.
