import type { Dimension, Issue, Rule, Tone, ToneColors } from './types'

/**
 * The findings of the mocked review: two screenshots (模型导入 / 成员管理)
 * checked against dimensions A + B + F.
 */
export const ISSUES: Issue[] = [
  {
    n: 1,
    tag: 'P0 · COPY-001',
    loc: '成员管理 · 删除确认弹窗',
    tone: 'danger',
    orig: '确定删除？／按钮“确定”',
    fix: '删除成员“张三”后不可恢复。是否删除？／按钮“删除成员”',
    note: '高影响操作未说明对象与后果；泛化按钮无法预期结果。',
    rules: 'HF-CMP-09 · HF-STA-06',
    scope: '成员管理列表页、成员详情页的删除入口',
  },
  {
    n: 2,
    tag: 'P1 · COPY-002',
    loc: '模型导入 · 失败提示',
    tone: 'warning',
    orig: '导入失败',
    fix: '模型导入失败，剩余磁盘空间不足，请释放存储空间后再试。',
    note: '表现／影响 + 原因 + 修复方式，三段齐全。',
    rules: 'SPT-ACC-01 · SPT-PAT-01',
    scope: '模型导入流程',
  },
  {
    n: 3,
    tag: 'P1 · COPY-003',
    loc: '任务列表 · 状态列',
    tone: 'warning',
    orig: '处理中／执行中／解析中',
    fix: '统一为“执行中”',
    note: '同一状态存在三种写法，无产品标准。',
    rules: '建议统一',
    scope: '任务列表、任务详情、导入面板',
  },
  {
    n: 4,
    tag: 'P2 · COPY-004',
    loc: '模型导入 · 占位符',
    tone: 'info',
    orig: '请输入',
    fix: '请输入服务地址，例如 https://10.0.0.1:8443',
    note: '占位符未说明格式与示例。',
    rules: 'HF-FMT-03',
    scope: '当前页面',
  },
  {
    n: 5,
    tag: 'UC-001 · 未涉及规范',
    loc: '模型导入 · 版本构建数',
    tone: 'violet',
    orig: '版本构建数',
    fix: '待设计师确认统计口径后补充术语表',
    note: '业务语义未定义，不给出直接改写。',
    rules: '无适用规则',
    scope: '模型导入、任务中心',
  },
]

/** 规则库 contents: HF- general high-frequency rules and SPT- prompt patterns. */
export const RULES: Rule[] = [
  {
    code: 'HF-CMP-09',
    title: '按钮应写明具体动作',
    hit: 1,
    desc: '泛化按钮词无法让用户预期结果；改为“删除成员”“保存并部署”等动宾结构。',
  },
  {
    code: 'HF-STA-06',
    title: '高影响操作须说明对象与后果',
    hit: 1,
    desc: '不可逆操作的确认文案需包含对象名称与后果。',
  },
  {
    code: 'HF-FMT-03',
    title: '占位符应给出格式或示例',
    hit: 1,
    desc: '仅写“请输入”无法说明期望格式；补充对象与示例值。',
  },
  {
    code: 'SPT-ACC-01',
    title: '错误信息三要素',
    hit: 1,
    desc: '错误信息应覆盖用户可见的表现／影响、错误原因，以及可执行的修复方式。',
  },
  {
    code: 'SPT-PAT-01',
    title: '结果性提示应含操作与对象',
    hit: 1,
    desc: '结果应包含实际操作或对象，避免仅写“操作成功／失败”。',
  },
  {
    code: 'SPT-PAT-02',
    title: '泛化结果句型的使用边界',
    hit: 0,
    desc: '仅在对象、动作或原因无法进一步明确时使用“操作失败。”。',
  },
  {
    code: 'SPT-PUN-02',
    title: '对话框主题句结尾不加句号',
    hit: 0,
    desc: '句末为名称、代码、路径或链接时同样不加句号。',
  },
]

/** The A–F review dimensions offered on the home screen and in the top bar. */
export const DIMENSIONS: Dimension[] = [
  { key: 'A', name: '基础文案与页面一致性', desc: '标题、字段、按钮、占位符、术语、格式与状态。' },
  { key: 'B', name: '状态与提示信息', desc: '成功、失败、进度、空状态、风险与修复指引。' },
  { key: 'C', name: '设计系统与品牌规范', desc: '需先确认设计系统名称或规范链接，否则不加载 PX- 规则。' },
  { key: 'D', name: '跨页面／流程一致性', desc: '多页面、多个状态或完整流程时使用。' },
  { key: 'E', name: '规范缺口与治理建议', desc: '识别后续需要补充的规范场景。' },
  { key: 'F', name: 'Markdown 修改清单', desc: '输出可直接交付团队的修改清单。' },
]

/** Filenames handed out, in order, as the user keeps adding screenshots. */
export const FILE_POOL = [
  '模型导入.png',
  '成员管理.png',
  '任务列表.png',
  '空状态.png',
  '导入失败.png',
]

export const TONE: Record<Tone, ToneColors> = {
  danger: { c: '#DC4634', bg: 'var(--danger-50)', fg: 'var(--danger-600)' },
  warning: { c: '#D9921A', bg: 'var(--warning-50)', fg: 'var(--warning-600)' },
  info: { c: '#D9921A', bg: 'var(--info-50)', fg: 'var(--info-500)' },
  violet: { c: '#6A52E3', bg: 'var(--violet-50)', fg: 'var(--violet-700)' },
}
