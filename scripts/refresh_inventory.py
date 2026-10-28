#!/usr/bin/env python3
"""Refresh asset metadata; preserve human visual/semantic judgments verbatim."""
import csv
import hashlib
import re
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / 'IMAGE_INVENTORY.csv'
FIELDS = ['asset_id', 'filename', 'directory', 'width', 'height', 'sha256',
          'duplicate_of', 'original_referenced', 'topic', 'subtopic', 'key_content',
          'educational_purpose', 'prerequisites', 'difficulty', 'importance',
          'readability', 'scientific_concerns', 'decision', 'target_section',
          'replacement', 'inspection_status', 'batch', 'attribution', 'licensing']

def main():
    existing = {}
    if DEST.exists():
        with DEST.open(encoding='utf-8-sig', newline='') as stream:
            for row in csv.DictReader(stream):
                existing[f"{row['directory']}/{row['filename']}"] = row
    original = (ROOT / 'archive/main-2021.tex').read_text()
    references = set(re.findall(r'\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}', original))
    rows, hashes = [], {}
    for directory in ('done', 'to-do', 'illustration'):
        for path in sorted((ROOT / directory).iterdir()):
            if not path.is_file():
                continue
            relative = path.relative_to(ROOT).as_posix()
            with Image.open(path) as picture:
                width, height = picture.size
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            row = {field: '' for field in FIELDS}
            row.update(existing.get(relative, {}))
            row.update(asset_id=relative, filename=path.name, directory=directory,
                       width=width, height=height, sha256=digest,
                       duplicate_of=hashes.get(digest, ''),
                       original_referenced='yes' if relative in references else 'no')
            row['inspection_status'] = row['inspection_status'] or 'not_visually_inspected'
            rows.append(row)
            hashes.setdefault(digest, relative)
    with DEST.open('w', encoding='utf-8-sig', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=FIELDS, lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)
    inspected = sum(row['inspection_status'] == 'detailed_visual' for row in rows)
    print(f'{len(rows)} source images; {inspected} detailed visual inspections; '
          f"{sum(bool(row['duplicate_of']) for row in rows)} exact duplicate files.")

if __name__ == '__main__':
    main()
