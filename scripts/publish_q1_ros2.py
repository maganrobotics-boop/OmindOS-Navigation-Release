"""Build and publish the pinned Q1 code increment after native acceptance."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import time
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / 'config/q1-ros2-release.json'
TAG = 'q1-ros2-v0.1.0-preview.1'


def gh(*args):
    return subprocess.check_output(['gh', *args], text=True)


def api(path):
    return json.loads(gh('api', '--header', 'Cache-Control: no-cache',
                         'repos/' + os.environ['GH_REPO'] + '/' + path))


def prepare():
    config = json.loads(CONFIG.read_text())
    sha = config['source_commit']
    if not re.fullmatch('[0-9a-f]{40}', sha) or config['source_repository'] != 'Omind-Robotics/OmindOS-Navigation':
        raise ValueError('Unexpected source target')
    source = ROOT / 'build/q1-ros2-source'
    distribution = ROOT / 'build/q1-ros2-distribution'
    if source.exists() or distribution.exists():
        raise ValueError('Use a fresh build directory to preserve previous artifacts')
    local = os.environ.get('Q1_LOCAL_SOURCE_ROOT')
    for name, expected in config['source_sha256'].items():
        relative = Path(name)
        if relative.is_absolute() or '..' in relative.parts:
            raise ValueError('Invalid source path')
        if local:
            raw = (Path(local) / name).read_bytes()
        else:
            url = 'https://raw.githubusercontent.com/' + config['source_repository'] + '/' + sha + '/' + name
            with urlopen(url, timeout=30) as response:
                raw = response.read(500_001)
        if len(raw) > 500_000 or hashlib.sha256(raw).hexdigest() != expected:
            raise ValueError('Pinned source hash mismatch: ' + name)
        target = source / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(raw)
    subprocess.run(['python3', '-m', 'unittest', 'discover', '-s', 'tests', '-p', 'test_q1_release.py', '-v'],
                   cwd=source, check=True)
    spec = importlib.util.spec_from_file_location('q1_release_builder', source / 'release/q1-ros2/package_release.py')
    builder = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(builder)
    builder.package(source, distribution, sha)
    shutil.copyfile(source / 'docs/validation/q1-ros2-20261025.json', distribution / 'NATIVE_VALIDATION.json')
    shutil.copyfile(ROOT / 'docs/Q1_ROS2_RELEASE.zh-CN.md', distribution / 'RELEASE_NOTES.zh-CN.md')
    files = sorted(p for p in distribution.iterdir() if p.is_file())
    if len(files) != 5:
        raise ValueError('Unexpected distribution files')
    return distribution, {p.name: (p.stat().st_size, 'sha256:' + hashlib.sha256(p.read_bytes()).hexdigest()) for p in files}


def main():
    distribution, expected = prepare()
    if os.environ.get('CHECK_ONLY') == '1':
        print(json.dumps({'status': 'PASS', 'tag': TAG, 'assets': list(expected), 'code_only': True}))
        return
    releases = [r for r in api('releases?per_page=100') if r['tag_name'] == TAG]
    if not releases:
        gh('release', 'create', TAG, '--target', os.environ['GITHUB_SHA'], '--draft', '--prerelease',
           '--title', 'Q1 ROS 2 simulation code · 0.1.0-preview.1',
           '--notes-file', str(distribution / 'RELEASE_NOTES.zh-CN.md'))
        for _ in range(10):
            releases = [r for r in api('releases?per_page=100') if r['tag_name'] == TAG]
            if releases:
                break
            time.sleep(2)
    if len(releases) != 1 or not releases[0]['prerelease']:
        raise ValueError('Unexpected release target')
    release = releases[0]
    existing = {a['name']: a for a in release['assets']}
    if not set(existing).issubset(expected):
        raise ValueError('Unexpected existing release asset')
    for name, asset in existing.items():
        if (asset['size'], asset.get('digest')) != expected[name]:
            raise ValueError('Existing asset differs; immutable release: ' + name)
    missing = sorted(set(expected) - set(existing))
    if missing and not release['draft']:
        raise ValueError('Published releases cannot be modified')
    if missing:
        gh('release', 'upload', TAG, *[str(distribution / name) for name in missing])
    for _ in range(10):
        release = api('releases/' + str(release['id']))
        assets = {a['name']: a for a in release['assets']}
        if set(assets) == set(expected) and all(assets[n].get('digest') for n in expected):
            break
        time.sleep(2)
    if set(assets) != set(expected):
        raise ValueError('Incomplete release upload')
    for name in expected:
        if (assets[name]['size'], assets[name]['digest']) != expected[name]:
            raise ValueError('Uploaded asset mismatch: ' + name)
    if release['draft']:
        release = json.loads(gh('api', '--method', 'PATCH',
            'repos/' + os.environ['GH_REPO'] + '/releases/' + str(release['id']),
            '-F', 'draft=false', '-F', 'prerelease=true', '-f', 'make_latest=false'))
    if release['draft'] or not release['prerelease']:
        raise ValueError('Publication was not confirmed')
    print(json.dumps({'url': release['html_url'], 'verified_assets': len(expected), 'hardware_tested': False}))


if __name__ == '__main__':
    main()
