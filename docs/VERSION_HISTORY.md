# 原型界面文案审查 Skill：版本更新记录

> 文档状态：当前生效  
> 当前版本：**v1.11.0**
> 更新日期：2026-08-20（GMT+8）  
> 适用对象：`prototype-ui-copy-review` Skill 及其参考规则、模板和来源登记。

## 版本策略

本 Skill 使用语义化版本号 `主版本.次版本.修订版本`。当审查流程、规则优先级、输出字段或兼容性发生不兼容变化时，升级主版本；当新增可复用的规则库、来源规范或输出能力时，升级次版本；当仅修正文案、示例、链接、规则编号或维护元数据时，升级修订版本。

每次修改 Skill 的 `SKILL.md`、`references/` 下的规则库、来源登记、提示词模板、交付模板、`scripts/`、`docs/README.md` 或本文件后，均必须在本文件新增一条版本记录。记录应保留改动原因、受影响文件、行为变化、兼容性和校验状态；不要只记录“优化”“调整”等不可追溯描述。

## 当前版本概览

| 版本 | 日期 | 类型 | 核心变化 | 兼容性 |
|---|---|---|---|---|
| v1.11.0 | 2026-08-20 | 次版本 | 新增一至五条 UI 文案的直接问答校验模式，直接给出合规结论、依据和最小建议。 | 向后兼容；完整审查、维度确认与修改清单流程不变。 |
| v1.10.0 | 2026-08-20 | 次版本 | 按 skill-creator 方法优化触发描述与主文件结构，补齐 SPT 来源脱敏，新增回归用例、触发测试集与敏感信息校验。 | 向后兼容；审查规则、分级与输出格式不变。 |
| v1.9.1 | 2026-08-20 | 修订版本 | 为公开仓库新增根目录 README 与贡献指南，并脱敏内部来源链接及页面元数据。 | 向后兼容；不改变审查规则、输出行为或已提炼范围。 |
| v1.9.0 | 2026-08-20 | 次版本 | 新增审查前维度确认与推荐组合，未指定范围时先引导用户选择检查项。 | 向后兼容；明确“完整审查”或具体维度时仍直接执行。 |
| v1.8.0 | 2026-08-20 | 次版本 | 新增任务级与页面级审查项选择，支持跳过不适用的 PX、SPT、跨页面检查、规范缺口或修改清单。 | 向后兼容；默认 `auto` 行为保持既有按需加载逻辑。 |
| v1.7.0 | 2026-08-20 | 次版本 | 新增未覆盖规范场景文案清单，供设计师评估规则缺口与最小治理动作。 | 向后兼容；不改变既有问题分级或修改清单。 |
| v1.6.0 | 2026-08-20 | 次版本 | 新增自动化结构一致性校验脚本，覆盖引用资源、版本同步与维护记录检查。 | 向后兼容；新增更新后预检步骤。 |
| v1.5.2 | 2026-08-20 | 修订版本 | 整体精炼主流程、Prompt 资产与 README，消除重复规则与模板说明。 | 向后兼容；规则编号、来源和交付能力不变。 |
| v1.5.1 | 2026-08-20 | 修订版本 | 将 README 与版本更新记录集成至 `docs/`，并建立每次 Skill 更新的同步维护约束。 | 向后兼容；文档位置迁移，链接已更新。 |
| v1.5.0 | 2026-08-20 | 次版本 | 接入系统产品“提示信息规范—常用句型”，新增 `SPT-` 规则、来源状态和提示信息审查边界。 | 向后兼容；仅在用户指定该规范或审查提示信息时加载。 |
| v1.4.0 | 2026-08-20 | 次版本 | 新增自动 Markdown 修改清单，支持默认、极简、按优先级、按页面和待确认项输出。 | 向后兼容；审查含可执行 P0/P1/P2 项时默认生成。 |
| v1.3.0 | 2026-08-19 | 次版本 | 接入 PaletX 设计系统文案规范与 `PX-` 规则编号，新增来源登记和冲突处理机制。 | 向后兼容；用户明确指定 PaletX/ZTE 设计系统时加载。 |
| v1.2.0 | 2026-08-20 | 次版本 | 新增 `HF-` 高频文案错误规则库，覆盖标点、状态、中英文混排、数字时间、术语、组件和反馈风险。 | 向后兼容；按材料类型按需加载。 |
| v1.1.0 | 2026-08-20 | 次版本 | 新增系统提示词、调用模板和产品设计系统规范输入协议。 | 向后兼容；用于自定义审查助手和工作流接入。 |
| v1.0.0 | 2026-08-20 | 初始版本 | 建立原型界面文案规范性与一致性审查流程、P0–P3 分级和报告模板。 | 初始发布。 |

