#!/usr/bin/env python3
"""
Pre-publish scanner for the portfolio repository.

Usage:
    python scripts/scan_sensitive.py

Exit code 0 — no findings, 1 — findings found.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SELF = Path(__file__).resolve()

SKIP_DIRS = {".git", ".idea", ".vscode", "__pycache__", "node_modules"}
TEXT_SUFFIXES = {
    ".md", ".txt", ".yaml", ".yml", ".json", ".puml", ".svg",
    ".html", ".css", ".js", ".ts", ".py", ".ps1", ".xml", ".csv",
}

# Terms that must not appear in a public portfolio.
# Keep this list short and specific to avoid false positives.
FORBIDDEN_TERMS = [
    # employer / client / bank names
    "Иннотех", "Innotech", "ВТБ", "VTB", "Сбербанк", "Сбер", "Альфа-Банк",
    "Беларусбанк", "БПС-Банк", "Приорбанк",
    # internal systems and modules (examples from the source diagrams)
    "IBBOSS", "ПП Касса", "ОПС КП", "ЦФТ", "ПЦ", "91204",
    "product_instance", "pmlngotsClient", "gold_storage_order",
    "agreement_end_date", "agreement_account", "subject_ogress", "subject_swift",
    "ОПЦ",
    # personal data from the source documents
    "Юшкевич", "yv10082006", "+375 (25) 721-51-48", "+375257215148",
    # internal endpoints / identifiers
    "/product_instance/", "/pmlngotsClient/", "/pp_operation/",
]

REGEXES = [
    # phone numbers (Belarus / Russia)
    (re.compile(r"\+375\s?\(?\d{2}\)?\s?\d{3}[-\s]?\d{2}[-\s]?\d{2}"), "phone number"),
    (re.compile(r"\+7\s?\(?\d{3}\)?\s?\d{3}[-\s]?\d{2}[-\s]?\d{2}"), "phone number"),
    # emails
    (re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"), "email"),
    # secrets
    (re.compile(r"-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----"), "private key"),
    (re.compile(r"(?i)\b(password|passwd|pwd|secret|api[_-]?key|access[_-]?token)\s*[:=]\s*['\"]?[^\s'\"]{6,}"), "possible secret"),
    # internal hostnames
    (re.compile(r"https?://[a-z0-9.-]*(confluence|jira|gitlab|nexus|artifactory)\.[a-z0-9.-]+", re.I), "internal URL"),
]

# Known-safe exceptions (documentation examples, public contacts of the author).
ALLOWLIST = {
    "yv10082006@gmail.com",
    "https://github.com/Balur77/cv_yushkevich",
    "github.com/Balur77/cv_yushkevich",
}


def is_text_file(path: Path) -> bool:
    if path.suffix.lower() not in TEXT_SUFFIXES:
        return False
    try:
        path.read_text(encoding="utf-8")
        return True
    except (UnicodeDecodeError, OSError):
        return False


def scan_file(path: Path) -> list[tuple[int, str, str]]:
    findings: list[tuple[int, str, str]] = []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (UnicodeDecodeError, OSError):
        return findings

    for number, line in enumerate(lines, start=1):
        # Skip allowlisted public contacts.
        cleaned = line
        for allowed in ALLOWLIST:
            cleaned = cleaned.replace(allowed, "")

        for term in FORBIDDEN_TERMS:
            if term.lower() in cleaned.lower():
                findings.append((number, term, line.strip()[:200]))

        for pattern, label in REGEXES:
            for match in pattern.finditer(cleaned):
                findings.append((number, f"{label}: {match.group(0)}", line.strip()[:200]))

    return findings


def main() -> int:
    all_findings: list[tuple[Path, int, str, str]] = []

    for path in sorted(ROOT.rglob("*")):
        if not path.is_file():
            continue
        if path.resolve() == SELF:
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if not is_text_file(path):
            continue

        for number, term, line in scan_file(path):
            all_findings.append((path.relative_to(ROOT), number, term, line))

    if not all_findings:
        print("OK: no sensitive terms found.")
        return 0

    print(f"FOUND {len(all_findings)} potential issue(s):\n")
    for rel, number, term, line in all_findings:
        print(f"{rel}:{number}: [{term}]")
        print(f"    {line}")
    print("\nReview each finding manually. Exit code: 1")
    return 1


if __name__ == "__main__":
    sys.exit(main())
