"""Weighted scoring of Azure ML / Vertex AI / SageMaker for three org profiles.
Scores (0-5) and weights are MY judgement inputs for the interview, not measurements. Edit and rerun."""
CRITERIA = ["data_gravity", "identity", "skills", "compliance", "contracts", "gpu_in_region", "exit_cost"]
# 0-5, higher is better for that org. exit_cost: 5 = easy to leave.
SCORES = {
 "bank_gcc_m365": {"azure_ml": [3, 5, 4, 5, 5, 3, 3], "vertex": [2, 2, 2, 3, 2, 3, 3], "sagemaker": [2, 2, 3, 4, 3, 3, 3]},
 "product_bigquery": {"azure_ml": [2, 2, 2, 3, 2, 3, 3], "vertex": [5, 4, 4, 3, 4, 3, 3], "sagemaker": [2, 3, 3, 3, 3, 3, 3]},
 "services_all_clouds": {"azure_ml": [3, 4, 3, 4, 3, 3, 3], "vertex": [4, 3, 3, 3, 3, 3, 3], "sagemaker": [3, 3, 4, 3, 3, 3, 3]},
}
WEIGHTS = {
 "bank_gcc_m365":       [2, 4, 2, 5, 3, 2, 1],
 "product_bigquery":    [5, 2, 3, 2, 2, 3, 2],
 "services_all_clouds": [1, 1, 2, 2, 1, 2, 5],   # exit cost and client choice dominate
}
def score(profile, weights=None):
    w = weights or WEIGHTS[profile]
    assert len(w) == len(CRITERIA)
    tot = sum(w)
    return {p: round(sum(a * b for a, b in zip(w, s)) / tot, 2) for p, s in SCORES[profile].items()}

for prof in SCORES:
    r = score(prof)
    print(f"{prof:22s}", r, "->", max(r, key=r.get) if len(set(r.values())) > 1 else "tie: decide on client")

# Sensitivity: SAME scores for the services firm, two clients with different weights.
# data_gravity, identity, skills, compliance, contracts, gpu_in_region, exit_cost
client_a = [1, 5, 1, 4, 1, 1, 1]   # identity + compliance heavy (Entra shop)
client_b = [5, 1, 1, 1, 1, 1, 1]   # warehouse-heavy
print("services, client A weights:", score("services_all_clouds", client_a))
print("services, client B weights:", score("services_all_clouds", client_b))
# Hand check for bank/azure_ml: (2*3+4*5+2*4+5*5+3*5+2*3+1*3)/19 = 83/19
print("hand check:", round((2*3 + 4*5 + 2*4 + 5*5 + 3*5 + 2*3 + 1*3) / 19, 2))
