/** Severity tone of an issue — drives pin colour, tag colour and card accent. */
export type Tone = 'danger' | 'warning' | 'info' | 'violet'

/** One finding in the 问题清单 / one annotation pin on the screenshot. */
export interface Issue {
  /** Pin number, 1-based; also the identity used for selection. */
  n: number
  /** Rendered label, e.g. `P0 · COPY-001` or `UC-001 · 未涉及规范`. */
  tag: string
  /** Where the copy lives, e.g. `成员管理 · 删除确认弹窗`. */
  loc: string
  tone: Tone
  /** The copy as it appears in the reviewed screen. */
  orig: string
  /** Proposed rewrite (or, for UC- items, the evaluation to run). */
  fix: string
  /** Why it was flagged. */
  note: string
  /** Rule codes backing the finding, ` · `-separated, or free text. */
  rules: string
  /** Which surfaces the change propagates to. */
  scope: string
}

/** One entry in the 规则库. */
export interface Rule {
  code: string
  title: string
  /** How many findings in the current review cite this rule. */
  hit: number
  desc: string
}

/** One of the A–F review dimensions. */
export interface Dimension {
  key: string
  name: string
  desc: string
}

/** Palette for a tone: pin/dot fill, soft background, foreground text. */
export interface ToneColors {
  c: string
  bg: string
  fg: string
}
