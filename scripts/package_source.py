#!/usr/bin/env python3
"""Create a deterministic archive containing only current, buildable source."""
import hashlib
import json
import zipfile
from pathlib import Path

root = Path(__file__).resolve().parents[1]
files = [root / name for name in ['main.tex', 'README.md', 'PROGRESS.md', 'EDITORIAL_PLAN.md', '.gitignore', '.gitattributes']]
for directory in ['chapters', 'figures', 'styles', 'scripts', 'docs']:
    files += [p for p in (root / directory).rglob('*') if p.is_file() and '__pycache__' not in p.parts]
output = root / 'review/handbook-source.zip'
with zipfile.ZipFile(output, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
    for path in sorted(files):
        info = zipfile.ZipInfo(path.relative_to(root).as_posix(), date_time=(2026, 1, 1, 0, 0, 0))
        info.create_system = 3
        info.external_attr = (0o100755 if path.name == 'build.sh' else 0o100644) << 16
        info.compress_type = zipfile.ZIP_DEFLATED
        archive.writestr(info, path.read_bytes())
print(json.dumps({'path': str(output.relative_to(root)), 'files': len(files), 'bytes': output.stat().st_size,
                  'sha256': hashlib.sha256(output.read_bytes()).hexdigest()}, ensure_ascii=False, indent=2))
