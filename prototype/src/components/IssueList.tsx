import type { CSSProperties } from 'react'
import { TONE } from '../data/review'
import type { Issue } from '../data/types'
import { Button } from '../ui/Button'
import { CopyIcon, InfoIcon } from './icons'
import type { Actions, Derived, Filter } from '../state/useReview'

const LEGEND = [
  { tone: 'var(--danger-500)', text: 'P0 必须修改：阻碍理解、误导或隐藏高影响后果' },
  { tone: 'var(--warning-500)', text: 'P1 强建议修改：不符规范或同一语义写法不一致' },
  { tone: 'var(--info-500)', text: 'P2 可优化：不影响理解，表达可更清楚' },
  { tone: 'var(--violet-500)', text: 'UC 未涵盖规范场景：不代表当前文案错误' },
]

interface Props {
  sel: number
  filter: Filter
  legendOpen: boolean
  copied: number | null
  actions: Actions
  derived: Derived
}

/** Column 3 of the workspace: the 问题清单 and its export action. */
export function IssueList({ sel, filter, legendOpen, copied, actions, derived }: Props) {
  return (
    <div className="issues">
      <div className="issues__head">
        <span className="issues__title">问题清单</span>
        <button
          className={legendOpen ? 'issues__legend-btn is-on' : 'issues__legend-btn'}
          title="查看 P0–P2 含义"
          aria-expanded={legendOpen}
          onClick={actions.toggleLegend}
        >
          <InfoIcon />
        </button>
        <span className="issues__filters">
          <span
            className={filter === 'all' ? 'chip is-on' : 'chip'}
            role="button"
            tabIndex={0}
            onClick={actions.showAll}
            onKeyDown={(e) => e.key === 'Enter' && actions.showAll()}
          >
            全部
          </span>
          <span
            className={filter === 'p01' ? 'chip is-on' : 'chip'}
            role="button"
            tabIndex={0}
            onClick={actions.onlyP01}
            onKeyDown={(e) => e.key === 'Enter' && actions.onlyP01()}
          >
            仅 P0/P1
          </span>
        </span>
      </div>

      {legendOpen && (
        <div className="legend">
          {LEGEND.map((l) => (
            <span className="legend__item" key={l.text}>
              <span className="legend__dot" style={{ '--tone': l.tone } as CSSProperties} />
              {l.text}
            </span>
          ))}
        </div>
      )}

      <div className="issues__body">
        {derived.list.map((it) => (
          <IssueCard
            key={it.n}
            issue={it}
            open={sel === it.n}
            copied={copied === it.n}
            actions={actions}
          />
        ))}
      </div>

      <div className="issues__foot">
        <Button variant="primary" size="sm" block onClick={actions.exportList}>
          生成修改清单
        </Button>
      </div>
    </div>
  )
}

interface CardProps {
  issue: Issue
  open: boolean
  copied: boolean
  actions: Actions
}

function IssueCard({ issue, open, copied, actions }: CardProps) {
  const t = TONE[issue.tone]
  const toneVars = { '--tone': t.c, '--tone-soft': t.bg, '--tone-fg': t.fg } as CSSProperties

  return (
    <div
      className={open ? 'issue is-on' : 'issue'}
      style={toneVars}
      role="button"
      tabIndex={0}
      aria-expanded={open}
      onClick={() => actions.select(issue.n)}
      onKeyDown={(e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault()
          actions.select(issue.n)
        }
      }}
    >
      <div className="issue__head">
        <span className="issue__n">{issue.n}</span>
        <span className="issue__tag">{issue.tag}</span>
        <span className="issue__loc">{issue.loc}</span>
      </div>

      {open ? (
        <div className="issue__detail">
          <div className="issue__crop">
            <div className="issue__crop-copy">{issue.orig}</div>
            <div className="issue__crop-caption">截图片段</div>
          </div>

          <div className="issue__fields">
            <div className="issue__field">
              <span className="issue__field-label">原文</span>
              <span className="issue__orig">{issue.orig}</span>
            </div>

            <div className="issue__field issue__field--fix">
              {/* UC- items are evaluated, not rewritten. */}
              <span className="issue__field-label">
                {issue.tone === 'violet' ? '评估' : '改为'}
              </span>
              <span className="issue__fix">{issue.fix}</span>
              <button
                className={copied ? 'issue__copy is-copied' : 'issue__copy'}
                title="复制修改后文案"
                onClick={(e) => {
                  e.stopPropagation()
                  actions.copyFix(issue)
                }}
              >
                <CopyIcon />
              </button>
            </div>

            <div className="issue__note">{issue.note}</div>

            <div className="issue__rules">
              <button
                className="issue__rule-code"
                onClick={(e) => {
                  e.stopPropagation()
                  actions.focusRules(issue)
                }}
              >
                {issue.rules}
              </button>
              <button
                className="issue__rule-link"
                onClick={(e) => {
                  e.stopPropagation()
                  actions.focusRules(issue)
                }}
              >
                查看规则
              </button>
            </div>

            <div className="issue__scope">影响范围：{issue.scope}</div>
          </div>
        </div>
      ) : (
        <div className="issue__summary">
          {issue.orig} → {issue.fix}
        </div>
      )}
    </div>
  )
}
