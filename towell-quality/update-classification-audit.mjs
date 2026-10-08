import fs from 'node:fs';
import {decode,department,group,getMetrics,CATALOGUE} from './dist/engine.js';
const load=k=>decode(JSON.parse(fs.readFileSync(`dist/${k}.json`,'utf8')));
const seconds=load('seconds'),production=[...load('costura'),...load('maquila')],audit=JSON.parse(fs.readFileSync('dist/audit.json','utf8'));
const september=getMetrics(seconds,production,{period:'2026-09'});
const names=group(seconds,4);
audit.classification={source:'Clasificación definida por el usuario en Dashboard de segundas costura',conversation:'6ac528b2-d980-83e8-8914-962ff8cb3417',message:'40d4540e-f97d-48bf-a1b5-33f7a687421c',catalogue_count:Object.keys(CATALOGUE).length,september:september.byDepartment,defects:names.map(([name,quantity])=>({name,department:department(['','','','',name]),quantity,september_quantity:september.rows.filter(r=>r[4]===name).reduce((n,r)=>n+r[5],0)}))};
fs.writeFileSync('dist/audit.json',JSON.stringify(audit));
console.log(JSON.stringify(audit.classification.september));