---

## 详细更新记录

### v1.11.0 · 少量 UI 文案直接问答校验

**变更类型。** 次版本。

**变更原因。** 用户只需确认一条或少量按钮、提示语、标题等 UI 文案时，完整审查报告、A–F 维度确认和独立修改清单会造成不必要的交互与输出负担。

**新增或修改内容。** 新增“单条文案直接问答”执行路径：用户一次提供一至五条可读、明确的 UI 文案，并直接询问是否合规、有没有问题、这样写是否可以或怎么改时，跳过 A–F 菜单，强制 `core: on`、`cross_page`/`coverage_gap`/`change_list: off`。回答按输入顺序仅输出结论、依据和建议；按类型按需加载 `HF-`、`SPT-`，仅在用户明确指定设计系统时加载 `PX-`。新增自定义助手调用模式 `single_copy_qa`、公开使用说明和回归/触发用例。

**行为变化。** 直接问答模式不输出 P0–P3、完整范围表、`COPY-` 编号、独立 Markdown 修改清单或 `UC-` 表；缺少组件、对象、业务状态或规则依据时输出“待确认”。文本超过五条、要求页面或流程比较、完整报告或清单时，继续使用既有完整审查流程。

**受影响文件。** `SKILL.md`、`references/prompt-templates.md`、`references/review-dimension-confirmation.md`、`README.md`、`docs/README.md`、`evals/evals.json`、`evals/trigger-eval.json`、`docs/VERSION_HISTORY.md`。

**兼容性与迁移。** 向后兼容。既有“审查页面/截图”、完整审查、维度确认、模块配置和 Markdown 修改清单行为不变；调用自定义助手时可选用 `single_copy_qa`。

**来源与边界。** 不新增规则来源。直接问答只能基于当前可见文本与已加载规则下结论，不推断业务、技术、安全、法务或品牌口径。

**校验状态。** 已通过 `python3 scripts/validate_skill_consistency.py --strict`（9 项通过，含 4 条回归用例结构检查与敏感信息扫描）与 `quick_validate.py prototype-ui-copy-review`；`git diff --check` 通过。

### v1.10.0 · skill-creator 优化：触发描述、主文件瘦身、回归用例与敏感信息校验

**变更类型。** 次版本。

**变更原因。** 按 anthropics/skills 的 skill-creator 方法复查本 Skill：description 只描述能力、缺少触发语境，用户说“看看这个页面文案”或只贴截图时可能不触发；`SKILL.md` 常驻加载的维护章节与 `CONTRIBUTING.md` 重复；v1.9.1 的来源脱敏遗漏了 `system-prompt-patterns.md` 中的内部地址与页面元数据；根目录 README 与贡献指南写死了维护者本机的 skill-creator 路径；仓库没有可重复运行的回归用例。

**新增或修改内容。** 重写 `SKILL.md` 的 description，补充触发场景（看看/检查/审查/把关/review、文案规范、提示信息规范、PaletX/ZTE、给开发的替换清单）与不适用场景（翻译、营销文案、视觉交互走查、i18n 资源整理）；在“分级与输出”增加单条问题的写法示例；将“Skill 维护与文档同步”收敛为指向 `CONTRIBUTING.md` 的简短段落，并把维护者资源合并为资源路由表的一行。`references/system-prompt-patterns.md` 移除内部来源地址、页面修改时间与 References 段，使用状态统一为“部分已提炼”；`references/source-register.md` 说明两类规则文件的位置。新增 `evals/evals.json`（3 条带断言的回归用例：完整审查并出极简清单、多页面跳过 PX 只查 HF/SPT、模糊请求先出维度菜单）与 `evals/trigger-eval.json`（20 条应触发/不应触发查询）。`scripts/validate_skill_consistency.py` 新增根目录 README/CONTRIBUTING 与 `evals/evals.json` 必需文件检查、description 长度与尖括号检查、`references/` 与根目录文档的链接检查、回归用例结构检查，以及内部主机/内网路径/私有网段 IP/机器专属 home 目录的敏感内容扫描；修正此前部分检查在已有错误时仍报“通过”的问题。根目录 `README.md`、`CONTRIBUTING.md` 改用 `$SKILL_CREATOR` 变量描述 quick_validate 路径，并补充回归与触发测试说明。

