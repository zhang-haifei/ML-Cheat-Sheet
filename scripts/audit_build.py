#!/usr/bin/env python3
"""Report PDF/log checks and original assets reachable from an actual entry point."""
import argparse
import csv
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
    dependencies=sources | set((root/'styles').glob('*.sty')) | {root/f'build/{target}.log'}
    if pdf.stat().st_mtime < max(path.stat().st_mtime for path in dependencies):
        raise RuntimeError('PDF is older than its sources/log; finish the build before auditing.')
    if b'%%EOF' not in pdf.read_bytes()[-1024:]:
        raise RuntimeError('PDF is incomplete; wait for the PDF writer to finish.')
    pages=len(fitz.open(pdf))
    if pages==0:
        raise RuntimeError('PDF has no pages; the build is incomplete.')
    with (root/'IMAGE_INVENTORY.csv').open(encoding='utf-8-sig',newline='') as f:
        inspected=sum(row['inspection_status']=='detailed_visual' for row in csv.DictReader(f))
    return dict(target=target,pages=pages,pdf_sha256=hashlib.sha256(pdf.read_bytes()).hexdigest(),
                overfull=log.count('Overfull \\hbox')+log.count('Overfull \\vbox'),
                underfull=log.count('Underfull \\hbox')+log.count('Underfull \\vbox'),
                missing_characters=log.count('Missing character:'),
                undefined_references=len(re.findall(r'Reference .* undefined',log)),
                source_files=len(sources),original_files_still_referenced=len(set(originals)),
                original_image_occurrences=len(originals),inspected_total=inspected)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('target');args=parser.parse_args()
    print(json.dumps(audit(args.target),ensure_ascii=False,indent=2))
