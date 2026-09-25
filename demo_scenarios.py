"""Version 2.2: deterministic, illustrative buying-stage scenarios.

Demographics and footprints are preserved. Other inputs vary by assumed buying
stage; scores and bands are never assigned directly. Not a calibrated market model.
"""
import random

STAGES=['Quiet','Exploring','Evaluating','Advanced evaluation']
MIX={'Quiet':[.70,.25,.05,0], 'Exploring':[.18,.52,.27,.03],
     'Evaluating':[.06,.18,.56,.20], 'Advanced evaluation':[.03,.10,.27,.60]}

def enrich(tables, products, fit):
    rng=random.Random(20260924)
    account_stages={};events=[]
    for a in tables['accounts']:
        aid=a['account_id']
        fit_value=fit({**a,'annual_revenue':float(a['annual_revenue']),'employee_count':int(a['employee_count'])})
        high_fit_example=fit_value>=94 and rng.random()<.65
        stage='Advanced evaluation' if high_fit_example else rng.choices(STAGES,weights=[.22,.33,.34,.11])[0]
        account_stages[aid]=(stage,high_fit_example)
        if high_fit_example: count,ages=28,(1,6)
        elif stage=='Advanced evaluation': count,ages=rng.randint(26,28),(2,25)
        elif stage=='Evaluating':count,ages=rng.randint(21,27),(5,75)
        elif stage=='Exploring':count,ages=rng.randint(13,20),(35,190)
        else:count,ages=rng.randint(3,10),(90,365)
        for _ in range(count):
            events.append({'account_id':aid,'channel':rng.choice(['Event','Webinar','Campaign','Website','Product Page']),'days_ago':str(rng.randint(*ages))})
    footprint={(r['account_id'],r['product_family']):r['deployment'] for r in tables['product_footprint']}
    # Retain closed records; regenerate open pipeline, never add it on top.
    opportunities=[dict(r) for r in tables['opportunities'] if r['status']!='Open']
    competition=[];product_engagement=[];manifest=[]
    for a in tables['accounts']:
        aid=a['account_id'];account_stage,high_fit=account_stages[aid]
        for product in products:
            state=footprint[aid,product]
            stage=rng.choices(STAGES,weights=MIX[account_stage])[0]
            if high_fit and state=='On-Premise' and rng.random()<.85:stage='Advanced evaluation'
            if stage=='Advanced evaluation':
                engagement=rng.randint(97,100);presence=.97;intensity=rng.randint(97,100);open_chance=.97;amount_range=(.94,1.0)
            elif stage=='Evaluating':
                engagement=rng.randint(76,94);presence=.78;intensity=rng.randint(68,93);open_chance=.75;amount_range=(.22,.72)
            elif stage=='Exploring':
                engagement=rng.randint(45,73);presence=.45;intensity=rng.randint(35,67);open_chance=.28;amount_range=(.04,.22)
            else:
                engagement=rng.randint(10,42);presence=.15;intensity=rng.randint(10,40);open_chance=.05;amount_range=(.005,.05)
            product_engagement.append({'account_id':aid,'product_family':product,'product_engagement_score':str(engagement)})
            competitor=None
            if rng.random()<presence:
                competitor=rng.choice(['Competitor A','Competitor B','Competitor C','Competitor D'])
                competition.append({'account_id':aid,'product_family':product,'competitor':competitor,'intensity':str(intensity)})
            amount=0
            if rng.random()<open_chance:
                amount=round(15_500_000*rng.uniform(*amount_range))
                opportunities.append({'account_id':aid,'product_family':product,'amount':str(amount),'status':'Open','weighted_amount':str(amount*.75)})
            manifest.append({'account_id':aid,'product_family':product,'account_stage':account_stage,'product_stage':stage,
                'high_fit_advanced_example':high_fit,'deployment_preserved':state,'engagement_index':engagement,
                'competitive_intensity':intensity if competitor else 0,'open_pipeline':amount})
    tables['engagement_events']=events
    tables['product_engagement']=product_engagement
    tables['competitors']=competition
    tables['opportunities']=opportunities
    return manifest
