#!/usr/bin/env python3
"""Report PDF/log checks and original assets reachable from an actual entry point."""
import argparse
import hashlib
import json
import re
from pathlib import Path
import fitz


def source_graph(root, target):
    visited, originals = set(), []
    def visit(path):
        if path in visited:
            return
        visited.add(path)
        text = re.sub(r'(?<!\\)%[^\n]*', '', path.read_text())
        originals.extend(re.findall(r'\\includegraphics(?:\[[^\]]*\])?\{((?:done|to-do|illustration)/[^}]+)\}',text))
        for name in re.findall(r'\\(?:input|include)\{([^}]+)\}',text):
            child=root/name
            if not child.suffix:
                child=child.with_suffix('.tex')
            visit(child)
    visit(root/f'{target}.tex')
    return visited, originals


def audit(target):
    root=Path(__file__).resolve().parents[1]
    pdf=root/f'build/{target}.pdf'
    log=(root/f'build/{target}.log').read_text()
    sources,originals=source_graph(root,target)
    # Never report the previous PDF while a newer source/log is still compiling.
    dependencies=sources | set((root/'styles').glob('*.sty')) | set((root/'figures').rglob('*.csv')) | {root/f'build/{target}.log'}
    if pdf.stat().st_mtime < max(path.stat().st_mtime for path in dependencies):
        raise RuntimeError('PDF is older than its sources/log; finish the build before auditing.')
    if b'%%EOF' not in pdf.read_bytes()[-1024:]:
        raise RuntimeError('PDF is incomplete; wait for the PDF writer to finish.')
    pages=len(fitz.open(pdf))
    if pages==0:
        raise RuntimeError('PDF has no pages; the build is incomplete.')
    document=fitz.open(pdf)
    links=[link for page in document for link in page.get_links()]
    internal=[link for link in links if 'page' in link]
    invalid=[link for link in internal if not 0 <= link['page'] < pages]
    missing_inputs=[str(p.relative_to(root)) for p in sources if not p.is_file()]
    return dict(target=target,pages=pages,pdf_sha256=hashlib.sha256(pdf.read_bytes()).hexdigest(),
                overfull=log.count('Overfull \\hbox')+log.count('Overfull \\vbox'),
                underfull=log.count('Underfull \\hbox')+log.count('Underfull \\vbox'),
                missing_characters=log.count('Missing character:'),
                undefined_references=len(re.findall(r'Reference .* undefined',log)),
                source_files=len(sources),original_files_still_referenced=len(set(originals)),
                original_image_occurrences=len(originals),
                independent_figure_sources=len(list((root/'figures').rglob('*.tex'))),
                internal_links=len(internal),invalid_internal_links=len(invalid),
                missing_inputs=missing_inputs)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('target');args=parser.parse_args()
    result=audit(args.target)
    print(json.dumps(result,ensure_ascii=False,indent=2))
    failures=['overfull','underfull','missing_characters','undefined_references','original_files_still_referenced','invalid_internal_links']
    if any(result[key] for key in failures) or result['missing_inputs']:
        raise SystemExit(1)