**行为变化。** 审查规则、优先级、P0–P3 分级、模块配置与输出格式不变。触发层面：对未说“审查”但明确要求检查页面文案、截图或原型的请求更稳定地触发；对翻译、营销文案、视觉走查等请求明确不触发。校验层面：公开仓库中再次出现内部链接或机器路径会被脚本判为错误。

**受影响文件。** `SKILL.md`、`README.md`、`CONTRIBUTING.md`、`references/system-prompt-patterns.md`、`references/source-register.md`、`scripts/validate_skill_consistency.py`、`evals/evals.json`、`evals/trigger-eval.json`、`docs/README.md`、`docs/VERSION_HISTORY.md`。

**兼容性与迁移。** 向后兼容。既有调用、规则编号、来源提炼范围与清单格式不变；维护者需保证 `evals/evals.json` 与根目录 README/CONTRIBUTING 存在，否则校验脚本报错。

**来源与边界。** 不新增规则来源。`SRC-SPT-PATTERN-001` 继续为“部分已提炼”的内部来源，仅保留来源编号、提取日期、覆盖范围与脱敏描述。

**校验状态。** 已通过 `python3 scripts/validate_skill_consistency.py --strict`（9 项通过）与 skill-creator `quick_validate.py`。skill-creator 回归评测：3 条用例共 29 条断言，旧版与新版均全部通过。触发测试（20 条查询 × 3 次，每个 description 独立 project root 串行运行）：旧描述应触发 28/30、误触发 0/30；新描述应触发 30/30、误触发 0/30，两者均 20/20 通过阈值。

### v1.9.1 · 公开仓库入口与来源登记脱敏

**变更类型。** 修订版本。

**变更原因。** Skill 已作为公开仓库发布。原有完整使用手册位于 `docs/`，不利于仓库访客快速了解安装、使用和校验方式；同时，来源登记包含不应在公开仓库暴露的内部访问地址与页面元数据。

**新增或修改内容。** 新增根目录 `README.md`，提供能力概览、快速使用、规则编号、目录导航、校验命令、来源边界与许可证提示；新增 `CONTRIBUTING.md`，明确规则编号、来源公开性、敏感信息、文档/版本同步、校验和 PR 要求。将 `SRC-SPT-PATTERN-001` 改为“内部来源（链接不公开）”，保留来源编号、提取日期、覆盖范围、提炼状态与授权维护流程，移除内部访问 URL 和具体页面元数据。同步更新用户文档版本号。

**行为变化。** 不改变既有 `HF-`、`PX-`、`SPT-` 规则、审查流程、默认范围或输出格式；公开协作时，贡献者必须避免提交内部链接、正文、截图、访问路径和其他敏感材料。

**受影响文件。** `README.md`、`CONTRIBUTING.md`、`references/source-register.md`、`docs/README.md`、`docs/VERSION_HISTORY.md`。

**兼容性与迁移。** 向后兼容。现有调用、规则编号和已提炼范围不变；原本依赖内部链接进行维护的人员改为通过授权内部渠道核验来源。

**来源与边界。** 不新增规则来源。内部来源保留为脱敏登记，不表示公开授权、再分发授权或对内部资料的开放访问。

**校验状态。** 已通过 `python3 scripts/validate_skill_consistency.py --strict` 与 `quick_validate.py prototype-ui-copy-review`。

### v1.9.0 · 审查前维度确认与推荐组合

**变更类型。** 次版本。

**变更原因。** 用户通常知道需要“审查页面”，但不一定了解可选择的检查维度；直接按默认规则执行可能导致范围与其实际评审目标不匹配。

