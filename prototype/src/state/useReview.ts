import { useCallback, useEffect, useMemo, useRef, useState } from 'react'
import { DIMENSIONS, FILE_POOL, ISSUES, RULES } from '../data/review'
import { quickAnswers, toLines } from '../data/quickAnswers'
import type { Issue } from '../data/types'

export type Stage = 'start' | 'dim' | 'quick' | 'review'
export type InputTab = 'file' | 'text'
export type Filter = 'all' | 'p01'
export type CanvasFile = 'import' | 'member'
export type DrawerPanel = 'rules' | 'history'
export type RuleSource = 'all' | 'HF' | 'SPT'

interface ReviewState {
  stage: Stage
  /** Home-screen input mode: drop screenshots or paste copy. */
  tab: InputTab
  /** Contents of the home-screen textarea; also the 速答 transcript. */
  text: string
  /** Contents of the 速答 follow-up field. */
  follow: string
  /** Screenshots queued on the home screen. */
  files: string[]
  /** Screenshots attached to the composer but not yet sent. */
  pending: string[]
  /** Selected review dimensions, A–F. */
  dims: string[]
  /** Whether the dimension editor is open (inline on home, popover elsewhere). */
  dimEdit: boolean
  /** Currently selected issue number. */
  sel: number
  filter: Filter
  /** Which screenshot tab is active on the canvas. */
  file: CanvasFile
  /** Whether the Markdown change list has been generated. */
  exported: boolean
  /** Issue whose copy button is briefly highlighted. */
  copied: number | null
  toast: string
  /** Whether the P0–P2 legend is expanded. */
  legend: boolean
  /** Whether the workspace drawer is open. */
  rules: boolean
  panel: DrawerPanel
  ruleSrc: RuleSource
  /** Rule codes to isolate and highlight, set by 查看规则 on an issue. */
  ruleFocus: string[]
}

const INITIAL: ReviewState = {
  stage: 'start',
  tab: 'file',
  text: '',
  follow: '',
  files: ['模型导入.png', '成员管理.png'],
  pending: [],
  dims: ['A', 'B', 'F'],
  dimEdit: false,
  sel: 1,
  filter: 'all',
  file: 'import',
  exported: false,
  copied: null,
  toast: '',
  legend: false,
  rules: false,
  panel: 'rules',
  ruleSrc: 'all',
  ruleFocus: [],
}

const TOAST_MS = 1800

