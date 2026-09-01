import { Button } from '../ui/Button'
import { DimensionRows } from './DimensionRows'
import type { Actions, Derived } from '../state/useReview'

interface Props {
  dims: string[]
  actions: Actions
  derived: Derived
}

export function TopBar({ dims, actions, derived }: Props) {
  return (
    <div className="topbar">
      <button className="topbar__logo" onClick={actions.goHome} title="返回首页">
        <img src="/assets/logo-computer.png" alt="" />
        <span className="topbar__wordmark">UI-COPY</span>
      </button>

      <span className="topbar__dims">
        <span
          className="dim-pill"
          role="button"
          tabIndex={0}
          title="重新选择审查项"
          onClick={actions.toggleDimEdit}
          onKeyDown={(e) => {
            if (e.key === 'Enter' || e.key === ' ') {
              e.preventDefault()
              actions.toggleDimEdit()
            }
          }}
        >
          {derived.dimLabel} <span className="dim-pill__caret">▾</span>
        </span>

        {derived.dimPanelOpen && (
          <div className="dim-popover">
            <div className="dim-popover__head">
              <span className="dim-popover__title">重新选择审查维度</span>
              <span className="dim-popover__hint">取消勾选的模块不再作判定</span>
            </div>
            <DimensionRows
              dimensions={derived.dimensions}
              selected={dims}
              onToggle={actions.toggleDim}
            />
            <div className="dim-popover__foot">
              <span>{derived.dimEditHint}</span>
              <span className="dim-popover__actions">
                <Button variant="ghost" size="sm" onClick={actions.toggleDimEdit}>
                  取消
                </Button>
                <Button variant="primary" size="sm" onClick={actions.rerun}>
                  重新审查
                </Button>
              </span>
            </div>
          </div>
        )}
      </span>

      <div className="topbar__actions">
        <Button variant="ghost" size="sm" onClick={actions.openHistory}>
          历史审查
        </Button>
        <Button variant="ghost" size="sm" onClick={actions.openRules}>
          规则库
        </Button>
      </div>
    </div>
  )
}
