isolation test: acme and gamma never receive beta-CANARY across 50 results each
served/sent: {'acme': 69, 'beta': 5} {'acme': 500, 'beta': 5}
cost units per tenant: {'acme': 2.1, 'beta': 0.4, 'gamma': 5.0}
tenant with      5,000 vectors: shared      0.1 vs dedicated  200.0  (ASSUMED monthly cost units)
tenant with    100,000 vectors: shared      2.0 vs dedicated  200.0  (ASSUMED monthly cost units)
tenant with  5,000,000 vectors: shared    100.0 vs dedicated  200.0  (ASSUMED monthly cost units)
tenant with 20,000,000 vectors: shared    400.0 vs dedicated  200.0  (ASSUMED monthly cost units)
offboarding: rows 91 -> 60 ; no beta vectors or text remain in this store (backups, caches and logs need their own deletion)
