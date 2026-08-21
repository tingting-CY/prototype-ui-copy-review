/**
 * Design: 留白校样 — 数字瑞士极简主义，近白画布、无衬线排版、朱砂修订点缀。
 * Keep one light theme, generous negative space, two primary actions, and one real interactive workbench.
 */
import { useEffect, useMemo, useState } from "react";
import {
  ArrowDownRight,
  ArrowUpRight,
  Check,
  Copy,
  Download,
  FileText,
  Code2,
  Menu,
  ShieldCheck,
  Sparkles,
  X,
} from "lucide-react";

type Verdict = "符合" | "不符合" | "待确认";

type ReviewAnswer = {
  source: string;
  verdict: Verdict;
  rule: string;
  suggestion: string;
};

const REPOSITORY = "https://github.com/tingting-CY/prototype-ui-copy-review";
const DOCUMENTATION = `${REPOSITORY}/blob/main/docs/README.md`;
const RELEASE_PAGE = `${REPOSITORY}/releases/tag/v1.11.0`;
const RELEASE_DOWNLOAD = `${REPOSITORY}/releases/download/v1.11.0/prototype-ui-copy-review-v1.11.0.skill`;
const DEFAULT_COPY = "正在加载...\n操作成功\n删除确认弹窗按钮：确定";

const capabilities = [
  ["HF-", "高频规则", "标点、状态、混排与组件用语，按可判定规则检查。"],
  ["SPT-", "提示信息", "让成功、失败和进行中反馈更具体、更可执行。"],
  ["PX-", "设计系统", "仅在指定时加载产品设计系统，避免无关结论。"],
  ["COPY-", "修改清单", "完整审查将结论转成可追溯、可落地的团队动作。"],
];

const steps = [
  ["01", "INPUT", "提交材料", "截图、原型、文案清单，或一条待确认的 UI 文案。"],
  ["02", "HF- / SPT-", "获得结论", "明确的问题给出规则依据；业务语境不足时标为待确认。"],
  ["03", "COPY-", "落地修改", "完整审查交付修改清单，并将重复场景沉淀为规范。"],
];

function reviewCopy(rawText: string): ReviewAnswer[] {
  const entries = rawText.split("\n").map((item) => item.trim()).filter(Boolean).slice(0, 5);

  return entries.map((source) => {
    if (source.includes("正在加载...")) {
      return { source, verdict: "不符合", rule: "HF-PUN-05", suggestion: "改为“正在加载……”。" };
    }
    if (source.includes("操作成功") || source.includes("处理完成")) {
      return { source, verdict: "待确认", rule: "HF-STA-03", suggestion: "补充真实对象与动作，例如“规则已保存”。" };
    }
    if (source.includes("确定") && (source.includes("删除") || source.includes("移除"))) {
      return { source, verdict: "不符合", rule: "HF-STA-06", suggestion: "将泛化按钮替换为具体动作，例如“删除规则”。" };
    }
    return { source, verdict: "待确认", rule: "HF-GEN-04", suggestion: "补充组件、对象或真实状态后再核验。" };
  });
}

function Verdict({ value }: { value: Verdict }) {
  return <span className={`verdict verdict-${value}`}>{value}</span>;
}

