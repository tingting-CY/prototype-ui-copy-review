/** Lucide-style line icons, inlined so they inherit `currentColor`. */

const base = {
  viewBox: '0 0 24 24',
  fill: 'none',
  stroke: 'currentColor',
  strokeLinecap: 'round',
  strokeLinejoin: 'round',
} as const

export function InfoIcon() {
  return (
    <svg width="13" height="13" strokeWidth="1.75" {...base}>
      <circle cx="12" cy="12" r="9" />
      <path d="M12 16v-4M12 8h.01" />
    </svg>
  )
}

export function CopyIcon() {
  return (
    <svg width="13" height="13" strokeWidth="1.75" {...base}>
      <rect x="9" y="9" width="12" height="12" rx="2" />
      <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1" />
    </svg>
  )
}

export function CheckIcon() {
  return (
    <svg width="14" height="14" strokeWidth="2" {...base}>
      <path d="M20 6 9 17l-5-5" />
    </svg>
  )
}
