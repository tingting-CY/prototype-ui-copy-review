# prototype-ui-copy-review

> 面向原型、界面截图、页面流程、录屏、文案清单与 PRD 的**简体中文 UI 文案规范性与一致性审查 Skill**。

当前源码版本为 **v2.0.0**。本版本重构了运行时加载路径：普通请求直接审查，只读取材料命中的规则分片；PaletX、SPT、Markdown 修改清单和规范缺口治理均按明确需求加载。

## 能力

| 能力 | 行为 |
|---|---|
| 少量文案问答 | 对 1–5 条明确 UI 文案直接返回“结论、依据、建议”。 |
| 页面与流程审查 | 检查标题、字段、按钮、弹窗、术语、标点、格式、状态反馈、风险和跨页一致性。 |
| 分层规则 | 支持项目规则、PaletX/ZTE（`PX-`）、系统提示信息来源规范（`SPT-`）与通用高频规则（`HF-`）。 |
| 可执行清单 | 用户要求时生成带 `COPY-` 编号的 Markdown 替换清单。 |
| 规范治理 | 用户要求补规范时，以 `UC-` 记录现有规则无法唯一判定的真实场景。 |
| 预算门禁 | CI 检查 Skill 主文件和典型加载路径的 token 上限。 |

## v2 默认行为

| 模块 | 默认值 |
|---|---|
| HF 通用规则 | 启用；按标点、格式、状态反馈、术语组件、语言分片加载。 |
| 跨页面一致性 | 两个及以上相关页面或状态时启用。 |
| PaletX/ZTE | 用户或项目明确指定时启用。 |
| SPT 来源规则 | 用户或项目明确指定“系统产品提示信息规范”“常用句型”或 `SPT-` 时启用。 |
| `COPY-` 清单 | 用户要求清单、导出或“给开发直接替换”时启用。 |
| `UC-` 规范缺口 | 用户要求规范治理、补规则或识别缺口时启用。 |
| P3 优化建议 | 默认省略；用户要求时输出。 |

用户只说“审查这个页面”时，Skill 会直接按默认范围执行，不再先展示 A–F 菜单。材料不足时才请求补充。业务、法务、安全、技术参数或品牌术语不明确时，结果标记为“待确认”，不会猜测。

## 示例

```text
删除确认弹窗按钮写“确定”合规吗？

检查这张设置页截图里的中文文案。

按 PaletX 设计系统审查成员邀请流程，重点检查术语和按钮。

按系统产品提示信息规范检查这些失败提示。

完整审查这批页面，并生成给开发直接替换的 Markdown 清单。

找出这些页面尚未被规范覆盖的文案场景，给出补规则建议。
```

## 安装

克隆后将整个目录导入支持本地 Skill 的宿主环境：

```bash
git clone https://github.com/tingting-CY/prototype-ui-copy-review.git
```

已发布安装包见 [Releases](https://github.com/tingting-CY/prototype-ui-copy-review/releases)。请保留完整目录；不要只复制 `SKILL.md`，否则按需加载的规则分片将不可用。

## 规则结构

```text
references/
├── hf-core.md
├── hf-punctuation.md
├── hf-format.md
├── hf-state-feedback.md
├── hf-terminology-components.md
├── hf-language.md
├── paletx-design-system-copy-spec.md
├── system-prompt-patterns.md
├── change-list-schema.md
├── coverage-gap-schema.md
├── prompt-templates.md
└── source-register.md
```

原有 75 个 `HF-` 规则编号在 v2 中全部保留，仅改变文件组织方式。详细使用方式见[完整使用手册](docs/README.md)，兼容性说明见[版本记录](docs/VERSION_HISTORY.md)。

## 本地校验

```bash
python3 scripts/validate_skill_consistency.py --strict
python3 scripts/validate_token_budget.py
python3 /path/to/skill-creator/scripts/quick_validate.py /absolute/path/to/prototype-ui-copy-review
```

`validate_token_budget.py` 需要 `tiktoken==0.14.0`。GitHub Actions 会自动安装依赖并执行结构、JSON 和 token 预算校验。

## 项目资源

| 资源 | 说明 |
|---|---|
| [完整使用手册](docs/README.md) | 模式、加载策略和输出格式。 |
| [版本记录](docs/VERSION_HISTORY.md) | v2 迁移说明与历史变更。 |
| [维护指南](CONTRIBUTING.md) | 规则、来源、预算和 PR 要求。 |
| [回归用例](evals/evals.json) | 默认直出、显式来源规则、清单与治理行为。 |
| [Token 预算](evals/token-budgets.json) | 主文件与典型运行路径的预算上限。 |

请勿提交凭据、内部系统地址、未授权截图、内部文档正文或未经确认的业务、法务与安全口径。
