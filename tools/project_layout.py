#!/usr/bin/env python3
"""Validate the two allowed Extended Mind project layouts."""
import argparse
import json
import os
from pathlib import Path
import re
import sys


LAYOUT = re.compile(r"(?m)^layout:\s*(workspace|dev)\s*$")
WHERE = re.compile(
    r"^-\s+[^=\r\n]+?=\s+(.+?)\s{2,}access:\s+(?:ro|rw)(?:\s|$)"
)


def normalized(path):
    return os.path.normcase(os.path.normpath(str(path.resolve(strict=False))))


def where_paths(text):
    paths = []
    inside = False
    for line in text.splitlines():
        if line.strip() == "where:" and not line.startswith((" ", "\t")):
            inside = True
            continue
        if inside and re.match(r"^[a-z][\w-]*:\s*", line):
            break
        if inside and line.startswith("- "):
            match = WHERE.match(line)
            if match:
                paths.append(match.group(1).strip())
    return paths


def check(repo_root, dev_root):
    workspace = repo_root / "workspace"
    errors = []
    projects = []
    owners = {}

    if not workspace.is_dir():
        return {"ok": False, "errors": [f"missing workspace: {workspace}"], "projects": []}

    for folder in sorted((p for p in workspace.iterdir() if p.is_dir()),
                         key=lambda p: p.name.casefold()):
        record = folder / "PROJECT.md"
        if not record.is_file():
            errors.append(f"workspace/{folder.name}: missing PROJECT.md")
            continue
        text = record.read_text(encoding="utf-8-sig")
        layouts = LAYOUT.findall(text)
        roots = where_paths(text)
        if len(layouts) != 1:
            errors.append(f"workspace/{folder.name}: expected one layout:, found {len(layouts)}")
            continue
        layout = layouts[0]
        item = {"project": folder.name, "layout": layout}
        if layout == "workspace":
            if roots:
                errors.append(f"workspace/{folder.name}: workspace layout cannot declare where:")
            item["root"] = str(folder)
        else:
            if len(roots) != 1:
                errors.append(f"workspace/{folder.name}: dev layout needs exactly one where:, found {len(roots)}")
            else:
                root = Path(roots[0])
                item["root"] = str(root)
                if not root.is_absolute():
                    errors.append(f"workspace/{folder.name}: dev root is not absolute: {root}")
                elif normalized(root.parent) != normalized(dev_root):
                    errors.append(f"workspace/{folder.name}: dev root is not an immediate child of {dev_root}: {root}")
                elif not root.is_dir():
                    errors.append(f"workspace/{folder.name}: dev root does not resolve: {root}")
                key = normalized(root)
                if key in owners:
                    errors.append(f"workspace/{folder.name}: dev root also owned by {owners[key]}: {root}")
                else:
                    owners[key] = f"workspace/{folder.name}"
        projects.append(item)

    if not dev_root.is_dir():
        errors.append(f"dev root does not resolve: {dev_root}")
    else:
        for folder in sorted((p for p in dev_root.iterdir() if p.is_dir()),
                             key=lambda p: p.name.casefold()):
            if normalized(folder) not in owners:
                errors.append(f"unregistered dev folder: {folder}")

    return {"ok": not errors, "repo_root": str(repo_root),
            "dev_root": str(dev_root), "projects": projects, "errors": errors}


def main():
    default_repo = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=default_repo)
    parser.add_argument("--dev-root", type=Path, default=default_repo.parent)
    args = parser.parse_args()
    result = check(args.repo_root.resolve(), args.dev_root.resolve())
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
