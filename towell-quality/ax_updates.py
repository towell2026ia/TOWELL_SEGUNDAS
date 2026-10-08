"""Append-only AX HTML updates. No credentials; original inputs are read-only."""
import argparse, collections, datetime, hashlib, json, re, unicodedata
from html.parser import HTMLParser
from pathlib import Path

ROOT=Path(__file__).resolve().parent
FOLDER=Path(r'C:\Users\gcalidad\OneDrive - Towell\Documentos\AX')
STATE=ROOT/'updates'/'state.json'
KEYS={'COSTURA':'costura','MAQUILA':'maquila','SEGUNDAS_COSTURA':'seconds','SEGUNDAS_CRUDO':'crudo'}
def norm(s):return re.sub(r'\s+',' ',''.join(c for c in unicodedata.normalize('NFD',str(s)) if unicodedata.category(c)!='Mn').strip().lower())
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def save(p,v):
 p.parent.mkdir(parents=True,exist_ok=True)
 tmp=p.with_suffix(p.suffix+'.tmp');tmp.write_text(json.dumps(v,ensure_ascii=False,separators=(',',':')),encoding='utf-8');tmp.replace(p)
class Rows(HTMLParser):
 def __init__(self):super().__init__();self.rows=[];self.row=None;self.cell=None
 def handle_starttag(self,tag,attrs):
  if tag=='tr':self.row=[]
  elif tag in ('td','th') and self.row is not None:self.cell=[]
  elif tag=='br' and self.cell is not None:self.cell.append(' ')
 def handle_data(self,data):
  if self.cell is not None:self.cell.append(data)
 def handle_endtag(self,tag):
  if tag in ('td','th') and self.cell is not None:
   self.row.append(re.sub(r'\s+',' ',''.join(self.cell)).strip());self.cell=None
  elif tag=='tr' and self.row is not None:self.rows.append(self.row);self.row=None
def text(p):
 b=p.read_bytes()
 for enc in ('utf-8-sig','cp1252'):
  try:return b.decode(enc)
  except UnicodeDecodeError:pass
 raise ValueError('Codificación no reconocida')
def field(headers,*aliases,last=False,required=False):
 hits=[]
 for alias in aliases:
  hits=[i for i,s in enumerate(headers) if norm(s)==norm(alias)]
  if hits:break
 if not hits:
  if required:raise ValueError('Falta columna: '+aliases[0])
  return None
 return hits[-1] if last else hits[0]
def number(s):
 s=s.strip().replace(' ','')
 if not re.fullmatch(r'-?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?',s):raise ValueError('Cantidad no válida o separador ambiguo: '+s)
 return float(s.replace(',',''))
def day(s):
 for fmt in ('%d/%m/%Y','%d-%m-%Y','%Y-%m-%d'):
  try:return datetime.datetime.strptime(s,fmt).date().isoformat()
  except ValueError:pass
 raise ValueError('Fecha no válida: '+s)
