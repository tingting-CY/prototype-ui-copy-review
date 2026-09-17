# 原型界面文案审查 Skill

> **版本：v2.0.0**
> **用途：** 审查简体中文 UI 文案，并以尽量小的规则上下文输出可验证、可执行的修改建议。

## 适用范围

Skill 适用于 Web、移动端、后台、小程序和桌面端的用户可见文本，包括标题、导航、字段、占位符、按钮、弹窗、帮助说明、状态、成功/失败反馈、空状态与风险提示。输入可以是截图、原型链接、录屏、文案表格、PRD 或混合材料。

它不处理翻译与本地化、营销长文案、视觉与交互走查或代码中的 i18n 资源治理。无法验证的业务、技术、安全、法务和品牌口径标记为“待确认”。

## 执行模式

| 模式 | 触发 | 输出 |
|---|---|---|
| 少量文案问答 | 1–5 条明确文案，询问是否合规或怎么改。 | 每条仅输出结论、依据、建议。 |
| 页面/流程审查 | 提供页面、截图、流程、文案表或 PRD。 | 直接按默认范围审查；P3 默认省略。 |
| 规范维护 | 要求完善设计规范、补规则或识别覆盖缺口。 | 输出规则维护建议；需要时生成 `UC-` 表。 |

页面/流程请求不再先展示维度菜单。用户已经提供材料时直接执行；缺少材料或存在会实质改变结论的关键信息时才追问。

## 默认加载策略

| 模块 | 默认行为 |
|---|---|
| `hf-core.md` | 每次审查加载。 |
| HF 分类规则 | 只加载材料命中的分类。 |
| 跨页面一致性 | 两个及以上相关页面/状态时启用。 |
| `PX-` | 明确指定 PaletX/ZTE 或项目已确认采用时加载。 |
| `SPT-` | 明确指定系统产品提示信息规范、常用句型或 `SPT-` 时加载；一般反馈使用 HF。 |
| 项目规则 | 提供有效项目规范、术语表或合规口径时加载。 |
| `COPY-` | 明确要求修改清单、Markdown 导出或给开发替换时生成。 |
| `UC-` | 明确要求治理规范、补规则或识别覆盖缺口时生成。 |
| `source-register.md` | 仅核验来源、处理冲突或维护规则时读取。 |

用户可以直接用自然语言覆盖默认值，例如“跳过 PX”“只查标点和状态”“包含 P3”“给开发替换清单”。不需要使用配置协议。

## HF 分片路由

| 材料信号 | 规则文件 | 代表规则 |
|---|---|---|
| 所有审查 | `hf-core.md` | `HF-GEN-*` |
| 标点、空格、省略号 | `hf-punctuation.md` | `HF-PUN-*`、`HF-SPC-*` |
| 中英文、数字、日期、单位 | `hf-format.md` | `HF-MIX-*`、`HF-NUM-*` |
| 动作、状态、反馈、校验、风险 | `hf-state-feedback.md` | `HF-STA-*`、`HF-FBK-*` |
| 术语、标题、按钮、字段、占位符 | `hf-terminology-components.md` | `HF-TERM-*`、`HF-CMP-*` |
| 语法、语气、可读性 | `hf-language.md` | `HF-LNG-*` |

“完整审查”表示完整检查材料实际包含的类型，而不是机械加载全部规则文件。

## 规则优先级

```text
安全 / 法律 / 项目专属规范
        ↓
已确认的来源规则（PX- / SPT-）
        ↓
HF 通用规则
        ↓
材料内语义明确且一致的既有口径
        ↓
建议统一
```

每项“违反规则”必须保留位置、原文和适用编号。来源或业务信息不足时，不把偏好包装为规则。

## 输出

### 少量文案问答

```markdown
1. **结论：** 不符合
   **依据：** HF-PUN-05
   **建议：** “正在加载...”改为“正在加载……”。
```

该模式不输出 P0–P3、范围矩阵、`COPY-` 或 `UC-`。

### 页面/流程审查

先用一句话说明范围、规则和限制，再按优先级输出：**位置、原文、改为、依据、影响范围**。

| 级别 | 条件 |
|---|---|
| P0 | 可能导致错误操作、误导关键结果或掩盖不可逆风险。 |
| P1 | 关键流程对象、动作、状态或术语冲突。 |
| P2 | 可验证的书写、格式、语气或局部命名不一致。 |
| P3 | 无明确规则冲突的可读性优化；默认省略。 |

### Markdown 修改清单

只有用户明确要求时读取 `change-list-schema.md` 并生成 `COPY-` 表。普通审查不再重复生成一份内容相同的报告和清单。

### 规范缺口

只有用户明确要求规范治理时读取 `coverage-gap-schema.md`。`UC-` 条目不是缺陷，不使用 P0–P3，也不提供未经确认的唯一改写。

## v1 → v2 迁移

| v1 行为 | v2 行为 |
|---|---|
| 模糊页面请求先展示 A–F 菜单 | 直接按默认范围审查。 |
| 一般反馈自动加载 SPT | 一般反馈使用 HF；只有明确指定来源规范才加载 SPT。 |
| 有 P0/P1/P2 时自动生成修改清单 | 只有用户明确要求时生成。 |
| 规范缺口默认自动检查 | 只有治理请求才检查。 |
| HF 规则单文件加载 | 按类别分片，75 个规则编号保持不变。 |
| 常见输出包含范围矩阵和重复清单 | 默认一句范围声明加紧凑问题列表。 |

依赖旧自动行为的调用方应在任务中明确加入“生成 Markdown 修改清单”“按 SPT 规范”或“识别规范缺口”。

## 自定义助手

配置系统提示词或 API 工作流时读取 `references/prompt-templates.md`。稳定行为放入系统提示词；项目术语、来源规则、业务口径和本次材料动态传入。

## 资源索引

| 资源 | 何时读取 |
|---|---|
| `SKILL.md` | 运行边界、默认值、路由和输出契约。 |
| `references/hf-core.md` | 所有审查共用边界。 |
| `references/hf-punctuation.md` | 标点与空格。 |
| `references/hf-format.md` | 中英文与数据格式。 |
| `references/hf-state-feedback.md` | 动作、状态与反馈。 |
| `references/hf-terminology-components.md` | 术语、命名与组件。 |
| `references/hf-language.md` | 语法、语气与可读性。 |
| `references/paletx-design-system-copy-spec.md` | 明确使用 PaletX/ZTE。 |
| `references/system-prompt-patterns.md` | 明确使用 SPT 来源规范。 |
| `references/change-list-schema.md` | 用户要求 Markdown 修改清单。 |
| `references/coverage-gap-schema.md` | 用户要求规范治理。 |
| `references/prompt-templates.md` | 配置自定义助手或调用模板。 |
| `references/source-register.md` | 来源核验、冲突或维护。 |
| `docs/VERSION_HISTORY.md` | 版本与迁移记录。 |
| `evals/evals.json` | 行为回归。 |
| `evals/trigger-eval.json` | 触发准确率回归。 |
| `evals/token-budgets.json` | Token 预算定义。 |
| `scripts/validate_token_budget.py` | Token 预算校验器。 |

## 校验

```bash
python3 scripts/validate_skill_consistency.py --strict
python3 scripts/validate_token_budget.py
python3 /path/to/skill-creator/scripts/quick_validate.py /absolute/path/to/prototype-ui-copy-review
git diff --check
```

修改规则或默认行为后，同步更新版本记录、回归用例和 token 预算。不要为了压缩 token 删除会影响判定安全性的适用边界或例外；优先通过分片和按需加载控制成本。
