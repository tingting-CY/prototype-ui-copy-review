---
name: prototype-ui-copy-review
description: 审查原型、线框图、页面流程、界面截图或产品需求中的简体中文 UI 文案。用于发现术语、命名、标点、格式、状态提示、反馈文案与跨页面一致性问题，并输出带规则依据、可直接落地的修改建议和 Markdown 修改清单。
---

# 原型界面文案规范性与一致性审查

## 目标与边界

审查用户可见的页面标题、导航、字段、占位符、按钮、弹窗、帮助说明、空状态、成功/失败反馈和风险提示。输入可以是截图、原型链接、录屏、文案清单、需求文档或混合材料。

只基于可见文字、结构化材料和已确认规则下结论。不要猜测模糊、截断、未提供或无法进入的内容；不要把视觉、交互、功能完整性或未证实的业务规则当作文案缺陷。业务定义、法务/安全口径、技术参数或品牌术语不明确时，标记为“待确认”或“规范待维护项”。

## 资源路由

按任务需要读取最少的参考文件，不要将所有规则机械套用。

| 任务或材料特征 | 必读资源 | 作用 |
|---|---|---|
| 任意审查任务 | 本文件 | 确定边界、优先级、流程和交付要求。 |
| 用户要求选择、跳过、仅提示或按页面差异化审查项 | [`references/review-scope-configuration.md`](references/review-scope-configuration.md) | 解析 `core`、`px`、`spt`、`project`、`cross_page`、`coverage_gap` 和 `change_list` 的任务级/页面级配置。 |
| 用户只要求“审查/检查”，但未说明检查维度 | [`references/review-dimension-confirmation.md`](references/review-dimension-confirmation.md) | 先用一次性菜单确认维度或推荐组合，再映射为模块配置。 |
| 标点、状态、中英文混排、数字单位、术语、组件或风险提示 | [`references/high-frequency-copy-rules.md`](references/high-frequency-copy-rules.md) | 加载适用的 `HF-` 默认规则、例外与改写示例。 |
| 用户指定 PaletX/ZTE 设计系统 | [`references/source-register.md`](references/source-register.md)；[`references/paletx-design-system-copy-spec.md`](references/paletx-design-system-copy-spec.md) | 使用已提炼的 `PX-` 规则，并说明来源状态。 |
| 审查成功、失败、错误、异常或常用提示句型 | [`references/source-register.md`](references/source-register.md)；[`references/system-prompt-patterns.md`](references/system-prompt-patterns.md) | 使用已验证的 `SPT-` 句型和提示信息结构。 |
| 配置自定义审查助手、调用模板或设计系统维护模式 | [`references/prompt-templates.md`](references/prompt-templates.md) | 提供系统提示词、输入协议和调用模板。 |
| 需要交付可勾选的 Markdown 修改清单 | [`references/markdown-change-list.md`](references/markdown-change-list.md) | 规定筛选、编号、分组、模板和文件命名。 |
| 需要识别现有规范未覆盖的文案场景 | [`references/uncovered-copy-scenarios.md`](references/uncovered-copy-scenarios.md) | 判定新场景、业务语义缺失、格式缺失、来源不完整或规则冲突，并输出设计评估清单。 |
| 需要了解功能、版本或变更历史 | [`docs/README.md`](docs/README.md)；[`docs/VERSION_HISTORY.md`](docs/VERSION_HISTORY.md) | 提供用户可读介绍与可追溯版本记录。 |
| 修改 Skill 后需要预检结构一致性 | [`scripts/validate_skill_consistency.py`](scripts/validate_skill_consistency.py) | 校验必需文件、内部链接、资源路由、README/版本同步和来源登记结构。 |

## 规则优先级与证据要求

按以下顺序判断：**明确的安全、法律或项目专属规范** > **已确认的设计系统与提示信息规范（`PX-` / `SPT-`）** > **通用高频规则（`HF-`）** > **同一材料中语义明确且一致的既有口径** > **建议统一**。

