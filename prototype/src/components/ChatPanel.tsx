import { Button } from '../ui/Button'
import type { Actions, Derived } from '../state/useReview'

interface Props {
  pending: string[]
  exported: boolean
  actions: Actions
  derived: Derived
}

/** Column 1 of the workspace: the conversation and the composer. */
export function ChatPanel({ pending, exported, actions, derived }: Props) {
  return (
    <div className="chat">
      <div className="chat__scroll">
        <div className="bubble-user chat__ask">A、B、F，跳过 C</div>

        <div className="chat__row">
          <img className="chat__avatar--lead" src="/assets/logo-computer.png" alt="助手" />
          <div className="chat__stack">
            <div className="bubble-assistant">{derived.summaryLine}</div>

            <div className="stats">
              <div className="stats__cell">
                <div className="stats__value stats__value--p0">{derived.statP0}</div>
                <div className="stats__label">P0 必改</div>
              </div>
              <div className="stats__cell">
                <div className="stats__value stats__value--p1">{derived.statP1}</div>
                <div className="stats__label">P1 强建议</div>
              </div>
              <div className="stats__cell">
                <div className="stats__value stats__value--p2">{derived.statP2}</div>
                <div className="stats__label">P2 可优化</div>
              </div>
              <div className="stats__cell">
                <div className="stats__value stats__value--uc">{derived.statUC}</div>
                <div className="stats__label">未覆盖</div>
              </div>
            </div>

            <div className="chat__quick-actions">
              <Button variant="secondary" size="sm" onClick={actions.onlyP01}>
                只要 P0/P1
              </Button>
              <Button variant="secondary" size="sm" onClick={actions.showAll}>
                全部显示
              </Button>
            </div>
          </div>
        </div>

        {exported && (
          <div className="chat__row">
            <img className="avatar" src="/assets/logo-computer.png" alt="助手" />
            <div className="export-card">
              <div className="export-card__text">
                已生成 llm-config-copy-change-list.md：必须修改 3 项、待确认 1 项，默认不含 P3。
              </div>
              <div className="export-card__file">
                <span className="export-card__name">llm-config-copy-change-list.md</span>
                <span className="export-card__download">下载</span>
              </div>
            </div>
          </div>
        )}
      </div>

      <div className="composer">
        {pending.length > 0 && (
          <div className="composer__pending">
            {pending.map((name, i) => (
              <div className="pending-chip" key={`${name}-${i}`}>
                <span className="pending-chip__thumb" />
                <span className="pending-chip__name">{name}</span>
                <button
                  className="pending-chip__remove"
                  aria-label={`移除 ${name}`}
                  onClick={() => actions.removePending(i)}
                >
                  ×
                </button>
              </div>
            ))}
          </div>
        )}

        <div className="composer__field">
          <button className="composer__attach" title="继续添加图片" onClick={actions.attach}>
            ＋
          </button>
          <span className="composer__hint">{derived.composerHint}</span>
          <span className="composer__send" />
        </div>
      </div>
    </div>
  )
}
