# Validate an archify architecture IR and apply the validator's labelAt suggestions until it passes.
# Usage: python archify_autofix.py <ir.json> [--archify <path to archify checkout>] [--keep "label1" "label2" ...]
# The archify checkout is `git clone https://github.com/tt-a1i/archify` (MIT); default path: env ARCHIFY or ../../../archify.
import io, json, os, re, subprocess, sys
args = sys.argv[1:]
ir_path = args[0]
archify = os.environ.get("ARCHIFY", os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "archify"))
keep = []
if "--archify" in args: archify = args[args.index("--archify") + 1]
if "--keep" in args: keep = args[args.index("--keep") + 1:]
bin_ = os.path.join(archify, "archify", "bin", "archify.mjs")

def validate():
    r = subprocess.run(["node", bin_, "validate", "architecture", ir_path, "--quality", "showcase", "--json"], capture_output=True, text=True, encoding="utf-8")
    try: return json.loads(r.stdout)
    except Exception: return {"raw": r.stdout + r.stderr}

for rnd in range(10):
    d = validate()
    if "raw" in d: print(d["raw"][:3000]); sys.exit(1)
    diags = d.get("diagnostics", [])
    if d.get("ok"): print("OK after", rnd, "rounds"); sys.exit(0)
    ir = json.load(io.open(ir_path, encoding="utf-8")); applied = 0
    for x in diags:
        m = re.search(r'Label "(.+?)" overlaps .*?Suggested fix: labelAt \[(-?\d+), (-?\d+)\]', x.get("message", ""), re.S)
        if not m: continue
        lab, ax, ay = m.group(1), int(m.group(2)), int(m.group(3))
        if lab in keep: continue
        for c in ir["connections"]:
            if c["label"] == lab and c.get("labelAt") != [ax, ay]:
                c["labelAt"] = [ax, ay]; applied += 1; break
    io.open(ir_path, "w", encoding="utf-8", newline="\n").write(json.dumps(ir, ensure_ascii=False, indent=2))
    print(f"round {rnd}: {len(diags)} diagnostics, applied {applied} labelAt fixes")
    if applied == 0:
        for x in diags[:40]: print("-", x.get("code"), "|", x.get("message", "")[:500].replace("\n", " "))
        sys.exit(2)