def parse(p):
 source=text(p)
 if 'Microsoft Dynamics' not in source:raise ValueError('No es un HTML AX reconocido')
 parser=Rows();parser.feed(source)
 header_index=next((i for i,r in enumerate(parser.rows) if field(r,'Fecha') is not None and field(r,'Nombre del artículo','Modelo','Nombre de artículo') is not None),None)
 if header_index is None:
  # AX emits generic empty reports without any identifying header or title.
  if len(parser.rows)<=5 and 'Informe autom' in source:return {'type':'AX_SIN_MOVIMIENTOS','rows':[],'headers':[]}
  raise ValueError('Estructura desconocida: auditar columnas antes de incorporar')
 h=parser.rows[header_index]
 defect=field(h,'Defecto','Tipo de segunda','Tipo de segundas','Nombre del tipo de segunda','Descripción tipo de segunda','Tipo de defecto')
 inv=field(h,'InventQty');bom=field(h,'BomQty');turn=field(h,'Turno');salon=field(h,'Salón','Salon')
 if inv is not None and bom is not None and defect is None:typ='MAQUILA';qty=inv
 elif defect is not None and turn is not None and salon is not None:typ='SEGUNDAS_CRUDO';qty=field(h,'Cantidad',required=True)
 elif defect is not None:typ='SEGUNDAS_COSTURA';qty=field(h,'Cantidad',required=True)
 elif inv is None and field(h,'Cantidad') is not None:typ='COSTURA';qty=field(h,'Cantidad',required=True)
 else:raise ValueError('No se puede identificar el informe por su estructura')
 cols=[field(h,'Fecha',required=True),field(h,'Nombre del artículo','Nombre de artículo','Modelo',required=True),field(h,'Tamaño'),field(h,'Nombre del color','Color nombre','Nombre'),defect,qty,None,field(h,'Código de artículo','Codigo de articulo','Código','Artículo'),field(h,'Número de serie','Registro','Identificador','Producción'),None,turn,field(h,'Localidad','Localidad / Telar','Telar',last=typ=='MAQUILA'),salon,None]
 if cols[3] is None:cols[3]=field(h,'Color')
 records=[]
 for rownum,r in enumerate(parser.rows[header_index+1:],header_index+2):
  if r==h or len(r)<=cols[0] or not r[cols[0]]:continue
  if norm(r[cols[0]])=='fecha' or norm(r[cols[0]]).startswith('total'):continue
  if len(r)!=len(h):raise ValueError('Fila incompleta: '+str(rownum))
  out=[r[i] if i is not None else '' for i in cols]
  out[0]=day(out[0]);out[5]=number(out[5]);out[6]=typ;out[9]=rownum
  if out[5]<0:raise ValueError('Reverso/ajuste negativo pendiente de validación: '+str(rownum))
  if not out[1] or (defect is not None and not out[4]):raise ValueError('Modelo o defecto ausente: '+str(rownum))
  if typ=='MAQUILA':
   warehouse=field(h,'Almacén',required=True)
   if r[warehouse]!='A-RECEPMAQ':raise ValueError('Movimiento de Maquila distinto del origen A-RECEPMAQ validado')
  out.extend([p.name,typ]);records.append(out)
 return {'type':typ,'headers':h,'rows':records}
def decode(v):
 rows=[]
 for r in v['rows']:
  r=r.copy()
  for i,d in v['dict'].items():r[int(i)]=d[r[int(i)]]
  rows.append(r)
 return rows
def encode(v,rows):
 dictionaries={str(i):[] for i in [1,2,3,4,6,7,8,10,11,12,13,14,15]};maps={i:{} for i in dictionaries};out=[]
 for row in rows:
  r=row.copy()+['']*max(0,16-len(row))
  for s,d in dictionaries.items():
   i=int(s);val=r[i]
   if val not in maps[s]:maps[s][val]=len(d);d.append(val)
   r[i]=maps[s][val]
  out.append(r)
 return {'columns':v['columns'][:14]+['source_file','source_type'],'dict':dictionaries,'rows':out}
def fingerprint(r):return json.dumps(r[:9]+r[10:14],ensure_ascii=False,separators=(',',':'))
def incorporate(existing,incoming):
 known=collections.Counter(fingerprint(r) for r in existing);seen=collections.Counter();new=[];duplicates=0
 cutoff=max((x[0] for x in existing if len(x)<=14 or not x[14]),default='')
 stable={ (r[6],r[8]):fingerprint(r) for r in existing if r[8] and r[6]=='MAQUILA'}
 for r in incoming:
  f=fingerprint(r);seen[f]+=1
  if r[6]=='MAQUILA' and r[8] and (r[6],r[8]) in stable:
   if stable[(r[6],r[8])]!=f:raise ValueError('Identificador existente con contenido diferente; sustitución explícita requerida')
   duplicates+=1;continue
  if seen[f]<=known[f]:duplicates+=1
  else:
   if r[0]<=cutoff:raise ValueError('Movimiento no conciliado dentro de un periodo histórico validado; revisar antes de incorporar: '+r[0])
   new.append(r)
   if r[6]=='MAQUILA' and r[8]:stable[(r[6],r[8])]=f
 return new,duplicates
def scan(state):
 found=[]
 for p in sorted(FOLDER.iterdir()):
  if p.is_file() and p.suffix.lower() in ('.htm','.html'):
   sha=digest(p)
   if state.get('files',{}).get(str(p))!=sha:found.append({'path':str(p),'sha256':sha,'bytes':p.stat().st_size})
 return found
