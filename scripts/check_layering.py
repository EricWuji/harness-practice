#!/usr/bin/env python3
from pathlib import Path
import re
import sys

LAYERS = ["Types", "Config", "Repo", "Service", "Runtime", "UI"]
INDEX = {name: i for i, name in enumerate(LAYERS)}

# Heuristic patterns for common languages / path-style refs.
PATTERNS = [
    re.compile(r"\bfrom\s+([A-Za-z_][\w./-]*)\s+import\b"),
    re.compile(r"\bimport\s+([A-Za-z_][\w./-]*)\b"),
    re.compile(r"require\(['\"]([^'\"]+)['\"]\)"),
    re.compile(r"from\s+['\"]([^'\"]+)['\"]"),
]

TEXT_EXT = {".py", ".ts", ".tsx", ".js", ".jsx", ".go", ".java", ".kt", ".rs", ".md"}

violations = []
for layer in LAYERS:
    root = Path(layer)
    if not root.exists():
        continue
    for p in root.rglob("*"):
        if not p.is_file() or p.suffix not in TEXT_EXT:
            continue
        txt = p.read_text(encoding="utf-8", errors="ignore")
        refs = set()
        for pat in PATTERNS:
            refs.update(m.group(1) for m in pat.finditer(txt))

        for ref in refs:
            for target in LAYERS:
                token = target + "/"
                mod = target + "."
                if ref == target or ref.startswith(token) or ref.startswith(mod):
                    if INDEX[target] > INDEX[layer]:
                        violations.append(f"{p}: {layer} cannot depend on upper layer {target} via '{ref}'")

if violations:
    print("Layering violations detected:")
    for v in violations:
        print("-", v)
    sys.exit(1)

print("Layering check passed: no reverse dependencies found.")
