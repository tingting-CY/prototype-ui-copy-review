#!/usr/bin/env python3
"""Validate internal structure consistency for prototype-ui-copy-review.

Usage:
  python3 scripts/validate_skill_consistency.py
  python3 scripts/validate_skill_consistency.py --root /path/to/prototype-ui-copy-review --json
  python3 scripts/validate_skill_consistency.py --strict

Checks (dependency-free, current file snapshot only):
  1. Required v2 files exist and removed v1 runtime files stay absent.
  2. SKILL.md frontmatter has the expected name and a non-empty description.
  3. SKILL.md routes to every runtime reference and mentions the HF-/PX-/SPT- prefixes.
  4. docs/README.md lists every runtime resource.
  5. docs/README.md and docs/VERSION_HISTORY.md agree on the current version and the
     current version has a detailed record with the required fields.
  6. Local Markdown links resolve, across SKILL.md, root docs, docs/ and references/.
  7. references/source-register.md has the registry table and expected source IDs.
  8. The six HF shards contain the complete, unique 75-rule inventory.
  9. Evaluation and token-budget JSON files parse and target valid files.
  10. No sensitive content: internal hosts, intranet paths, private IPs or
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
    "references/hf-core.md",
    "references/hf-punctuation.md",
    "references/hf-format.md",
    "references/hf-state-feedback.md",
    "references/hf-terminology-components.md",
    "references/hf-language.md",
    "references/change-list-schema.md",
    "references/coverage-gap-schema.md",
    "references/paletx-design-system-copy-spec.md",
    "references/prompt-templates.md",
    "references/source-register.md",
    "references/system-prompt-patterns.md",
    "docs/README.md",
    "docs/VERSION_HISTORY.md",
    "scripts/validate_skill_consistency.py",
    "scripts/validate_token_budget.py",
    "evals/evals.json",
    "evals/trigger-eval.json",
    "evals/token-budgets.json",
)

LEGACY_FILES = (
    "references/high-frequency-copy-rules.md",
    "references/markdown-change-list.md",
    "references/review-scope-configuration.md",
    "references/review-dimension-confirmation.md",
    "references/uncovered-copy-scenarios.md",
)

SKILL_REQUIRED_LINKS = (
    "references/hf-core.md",
    "references/hf-punctuation.md",
    "references/hf-format.md",
    "references/hf-state-feedback.md",
    "references/hf-terminology-components.md",
    "references/hf-language.md",
    "references/change-list-schema.md",
    "references/coverage-gap-schema.md",
    "references/source-register.md",
    "references/paletx-design-system-copy-spec.md",
    "references/system-prompt-patterns.md",
    "references/prompt-templates.md",
    "docs/README.md",
    "docs/VERSION_HISTORY.md",
    "CONTRIBUTING.md",
)

README_REQUIRED_REFERENCES = (
    "SKILL.md",
    "references/hf-core.md",
    "references/hf-punctuation.md",
    "references/hf-format.md",
    "references/hf-state-feedback.md",
    "references/hf-terminology-components.md",
    "references/hf-language.md",
    "references/paletx-design-system-copy-spec.md",
    "references/system-prompt-patterns.md",
    "references/prompt-templates.md",
    "references/change-list-schema.md",
    "references/coverage-gap-schema.md",
    "references/source-register.md",
    "docs/VERSION_HISTORY.md",
    "evals/evals.json",
    "evals/trigger-eval.json",
    "evals/token-budgets.json",
    "scripts/validate_token_budget.py",
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

EXPECTED_HF_RULE_COUNTS = {
    "GEN": 5,
    "PUN": 10,
    "SPC": 4,
    "STA": 10,
    "MIX": 8,
    "NUM": 9,
    "TERM": 6,
    "CMP": 9,
    "LNG": 8,
    "FBK": 6,
}
HF_RULE = re.compile(r"HF-([A-Z]+)-(\d{2})")

EVAL_CHECK_FIELDS = {
    "regex_all": ("patterns",),
    "regex_none_all": ("patterns",),
    "regex_any": ("patterns",),
    "regex_none": ("pattern",),
    "distinct_min": ("pattern", "min"),
}
REQUIRED_EVAL_CONTRACTS = {
    "full-review-explicit-change-list": {
        "no_dimension_menu": {"check": "regex_none_all", "patterns": {"请回复选项", "A、B、F"}},
        "no_source_rules": {
            "check": "regex_none_all",
            "patterns": {r"PX-[A-Z]{2,5}-\d{2}", r"SPT-[A-Z]{3}-\d{2}"},
        },
        "change_list_present": {"check": "distinct_min", "pattern": r"COPY-\d{3}", "min": 5},
        "no_default_p3": {"check": "regex_none", "pattern": r"\|\s*P3\s*\|"},
    },
    "multi-page-generic-feedback-no-spt": {
        "no_menu": {"check": "regex_none_all", "patterns": {"请回复选项", "A、B、F"}},
        "no_spt": {"check": "regex_none", "pattern": r"SPT-[A-Z]{3}-\d{2}"},
        "no_change_list": {"check": "regex_none", "pattern": r"COPY-\d{3}"},
    },
    "vague-page-direct-default": {
        "direct_review": {"check": "regex_any", "patterns": {"HF-CMP-05", "手机号"}},
        "no_menu": {"check": "regex_none_all", "patterns": {"请回复选项", "A、B、F"}},
        "no_optional_artifacts": {
            "check": "regex_none_all",
            "patterns": {r"COPY-\d{3}", r"UC-\d{3}", r"SPT-[A-Z]{3}-\d{2}", r"PX-[A-Z]{2,5}-\d{2}"},
        },
    },
    "single-copy-direct-qa": {
        "direct_fields": {"check": "regex_all", "patterns": {"结论", "依据", "建议"}},
        "no_full_artifacts": {"check": "regex_none_all", "patterns": {r"COPY-\d{3}", r"UC-\d{3}", "P0", "P1", "P2", "P3"}},
        "no_spt": {"check": "regex_none", "pattern": r"SPT-[A-Z]{3}-\d{2}"},
    },
    "explicit-spt-source-review": {
        "spt_used": {"check": "regex_any", "patterns": {"SPT-ACC-01", "SPT-PAT-01"}},
        "no_copy": {"check": "regex_none", "pattern": r"COPY-\d{3}"},
    },
    "governance-explicit-uc": {
        "uc_present": {"check": "regex_any", "patterns": {"UC-001", "未涉及规范场景文案"}},
        "governance_fields": {"check": "regex_all", "patterns": {"未覆盖原因", "需要评估", "推荐规范动作"}},
        "no_copy": {"check": "regex_none", "pattern": r"COPY-\d{3}"},
    },
}
REQUIRED_TOKEN_BUDGETS = {
    "frontmatter_description": {"kind": "description", "files": set()},
    "skill_body": {"kind": None, "files": {"SKILL.md"}},
    "single_punctuation": {
        "kind": None,
        "files": {"SKILL.md", "references/hf-core.md", "references/hf-punctuation.md"},
    },
    "single_feedback_general": {
        "kind": None,
        "files": {"SKILL.md", "references/hf-core.md", "references/hf-state-feedback.md"},
    },
    "single_terminology_component": {
        "kind": None,
        "files": {"SKILL.md", "references/hf-core.md", "references/hf-terminology-components.md"},
    },
    "standard_page_with_change_list": {
        "kind": None,
        "files": {"SKILL.md", "references/hf-core.md", "references/change-list-schema.md"},
    },
    "explicit_spt_review": {
        "kind": None,
        "files": {"SKILL.md", "references/hf-core.md", "references/system-prompt-patterns.md"},
    },
    "paletx_component_review": {
        "kind": None,
        "files": {"SKILL.md", "references/hf-core.md", "references/paletx-design-system-copy-spec.md"},
    },
    "governance_with_coverage_gap": {
        "kind": None,
        "files": {"SKILL.md", "references/hf-core.md", "references/coverage-gap-schema.md"},
    },
    "custom_assistant_setup": {
        "kind": None,
        "files": {"SKILL.md", "references/prompt-templates.md"},
    },
    "source_registry_maintenance": {
        "kind": None,
        "files": {"SKILL.md", "references/source-register.md"},
    },
    "all_hf_runtime_shards": {
        "kind": None,
        "files": {
            "SKILL.md", "references/hf-core.md", "references/hf-punctuation.md",
            "references/hf-format.md", "references/hf-state-feedback.md",
            "references/hf-terminology-components.md", "references/hf-language.md",
        },
    },
}

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
    legacy = [relative for relative in LEGACY_FILES if (report.root / relative).exists()]
    if legacy:
        for relative in legacy:
            report.error(f"v2 已移除的旧运行文件仍存在：{relative}")
    if not missing and not legacy:
        report.ok(f"v2 文件结构完整（{len(EXPECTED_FILES)} 项）")


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
        eval_ids: set[int] = set()
        eval_names: set[str] = set()
        for index, item in enumerate(evals):
            if not isinstance(item, dict):
                report.error(f"evals/evals.json 第 {index} 条必须是对象。")
                continue
            for key in ("id", "name", "prompt", "expected_output", "assertions"):
                if key not in item:
                    report.error(f"evals/evals.json 第 {index} 条缺少字段：{key}")
            eval_id = item.get("id")
            name = item.get("name")
            if not isinstance(eval_id, int) or eval_id in eval_ids:
                report.error(f"evals/evals.json 第 {index} 条 id 必须是唯一整数。")
            else:
                eval_ids.add(eval_id)
            if not isinstance(name, str) or not name or name in eval_names:
                report.error(f"evals/evals.json 第 {index} 条 name 必须是唯一非空字符串。")
            else:
                eval_names.add(name)
            for field_name in ("prompt", "expected_output"):
                if not isinstance(item.get(field_name), str) or not item[field_name].strip():
                    report.error(f"evals/evals.json 第 {index} 条 {field_name} 必须是非空字符串。")

            assertions = item.get("assertions")
            if not isinstance(assertions, list) or not assertions:
                report.error(f"evals/evals.json 第 {index} 条 assertions 必须是非空数组。")
                continue
            assertion_ids: set[str] = set()
            for assertion_index, assertion in enumerate(assertions):
                if not isinstance(assertion, dict):
                    report.error(f"eval {name or index} 的断言 {assertion_index} 必须是对象。")
                    continue
                for key in ("id", "text", "check"):
                    if key not in assertion:
                        report.error(f"eval {name or index} 的断言 {assertion_index} 缺少 {key}。")
                assertion_id = assertion.get("id")
                check = assertion.get("check")
                if not isinstance(assertion.get("text"), str) or not assertion["text"].strip():
                    report.error(f"eval {name or index} 的断言 {assertion_id} 的 text 必须是非空字符串。")
                if not isinstance(assertion_id, str) or not assertion_id or assertion_id in assertion_ids:
                    report.error(f"eval {name or index} 的断言 id 必须是唯一非空字符串。")
                else:
                    assertion_ids.add(assertion_id)
                if check not in EVAL_CHECK_FIELDS:
                    report.error(f"eval {name or index} 的断言 {assertion_id} 使用未知 check：{check}")
                    continue
                for required_field in EVAL_CHECK_FIELDS[check]:
                    if required_field not in assertion:
                        report.error(f"eval {name or index} 的断言 {assertion_id} 缺少 {required_field}。")
                patterns = assertion.get("patterns")
                pattern = assertion.get("pattern")
                if patterns is not None and (not isinstance(patterns, list) or not patterns):
                    report.error(f"eval {name or index} 的断言 {assertion_id} 的 patterns 必须是非空数组。")
                regexes = patterns if isinstance(patterns, list) else ([pattern] if isinstance(pattern, str) else [])
                for value in regexes:
                    if not isinstance(value, str) or not value:
                        report.error(f"eval {name or index} 的断言 {assertion_id} 含无效正则。")
                        continue
                    try:
                        re.compile(value)
                    except re.error as exc:
                        report.error(f"eval {name or index} 的断言 {assertion_id} 正则无效：{exc}")
                if check == "distinct_min" and (
                    not isinstance(assertion.get("min"), int) or assertion["min"] <= 0
                ):
                    report.error(f"eval {name or index} 的断言 {assertion_id} 的 min 必须为正整数。")

            assertion_by_id = {
                assertion.get("id"): assertion
                for assertion in assertions
                if isinstance(assertion, dict) and isinstance(assertion.get("id"), str)
            }
            contracts = REQUIRED_EVAL_CONTRACTS.get(name, {})
            missing_assertions = set(contracts) - assertion_ids
            for assertion_id in sorted(missing_assertions):
                report.error(f"eval {name} 缺少 v2 核心断言：{assertion_id}")
            for assertion_id, contract in contracts.items():
                assertion = assertion_by_id.get(assertion_id)
                if assertion is None:
                    continue
                if assertion.get("check") != contract["check"]:
                    report.error(
                        f"eval {name} 的核心断言 {assertion_id} check 必须为 {contract['check']}。"
                    )
                if "pattern" in contract and assertion.get("pattern") != contract["pattern"]:
                    report.error(f"eval {name} 的核心断言 {assertion_id} pattern 不符合 v2 契约。")
                if "patterns" in contract:
                    actual_patterns = assertion.get("patterns")
                    actual_set = {
                        value for value in actual_patterns if isinstance(value, str)
                    } if isinstance(actual_patterns, list) else set()
                    missing_patterns = contract["patterns"] - actual_set
                    if missing_patterns:
                        report.error(
                            f"eval {name} 的核心断言 {assertion_id} 缺少关键 patterns："
                            f"{', '.join(sorted(missing_patterns))}"
                        )
                if "min" in contract:
                    actual_min = assertion.get("min")
                    if (
                        not isinstance(actual_min, int)
                        or isinstance(actual_min, bool)
                        or actual_min != contract["min"]
                    ):
                        report.error(
                            f"eval {name} 的核心断言 {assertion_id} min 必须为 {contract['min']}。"
                        )
        for name in sorted(set(REQUIRED_EVAL_CONTRACTS) - eval_names):
            report.error(f"evals/evals.json 缺少 v2 核心用例：{name}")
    report.ok_if_clean(before, f"回归用例可解析（{len(evals) if isinstance(evals, list) else 0} 条）")


def check_hf_rule_inventory(root: Path, report: Report) -> None:
    before = len(report.errors)
    shard_paths = sorted((root / "references").glob("hf-*.md"))
    seen: dict[str, list[str]] = {}
    for path in shard_paths:
        text = read_text(path, report)
        for family, number in HF_RULE.findall(text):
            rule_id = f"HF-{family}-{number}"
            seen.setdefault(rule_id, []).append(path.name)

    expected = {
        f"HF-{family}-{number:02d}"
        for family, count in EXPECTED_HF_RULE_COUNTS.items()
        for number in range(1, count + 1)
    }
    actual = set(seen)
    for rule_id in sorted(expected - actual):
        report.error(f"HF 规则分片缺少编号：{rule_id}")
    for rule_id in sorted(actual - expected):
        report.error(f"HF 规则分片包含未知编号：{rule_id}")
    for rule_id, files in sorted(seen.items()):
        if len(files) > 1:
            report.error(f"HF 规则编号重复：{rule_id}（{', '.join(files)}）")
    report.ok_if_clean(before, f"HF 规则编号完整且唯一（{len(actual)} 条，{len(shard_paths)} 个分片）")


def check_token_budget_manifest(root: Path, report: Report) -> None:
    before = len(report.errors)
    path = root / "evals/token-budgets.json"
    if not path.is_file():
        return
    try:
        data = json.loads(read_text(path, report))
    except json.JSONDecodeError as exc:
        report.error(f"evals/token-budgets.json 不是合法 JSON：{exc}")
        return
    if data.get("tokenizer") != "o200k_base":
        report.error("token 预算 tokenizer 必须为 o200k_base。")
    if not isinstance(data.get("tiktoken_version"), str) or not data["tiktoken_version"]:
        report.error("token 预算必须声明非空 tiktoken_version。")
    budgets = data.get("budgets")
    if not isinstance(budgets, list) or not budgets:
        report.error("token-budgets.json 的 budgets 必须是非空数组。")
        return
    names: set[str] = set()
    budget_by_name: dict[str, dict] = {}
    for index, budget in enumerate(budgets):
        if not isinstance(budget, dict):
            report.error(f"token 预算第 {index} 项必须是对象。")
            continue
        name = budget.get("name")
        if not isinstance(name, str) or not name:
            report.error(f"token 预算第 {index} 项缺少 name。")
        elif name in names:
            report.error(f"token 预算名称重复：{name}")
        else:
            names.add(name)
            budget_by_name[name] = budget
        maximum = budget.get("max_tokens")
        if not isinstance(maximum, int) or isinstance(maximum, bool) or maximum <= 0:
            report.error(f"token 预算 {name or index} 的 max_tokens 必须为正整数。")
        kind = budget.get("kind")
        if kind not in (None, "description"):
            report.error(f"token 预算 {name or index} 使用未知 kind：{kind}")
        files = budget.get("files")
        if kind == "description":
            if files not in (None, []):
                report.error(f"description 预算 {name or index} 不得声明 files。")
            continue
        if not isinstance(files, list) or not files:
            report.error(f"token 预算 {name or index} 的 files 必须是非空数组。")
            continue
        valid_paths = [relative for relative in files if isinstance(relative, str) and relative]
        if len(valid_paths) != len(files):
            report.error(f"token 预算 {name or index} 含无效路径。")
        if len(valid_paths) != len(set(valid_paths)):
            report.error(f"token 预算 {name or index} 的 files 含重复路径。")
        for relative in files:
            if not isinstance(relative, str) or not relative:
                continue
            relative_path = Path(relative)
            if relative_path.is_absolute() or ".." in relative_path.parts:
                report.error(f"token 预算 {name or index} 路径必须位于仓库内：{relative}")
                continue
            if not (root / relative_path).is_file():
                report.error(f"token 预算 {name or index} 引用了不存在的文件：{relative}")

    for name, requirement in REQUIRED_TOKEN_BUDGETS.items():
        budget = budget_by_name.get(name)
        if budget is None:
            report.error(f"token 预算缺少 v2 必需路径：{name}")
            continue
        if budget.get("kind") != requirement["kind"]:
            report.error(f"token 预算 {name} 的 kind 不符合 v2 契约。")
        raw_files = budget.get("files", [])
        actual_files = {
            relative for relative in raw_files
            if isinstance(relative, str) and relative
        } if isinstance(raw_files, list) else set()
        missing_files = requirement["files"] - actual_files
        for relative in sorted(missing_files):
            report.error(f"token 预算 {name} 缺少必需文件：{relative}")
    report.ok_if_clean(before, f"token 预算清单可解析（{len(budgets)} 条）")


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
    check_hf_rule_inventory(root, report)
    check_evals(root, report)
    check_token_budget_manifest(root, report)
    check_sensitive_content(root, report)
    return render(report, args.json, args.strict)


if __name__ == "__main__":
    sys.exit(main())
