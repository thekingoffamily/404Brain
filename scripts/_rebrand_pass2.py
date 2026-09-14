"""Second pass: BrainFoo → BrainFoo, BRAIN_ → BRAIN_, leftover paths."""
from __future__ import annotations

import os
import re
from pathlib import Path

ROOT = Path(r"c:\Users\palapalaru\Desktop\404Brain")
SKIP = {".git", "node_modules", "out", ".build", ".tmp", ".tmp2", "coverage", "articles", ".cursor", "__pycache__"}

TEXT_EXTS = {
    ".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs", ".json", ".md", ".css", ".scss",
    ".html", ".yml", ".yaml", ".txt", ".bat", ".sh", ".ps1", ".xml", ".iss", ".desktop",
    ".gitignore", ".py",
}

# Order matters
SUBS = [
    (re.compile(r"\bvoideditor\b"), "thekingoffamily"),  # org refs → ours where possible
    (re.compile(r"github\.com/thekingoffamily/void\b"), "github.com/thekingoffamily/404Brain"),
    (re.compile(r"github\.com/thekingoffamily/brain-builder\b"), "github.com/thekingoffamily/404Brain"),
    (re.compile(r"\bbrainVoid"), "brain"),
    (re.compile(r"\bBrainVoid"), "Brain"),
    (re.compile(r"\bVOID_"), "BRAIN_"),
    (re.compile(r"\bVOID([A-Z][A-Za-z0-9_]*)"), r"BRAIN\1"),
    (re.compile(r"\bVoid([A-Za-z0-9_]+)"), r"Brain\1"),
    (re.compile(r"\bVoid\b"), "Brain"),
    (re.compile(r"\bVOID\b"), "BRAIN"),
    (re.compile(r"inno-brain"), "inno-brain"),
    (re.compile(r"void\.css"), "brain.css"),
    (re.compile(r"void\.desktop"), "brain.desktop"),
    (re.compile(r"void\.png"), "brain.png"),
    (re.compile(r"\.brainrules"), ".brainrules"),
    (re.compile(r"workbench/brain/"), "workbench/brain/"),
    (re.compile(r"brain_icons"), "brain_icons"),
    (re.compile(r"brain_cube"), "brain_cube"),
    (re.compile(r"slice_of_brain"), "slice_of_brain"),
]


def walk_files():
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP and not d.startswith("out-")]
        for fn in filenames:
            yield Path(dirpath) / fn


def transform(s: str) -> str:
    for rx, rep in SUBS:
        s = rx.sub(rep, s)
    return s


def main():
    changed = 0
    for p in walk_files():
        if p.suffix.lower() not in TEXT_EXTS and p.name not in {".gitignore", ".brainrules", ".brainrules"}:
            continue
        try:
            raw = p.read_bytes()
        except OSError:
            continue
        if b"\0" in raw[:2048]:
            continue
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError:
            continue
        new = transform(text)
        if new != text:
            p.write_text(new, encoding="utf-8", newline="\n")
            changed += 1
            print("edit", p.relative_to(ROOT))

    # rename leftover path names
    paths = sorted(walk_files(), key=lambda x: len(x.parts), reverse=True)
    dirs = []
    for dirpath, dirnames, _ in os.walk(ROOT, topdown=False):
        for d in dirnames:
            if d in SKIP:
                continue
            dirs.append(Path(dirpath) / d)
    dirs = sorted(dirs, key=lambda x: len(x.parts), reverse=True)

    def ren(p: Path):
        name = p.name
        new = name
        new = new.replace("inno-brain", "inno-brain")
        new = new.replace("brain.css", "brain.css")
        new = new.replace("brain.desktop", "brain.desktop")
        new = new.replace("brain.png", "brain.png")
        new = new.replace(".brainrules", ".brainrules")
        new = new.replace("brain_icons", "brain_icons")
        new = re.sub(r"^void$", "brain", new)
        new = re.sub(r"^Brain", "Brain", new)
        new = re.sub(r"^BRAIN", "BRAIN", new)
        if new != name and not (p.with_name(new)).exists():
            print("REN", p.relative_to(ROOT), "->", new)
            p.rename(p.with_name(new))

    for p in paths:
        if p.exists():
            ren(p)
    for d in dirs:
        if d.exists():
            ren(d)

    print("content changed", changed)


if __name__ == "__main__":
    main()
