#!/usr/bin/env python3
"""Hash an explicit project's tracked and untracked files; never classify intent."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys


def inventory(root, includes):
    root = root.resolve()
    if not includes:
        raise ValueError("Name the permitted scope with at least one --include.")
    normalized = []
    for item in includes:
        target = (root / item).resolve()
        rel = target.relative_to(root).as_posix()
        if any(part == ".git" for part in Path(rel).parts):
            raise ValueError("The Git metadata directory is not project content.")
        normalized.append(rel)
    result = subprocess.run(["git", "-c", "safe.directory=" + str(root), "-C", str(root), "ls-files", "-z", "--cached",
                             "--others", "--exclude-standard", "--"] +
                            ["." if p == "." else ":(literal)" + p for p in normalized],
                            check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    files = {}
    for raw in sorted(set(result.stdout.split(b"\0")) - {b""}):
        rel = raw.decode("utf-8")
        path = root / rel
        # Do not follow a symlink/junction outside the declared root.
        path.resolve().relative_to(root)
        if path.is_symlink():
            raise ValueError("Symlink requires separate scoped inspection: " + rel)
        if path.is_file():
            hasher = hashlib.sha256()
            with path.open("rb") as stream:
                for block in iter(lambda: stream.read(1024 * 1024), b""):
                    hasher.update(block)
            files[rel] = hasher.hexdigest()
    return {"version": 1, "root": str(root), "include": normalized, "files": files}


def changes(before, after):
    if before["root"] != after["root"] or before["include"] != after["include"]:
        raise ValueError("Baseline root/scope differs; do not silently reset it.")
    old, new = before["files"], after["files"]
    return {"added": sorted(set(new) - set(old)), "removed": sorted(set(old) - set(new)),
            "modified": sorted(k for k in old.keys() & new.keys() if old[k] != new[k]),
            "coverage": "tracked plus non-ignored untracked files in the explicit scope",
            "classification": "not assessed; compare with the user's decisions"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["snapshot", "changes"])
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--include", action="append", required=True)
    parser.add_argument("--baseline", type=Path, required=True)
    args = parser.parse_args()
    try:
        current = inventory(args.root, args.include)
        if args.action == "snapshot":
            # A changed scope/window is a new baseline filename, never an overwrite.
            args.baseline.parent.mkdir(parents=True, exist_ok=True)
            with args.baseline.open("x", encoding="utf-8") as stream:
                json.dump(current, stream, indent=2, ensure_ascii=False)
            print(json.dumps({"baseline": str(args.baseline), "files": len(current["files"])}))
        else:
            before = json.loads(args.baseline.read_text(encoding="utf-8-sig"))
            print(json.dumps(changes(before, current), indent=2, ensure_ascii=False))
    except (ValueError, KeyError, OSError, subprocess.CalledProcessError) as exc:
        print("inventory: " + str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
