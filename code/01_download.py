#!/usr/bin/env python3
"""Download the prototype's raw inputs into data/raw/ and record each in MANIFEST.json.

Inputs : SOURCES below (URL, license, expected size).
Outputs: data/raw/<file>, data/raw/MANIFEST.json (url, license, date, bytes, sha256).

Nothing is downloaded unless --yes is given; --list prints the sources and sizes.
Requests carry a user-agent that names the project and a contact e-mail. Existing files
whose SHA-256 is already in the manifest are skipped.
"""
import argparse
import datetime as dt
import hashlib
import json
import pathlib
import sys
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
MANIFEST = RAW / "MANIFEST.json"
UA = "gatekeepers-mirror prototype (research; mailto:huaxiga@umich.edu)"

SOURCES = {
    "iclr26v1.parquet": {
        "url": "https://raw.githubusercontent.com/berenslab/iclr-dataset/main/data/iclr26v1.parquet",
        "license": "MIT (berenslab/iclr-dataset)",
        "expected_bytes": 48993373,
        "note": "ICLR 2017-2026 submissions: title, abstract, authors, decision, scores, keywords, label",
    },
}


def sha256(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_manifest() -> dict:
    if MANIFEST.exists():
        return json.loads(MANIFEST.read_text(encoding="utf-8"))
    return {}


def save_manifest(m: dict) -> None:
    MANIFEST.write_text(json.dumps(m, indent=2, ensure_ascii=False), encoding="utf-8")


def download(name: str, spec: dict, manifest: dict) -> None:
    dest = RAW / name
    if dest.exists() and name in manifest and manifest[name].get("sha256") == sha256(dest):
        print(f"skip {name}: already present and verified")
        return
    req = urllib.request.Request(spec["url"], headers={"User-Agent": UA})
    print(f"downloading {name} from {spec['url']}")
    with urllib.request.urlopen(req, timeout=120) as r, open(dest, "wb") as f:
        while True:
            chunk = r.read(1 << 20)
            if not chunk:
                break
            f.write(chunk)
    size = dest.stat().st_size
    if spec.get("expected_bytes") and abs(size - spec["expected_bytes"]) > 0.05 * spec["expected_bytes"]:
        print(f"warning: {name} is {size} bytes, expected about {spec['expected_bytes']}")
    manifest[name] = {
        "url": spec["url"],
        "license": spec["license"],
        "downloaded": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "bytes": size,
        "sha256": sha256(dest),
        "note": spec.get("note", ""),
    }
    save_manifest(manifest)
    print(f"done {name}: {size} bytes")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--list", action="store_true", help="print sources and sizes, download nothing")
    ap.add_argument("--yes", action="store_true", help="actually download")
    ap.add_argument("--only", nargs="*", help="restrict to these file names")
    args = ap.parse_args()
    names = args.only or list(SOURCES)
    if args.list or not args.yes:
        for n in names:
            s = SOURCES[n]
            print(f"{n}\t{s['expected_bytes']/1e6:.1f} MB\t{s['license']}\t{s['url']}")
        if not args.yes:
            print("(no download: pass --yes)")
        return 0
    RAW.mkdir(parents=True, exist_ok=True)
    manifest = load_manifest()
    for n in names:
        download(n, SOURCES[n], manifest)
    return 0


if __name__ == "__main__":
    sys.exit(main())
