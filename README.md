# prototype-ui-copy-review

> 面向原型、线框图、页面流程、界面截图、录屏、文案清单与需求文档的**简体中文 UI 文案规范性与一致性审查 Skill**。

该 Skill 面向产品、设计与研发协作场景，审查用户可见文案中的术语、命名、标点、格式、状态反馈、风险提示与跨页面一致性问题。它输出带规则依据的审查结论和可直接落地的改写建议，而不会把无法验证的业务猜测包装成文案缺陷。

## 能力概览

| 能力 | 用途 |
|---|---|
| 分层规则审查 | 按项目专属规范、`PX-` / `SPT-` 规则与 `HF-` 高频规则的优先级核验。 |
| 单条文案直接问答 | 对 1–5 条明确 UI 文案直接返回“结论、依据、建议”。 |
| 完整页面与流程审查 | 对截图、原型、录屏、文案表格或需求文档进行分级审查与横向一致性核对。 |
| 可执行修改清单 | 为明确的问题生成可勾选、可追溯的 `COPY-` Markdown 修改项。 |
| 规范缺口治理 | 以 `UC-` 记录现有规则尚未覆盖、但值得治理的真实场景。 |
| 可重复校验 | 内置结构一致性、链接、来源登记、版本与回归用例校验。 |

## 适用范围

适用于 Web、移动端、后台系统、小程序和桌面端的**用户可见文本**，包括标题、导航、字段、占位符、按钮、弹窗、帮助说明、空状态、成功/失败反馈和风险提示。

> [!IMPORTANT]
> 请将整个目录作为一个 Skill 保留。不要单独复制 `SKILL.md`、规则文件或提示词模板；主流程会按任务需要加载 `references/`、`docs/`、`evals/` 与 `scripts/` 中的关联资源。

以下内容不属于本 Skill 的范围：翻译或多语言本地化、营销长文案创作、视觉与交互走查，以及代码中的 i18n 资源整理。业务定义、法务/安全口径、技术参数或品牌术语不明确时，Skill 会标记为“待确认”或“规范待维护项”。

## 安装

最新版为 [v1.11.0](https://github.com/tingting-CY/prototype-ui-copy-review/releases/tag/v1.11.0)，包含完整安装包和 SHA-256 校验文件。

| 方式 | 操作 |
|---|---|
| Release 安装包 | 下载 [`prototype-ui-copy-review-v1.11.0.skill`](https://github.com/tingting-CY/prototype-ui-copy-review/releases/download/v1.11.0/prototype-ui-copy-review-v1.11.0.skill)，并按需下载对应的 [SHA-256 校验文件](https://github.com/tingting-CY/prototype-ui-copy-review/releases/download/v1.11.0/prototype-ui-copy-review-v1.11.0.skill.sha256)。 |
| Git 克隆 | 克隆仓库后，将完整的 `prototype-ui-copy-review/` 目录导入支持本地 Skill 的宿主环境。 |

```bash
git clone https://github.com/tingting-CY/prototype-ui-copy-review.git
```

不同 AI 工具的本地 Skill 导入位置和步骤可能不同；请使用所选工具提供的导入方式，并始终保留完整目录结构。本仓库没有浏览器端执行入口。

## 使用模式

| 模式 | 触发方式 | 输出 |
|---|---|---|
| 单条文案直接问答 | 一次发送 1–5 条明确 UI 文案，并询问是否合规、有没有问题或怎么改。 | 按输入顺序返回“结论、依据、建议”；不生成完整报告、`COPY-` 清单或 `UC-` 表。 |
| 页面或流程审查 | 提供截图、原型、录屏、文案表格或需求文档。 | 在未指定范围时先确认 A–F 审查维度，再按适用规则输出问题与直接改写。 |
| 完整审查与清单 | 明确要求完整审查、跨页面比对、评审材料或 Markdown 清单。 | 输出 P0–P3 审查报告；按配置生成 `COPY-` 修改清单与 `UC-` 规范缺口列表。 |

### 示例请求

```text
删除确认弹窗按钮写“确定”合规吗？

请直接检查：正在加载...；操作成功；确定删除？

按 PaletX 设计系统审查“成员邀请”流程，重点检查术语、按钮和状态反馈。

本页不涉及 PX 规范，跳过 PX；仅检查上传失败提示和高频文案问题。

完整审查这批截图，并生成给开发直接替换的 Markdown 清单。
```

当用户只说“审查这个页面”而未说明范围时，Skill 会先给出一次性 A–F 检查维度菜单；用户可回复选项、自然语言范围、“按推荐执行”或“完整审查”。完整调用协议、模块配置与输出边界见 [docs/README.md](docs/README.md)。

## 规则与输出

| 标识 | 内容 |
|---|---|
| `HF-` | 高频 UI 文案规则，覆盖标点、状态、中英文混排、数字单位、术语、组件和风险提示。 |
| `PX-` | 已提炼的 PaletX/ZTE 设计系统文案规则；仅在用户明确指定且适用时加载。 |
| `SPT-` | 系统提示信息句型，覆盖成功、失败、错误、异常与常用反馈。 |
| `COPY-` | 标识可执行、可勾选的 Markdown 修改清单条目。 |
| `UC-` | 记录无法由现有规则给出唯一结论、但值得建立规范的场景。 |

规则优先级为：**明确的安全、法律或项目专属规范** > **已确认的 `PX-` / `SPT-` 规范** > **`HF-` 通用高频规则** > **材料中语义明确且一致的既有口径** > **建议统一**。

## 项目结构

```text
.
├── SKILL.md                          # 审查边界、资源路由、流程与交付要求
├── references/                       # HF-/PX-/SPT- 规则、模板、配置与来源登记
├── docs/
│   ├── README.md                     # 完整使用手册
│   └── VERSION_HISTORY.md            # Skill 功能迭代记录
├── scripts/
│   └── validate_skill_consistency.py # 结构、链接、来源与敏感信息校验
├── evals/
│   ├── evals.json                    # 回归用例与断言
│   └── trigger-eval.json             # description 触发准确率测试集
├── .github/workflows/                # 自动结构校验工作流
├── CONTRIBUTING.md                   # 贡献规则与维护流程
└── .gitignore
```

## 本地校验

在包含本目录的 Skills 根目录中运行：

```bash
python3 prototype-ui-copy-review/scripts/validate_skill_consistency.py --strict --root prototype-ui-copy-review

# 若本机已安装 skill-creator：
python3 /path/to/skill-creator/scripts/quick_validate.py prototype-ui-copy-review
```

第一项会检查必需文件、资源路由、本地链接、版本同步、来源登记、回归用例以及内部链接和机器专属路径。第二项检查 Skill 的基础结构。修改 `SKILL.md`、流程、规则或 description 后，建议再使用 `evals/evals.json` 和 `evals/trigger-eval.json` 进行回归验证。

## 项目资源

| 资源 | 说明 |
|---|---|
| [完整使用手册](docs/README.md) | 调用方式、审查范围、模块配置和输出格式。 |
| [版本记录](docs/VERSION_HISTORY.md) | 从 v1.0.0 到当前版本的功能变更。 |
| [维护指南](CONTRIBUTING.md) | 规则编号、来源治理、校验与提交要求。 |
| [最新 Release](https://github.com/tingting-CY/prototype-ui-copy-review/releases/tag/v1.11.0) | v1.11.0 完整 `.skill` 安装包与 SHA-256 文件。 |

请勿提交凭据、内部系统地址、未获授权的截图、内部文档正文或未经确认的业务、法务与安全口径。来源登记仅保留经确认可公开的外部链接；内部来源应使用来源编号和脱敏描述。
