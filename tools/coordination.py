#!/usr/bin/env python3
"""Session submissions, serialized publication and exact ritual windows (stdlib).

LIVE.md is advisory human-assigned ownership. The OS lock serializes this helper
only; it does not prevent an editor or another program from writing shared files.
"""
import argparse
import base64
from contextlib import contextmanager
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import sys
import uuid


def digest(data):
    return hashlib.sha256(data).hexdigest()


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")


def timestamp():
    return datetime.now(timezone.utc).isoformat()


def inside(root, path):
    target = (root / path).resolve()
    target.relative_to(root.resolve())
    return target


def identifier(value):
    if not re.fullmatch(r"[a-f0-9]{32}", value):
        raise ValueError("Expected a full session/window UUID, without hyphens.")
    return value


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def create(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())


def session_path(root, session):
    return inside(root, "coordination/sessions/" + identifier(session))


def new_session(root, agent, scope, task, role, base, inputs, mode="work", interactive=False):
    if not re.fullmatch(r"[\w.-]+", agent) or not re.fullmatch(r"(?:project/[\w-]+|general)", scope):
        raise ValueError("Invalid agent or scope.")
    if role not in ("reviewer", "writer", "integrator") or mode not in ("work", "review", "CONSOLIDATED", "feynman", "socratic", "devil", "sleep"):
        raise ValueError("Invalid role or mode.")
    if not task.strip() or not base.strip() or any(c in base for c in "\n\r|"):
        raise ValueError("Task and single-line base revision are required.")
    sid = uuid.uuid4().hex
    snapshots = {}
    for path in inputs:
        target = inside(root, path)
        snapshots[target.relative_to(root.resolve()).as_posix()] = digest(target.read_bytes())
    value = dict(session=sid, agent=agent, scope=scope, task=task, role=role,
                 base=base, inputs=snapshots, started=timestamp(), mode=mode)
    if interactive:
        value["interactive"] = True
    directory = session_path(root, sid)
    directory.mkdir(parents=True, exist_ok=False)
    create(directory / "session.json", encoded(value))
    return value


def check_inputs(root, session):
    info = load(session_path(root, session) / "session.json")
    changed = []
    for name, expected in info["inputs"].items():
        path = inside(root, name)
        if not path.is_file() or digest(path.read_bytes()) != expected:
            changed.append(name)
    return dict(session=session, changed=changed, base=info["base"])


def submit(root, session, body):
    info = load(session_path(root, session) / "session.json")
    body = body.strip()
    if not body or re.search(r"(?m)^(?:SESSLOG|record-id:|END-SESSLOG)", body):
        raise ValueError("Submit the body only; log headers and record markers are reserved.")
    for field in ("topics:", "provenance:", "next:"):
        if not re.search(r"(?m)^" + field, body):
            raise ValueError("Missing handoff field: " + field)
    path = session_path(root, session) / "handoff.json"
    if path.exists():
        prior = load(path)
        if prior["body"] != body or prior["session"] != info:
            raise ValueError("Submission is immutable; open a new session for a correction.")
        return prior
    record = dict(id=session, session=info, body=body, submitted=timestamp())
    create(path, encoded(record))
    return record


