from pathlib import Path
import tarfile,json,hashlib,subprocess
project=Path('towell-quality').resolve()
stage=project/'.sites-runtime/package-stage/dist'
archive=Path('towell-quality.tar.gz').resolve()
assert stage.is_relative_to(project)
assert (stage/'index.html').is_file()
config=json.loads((stage/'.openai/hosting.json').read_text(encoding='utf8'))
assert config['project_id']=='appgprj_6ac539ef3ed081919bf0a98c6c00968f'
assert config['static']['directory']=='dist' and config['d1'] is None and config['r2'] is None
for f in (project/'dist').rglob('*'):
 if f.is_file():assert hashlib.sha256(f.read_bytes()).digest()==hashlib.sha256((stage/f.relative_to(project/'dist')).read_bytes()).digest()
with tarfile.open(archive,'w:gz',format=tarfile.PAX_FORMAT) as tar:tar.add(stage,arcname='dist')
with tarfile.open(archive,'r:gz') as tar:
 names=tar.getnames()
 assert 'dist/.openai/hosting.json' in names and 'dist/index.html' in names
 assert all(not n.startswith('/') and '..' not in Path(n).parts for n in names)
 assert all(not m.issym() and not m.islnk() for m in tar.getmembers())
print(json.dumps({'archive':str(archive),'files':len(names),'bytes':archive.stat().st_size,'validation':'manifest, static assets, exact source hashes, safe paths'}))
