/* Pure analytical presentation functions, shared by the UI and tests. */
(function(root){
  'use strict';
  const decode = d => d.rows.map(values=>{const r=Object.fromEntries(d.columns.map((c,i)=>[c,values[i]])); return {...r,...d.accounts[r.ai],product:d.products[r.pi],key:`${r.ai}:${r.pi}`};});
  function matches(r,s,{ignoreSearch=false,ignoreProduct=false,ignoreType=false,ignoreBands=false}={}){
    return (s.scope==='all'||r.score>=55)&&(!s.product||ignoreProduct||r.product===s.product)&&(!s.industry||r.industry===s.industry)&&(!s.region||r.region===s.region)&&(!s.type||ignoreType||r.type===s.type)&&(!s.bands.length||ignoreBands||s.bands.includes(r.band))&&(ignoreSearch||!s.search||`${r.account_name} ${r.account_id}`.toLowerCase().includes(s.search.toLowerCase()));
  }
  function order(rows,sort='score'){
    return [...rows].sort((a,b)=>sort==='name'?a.account_name.localeCompare(b.account_name,undefined,{numeric:true})||a.rank-b.rank:sort==='pipeline'?b.pipeline-a.pipeline||a.rank-b.rank:a.rank-b.rank);
  }
  const filter=(rows,s)=>order(rows.filter(r=>matches(r,s)),s.sort);
  const totals=rows=>({count:rows.length,accounts:new Set(rows.map(r=>r.account_id)).size,pipeline:rows.reduce((n,r)=>n+r.pipeline,0),modern:rows.filter(r=>r.type==='Modernization').length,strategic:rows.filter(r=>r.score>=55).length});
  function csv(rows){
    const fields=['account_id','account_name','product','industry','region','deployment','type','score','band','pipeline','open_count','rank'];
    const quote=v=>'"'+String(v??'').replace(/^[=+@\-\t\r]/,"'$&").replaceAll('"','""')+'"';
    return '\uFEFF'+[fields,...rows.map(r=>fields.map(k=>r[k]))].map(row=>row.map(quote).join(',')).join('\r\n');
  }
  const initialState=()=>({scope:'all',product:'',industry:'',region:'',type:'',bands:[],search:'',sort:'score'});
  root.PursuitCore={decode,matches,order,filter,totals,csv,initialState};
  if(typeof module!=='undefined') module.exports=root.PursuitCore;
})(globalThis);
