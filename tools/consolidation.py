"""Consolidation helper, read side. Stdlib only, Python 3.9.

tools/coordination.py forwards `pending`, `rule` and `rules` here and calls
relay() after `submit` and `publish`. Writes go only under
coordination/proposals/, only in calls that carry a session (relay,
`pending --full --session`, `rule`), through temp files and os.replace, inside
the proposals lock. Nothing here writes kb/, AGENTS.md, schedule.md, a
PROJECT.md, sesslog.md, a .zh.md file or a workspace/ project folder, and
nothing is applied: a `y` approves, the agent's attended commit applies.
`stage` and `apply` arrive with a later drafting step.
"""
import argparse
from contextlib import contextmanager, nullcontext
from datetime import date, datetime, timedelta
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import sys

_spec = importlib.util.spec_from_file_location("coordination_core", Path(__file__).with_name("coordination.py"))
C = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(C)

P = "coordination/proposals"
CONTROL = "coordination/consolidation.md"
KEYS = ("state", "drafts-per-week", "targets", "scopes", "backlog", "pool")
STATES = ("off", "paused", "shadow", "on")
TARGETS = ("principles", "notes", "schedule", "skills", "rules", "retire", "publish")
FOLDER = {"open": "", "stub": "", "done": "done/", "rejected": "rejected/", "expired": "expired/"}
LESSON_LANES = ("fail-fix", "success", "source")
LANE_CARDS = ("inbox", "predict", "publish", "labels", "rules-drift")
DRIFT = ("text", "orphan", "missing-home", "retired-copy", "anchor", "label", "when", "dup")
CAP, STUB_DAYS, LATER_DAYS = 6, 30, 14
NOISE = re.compile(r"(no|lacks?|absent|missing|still has no)\b.{0,40}\b(procedure|task[- ]type)", re.I)
BEGIN = re.compile(rb"(?m)^<!-- routing: ([a-f0-9]{16}) start:(\d+) through:(\d+) sha256:([a-f0-9]{64}) -->\r?$")
DONE = re.compile(rb"(?m)^<!-- routed: ([a-f0-9]{16}) receipt:(\S+) sha256:([a-f0-9]{64}) -->\r?$")
LEGACY = re.compile(rb"(?m)^<!-- routed: ritual .*-->\r?$")


class Busy(Exception):
    pass


class Parser(argparse.ArgumentParser):
    def error(self, message):
        raise ValueError(message)


# ---- small I/O ----------------------------------------------------------------------------------

def today():
    return date.today()


def lf(text):
    return text.replace("\r\n", "\n")


