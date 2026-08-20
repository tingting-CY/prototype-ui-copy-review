#!/usr/bin/env python3
"""Validate internal structure consistency for prototype-ui-copy-review.

Usage:
  python3 scripts/validate_skill_consistency.py
  python3 scripts/validate_skill_consistency.py --root /path/to/prototype-ui-copy-review --json
  python3 scripts/validate_skill_consistency.py --strict

Checks (dependency-free, current file snapshot only):
  1. Required files exist (SKILL.md, references/, docs/, scripts/, evals/, root README/CONTRIBUTING).
  2. SKILL.md frontmatter has the expected name and a non-empty description.
  3. SKILL.md routes to every reference file and mentions the HF-/PX-/SPT- prefixes.
  4. docs/README.md lists every resource.
  5. docs/README.md and docs/VERSION_HISTORY.md agree on the current version and the
     current version has a detailed record with the required fields.
  6. Local Markdown links resolve, across SKILL.md, root docs, docs/ and references/.
  7. references/source-register.md has the registry table and expected source IDs.
  8. evals/evals.json parses and targets this skill.
  9. No sensitive content: internal hosts, intranet paths, private IPs or
     machine-specific home directories in any tracked .md/.py/.json file.

The script does not infer whether documentation was updated for an uncommitted source change.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import unquote

SKILL_NAME = "prototype-ui-copy-review"

EXPECTED_FILES = (
    "SKILL.md",
    "README.md",
    "CONTRIBUTING.md",
    "references/high-frequency-copy-rules.md",
    "references/markdown-change-list.md",
    "references/paletx-design-system-copy-spec.md",
    "references/prompt-templates.md",
    "references/source-register.md",
    "references/review-scope-configuration.md",
    "references/review-dimension-confirmation.md",
    "references/system-prompt-patterns.md",
    "references/uncovered-copy-scenarios.md",
    "docs/README.md",
    "docs/VERSION_HISTORY.md",
    "scripts/validate_skill_consistency.py",
    "evals/evals.json",
)

SKILL_REQUIRED_LINKS = (
    "references/high-frequency-copy-rules.md",
    "references/source-register.md",
    "references/paletx-design-system-copy-spec.md",
    "references/system-prompt-patterns.md",
    "references/prompt-templates.md",
    "references/markdown-change-list.md",
    "references/review-scope-configuration.md",
    "references/review-dimension-confirmation.md",
    "references/uncovered-copy-scenarios.md",
    "docs/README.md",
    "docs/VERSION_HISTORY.md",
)

README_REQUIRED_REFERENCES = (
    "SKILL.md",
    "references/high-frequency-copy-rules.md",
    "references/paletx-design-system-copy-spec.md",
    "references/system-prompt-patterns.md",
    "references/prompt-templates.md",
    "references/markdown-change-list.md",
    "references/source-register.md",
    "references/review-scope-configuration.md",
    "references/review-dimension-confirmation.md",
    "references/uncovered-copy-scenarios.md",
    "docs/VERSION_HISTORY.md",
    "evals/evals.json",
)

LINK_CHECK_FILES = (
    "SKILL.md",
    "README.md",
    "CONTRIBUTING.md",
    "docs/README.md",
    "docs/VERSION_HISTORY.md",
)

# Patterns that must never appear in a public repository. Each entry is
# (label, compiled regex). Public, approved sources (for example the PaletX
# site) are not matched; only intranet hosts, intranet paths, private IP
# ranges and machine-specific home directories are.
SENSITIVE_PATTERNS = (
    ("内部 wiki 主机", re.compile(r"i\.zte\.com\.cn")),
    ("内部 wiki 路径", re.compile(r"/ispace/")),
    ("私有网段 IP", re.compile(r"\b(?:10\.\d{1,3}|192\.168|172\.(?:1[6-9]|2\d|3[01]))\.\d{1,3}\.\d{1,3}\b")),
    ("机器专属 home 路径", re.compile(r"(?<![\w/])/(?:home|Users)/[A-Za-z0-9._-]+/")),
)
SENSITIVE_SCAN_SUFFIXES = (".md", ".py", ".json")
SENSITIVE_SCAN_SKIP_DIRS = {".git", "__pycache__", ".venv", "node_modules"}
# The validator itself holds the patterns and is excluded from the scan.
SENSITIVE_SCAN_SKIP_FILES = {"scripts/validate_skill_consistency.py"}

MARKDOWN_LINK = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")
SEMVER = re.compile(r"^v\d+\.\d+\.\d+$")
CURRENT_VERSION = re.compile(r"当前版本：\*\*(v\d+\.\d+\.\d+)\*\*")
README_VERSION = re.compile(r"\*\*版本：(v\d+\.\d+\.\d+)\*\*")


@dataclass
class Report:
    root: Path
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    checks: list[str] = field(default_factory=list)

    def ok(self, message: str) -> None:
        self.checks.append(message)

    def error(self, message: str) -> None:
        self.errors.append(message)

    def warning(self, message: str) -> None:
        self.warnings.append(message)

    def ok_if_clean(self, before: int, message: str) -> None:
        """Record a passing check only when no new errors were added since `before`."""
        if len(self.errors) == before:
            self.ok(message)


def read_text(path: Path, report: Report) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        report.error(f"无法读取 {path.relative_to(report.root)}：{exc}")
        return ""


def local_markdown_links(text: str) -> list[str]:
    links: list[str] = []
    for raw_target in MARKDOWN_LINK.findall(text):
        target = raw_target.strip().split(maxsplit=1)[0]
        target = target.split("#", 1)[0].split("?", 1)[0]
        if not target or "://" in target or target.startswith("mailto:"):
            continue
        links.append(unquote(target))
    return links


def check_required_files(report: Report) -> None:
    missing = [relative for relative in EXPECTED_FILES if not (report.root / relative).is_file()]
    if missing:
        for relative in missing:
            report.error(f"缺少必需文件：{relative}")
    else:
        report.ok(f"必需文件齐全（{len(EXPECTED_FILES)} 项）")


def check_frontmatter(skill_text: str, report: Report) -> None:
    before = len(report.errors)
    if not skill_text.startswith("---\n"):
        report.error("SKILL.md 缺少 YAML frontmatter 起始分隔符。")
        return
    parts = skill_text.split("---", 2)
    if len(parts) < 3:
        report.error("SKILL.md 的 YAML frontmatter 未正确闭合。")
        return
    frontmatter = parts[1]
    name = re.search(r"^name:\s*(.+)$", frontmatter, re.MULTILINE)
    description = re.search(r"^description:\s*(.+)$", frontmatter, re.MULTILINE)
    if not name or name.group(1).strip() != SKILL_NAME:
        report.error(f"SKILL.md 的 name 必须为 {SKILL_NAME}。")
    if not description or not description.group(1).strip():
        report.error("SKILL.md 的 description 不能为空。")
    elif "<" in description.group(1) or ">" in description.group(1):
        report.error("SKILL.md 的 description 不能包含尖括号。")
    elif len(description.group(1).strip()) > 1024:
        report.error("SKILL.md 的 description 超过 1024 字符。")
    report.ok_if_clean(before, "SKILL.md frontmatter 完整")


def check_markdown_links(root: Path, files: tuple[str, ...], report: Report) -> None:
    before = len(report.errors)
    checked = 0
    for relative in files:
        source = root / relative
        if not source.is_file():
            continue
        for target in local_markdown_links(read_text(source, report)):
            resolved = (source.parent / target).resolve()
            try:
                resolved.relative_to(root.resolve())
            except ValueError:
                report.warning(f"{relative} 引用了 Skill 目录外的本地文件：{target}")
                continue
            if not resolved.is_file():
                report.error(f"{relative} 的本地链接不存在：{target}")
            else:
                checked += 1
    report.ok_if_clean(before, f"本地 Markdown 链接可解析（{checked} 项）")


def check_resource_routes(skill_text: str, report: Report) -> None:
    before = len(report.errors)
    links = set(local_markdown_links(skill_text))
    for relative in SKILL_REQUIRED_LINKS:
        if relative not in links:
            report.error(f"SKILL.md 缺少资源路由链接：{relative}")
    for token in ("HF-", "PX-", "SPT-"):
        if token not in skill_text:
            report.error(f"SKILL.md 缺少规则前缀说明：{token}")
    report.ok_if_clean(before, "资源路由与规则前缀完整")


def check_readme_references(readme_text: str, report: Report) -> None:
    before = len(report.errors)
    for relative in README_REQUIRED_REFERENCES:
        if relative not in readme_text:
            report.error(f"docs/README.md 未列出资源：{relative}")
    report.ok_if_clean(before, "README 资源索引完整")


def extract_version(pattern: re.Pattern[str], text: str, label: str, report: Report) -> str | None:
    match = pattern.search(text)
    if not match:
        report.error(f"未在 {label} 中找到版本号。")
        return None
    version = match.group(1)
    if not SEMVER.fullmatch(version):
        report.error(f"{label} 的版本号不符合 v主.次.修订 格式：{version}")
        return None
    return version


def check_versions(readme_text: str, history_text: str, report: Report) -> None:
    before = len(report.errors)
    readme_version = extract_version(README_VERSION, readme_text, "docs/README.md", report)
    history_version = extract_version(CURRENT_VERSION, history_text, "docs/VERSION_HISTORY.md", report)
    if not readme_version or not history_version:
        return
    if readme_version != history_version:
        report.error(f"版本不同步：README 为 {readme_version}，VERSION_HISTORY 为 {history_version}。")
        return

    table_row = f"| {history_version} |"
    heading = f"### {history_version}"
    if table_row not in history_text:
        report.error(f"VERSION_HISTORY 缺少当前版本的概览表行：{history_version}。")
    if heading not in history_text:
        report.error(f"VERSION_HISTORY 缺少当前版本的详细记录标题：{heading}。")
        return

    section = history_text.split(heading, 1)[1]
    next_heading = re.search(r"\n### v\d+\.\d+\.\d+", section)
    if next_heading:
        section = section[: next_heading.start()]
    for required_field in ("受影响文件", "兼容性", "校验状态"):
        if required_field not in section:
            report.error(f"当前版本详细记录缺少字段：{required_field}。")
    report.ok_if_clean(before, f"README 与版本记录同步：{history_version}")


def check_source_registry(root: Path, report: Report) -> None:
    before = len(report.errors)
    text = read_text(root / "references/source-register.md", report)
    if "| 来源 ID |" not in text:
        report.error("source-register.md 缺少来源登记表头。")
    for expected in ("SRC-PX-COPY-001", "SRC-SPT-PATTERN-001"):
        if expected not in text:
            report.warning(f"source-register.md 未发现预期来源：{expected}。")
    report.ok_if_clean(before, "来源登记结构可识别")


def check_evals(root: Path, report: Report) -> None:
    before = len(report.errors)
    path = root / "evals/evals.json"
    if not path.is_file():
        return
    try:
        data = json.loads(read_text(path, report))
    except json.JSONDecodeError as exc:
        report.error(f"evals/evals.json 不是合法 JSON：{exc}")
        return
    if data.get("skill_name") != SKILL_NAME:
        report.error(f"evals/evals.json 的 skill_name 必须为 {SKILL_NAME}。")
    evals = data.get("evals")
    if not isinstance(evals, list) or not evals:
        report.error("evals/evals.json 的 evals 必须是非空数组。")
    else:
        for index, item in enumerate(evals):
            for key in ("id", "prompt", "expected_output"):
                if key not in item:
                    report.error(f"evals/evals.json 第 {index} 条缺少字段：{key}")
    report.ok_if_clean(before, f"回归用例可解析（{len(evals) if isinstance(evals, list) else 0} 条）")


def iter_scan_files(root: Path):
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.suffix not in SENSITIVE_SCAN_SUFFIXES:
            continue
        relative = path.relative_to(root)
        if any(part in SENSITIVE_SCAN_SKIP_DIRS for part in relative.parts):
            continue
        if relative.as_posix() in SENSITIVE_SCAN_SKIP_FILES:
            continue
        yield path


def check_sensitive_content(root: Path, report: Report) -> None:
    before = len(report.errors)
    scanned = 0
    for path in iter_scan_files(root):
        scanned += 1
        text = read_text(path, report)
        for line_number, line in enumerate(text.splitlines(), start=1):
            for label, pattern in SENSITIVE_PATTERNS:
                if pattern.search(line):
                    relative = path.relative_to(root)
                    report.error(f"{relative}:{line_number} 含敏感内容（{label}）：{line.strip()[:120]}")
    report.ok_if_clean(before, f"未发现内部链接或机器专属路径（扫描 {scanned} 个文件）")


def render(report: Report, as_json: bool, strict: bool) -> int:
    failed = bool(report.errors or (strict and report.warnings))
    payload = {
        "root": str(report.root),
        "status": "FAIL" if failed else "PASS",
        "checks": report.checks,
        "warnings": report.warnings,
        "errors": report.errors,
    }
    if as_json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(f"[{'FAIL' if failed else 'PASS'}] Skill 结构一致性校验：{report.root}")
        for message in report.checks:
            print(f"  ✓ {message}")
        for message in report.warnings:
            print(f"  ! 警告：{message}")
        for message in report.errors:
            print(f"  ✗ 错误：{message}")
        print(f"摘要：{len(report.checks)} 项通过，{len(report.warnings)} 项警告，{len(report.errors)} 项错误")
    return 1 if failed else 0


def main() -> int:
    parser = argparse.ArgumentParser(description=f"校验 {SKILL_NAME} 的内部结构一致性。")
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Skill 根目录；默认使用本脚本所在 scripts/ 的上级目录。",
    )
    parser.add_argument("--json", action="store_true", help="以 JSON 输出校验结果。")
    parser.add_argument("--strict", action="store_true", help="将警告视为失败。")
    args = parser.parse_args()

    root = args.root.resolve()
    report = Report(root=root)
    if not root.is_dir():
        report.error(f"Skill 根目录不存在：{root}")
        return render(report, args.json, args.strict)

    check_required_files(report)
    skill_path = root / "SKILL.md"
    readme_path = root / "docs/README.md"
    history_path = root / "docs/VERSION_HISTORY.md"
    skill_text = read_text(skill_path, report) if skill_path.is_file() else ""
    readme_text = read_text(readme_path, report) if readme_path.is_file() else ""
    history_text = read_text(history_path, report) if history_path.is_file() else ""

    if skill_text:
        check_frontmatter(skill_text, report)
        check_resource_routes(skill_text, report)
    if readme_text:
        check_readme_references(readme_text, report)
    if readme_text and history_text:
        check_versions(readme_text, history_text, report)
    reference_files = tuple(
        str(path.relative_to(root)) for path in sorted((root / "references").glob("*.md"))
    ) if (root / "references").is_dir() else ()
    check_markdown_links(root, LINK_CHECK_FILES + reference_files, report)
    check_source_registry(root, report)
    check_evals(root, report)
    check_sensitive_content(root, report)
    return render(report, args.json, args.strict)


if __name__ == "__main__":
    sys.exit(main())
