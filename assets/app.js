'use strict';
const D=window.PURSUITS_DATA, C=window.PursuitCore, all=C.decode(D);
const $=id=>document.getElementById(id);
const esc=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const fmt=n=>n.toLocaleString('en-US');
const money=n=>n>=1e9?`$${(n/1e9).toFixed(2)}B`:n>=1e6?`$${(n/1e6).toFixed(1)}M`:n>=1000?`$${(n/1000).toFixed(0)}K`:`$${fmt(n)}`;
const exactMoney=n=>new Intl.NumberFormat('en-US',{style:'currency',currency:'USD',maximumFractionDigits:0}).format(n);
const types=['Modernization','Whitespace','Competitive','Expansion'];
const symbols=['↗','◇','◎','+'];
const typeSub=['Evolve the installed base','Explore a new footprint','Investigate competitive activity','Review growth potential'];
let state=C.initialState();
let page=0, selected=null, filtered=[], toastTimer;
const pageSize=8;

function fillOptions(id,values){$(id).insertAdjacentHTML('beforeend',[...new Set(values)].sort().map(v=>`<option value="${esc(v)}">${esc(v)}</option>`).join(''));}
function reset(){state=C.initialState();page=0;selected=null;for(const id of ['product','industry','region','type','search'])$(id).value='';$('sort').value='score';render();}
function setFilter(field,value){state[field]=value;page=0;if($(field))$(field).value=value;render();}
function toggleBand(band){state.bands=state.bands.includes(band)?state.bands.filter(b=>b!==band):[...state.bands,band];page=0;render();}
function renderCharts(){
  const max=Math.max(1,...D.products.map(p=>filtered.filter(r=>r.product===p).length));
  $('product-chart').innerHTML=D.products.map(product=>{const n=filtered.filter(r=>r.product===product).length;return `<button class="chart-row ${state.product===product?'active':''}" data-product="${esc(product)}" aria-pressed="${state.product===product}" aria-label="${esc(product)}: ${n} pursuits; toggle filter"><span>${esc(product)}</span><span class="track"><i style="width:${n/max*100}%"></i></span><strong>${fmt(n)}</strong><small>${filtered.length?(n/filtered.length*100).toFixed(0):0}%</small></button>`;}).join('');
  const bands=D.bands.map(b=>({b,n:filtered.filter(r=>r.band===b).length}));const peak=Math.max(1,...bands.map(b=>b.n));
  const ranges=['85–100','70–84.9','55–69.9','40–54.9','0–39.9'];
  $('score-chart').innerHTML=bands.map(({b,n},i)=>`<button class="hist-col ${state.bands.includes(b)?'active':''}" data-band="${esc(b)}" aria-pressed="${state.bands.includes(b)}" aria-label="${esc(b)}: ${n} pursuits; toggle filter"><strong>${fmt(n)}</strong><span class="hist-bar" style="height:${n/peak*125}px"></span><span>${esc(b)}<small>${ranges[i]}</small></span></button>`).join('');
  const high=filtered.filter(r=>r.score>=70).length;
  $('signal-insight').textContent=!filtered.length?'No pursuits match this combination. Reset filters to explore again.':`${fmt(high)} ${high===1?'pursuit scores':'pursuits score'} 70+. Curated synthetic examples use the same fixed rules. ${state.scope==='strategic'?'Scores below 55 are excluded in this view.':'All score bands are included.'}`;
  $('type-cards').innerHTML=types.map((type,i)=>{const n=filtered.filter(r=>r.type===type).length;return `<button class="type-card ${state.type===type?'active':''}" data-type="${type}" aria-pressed="${state.type===type}"><span class="type-symbol" aria-hidden="true">${symbols[i]}</span><span><b>${type}</b><small>${typeSub[i]}</small></span><strong>${fmt(n)}</strong></button>`;}).join('');
}
function showDetail(r){
  if(!r){$('detail').innerHTML='<div class="empty"><h3>No pursuit selected</h3><p>Broaden your filters to explore account evidence.</p></div>';return;}
  const contributions=r.signals.map((v,i)=>v*D.components[i][1]/100);
  const channelText=Object.entries(r.channels).sort((a,b)=>b[1]-a[1]).map(([ch,n])=>`${fmt(n)} ${ch.toLowerCase()} ${n===1?'record':'records'}`).join(', ');
  const brief=`${r.account_name} has ${r.deployment==='No Footprint'?'no recorded footprint':r.deployment.toLowerCase()+' deployment'} in ${r.product}. Its supplied product-engagement index is ${r.engagement}/100. ${r.event_count} account-wide activity records inform intent, including ${r.recent_count} within 90 relative days. ${r.open_count?`${r.open_count} open product ${r.open_count===1?'opportunity totals':'opportunities total'} ${exactMoney(r.pipeline)}.`:'No open product pipeline is recorded.'}`;
  let next=r.type==='Whitespace'?'Validate product need and the recorded footprint with the account owner before proposing a new-product conversation.':r.type==='Modernization'?'Review the current deployment, technical constraints and migration appetite with the account owner.':r.type==='Competitive'?'Validate competitor presence and timing; high intensity may indicate risk as well as an opening.':'Check adoption, unmet needs and existing account plans before proposing expansion.';
  if(r.open_count)next+=' Coordinate with the existing opportunity owner; do not treat this as net-new pipeline.';
  $('detail').innerHTML=`<p class="eyebrow">PURSUIT INTELLIGENCE</p><h3>${esc(r.account_name)}</h3><p class="account-meta">${esc(r.account_id)} · ${esc(r.region)} · ${esc(r.industry)}<br>${esc(r.customer_tier)} · ${fmt(r.employee_count)} employees</p><div class="detail-product">${esc(r.product)}</div><span class="tag ${r.type}">${r.type}</span> <span class="detail-note">${esc(r.deployment)}</span><div class="score-hero"><div class="score-ring" style="--progress:${r.score}"><strong>${r.score.toFixed(1)}</strong></div><div><b>${r.band}</b><small>Priority score / 100</small><small>Portfolio rank #${fmt(r.rank)}</small></div></div><h4>What contributes to this score?</h4>${D.components.map(([label,w],i)=>`<div class="signal-row"><div><span>${label}</span><strong>${contributions[i].toFixed(1)} / ${w}</strong></div><div class="track"><i style="width:${r.signals[i]}%"></i></div></div>`).join('')}<p class="detail-note">Bars show weighted contributions—not probabilities. Components are displayed rounded; the total uses unrounded values.</p><div class="brief"><h4>Evidence brief · template generated</h4><p>${esc(brief)}</p>${D.scenarios.some(s=>s.account_id===r.account_id)?'<p class="detail-note">This account includes a documented synthetic demo scenario. See Methodology for context.</p>':''}</div><div class="evidence"><details><summary>Inspect the underlying signals</summary><dl><dt>Customer fit · ${r.fit.toFixed(1)}/100</dt><dd>Annual revenue ${exactMoney(r.annual_revenue)}; ${fmt(r.employee_count)} employees; ${esc(r.industry)}. Target-industry and size assumptions are documented in Methodology.</dd><dt>Account intent · ${r.intent.toFixed(1)}/100</dt><dd>${esc(channelText)}. Latest record ${r.latest_days===null?'not available':r.latest_days+' relative days ago'}. These are account-level records, not unique people or product-specific events. No absolute event dates were supplied.</dd><dt>Product engagement · ${r.engagement}/100</dt><dd>A synthetic source-provided index, not reconstructed from raw product events.</dd><dt>Competitive intensity · ${r.competition}/100</dt><dd>${r.competitors.length?esc(r.competitors.join(', '))+' recorded. Highest intensity used.':'No competitor record. Zero contribution does not establish absence.'}</dd><dt>Open product pipeline · ${exactMoney(r.pipeline)}</dt><dd>${r.open_count} open records. Normalized pipeline signal: ${r.signals[6].toFixed(1)}/100. Unweighted amount; not a revenue forecast.</dd></dl></details></div><p class="next-step"><b>Suggested next step</b><br>${esc(next)}</p>`;
}
function renderTable(){
  const last=Math.max(0,Math.ceil(filtered.length/pageSize)-1);page=Math.min(page,last);
  const current=filtered.slice(page*pageSize,(page+1)*pageSize);
  $('rows').innerHTML=current.length?current.map(r=>`<tr class="${r.key===selected?'selected':''}"><td><button class="account-link" data-key="${r.key}" aria-label="Inspect ${esc(r.account_name)}, ${esc(r.product)}" aria-pressed="${r.key===selected}">${esc(r.account_name)}</button><small>${esc(r.product)} · ${esc(r.region)}</small></td><td><span class="tag ${r.type}">${r.type}</span><small>${esc(r.deployment)}</small></td><td><span class="score-number">${r.score.toFixed(1)}</span><span class="mini-bar"><i style="width:${r.score}%"></i></span></td><td title="${exactMoney(r.pipeline)}">${money(r.pipeline)}<small>${r.open_count} open ${r.open_count===1?'record':'records'}</small></td></tr>`).join(''):'<tr><td colspan="4" class="empty">No matching pursuits. Try fewer filters or switch to All signals.</td></tr>';
  $('page-label').textContent=filtered.length?`${fmt(page*pageSize+1)}–${fmt(Math.min((page+1)*pageSize,filtered.length))} of ${fmt(filtered.length)}`:'0 pursuits';
  $('prev').disabled=page===0;$('next').disabled=page>=last;
  showDetail(filtered.find(r=>r.key===selected));
}
function render(){
  filtered=C.filter(all,state);if(!filtered.some(r=>r.key===selected))selected=filtered[0]?.key??null;
  const totals=C.totals(filtered);
  $('metric-pursuits').textContent=fmt(totals.strategic);$('metric-scope').textContent=state.scope==='all'?`${fmt(totals.count)} total combinations in view`:'Scores of 55 or more';
  $('metric-accounts').textContent=fmt(totals.accounts);$('metric-pipeline').textContent=money(totals.pipeline);$('metric-pipeline').title=exactMoney(totals.pipeline);
  $('metric-modern').textContent=fmt(totals.modern);$('metric-modern-share').textContent=`${totals.count?(totals.modern/totals.count*100).toFixed(1):'0'}% of the filtered combinations`;
  $('scope-note').innerHTML=`Showing <strong>${fmt(totals.count)} account–product combinations</strong> from ${fmt(D.audit.accounts)} synthetic accounts and ${D.products.length} product families. ${state.scope==='strategic'?'Strategic view includes scores ≥55.':'All signals includes scores below 55.'} Metrics and charts follow all filters.`;
  $('result-count').textContent=`${fmt(totals.count)} pursuits · ${fmt(totals.accounts)} accounts`;
  $('export').disabled=!filtered.length;
  for(const v of ['strategic','all']){const b=$('scope-'+v);b.classList.toggle('selected',state.scope===v);b.setAttribute('aria-pressed',String(state.scope===v));}
  $('band-summary').textContent=state.bands.length?`${state.bands.length} ${state.bands.length===1?'band':'bands'} selected`:'All bands';
  document.querySelectorAll('[data-band-input]').forEach(el=>el.checked=state.bands.includes(el.value));
  const choices=new Map(all.filter(r=>C.matches(r,state,{ignoreSearch:true})).map(r=>[r.account_id,r]));
  $('account-options').innerHTML=[...choices.values()].sort((a,b)=>a.account_name.localeCompare(b.account_name,undefined,{numeric:true})).map(r=>`<option value="${esc(r.account_name)}" label="${esc(r.account_id+' · '+r.region)}"></option>`).join('');
  renderCharts();renderTable();
}
function navigate(view){
  const method=view==='method';$('workspace').hidden=method;document.querySelector('.hero').hidden=method;
  $('method').hidden=!method;$('overview').hidden=view!=='overview';$('explorer').hidden=view!=='explorer';
  document.querySelectorAll('[data-view]').forEach(b=>{b.classList.toggle('active',b.dataset.view===view);if(b.dataset.view===view)b.setAttribute('aria-current','page');else b.removeAttribute('aria-current');});
  $('breadcrumb').textContent=({overview:'Overview',explorer:'Account Explorer',method:'Methodology'})[view];
  window.scrollTo({top:0,behavior:'auto'});
}
fillOptions('product',D.products);fillOptions('industry',D.accounts.map(a=>a.industry));fillOptions('region',D.accounts.map(a=>a.region));fillOptions('type',types);
$('band-options').innerHTML=D.bands.map((b,i)=>`<label><input type="checkbox" data-band-input value="${esc(b)}">${b}</label>`).join('')+'<button id="clear-bands" class="text-button">Clear band selection</button>';
for(const id of ['product','industry','region','type'])$(id).addEventListener('change',e=>setFilter(id,e.target.value));
$('search').addEventListener('input',e=>setFilter('search',e.target.value));
$('sort').addEventListener('change',e=>setFilter('sort',e.target.value));
$('reset').addEventListener('click',reset);
for(const v of ['strategic','all'])$('scope-'+v).addEventListener('click',()=>setFilter('scope',v));
$('band-options').addEventListener('change',e=>{if(e.target.matches('[data-band-input]'))toggleBand(e.target.value);});
$('clear-bands').addEventListener('click',()=>{state.bands=[];page=0;render();});
document.addEventListener('click',e=>{
  const p=e.target.closest('[data-product]');if(p)setFilter('product',state.product===p.dataset.product?'':p.dataset.product);
  const b=e.target.closest('[data-band]');if(b)toggleBand(b.dataset.band);
  const t=e.target.closest('[data-type]');if(t)setFilter('type',state.type===t.dataset.type?'':t.dataset.type);
  const row=e.target.closest('[data-key]');if(row){selected=row.dataset.key;renderTable();if(window.innerWidth<1000)$('detail').scrollIntoView({behavior:'smooth',block:'start'});}
  const nav=e.target.closest('[data-view]');if(nav)navigate(nav.dataset.view);
  if(!e.target.closest('#band-menu'))$('band-menu').open=false;
});
document.querySelector('.brand').addEventListener('click',e=>{e.preventDefault();navigate('overview');});
document.addEventListener('keydown',e=>{if(e.key==='Escape')$('band-menu').open=false;});
$('prev').addEventListener('click',()=>{page--;renderTable();});$('next').addEventListener('click',()=>{page++;renderTable();});
$('export').addEventListener('click',()=>{
  const rows=C.order(filtered,'score').slice(0,Number($('export-limit').value));
  const blob=new Blob([C.csv(rows)],{type:'text/csv;charset=utf-8'}),url=URL.createObjectURL(blob);
  const a=document.createElement('a');a.href=url;a.download='strategic-pursuits-shortlist.csv';document.body.append(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),1000);
  $('toast').textContent=`Exported ${rows.length} pursuits, ranked by priority score. Filters respected.`;$('toast').hidden=false;clearTimeout(toastTimer);toastTimer=setTimeout(()=>$('toast').hidden=true,5000);
});
$('weight-list').innerHTML=D.components.map(([label,w])=>`<div class="weight"><span>${label}</span><strong>${w}%</strong></div>`).join('');
$('audit-summary').innerHTML=`<b>Build-time reconciliation passed</b><br>${D.audit.synthetic_scenarios} documented synthetic scenarios<br>${fmt(D.audit.combinations)} unique account–product rows<br>${fmt(D.audit.whitespace)} source whitespace records preserved<br>${exactMoney(D.audit.open_pipeline)} open pipeline reconciled to effective inputs<br>No invalid account links or missing footprint/engagement combinations`;
render();
navigate('overview');
