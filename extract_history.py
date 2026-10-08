import openpyxl,json,datetime,pathlib,hashlib,collections,warnings
warnings.filterwarnings('ignore',category=UserWarning)
source=pathlib.Path(r'C:\Users\gcalidad\OneDrive - Towell\Documentos\AX\Segundas 2026.xlsx')
out=pathlib.Path('towell-quality/dist');out.mkdir(parents=True,exist_ok=True)
w=openpyxl.load_workbook(source,read_only=True,data_only=True)
def text(v): return '' if v is None else str(v).strip()
def date(v): return v.strftime('%Y-%m-%d') if isinstance(v,datetime.datetime) else None
def num(v): return float(v) if isinstance(v,(float,int)) else 0
columns=['date','model','size','color','defect','qty','origin','code','reference','row','turn','locality','salon','type']
def record(d,model,size,color,defect,qty,origin,code,ref,row,turn='',locality='',salon='',typ=''):
 return [d,text(model),text(size),text(color),text(defect),qty,origin,text(code),text(ref),row,text(turn),text(locality),text(salon),text(typ)]
datasets={};audit={};monthly=collections.defaultdict(lambda:collections.defaultdict(float))
for name in ['SEGUNDAS','Tipo de Segundas Costura','COSTURA','MAQUILA','Segundas Crudo','%Segundas']:
 records=[]; stats=collections.Counter(); invalid=[]; choices=collections.defaultdict(float)
 for i,r in enumerate(w[name].iter_rows(values_only=True),1):
  if name in ['SEGUNDAS','Tipo de Segundas Costura']:
   d=date(r[5]);q=num(r[15])
   if d: records.append(record(d,r[7],r[9],r[11],r[4],q,'SEGUNDAS_COSTURA',r[6],str(r[1])+' / '+text(r[2]),i,typ=r[0]))
  elif name=='COSTURA':
   d=date(r[0]);q=num(r[11])
   if d:
    records.append(record(d,r[2],r[4],r[6],'',q,'COSTURA',r[1],r[10],i,locality=r[9]))
    monthly[d[:7]]['costura_all']+=q
    monthly[d[:7]]['costura_'+text(r[9])]+=q
  elif name=='MAQUILA':
   d=date(r[1]);q=num(r[12])
   if d:
    records.append(record(d,r[3],r[5],r[7],'',q,'MAQUILA',r[2],r[11],i,locality=r[25]))
    monthly[d[:7]]['maquila_consumo']+=abs(num(r[26]));monthly[d[:7]]['maquila_invent']+=num(r[12])
  elif name=='Segundas Crudo':
   d=date(r[1]);q=num(r[29])
   if d: records.append(record(d,r[4],r[6],r[8],r[30],q,'SEGUNDAS_CRUDO',r[3],r[13],i,r[27],r[11],r[12]))
  else:
   d=date(r[0]);q=num(r[6])
   if d: records.append(record(d,r[3],r[4],r[5],'',q,'EXCEL_CONSOLIDADO',r[2],'',i,typ=r[1]))
 for r in records:
  stats['records']+=1;stats['quantity']+=r[5]
  if name=='SEGUNDAS':monthly[r[0][:7]]['segundas']+=r[5]
  if name=='%Segundas':monthly[r[0][:7]]['excel_production']+=r[5]
 same=collections.Counter(tuple(r[:9]+r[10:]) for r in records)
 stats['identical_content_extra_rows']=sum(n-1 for n in same.values() if n>1)
 audit[name]={'records':len(records),'quantity':sum(r[5] for r in records),'identical_content_extra_rows':stats['identical_content_extra_rows'],'min_date':min((r[0] for r in records),default=None),'max_date':max((r[0] for r in records),default=None)}
 datasets[name]=records
 print(name,json.dumps(audit[name]))
print('MONTHLY',json.dumps(monthly))
identical=datasets['SEGUNDAS']==datasets['Tipo de Segundas Costura']
print('MIRROR_IDENTICAL',identical)
audit['mirror_identical']=identical
audit['monthly']=monthly
def grouped(rows):
 g=collections.defaultdict(float)
 for r in rows:
  if r[0].startswith('2026-09'):g[tuple(r[:4])]+=r[5]
 return g
actual=grouped(datasets['COSTURA']+datasets['MAQUILA']);reference=grouped(datasets['%Segundas'])
differences=[{'dimensions':k,'raw':actual.get(k,0),'excel':reference.get(k,0)} for k in actual.keys()|reference.keys() if abs(actual.get(k,0)-reference.get(k,0))>1e-9]
audit['reconciliation']={'month':'2026-09','production_excel':1000316,'seconds_excel':26686,'rate_excel':0.02667756988791542,'production_raw':sum(actual.values()),'dimension_groups_different':len(differences),'difference_examples':differences[:8]}
print('RECONCILIATION',json.dumps(audit['reconciliation'],ensure_ascii=True))
audit['source']={'name':source.name,'sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'bytes':source.stat().st_size}
pathlib.Path('historical-audit.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2),encoding='utf-8')
# Dictionary encoding preserves all source rows and repeated observations.
for name,key in [('SEGUNDAS','seconds'),('COSTURA','costura'),('MAQUILA','maquila'),('Segundas Crudo','crudo'),('%Segundas','reference')]:
 dictionaries={str(i):[] for i in [1,2,3,4,6,7,8,10,11,12,13]};maps={i:{} for i in dictionaries};data=[]
 for r in datasets[name]:
  copy=r.copy()
  for ii,dictionary in dictionaries.items():
   i=int(ii);value=r[i]
   if value not in maps[ii]:maps[ii][value]=len(dictionary);dictionary.append(value)
   copy[i]=maps[ii][value]
  data.append(copy)
 (out/(key+'.json')).write_text(json.dumps({'columns':columns,'dict':dictionaries,'rows':data},ensure_ascii=False,separators=(',',':')),encoding='utf-8')
(out/'audit.json').write_text(json.dumps(audit,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
