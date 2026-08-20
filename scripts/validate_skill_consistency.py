#!/usr/bin/env python3
"""Validate internal structure consistency for prototype-ui-copy-review.

Usage:
  python3 scripts/validate_skill_consistency.py
  python3 scripts/validate_skill_consistency.py --root /path/to/prototype-ui-copy-review --json

The script is intentionally dependency-free. It validates the current file snapshot;
it does not infer whether documentation was updated for an uncommitted source change.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import unquote

EXPECTED_FILES = (
    "SKILL.md",
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
)

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
    if not name or name.group(1).strip() != "prototype-ui-copy-review":
        report.error("SKILL.md 的 name 必须为 prototype-ui-copy-review。")
    if not description or not description.group(1).strip():
        report.error("SKILL.md 的 description 不能为空。")
    if not report.errors:
        report.ok("SKILL.md frontmatter 完整")


def check_markdown_links(root: Path, files: tuple[str, ...], report: Report) -> None:
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
    report.ok(f"本地 Markdown 链接可解析（{checked} 项）")


def check_resource_routes(skill_text: str, report: Report) -> None:
    links = set(local_markdown_links(skill_text))
    for relative in SKILL_REQUIRED_LINKS:
        if relative not in links:
            report.error(f"SKILL.md 缺少资源路由链接：{relative}")
    for token in ("HF-", "PX-", "SPT-"):
        if token not in skill_text:
            report.error(f"SKILL.md 缺少规则前缀说明：{token}")
    if not report.errors:
        report.ok("资源路由与规则前缀完整")


def check_readme_references(readme_text: str, report: Report) -> None:
    for relative in README_REQUIRED_REFERENCES:
        if relative not in readme_text:
            report.error(f"docs/README.md 未列出资源：{relative}")
    report.ok("README 资源索引完整")


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
    report.ok(f"README 与版本记录同步：{history_version}")


def check_source_registry(root: Path, report: Report) -> None:
    text = read_text(root / "references/source-register.md", report)
    if "| 来源 ID |" not in text:
        report.error("source-register.md 缺少来源登记表头。")
    for expected in ("SRC-PX-COPY-001", "SRC-SPT-PATTERN-001"):
        if expected not in text:
            report.warning(f"source-register.md 未发现预期来源：{expected}。")
    report.ok("来源登记结构可识别")


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
    parser = argparse.ArgumentParser(description="校验 prototype-ui-copy-review 的内部结构一致性。")
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
    check_markdown_links(root, ("SKILL.md", "docs/README.md", "docs/VERSION_HISTORY.md"), report)
    check_source_registry(root, report)
    return render(report, args.json, args.strict)


if __name__ == "__main__":
    sys.exit(main())
