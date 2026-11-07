"""Session Tracker: append-only JSONL log with a readable TXT view.

Usage:
  python -I tracker/tracker.py check
  python -I tracker/tracker.py render
  python -I tracker/tracker.py add '<json object>'
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
LOG = HERE / "sessions.jsonl"
TXT = HERE / "sessions.txt"

REQUIRED = ("ts", "session", "title", "device", "kind", "evidence", "status", "by")
KINDS = {"start", "restart", "compact", "conn_lost", "limit", "crash", "archived",
         "renamed", "message", "trust", "observation", "handoff"}
STATUSES = {"VERIFIED", "REPORTED", "PROPOSED", "UNKNOWN"}
TS_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")


def validate(entry):
    """Return a list of problems with one entry; empty list means valid."""
    if not isinstance(entry, dict):
        return ["not a JSON object"]
    problems = [f"missing field: {f}" for f in REQUIRED if not entry.get(f)]
    if entry.get("ts") and not TS_RE.match(entry["ts"]):
        problems.append(f"bad ts: {entry['ts']}")
    if entry.get("kind") and entry["kind"] not in KINDS:
        problems.append(f"unknown kind: {entry['kind']}")
    if entry.get("status") and entry["status"] not in STATUSES:
        problems.append(f"unknown status: {entry['status']}")
    if entry.get("ts_precision", "exact") not in ("exact", "approx"):
        problems.append(f"bad ts_precision: {entry['ts_precision']}")
    return problems


def load():
    entries, problems = [], []
    if not LOG.exists():
        return entries, problems
    for n, line in enumerate(LOG.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            entry = json.loads(line)
        except json.JSONDecodeError as e:
            problems.append(f"line {n}: invalid JSON ({e.msg})")
            continue
        problems += [f"line {n}: {p}" for p in validate(entry)]
        entries.append(entry)
    return entries, problems


def render(entries):
    lines = ["SESSION TRACKER · KOMPAS / MasterBase",
             "Генерирано от sessions.jsonl. Не редактирай на ръка.", ""]
    for e in sorted(entries, key=lambda x: x["ts"]):
        approx = " ~" if e.get("ts_precision") == "approx" else ""
        lines.append(f"{e['ts']}{approx} | {e['status']:<8} | {e['kind']:<11} | "
                     f"{e['title']} [{e['device']}]")
        lines.append(f"    доказателство: {e['evidence']}")
        if e.get("note"):
            lines.append(f"    бележка: {e['note']}")
        lines.append(f"    записал: {e['by']}")
    TXT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main(argv):
    if len(argv) < 2 or argv[1] not in ("check", "render", "add"):
        print(__doc__)
        return 2
    cmd = argv[1]
    if cmd == "add":
        if len(argv) != 3:
            print("add needs exactly one JSON argument")
            return 2
        entry = json.loads(argv[2])
        problems = validate(entry)
        if problems:
            print("REFUSED: " + "; ".join(problems))
            return 1
        with LOG.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        print("ADDED")
        return 0
    entries, problems = load()
    if problems:
        print("\n".join(problems))
        return 1
    if cmd == "render":
        render(entries)
    print(f"OK: {len(entries)} entries")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