export function useReview() {
  const [s, setS] = useState<ReviewState>(INITIAL)
  const toastTimer = useRef<ReturnType<typeof setTimeout> | null>(null)

  const patch = useCallback((next: Partial<ReviewState>) => {
    setS((prev) => ({ ...prev, ...next }))
  }, [])

  useEffect(() => () => {
    if (toastTimer.current) clearTimeout(toastTimer.current)
  }, [])

  const lines = useMemo(() => toLines(s.text), [s.text])

  /** UC- findings only exist when dimension E is selected. */
  const inScope = useCallback(
    (d: Issue) => d.tone !== 'violet' || s.dims.includes('E'),
    [s.dims],
  )
  const visible = useCallback(
    (d: Issue) =>
      inScope(d) && (s.filter === 'all' || d.tag.startsWith('P0') || d.tag.startsWith('P1')),
    [inScope, s.filter],
  )

  const scoped = useMemo(() => ISSUES.filter(inScope), [inScope])
  const list = useMemo(() => ISSUES.filter(visible), [visible])

  const actions = useMemo(
    () => ({
      /* --- navigation --- */
      goHome: () => patch({ stage: 'start', dimEdit: false, rules: false, legend: false }),
      goReview: () => patch({ stage: 'review' }),

      /* --- home screen --- */
      setTab: (tab: InputTab) => patch({ tab }),
      setText: (text: string) => patch({ text }),
      addFile: () =>
        setS((p) => ({ ...p, files: p.files.concat([FILE_POOL[p.files.length % FILE_POOL.length]]) })),
      removeFile: (i: number) =>
        setS((p) => ({ ...p, files: p.files.filter((_, j) => j !== i) })),
      fillExample: () => patch({ tab: 'text', text: '操作失败\n确定删除？\n任务保存失败' }),
      /** 1–5 lines go to 速答; more than 5 escalate to the full review. */
      submitText: () => patch({ stage: lines.length > 0 && lines.length <= 5 ? 'quick' : 'dim' }),

      /* --- 速答 follow-up --- */
      setFollow: (follow: string) => patch({ follow }),
      submitFollow: () =>
        setS((p) => {
          const t = p.follow.trim()
          if (!t) return p
          return { ...p, text: (p.text ? p.text + '\n' : '') + t, follow: '' }
        }),

      /* --- dimensions --- */
      toggleDim: (k: string) =>
        setS((p) => ({
          ...p,
          dims: p.dims.includes(k) ? p.dims.filter((x) => x !== k) : p.dims.concat([k]).sort(),
        })),
      toggleDimEdit: () => setS((p) => ({ ...p, dimEdit: !p.dimEdit })),
      rerun: () => patch({ dimEdit: false, exported: false, sel: 1, filter: 'all' }),

      /* --- review workspace --- */
      select: (n: number) => patch({ sel: n }),
      onlyP01: () => patch({ filter: 'p01', sel: 1 }),
      showAll: () => patch({ filter: 'all' }),
      pickFile: (file: CanvasFile) => patch({ file }),
      exportList: () => patch({ exported: true }),
      toggleLegend: () => setS((p) => ({ ...p, legend: !p.legend })),
      attach: () =>
        setS((p) => ({
          ...p,
          pending: p.pending.concat([FILE_POOL[(p.files.length + p.pending.length) % FILE_POOL.length]]),
        })),
      removePending: (i: number) =>
        setS((p) => ({ ...p, pending: p.pending.filter((_, j) => j !== i) })),

      copyFix: (issue: Issue) => {
        void navigator.clipboard?.writeText(issue.fix).catch(() => {})
        patch({ copied: issue.n, toast: '已复制修改后文案' })
        if (toastTimer.current) clearTimeout(toastTimer.current)
        toastTimer.current = setTimeout(() => patch({ copied: null, toast: '' }), TOAST_MS)
      },

      /* --- workspace drawer --- */
      openRules: () => patch({ rules: true, panel: 'rules', ruleSrc: 'all', ruleFocus: [] }),
      openHistory: () => patch({ rules: true, panel: 'history' }),
      closeDrawer: () => patch({ rules: false, ruleFocus: [] }),
      showPanel: (panel: DrawerPanel) => patch({ panel }),
      setRuleSrc: (ruleSrc: RuleSource) => patch({ ruleSrc, ruleFocus: [] }),
      /** Open the drawer isolated to the rules an issue cites. */
      focusRules: (issue: Issue) =>
        patch({
          rules: true,
          panel: 'rules',
          ruleSrc: 'all',
          ruleFocus: issue.rules.split(' · ').filter((c) => RULES.some((r) => r.code === c)),
        }),
    }),
    [patch, lines.length],
  )

  const derived = useMemo(() => {
    const dimsLabel = s.dims.length ? s.dims.join(' + ') : ''
    return {
      lines: lines.length,
      list,
      visible,

      /* home screen */
      fileHint: `${s.files.length} 张截图 · 两张以上会同时检查跨页面一致性`,
      textHint:
        lines.length > 5
          ? '超过 5 条，将按完整审查流程处理'
          : lines.length > 0
            ? `${lines.length} 条文案 · 走单条速答模式`
            : '一至五条走速答，超过五条进入完整审查',
      textCta: lines.length > 5 ? '开始完整审查' : '让我判断',

      /* dimensions */
      dimLabel: dimsLabel || '未选维度',
      dimCta: `按 ${dimsLabel || '推荐'} 开始`,
      dimEditHint: s.dims.includes('E')
        ? '已包含 E，将输出 UC- 未覆盖场景'
        : '未选 E，不输出 UC- 章节',
      dimToggleLabel: s.dimEdit ? '收起' : '调整',
      dimEditOpen: s.dimEdit && s.stage === 'start',
      dimPanelOpen: s.dimEdit && s.stage !== 'start',
      dimensions: DIMENSIONS,

      /* review workspace */
      pinCountLabel: `${list.length} 处标注`,
      summaryLine: `已按 ${dimsLabel || '推荐维度'} 审查 ${s.files.length} 张截图，共 ${scoped.length} 项。点右侧标注或清单条目可以逐条查看。`,
      statP0: scoped.filter((d) => d.tone === 'danger').length,
      statP1: scoped.filter((d) => d.tag.startsWith('P1')).length,
      statP2: scoped.filter((d) => d.tag.startsWith('P2')).length,
      statUC: scoped.filter((d) => d.tone === 'violet').length,
      composerHint: s.pending.length
        ? '补充说明后发送，我会把新截图并入本次审查'
        : '继续提问，或粘贴一条文案让我判断',

      /* 速答 */
      quickIntro: `这 ${lines.length} 条按单条速答处理，只看当前可见文本可判定的问题。`,
      answers: quickAnswers(s.text),

      /* 规则库 */
      ruleScopeLabel: s.ruleFocus.length ? `本条依据 ${s.ruleFocus.length} 项` : `${RULES.length} 项`,
      ruleList: RULES.filter((r) =>
        s.ruleFocus.length
          ? s.ruleFocus.includes(r.code)
          : s.ruleSrc === 'all' || r.code.startsWith(s.ruleSrc),
      ),
    }
  }, [s, lines, list, scoped, visible])

  return { s, actions, derived }
}

export type ReviewApi = ReturnType<typeof useReview>
export type Actions = ReviewApi['actions']
export type Derived = ReviewApi['derived']
