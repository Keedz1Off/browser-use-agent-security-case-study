"""Offline integrity checks; no network, target execution or writes."""
import hashlib
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote

def main():
    root = Path(__file__).resolve().parent
    manifest = json.loads((root / "MANIFEST.json").read_text(encoding="utf-8"))
    errors = []
    checked = 0
    for name, expected in manifest["files"].items():
        relative = Path(name)
        path = (root / relative).resolve()
        if relative.is_absolute() or not path.is_relative_to(root):
            errors.append("unsafe manifest path: " + name)
            continue
        if not path.is_file():
            errors.append("missing file: " + name)
            continue
        data = path.read_bytes()
        if len(data) != expected["bytes"] or hashlib.sha256(data).hexdigest() != expected["sha256"]:
            errors.append("digest or size mismatch: " + name)
        checked += 1
    links = 0
    for name in manifest["files"]:
        if not name.endswith(".md"):
            continue
        source = root / name
        for link in re.findall(r"\]\(([^)]+)\)", source.read_text(encoding="utf-8")):
            target = link.strip().strip("<>").split("#", 1)[0]
            if not target or re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target):
                continue
            resolved = (source.parent / unquote(target)).resolve()
            if not resolved.is_relative_to(root) or not resolved.exists():
                errors.append("broken/unsafe local link in " + name + ": " + link)
            links += 1
    result = {"files_checked": checked, "local_links_checked": links,
              "errors": errors, "scope": "offline package integrity, not target replay"}
    print(json.dumps(result, indent=2))
    return 1 if errors else 0

if __name__ == "__main__":
    sys.exit(main())
