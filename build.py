"""Rebuild the standalone Strategic Pursuits demo. Python 3.10+, standard library only.

Source CSVs are preserved; seeded demo scenarios are reproducible. No model training occurs.
"""
import csv
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
from demo_scenarios import enrich

ROOT = Path(__file__).resolve().parent
PRODUCTS = ['Infrastructure', 'Database', 'Analytics & Data', 'AI & ML', 'Security', 'Applications', 'Integration']
TARGETS = {'Manufacturing', 'Financial Services', 'Telecommunications', 'Healthcare', 'Energy'}
COMPONENTS = [('Customer fit', 20), ('Customer intent', 20), ('Product engagement', 15), ('Product whitespace', 10), ('Modernization', 15), ('Competitive intensity', 10), ('Product pipeline', 10)]
BANDS = ['Very Strong', 'Strong', 'Moderate', 'Emerging', 'Not Prioritized']

def read(name):
    with (ROOT / 'data/source' / (name + '.csv')).open(encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))

def minmax(values):
    lo, hi = min(values), max(values)
    return [0.0 if hi == lo else (v-lo)/(hi-lo)*100 for v in values]

def band(score):
    return BANDS[0] if score >= 85 else BANDS[1] if score >= 70 else BANDS[2] if score >= 55 else BANDS[3] if score >= 40 else BANDS[4]

def deployment(states):
    active = set(states) - {'No Footprint'}
    if not active: return 'No Footprint'
    if 'Hybrid' in active or {'Cloud', 'On-Premise'} <= active: return 'Hybrid'
    return 'On-Premise' if 'On-Premise' in active else 'Cloud'

def modernization(state, engagement):
    if state == 'On-Premise': return 85 if engagement >= 60 else 55
    return {'Hybrid':65, 'Cloud':20, 'No Footprint':0}[state]

def classify(state, modern, competition):
    if state == 'No Footprint': return 'Whitespace'
    if modern >= 65: return 'Modernization'
    if competition >= 60: return 'Competitive'
    return 'Expansion'

def fit(a):
    revenue = a['annual_revenue']; employees = a['employee_count']
    rs = 100 if revenue >= 5e9 else 85 if revenue >= 1e9 else 65 if revenue >= 5e8 else 45
    es = 100 if employees >= 25000 else 85 if employees >= 10000 else 65 if employees >= 5000 else 45
    return rs*.4 + es*.3 + (100 if a['industry'] in TARGETS else 55)*.3

def score(values):
    # Scale then round-to-even, matching numpy/pandas' original one-decimal path.
    total=sum(v*(w/100) for v, (_,w) in zip(values,COMPONENTS))
    return round(total*10)/10

