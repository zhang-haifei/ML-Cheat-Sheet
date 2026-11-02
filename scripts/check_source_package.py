#!/usr/bin/env python3
"""Check the delivered ZIP through extraction, repackaging and write failures."""
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path
from unittest.mock import patch


def verify():
    root = Path(__file__).resolve().parents[1]
    archive_path = root / 'review/handbook-source.zip'
    if not archive_path.is_file():
        raise SystemExit('Run python scripts/package_source.py first.')
    delivered = archive_path.read_bytes()
    with tempfile.TemporaryDirectory(prefix='handbook-package-') as directory:
        source = Path(directory) / 'fresh source with spaces'
        source.mkdir()
        with zipfile.ZipFile(archive_path) as archive:
            members = archive.infolist()
            assert archive.testzip() is None
            for member in members:
                name = Path(member.filename)
                assert not name.is_absolute() and '..' not in name.parts
                assert name.suffix not in ['.pdf', '.zip']
                assert archive.read(member.filename) == (root / name).read_bytes(), name
            assert archive.getinfo('scripts/build.sh').external_attr >> 16 == 0o100755
            archive.getinfo('scripts/check_source_package.py')
            archive.extractall(source)
            for member in members:
                os.chmod(source / member.filename, member.external_attr >> 16)
        assert not (source / 'review').exists()

        def run_package():
            result = subprocess.run([sys.executable, 'scripts/package_source.py'],
                                    cwd=source, capture_output=True, text=True)
            assert result.returncode == 0, result.stderr
            return json.loads(result.stdout)

        first = run_package()
        output = source / 'review/handbook-source.zip'
        assert output.read_bytes() == delivered
        run_package()
        assert output.read_bytes() == delivered

        readme = source / 'README.md'
        contents = readme.read_bytes()
        readme.unlink()
        failed = subprocess.run([sys.executable, 'scripts/package_source.py'],
                                cwd=source, capture_output=True, text=True)
        assert failed.returncode != 0 and output.read_bytes() == delivered
        readme.write_bytes(contents)

        spec = importlib.util.spec_from_file_location('package_check',
                                                      source / 'scripts/package_source.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        original = zipfile.ZipFile.writestr

        def interrupted(archive, *args, **kwargs):
            original(archive, *args, **kwargs)
            raise OSError('Injected archive write interruption')

        try:
            with patch.object(zipfile.ZipFile, 'writestr', interrupted):
                module.package(source)
        except OSError:
            pass
        else:
            raise AssertionError('Expected an injected write interruption')
        assert output.read_bytes() == delivered
        assert set(output.parent.iterdir()) == {output}
        return {'status': 'PASS', 'source_members': first['files'],
                'fresh_extraction_repackage_identical': True,
                'repeat_package_identical': True, 'build_script_archive_mode': '100755',
                'missing_input_preserves_previous_archive': True,
                'mid_write_failure_preserves_previous_archive': True,
                'failed_write_leaves_no_temporary_file': True}


if __name__ == '__main__':
    print(json.dumps(verify(), ensure_ascii=False, indent=2))
