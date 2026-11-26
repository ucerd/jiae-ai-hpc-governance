"""Check consistency of the release manifest and checksum list and verify listed bytes."""
import hashlib
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

def main():
    manifest = json.loads((ROOT/'MANIFEST.json').read_text())
    if manifest['version'] != (ROOT/'VERSION').read_text().strip():
        raise ValueError('Version mismatch')
    expected = {x['path']: (x['sha256'], x['bytes']) for x in manifest['files']}
    lines = (ROOT/'SHA256SUMS.txt').read_text().splitlines()
    sums = {name: digest for digest, name in (line.split('  ', 1) for line in lines)}
    if len(expected) != len(manifest['files']) or len(sums) != len(lines) or sums != {n:d for n,(d,_) in expected.items()}:
        raise ValueError('Manifest and checksum list differ')
    for name, (digest, size) in expected.items():
        path = ROOT/name
        if not path.resolve().is_relative_to(ROOT) or path.is_symlink():
            raise ValueError('Unsafe path: '+name)
        b = path.read_bytes()
        if len(b) != size or hashlib.sha256(b).hexdigest() != digest:
            raise ValueError('Integrity mismatch: '+name)
    print(f'Integrity checks passed ({len(expected)} files).')

if __name__ == '__main__':
    main()
