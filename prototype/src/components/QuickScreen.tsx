import type { CSSProperties } from 'react'
import { Button } from '../ui/Button'
import type { Actions, Derived } from '../state/useReview'

interface Props {
  text: string
  follow: string
  actions: Actions
  derived: Derived
}

/** 单条速答: line-by-line verdicts, no P0–P3 grading and no change list. */
export function QuickScreen({ text, follow, actions, derived }: Props) {
  return (
    <div className="convo">
      <div className="convo__inner convo__inner--quick">
        <div className="quick__prompt">{text}</div>

        <div className="convo__row">
          <img className="avatar" src="/assets/logo-computer.png" alt="助手" />
          <div className="convo__stack">
            <div className="bubble-assistant">{derived.quickIntro}</div>

            {derived.answers.map((a, i) => (
              <div className="answer" key={i}>
                <div className="answer__head">
                  <span
                    className="answer__dot"
                    style={{ '--tone': a.tone } as CSSProperties}
                  />
                  <span className="answer__verdict">{a.verdict}</span>
                  <span className="answer__text">{a.text}</span>
                </div>
                <div className="answer__body">
                  <div className="answer__field">
                    <span className="answer__label">依据</span>
                    <span className="answer__value">{a.basis}</span>
                  </div>
                  <div className="answer__field">
                    <span className="answer__label">建议</span>
                    <span className="answer__value answer__value--strong">{a.advice}</span>
                  </div>
                </div>
              </div>
            ))}

            <div className="quick__note">
              速答模式不输出 P0–P3、COPY- 编号或修改清单。需要页面或流程一致性时，可升级为完整审查。
            </div>

            <div className="quick__follow">
              <input
                value={follow}
                onChange={(e) => actions.setFollow(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === 'Enter') {
                    e.preventDefault()
                    actions.submitFollow()
                  }
                }}
                placeholder="再贴一条文案，例如：导入失败"
              />
              <Button variant="primary" size="sm" onClick={actions.submitFollow}>
                继续判断
              </Button>
            </div>

            <div className="quick__note quick__note--fine">
              仅支持文案文本；截图与流程一致性不在速答范围内。
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