export default function Home() {
  const [sourceText, setSourceText] = useState(DEFAULT_COPY);
  const [hasRun, setHasRun] = useState(false);
  const [copied, setCopied] = useState(false);
  const [menuOpen, setMenuOpen] = useState(false);
  const [pageReady, setPageReady] = useState(false);
  const answers = useMemo(() => reviewCopy(sourceText), [sourceText]);

  useEffect(() => {
    const timer = window.setTimeout(() => setPageReady(true), 60);
    return () => window.clearTimeout(timer);
  }, []);

  const copyCommand = async () => {
    await navigator.clipboard.writeText(`git clone ${REPOSITORY}.git`);
    setCopied(true);
    window.setTimeout(() => setCopied(false), 1600);
  };

  return (
    <main className={`quiet-shell ${pageReady ? "is-ready" : ""}`}>
      <div className="page-loader" aria-hidden="true"><span /></div>
      <header className="quiet-nav">
        <a className="brand" href="#top" aria-label="文案校样首页">
          <img src="assets/ui-copy-review-logo.webp" alt="" />
          <span>文案校样</span><small>UI COPY REVIEW</small>
        </a>
        <nav className="nav-links" aria-label="主导航">
          <a href="#demo">直接问答</a><a href="#rules">规则</a><a href="#process">流程</a><a href="#install">安装</a>
        </nav>
        <a className="nav-github" href={REPOSITORY} target="_blank" rel="noreferrer"><Code2 size={15} /> GitHub <ArrowUpRight size={14} /></a>
        <button className="menu-button" onClick={() => setMenuOpen(!menuOpen)} aria-label="切换导航菜单">{menuOpen ? <X size={19} /> : <Menu size={19} />}</button>
        {menuOpen && <nav className="mobile-nav" aria-label="移动端主导航"><a href="#demo" onClick={() => setMenuOpen(false)}>直接问答</a><a href="#rules" onClick={() => setMenuOpen(false)}>规则</a><a href="#process" onClick={() => setMenuOpen(false)}>流程</a><a href="#install" onClick={() => setMenuOpen(false)}>安装</a></nav>}
      </header>

      <section id="top" className="hero frame">
        <div className="hero-copy">
          <p className="version-note"><span /> v1.11.0 · 中文 UI 文案审校 Skill</p>
          <h1>UI 文案，<br />先有<span>明确结论</span>。</h1>
          <p className="hero-lead">面向原型、截图和真实页面流程的中文文案审校工具。发现问题，说明依据，直接给出可落地的改法。</p>
          <p className="proof-tag"><b>COPY-001</b><span>凭感觉写</span><i>→</i><span>按规则改</span></p>
          <div className="hero-actions">
            <a className="button primary release-cta" href={RELEASE_DOWNLOAD}><Download size={17} /> 下载 Release · v1.11.0</a>
            <a className="button secondary" href="#demo">直接检查一条文案 <ArrowDownRight size={17} /></a>
          </div>
        </div>
        <figure className="hero-visual">
          <img src="assets/ui-copy-review-hero.webp" alt="校样编辑风格的文案审查工作台" />
          <figcaption><img src="assets/ui-copy-review-logo.webp" alt="" /> 仅对明确规则给出结论</figcaption>
        </figure>
      </section>

      <div className="skill-strip frame" aria-label="Skill 信息"><span>ZH-CN</span><span>HF 高频规则</span><span>SPT 提示信息</span><span>PX 设计系统</span><span>可追溯修改建议</span></div>

      <section id="demo" className="section frame demo-section">
        <div className="section-intro">
          <p className="section-number">01 / DIRECT QA</p>
          <h2>少量文案，<br />直接回答。</h2>
          <p>一次输入一至五条明确的 UI 文案。无需选择复杂范围，只返回结论、规则依据和最小修改建议。</p>
        </div>
        <div className="review-workbench">
          <div className="input-pane">
            <div className="pane-label"><span>输入文案</span><small>1–5 条</small></div>
            <label className="sr-only" htmlFor="copy-input">输入待检查文案</label>
            <textarea id="copy-input" value={sourceText} onChange={(event) => setSourceText(event.target.value)} placeholder="例如：正在加载..." />
            <div className="input-footer"><span>建议包含组件或场景</span><button onClick={() => setHasRun(true)}><Sparkles size={15} /> 检查文案</button></div>
          </div>
          <div className={`output-pane ${hasRun ? "has-run" : ""}`}>
            <div className="pane-label"><span>审校结论</span><small>HF- / SPT- / PX-</small></div>
            <div className="answer-list">
              {answers.length === 0 ? <p className="empty-answer">输入一条文案后，结果会出现在这里。</p> : answers.map((answer, index) => <article className="answer" key={`${answer.source}-${index}`}><div><span className="answer-index">{String(index + 1).padStart(2, "0")}</span><Verdict value={answer.verdict} /></div><strong>{answer.source}</strong><p><span>依据</span><code>{answer.rule}</code></p><p><span>建议</span>{answer.suggestion}</p></article>)}
            </div>
            <p className="demo-note">静态交互示例，不替代安装后的完整 Skill 审查。</p>
          </div>
        </div>
      </section>

      <section id="rules" className="section frame rules-section">
        <div className="section-intro narrow">
          <p className="section-number">02 / RULE ASSETS</p>
          <h2>让团队判断<br />有同一把尺子。</h2>
        </div>
        <div className="rule-grid">
          {capabilities.map(([code, title, body]) => <article key={code}><code>{code}</code><h3>{title}</h3><p>{body}</p></article>)}
        </div>
      </section>

      <section id="process" className="section frame process-section">
        <div className="section-intro narrow"><p className="section-number">03 / PROCESS</p><h2>把“建议优化”<br />变成可执行修改。</h2></div>
        <div className="process-list">{steps.map(([number, signal, title, body]) => <article key={number}><span>{number}</span><div><code>{signal}</code><h3>{title}</h3><p>{body}</p></div></article>)}</div>
        <a className="text-link" href={DOCUMENTATION} target="_blank" rel="noreferrer">阅读完整审查流程 <ArrowUpRight size={16} /></a>
      </section>

      <section id="install" className="section frame install-section">
        <div className="install-copy"><p className="section-number">04 / INSTALL</p><h2>下载完整 Release，<br />保留完整目录。</h2><p>主流程、规则库、模板、回归用例和校验脚本彼此关联。请下载完整安装包，而非单独复制文件。</p><div className="install-actions"><a className="button primary release-cta" href={RELEASE_DOWNLOAD}><Download size={17} /> 下载 Release · v1.11.0</a><a className="plain-link" href={RELEASE_PAGE} target="_blank" rel="noreferrer">查看更新说明 <ArrowUpRight size={15} /></a></div><p className="release-note"><span>最新版</span> 完整 `.skill` 安装包，附带 SHA-256 校验文件。</p></div>
        <div className="command-block"><p>也可以从源码克隆</p><code><b>$</b> git clone {REPOSITORY}.git</code><button onClick={copyCommand}>{copied ? <Check size={15} /> : <Copy size={15} />}{copied ? "已复制" : "复制命令"}</button></div>
      </section>

      <aside className="boundary frame"><ShieldCheck size={17} /><p><strong>使用边界：</strong>Skill 只对可见文案与已确认规则给出结论。涉及业务定义、权限、真实状态、安全、法务或品牌口径时，会标为“待确认”。</p></aside>

      <footer className="footer frame"><div className="footer-brand"><img src="assets/ui-copy-review-logo.webp" alt="" /><span>文案校样</span><small>UI COPY REVIEW · v1.11.0</small></div><div><a href={REPOSITORY} target="_blank" rel="noreferrer">GitHub</a><a href={`${REPOSITORY}/releases`} target="_blank" rel="noreferrer"><FileText size={14} /> Releases</a><a href={`${REPOSITORY}/blob/main/CONTRIBUTING.md`} target="_blank" rel="noreferrer">贡献指南</a></div></footer>
    </main>
  );
}
