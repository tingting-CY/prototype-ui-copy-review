---
name: prototype-ui-copy-review
description: 审查简体中文 UI 文案的规范性与一致性，适用于原型、线框图、界面截图、录屏、文案清单或 PRD；检查标题、字段、按钮、弹窗、状态/错误提示、术语、标点和跨页面一致性，并可输出规则编号及 Markdown 修改清单。用户要求检查、审查或 review 界面文字，或询问少量 UI 文案是否合规时使用。指定 PaletX/ZTE 或提示信息规范时加载对应来源规则。不用于翻译、本地化、营销写作、视觉/交互审查或 i18n 代码治理。
---

# 中文 UI 文案审查

## 核心边界

只根据可见文字、明确材料和已确认规则下结论。不要猜测模糊、截断或未提供的内容，也不要把视觉、交互或未证实的业务规则当作文案缺陷。改写不得改变权限、价格、时限、数据范围、可逆性、合规义务或真实状态；无法确认时标记“待确认”。

规则优先级：**安全/法律/项目专属规范 > 已确认的来源规则 > 通用规则 > 材料内一致口径 > 建议统一**。每项硬性问题必须保留位置、原文和规则编号；没有规则依据时不要写成“违反规范”。

## 选择模式

1. **少量文案问答**：用户提供 1–5 条明确 UI 文案并询问是否合规或怎么改时，直接逐条输出“结论、依据、建议”，不生成范围表、P0–P3、`COPY-` 或 `UC-`。
2. **页面/流程审查**：其他情况直接按默认范围执行；不要仅因用户说“看看/检查”而先追问菜单。缺少审查材料时再请求材料。
3. **规范维护**：仅当用户要求完善规则或治理规范时，检查规则冲突、缺失、例外、版本和所有者。

## 默认范围

| 模块 | 默认行为 |
|---|---|
| 通用规则 | 始终启用，只加载材料命中的 `HF-` 分片。 |
| 跨页面一致性 | 有两个及以上相关页面或状态时启用。 |
| PaletX/ZTE | 仅在用户或项目明确指定时启用，并引用 `PX-`。 |
| SPT 来源规则 | 仅在用户或项目明确指定“系统产品提示信息规范”“常用句型”或 `SPT-` 时启用；一般反馈使用 HF 规则。 |
| 项目规范 | 用户提供有效术语、品牌、业务、安全或法务规则时启用。 |
| `COPY-` 修改清单 | 仅在用户要求清单、导出或“给开发直接替换”时生成。 |
| `UC-` 规范缺口 | 仅在用户要求规范治理、补规则或识别覆盖缺口时生成。 |

直接遵循用户指定的范围、排除项或页面差异。设计系统未确认时使用通用规则，并说明未加载来源规则。

## 最小资源路由

先识别组件和问题类型，只读取命中文件；“完整审查”也不读取材料未涉及的类别。

| 信号 | 读取 |
|---|---|
| 所有审查 | [`references/hf-core.md`](references/hf-core.md) |
| 标点、空格、省略号 | [`references/hf-punctuation.md`](references/hf-punctuation.md) |
| 中英文、数字、日期、时间、金额、单位 | [`references/hf-format.md`](references/hf-format.md) |
| 动作、状态、成功、失败、空状态、校验、风险 | [`references/hf-state-feedback.md`](references/hf-state-feedback.md) |
| 术语、标题、字段、按钮、占位符、组件 | [`references/hf-terminology-components.md`](references/hf-terminology-components.md) |
| 语法、语气、可读性 | [`references/hf-language.md`](references/hf-language.md) |
| 明确指定 PaletX/ZTE | [`references/paletx-design-system-copy-spec.md`](references/paletx-design-system-copy-spec.md) |
| 明确指定系统提示信息规范/SPT | [`references/system-prompt-patterns.md`](references/system-prompt-patterns.md) |
| 要求 Markdown 修改清单 | [`references/change-list-schema.md`](references/change-list-schema.md) |
| 要求规范缺口治理 | [`references/coverage-gap-schema.md`](references/coverage-gap-schema.md) |
| 配置自定义助手 | [`references/prompt-templates.md`](references/prompt-templates.md) |
| 核验或维护来源 | [`references/source-register.md`](references/source-register.md) |

维护文档、评测和版本记录不参与普通审查。

## 审查流程

1. 提取页面、组件、状态、原文及可见限制。
2. 建立对象、动作、状态、格式和术语基线。
3. 按组件语境应用已加载规则；合并同一根因的多处问题。
4. 多页面时核对同一对象、动作和状态；仅在材料覆盖时检查入口、进行中、成功、失败、无结果、无权限、不可用和确认。
5. 给出保持业务语义的最小改写；不确定项单列“待确认”。
6. 仅按用户要求生成 `COPY-` 清单或 `UC-` 治理表。

## 分级与输出

| 级别 | 条件 |
|---|---|
| P0 | 可能导致错误操作、误导关键结果或掩盖不可逆风险。 |
| P1 | 关键流程中的对象、动作、状态或术语冲突。 |
| P2 | 可验证的书写、格式、语气或局部命名不一致。 |
| P3 | 无明确规则冲突的可读性优化；只有用户明确要求时输出。 |

页面/流程审查先用一句话声明范围、规则和限制，再按优先级列问题。每项包含：**位置、原文、改为、依据、影响范围**。没有问题时说明未发现当前范围内的可验证问题。

不要重复输出完整规则、推理过程或两份内容相同的“报告 + 清单”。用户要求极简交付时直接输出：`编号 | 优先级 | 位置 | 原文 | 修改后 | 依据`。

## 维护

修改本 Skill 时，按 [`CONTRIBUTING.md`](CONTRIBUTING.md) 同步 [`docs/README.md`](docs/README.md) 与 [`docs/VERSION_HISTORY.md`](docs/VERSION_HISTORY.md)，并运行结构、token 预算和回归校验。