**新增或修改内容。** 新增 `references/review-dimension-confirmation.md`，定义追问与直接执行的判断条件、A–F 用户可见维度菜单、材料信号推荐组合、一次性确认问题及选项到模块配置的映射。主流程和系统提示词在用户未指定范围时先确认维度；README 与结构校验脚本同步纳入新能力。

**行为变化。** 用户仅说“审查/检查”时，Skill 会先追问一次并推荐组合；用户可回复选项、自然语言范围、“按推荐执行”或“完整审查”。用户已指定维度、规则、排除项、模块配置或要求直接出结果时，不重复追问。

**受影响文件。** `SKILL.md`、`references/review-dimension-confirmation.md`、`references/prompt-templates.md`、`scripts/validate_skill_consistency.py`、`docs/README.md`、`docs/VERSION_HISTORY.md`。

**兼容性与迁移。** 向后兼容。明确范围的既有调用保持直接执行；仅未指定范围的审查新增一次确认步骤。

**来源与边界。** 不新增外部来源。一次确认只用于选择审查维度，不收集业务、账号或敏感信息；已确认的安全、法律和项目强制规范仍不可被绕过。

**校验状态。** 已通过 `python3 scripts/validate_skill_consistency.py --strict` 与 `quick_validate.py prototype-ui-copy-review`。

### v1.8.0 · 可选审查项与页面级覆盖

**变更类型。** 次版本。

**变更原因。** 同一批审查材料的页面并不总适用 PaletX/ZTE 设计系统、提示信息句型或跨页面检查；若自动生成不适用的模块结论，会增加设计评审噪声。

**新增或修改内容。** 新增 `references/review-scope-configuration.md`，定义 `core`、`px`、`spt`、`project`、`cross_page`、`coverage_gap` 和 `change_list` 模块的 `auto/on/off/notice` 配置、任务级与页面级优先级、自然语言快捷指令和输出声明模板。`SKILL.md`、Prompt 资产和 Markdown 修改清单同步按配置启用、跳过或仅提示模块；结构校验脚本与 README 已纳入新资源。

**行为变化。** 用户可直接说“本页不涉及 PX 规范，跳过 PX”。被设为 `off` 的模块不加载规则、不产生问题或专属章节；`notice` 只记录未审查范围。页面级配置优先于任务级，未指定时保留既有 `auto` 按需加载行为。

**受影响文件。** `SKILL.md`、`references/review-scope-configuration.md`、`references/prompt-templates.md`、`references/markdown-change-list.md`、`scripts/validate_skill_consistency.py`、`docs/README.md`、`docs/VERSION_HISTORY.md`。

**兼容性与迁移。** 向后兼容。既有审查任务不需要修改；未提供配置时沿用 `auto`。项目安全、法律或其他明确强制规范不会因可选配置被绕过。

**来源与边界。** 不新增外部来源。配置只控制本次审查范围和输出，不改变规则库、来源提炼状态或业务口径。

**校验状态。** 已通过 `python3 scripts/validate_skill_consistency.py --strict` 与 `quick_validate.py prototype-ui-copy-review`。

### v1.7.0 · 未覆盖规范场景文案清单

**变更类型。** 次版本。

**变更原因。** 审查中可能出现真实、重要但尚无规则可判定的文案场景；若仅输出待确认或优化建议，设计师难以判断是否需要建立新的场景规范。

**新增或修改内容。** 新增 `references/uncovered-copy-scenarios.md`，定义未覆盖场景的判定边界、排除条件、`UC-` 编号、设计评估字段与治理模板；主流程、系统提示词和 Markdown 修改清单增加独立的“未涉及规范场景文案”章节。结构校验脚本同步检查新增资源、主文件路由与 README 索引。

**行为变化。** 审查结束时，Skill 会在不影响 P0–P3 缺陷清单的前提下，单列没有可适用规则的真实场景。该清单不视为错误，不提供伪造的直接改写，且仅在存在符合条件的场景时输出。

**受影响文件。** `SKILL.md`、`references/uncovered-copy-scenarios.md`、`references/markdown-change-list.md`、`references/prompt-templates.md`、`scripts/validate_skill_consistency.py`、`docs/README.md`、`docs/VERSION_HISTORY.md`。

**兼容性与迁移。** 向后兼容。既有 `COPY-` 清单、`HF-`/`PX-`/`SPT-` 规则和 P0–P3 分级保持不变；新增 `UC-` 仅用于规范治理。

