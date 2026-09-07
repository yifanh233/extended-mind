#!/usr/bin/env python3
"""Durable inbox windows. No deletion; completion needs a saved routing receipt."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys
import uuid

BEGIN = re.compile(rb"(?m)^<!-- routing: ([a-f0-9]{16}) start:(\d+) through:(\d+) sha256:([a-f0-9]{64}) -->\r?$")
DONE = re.compile(rb"(?m)^<!-- routed: ([a-f0-9]{16}) receipt:(\S+) sha256:([a-f0-9]{64}) -->\r?$")


def digest(data):
    return hashlib.sha256(data).hexdigest()


def append(path, data):
    with path.open("ab") as stream:
        stream.write(data)
        stream.flush()
        import os
        os.fsync(stream.fileno())


def state(path):
    data = path.read_bytes()
    begins = list(BEGIN.finditer(data))
    completed = {m[1] for m in DONE.finditer(data)}
    pending = [m for m in begins if m[1] not in completed]
    if len(pending) > 1:
        raise ValueError("Multiple pending batches: reconcile them before routing.")
    # A torn marker is not a completed operation. Fail instead of skipping it.
    valid = {m.start() for m in begins} | {m.start() for m in DONE.finditer(data)}
    for m in re.finditer(rb"(?m)^<!-- (?:routing:|routed: [a-f0-9]{16})", data):
        if m.start() not in valid:
            raise ValueError("Incomplete cursor marker: inspect and recover before routing.")
    return data, begins, pending


def window(data, marker):
    start, through = int(marker[2]), int(marker[3])
    if not 0 <= start <= through <= marker.start():
        raise ValueError("Invalid inbox boundary.")
    payload = data[start:through]
    if digest(payload) != marker[4].decode():
        raise ValueError("Inbox window changed; recover from the saved source before completing.")
    items = []
    offset = start
    for line in payload.splitlines(keepends=True):
        text = line.decode("utf-8-sig").strip()
        if text and not text.startswith("<!-- routing:") and not text.startswith("<!-- routed:"):
            items.append({"id": str(offset), "text": text})
        offset += len(line)
    return {"batch": marker[1].decode(), "items": items}


def begin(path):
    data, begins, pending = state(path)
    if pending:
        return window(data, pending[0])
    if begins:
        start = begins[-1].end()
    else:
        # Legacy markers are prior acknowledgements. With none, skip only the header.
        old = list(re.finditer(rb"(?m)^<!-- routed: ritual .*-->\r?$", data))
        divider = re.search(rb"(?m)^---\r?\n", data)
        start = old[-1].end() if old else (divider.end() if divider else 0)
    batch = uuid.uuid4().hex[:16]
    marker = ("\n<!-- routing: %s start:%d through:%d sha256:%s -->\n" %
              (batch, start, len(data), digest(data[start:]))).encode()
    append(path, marker)
    return window(path.read_bytes(), list(BEGIN.finditer(path.read_bytes()))[-1])


def complete(path, receipt_path):
    data, begins, pending = state(path)
    receipt_path = receipt_path.resolve()
    root = path.parent.resolve()
    relative = receipt_path.relative_to(root).as_posix()
    if any(c.isspace() for c in relative):
        raise ValueError("Use a receipt filename without spaces.")
    receipt_bytes = receipt_path.read_bytes()
    receipt = json.loads(receipt_bytes)
    batch = receipt["batch"]
    matching = [m for m in begins if m[1].decode() == batch]
    if len(matching) != 1:
        raise ValueError("Receipt must name an existing batch.")
    expected = window(data, matching[0])
    routes = receipt["routes"]
    ids = [r["id"] for r in routes]
    if sorted(ids) != sorted(i["id"] for i in expected["items"]):
        raise ValueError("Receipt must route every item exactly once.")
    for route in routes:
        dest = (root / route["destination"]).resolve()
        dest.relative_to(root)
        anchor = "inbox:%s:%s" % (batch, route["id"])
        if anchor not in dest.read_text(encoding="utf-8-sig"):
            raise ValueError("Destination is missing durable source anchor " + anchor)
    existing = [m for m in DONE.finditer(data) if m[1].decode() == batch]
    if existing:
        if existing[0][3].decode() != digest(receipt_bytes):
            raise ValueError("Completed receipt changed; retain the original receipt.")
        return {"batch": batch, "status": "already-complete"}
    if not pending or pending[0][1].decode() != batch:
        raise ValueError("Complete the pending batch first.")
    append(path, ("\n<!-- routed: %s receipt:%s sha256:%s -->\n" %
                  (batch, relative, digest(receipt_bytes))).encode())
    return {"batch": batch, "status": "complete"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["begin", "complete"])
    parser.add_argument("--inbox", type=Path, default=Path("inbox.md"))
    parser.add_argument("--receipt", type=Path)
    args = parser.parse_args()
    try:
        if args.action == "complete" and not args.receipt:
            parser.error("complete requires --receipt")
        result = begin(args.inbox) if args.action == "begin" else complete(args.inbox, args.receipt)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except (ValueError, KeyError, TypeError, OSError) as exc:
        print("inbox: " + str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