def sha(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def age(iso):
    try:
        return (today() - date.fromisoformat((iso or "")[:10])).days
    except ValueError:
        return -1


def split(value):
    return [x.strip().lstrip("#") for x in (value or "").split(",") if x.strip()]


def sees(scope, record_scope):
    return scope in (None, "project/system") or record_scope == scope


def slug(scope):
    return (scope or "general").split("/")[-1]


def read(root, rel):
    path = root / rel
    return lf(path.read_text(encoding="utf-8-sig", errors="replace")) if path.is_file() else None


def at_head(root, rel):
    try:
        run = subprocess.run(["git", "-C", str(root), "show", "HEAD:./" + rel], capture_output=True, timeout=10,
                             creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
    except (OSError, subprocess.SubprocessError):
        return None
    return lf(run.stdout.decode("utf-8-sig", "replace")) if run.returncode == 0 else None


def write(root, rel, text):
    if not rel.startswith(P + "/"):
        raise ValueError("consolidation writes only under " + P)
    path = C.inside(root, rel)
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(path.name + ".tmp")
    temp.write_bytes(text.encode("utf-8"))
    os.replace(str(temp), str(path))


def ledger_rows(root):
    return [json.loads(line) for line in (read(root, P + "/ledger.jsonl") or "").split("\n") if line.strip()]


def log(root, ev, ident, session, lane, **extra):
    row = dict(t=datetime.now().astimezone().isoformat(timespec="seconds"), ev=ev, id=ident, session=session, lane=lane, **extra)
    write(root, P + "/ledger.jsonl", (read(root, P + "/ledger.jsonl") or "") + json.dumps(row, sort_keys=True) + "\n")


def state(root):
    return json.loads(read(root, P + "/state.json") or "{}")


def save_state(root, value):
    write(root, P + "/state.json", json.dumps(value, indent=2, sort_keys=True) + "\n")


@contextmanager
def locked(root):
    guard = C.publication_lock(root, P + "/.lock")
    try:
        guard.__enter__()
    except OSError:
        raise Busy() from None
    try:
        yield
    finally:
        guard.__exit__(None, None, None)


def session_info(root, session):
    return C.load(C.session_path(root, session.lstrip("#")) / "session.json")


# ---- control: the narrower of the working file and HEAD -------------------------------------------

def convert(key, v):
    items = [x.strip() for x in v.split(",") if x.strip()]
    if key == "state":
        pause = re.fullmatch(r"paused until (\d{4}-\d{2}-\d{2})", v)
        if v in ("off", "shadow", "on") or pause:
            return ("paused", pause.group(1)) if pause else (v, None)
    elif key == "drafts-per-week" and v.isdigit():
        return int(v)
    elif key == "targets" and items and all(x in TARGETS for x in items):
        return set(items)
    elif key == "scopes":
        m = re.fullmatch(r"(all except|only) ([\w-]+(?:\s*,\s*[\w-]+)*)", v)
        if v == "all" or m:
            return ("all", set()) if v == "all" else (m.group(1), {x.strip() for x in m.group(2).split(",")})
    elif key == "backlog" and v in ("on", "off"):
        return v == "on"
    elif key == "pool" and re.fullmatch(r"\d{4}-\d{2}-\d{2}", v):
        return v
    raise ValueError(key)


def parse_control(text):
    value = {}
    for raw in text.split("\n"):
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        m = re.fullmatch(r"([a-z-]+):\s*(.*)", line)
        if not m or m.group(1) not in KEYS or m.group(1) in value:
            return None, "unknown or repeated key " + (m.group(1) if m else line[:20])
        try:
            value[m.group(1)] = convert(m.group(1), m.group(2).strip())
        except ValueError:
            return None, "bad %s: %s" % (m.group(1), m.group(2).strip()[:30])
    missing = [k for k in KEYS if k not in value]
    return (None, "missing " + ", ".join(missing)) if missing else (value, "")


def control(root):
    work = read(root, CONTROL)
    if work is None:
        return None, "no control file"
    committed = at_head(root, CONTROL)
    if committed is None:
        return None, "control not committed"
    (a, why_a), (b, why_b) = parse_control(work), parse_control(committed)
    if a is None or b is None:
        return None, "control unparsable: " + (why_a or why_b)
    # "system" is always a scope: a new install has no workspace/system/ folder.
    known = {p.name for p in (root / "workspace").glob("*") if p.is_dir()} | {"general", "system"}

    def allowed(spec):
        kind, names = spec
        return set(known) if kind == "all" else known - names if kind == "all except" else set(names)
    first = min(a, b, key=lambda v: STATES.index(v["state"][0]))["state"][0]
    return dict(state=first, until=max(v["state"][1] for v in (a, b) if v["state"][0] == "paused") if first == "paused" else None,
                drafts=min(a["drafts-per-week"], b["drafts-per-week"]), targets=a["targets"] & b["targets"],
                scopes=allowed(a["scopes"]) & allowed(b["scopes"]), backlog=a["backlog"] and b["backlog"],
                pool=max(a["pool"], b["pool"]), hashes=[sha(work), sha(committed)]), ""


def off_line(ctl, why):
    if ctl is None:
        return "EM · consolidation off (" + why + ")"
    if ctl["state"] == "paused" and ctl["until"] < today().isoformat():
        # A pause past its date stays off: resuming by itself would widen without a commit.
        return "EM · consolidation off (pause expired %s; edit %s)" % (ctl["until"], CONTROL)
    return "EM · consolidation paused until " + ctl["until"] if ctl["state"] == "paused" else "EM · consolidation off"


# ---- records and lessons (CODE 5.2) -------------------------------------------------------------

def records(root):
    text, recs = read(root, "sesslog.md") or "", []
    starts = [m.start() for m in re.finditer(r"(?m)^SESSLOG ", text)] + [len(text)]
    for a, b in zip(starts, starts[1:]):
        block = text[a:b].strip()
        first = block.split("\n", 1)[0]
        words = first.split()

        def field(name):
            found = re.search(r"\| %s: (\S+)" % name, first)
            return found.group(1) if found else None
        rid = re.search(r"(?m)^record-id: ([a-f0-9]{32})\b", block)
        key = words[1] if len(words) > 1 else ""
        recs.append(dict(id=rid.group(1) if rid else sha(block), key=key, session=field("session"), agent=field("agent"),
                         scope=field("scope") or "general", date=key[:10], text=block, published=True,
                         consolidated=field("mode") == "CONSOLIDATED"))
    published = {r["id"] for r in recs}
    for path in sorted((root / "coordination/sessions").glob("*/handoff.json")):
        h = C.load(path)
        if h.get("id") not in published:
            info = h.get("session") or {}
            recs.append(dict(id=h["id"], key=h["id"], session=h["id"], agent=info.get("agent"), scope=info.get("scope", "general"),
                             date=h.get("submitted", "")[:10], text=h.get("body", ""), published=False, consolidated=False))
    return recs


def lessons(recs, pool):
    out = []
    for r in recs:
        if r["date"] < pool:
            continue
        ext = bool(re.search(r"(?m)^ext:\s*yes\b", r["text"]))
        for line in re.findall(r"(?m)^principles:(.*)$", r["text"]):
            m = re.search(r'candidate="(.*?)"(?=\s+[a-z-]+=|\s*$)', line)
            if not m or m.group(1).strip().lower() in ("", "none") or NOISE.search(m.group(1)):
                continue
            tail = line[m.end():]

            def pick(pattern):
                found = re.search(pattern, tail)
                return found.group(1) if found else None
            out.append(dict(rec=r, text=m.group(1), kind=pick(r"\bkind=([a-z-]+)"), proof=pick(r"\bproof=(\S+)"),
                            quote=pick(r'\bquote="(.*?)"(?=\s+[a-z-]+=|\s*$)'), ext=ext))
    return out


def resolves(root, proof, keys):
    if not proof or re.match(r"[a-z][\w+.-]*://", proof):
        return False
    if proof.startswith("sesslog#"):
        return proof[8:] in keys
    if re.fullmatch(r"[a-f0-9]{32}", proof):
        return proof in keys
    try:
        return C.inside(root, re.split(r"::|:(?=\d)", proof)[0]).exists()
    except (ValueError, OSError):
        return False


def cited(root, source):
    return bool(source) and any(source in p.read_text(encoding="utf-8", errors="replace") for p in (root / "kb").rglob("*.md"))


def tallies(rows):
    tally = {}
    for row in rows:
        if row.get("ev") in ("y", "n"):
            tally.setdefault(row.get("lane"), [0, 0])[row["ev"] == "n"] += 1
    return tally


def candidates(root, ctl, scope, recs):
    """Ripe lessons in lane order, oldest first, and the count of words? lessons (never ripe in this edition)."""
    privates = {s for s, p in projects(root).items() if p["private"]}
    taken = {r for _, rec in on_disk(root) for r in rec.get("records", [])}
    keys = {k for r in recs for k in (r["id"], r["key"])}
    stopped = {lane for lane, (y, n) in tallies(ledger_rows(root)).items() if y + n >= 4 and n > y}
    ripe, words = [], 0
    for les in lessons(recs, ctl["pool"]):
        where = les["rec"]["scope"]
        if les["ext"] or les["rec"]["id"] in taken or not sees(scope, where) or slug(where) not in ctl["scopes"] \
                or (slug(where) in privates and where != scope):
            continue
        kind = les["kind"]
        words += kind == "words"
        if kind not in stopped and ((kind in ("fail-fix", "success") and resolves(root, les["proof"], keys))
                                    or (kind == "source" and cited(root, les["proof"]))):
            ripe.append((LESSON_LANES.index(kind), les["rec"]["date"], kind, les))
    return [(kind, les) for _, _, kind, les in sorted(ripe, key=lambda x: x[:2])], words


# ---- projects and the rule library (S4.6 grammar) ------------------------------------------------

def projects(root):
    out = {}
    for path in sorted((root / "workspace").glob("*/PROJECT.md")):
        text = lf(path.read_text(encoding="utf-8-sig", errors="replace"))
        m = re.search(r"(?m)^labels:(.*)$", text)
        out[path.parent.name] = dict(path="workspace/%s/PROJECT.md" % path.parent.name, text=text,
                                     labels=None if m is None else split(m.group(1)),
                                     private=bool(re.search(r"(?m)^private:\s*true\s*$", text)))
    return out


def library(root):
    text = read(root, "kb/rules.md")
    if text is None:
        return None
    parts = re.split(r"(?m)^## (R-\d{3})[ \t]*$", text)

    def listing(key):
        found = re.search(r"(?m)^%s:(.*)$" % key, parts[0])
        return split(found.group(1)) if found else []
    entries = []
    for rid, body in zip(parts[1::2], parts[2::2]):
        entry = dict(id=rid)
        for line in body.split("\n"):
            m = re.match(r"([a-z]+): ?(.*)$", line)
            if m and m.group(1) not in entry:
                entry[m.group(1)] = m.group(2).strip()
        entry["labels"] = split(entry.get("labels"))
        entry["active"] = entry.get("status", "active").startswith("active")
        entries.append(entry)
    return dict(allowed=listing("labels-allowed"), proposed=listing("labels-proposed"), entries=entries)


def norm(line):
    text = re.sub(r"^- ", "", lf(line).strip())
    text = re.sub(r"^\(\d[^)]*\)\s*", "", re.sub(r"^constraints:\s*", "", text))
    return re.sub(r"(\s*\[[^\[\]]*\])+\s*$", "", text).strip()


def rules_check(root):
    lib = library(root)
    if lib is None:
        return ["no library: kb/rules.md absent"]
    allowed, drift, info = set(lib["allowed"]), [], []
    load = read(root, "kb/LOAD.md") or ""
    ids = set(re.findall(r"(?m)^\| ((?!when\b|---)[a-z-]+) \|", load)) if re.search(r"(?m)^\| when \|", load) else None
    if ids is None:
        info.append("when-unchecked")
    by_id, by_text = {}, {}
    for e in lib["entries"]:
        if e["id"] in by_id:
            drift.append("dup %s id" % e["id"])
        by_id.setdefault(e["id"], e)
        if e.get("text"):
            if by_text.get(norm(e["text"]), e["id"]) != e["id"]:
                drift.append("dup %s %s" % (e["id"], by_text[norm(e["text"])]))
            by_text.setdefault(norm(e["text"]), e["id"])
        drift += ["label %s %s" % (e["id"], x) for x in e["labels"] if x not in allowed and x != "?"]
        if ids is not None and e.get("when") not in ids | {"always", "?"}:
            drift.append("when %s %s" % (e["id"], e.get("when")))
    copies = {}
    for name, p in projects(root).items():
        if p["labels"] is None:
            info.append("unlabelled " + name)
        drift += ["label %s %s" % (name, x) for x in p["labels"] or [] if x not in allowed - {"all", "local"}]
        for n, line in enumerate(p["text"].split("\n"), 1):
            for rid in re.findall(r"\[(R-\d{3})\]", line):
                copies.setdefault(rid, []).append((p["path"], n, line))
    for rid, rows in sorted(copies.items()):
        e = by_id.get(rid)
        for path, n, line in rows:
            if e is None:
                drift.append("orphan [%s] %s:%d" % (rid, path, n))
            elif not e["active"]:
                drift.append("retired-copy %s %s:%d" % (rid, path, n))
            elif e.get("text") and norm(line) != norm(e["text"]):
                drift.append("text %s %s:%d" % (rid, path, n))
    for e in by_id.values():
        home = e.get("home", "")
        path = (home.split() or [""])[0]
        if not e["active"]:
            continue
        if path == "kb/rules.md" and e.get("text"):
            # An optional rule: the library entry is its home; it binds only where a project carries a tagged copy.
            continue
        body = read(root, path) if path and (root / path).is_file() else None
        if body is None:
            drift.append("missing-home %s %s" % (e["id"], home))
        elif e.get("text") and not any(row[0] == path for row in copies.get(e["id"], [])):
            hit = next((n for n, line in enumerate(body.split("\n"), 1) if norm(e["text"]) in norm(line)), None)
            if hit:
                info.append("untagged %s %s:%d" % (e["id"], path, hit))
            else:
                drift.append("missing-home %s %s" % (e["id"], home))
        elif not e.get("text") and "anchor" in e and body.count(e["anchor"]) != 1:
            drift.append("anchor %s %s" % (e["id"], home))
    return drift + info


def rules_for(root, labels, skip=()):
    lib = library(root)
    if lib is None:
        raise ValueError("no library: kb/rules.md absent")
    for x in labels:
        if x not in lib["allowed"]:
            raise ValueError(("label %s awaits #labels L0" if x in lib["proposed"] else "label %s is not in labels-allowed") % x)
    want = set(labels) - {"all", "local", "?"}
    return ["- (%s) %s  [%s]" % (today().isoformat(), e["text"], e["id"]) for e in lib["entries"]
            if e["active"] and e.get("text") and want & set(e["labels"]) and e["id"] not in skip]


def label_items(root):
    lib, projs = library(root), projects(root)
    items = ["labels:" + name for name, p in projs.items() if p["labels"] is None]
    allowed = set(lib["allowed"]) - {"all", "local"} if lib else set()
    for name, p in projs.items():
        have = set(re.findall(r"\[(R-\d{3})\]", p["text"]))
        items += ["%s:%s" % (name, e["id"]) for e in (lib or {}).get("entries", [])
                  if e["active"] and e.get("text") and set(e["labels"]) & set(p["labels"] or []) & allowed
                  and e["id"] not in have and e.get("home") != p["path"]]
    return items


# ---- lanes, seed and cards -------------------------------------------------------------------------

def lanes(root, recs, scope):
    out, day = {}, today().isoformat()
    data = (root / "inbox.md").read_bytes() if (root / "inbox.md").is_file() else b""
    routed = {m.group(1) for m in DONE.finditer(data)}
    cut = max([int(m.group(3)) for m in BEGIN.finditer(data) if m.group(1) in routed] + [m.end() for m in LEGACY.finditer(data)] + [0])
    dates = sorted(re.findall(r"(?m)^- (\d{4}-\d{2}-\d{2})", data[cut:].decode("utf-8", "replace")))
    if dates and age(dates[0]) >= 14:
        out["inbox"] = (["inbox:" + dates[0]], "#inbox · %d unrouted inbox lines, oldest %s (%d days) → route them in the deep pass "
                        "(§F 1b); y #inbox schedules that pass · later #inbox" % (len(dates), dates[0], age(dates[0])))
    due = [m.group(1) for m in re.finditer(r"(?m)^- (P-\d+) \|.*?\| due: (\d{4}-\d{2}-\d{2}) \| resolved: [–-][ \t]*(?:\||$)",
                                           read(root, "kb/predictions.md") or "") if m.group(2) <= day]
    if due:
        out["predict"] = (due, "#predict · %d predictions past due and unresolved: %s → resolve each in kb/predictions.md"
                          % (len(due), ", ".join(due)))
    late = [r for r in recs if not r["published"] and age(r["date"]) >= 2 and sees(scope, r["scope"])]
    if late:
        out["publish"] = ([r["id"][:8] for r in late], "#publish · %d records submitted but never published; the sole worker "
                          "runs coordination.py publish:\n" % len(late) + "\n".join("%s · %s · submitted %s" % (r["id"][:8], r["scope"], r["date"]) for r in late))
    items = label_items(root)
    if items:
        out["labels"] = (items, "#labels · give each project a labels: line, then copy each matching library rule, tagged "
                         "[R-###] (templates §G, §W):\n" + "\n".join(
                             i + (" — no labels: line" if i.startswith("labels:") else " — copy into that project's constraints:") for i in items))
    drift = [line for line in rules_check(root) if line.split()[0] in DRIFT]
    if drift:
        keys = list(dict.fromkeys(":".join(line.split()[:2]).replace("[", "").replace("]", "") for line in drift))
        out["rules-drift"] = (keys, "#rules-drift · kb/rules.md and its copies differ; fix both in one diff, the library wins "
                              "(rule 1):\n" + "\n".join(drift))
    return out


def load_seed(root):
    text = at_head(root, P + "/seed.md")
    if text is None:
        return None
    parts = re.split(r"(?m)^## card: ([a-z0-9-]+)[ \t]*$", text)

    def keys(block):
        return dict(re.findall(r"(?m)^([a-z-]+):[ \t]*(.*?)[ \t]*$", block))
    head = keys(parts[0])
    seed = dict(batches=[split(b) for b in head.get("batches", "").split("|")], drip=split(head.get("drip")), cards={})
    for cid, block in zip(parts[1::2], parts[2::2]):
        m = re.search(r"(?ms)^(.*?)^~~~[ \t]*\n(.*?)\n~~~[ \t]*$", block)
        if m:
            k = keys(m.group(1))
            seed["cards"][cid] = dict(cls=k.get("class", "checklist"), items=split(k.get("items")), records=split(k.get("records")), body=m.group(2))
    return seed


def card_path(ident, where=""):
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", ident or "") or ident in ("done", "rejected", "expired"):
        raise ValueError("bad card id: %s" % ident)
    return P + "/" + where + ident


def on_disk(root):
    found = []
    for where in ("", "done/", "rejected/", "expired/"):
        base = root / P / where
        for path in sorted(base.glob("*/item.json")) if base.is_dir() else []:
            found.append((where, json.loads(path.read_text(encoding="utf-8"))))
    return found


def load_item(root, ident):
    for where in ("", "done/", "rejected/", "expired/"):
        path = root / card_path(ident, where) / "item.json"
        if path.is_file():
            return where, json.loads(path.read_text(encoding="utf-8"))
    return None, {}


def save_item(root, rec):
    now, where = load_item(root, rec["id"])[0], FOLDER[rec["status"]]
    if now is not None and now != where:
        target = C.inside(root, card_path(rec["id"], where))
        target.parent.mkdir(parents=True, exist_ok=True)
        os.replace(str(C.inside(root, card_path(rec["id"], now))), str(target))
    write(root, card_path(rec["id"], where) + "/item.json", json.dumps(rec, indent=2, sort_keys=True, ensure_ascii=False) + "\n")


def fresh(ident, cls, lane, scope, records_=()):
    return {"id": ident, "class": cls, "lane": lane, "scope": scope or "project/system", "records": list(records_),
            "created": today().isoformat(), "status": "stub" if cls == "stub" else "open", "card_sha": "", "shown": {},
            "later_until": None, "reshow": False, "items": [], "covered": []}


def rulings(rec):
    return {i["id"]: i for i in rec.get("items", [])}


def status_of(items, rec):
    marks = [rulings(rec).get(i, {}).get("ruling") for i in items]
    if items and all(x in ("y", "n") for x in marks):
        return "rejected" if all(x == "n" for x in marks) else "done"
    return "stub" if rec.get("class") == "stub" else "open"


def view(cid, s, lane, rec):
    ruled, day = rulings(rec), today().isoformat()

    def settled(i):
        return ruled.get(i, {}).get("ruling") in ("y", "n")
    if s and s["items"] and (s["cls"] == "checklist" or lane) and not all(settled(i) for i in s["items"]):
        body, items, kind, seeded = s["body"], s["items"], s["cls"], True
    elif s and s["cls"] == "notes" and lane and not s["items"]:
        body, items, kind, seeded = s["body"], lane[0], "notes", False
    elif lane:
        body, items, kind, seeded = lane[1], [i for i in lane[0] if i not in rec.get("covered", [])], "lane", False
    else:
        return None
    if not items:
        return None
    pending = [i for i in items if not settled(i) and not (ruled.get(i, {}).get("ruling") == "later" and ruled[i].get("until", "") > day)]
    text = re.sub(r"(?m)^@@ [^\n]*? @@", "", lf(body + "\nitems: " + ", ".join(items)))
    return dict(id=cid, kind=kind, lane=cid if cid in LANE_CARDS else "seed", items=items, body=body, rec=rec, sha=sha(text),
                pending=pending, seeded=seeded, lane_items=lane[0] if lane else [], batch=None,
                listed=bool(pending) and (rec.get("later_until") or "") <= day)


def views(root, ctl, scope, recs):
    seed = load_seed(root) if ctl["backlog"] else None
    lane = lanes(root, recs, scope)
    order = [cid for batch in seed["batches"] for cid in batch] if seed else []
    batch = {cid: n for n, b in enumerate(seed["batches"]) for cid in b} if seed else {}
    out = []
    for cid in list(dict.fromkeys(order + [x for x in LANE_CARDS if x in lane])):
        s = seed["cards"].get(cid) if seed else None
        if (s and s["cls"] == "drip") or (s is None and cid not in lane):
            continue
        v = view(cid, s, lane.get(cid), load_item(root, cid)[1])
        if v:
            v["batch"] = batch.get(cid)
            out.append(v)
    for where, rec in on_disk(root):
        if where or rec.get("class") != "stub" or not sees(scope, rec.get("scope")):
            continue
        body = "#%s · shadow stub, information only (drafting arrives in a later step) · %s · record-id %s · %s" % (
            rec["id"], rec["lane"], ", ".join(r[:8] for r in rec["records"]), rec.get("scope"))
        v = view(rec["id"], None, ([rec["id"]], body), rec)
        v.update(kind="stub", lane=rec["lane"])
        out.append(v)
    return out


def choose(vs):
    listed = [v for v in vs if v["listed"]]
    batches = [v["batch"] for v in listed if v["batch"] is not None]
    first = [v for v in listed if batches and v["batch"] == min(batches)]
    return (first + [v for v in listed if v["batch"] is None and v["kind"] != "stub"] + [v for v in listed if v["kind"] == "stub"])[:4]


def render(v):
    ruled = rulings(v["rec"])

    def mark(i):
        r = ruled.get(i)
        return "open" if not r else "later until " + r.get("until", "?") if r["ruling"] == "later" else r["ruling"]
    return "\n=== #%s · %s · %s\nitems: %s\n%s" % (v["id"], v["kind"], v["lane"], " · ".join("%s %s" % (i, mark(i)) for i in v["items"]), v["body"])


# ---- housekeeping, relay line ------------------------------------------------------------------

def housekeep(root, ctl):
    for where, rec in on_disk(root):
        if not where and rec.get("class") == "stub" and age(rec.get("created")) >= STUB_DAYS:
            rec["status"] = "expired"
            save_item(root, rec)
            log(root, "expire", rec["id"], None, rec.get("lane"))
    st = state(root)
    if st.get("control", {}).get("logged") != ctl["hashes"]:
        log(root, "control", "control", None, "control", state=ctl["state"])
        st.setdefault("control", {})["logged"] = ctl["hashes"]
        save_state(root, st)


def sync(root, vs, scope):
    # A lane card whose condition cleared closes itself (moves to done/); only a scope that sees every lane does this.
    # A seed checklist card closes only by its rulings (S3.3), so one that `backlog: off` hides stays where it is.
    live, seed = {v["id"] for v in vs}, None
    for where, rec in on_disk(root) if sees(scope, None) else []:
        if where or rec.get("lane") not in LANE_CARDS or rec["id"] in live:
            continue
        seed = seed or load_seed(root) or {"cards": {}}
        s = seed["cards"].get(rec["id"])
        if s and s["cls"] == "checklist" and status_of(s["items"], rec) not in ("done", "rejected"):
            continue
        rec["status"] = "done"
        save_item(root, rec)


def deep_due(recs, st):
    last = max((r["date"] for r in recs if r["consolidated"]), default="")
    if (not last or age(last) >= 60) and (not st.get("deep_last") or age(st["deep_last"]) >= 7):
        return "deep pass due (last CONSOLIDATED %s)" % (last or "none")
    return ""


def summary(root, ctl, scope, recs, vs, named=()):
    st, parts = state(root), []
    if st.get("control", {}).get("seen") != ctl["hashes"]:
        parts.append("control changed: " + ctl["state"])
    if ctl["state"] == "on":
        parts.append("on needs a later drafting step; acting as shadow")
    parts += list(named)
    plan = (read(root, "schedule.md") or "").lower()
    owed = 0
    for r in recs:
        if r["date"] >= ctl["pool"] and sees(scope, r["scope"]):
            found = re.search(r"(?m)^owed:(.*)$", r["text"])
            owed += sum(1 for w in re.findall(r'\b(?:you|me)\s+"([^"]+)"', found.group(1) if found else "") if w.lower() not in plan)
    unsubmitted = 0
    for path in (root / "coordination/sessions").glob("*/session.json"):
        if not path.with_name("handoff.json").exists():
            info = C.load(path)
            unsubmitted += age(info.get("started")) >= 2 and sees(scope, info.get("scope"))
    counts = (("cards", sum(1 for v in vs if v["listed"] and v["kind"] != "stub")), ("stubs", sum(1 for v in vs if v["kind"] == "stub")),
              ("words?", candidates(root, ctl, scope, recs)[1]), ("unsubmitted", unsubmitted), ("owed", owed))
    parts += ["%s %d" % (label, n) for label, n in counts if n]
    parts += [x for x in [deep_due(recs, st)] if x]
    return ("EM · shadow: " + " · ".join(parts))[:220] if parts else "EM · —"


def relay(root, session, event):
    root = Path(root)
    ctl, why = control(root)
    if ctl is None or ctl["state"] in ("off", "paused"):
        return {"relay": off_line(ctl, why)}
    scope = session_info(root, session)["scope"]
    try:
        with locked(root):
            housekeep(root, ctl)
            recs, named = records(root), []
            if event == "submit" and ctl["drafts"] and slug(scope) in ctl["scopes"]:
                ripe = candidates(root, ctl, scope, recs)[0]
                if ripe and sum(1 for w, r in on_disk(root) if not w and r.get("class") == "stub") < CAP:
                    lane, les = ripe[0]
                    ident = hashlib.sha256((lane + "\n" + les["rec"]["id"]).encode("utf-8")).hexdigest()[:6]
                    save_item(root, fresh(ident, "stub", lane, les["rec"]["scope"], [les["rec"]["id"]]))
                    log(root, "stub", ident, session, lane)
                    named.append("would stage #%s (%s)" % (ident, lane))
            vs = views(root, ctl, scope, recs)
            sync(root, vs, scope)
            line, st = summary(root, ctl, scope, recs, vs, named), state(root)
            if deep_due(recs, st):
                st["deep_last"] = today().isoformat()
                save_state(root, st)
    except Busy:
        return {"relay": "EM · consolidation busy"}
    return {"relay": line}


# ---- subcommands ------------------------------------------------------------------------------

def statistics(root):
    rows = ledger_rows(root)
    stubs, words, shown, ruled = {}, {}, {}, {}
    for r in rows:
        ev, day = r.get("ev"), r.get("t", "")[:10]
        if ev == "stub":
            stubs[r.get("lane")] = stubs.get(r.get("lane"), 0) + 1
        if ev == "shown":
            shown.setdefault(r.get("id"), day)
        if ev in ("y", "n", "later", "reopen"):
            words[ev] = words.get(ev, 0) + 1
        if ev in ("y", "n", "later"):
            ruled.setdefault(r.get("id"), day)
    quick = [i for i, d in shown.items() if i in ruled and (date.fromisoformat(ruled[i]) - date.fromisoformat(d)).days <= 7]
    return {"stubs": stubs, "shown": sum(1 for r in rows if r.get("ev") == "shown"), "rulings": words,
            "ruled_within_7d": round(len(quick) / len(shown), 3) if shown else None,
            "reject_rate": {lane: round(n / (y + n), 3) for lane, (y, n) in tallies(rows).items()}}


def pending(root, scope, full, session, stats):
    if stats:
        print(json.dumps(statistics(root), indent=2, sort_keys=True))
        return 0
    ctl, why = control(root)
    if ctl is None or ctl["state"] in ("off", "paused"):
        print(off_line(ctl, why))
        return 0
    info = session_info(root, session) if session else None
    scope = scope or (info or {}).get("scope")
    record = full and info is not None and info.get("interactive") is True
    with locked(root) if record else nullcontext():
        if record:
            housekeep(root, ctl)
        recs = records(root)
        vs = views(root, ctl, scope, recs)
        if record:
            sync(root, vs, scope)
        print(summary(root, ctl, scope, recs, vs))
        if not full:
            cards = [v for v in vs if v["listed"] and v["kind"] != "stub"]
            if cards and not any(r.get("ev") == "shown" and r.get("t", "")[:10] == today().isoformat() for r in ledger_rows(root)):
                print("EM · waiting: %d cards, first #%s → say pending" % (len(cards), choose(cards)[0]["id"]))
            return 0
        # Seed and lane cards are kb items, shown in full only to project/system; another scope sees them as a count.
        mine = vs if sees(scope, "project/system") else [v for v in vs if v["kind"] == "stub"]
        held = 0 if mine is vs else sum(1 for v in vs if v["listed"] and v["kind"] != "stub")
        for v in choose(mine):
            print(render(v))
            if record:
                rec = v["rec"] or fresh(v["id"], "checklist", v["lane"], scope)
                rec.setdefault("shown", {})[session.lstrip("#")] = v["sha"]
                rec.update(card_sha=v["sha"], reshow=False, status="stub" if rec.get("class") == "stub" else "open")
                save_item(root, rec)
                log(root, "shown", v["id"], session.lstrip("#"), v["lane"])
        if held:
            print("EM · %d cards wait for a project/system session (kb items are reviewed only there)" % held)
        if record:
            st = state(root)
            st.setdefault("control", {})["seen"] = ctl["hashes"]
            save_state(root, st)
        elif info is not None:
            print("not interactive: nothing recorded")
    return 0


def owned(scope, ident, where):
    # Seed and lane cards are kb items: only project/system rules them; a stub belongs to its record's scope.
    if not sees(scope, where):
        raise ValueError("#%s is a %s card; rule it in a %s session" % (ident, where, where))


def reopen(root, ids, session, scope):
    plan, disk = [], on_disk(root)
    for x in ids:
        rec = load_item(root, x)[1] if re.fullmatch(r"[a-z0-9][a-z0-9-]*", x) else {}
        owner = rec or next((r for _, r in disk if x in rulings(r)), None)
        if not owner:
            raise ValueError("#%s is not a known card or ruled item" % x)
        owned(scope, owner["id"], owner.get("scope") if owner.get("class") == "stub" else "project/system")
        plan.append((x, owner, bool(rec)))
    for x, rec, whole in plan:
        rec.update(items=[] if whole else [i for i in rec["items"] if i["id"] != x], shown={}, reshow=False)
        if whole:
            rec.update(later_until=None, covered=[], created=today().isoformat() if rec.get("class") == "stub" else rec.get("created"))
        rec["status"] = "stub" if rec.get("class") == "stub" else "open"
        save_item(root, rec)
        log(root, "reopen", rec["id"], session, rec.get("lane"), items=[] if whole else [x])
    return "reopened " + ", ".join("#" + x for x, _, _ in plan)


def rule(root, word, ids, session, quote, reason="", skip="", labels=""):
    session, ids, skip = session.lstrip("#"), split(",".join(ids)), set(split(skip))
    if session_info(root, session).get("interactive") is not True:
        raise ValueError("rule needs an interactive session (coordination.py new --interactive)")
    ctl, why = control(root)
    if ctl is None or ctl["state"] in ("off", "paused"):
        raise ValueError(off_line(ctl, why))
    with locked(root):
        housekeep(root, ctl)
        scope = session_info(root, session)["scope"]
        vs = views(root, ctl, scope, records(root))
        sync(root, vs, scope)
        if word == "reopen":
            return reopen(root, ids, session, scope)
        cards, owner, plan = {v["id"]: v for v in vs}, {i: v for v in vs for i in v["items"]}, []
        for x in ids:
            v = cards.get(x) or owner.get(x)
            if v is None:
                raise ValueError("#%s is not an open card or item" % x)
            owned(scope, v["id"], v["rec"].get("scope") if v["kind"] == "stub" else "project/system")
            if v["rec"].get("shown", {}).get(session) != v["sha"]:
                raise ValueError("#%s was not shown in this session with its current text; run pending --full --session first" % v["id"])
            if word == "y" and v["rec"].get("reshow"):
                raise ValueError("#%s changed labels since it was shown; show it again before another y (rule 5)" % v["id"])
            plan.append((x, v))
        done, day = [], today()
        for x, v in plan:
            rec, chosen = v["rec"], ([i for i in v["pending"] if i not in skip] if x == v["id"] else [x])
            if word == "later" and x == v["id"]:
                rec["later_until"], chosen = (day + timedelta(days=LATER_DAYS)).isoformat(), []
            entries = rulings(rec)
            for i in chosen:
                entries[i] = dict(id=i, ruling=word, quote=quote, session=session, date=day.isoformat(), reason=reason, labels=split(labels))
                if word == "later":
                    entries[i]["until"] = (day + timedelta(days=LATER_DAYS)).isoformat()
            rec["items"] = list(entries.values())
            rec["reshow"] = rec.get("reshow") or bool(labels and word == "y")
            if v["seeded"] and all(entries.get(i, {}).get("ruling") in ("y", "n") for i in v["items"]):
                rec["covered"] = sorted(set(rec.get("covered", [])) | set(v["lane_items"]))
            rec["status"] = status_of(v["items"], rec)
            save_item(root, rec)
            log(root, word, v["id"], session, v["lane"], items=chosen)
            done.append("#%s%s → %s" % (v["id"], ": " + ", ".join(chosen) if chosen and chosen != [v["id"]] else "", rec["status"]))
        return "ruled %s %s" % (word, "; ".join(done))


def rules_cmd(root, labels, project, check):
    if check:
        lines = rules_check(root)
        if lines:
            print("\n".join(lines))
        return 0
    if project:
        p = projects(root).get(project)
        if p is None:
            raise ValueError("no project " + project)
        if p["labels"] is None:
            print("unlabelled " + project)
            return 0
        homed = {e["id"] for e in (library(root) or {}).get("entries", []) if e.get("home") == p["path"]}
        lines = rules_for(root, p["labels"], set(re.findall(r"\[(R-\d{3})\]", p["text"])) | homed)
    else:
        lines = rules_for(root, split(labels))
    if lines:
        print("\n".join(lines))
    return 0


def main(root, argv):
    root = Path(root)
    if argv and argv[0] in ("stage", "apply"):
        print("coordination: %s arrives with a later drafting step" % argv[0], file=sys.stderr)
        return 1
    parser = Parser(prog="coordination.py", description="Consolidation review, read side.")
    sub = parser.add_subparsers(dest="word", required=True)
    pen = sub.add_parser("pending")
    pen.add_argument("--scope")
    pen.add_argument("--full", action="store_true")
    pen.add_argument("--session")
    pen.add_argument("--stats", action="store_true")
    word = sub.add_parser("rule")
    word.add_argument("verb", choices=["y", "n", "later", "reopen"])
    word.add_argument("ids", nargs="+")
    word.add_argument("--session", required=True)
    word.add_argument("--quote", required=True)
    word.add_argument("--reason", default="")
    word.add_argument("--except", dest="skip", default="")
    word.add_argument("--labels", default="")
    lib = sub.add_parser("rules").add_mutually_exclusive_group(required=True)
    lib.add_argument("--labels")
    lib.add_argument("--project")
    lib.add_argument("--check", action="store_true")
    try:
        args = parser.parse_args(argv)
        if args.word == "pending":
            return pending(root, args.scope, args.full, args.session, args.stats)
        if args.word == "rule":
            print(rule(root, args.verb, args.ids, args.session, args.quote, args.reason, args.skip, args.labels))
            return 0
        return rules_cmd(root, args.labels, args.project, args.check)
    except Busy:
        print("EM · consolidation busy")
        return 1
    except (ValueError, OSError, KeyError) as exc:
        print("coordination: " + str(exc), file=sys.stderr)
        return 1
