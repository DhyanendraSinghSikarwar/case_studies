import re,glob
def clean(t):
    t=re.sub(r'\.?;? ?Editor note for Wave B: [^\n]*?no legal advice\.(;)?',lambda m:(';' if m.group(1) else ''),t)
    t=t.replace('Book 4 covers the monitoring mechanics','Book 4 Part 8 (monitoring) covers the mechanics')
    t=t.replace('Book 6 covers the technical trade-offs','Book 6 Part 6 covers data-science trade-offs with numbers')
    return t
for f in ['Book9_SoftSkills/Book9_SoftSkills_Part04.md']+glob.glob('scratch/B9P04_S*/answers.md'):
    t=open(f).read(); n=clean(t)
    if n!=t: open(f,'w').write(n); print('cleaned',f)
