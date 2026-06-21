#!/usr/bin/env python3
"""Small public-release audit for the BioSymphony small-molecules skill."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


TEXT_SUFFIXES = {
    ".cff",
    ".css",
    ".html",
    ".in",
    ".json",
    ".md",
    ".mol2",
    ".pdb",
    ".py",
    ".sdf",
    ".sh",
    ".svg",
    ".toml",
    ".ts",
    ".tsx",
    ".txt",
    ".yaml",
    ".yml",
}

SKIP_DIRS = {
    ".git",
    ".runtime",
    "__pycache__",
    ".venv",
    "venv",
    "env",
    "node_modules",
    "prep",
    "dock",
    "cofold_chai",
    "cofold_boltz",
    "decoys",
}

BLOCK_PATTERNS = [
    re.compile(r"/Users/[A-Za-z0-9._-]+/"),
    re.compile(r"(?i)\bgithub[_-]?\d*/[^\s]*-private\b"),
    re.compile(r"(?i)\b[A-Za-z0-9_.-]+-private\b"),
    re.compile(r"(?i)(api[_-]?key|secret|token|password)\s*[:=]\s*['\"][^'\"\s]{8,}"),
    re.compile(r"(?i)(pod[_ -]?id|network volume id)\s*[:=]"),
]

ALLOWED_PHRASES = {
    "No API keys, provider credentials, signed URLs, SSH keys, or registry auth",
    "API keys, provider credentials, signed URLs, SSH keys, or registry auth",
}

LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")

STYLE_FILES = {
    "README.md",
    "SKILL.md",
    "AGENTS.md",
    "PUBLIC_RELEASE.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "demos/kras-glue/README.md",
}

STYLE_PATTERNS = [
    (re.compile(r"[—–]"), "avoid em dashes and en dashes in front-door docs"),
    (re.compile(r"[→←]"), "avoid symbolic arrows in front-door docs"),
    (re.compile(r"(?i)\bfootgun\b"), "avoid informal warning language"),
    (re.compile(r"(?i)\bhard-won\b"), "avoid defensive section framing"),
    (re.compile(r"(?i)\b(jury|augist|august)\b"), "avoid unclear public-facing terms"),
]


def iter_files(root: Path):
    for path in root.rglob("*"):
        if any(part in SKIP_DIRS for part in path.relative_to(root).parts):
            continue
        if path.is_file():
            yield path


def is_text(path: Path) -> bool:
    return path.suffix.lower() in TEXT_SUFFIXES or path.name in {"Makefile", "LICENSE"}


def audit_text(root: Path) -> list[str]:
    failures: list[str] = []
    for path in iter_files(root):
        if not is_text(path):
            continue
        if path.relative_to(root).as_posix() == "scripts/public_audit.py":
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            failures.append(f"{path}: text-like file is not UTF-8")
            continue
        for i, line in enumerate(text.splitlines(), 1):
            if line.strip() in ALLOWED_PHRASES:
                continue
            for pat in BLOCK_PATTERNS:
                if pat.search(line):
                    rel = path.relative_to(root)
                    failures.append(f"{rel}:{i}: blocked pattern: {pat.pattern}")
    return failures


def audit_sizes(root: Path, max_mb: int) -> list[str]:
    failures: list[str] = []
    limit = max_mb * 1024 * 1024
    for path in iter_files(root):
        if path.stat().st_size > limit:
            rel = path.relative_to(root)
            failures.append(f"{rel}: file exceeds {max_mb} MB")
    return failures


def audit_links(root: Path) -> list[str]:
    failures: list[str] = []
    for path in iter_files(root):
        if path.suffix.lower() != ".md":
            continue
        text = path.read_text(encoding="utf-8")
        for i, line in enumerate(text.splitlines(), 1):
            for match in LINK_RE.finditer(line):
                target = match.group(1).split("#", 1)[0]
                if not target or target.startswith(("http://", "https://", "mailto:")):
                    continue
                if target.startswith("<") and target.endswith(">"):
                    target = target[1:-1]
                if not (path.parent / target).exists():
                    rel = path.relative_to(root)
                    failures.append(f"{rel}:{i}: missing local link target {target}")
    return failures


def audit_style(root: Path) -> list[str]:
    failures: list[str] = []
    for rel_path in sorted(STYLE_FILES):
        path = root / rel_path
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        for i, line in enumerate(text.splitlines(), 1):
            for pat, message in STYLE_PATTERNS:
                if pat.search(line):
                    failures.append(f"{rel_path}:{i}: {message}")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", nargs="?", default=".")
    parser.add_argument("--links-only", action="store_true")
    parser.add_argument("--style-only", action="store_true")
    parser.add_argument("--max-mb", type=int, default=10)
    args = parser.parse_args()

    root = Path(args.root).resolve()
    if args.style_only:
        failures = audit_style(root)
    else:
        failures = audit_links(root)
    if not args.links_only and not args.style_only:
        failures.extend(audit_text(root))
        failures.extend(audit_sizes(root, args.max_mb))
        failures.extend(audit_style(root))

    if failures:
        for failure in failures:
            print(failure)
        return 1
    print("public audit passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
