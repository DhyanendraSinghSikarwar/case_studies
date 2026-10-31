ASSUMED: 20M rows, 350 in / 60 out tokens, $0.20 / $0.80 per 1M tokens
one pass, online pricing:  $2,360
one pass, batch discount 0.5: $1,180  (discount is an assumption)
a prompt change forces a re-run of affected fields: 3 re-runs = $3,540
input tokens in total: 7.0B
run 1 stopped by budget: True | saved 572 | dead 28
resume: new calls 400 (none repeated for saved rows) | saved 950 | dead 50
prompt v2 run: calls 950 (rows already in the dead table are skipped, so a poison row is not retried forever)
audit of 100 sampled rows: 97 correct, 95% Wilson interval 0.92-0.99
