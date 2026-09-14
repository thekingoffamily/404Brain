"""
Rebrand filesystem + text: Brain product → Brain.
Does NOT rewrite TypeScript keyword `void` (return types etc.).
"""
from __future__ import annotations

import os
import re
import sys
from pathlib import Path

ROOT = Path(r"c:\Users\palapalaru\Desktop\404Brain")

SKIP_DIR_NAMES = {
    ".git",
    "node_modules",
    "out",
    ".build",
    ".tmp",
    ".tmp2",
    "coverage",
    "articles",
    ".cursor",
}

TEXT_EXTS = {
    ".ts",
    ".tsx",
    ".js",
    ".jsx",
    ".mjs",
    ".cjs",
    ".json",
    ".md",
    ".css",
    ".scss",
    ".html",
    ".htm",
    ".svg",
    ".yml",
    ".yaml",
    ".txt",
    ".bat",
    ".sh",
    ".ps1",
    ".xml",
    ".code-workspace",
    ".nvmrc",
    ".gitignore",
    ".editorconfig",
}

# Longest-first path / brand tokens
TOKEN_REPLACEMENTS: list[tuple[str, str]] = [
    ("BRAIN_CODEBASE_GUIDE", "BRAIN_CODEBASE_GUIDE"),
    ("slice_of_brain", "slice_of_brain"),
    ("brain_cube_noshadow", "brain_cube_noshadow"),
    ("void-editor-widgets-tsx", "brain-editor-widgets-tsx"),
    ("void-settings-tsx", "brain-settings-tsx"),
    ("void-onboarding", "brain-onboarding"),
    ("void-tooltip", "brain-tooltip"),
    ("void.contribution", "brain.contribution"),
    ("contrib/void", "contrib/brain"),
    ("contrib\\void", "contrib\\brain"),
    ("brain_icons", "brain_icons"),
    ("voidVersion", "brainVersion"),
    ("voidRelease", "brainRelease"),
    ("IVoid", "IBrain"),
    ("@@void-", "@@brain-"),
    ("text-void-", "text-brain-"),
    ("bg-void-", "bg-brain-"),
    ("border-void-", "border-brain-"),
    ("ring-void-", "ring-brain-"),
    ("from-void-", "from-brain-"),
    ("to-void-", "to-brain-"),
    ("divide-void-", "divide-brain-"),
    ("placeholder-void-", "placeholder-brain-"),
    ("caret-void-", "caret-brain-"),
    ("outline-void-", "outline-brain-"),
    ("decoration-void-", "decoration-brain-"),
    ("accent-void-", "accent-brain-"),
    ("fill-void-", "fill-brain-"),
    ("stroke-void-", "stroke-brain-"),
    ("shadow-void-", "shadow-brain-"),
    (".void-", ".brain-"),
    ("'void.", "'brain."),
    ('"void.', '"brain.'),
    ("`void.", "`brain."),
    ("void-tunnelservice", "brain-tunnelservice"),
    ("void-tunnel", "brain-tunnel"),
]

# Identifier camelCase: voidSettings → brainSettings (not TS keyword)
CAMEL_VOID = re.compile(r"\bvoid([A-Z][A-Za-z0-9_]*)")
# CSS / kebab leftover void-foo (not already replaced)
KEBAB_VOID = re.compile(r"(?<![A-Za-z0-9_])void-")
# snake leftover void_foo
SNAKE_VOID = re.compile(r"(?<![A-Za-z0-9_])void_")
# Capital brand Brain / BRAIN
CAP_VOID = re.compile(r"\bVoid\b")
ALLCAP_VOID = re.compile(r"\bVOID\b")


def should_skip_dir(name: str) -> bool:
    return name in SKIP_DIR_NAMES or name.startswith("out-")


def iter_files(root: Path):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if not should_skip_dir(d)]
        for fn in filenames:
            yield Path(dirpath) / fn


def transform_text(s: str) -> str:
    for a, b in TOKEN_REPLACEMENTS:
        s = s.replace(a, b)
    s = CAMEL_VOID.sub(r"brain\1", s)
    s = KEBAB_VOID.sub("brain-", s)
    s = SNAKE_VOID.sub("brain_", s)
    s = CAP_VOID.sub("Brain", s)
    s = ALLCAP_VOID.sub("BRAIN", s)
    return s


def is_text_file(p: Path) -> bool:
    if p.suffix.lower() in TEXT_EXTS:
        return True
    if p.name in {".gitignore", ".nvmrc", "Dockerfile", "Makefile"}:
        return True
    return False


def rewrite_contents() -> int:
    changed = 0
    for p in iter_files(ROOT):
        if not is_text_file(p):
            continue
        try:
            raw = p.read_bytes()
        except OSError:
            continue
        if b"\0" in raw[:4096]:
            continue
        for enc in ("utf-8", "utf-8-sig", "latin-1"):
            try:
                text = raw.decode(enc)
                break
            except UnicodeDecodeError:
                text = None
        else:
            continue
        new = transform_text(text)
        if new != text:
            p.write_text(new, encoding="utf-8", newline="\n")
            changed += 1
    return changed


def rename_path_component(name: str) -> str:
    n = name
    for a, b in TOKEN_REPLACEMENTS:
        # only apply tokens that look like path fragments
        if "/" in a or "\\" in a:
            continue
        n = n.replace(a, b)
    n = n.replace("Brain", "Brain").replace("BRAIN", "BRAIN")
    # voidFoo / void-foo / void_foo in filenames
    if n.lower().startswith("void") and not n.lower().startswith("void."):
        # voidOnboarding.tsx etc already Brain→Brain; lowercase voidX
        n2 = CAMEL_VOID.sub(r"brain\1", n)
        n2 = KEBAB_VOID.sub("brain-", n2)
        n2 = SNAKE_VOID.sub("brain_", n2)
        n = n2
    # exact folder/file "void"
    if n == "void":
        n = "brain"
    return n


def rename_tree() -> int:
    # deepest paths first
    all_paths = sorted(iter_files(ROOT), key=lambda p: len(p.parts), reverse=True)
    # also dirs
    dirs = []
    for dirpath, dirnames, _ in os.walk(ROOT, topdown=False):
        for d in dirnames:
            if should_skip_dir(d):
                continue
            dirs.append(Path(dirpath) / d)
    dirs = sorted(dirs, key=lambda p: len(p.parts), reverse=True)

    renames = 0

    def rename_one(p: Path) -> Path:
        nonlocal renames
        new_name = rename_path_component(p.name)
        if new_name == p.name:
            return p
        dest = p.with_name(new_name)
        if dest.exists():
            print("SKIP exists:", dest)
            return p
        p.rename(dest)
        renames += 1
        print("REN", p.relative_to(ROOT), "->", dest.relative_to(ROOT))
        return dest

    for p in all_paths:
        if p.exists():
            rename_one(p)
    for d in dirs:
        if d.exists():
            rename_one(d)
    return renames


def main() -> int:
    print("rewrite contents...")
    c = rewrite_contents()
    print("files content changed:", c)
    print("rename paths...")
    r = rename_tree()
    print("paths renamed:", r)
    # second pass content (imports may still mention old after first rename of only names)
    c2 = rewrite_contents()
    print("second content pass:", c2)
    return 0


if __name__ == "__main__":
    sys.exit(main())
