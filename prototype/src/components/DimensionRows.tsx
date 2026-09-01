import type { Dimension } from '../data/types'

interface Props {
  dimensions: Dimension[]
  selected: string[]
  onToggle: (key: string) => void
  /** 维度确认 renders the rows one step larger than the compact pickers. */
  size?: 'sm' | 'lg'
}

/** The A–F checklist, shared by the home fold, the top-bar popover and 维度确认. */
export function DimensionRows({ dimensions, selected, onToggle, size = 'sm' }: Props) {
  return (
    <div className={size === 'lg' ? 'dim-rows dim-rows--lg' : 'dim-rows'}>
      {dimensions.map((d) => {
        const on = selected.includes(d.key)
        return (
          <div
            key={d.key}
            className={on ? 'dim-row is-on' : 'dim-row'}
            role="checkbox"
            aria-checked={on}
            tabIndex={0}
            onClick={() => onToggle(d.key)}
            onKeyDown={(e) => {
              if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault()
                onToggle(d.key)
              }
            }}
          >
            <span className="dim-row__key">{d.key}</span>
            <div>
              <div className="dim-row__name">{d.name}</div>
              <div className="dim-row__desc">{d.desc}</div>
            </div>
          </div>
        )
      })}
    </div>
  )
}
