# 贡献指南

本仓库维护一个可验证、可追溯且按需加载的 UI 文案审查 Skill。改动应保持规则判断安全，同时避免扩大普通任务的上下文成本。

## 贡献类型

| 类型 | 示例 |
|---|---|
| 规则完善 | 增加有触发条件、例外和示例的 `HF-`、`PX-` 或 `SPT-` 规则。 |
| 流程优化 | 改进加载路由、分级、跨页核对、清单或治理流程。 |
| 模板与脚本 | 改进 Prompt、输出 schema、校验或 token 预算。 |
| 来源更新 | 在确认授权和适用边界后更新结构化来源规则。 |

不要提交未经确认的业务定义、法律结论、安全口径、品牌术语或英文译文。

## 文件职责

- `SKILL.md`：只保留运行边界、默认值、一级路由和最小输出契约。
- `references/hf-core.md`：所有审查共用的证据与语义边界。
- `references/hf-punctuation.md`：`HF-PUN-*`、`HF-SPC-*`。
- `references/hf-format.md`：`HF-MIX-*`、`HF-NUM-*`。
- `references/hf-state-feedback.md`：`HF-STA-*`、`HF-FBK-*`。
- `references/hf-terminology-components.md`：`HF-TERM-*`、`HF-CMP-*`。
- `references/hf-language.md`：`HF-LNG-*`。
- `references/paletx-design-system-copy-spec.md`、`system-prompt-patterns.md`：显式启用的来源规则。
- `references/change-list-schema.md`、`coverage-gap-schema.md`：按需交付 schema。
- `references/source-register.md`：来源和维护状态，不承载运行规则。

规则只维护在一个位置。不要在 `SKILL.md`、Prompt、README 和 schema 中复制规则正文。

## 规则要求

新增规则使用唯一稳定编号。每条规则至少说明适用条件、判断标准、必要例外，并在可安全确定时提供示例。无法验证的偏好不能成为强制规则。

| 前缀 | 适用内容 |
|---|---|
| `HF-` | 通用高频规则。 |
| `PX-` | PaletX/ZTE 来源规则。 |
| `SPT-` | 系统提示信息来源规则。 |
| `COPY-` | 可执行修改条目。 |
| `UC-` | 规范治理条目。 |

新 HF 规则必须放入最窄的现有分片；只有确实无法归类时才新增分片，并同步 `SKILL.md` 路由与 token 预算。

## 来源与公开性

外部来源同步登记来源 ID、名称、公开地址、提取日期、版本、覆盖范围、状态和维护规则。内部或受限来源不得公开 URL、正文、截图、账号或访问路径，只保留脱敏元数据。发现安全问题时不要通过公开 Issue 或 PR 暴露细节。

## 版本

修改 `SKILL.md`、规则、Prompt、输出、脚本或默认行为时更新 `docs/VERSION_HISTORY.md`；影响使用方式时同步根目录和 `docs/README.md`。

- 不兼容的默认行为或输出变化：主版本。
- 新增兼容能力或规则集：次版本。
- 文案、链接、元数据或兼容修正：修订版本。

## 校验

```bash
python3 scripts/validate_skill_consistency.py --strict
python3 scripts/validate_token_budget.py
python3 "$SKILL_CREATOR/scripts/quick_validate.py" /absolute/path/to/prototype-ui-copy-review
python3 -m json.tool evals/evals.json > /dev/null
python3 -m json.tool evals/trigger-eval.json > /dev/null
git diff --check
```

`validate_token_budget.py` 使用 `tiktoken==0.14.0` 与 `o200k_base`。不要仅提高预算来让 CI 通过；先说明增加成本的必要性，并优先拆分或按需加载。

修改 `SKILL.md`、description 或路由时，对比 `evals/evals.json` 与 `evals/trigger-eval.json`。PR 应说明：问题与动机、改动范围、兼容性、规则/来源依据、校验结果、token 变化和敏感信息复核。
