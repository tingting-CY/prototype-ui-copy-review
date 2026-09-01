import type { CSSProperties } from 'react'
import { ISSUES, TONE } from '../data/review'
import type { Issue } from '../data/types'
import type { Actions, CanvasFile, Derived } from '../state/useReview'

interface PinProps {
  n: number
  top: number
  sel: number
  visible: (d: Issue) => boolean
  onSelect: (n: number) => void
}

/** One numbered annotation hanging in the gutter beside the reviewed element. */
function Pin({ n, top, sel, visible, onSelect }: PinProps) {
  const issue = ISSUES[n - 1]
  const shown = visible(issue)
  const cls = ['pin', sel === n ? 'is-on' : '', shown ? '' : 'is-muted'].filter(Boolean).join(' ')

  return (
    <button
      className={cls}
      style={{ top, '--tone': TONE[issue.tone].c } as CSSProperties}
      aria-label={`标注 ${n}：${issue.tag}`}
      aria-hidden={!shown}
      onClick={() => onSelect(n)}
    >
      {n}
    </button>
  )
}

interface Props {
  file: CanvasFile
  sel: number
  actions: Actions
  derived: Derived
}

/** Column 2 of the workspace: the reviewed screen with its annotation pins. */
export function CanvasPanel({ file, sel, actions, derived }: Props) {
  const pin = (n: number, top: number) => (
    <Pin n={n} top={top} sel={sel} visible={derived.visible} onSelect={actions.select} />
  )

  return (
    <div className="canvas">
      <div className="canvas__bar">
        <div
          className={file === 'import' ? 'tab is-on' : 'tab'}
          role="button"
          tabIndex={0}
          onClick={() => actions.pickFile('import')}
          onKeyDown={(e) => e.key === 'Enter' && actions.pickFile('import')}
        >
          模型导入.png
        </div>
        <div
          className={file === 'member' ? 'tab is-on' : 'tab'}
          role="button"
          tabIndex={0}
          onClick={() => actions.pickFile('member')}
          onKeyDown={(e) => e.key === 'Enter' && actions.pickFile('member')}
        >
          成员管理.png
        </div>
        <div className="canvas__count">{derived.pinCountLabel}</div>
      </div>

      <div className="canvas__stage">
        <div className="shot">
          <div className="shot__chrome">模型管理 / 模型导入</div>
          <div className="shot__body">
            <div className="shot__title">模型导入</div>

            <div className="shot__field">
              {pin(4, 16)}
              <div className="shot__label">服务地址</div>
              <div className="shot__control shot__control--placeholder">请输入</div>
            </div>

            <div className="shot__field">
              {pin(5, 16)}
              <div className="shot__label">版本构建数</div>
              <div className="shot__control">12</div>
            </div>

            <div className="shot__field">
              {pin(3, 16)}
              <div className="shot__label">任务状态</div>
              <div className="shot__states">
                <span className="shot__state">处理中</span>
                <span className="shot__state">执行中</span>
                <span className="shot__state">解析中</span>
              </div>
            </div>

            <div className="shot__alert">
              {pin(2, 9)}
              <span className="shot__alert-dot" />
              <span className="shot__alert-text">导入失败</span>
            </div>

            <div className="shot__dialog">
              {pin(1, 20)}
              <div className="shot__dialog-title">确定删除？</div>
              <div className="shot__dialog-actions">
                <span className="shot__btn-ghost">取消</span>
                <span className="shot__btn-primary">确定</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