def build_data(enriched=True):
    tables = {n:read(n) for n in ['accounts','product_footprint','engagement_events','product_engagement','competitors','opportunities']}
    scenarios=enrich(tables,PRODUCTS,fit) if enriched else []
    accounts = tables['accounts']
    ids = {a['account_id'] for a in accounts}
    assert len(ids)==len(accounts), 'Duplicate account IDs'
    for name, records in tables.items():
        assert all(r['account_id'] in ids for r in records), f'Orphan account in {name}'
        if name not in ['accounts','engagement_events']:
            assert all(r['product_family'] in PRODUCTS for r in records), f'Unknown product in {name}'
    for name in ['product_footprint','product_engagement']:
        keys=[(r['account_id'],r['product_family']) for r in tables[name]]
        assert len(keys)==len(set(keys)), f'Duplicate source grain: {name}'
        assert len(keys)==len(accounts)*len(PRODUCTS), f'Incomplete account-product coverage: {name}'
    assert all(r['deployment'] in ['Cloud','On-Premise','Hybrid','No Footprint'] for r in tables['product_footprint'])
    assert all(r['deployment'] in ['Cloud','No Footprint'] for r in tables['product_footprint'] if r['product_family']=='AI & ML')
    assert all(0<=float(r['product_engagement_score'])<=100 for r in tables['product_engagement'])
    assert all(0<=float(r['intensity'])<=100 for r in tables['competitors'])
    assert all(0<=int(r['days_ago'])<=365 for r in tables['engagement_events'])
    assert all(float(r['amount'])>=0 and r['status'] in ['Open','Won','Lost','Closed'] for r in tables['opportunities'])
    assert all(float(r['consumption'])>=0 for r in tables['product_footprint'])
    events=defaultdict(list); fps=defaultdict(list); pe={}; comp=defaultdict(list); opp=defaultdict(list)
    for r in tables['engagement_events']: events[r['account_id']].append(r)
    for r in tables['product_footprint']: fps[r['account_id'],r['product_family']].append(r)
    for r in tables['product_engagement']: pe[r['account_id'],r['product_family']]=int(r['product_engagement_score'])
    for r in tables['competitors']: comp[r['account_id'],r['product_family']].append(r)
    for r in tables['opportunities']:
        if r['status']=='Open': opp[r['account_id'],r['product_family']].append(r)
    counts=[len(events[a['account_id']]) for a in accounts]
    weighted=[sum(max(.2,1-int(e['days_ago'])/365*.8) for e in events[a['account_id']]) for a in accounts]
    nc,nw=minmax(counts),minmax(weighted)
    normalized_accounts=[]
    for i,a in enumerate(accounts):
        a['annual_revenue']=float(a['annual_revenue']); a['employee_count']=int(a['employee_count'])
        aid=a['account_id']; ev=events[aid]
        normalized_accounts.append({**a,'fit':fit(a),'intent':nw[i]*.7+nc[i]*.3,
            'event_count':len(ev),'weighted_activity':round(weighted[i],4),
            'channels':dict(Counter(e['channel'] for e in ev)),
            'latest_days':min((int(e['days_ago']) for e in ev),default=None),
            'recent_count':sum(int(e['days_ago'])<=90 for e in ev)})
    rows=[]
    for ai,a in enumerate(normalized_accounts):
        for pi,product in enumerate(PRODUCTS):
            key=(a['account_id'],product); footprint=fps[key]
            state=deployment(r['deployment'] for r in footprint)
            engagement=pe[key]; modern=modernization(state,engagement)
            competitive=max((int(r['intensity']) for r in comp[key]),default=0)
            pipeline=sum(float(r['amount']) for r in opp[key])
            rows.append({'ai':ai,'pi':pi,'deployment':state,'engagement':engagement,'modernization':modern,
                'competition':competitive,'pipeline':pipeline,'open_count':len(opp[key]),
                'competitors':sorted(set(r['competitor'] for r in comp[key])),
                'type':classify(state,modern,competitive)})
    ps=minmax([r['pipeline'] for r in rows])
    for r,pipeline_score in zip(rows,ps):
        a=normalized_accounts[r['ai']]
        r['signals']=[a['fit'],a['intent'],r['engagement'],100 if r['deployment']=='No Footprint' else 0,r['modernization'],r['competition'],pipeline_score]
        r['score']=score(r['signals']); r['band']=band(r['score'])
    rows.sort(key=lambda r:(-r['score'],-r['pipeline'],normalized_accounts[r['ai']]['account_id'],PRODUCTS[r['pi']]))
    for rank,r in enumerate(rows,1): r['rank']=rank
    source_whitespace=sum(r['deployment']=='No Footprint' for r in tables['product_footprint'])
    assert source_whitespace==sum(r['deployment']=='No Footprint' for r in rows)
    expected=sum(float(r['amount']) for r in tables['opportunities'] if r['status']=='Open')
    assert sum(r['pipeline'] for r in rows)==expected, 'Pipeline reconciliation failed'
    cols=list(rows[0]); packed=[[r[c] for c in cols] for r in rows]
    audit={'source_rows':{n:len(v) for n,v in tables.items()},'accounts':len(accounts),'combinations':len(rows),
        'whitespace':source_whitespace,'strategic':sum(r['score']>=55 for r in rows),
        'bands':dict(Counter(r['band'] for r in rows)),'max_score':max(r['score'] for r in rows),
        'open_pipeline':expected,'synthetic_scenarios':len(scenarios),'source_hashes':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((ROOT/'data/source').glob('*.csv'))}}
    result={'version':'2.2','products':PRODUCTS,'components':COMPONENTS,'bands':BANDS,
        'accounts':normalized_accounts,'columns':cols,'rows':packed,'audit':audit}
    result['scenarios']=scenarios
    result['_tables']=tables
    return result, rows

def main():
    data, rows=build_data()
    tables=data.pop('_tables')
    effective=ROOT/'data/effective';effective.mkdir(exist_ok=True)
    for name,records in tables.items():
        with (effective/(name+'.csv')).open('w',encoding='utf-8',newline='') as f:
            writer=csv.DictWriter(f,fieldnames=list(records[0]));writer.writeheader();writer.writerows(records)
    (ROOT/'data/demo-scenarios.json').write_text(json.dumps(data['scenarios'],indent=2),encoding='utf-8')
    # The downloadable manifest keeps every product scenario. The browser only
    # needs a small account list for its disclosure, not a second full dataset.
    data['scenarios']=[{'account_id':aid} for aid in sorted({r['account_id'] for r in data['scenarios']})]
    (ROOT/'data/audit.json').write_text(json.dumps(data['audit'],indent=2),encoding='utf-8')
    payload=json.dumps(data,separators=(',',':'),ensure_ascii=True).replace('<','\\u003c')
    template=(ROOT/'assets/template.html').read_text(encoding='utf-8')
    css='\n'.join((ROOT/'assets'/name).read_text(encoding='utf-8') for name in ['style.css','navigation.css'])
    html=template.replace('/*__STYLE__*/',css)
    html=html.replace('/*__DATA__*/','window.PURSUITS_DATA='+payload+';')
    html=html.replace('/*__CORE__*/',(ROOT/'assets/core.js').read_text(encoding='utf-8'))
    html=html.replace('/*__APP__*/',(ROOT/'assets/app.js').read_text(encoding='utf-8'))
    (ROOT/'index.html').write_text(html,encoding='utf-8')
    fields=['rank','account_id','account_name','region','industry','product_family','deployment','type','score','band','pipeline','open_count']+[c for c,_ in COMPONENTS]
    with (ROOT/'data/account_product_scores.csv').open('w',encoding='utf-8',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=fields); writer.writeheader()
        for r in rows:
            a=data['accounts'][r['ai']]
            out={k:r[k] for k in ['rank','deployment','type','score','band','pipeline','open_count']}
            out.update({k:a[k] for k in ['account_id','account_name','region','industry']})
            out['product_family']=PRODUCTS[r['pi']]
            out.update({c:round(v,6) for (c,_),v in zip(COMPONENTS,r['signals'])})
            writer.writerow(out)
    print(json.dumps({k:v for k,v in data['audit'].items() if k!='source_hashes'},indent=2))
    print(f'Standalone page: {ROOT / "index.html"} ({len(html):,} characters)')

if __name__=='__main__': main()
