#!/usr/bin/env python3
"""Extract translatable string leaves from JSON, YAML and Java .properties resources.

Examples:
  python3 scripts/extract_i18n.py ./src/locales --root ./src/locales --output /tmp/copy.jsonl
  python3 scripts/extract_i18n.py ./locales/en-US.json --locale en-US --format csv --output copy.csv
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path
from typing import Any, Iterable

SUPPORTED = {".json", ".yaml", ".yml", ".properties"}
LOCALE_RE = re.compile(r"(?i)(?<![A-Za-z])([a-z]{2,3}(?:[-_][A-Za-z0-9]{2,8})+)(?![A-Za-z])")
SKIP_DIRS = {".git", ".svn", "node_modules", "vendor", "build", "dist", "__pycache__"}


def infer_locale(path: Path) -> str:
    """Infer a locale from path components such as en-US/common.json."""
    for part in reversed(path.parts):
        candidates = LOCALE_RE.findall(part)
        if candidates:
            candidate = candidates[-1]
            return candidate.replace("_", "-")
    return ""


def walk_strings(value: Any, prefix: str = "") -> Iterable[tuple[str, str]]:
    """Yield flattened dot keys and string leaves; preserve array indexes."""
    if isinstance(value, dict):
        for key, child in value.items():
            key = str(key)
            if key.startswith("@"):
                continue  # ARB metadata (e.g. @saveButton) is not user-facing copy.
            child_key = f"{prefix}.{key}" if prefix else key
            yield from walk_strings(child, child_key)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            child_key = f"{prefix}[{index}]" if prefix else f"[{index}]"
            yield from walk_strings(child, child_key)
    elif isinstance(value, str):
        yield prefix, value


def parse_properties(text: str) -> dict[str, str]:
    """Parse the common Java properties syntax, including continued lines."""
    logical_lines: list[str] = []
    pending = ""
    for raw in text.splitlines():
        line = raw.rstrip()
        if pending:
            line = pending + line.lstrip()
            pending = ""
        slash_count = len(line) - len(line.rstrip("\\"))
        if slash_count % 2:
            pending = line[:-1]
            continue
        logical_lines.append(line)
    if pending:
        logical_lines.append(pending)

    result: dict[str, str] = {}
    for line in logical_lines:
        stripped = line.lstrip()
        if not stripped or stripped.startswith(("#", "!")):
            continue
        match = re.match(r"((?:\\.|[^:=\s])+)(?:\s*[:=]\s*|\s+)(.*)$", stripped)
        if match:
            key, value = match.groups()
        else:
            key, value = stripped, ""
        key = re.sub(r"\\([:=#!\s])", r"\1", key)
        value = re.sub(r"\\([:=#!\s])", r"\1", value)
        if key:
            result[key] = value
    return result


def parse_resource(path: Path) -> Any:
    text = path.read_text(encoding="utf-8-sig")
    suffix = path.suffix.lower()
    if suffix == ".json":
        return json.loads(text)
    if suffix in {".yaml", ".yml"}:
        try:
            import yaml  # type: ignore[import-not-found]
        except ImportError as exc:
            raise ValueError("YAML support requires PyYAML; install it with: pip install PyYAML") from exc
        return yaml.safe_load(text)
    if suffix == ".properties":
        return parse_properties(text)
    raise ValueError(f"Unsupported format: {suffix}")


def iter_files(inputs: list[Path]) -> Iterable[Path]:
    seen: set[Path] = set()
    for item in inputs:
        if item.is_file():
            candidates = [item] if item.suffix.lower() in SUPPORTED else []
        elif item.is_dir():
            candidates = (
                path for path in item.rglob("*")
                if path.is_file()
                and path.suffix.lower() in SUPPORTED
                and not any(part in SKIP_DIRS or part.startswith(".") for part in path.relative_to(item).parts[:-1])
            )
        else:
            raise FileNotFoundError(item)
        for path in candidates:
            resolved = path.resolve()
            if resolved not in seen:
                seen.add(resolved)
                yield path


def extract(paths: Iterable[Path], root: Path | None, locale: str | None,
            include_pattern: re.Pattern[str] | None, exclude_pattern: re.Pattern[str] | None) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for path in paths:
        parsed = parse_resource(path)
        source_path = path.resolve()
        if root:
            try:
                display_path = source_path.relative_to(root.resolve()).as_posix()
            except ValueError:
                display_path = path.as_posix()
        else:
            display_path = path.as_posix()
        detected_locale = locale or infer_locale(path)
        for key, text in walk_strings(parsed):
            if include_pattern and not include_pattern.search(key):
                continue
            if exclude_pattern and exclude_pattern.search(key):
                continue
            rows.append({
                "key": key,
                "locale": detected_locale,
                "source_file": display_path,
                "text": text,
            })
    return rows


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("inputs", nargs="+", type=Path, help="Resource files or directories")
    parser.add_argument("--root", type=Path, help="Base directory for relative source_file values")
    parser.add_argument("--locale", help="Explicit locale; otherwise infer it from the path")
    parser.add_argument("--include-key", help="Only include keys matching this regular expression")
    parser.add_argument("--exclude-key", help="Exclude keys matching this regular expression")
    parser.add_argument("--format", choices=("jsonl", "csv"), default="jsonl")
    parser.add_argument("--output", type=Path, required=True, help="Output file; use - for stdout")
    args = parser.parse_args(argv)

    try:
        paths = list(iter_files(args.inputs))
        if not paths:
            parser.error("No supported resource files found (.json, .yaml, .yml, .properties)")
        include = re.compile(args.include_key) if args.include_key else None
        exclude = re.compile(args.exclude_key) if args.exclude_key else None
        rows = extract(paths, args.root, args.locale, include, exclude)
        if args.output == Path("-"):
            if args.format == "jsonl":
                for row in rows:
                    print(json.dumps(row, ensure_ascii=False))
            else:
                writer = csv.DictWriter(sys.stdout, fieldnames=("key", "locale", "source_file", "text"))
                writer.writeheader()
                writer.writerows(rows)
        else:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            with args.output.open("w", encoding="utf-8-sig" if args.format == "csv" else "utf-8", newline="") as stream:
                if args.format == "jsonl":
                    for row in rows:
                        stream.write(json.dumps(row, ensure_ascii=False) + "\n")
                else:
                    writer = csv.DictWriter(stream, fieldnames=("key", "locale", "source_file", "text"))
                    writer.writeheader()
                    writer.writerows(rows)
        print(f"Extracted {len(rows)} strings from {len(paths)} files", file=sys.stderr)
        return 0
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError, re.error) as exc:
        parser.error(str(exc))
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
