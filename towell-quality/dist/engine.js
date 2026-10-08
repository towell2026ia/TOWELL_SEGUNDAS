export const DEPARTMENTS=['TEJIDO','TINTORERÍA','COSTURA','SIN CLASIFICAR'];
// Full catalogue defined by the user in "Dashboard de segundas costura".
// Eight additional historical names assigned explicitly by the user on 2026-10-06.
export const CATALOGUE={
 'Rayas':'TEJIDO',
 'Subida a Rizo por Orilla corta':'TEJIDO',
 'Error de medida / Retazo':'TEJIDO',
 'Hilo Faltante':'TEJIDO',
 'Marra':'TEJIDO',
 'Trama Rota':'TEJIDO',
 'Oalla con Plano / Sin Rizo / Sin Plano de corte':'TEJIDO',
 'Grasa / Aceite Telar':'TEJIDO',
 'Rizo Escurrido':'TEJIDO',
 'Toalla sin Plano':'TEJIDO',
 'Rota Tejido':'TEJIDO',
 'Metida de Mano':'TEJIDO',
 'Mancha de Óxido':'TEJIDO',
 'Mezcla de Hilatura':'TEJIDO',
 'Hilos Mal Tejidos Rizo':'TEJIDO',
 'Error de Trama':'TEJIDO',
 'Hilos Mal Tejidos Pie / Plano':'TEJIDO',
 'Error de Dibujo':'TEJIDO',
 'Orilla Deshilada':'TEJIDO',
 'Defecto de Teñido':'TINTORERÍA',
 'Rizo Maltratado':'TINTORERÍA',
 'Rizo Jalado':'TINTORERÍA',
 'Rota Tintorería':'TINTORERÍA',
 'Defecto de Secado':'TINTORERÍA',
 'Subida a Rizo Costura Longitudinal':'COSTURA',
 'Subida a Rizo por mal corte':'COSTURA',
 'Rota Costura':'COSTURA',
 'Subida a Rizo Costura Transversal':'COSTURA',
 'Rota':'TINTORERÍA',
 'Defectos de Estampado':'COSTURA',
 'Mancha Acabado':'COSTURA',
 'Segunda Global':'TINTORERÍA',
 'Rizo Salpicado':'TEJIDO',
 'Rollos Invertidos':'TEJIDO',
 'Error de Peso':'TEJIDO',
 'Gasa de vuelta suelta':'TEJIDO'
};
export const LIMITS={GLOBAL:1.6,TEJIDO:1,'TINTORERÍA':.3,COSTURA:.3};
export const IDX={model:1,size:2,color:3,defect:4,turn:10,locality:11,salon:12};
export function normalize(s){return String(s).normalize('NFD').replace(/[\u0300-\u036f]/g,'').trim().replace(/\s*\/\s*/g,'/').replace(/\s+/g,' ').toUpperCase();}
const departmentCache=new Map(Object.entries(CATALOGUE).map(([d,p])=>[normalize(d),p]));
export function department(r){return departmentCache.get(normalize(r[4]))||'SIN CLASIFICAR';}
export function decode(payload){return payload.rows.map(row=>{const r=row.slice();for(const [i,dict]of Object.entries(payload.dict))r[+i]=dict[r[+i]];return r;});}
export const sum=rows=>rows.reduce((n,r)=>n+r[5],0);
export function ratio(n,d){return d>0?n/d*100:null;}
export function inPeriod(r,period){if(!period||period==='all')return true;if(period.includes('..')){const[start,end]=period.split('..');const month=r[0].slice(0,7);return month>=start&&month<=end;}return r[0].startsWith(period);}
export function matches(r,f,production=false){if(!inPeriod(r,f.period))return false;for(const[k,i]of Object.entries(IDX)){if(production&&!['model','size','color'].includes(k))continue;if(f[k]&&r[i]!== (f[k]==='__missing__'?'':f[k]))return false;}return production||!f.department||department(r)===f.department;}
export const select=(rows,filters,production=false)=>rows.filter(r=>matches(r,filters,production));
export function group(rows,index){const m=new Map();for(const r of rows){const k=typeof index==='function'?index(r):r[index];m.set(k,(m.get(k)||0)+r[5]);}return [...m].sort((a,b)=>b[1]-a[1]);}
export function previousMonth(period){if(!/^\d{4}-\d{2}$/.test(period||''))return null;const d=new Date(period+'-01T12:00:00Z');d.setUTCMonth(d.getUTCMonth()-1);return d.toISOString().slice(0,7);}
export function week(date){const d=new Date(date+'T12:00:00Z');d.setUTCDate(d.getUTCDate()-((d.getUTCDay()+6)%7));return d.toISOString().slice(0,10);}
export function bucket(date,granularity){return granularity==='month'?date.slice(0,7):granularity==='week'?week(date):date;}
export function getMetrics(seconds,production,f){const rows=select(seconds,f),p=select(production,f,true),total=sum(rows),den=sum(p);const byDepartment=Object.fromEntries(DEPARTMENTS.map(d=>[d,sum(rows.filter(r=>department(r)===d))]));return {rows,production:p,total,den,rate:ratio(total,den),byDepartment,costura:sum(p.filter(r=>r[6]==='COSTURA')),maquila:sum(p.filter(r=>r[6]==='MAQUILA'))};}
export function getTrend(rows,production,granularity,crudo=false){const a=new Map(group(rows,r=>bucket(r[0],granularity)));const b=new Map(group(production,r=>bucket(r[0],granularity)));return [...new Set([...a.keys(),...b.keys()])].sort().map(k=>({date:k,qty:a.get(k)||0,den:b.get(k)||0,value:crudo?a.get(k)||0:ratio(a.get(k)||0,b.get(k)||0)}));}
export function modelRates(rows,production){const p=new Map(group(production,1));return group(rows,1).map(([name,qty])=>({name,qty,den:p.get(name)||0,rate:ratio(qty,p.get(name)||0)}));}
export function alertRules(current,previous,{crudo=false,target=1.6,label='GLOBAL',trend=[]}={}){
 const alerts=[];
 if(!crudo&&current.rate!==null&&current.rate>target)alerts.push({kind:'danger',title:'LÍMITE · '+label,text:`El indicador alcanza ${current.rate.toFixed(2)}%, superior al máximo de ${target.toFixed(2)}%.`});
 if(!crudo&&label==='GLOBAL')for(const d of DEPARTMENTS.slice(0,3)){const p=ratio(current.byDepartment[d],current.den);if(p!==null&&p>LIMITS[d])alerts.push({kind:'danger',title:'LÍMITE · '+d,text:`El indicador alcanza ${p.toFixed(2)}%, superior al máximo de ${LIMITS[d].toFixed(2)}%.`});}
 if(!crudo&&current.byDepartment?.['SIN CLASIFICAR']>0)alerts.push({kind:'info',title:'CATÁLOGO · DEPARTAMENTO PENDIENTE',text:`${current.byDepartment['SIN CLASIFICAR']} segundas tienen un defecto identificado que aún no tiene asignación en el catálogo departamental del Site. Están incluidas en Global.`});
 const valid=trend.filter(x=>x.value!==null);const last=valid.slice(-3);
 if(last.length===3&&last[0].value<last[1].value&&last[1].value<last[2].value)alerts.push({kind:'warning',title:'TENDENCIA · '+label,text:`El indicador aumenta en los tres últimos periodos con datos: ${last.map(x=>x.date).join(', ')}.`});
 if(previous){const prior=new Map(group(previous.rows,4));for(const[d,q]of group(current.rows,4).slice(0,6)){const p=prior.get(d)||0;if(p>0&&q>=5&&(q-p)/p>=.3)alerts.push({kind:'warning',title:'DEFECTO · '+d.toUpperCase(),text:`La cantidad aumenta ${Math.round((q-p)/p*100)}% frente al mes anterior (${p} → ${q}).`});}}
 const top=group(current.rows,1).slice(0,3);if(top.length===3&&current.total>0){const concentration=top.reduce((n,x)=>n+x[1],0)/current.total*100;if(concentration>=50)alerts.push({kind:'info',title:'CONCENTRACIÓN',text:`Tres modelos concentran ${concentration.toFixed(1)}% de la cantidad registrada: ${top.map(x=>x[0]).join(', ')}.`});}
 return alerts;
}