**来源与边界。** 不新增外部来源。未覆盖清单只基于当前已加载规则和可见材料，不能代替设计师、产品或规则负责人对是否立项和如何制定规则的判断。

**校验状态。** 已通过 `python3 scripts/validate_skill_consistency.py --strict` 与 `quick_validate.py prototype-ui-copy-review`。

### v1.6.0 · 自动化结构一致性校验

**变更类型。** 次版本。

**变更原因。** 防止后续分批更新导致 `SKILL.md`、引用资源、README、版本记录和来源登记发生断链或版本不同步。

**新增或修改内容。** 新增 `scripts/validate_skill_consistency.py`。脚本无需第三方依赖，默认校验必需文件、YAML frontmatter、本地 Markdown 链接、资源路由、README 资源索引、README 与版本记录同步、当前版本详细记录字段和来源登记表结构；支持 `--root`、`--json` 与 `--strict`。

**受影响文件。** `scripts/validate_skill_consistency.py`、`SKILL.md`、`docs/README.md`、`docs/VERSION_HISTORY.md`。

**兼容性与迁移。** 向后兼容。后续 Skill 更新须先运行 `python3 scripts/validate_skill_consistency.py`，再运行标准结构校验。

**来源与边界。** 脚本检查当前文件快照的结构一致性，不能在没有版本控制基线的情况下推断某次改动是否遗漏了文档更新。

**校验状态。** 已通过 `python3 scripts/validate_skill_consistency.py --strict` 与 `quick_validate.py prototype-ui-copy-review`。

### v1.5.2 · 整体精炼与引用收敛

**变更类型。** 修订版本。

**变更原因。** 多批次功能接入后，主流程、系统提示词、修改清单说明和 README 出现重复表述，增加加载成本并可能造成后续维护不一致。

**新增或修改内容。** 将 `SKILL.md` 收敛为边界、资源路由、规则优先级、六步流程、分级和交付要求；将 `prompt-templates.md` 收敛为输入分层、系统提示词、调用模板和维护模式；将 README 收敛为用户可见能力、调用方式、资源索引与维护约定。完整规则、来源细节和清单模板继续只保留在各自参考文件中。

**保留能力。** `HF-`、`PX-`、`SPT-` 规则编号与优先级、设计系统来源登记、自动 Markdown 修改清单、设计系统维护模式、P0–P3 分级及文档同步机制均保持不变。

**受影响文件。** `SKILL.md`、`references/prompt-templates.md`、`docs/README.md`、`docs/VERSION_HISTORY.md`。

**兼容性与迁移。** 向后兼容。既有调用指令、规则编号、来源文件和清单文件名无需迁移。

**来源与边界。** 不适用；未扩展或改变任何来源网页的已提炼范围。

**校验状态。** 已通过 `quick_validate.py prototype-ui-copy-review`。

### v1.5.1 · 文档目录集成与同步维护

**变更类型。** 修订版本。

**变更原因。** 将对外功能介绍与版本记录随 Skill 一起分发，并防止后续规则、模板或行为更新后文档失同步。

**新增或修改内容。** 将 README 和版本更新记录迁移至 `docs/README.md`、`docs/VERSION_HISTORY.md`；在 `SKILL.md` 中加入强制同步维护要求；README 内部链接已更新。

**受影响文件。** `SKILL.md`、`docs/README.md`、`docs/VERSION_HISTORY.md`。

**兼容性与迁移。** 向后兼容。原外部维护文档路径已迁移至 Skill 目录；后续以 `docs/` 路径为准。

**来源与边界。** 不适用。

**校验状态。** 已通过 `quick_validate.py prototype-ui-copy-review`。

### v1.5.0 · 系统产品提示信息常用句型

**新增内容。** 新增 `references/system-prompt-patterns.md`，以 `SPT-ACC`、`SPT-PUN` 和 `SPT-PAT` 编号覆盖提示信息准确性结构、标点例外、成功/失败结果性提示、泛化操作状态和对象级错误提示。错误信息默认按“表现/影响 + 原因 + 修复方式”审查；原因、修复方式和英文译文无法验证时，必须进入待确认项。

