import { Button } from '../ui/Button'
import { DimensionRows } from './DimensionRows'
import type { Actions, Derived } from '../state/useReview'

interface Props {
  dims: string[]
  actions: Actions
  derived: Derived
}

/** 维度确认: the assistant proposes A + B + F before the review starts. */
export function DimensionScreen({ dims, actions, derived }: Props) {
  return (
    <div className="convo">
      <div className="convo__inner convo__inner--dim">
        <div className="dim-screen__ask">
          <div className="bubble-user">帮我看看这两张原型截图的文案。</div>
          <div className="dim-screen__files">
            <div className="dim-screen__file">模型导入.png</div>
            <div className="dim-screen__file">成员管理.png</div>
          </div>
        </div>

        <div className="convo__row">
          <img className="avatar" src="/assets/logo-computer.png" alt="助手" />
          <div className="bubble-assistant">
            材料里能看到失败提示和状态词，建议先选 <b>A + B + F</b>。也可以回复“完整审查”。
          </div>
        </div>

        <div className="dim-screen__card">
          <DimensionRows
            dimensions={derived.dimensions}
            selected={dims}
            onToggle={actions.toggleDim}
            size="lg"
          />
        </div>

        <div className="dim-screen__actions">
          <Button variant="primary" size="sm" onClick={actions.goReview}>
            {derived.dimCta}
          </Button>
          <Button variant="ghost" size="sm" onClick={actions.goReview}>
            完整审查
          </Button>
        </div>
      </div>
    </div>
  )
}
