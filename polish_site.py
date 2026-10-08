from pathlib import Path
p=Path('towell-quality/dist/app.js');s=p.read_text(encoding='utf8')
s=s.replace('r[IDX[k]]).filter(Boolean)',"(r[IDX[k]]||'__missing__'))")
s=s.replace("const selected=filters[k]||'';preceding[k]=selected;","if(k!=='period'&&filters[k]&&!opts.includes(filters[k]))delete filters[k];const selected=filters[k]||'';preceding[k]=selected;")
s=s.replace('monthLabel(o):o)',"monthLabel(o):o==='__missing__'?'Sin dato':o)")
s=s.replace('escape(n)}<',"escape(n||'Sin dato')}<")
s=s.replace('origin:\'','origin:\'')
p.write_text(s,encoding='utf8')
c=Path('towell-quality/dist/styles.css');c.write_text(c.read_text(encoding='utf8')+'\n.sr-only{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap}\n',encoding='utf8')