def main():
 cli=argparse.ArgumentParser();cli.add_argument('mode',choices=['initialize','scan','plan','apply','ack','verify']);args=cli.parse_args()
 state=read(STATE) if STATE.exists() else {'files':{},'loads':[]}
 if args.mode=='initialize':
  if STATE.exists():raise ValueError('El seguimiento ya está inicializado')
  state['files']={str(p):digest(p) for p in FOLDER.iterdir() if p.is_file() and p.suffix.lower() in ('.htm','.html')}
  state['baseline_datasets']={}
  for key in KEYS.values():
   rows=decode(read(ROOT/'dist'/f'{key}.json'))
   prefix=json.dumps([r[:14] for r in rows],ensure_ascii=False,separators=(',',':')).encode()
   state['baseline_datasets'][key]={'rows':len(rows),'sha256':hashlib.sha256(prefix).hexdigest()}
  state['started_at']=datetime.datetime.now(datetime.timezone.utc).isoformat();state['baseline']='Informes presentes al activar el seguimiento; no incorporados al histórico';save(STATE,state);print(json.dumps({'baseline_files':len(state['files']),'new_records':0}));return
 if args.mode=='verify':
  assert state.get('baseline_datasets'),'Falta el control del histórico inicial'
  for key,control in state['baseline_datasets'].items():
   rows=decode(read(ROOT/'dist'/f'{key}.json'))
   assert len(rows)>=control['rows'],'El histórico perdió registros'
   prefix=json.dumps([r[:14] for r in rows[:control['rows']]],ensure_ascii=False,separators=(',',':')).encode()
   assert hashlib.sha256(prefix).hexdigest()==control['sha256'],'El histórico validado fue alterado: '+key
  print(json.dumps({'baseline':'INTACTO'}));return
 changed=scan(state)
 if args.mode=='scan':print(json.dumps({'changed':changed},ensure_ascii=False));return
 if args.mode=='ack':
  pending=read(ROOT/'updates'/'pending.json')
  for load in pending['loads']:
   p=Path(load['path'])
   archived=ROOT/'updates'/'sources'/(load['sha256']+'.htm')
   if not archived.exists() or digest(archived)!=load['sha256']:raise ValueError('La fuente archivada de la publicación no coincide')
   state['files'][str(p)]=load['sha256'];state['loads'].append(load)
  save(STATE,state);print(json.dumps({'acknowledged':len(pending['loads'])}));return
 if (ROOT/'updates'/'pending.json').exists():
  pending=read(ROOT/'updates'/'pending.json')
  if any(state['files'].get(l['path'])!=l['sha256'] for l in pending['loads']):raise ValueError('Existe una actualización pendiente de publicación: completar o recuperar antes de importar más')
 datasets={k:read(ROOT/'dist'/f'{k}.json') for k in KEYS.values()};allrows={k:decode(v) for k,v in datasets.items()};loads=[]
 for change in changed:
  p=Path(change['path']);report=parse(p);typ=report['type'];new=[];duplicates=0
  if digest(p)!=change['sha256']:raise ValueError('El informe cambió durante la lectura; reintentar cuando OneDrive termine de sincronizar')
  if report['rows']:
   key=KEYS[typ];new,duplicates=incorporate(allrows[key],report['rows']);allrows[key].extend(new)
  loads.append({**change,'type':typ,'records':len(report['rows']),'new':len(new),'duplicates':duplicates,'status':'VALIDADO – SIN MOVIMIENTOS' if not report['rows'] else 'VALIDADO','period_start':min((r[0] for r in report['rows']),default=None),'period_end':max((r[0] for r in report['rows']),default=None)})
 result={'loads':loads,'new_records':sum(l['new'] for l in loads)}
 if args.mode=='apply' and loads:
  backup=ROOT/'updates'/'backup'/datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%f')
  result['backup']=str(backup)
  for key in {KEYS[l['type']] for l in loads if l['new']}:
   save(backup/f'{key}.json',datasets[key])
  for load in loads:
   archived=ROOT/'updates'/'sources'/(load['sha256']+'.htm');archived.parent.mkdir(parents=True,exist_ok=True);archived.write_bytes(Path(load['path']).read_bytes())
   if digest(archived)!=load['sha256']:raise ValueError('El informe cambió antes de archivar; no se incorporaron movimientos')
  save(ROOT/'updates'/'pending.json',result)
  for key in {KEYS[l['type']] for l in loads if l['new']}:
   save(ROOT/'dist'/f'{key}.json',encode(datasets[key],allrows[key]))
 print(json.dumps(result,ensure_ascii=False))
if __name__=='__main__':main()
