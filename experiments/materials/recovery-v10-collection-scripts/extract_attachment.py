"""Extract a bounded source-only attachment into an isolated evidence directory; execute nothing."""
import json,hashlib,sys
from pathlib import Path,PurePosixPath
import py7zr
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT))
from scripts.prepare_privacy_issue_discussions import write_json
AUDIT=ROOT/'experiments/materials/evidence-20261106-v10-recovery'
LINK=ROOT/'dataset/personal_data_protection_github/source/linked_artifacts_20261106_v10'
a=next(x for x in json.loads((AUDIT/'attempts.json').read_text()) if x['kind']=='binary' and x['status']=='downloaded');f=ROOT/a['raw']['file'];dest=AUDIT/'attachment_sources';dest.mkdir(exist_ok=True)
with py7zr.SevenZipFile(f) as z:
 entries=z.list();assert len(entries)<200 and sum(e.uncompressed for e in entries)<5_000_000
 assert all(not PurePosixPath(e.filename).is_absolute() and '..' not in PurePosixPath(e.filename).parts and '\\' not in e.filename for e in entries)
 assert all(not e.is_symlink for e in entries)
 z.extractall(path=dest)
files=[];chunks=[]
for p in sorted(dest.rglob('*')):
 if p.is_file():
  assert p.resolve().is_relative_to(dest.resolve()) and not p.is_symlink()
  data=p.read_bytes();text=data.decode('utf-8');assert '\x00' not in text
  name=str(p.relative_to(dest));files.append({'path':name,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()});chunks.append(f'\nFILE: {name}\n'+text)
url=a['url'];cache=LINK/'results'/(hashlib.sha256(url.encode()).hexdigest()+'.json');old=json.loads(cache.read_text())
text='Source attachment inventory: '+json.dumps(files,ensure_ascii=False)+'\n'+'\n'.join(chunks)
old.update(status='partial',text=text,retrieval_url=a['raw']['final_url'],fetched_at=a['raw']['fetched_at'],source_sha256=hashlib.sha256(text.encode()).hexdigest(),attachment_sha256=a['raw']['sha256'],attachment_file=a['raw']['file'],attachment_members=files,recovery_method='Downloaded original cited 7z; validated paths, links and total size; extracted UTF-8 source without executing any content',reason='All 53 source files from the cited attachment are preserved. The branch is mutable and case-time identity is unknown. Agent display may excerpt this large bundle; request specific files when needed.')
assert len(files)==53
write_json(cache,old);write_json(AUDIT/'attachment_audit.json',{'url':url,'archive':a['raw'],'file_count':len(files),'files':files,'executed':False,'status':'partial'})
print('Source attachment recovered:',len(files),'files;',sum(x['bytes'] for x in files),'bytes')
