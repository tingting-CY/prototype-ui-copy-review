import { useReview } from './state/useReview'
import { TopBar } from './components/TopBar'
import { StartScreen } from './components/StartScreen'
import { DimensionScreen } from './components/DimensionScreen'
import { QuickScreen } from './components/QuickScreen'
import { ChatPanel } from './components/ChatPanel'
import { CanvasPanel } from './components/CanvasPanel'
import { IssueList } from './components/IssueList'
import { WorkspaceDrawer } from './components/WorkspaceDrawer'
import { CheckIcon } from './components/icons'

export default function App() {
  const { s, actions, derived } = useReview()

  return (
    <div className="app">
      <TopBar dims={s.dims} actions={actions} derived={derived} />

      {s.stage === 'start' && (
        <StartScreen
          files={s.files}
          tab={s.tab}
          text={s.text}
          dims={s.dims}
          actions={actions}
          derived={derived}
        />
      )}

      {s.stage === 'dim' && <DimensionScreen dims={s.dims} actions={actions} derived={derived} />}

      {s.stage === 'quick' && (
        <QuickScreen text={s.text} follow={s.follow} actions={actions} derived={derived} />
      )}

      {s.stage === 'review' && (
        <div className="review">
          <ChatPanel
            pending={s.pending}
            exported={s.exported}
            actions={actions}
            derived={derived}
          />
          <CanvasPanel file={s.file} sel={s.sel} actions={actions} derived={derived} />
          <IssueList
            sel={s.sel}
            filter={s.filter}
            legendOpen={s.legend}
            copied={s.copied}
            actions={actions}
            derived={derived}
          />
        </div>
      )}

      {s.toast && (
        <div className="toast" role="status">
          <CheckIcon />
          {s.toast}
        </div>
      )}

      {s.rules && (
        <WorkspaceDrawer
          panel={s.panel}
          ruleSrc={s.ruleSrc}
          ruleFocus={s.ruleFocus}
          actions={actions}
          derived={derived}
        />
      )}
    </div>
  )
}
