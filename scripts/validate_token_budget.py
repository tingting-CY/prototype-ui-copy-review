#!/usr/bin/env python3
"""Validate runtime token budgets declared in evals/token-budgets.json."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

try:
    import tiktoken
except ImportError:
    print("缺少依赖：请运行 python3 -m pip install tiktoken==0.14.0", file=sys.stderr)
    raise SystemExit(2)


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        raise SystemExit(f"无法读取 {path}: {exc}") from exc


def load_config(path: Path) -> dict:
    try:
        data = json.loads(read_text(path))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"预算清单不是合法 JSON：{exc}") from exc
    if not isinstance(data, dict):
        raise SystemExit("预算清单根节点必须是对象。")
    return data


def validate_config(root: Path, config: dict) -> list[dict]:
    tokenizer = config.get("tokenizer")
    if not isinstance(tokenizer, str) or not tokenizer:
        raise SystemExit("预算清单必须声明非空 tokenizer。")
    expected_version = config.get("tiktoken_version")
    if not isinstance(expected_version, str) or not expected_version:
        raise SystemExit("预算清单必须声明非空 tiktoken_version。")
    if tiktoken.__version__ != expected_version:
        raise SystemExit(
            f"tiktoken 版本不一致：当前 {tiktoken.__version__}，要求 {expected_version}。"
        )

    budgets = config.get("budgets")
    if not isinstance(budgets, list) or not budgets:
        raise SystemExit("预算清单的 budgets 必须是非空数组。")

    names: set[str] = set()
    for index, budget in enumerate(budgets):
        if not isinstance(budget, dict):
            raise SystemExit(f"预算第 {index} 项必须是对象。")
        name = budget.get("name")
        if not isinstance(name, str) or not name:
            raise SystemExit(f"预算第 {index} 项缺少非空 name。")
        if name in names:
            raise SystemExit(f"预算名称重复：{name}")
        names.add(name)

        maximum = budget.get("max_tokens")
        if not isinstance(maximum, int) or isinstance(maximum, bool) or maximum <= 0:
            raise SystemExit(f"预算 {name} 的 max_tokens 必须为正整数。")

        kind = budget.get("kind")
        if kind not in (None, "description"):
            raise SystemExit(f"预算 {name} 使用未知 kind：{kind}")
        files = budget.get("files")
        if kind == "description":
            if files not in (None, []):
                raise SystemExit(f"description 预算 {name} 不得声明 files。")
            continue
        if not isinstance(files, list) or not files:
            raise SystemExit(f"预算 {name} 的 files 必须是非空数组。")
        if any(not isinstance(relative, str) or not relative for relative in files):
            raise SystemExit(f"预算 {name} 含无效路径。")
        if len(files) != len(set(files)):
            raise SystemExit(f"预算 {name} 的 files 含重复路径。")
        for relative in files:
            relative_path = Path(relative)
            if relative_path.is_absolute() or ".." in relative_path.parts:
                raise SystemExit(f"预算 {name} 路径必须位于仓库内：{relative}")
            resolved = (root / relative_path).resolve()
            try:
                resolved.relative_to(root)
            except ValueError as exc:
                raise SystemExit(f"预算 {name} 路径逃逸仓库：{relative}") from exc
            if not resolved.is_file():
                raise SystemExit(f"预算 {name} 引用了不存在的文件：{relative}")
    return budgets


def main() -> int:
    parser = argparse.ArgumentParser(description="校验 Skill 典型加载路径的 token 预算。")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--json", action="store_true", help="输出 JSON 结果。")
    args = parser.parse_args()

    root = args.root.resolve()
    config = load_config(root / "evals/token-budgets.json")
    budgets = validate_config(root, config)
    try:
        encoding = tiktoken.get_encoding(config["tokenizer"])
    except ValueError as exc:
        raise SystemExit(f"未知 tokenizer：{config['tokenizer']}") from exc

    skill_text = read_text(root / "SKILL.md")
    results = []
    failed = False

    for budget in budgets:
        if budget.get("kind") == "description":
            match = re.search(r"^description:\s*(.+)$", skill_text, re.MULTILINE)
            if not match:
                raise SystemExit("SKILL.md frontmatter 缺少 description。")
            payload = match.group(1).strip()
            files = ["SKILL.md#description"]
        else:
            files = budget["files"]
            payload = "\n".join(read_text(root / relative) for relative in files)

        actual = len(encoding.encode(payload))
        maximum = budget["max_tokens"]
        passed = actual <= maximum
        failed = failed or not passed
        results.append({
            "name": budget["name"],
            "actual_tokens": actual,
            "max_tokens": maximum,
            "remaining": maximum - actual,
            "status": "PASS" if passed else "FAIL",
            "files": files,
        })

    output = {
        "status": "FAIL" if failed else "PASS",
        "tokenizer": config["tokenizer"],
        "tiktoken_version": tiktoken.__version__,
        "results": results,
    }
    if args.json:
        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        print(f"[{'FAIL' if failed else 'PASS'}] Token 预算校验（{config['tokenizer']}）")
        for item in results:
            print(
                f"  {'✓' if item['status'] == 'PASS' else '✗'} {item['name']}: "
                f"{item['actual_tokens']} / {item['max_tokens']} "
                f"(余量 {item['remaining']})"
            )
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
