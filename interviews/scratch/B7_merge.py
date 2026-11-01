import re,sys,glob
N=int(sys.argv[1])
folders=sorted(glob.glob('scratch/B7P%02d_C*'%N))
txt=''
for d in folders:
    p=d+'/profiles.md'
    try: s=open(p).read().strip()
    except FileNotFoundError: print('missing',p); continue
    txt+=s+'\n\n'
bl=re.split(r'(?m)^(?=### C\d+ )',txt)[1:]
nums=[int(re.match(r'### C(\d+)',b).group(1)) for b in bl]
print('profiles',nums)
assert nums==sorted(nums)
out='scratch/B7P%02d_body.md'%N
open(out,'w').write(''.join(bl))
print('wrote',out)
