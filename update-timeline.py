from pathlib import Path
p=Path('towell-quality/dist')
app=(p/'app.js').read_text(encoding='utf-8')
app=app.replace("const monthLabel=s=>s==='all'?'Todo el histórico':new Date(s+'-01T12:00:00Z').toLocaleDateString('es-MX',{month:'long',year:'numeric',timeZone:'UTC'});", "const monthLabel=s=>!s||s==='all'?'Todo el histórico':s.includes('..')?s.split('..').map(monthLabel).join(' – '):new Date(s+'-01T12:00:00Z').toLocaleDateString('es-MX',{month:'long',year:'numeric',timeZone:'UTC'});")
start=app.index('function filterUi()')
end=app.index('function kpi(',start)
app=app[:start]+'''function setPeriod(period){filters={period};granularity=period==='all'||period.includes('..')?'month':'day';page=0;render();}
function timelineUi(){
 const months=[...new Set(allBase().map(r=>r[0].slice(0,7)))].sort();
 const bounds=filters.period==='all'?[months[0],months.at(-1)]:filters.period.split('..');
 const from=Math.max(0,months.indexOf(bounds[0])),to=Math.max(from,months.indexOf(bounds[1]||bounds[0]));
 return `<div class="timeline"><div class="timeline-heading"><div><span class="timeline-label">Periodo</span><strong id="timeline-selection">${escape(monthLabel(filters.period))}</strong></div><button type="button" class="button timeline-all" id="timeline-all" aria-pressed="${filters.period==='all'}">Todo el histórico</button></div><div class="timeline-scroll"><div class="timeline-months" role="group" aria-label="Meses del histórico">${months.map((m,i)=>`<button type="button" data-month="${m}" class="timeline-month ${i>=from&&i<=to?'selected':''}" aria-pressed="${i>=from&&i<=to}" aria-label="${escape(monthLabel(m))}"><span>${new Date(m+'-01T12:00:00Z').toLocaleDateString('es-MX',{month:'short',timeZone:'UTC'})}</span><small>${m.slice(0,4)}</small></button>`).join('')}</div></div><div class="timeline-range"><label for="timeline-from">Desde <input id="timeline-from" type="range" min="0" max="${months.length-1}" step="1" value="${from}" aria-valuetext="${escape(monthLabel(months[from]))}"></label><label for="timeline-to">Hasta <input id="timeline-to" type="range" min="0" max="${months.length-1}" step="1" value="${to}" aria-valuetext="${escape(monthLabel(months[to]))}"></label></div></div>`;
}
function filterUi(){
 let preceding=effective({period:filters.period});
 const html=fields().filter(k=>k!=='period').map(k=>{const rows=select(allBase(),preceding),opts=[...new Set(rows.map(r=>k==='department'?department(r):(r[IDX[k]]||'__missing__')))].sort((a,b)=>a.localeCompare(b,'es'));if(filters[k]&&!opts.includes(filters[k]))delete filters[k];const selected=filters[k]||'';preceding[k]=selected;return `<div class="field"><label for="filter-${k}">${fieldLabels[k]}</label><select id="filter-${k}" data-filter="${k}"><option value="">Todos</option>${opts.map(o=>`<option value="${escape(o)}"${selected===o?' selected':''}>${escape(o==='__missing__'?'Sin dato':o)}</option>`).join('')}</select></div>`;}).join('');
 $('filters').innerHTML=timelineUi()+html+'<button class="clear" id="clear-filters">Limpiar filtros</button>';
 document.querySelectorAll('[data-filter]').forEach(el=>el.addEventListener('change',e=>{const k=e.target.dataset.filter,keys=fields(),index=keys.indexOf(k);filters[k]=e.target.value;for(const x of keys.slice(index+1))delete filters[x];page=0;render();}));
 const months=[...new Set(allBase().map(r=>r[0].slice(0,7)))].sort(),from=$('timeline-from'),to=$('timeline-to');
 const bounds=()=>{let a=+from.value,b=+to.value;return[a,b];};
 function preview(which){if(+from.value>+to.value){if(which==='from')to.value=from.value;else from.value=to.value;}const[a,b]=bounds();from.setAttribute('aria-valuetext',monthLabel(months[a]));to.setAttribute('aria-valuetext',monthLabel(months[b]));$('timeline-selection').textContent=monthLabel(a===b?months[a]:months[a]+'..'+months[b]);document.querySelectorAll('[data-month]').forEach((el,i)=>{el.classList.toggle('selected',i>=a&&i<=b);el.setAttribute('aria-pressed',String(i>=a&&i<=b));});}
 for(const [el,name]of[[from,'from'],[to,'to']]){el.addEventListener('input',()=>preview(name));el.addEventListener('change',()=>{preview(name);const[a,b]=bounds();setPeriod(a===b?months[a]:months[a]+'..'+months[b]);});}
 document.querySelectorAll('[data-month]').forEach(el=>el.addEventListener('click',e=>{const m=el.dataset.month;if(e.shiftKey&&filters.period!=='all'){const anchor=filters.period.split('..')[0];setPeriod([anchor,m].sort().join('..'));}else setPeriod(m);}));
 $('timeline-all').onclick=()=>setPeriod('all');$('clear-filters').onclick=()=>setPeriod('all');
}
''' + app[end:]
app=app.replace("$('download').hidden=isAdmin;",'')
start=app.index("$('download').onclick=")
end=app.index('async function init()',start)
app=app[:start]+app[end:]
(p/'app.js').write_text(app,encoding='utf-8')
html=(p/'index.html').read_text(encoding='utf-8')
start=html.index('<div class="private-label">');end=html.index('</header>',start)
html=html[:start]+html[end:]
start=html.index('<div class="heading-right">');end=html.index('</div></div>',start)
html=html[:start]+html[end+6:]
(p/'index.html').write_text(html,encoding='utf-8')
css='''
.timeline{flex:0 0 100%;width:100%;padding-bottom:18px;margin-bottom:2px;border-bottom:1px solid var(--line)}.timeline-heading{display:flex;align-items:center;justify-content:space-between;gap:16px;margin-bottom:16px}.timeline-heading>div{display:flex;align-items:baseline;flex-wrap:wrap;gap:16px}.timeline-label{font-size:14px;color:var(--muted);font-weight:600}.timeline-heading strong{font-size:16px;font-weight:600;color:var(--navy)}.timeline-all[aria-pressed="true"]{background:var(--navy);color:white}.timeline-scroll{overflow-x:auto;padding:3px 3px 7px}.timeline-months{display:flex;min-width:540px;border-radius:5px;background:#edf2f6;gap:3px;padding:4px}.timeline-month{flex:1;min-width:56px;min-height:55px;border:0;border-radius:3px;background:transparent;color:var(--muted);font-size:14px;padding:7px 4px}.timeline-month span{display:block;text-transform:capitalize;font-weight:600}.timeline-month small{display:block;font-size:12px}.timeline-month:hover{background:#dbe7ef;color:var(--navy)}.timeline-month.selected{background:var(--blue);color:white}.timeline-range{display:flex;gap:24px;margin-top:10px}.timeline-range label{display:flex;align-items:center;gap:12px;flex:1;font-size:14px;color:var(--muted)}.timeline-range input{width:100%;min-width:0;accent-color:var(--blue);cursor:pointer;height:24px}.timeline-range input:focus-visible{outline:3px solid #4092ce;outline-offset:3px}@media(max-width:700px){.timeline-heading{align-items:start}.timeline-heading>div{display:block}.timeline-heading strong{display:block;margin-top:5px;font-size:14px}.timeline-all{font-size:13px;white-space:nowrap}.timeline-range{gap:12px}.timeline-range label{gap:6px;font-size:13px}}
'''
with (p/'styles.css').open('a',encoding='utf-8')as f:f.write(css)
