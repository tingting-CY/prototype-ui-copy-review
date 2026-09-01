/** A single-line verdict produced by 单条速答 mode. */
export interface QuickAnswer {
  /** The submitted line, truncated for the card header. */
  text: string
  verdict: '符合' | '不符合' | '待确认'
  /** Dot colour for the verdict. */
  tone: string
  basis: string
  advice: string
}

/**
 * Judge one line of copy. 速答 only reasons about the visible text, so
 * anything without a component or object lands in 待确认.
 */
function judge(t: string): Pick<QuickAnswer, 'verdict' | 'tone' | 'basis' | 'advice'> {
  if (/操作失败|操作成功/.test(t)) {
    return {
      verdict: '不符合',
      tone: '#D9921A',
      basis: 'SPT-PAT-02 仅在对象、动作或原因无法进一步明确时使用；可明确时应优先 SPT-PAT-01。',
      advice: '补全操作与对象，例如“导出终端数据失败。”原因已知时再补原因与修复方式。',
    }
  }
  if (/删除|清空|重置/.test(t)) {
    return {
      verdict: '不符合',
      tone: '#DC4634',
      basis: 'HF-STA-06 高影响操作须说明对象与后果；HF-CMP-09 按钮应写明具体动作。',
      advice: '改为“删除成员“张三”后不可恢复。是否删除？”，按钮写“删除成员”。',
    }
  }
  if (/失败|错误|异常/.test(t)) {
    return {
      verdict: '不符合',
      tone: '#D9921A',
      basis: 'SPT-ACC-01 错误信息应覆盖表现／影响、原因与可执行的修复方式。',
      advice: '补上原因与修复动作；原因不可验证时只写已知影响，并列为待确认。',
    }
  }
  if (/。$/.test(t)) {
    return {
      verdict: '符合',
      tone: '#1F9D55',
      basis: 'SPT-PUN-01 常规中文提示句末使用中文句号。',
      advice: '保持原文。',
    }
  }
  return {
    verdict: '待确认',
    tone: '#6C717D',
    basis: '缺少组件、对象或业务口径，当前范围内无法判定。',
    advice: '补充所在组件与触发场景后我再判断。',
  }
}

/** Split a textarea's contents into the non-empty lines 速答 will judge. */
export function toLines(text: string): string[] {
  return text
    .split('\n')
    .map((l) => l.trim())
    .filter(Boolean)
}

export function quickAnswers(text: string): QuickAnswer[] {
  return toLines(text).map((t) => ({
    text: t.length > 18 ? t.slice(0, 18) + '…' : t,
    ...judge(t),
  }))
}
