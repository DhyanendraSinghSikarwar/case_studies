#!/usr/bin/env bash
# Simulates what the runner does: the unsafe form pastes the title INTO the script text first.
TITLE='x"; echo INJECTED-COMMAND-RAN; echo "'
echo "--- unsafe: expression pasted into the script text"
printf 'echo "PR title is %s"\n' "$TITLE" > /tmp/claude-0/b7_q01_10/unsafe_step.sh
cat /tmp/claude-0/b7_q01_10/unsafe_step.sh
bash /tmp/claude-0/b7_q01_10/unsafe_step.sh
echo "--- safe: value passed as an environment variable"
PR_TITLE="$TITLE" bash -c 'echo "PR title is $PR_TITLE"'
