# Break-even: API model vs self-hosted fine-tuned small model.
# ALL NUMBERS BELOW ARE ASSUMED for illustration. Replace them with your own quotes and benchmarks.
import math
API_PRICE_PER_1M = 3.00     # ASSUMED blended USD per 1M tokens (input+output mix) for the API model
GPU_COST_PER_HR  = 2.00     # ASSUMED USD per hour for one GPU kept on 24x7
THROUGHPUT_TPS   = 1500     # ASSUMED sustained tokens/s per GPU at 100% load (batched)
FT_ONE_OFF       = 3000.0   # ASSUMED one-off USD: data work, training runs, evals
OPS_MONTHLY      = 1500.0   # ASSUMED monthly USD for maintenance / on-call share
HOURS = 730

gpu_month = GPU_COST_PER_HR * HOURS
cap_m = THROUGHPUT_TPS * 3600 * HOURS / 1e6          # M tokens one GPU can serve per month at 100%
print(f"one GPU: {gpu_month:,.0f} USD/month, capacity {cap_m:,.0f}M tokens/month at 100% load")

def self_cost(vol_m, util):
    """util = average utilisation you actually achieve (traffic is bursty, so < 100%)."""
    gpus = max(1, math.ceil(vol_m / (cap_m * util)))
    return gpus * gpu_month + OPS_MONTHLY

def api_cost(vol_m):
    return API_PRICE_PER_1M * vol_m

print("\nGPU-only cost per 1M tokens vs API price", API_PRICE_PER_1M)
for util in (0.7, 0.5, 0.3, 0.1):
    print(f"  util {util:.0%}: {gpu_month/(cap_m*util):.2f} USD per 1M tokens")

print("\nMonthly break-even volume (self-host cheaper from here)")
for util in (0.7, 0.5, 0.3, 0.1):
    v = next((m for m in range(1, 50000) if self_cost(m, util) < api_cost(m)), None)
    print(f"  util {util:.0%}: {('%dM tokens/month' % v) if v else 'never (GPU per-token cost >= API price)'}")

vol, util = 2000, 0.5
sav = api_cost(vol) - self_cost(vol, util)
print(f"\nAt {vol}M tokens/month, util {util:.0%}: API {api_cost(vol):,.0f} vs self {self_cost(vol, util):,.0f} USD/month,"
      f" saving {sav:,.0f}; one-off {FT_ONE_OFF:,.0f} pays back in {FT_ONE_OFF/sav:.1f} months")
