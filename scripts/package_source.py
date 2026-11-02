#!/usr/bin/env python3
"""Create a deterministic archive containing only current, buildable source."""
import hashlib
import json
import os
import tempfile
import zipfile
from pathlib import Path


def package(root):
    files = [root / name for name in ['main.tex', 'README.md', 'PROGRESS.md',
                                    'EDITORIAL_PLAN.md', '.gitignore', '.gitattributes']]
    for directory in ['chapters', 'figures', 'styles', 'scripts', 'docs']:
        files += [p for p in (root / directory).rglob('*')
                  if p.is_file() and '__pycache__' not in p.parts]
    # Read before opening any output, so missing inputs cannot truncate a valid ZIP.
    entries = [(p.relative_to(root).as_posix(), p.read_bytes()) for p in sorted(files)]
    output = root / 'review/handbook-source.zip'
    output.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(prefix='.handbook-source-',
                                                suffix='.tmp', dir=output.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, 'wb') as stream:
            with zipfile.ZipFile(stream, 'w', compression=zipfile.ZIP_DEFLATED,
                                 compresslevel=9) as archive:
                for name, contents in entries:
                    info = zipfile.ZipInfo(name, date_time=(2026, 1, 1, 0, 0, 0))
                    info.create_system = 3
                    info.external_attr = (0o100755 if name == 'scripts/build.sh'
                                          else 0o100644) << 16
                    info.compress_type = zipfile.ZIP_DEFLATED
                    archive.writestr(info, contents)
        temporary.chmod(0o644)
        os.replace(temporary, output)
    finally:
        temporary.unlink(missing_ok=True)
    return {'path': str(output.relative_to(root)), 'files': len(entries),
            'bytes': output.stat().st_size,
            'sha256': hashlib.sha256(output.read_bytes()).hexdigest()}


if __name__ == '__main__':
    print(json.dumps(package(Path(__file__).resolve().parents[1]),
                     ensure_ascii=False, indent=2))