每项“违反规则”都必须保留原文、位置和适用规则编号。没有可验证规则或冲突证据时，不把偏好写成硬性错误；改为“建议统一”或“待确认”。来源未完整提炼时，仅使用其已验证范围，不得补写规则或英文口径。

## 审查流程

1. **界定范围并确认维度。** 记录材料类型、已覆盖页面/状态、可见文字和限制。用户已指定规则、维度、排除项或“完整审查”时直接解析配置；仅说“审查/检查”时，按 `review-dimension-confirmation.md` 追问一次。用户回复选项、自然语言范围或“按推荐执行”后再继续。
2. **建立选择后的基线。** 将确认的维度映射为任务级/页面级模块配置；仅加载本次已启用的项目规范、来源规则或 `HF-` 分类。对 `off` 模块不作判定，对 `notice` 模块只在范围说明中标识未审查。
3. **逐项核验。** 结合组件角色检查书写、术语、格式、状态、反馈和风险提示；不要用一种句式规则判断所有组件。
4. **横向核对。** 比较同一对象和动作在导航、标题、字段、按钮、弹窗、列表、详情和状态反馈中的表达；关键流程还要检查入口、进行中、成功、失败、无结果、无权限、不可用和确认是否闭环。
5. **分级、改写与识别缺口。** 为可判定问题以最小改动给出可复制文本；同时识别没有可适用规则、但值得建立规范的文案场景。不得改变权限、数据范围、价格、时限、可逆性、合规义务或真实系统状态。
6. **交付与沉淀。** 先声明用户确认的审查维度，以及实际启用、跳过和仅提示的模块；再输出简洁审查报告。有明确位置、原文与改法的 P0/P1/P2 项按 `change_list` 配置生成 Markdown 修改清单。将规则冲突、缺失或频繁复发的问题列为“规范待维护项”；仅在 `coverage_gap` 启用时，将无法由现有规范给出唯一结论的场景列为“未涉及规范场景文案”。

## 分级与输出

| 级别 | 使用条件 | 默认处理 |
|---|---|---|
| P0 | 可能导致错误操作、误导关键结果、掩盖不可逆风险或阻断关键理解。 | 上线前修复。 |
| P1 | 关键流程中的对象、动作、状态或术语冲突。 | 本轮评审修复。 |
| P2 | 可验证的书写、格式、语气或局部命名不一致。 | 纳入近期治理。 |
| P3 | 无明确规则冲突或用户风险的可读性优化。 | 按需处理。 |

报告先说明范围、规则基线与限制；随后列出按优先级排序的问题。每条可执行问题至少包括：**位置、原文、直接改写、依据、影响范围**。不确定的业务、技术、安全、法务或术语问题只进入待确认项，不伪装为可直接替换。

当 `coverage_gap` 为 `auto` 或 `on` 时，按 `uncovered-copy-scenarios.md` 单独检查是否存在未被现有规范覆盖的文案场景。该清单不使用 P0–P3，不给出伪造的直接替换文案；仅记录场景证据、未覆盖原因、设计师需评估的内容和最小规范动作。`coverage_gap: off` 时不输出该章节。

除非用户明确要求，不重写全部页面文案。用户要求“给开发直接替换”“极简清单”或“导出 Markdown”时，使用 `markdown-change-list.md` 的对应模板。

## Skill 维护与文档同步

修改本 Skill 的 `SKILL.md`、`references/`、来源登记、提示词、输出行为或 `docs/` 时，必须同步执行：

1. 判断用户可见能力、使用方式、规则范围或限制是否变化；若变化，更新 `docs/README.md`。
2. 升级或确认版本号，并在 `docs/VERSION_HISTORY.md` 顶部记录变更原因、受影响文件、兼容性、来源边界和校验结果。
3. 文档同步后依次运行 `python3 scripts/validate_skill_consistency.py` 与 Skill 结构校验；若校验失败，修复后重新运行，并更新版本记录。

不要在本文件重复规则库、提示词模板、修改清单模板、来源细节或完整版本历史；以上资源是各自内容的唯一维护位置。