**来源与边界。** 在 `references/source-register.md` 中登记 `SRC-SPT-PATTERN-001`。该来源当前标记为“部分已提炼”，因此 Skill 不得虚构未读取到的句型；需要新类型句型时，应标记为规范待维护项。

**受影响文件。** `SKILL.md`、`references/system-prompt-patterns.md`、`references/source-register.md`。

**校验状态。** 已通过 `quick_validate.py prototype-ui-copy-review`。

### v1.4.0 · 自动 Markdown 修改清单

**新增内容。** 新增 `references/markdown-change-list.md`，定义自动生成条件、默认排序、`COPY-` 编号、复选框结构、待确认项边界、极简清单和输出文件命名约定。

**行为变化。** 审查发现至少一条原文、位置和直接改法均明确的 P0/P1/P2 问题时，自动输出独立 Markdown 修改清单；没有可执行项时，也必须输出明确结论而不是空表格。

**受影响文件。** `SKILL.md`、`references/markdown-change-list.md`、`references/prompt-templates.md`。

**校验状态。** 已通过结构与元数据校验。

### v1.3.0 · PaletX 设计系统文案规范接入

**新增内容。** 新增 `references/paletx-design-system-copy-spec.md` 和 `references/source-register.md`，将 PaletX 设计系统中的已提炼规范转为可引用的 `PX-` 规则。

**行为变化。** 用户要求依据 PaletX/ZTE 设计系统审查时，Skill 先加载来源登记与 `PX-` 规则；项目专属规范、术语表、法务与安全口径仍优先于设计系统规则。

**受影响文件。** `SKILL.md`、`references/paletx-design-system-copy-spec.md`、`references/source-register.md`。

**校验状态。** 已通过结构与元数据校验。

### v1.2.0 · 高频界面文案错误规则库

**新增内容。** 新增 `references/high-frequency-copy-rules.md`，以 `HF-` 编号描述高频错误、触发条件、例外和直接改写示例。

**覆盖范围。** 标点与空格、状态与时态、中英文混排、数字日期单位、术语命名、组件文案、语法语气，以及错误和风险提示。

**受影响文件。** `SKILL.md`、`references/high-frequency-copy-rules.md`。

**校验状态。** 已通过结构与元数据校验。

### v1.1.0 · 提示词资产与设计系统输入协议

**新增内容。** 新增 `references/prompt-templates.md`，提供系统提示词、任务调用模板、设计系统规范输入协议、审查输出约束和维护模式。

**行为变化。** 可将 Skill 接入自定义审查助手或工作流，并将经确认的产品规范作为最高业务基线。

**受影响文件。** `SKILL.md`、`references/prompt-templates.md`。

**校验状态。** 已通过结构与元数据校验。

### v1.0.0 · 初始发布

**新增内容。** 建立页面/截图/文案清单审查边界、八步工作流、基础规则、跨页面一致性检查、状态闭环、P0–P3 严重性分级与 Markdown 审查报告模板。

**受影响文件。** `SKILL.md`。

---

## 后续更新登记模板

将以下模板复制到本文件顶部的“详细更新记录”区域，并同步更新“当前版本概览”。

```markdown
### vX.Y.Z · [更新主题]

**变更类型。** [主版本 / 次版本 / 修订版本]

**变更原因。** [解决的真实问题或新增能力]

**新增或修改内容。** [规则、流程、来源、模板、字段或行为]

**受影响文件。** `[文件路径]`。

**兼容性与迁移。** [向后兼容 / 不兼容变化 / 迁移动作 / 不适用]

**来源与边界。** [新增来源 ID、提炼状态、适用范围和未覆盖内容；没有则写“不适用”]

**校验状态。** [执行的校验及结果]
```

## 维护检查清单

每次更新前后，完成以下检查：

- [ ] 规则、示例和来源状态与实际文件一致。
- [ ] 所有新增规则都有唯一编号，并明确优先级、例外和适用边界。
- [ ] 不把未核验的网页内容或业务口径写成确定规则。
- [ ] 自动修改清单、系统提示词和审查报告模板仍能引用新增规则。
- [ ] 已更新本文件的版本号、日期、受影响文件和校验结果。
- [ ] 已运行 Skill 结构校验；若校验失败，已在登记中说明修复结果。
