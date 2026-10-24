FAIL  buggy  T1 tenant a still gets its own context (ctx 0 chars)
PASS  fixed  T1 tenant a still gets its own context (ctx 53 chars)
FAIL  buggy  T5 cache keyed by tenant
PASS  fixed  T5 cache keyed by tenant
FAIL  buggy  T7 api key not logged
PASS  fixed  T7 api key not logged
FAIL  buggy  T6 stops generating after disconnect (tokens made: 50)
PASS  fixed  T6 stops generating after disconnect (tokens made: 1)
FAIL  buggy  T8 loop stays responsive (max gap 0.16s)
PASS  fixed  T8 loop stays responsive (max gap 0.01s)
PASS  fixed  T2 slow dependency times out in <1s
PASS  fixed  T4 context bounded (cites 1 of 3)
PASS  fixed  T3 citations are retrieved chunk ids
PASS  fixed  T2b model passed per request (cache key includes it)
FAIL  buggy  T3 citations are retrieved chunk ids