@contextmanager
def publication_lock(root, name="coordination/publication.lock"):
    # Persistent file, process-held lock: a forgotten filename is NOT a held lock.
    path = inside(root, name)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a+b") as stream:
        if path.stat().st_size == 0:
            stream.write(b"0")
            stream.flush()
        stream.seek(0)
        if os.name == "nt":
            import msvcrt
            msvcrt.locking(stream.fileno(), msvcrt.LK_NBLCK, 1)
        else:
            import fcntl
            fcntl.flock(stream.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        try:
            yield
        finally:
            stream.seek(0)
            if os.name == "nt":
                msvcrt.locking(stream.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                fcntl.flock(stream.fileno(), fcntl.LOCK_UN)


def require_publisher(root, publisher):
    info = load(session_path(root, publisher) / "session.json")
    live = (root / "LIVE.md").read_text(encoding="utf-8-sig")
    if info["role"] != "integrator" or re.findall(r"(?m)^Publisher: ([a-f0-9]{32})\s*$", live) != [publisher]:
        raise ValueError("Publication requires the single integrator explicitly assigned in LIVE.md.")
    rows = [line for line in live.splitlines() if line.startswith("- session: " + publisher + " |")]
    if len(rows) != 1:
        raise ValueError("Publisher needs exactly one current ownership row.")
    fields = dict(part.strip().split(": ", 1) for part in rows[0][2:].split(" | "))
    expiry = datetime.fromisoformat(fields["expires"].replace("Z", "+00:00"))
    if fields.get("state") != "active" or expiry.tzinfo is None or expiry <= datetime.now(timezone.utc):
        raise ValueError("Publisher released or expired. Reconcile ownership; never auto-take over.")


def append_bytes(path, data):
    with path.open("ab") as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())


def recover_publication(root):
    journal = inside(root, "coordination/pending-publication.json")
    if not journal.exists():
        return
    pending = load(journal)
    data = (root / "sesslog.md").read_bytes()
    expected = base64.b64decode(pending["append"], validate=True)
    offset = pending["offset"]
    tail = data[offset:]
    if digest(data[:offset]) != pending["prefix_sha256"] or not expected.startswith(tail):
        raise ValueError("Publication interrupted with conflicting bytes; preserve journal and reconcile manually.")
    append_bytes(root / "sesslog.md", expected[len(tail):])
    journal.unlink()


def publish(root, session, publisher):
    record_path = session_path(root, session) / "handoff.json"
    record_bytes = record_path.read_bytes()
    record = json.loads(record_bytes)
    source_hash = digest(record_bytes)
    with publication_lock(root):
        require_publisher(root, publisher)
        recover_publication(root)
        data = (root / "sesslog.md").read_bytes()
        text = data.decode("utf-8-sig")
        marker = "record-id: " + session + " | source-sha256: " + source_hash
        prior = [block for block in blocks(text) if re.search(r"(?m)^record-id: " + session + r"(?: |$)", block["text"])]
        if prior:
            expected = marker + " | publisher: "
            if len(prior) != 1 or expected not in prior[0]["text"] or not prior[0]["text"].endswith(record["body"] + "\nEND-SESSLOG " + session):
                raise ValueError("Published record changed or duplicated; reconcile before retrying.")
            return dict(status="already-published", key=prior[0]["text"].split(" |", 1)[0][8:], id=session)
        info = record["session"]
        day = datetime.now().astimezone().date().isoformat()
        numbers = re.findall(r"(?m)^SESSLOG " + day + r"\.(\d+)(?:@[^ |]+)? .*?scope: " + re.escape(info["scope"]) + r"(?:\s*\||\s*$)", text)
        key = day + "." + str(max(map(int, numbers), default=0) + 1)
        header = "SESSLOG %s | mode: %s | agent: %s | scope: %s | boots-from: %s | session: %s" % (key, info["mode"], info["agent"], info["scope"], info["base"], session)
        payload = ("\n\n" + header + "\n" + marker + " | publisher: " + publisher + "\n" + record["body"] + "\nEND-SESSLOG " + session + "\n").encode("utf-8")
        pending = dict(offset=len(data), prefix_sha256=digest(data), append=base64.b64encode(payload).decode("ascii"))
        create(inside(root, "coordination/pending-publication.json"), encoded(pending))
        recover_publication(root)
        return dict(status="published", key=key, id=session)


def blocks(text):
    starts = list(re.finditer(r"(?m)^SESSLOG ", text))
    counts = {}
    result = []
    for index, start in enumerate(starts):
        block = text[start.start():starts[index + 1].start() if index + 1 < len(starts) else len(text)].strip()
        fingerprint = digest(block.encode("utf-8"))
        counts[fingerprint] = counts.get(fingerprint, 0) + 1
        if re.search(r"\| mode: CONSOLIDATED(?:\s*\||\s*$)", block.splitlines()[0]):
            continue
        result.append(dict(id=fingerprint + ":" + str(counts[fingerprint]), text=block))
    return result


def processed(root):
    done = set()
    for path in inside(root, "coordination/receipts").glob("*.json"):
        receipt = load(path)
        evidence = inside(root, receipt["evidence"])
        snapshot = inside(root, receipt["snapshot"])
        if digest(evidence.read_bytes()) != receipt["evidence_sha256"] or digest(snapshot.read_bytes()) != receipt["snapshot_sha256"]:
            raise ValueError("A ritual receipt's evidence or snapshot changed: " + path.name)
        done.update(receipt["processed"])
    return done


def window(root, output):
    with publication_lock(root):
        return capture_window(root, output)


def capture_window(root, output):
    if inside(root, "coordination/pending-publication.json").exists():
        raise ValueError("Recover interrupted publication before taking a ritual window.")
    done = processed(root)
    candidates = blocks((root / "sesslog.md").read_text(encoding="utf-8-sig"))
    value = dict(id=uuid.uuid4().hex, created=timestamp(), bootstrap=not any(inside(root, "coordination/receipts").glob("*.json")),
                 records=[b for b in candidates if b["id"] not in done])
    create(inside(root, output), encoded(value))
    return dict(id=value["id"], records=len(value["records"]), bootstrap=value["bootstrap"], snapshot=output)


def complete(root, snapshot, evidence, publisher):
    with publication_lock(root):
        return acknowledge_window(root, snapshot, evidence, publisher)


def acknowledge_window(root, snapshot, evidence, publisher):
    require_publisher(root, publisher)
    if inside(root, "coordination/pending-publication.json").exists():
        raise ValueError("Recover interrupted publication before acknowledging a window.")
    snapshot_path, evidence_path = inside(root, snapshot), inside(root, evidence)
    value = load(snapshot_path)
    wid = identifier(value["id"])
    ids = [b["id"] for b in value["records"]]
    current = {b["id"]: b["text"] for b in blocks((root / "sesslog.md").read_text(encoding="utf-8-sig"))}
    if len(set(ids)) != len(ids) or any(current.get(b["id"]) != b["text"] for b in value["records"]):
        raise ValueError("Snapshot records changed; do not acknowledge this window.")
    if ("coordination-window:" + wid) not in evidence_path.read_text(encoding="utf-8"):
        raise ValueError("Saved ritual evidence must name coordination-window:" + wid)
    receipt = dict(processed=ids, snapshot=snapshot_path.relative_to(root.resolve()).as_posix(),
                   snapshot_sha256=digest(snapshot_path.read_bytes()), evidence=evidence_path.relative_to(root.resolve()).as_posix(),
                   evidence_sha256=digest(evidence_path.read_bytes()), publisher=publisher)
    path = inside(root, "coordination/receipts/" + wid + ".json")
    if path.exists():
        if load(path) != receipt:
            raise ValueError("Receipt is immutable.")
        return dict(status="already-complete", id=wid)
    create(path, encoded(receipt))
    return dict(status="complete", id=wid, records=len(ids))


FORWARD = ("pending", "rule", "rules", "stage", "apply")


def consolidation_module():
    path = Path(__file__).with_name("consolidation.py")
    if not path.is_file():
        return None
    spec = importlib.util.spec_from_file_location("consolidation", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def relay(root, session, event):
    # Runs after the record is stored; a helper failure never fails the handback.
    try:
        module = consolidation_module()
        out = {} if module is None else module.relay(root, session, event)
    except (Exception, SystemExit) as exc:
        return {"relay": "EM · consolidation unavailable: " + type(exc).__name__ + ": " + " ".join(str(exc).split())[:60]}
    return out if isinstance(out, dict) else {"relay": "EM · consolidation unavailable: bad relay result"}


def main():
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    first = argparse.ArgumentParser(add_help=False)
    first.add_argument("--root", type=Path, default=Path.cwd())
    known, rest = first.parse_known_args()
    if rest and rest[0] in FORWARD:
        module = consolidation_module()
        if module is None:
            print("coordination: consolidation helper not installed", file=sys.stderr)
            return 1
        return module.main(known.root.resolve(), rest)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    sub = parser.add_subparsers(dest="action", required=True)
    new = sub.add_parser("new")
    for name in ("agent", "scope", "task", "base"):
        new.add_argument("--" + name, required=True)
    new.add_argument("--role", choices=["reviewer", "writer", "integrator"], default="reviewer")
    new.add_argument("--mode", default="work")
    new.add_argument("--input", action="append", default=[])
    new.add_argument("--interactive", action="store_true")
    for action in ("check", "submit", "publish"):
        command = sub.add_parser(action)
        command.add_argument("--session", required=True)
        if action == "submit":
            command.add_argument("--body", required=True)
        if action == "publish":
            command.add_argument("--publisher", required=True)
    sub.add_parser("window").add_argument("--output", required=True)
    ack = sub.add_parser("complete")
    for name in ("snapshot", "evidence", "publisher"):
        ack.add_argument("--" + name, required=True)
    args = parser.parse_args()
    root = args.root.resolve()
    try:
        if args.action == "new":
            result = new_session(root, args.agent, args.scope, args.task, args.role, args.base, args.input, args.mode, args.interactive)
        elif args.action == "check":
            result = check_inputs(root, args.session)
        elif args.action == "submit":
            fresh = not (session_path(root, args.session) / "handoff.json").exists()
            result = submit(root, args.session, inside(root, args.body).read_text(encoding="utf-8-sig"))
            result = dict(status="submitted", id=result["id"])
            result.update(relay(root, args.session, "submit" if fresh else "resubmit"))
        elif args.action == "publish":
            result = publish(root, args.session, args.publisher)
            result.update(relay(root, args.session, "publish"))
        elif args.action == "window":
            result = window(root, args.output)
        else:
            result = complete(root, args.snapshot, args.evidence, args.publisher)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except (ValueError, OSError, KeyError, TypeError) as exc:
        print("coordination: " + str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
