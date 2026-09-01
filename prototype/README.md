# 文案审查助手 · 交互原型

本目录是 `prototype-ui-copy-review` Skill 的**可点击 Web 原型**，用于演示这套审查流程在产品界面上的形态：从发起审查、确认 A–F 维度，到三栏审查台、问题清单与规则库。

原型不调用任何模型或服务，全部结论均为写死的示例数据，用于评估交互与信息结构，不能作为审查工具使用。

## 运行

```bash
cd prototype
npm install
npm run dev      # http://localhost:5173
npm run build    # 类型检查 + 生产构建
```

## 覆盖的界面

| 阶段 | 界面 | 进入方式 |
|---|---|---|
| `start` | 首页：拖入截图或直接输入文案，可展开配置审查项 | 初始状态，或点击左上角 logo |
| `dim` | 维度确认：助手先给出 A + B + F 推荐 | 文案为空或超过 5 条时 |
| `quick` | 单条速答：逐条给出结论／依据／建议 | 文案为 1–5 条时 |
| `review` | 三栏审查台：对话 · 标注截图 · 问题清单 | 点击「开始审查」 |

顶栏的维度胶囊、「历史审查」与「规则库」在任何阶段都可用。

## 与 Skill 的对应关系

原型中的编号体系与 [SKILL.md](../SKILL.md) 及 `references/` 保持一致：

| 原型中的呈现 | 对应资源 |
|---|---|
| A–F 维度菜单 | [references/review-dimension-confirmation.md](../references/review-dimension-confirmation.md) |
| P0–P2 分级与问题卡 | [SKILL.md](../SKILL.md) |
| `COPY-` 修改清单 | [references/markdown-change-list.md](../references/markdown-change-list.md) |
| `UC-` 未涉及规范场景（勾选 E 才输出） | [references/uncovered-copy-scenarios.md](../references/uncovered-copy-scenarios.md) |
| 规则库中的 `HF-` / `SPT-` 条目 | [references/high-frequency-copy-rules.md](../references/high-frequency-copy-rules.md)、[references/system-prompt-patterns.md](../references/system-prompt-patterns.md) |

示例数据集中在 `src/data/`，规则编号与文案改法均取自上述规则文件；调整示例时请同步核对编号是否仍然存在。

## 目录结构

```text
prototype/
├── src/
│   ├── App.tsx                  # 阶段切换、抽屉与全局提示挂载
│   ├── state/useReview.ts       # 全部状态、动作与派生值
│   ├── data/                    # 示例问题、规则、维度与速答判定
│   ├── components/              # 每个界面／每栏一个组件
│   ├── ui/Button.tsx            # 设计系统按钮
│   └── styles/                  # tokens/ 为设计系统原样拷贝
└── public/assets/               # logo 与首页插图
```

## 技术栈

React 19 + TypeScript + Vite。`src/styles/tokens/` 由设计系统导出后原样拷贝，请勿在此目录内直接修改；如需更新，重新拷贝一次。
