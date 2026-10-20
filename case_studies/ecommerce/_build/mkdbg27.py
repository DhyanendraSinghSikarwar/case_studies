import re,sys
D=sys.argv[1]
s=open("_build/src/cs27.src",encoding="utf-8").read()
cells=re.split(r"^#%% (md|code)\s*$",s,flags=re.M)
out=["import matplotlib,time\nmatplotlib.use('Agg')\n_T=time.time()\n"]
n=0
for i in range(1,len(cells),2):
    if cells[i]=="code":
        c=cells[i+1]
        if c.strip().startswith("%%writefile"): continue
        c=c.replace("t0 = time.time(); raw, prod, truth = gen.generate(seed=SEED)","t0=time.time(); raw=pd.read_csv('data/cs27/ratings.csv.gz',parse_dates=['ts']); prod=pd.read_csv('data/cs27/products.csv.gz'); truth=pd.read_csv('data/cs27/users_truth.csv.gz')")
        c=c.replace('raw.to_csv("data/cs27/ratings.csv.gz", index=False); prod.to_csv("data/cs27/products.csv.gz", index=False); truth.to_csv("data/cs27/users_truth.csv.gz", index=False)',"")
        lines=c.rstrip().split("\n"); last=lines[-1]
        if re.match(r"^[A-Za-z_][\w\.]*(\.round\(\d\))?$",last): lines[-1]="print("+last+")"
        out.append("\n".join(lines)+f"\nprint('### cell {n} done', round(time.time()-_T), flush=True)\n"); n+=1
open(D+"/dbg27.py","w",encoding="utf-8").write("\n".join(out))
