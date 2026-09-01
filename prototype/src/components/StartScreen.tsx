import { Button } from '../ui/Button'
import { DimensionRows } from './DimensionRows'
import type { Actions, Derived } from '../state/useReview'

interface Props {
  files: string[]
  tab: 'file' | 'text'
  text: string
  dims: string[]
  actions: Actions
  derived: Derived
}

/** 首页: hero, screenshot/copy input, and the collapsed 审查项 configurator. */
export function StartScreen({ files, tab, text, dims, actions, derived }: Props) {
  return (
    <div className="start">
      <div className="start__inner">
        <div className="hero">
          <div className="hero__art">
            <div className="hero__glow" />
            <img src="/assets/reviewer-illustration.png" alt="设计师正在审查界面文案" />
          </div>
          <div className="hero__copy">
            <div className="hero__eyebrow">
              <span />
              <span>SOMETHING&apos;S IN REVIEW</span>
            </div>
            <div className="hero__title">She&apos;s reviewing something...</div>
            <div className="hero__sub">
              支持截图、原型链接、录屏、文案清单或需求文档。只基于可见文字下结论，不猜测未提供的内容。
            </div>
          </div>
        </div>

        <div className="input-card">
          <div className="input-card__tabs">
            <span
              className={tab !== 'text' ? 'chip is-on' : 'chip'}
              role="button"
              tabIndex={0}
              onClick={() => actions.setTab('file')}
              onKeyDown={(e) => e.key === 'Enter' && actions.setTab('file')}
            >
              拖入图片
            </span>
            <span
              className={tab === 'text' ? 'chip is-on' : 'chip'}
              role="button"
              tabIndex={0}
              onClick={() => actions.setTab('text')}
              onKeyDown={(e) => e.key === 'Enter' && actions.setTab('text')}
            >
              直接输入文案
            </span>
          </div>

          {tab !== 'text' ? (
            <div className="input-card__body">
              <div
                className="dropzone"
                role="button"
                tabIndex={0}
                onClick={actions.addFile}
                onKeyDown={(e) => e.key === 'Enter' && actions.addFile()}
              >
                <div className="dropzone__text">
                  <div className="dropzone__title">拖入截图，或粘贴原型链接</div>
                  <div className="dropzone__formats">PNG · JPG</div>
                </div>
                <span className="dropzone__action">
                  <Button
                    variant="secondary"
                    size="sm"
                    onClick={(e) => {
                      e.stopPropagation()
                      actions.addFile()
                    }}
                  >
                    选择文件
                  </Button>
                </span>
              </div>

              {files.length > 0 && (
                <>
                  <div className="file-chips">
                    {files.map((name, i) => (
                      <div className="file-chip" key={`${name}-${i}`}>
                        <span className="file-chip__thumb" />
                        <span className="file-chip__name">{name}</span>
                        <button
                          className="file-chip__remove"
                          aria-label={`移除 ${name}`}
                          onClick={() => actions.removeFile(i)}
                        >
                          ×
                        </button>
                      </div>
                    ))}
                  </div>
                  <div className="submit-row">
                    <span className="submit-row__hint">{derived.fileHint}</span>
                    <span className="submit-row__action">
                      <Button variant="primary" size="sm" onClick={actions.goReview}>
                        开始审查
                      </Button>
                    </span>
                  </div>
                </>
              )}
            </div>
          ) : (
            <div className="input-card__body input-card__body--text">
              <textarea
                className="copy-input"
                value={text}
                onChange={(e) => actions.setText(e.target.value)}
                placeholder={'粘贴界面文案，一行一条。例如：\n导入失败\n确定删除？'}
              />
              <div className="submit-row">
                <span className="submit-row__hint">{derived.textHint}</span>
                <span className="submit-row__action">
                  <Button variant="primary" size="sm" onClick={actions.submitText}>
                    {derived.textCta}
                  </Button>
                </span>
              </div>
              <div className="example-chips">
                <span
                  className="example-chip"
                  role="button"
                  tabIndex={0}
                  onClick={actions.fillExample}
                  onKeyDown={(e) => e.key === 'Enter' && actions.fillExample()}
                >
                  试一个示例
                </span>
              </div>
            </div>
          )}
        </div>

        <div className="dim-fold">
          <button className="dim-fold__head" onClick={actions.toggleDimEdit}>
            <span className="dim-fold__label">审查项</span>
            <span className="dim-fold__badge">{derived.dimLabel}</span>
            <span className="dim-fold__hint">{derived.dimEditHint}</span>
            <span className="dim-fold__toggle">{derived.dimToggleLabel}</span>
          </button>
          {derived.dimEditOpen && (
            <div className="dim-fold__body">
              <DimensionRows
                dimensions={derived.dimensions}
                selected={dims}
                onToggle={actions.toggleDim}
              />
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
