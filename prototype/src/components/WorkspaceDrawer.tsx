import type { Actions, Derived, DrawerPanel, RuleSource } from '../state/useReview'

/** Past reviews shown in 历史审查; the first is the session in progress. */
const HISTORY = [
  {
    name: '模型管理 · 导入与成员流程',
    when: '当前 · 今天 14:20',
    current: true,
    badges: [
      { label: 'P0 1', kind: 'p0' },
      { label: 'P1 2', kind: 'p1' },
      { label: 'P2 1', kind: 'p2' },
      { label: 'UC 1', kind: 'uc' },
    ],
    meta: 'A + B + F · 2 张截图',
  },
  {
    name: '任务中心 · 空状态与错误提示',
    when: '8 月 28 日',
    current: false,
    badges: [
      { label: 'P1 3', kind: 'p1' },
      { label: 'UC 2', kind: 'uc' },
    ],
    meta: 'A + B + E + F · 6 张截图 · 清单已导出',
  },
  {
    name: '单条速答 · 操作失败提示',
    when: '8 月 27 日',
    current: false,
    badges: [{ label: '速答', kind: 'quick' }],
    meta: '',
  },
] as const

const RULE_TABS: { src: RuleSource; label: string }[] = [
  { src: 'all', label: '全部' },
  { src: 'HF', label: 'HF- 通用高频' },
  { src: 'SPT', label: 'SPT- 提示句型' },
]

interface Props {
  panel: DrawerPanel
  ruleSrc: RuleSource
  ruleFocus: string[]
  actions: Actions
  derived: Derived
}

export function WorkspaceDrawer({ panel, ruleSrc, ruleFocus, actions, derived }: Props) {
  return (
    <div className="drawer">
      <button className="drawer__scrim" aria-label="关闭" onClick={actions.closeDrawer} />
      <div className="drawer__sheet">
        <div className="drawer__nav">
          <div className="drawer__nav-label">工作区</div>
          <button
            className={panel === 'history' ? 'drawer__nav-item is-on' : 'drawer__nav-item'}
            onClick={() => actions.showPanel('history')}
          >
            历史审查
          </button>
          <button
            className={panel !== 'history' ? 'drawer__nav-item is-on' : 'drawer__nav-item'}
            onClick={() => actions.showPanel('rules')}
          >
            规则库
          </button>
          <div className="drawer__nav-note">规范待维护项 3 条，来自近 30 天的重复问题。</div>
        </div>

        <div className="drawer__content">
          {panel === 'history' ? (
            <>
              <div className="drawer__head">
                <span className="drawer__title">历史审查</span>
                <span className="drawer__meta">近 30 天 3 次</span>
                <button className="drawer__close" aria-label="关闭" onClick={actions.closeDrawer}>
                  ×
                </button>
              </div>
              <div className="drawer__body">
                {HISTORY.map((h) => (
                  <div
                    className={h.current ? 'history-card is-current' : 'history-card'}
                    key={h.name}
                  >
                    <div className="history-card__head">
                      <span className="history-card__name">{h.name}</span>
                      <span className="history-card__when">{h.when}</span>
                    </div>
                    <div className="history-card__badges">
                      {h.badges.map((b) => (
                        <span
                          className={`history-card__badge history-card__badge--${b.kind}`}
                          key={b.label}
                        >
                          {b.label}
                        </span>
                      ))}
                    </div>
                    {h.meta && <div className="history-card__meta">{h.meta}</div>}
                  </div>
                ))}
              </div>
            </>
          ) : (
            <>
              <div className="drawer__head">
                <span className="drawer__title">规则库</span>
                <span className="drawer__meta">{derived.ruleScopeLabel}</span>
                <button className="drawer__close" aria-label="关闭" onClick={actions.closeDrawer}>
                  ×
                </button>
              </div>

              <div className="drawer__tabs">
                {RULE_TABS.map((t) => {
                  /* 全部 loses its active state while a single issue's rules are isolated. */
                  const on =
                    t.src === 'all'
                      ? ruleSrc === 'all' && ruleFocus.length === 0
                      : ruleSrc === t.src
                  return (
                    <span
                      className={on ? 'chip is-on' : 'chip'}
                      role="button"
                      tabIndex={0}
                      key={t.src}
                      onClick={() => actions.setRuleSrc(t.src)}
                      onKeyDown={(e) => e.key === 'Enter' && actions.setRuleSrc(t.src)}
                    >
                      {t.label}
                    </span>
                  )
                })}
              </div>

              <div className="drawer__body">
                {derived.ruleList.map((r) => (
                  <div
                    className={
                      ruleFocus.includes(r.code) ? 'rule-card is-focused' : 'rule-card'
                    }
                    key={r.code}
                  >
                    <div className="rule-card__head">
                      <span className="rule-card__code">{r.code}</span>
                      <span className="rule-card__title">{r.title}</span>
                      <span className="rule-card__hits">命中 {r.hit}</span>
                    </div>
                    <div className="rule-card__desc">{r.desc}</div>
                  </div>
                ))}
              </div>

              <div className="drawer__foot">SPT- 为部分提炼来源，仅在已核验范围内使用。</div>
            </>
          )}
        </div>
      </div>
    </div>
  )
}
