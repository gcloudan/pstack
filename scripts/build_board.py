#!/usr/bin/env python3
"""Generate a read-only adoption board; no service or model calls."""
from pathlib import Path
import json
import argparse
from datetime import datetime, timezone

root = Path(__file__).resolve().parent.parent
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output', type=Path, default=root / 'board/index.html')
args = parser.parse_args()
adoption = json.loads((root / 'adoption.json').read_text())
snapshot = json.loads((root / 'upstream/snapshot.json').read_text())
receipt_path = root / 'adapters/hermes/installation.local.json'
receipt = json.loads(receipt_path.read_text()) if receipt_path.exists() else {}
data = {'adoption': adoption, 'receipt': receipt, 'source_count': len(snapshot['files_sha256']),
        'commit': snapshot['commit'], 'generated': datetime.now(timezone.utc).isoformat()}
payload = json.dumps(data).replace('<', '\\u003c')
html = '''<!doctype html>
<html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Pstack adoption board</title>
<style>
:root{font-family:system-ui,sans-serif;color:#e5edf8;background:#101826}body{max-width:1150px;margin:40px auto;padding:0 24px}h1{font-size:32px;margin-bottom:8px}p{color:#b6c4d9;line-height:1.6}.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:14px;margin:25px 0}.card,details{background:#1a2639;border:1px solid #344760;border-radius:12px;padding:18px}.number{font-size:30px;color:#76e0bb}.label{font-size:14px;color:#c1cce0}.flow{padding:18px;background:#182e30;border-left:4px solid #76e0bb;line-height:1.7}input,select{padding:12px;border-radius:8px;border:1px solid #52657d;background:#182538;color:white;margin:18px 10px 18px 0}input{width:min(450px,85%)}details{margin:10px 0}summary{cursor:pointer;display:flex;justify-content:space-between;gap:14px;flex-wrap:wrap}.badge{font-size:13px;color:#76e0bb}.meta{font-size:13px;color:#99acc7}a{color:#83c8ff}code{color:#cae7ff}#evidence{background:#1a2639;padding:18px;border-radius:10px}button{background:#28425c;color:white;padding:10px;border:0;border-radius:6px;cursor:pointer}
</style>
<h1>Your pstack adoption board</h1>
<p>Whole source preserved. Useful methods adopted separately for Cursor and Hermes.</p>
<div class="cards" id="cards"></div>
<div class="flow">Question → existing compatible recipe → trace directly or delegate distinct responsibilities → parent checks evidence → one answer.<br>Next adoption: compare → adapt → exercise → record → install.</div>
<h2>Hermes checkpoint</h2><div id="evidence"></div>
<h2>Feature ledger</h2><p>“Adapted” below refers to the main Cursor layer. The Hermes badge identifies its separately installed methods. Preserved source is available for review, not active behavior.</p>
<label>Search <input id="search" placeholder="how, swarm, verification…"></label>
<label>Filter <select id="filter"><option value="all">All features</option><option value="adapted">Adapted in main layer</option><option value="hermes">Installed on Hermes</option><option value="preserved">Preserved only</option></select></label>
<div id="count" class="meta"></div><div id="features"></div>
<p class="meta" id="stamp"></p>
<script id="data" type="application/json">PAYLOAD</script>
<script>
const d=JSON.parse(document.getElementById('data').textContent);
const installed=new Set(d.receipt.installed_skills||[]);
const hermesMap={how:'pstack-how',swarm:'pstack-swarm','blast-radius':'pstack-impact'};
function el(tag,text,cls){const n=document.createElement(tag);n.textContent=text;if(cls)n.className=cls;return n}
const cards=[['Source files',d.source_count],['Recorded features',d.adoption.features.length],['Hermes skills installed',installed.size],['Live model trial',d.receipt.live_model_task_observed?'Observed':'Unobserved']];
for(const [label,value] of cards){const c=el('div','','card');c.append(el('div',String(value),'number'),el('div',label,'label'));document.getElementById('cards').append(c)}
const e=document.getElementById('evidence');
e.append(el('p',installed.size?`Native loader verified: ${d.receipt.loader_verified?'yes':'not verified'}. Catalog ${d.receipt.before_count} → ${d.receipt.after_count}; existing names retained: ${d.receipt.existing_catalog_preserved?'yes':'unverified'}.`:'No host installation receipt loaded.'));
e.append(el('p','Fresh sessions can discover installed skills. Current conversations may retain their cached catalog. This board is a generated receipt, not live agent activity.'));
e.append(el('p','Try in Hermes: “Load pstack-how and explain how this subsystem works. Use pstack-swarm only if distinct investigations improve coverage.”'));
if(installed.has('pstack-adopt'))e.append(el('p','Also installed: pstack-adopt, the feature-by-feature adoption workflow.'));
function render(){const q=document.getElementById('search').value.toLowerCase();const filter=document.getElementById('filter').value;const out=document.getElementById('features');out.replaceChildren();let count=0;
for(const f of d.adoption.features){const onHermes=installed.has(hermesMap[f.id]);const adapted=f.status.includes('adapted');if(q&&!JSON.stringify(f).toLowerCase().includes(q))continue;if(filter==='hermes'&&!onHermes)continue;if(filter==='adapted'&&!adapted)continue;if(filter==='preserved'&&f.status!=='preserved')continue;count++;const row=el('details','');const summary=el('summary','');summary.append(el('strong',f.id),el('span',f.status+(onHermes?' · Hermes installed':''),'badge'));row.append(summary,el('p',f.decision),el('p',f.kind+' · '+f.source,'meta'));if(f.adapted_skills?.length)row.append(el('p','Main layer: '+f.adapted_skills.join(', ')));out.append(row)}document.getElementById('count').textContent=count+' features shown'}
document.getElementById('search').addEventListener('input',render);document.getElementById('filter').addEventListener('change',render);render();
document.getElementById('stamp').textContent='Generated '+d.generated+' · upstream '+d.commit.slice(0,12)+'. Refresh by rerunning scripts/build_board.py on Hermes.';
</script></html>'''
args.output.parent.mkdir(parents=True, exist_ok=True)
args.output.write_text(html.replace('PAYLOAD', payload), encoding='utf-8')
print(args.output)
