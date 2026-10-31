import re,sys
f=sys.argv[1]
t=open(f,encoding='utf-8').read()
bl=re.split(r'(?m)^(?=### C\d+ )',t)[1:]
labs=['Evidence level','Roles seen in sources','Process overview (as reported)','Round by round','Question types','Sample questions (illustrative)','What they score','Level notes','Preparation plan (2 weeks)','Common mistakes','Recent changes and AI-era notes','Sources','Confidence and what to verify']
bad=[]
for b in bl:
    n=b.split('\n')[0][:40]
    pos=[b.find('\n**'+l+':**') for l in labs]
    if -1 in pos or pos!=sorted(pos): bad.append((n,'labels',[labs[i] for i,p in enumerate(pos) if p==-1]))
    if b.count('```')%2: bad.append((n,'fence'))
    body=b.split('**Sources:**')[0]
    if len(re.findall(r'\[(?:S\d+|G|U)\]',body))<8: bad.append((n,'few evidence tags'))
    src=b.split('**Sources:**')[1].split('**Confidence')[0] if '**Sources:**' in b else ''
    urls=re.findall(r'https?://[^\s)>\]]+',src)
    if len(urls)<2: bad.append((n,'few source urls',len(urls)))

    have=set(re.findall(r'(?m)^\s*(?:[-*]|\d+\.)?\s*S(\d+)\s*[.:]',src))
    used=set(re.findall(r'S(\d+)',' '.join(re.findall(r'\[[^\]]*\]',body))))
    if used-have: bad.append((n,'tags without a source',sorted(used-have)))
    sq=b.split('**Sample questions (illustrative):**')[1].split('\n**')[0] if '**Sample questions (illustrative):**' in b else ''
    items=[l for l in sq.split('\n') if re.match(r'\s*(?:[-*]|\d+\.)\s',l)]
    if not 5<=len(items)<=8: bad.append((n,'sample question count',len(items)))
    for l in items:
        if not re.search(r'\[(?:illustrative|S\d+)\]',l): bad.append((n,'untagged sample question',l[:50]))
pat=re.compile(r'(?i)\bLPA\b|\blakhs?\b|\bcrores?\b|\bCTC\b|\bsalary\b|\bsalaries\b|compensation|base pay|per annum|[$€₹£]\s?\d|\b(?:USD|EUR|INR|GBP)\s?\d|\d\s?(?:USD|EUR|INR|GBP)\b')
sal=[(m.group(0),t[max(0,m.start()-40):m.end()+40].replace('\n',' ')) for m in pat.finditer(t)]
print(len(bl),'profiles; bad:',bad)
print('salary-pattern hits:',len(sal),sal[:5])
print('pending markers:',t.count('ANSWER_PENDING'))
