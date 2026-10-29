from pathlib import Path
import json,re,argparse,statistics,fitz
ROOT=Path(__file__).resolve().parents[1]

def scan(pdf_path,aux_path):
    doc=fitz.open(pdf_path);aux=Path(aux_path).read_text();starts=[]
    for source in (ROOT/'chapters').glob('*.tex'):
        m=re.search(r'\\chapter\{([^}]+)\}\s*\\label\{([^}]+)\}',source.read_text())
        if not m:continue
        ref=re.search(r'\\newlabel\{'+re.escape(m[2])+r'\}\{\{[^}]*\}\{([^}]*)\}',aux)
        if not ref:continue
        number=ref[1]
        found=[i for i,p in enumerate(doc) if p.get_label()==number]
        if found:starts.append((found[0],m[1]))
    for i,p in enumerate(doc):
        if '参考资料与继续阅读' in p.get_text() and i>len(doc)-5:
            starts.append((i,'参考资料'));break
    starts=sorted(set(starts));first=starts[0][0]
    sparse={i for i,p in enumerate(doc) if len(p.get_text().strip())<80}
    ends=set()
    for k,(start,name) in enumerate(starts):
        end=(starts[k+1][0]-1 if k+1<len(starts) else len(doc)-1)
        while end in sparse and end>start:end-=1
        ends.add(end)
    rows=[]
    top=68.;bottom=774.
    for i,p in enumerate(doc):
        words=[w for w in p.get_text('words') if w[1]>=top-2 and w[3]<=bottom+4]
        extent=max((w[3] for w in words),default=top)
        regular=i>=first and i not in ends and i not in sparse
        rows.append({'pdf_page':i+1,'printed':p.get_label(),'chapter_end':i in ends,'regular':regular,'bottom_used_fraction':round((extent-top)/(bottom-top),3),'bottom_gap_mm':round(max(0,bottom-extent)*25.4/72,1)})
    regular=[r for r in rows if r['regular']]
    result={'method':'Last body-text bounding box within y=68..774pt, excluding chapter ends and sparse title pages; this is a whitespace screening aid, not ink-area density.', 'mean_regular_bottom_gap_mm':round(statistics.mean(r['bottom_gap_mm'] for r in regular),1),'median_regular_bottom_gap_mm':round(statistics.median(r['bottom_gap_mm'] for r in regular),1),'pdf_pages':len(doc),'chapter_starts':[{'pdf_page':i+1,'title':t} for i,t in starts],'chapter_end_pdf_pages':sorted(i+1 for i in ends),'regular_pages':len(regular),'mean_regular_bottom_used_fraction':round(sum(r['bottom_used_fraction'] for r in regular)/len(regular),3),'regular_bottom_gap_over_35mm':[r for r in regular if r['bottom_gap_mm']>35],'rows':rows}
    return result

if __name__=='__main__':
    parser=argparse.ArgumentParser(description='Screen regular pages for large bottom whitespace; inspect flagged pages visually.')
    parser.add_argument('--pdf',type=Path,default=ROOT/'build/main.pdf')
    parser.add_argument('--aux',type=Path,default=ROOT/'build/main.aux')
    args=parser.parse_args()
    print(json.dumps(scan(args.pdf,args.aux),ensure_ascii=False,indent=2))
