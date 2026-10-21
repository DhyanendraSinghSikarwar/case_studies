from scipy.stats import chisquare
obs=[50_600, 49_000]            # control, treatment; planned 50/50
stat,p=chisquare(obs, f_exp=[sum(obs)/2]*2)
print(round(stat,1), p)
