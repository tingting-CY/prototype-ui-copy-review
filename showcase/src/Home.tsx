/**
 * Design: 校样工作台 — 瑞士编辑排版、暖白纸张、深墨文字与校样朱砂标记。
 * Keep the page text-led, asymmetric, and proofreader-like rather than card-heavy SaaS UI.
 */
import { useMemo, useState } from "react";
import {
  ArrowDownRight,
  ArrowUpRight,
  BookOpen,
  Check,
  ChevronRight,
  ClipboardCheck,
  Code2,
  Copy,
  Download,
  ExternalLink,
  FileText,
  Menu,
  Play,
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
const SOURCE_ZIP = `${REPOSITORY}/archive/refs/heads/main.zip`;
const RELEASE_PAGE = `${REPOSITORY}/releases/tag/v1.11.0`;
const RELEASE_DOWNLOAD = `${REPOSITORY}/releases/download/v1.11.0/prototype-ui-copy-review-v1.11.0.skill`;

const DEFAULT_COPY = "正在加载...\n操作成功\n删除确认弹窗按钮：确定";

function reviewCopy(rawText: string): ReviewAnswer[] {
  const entries = rawText
    .split("\n")
    .map((item) => item.trim())
    .filter(Boolean)
    .slice(0, 5);

  return entries.map((source) => {
    if (source.includes("正在加载...")) {
      return {
        source,
        verdict: "不符合",
        rule: "HF-PUN-05",
        suggestion: "改为“正在加载……”。",
      };
    }
    if (source.includes("操作成功") || source.includes("处理完成")) {
      return {
        source,
        verdict: "待确认",
        rule: "HF-STA-03",
        suggestion: "补充真实对象与动作，例如“规则已保存”。",
      };
    }
    if (source.includes("确定") && (source.includes("删除") || source.includes("移除"))) {
      return {
        source,
        verdict: "不符合",
        rule: "HF-STA-06",
        suggestion: "将泛化按钮替换为具体动作，例如“删除规则”。",
      };
    }
    return {
      source,
      verdict: "待确认",
      rule: "HF-GEN-04",
      suggestion: "补充组件、对象或真实状态后再核验。",
    };
  });
}

const capabilityRows = [
  ["01", "把高频错误变成可判定规则", "标点、状态、中英文混排、数字单位、组件用语与风险提示，不再只靠经验判断。", "HF-"],
  ["02", "把提示信息写得更清楚", "成功、失败、异常、进行中等反馈按状态结构核验，避免“操作成功”式泛化表达。", "SPT-"],
  ["03", "把设计系统落到每一句话", "仅在指定时加载 PaletX/ZTE 设计系统规则，防止不适用的结论干扰审查。", "PX-"],
  ["04", "把审查结论变成团队动作", "完整审查可输出带规则依据的 Markdown 修改清单，并记录值得补充的规范缺口。", "COPY-"],
];

const workflowSteps = [
  ["01", "提交材料", "截图、原型、文案清单或一条待确认的 UI 文案。"],
  ["02", "明确范围", "完整审查时选择维度；单条问答直接进入核验。"],
  ["03", "获得结论", "用规则编号说明问题，并保留“待确认”的业务边界。"],
  ["04", "交付与沉淀", "输出修改清单，或将重复出现的场景升级为规范治理项。"],
];

function VerdictStamp({ verdict }: { verdict: Verdict }) {
  return <span className={`verdict-stamp verdict-${verdict}`}>{verdict}</span>;
}

export default function Home() {
  const [sourceText, setSourceText] = useState(DEFAULT_COPY);
  const [hasRun, setHasRun] = useState(false);
  const [copied, setCopied] = useState(false);
  const [menuOpen, setMenuOpen] = useState(false);
  const answers = useMemo(() => reviewCopy(sourceText), [sourceText]);

  const handleCopy = async () => {
    await navigator.clipboard.writeText(`git clone ${REPOSITORY}.git`);
    setCopied(true);
    window.setTimeout(() => setCopied(false), 1800);
  };

  return (
    <main className="site-shell">
      <aside className="archive-rail" aria-hidden="true">
        <img src="assets/ui-copy-review-logo.webp" alt="" />
        <span>00 / 开篇</span><i />
        <span>01 / 问答</span><i />
        <span>02 / 规则</span><i />
        <span>03 / 安装</span>
      </aside>
      <header className="topbar">
        <a className="brand" href="#top" aria-label="UI Copy Review Skill 首页">
          <img src="assets/ui-copy-review-logo.webp" alt="" />
          <span>文案校样</span>
          <small>UI COPY REVIEW</small>
        </a>
        <nav className="desktop-nav" aria-label="主导航">
          <a href="#demo">直接问答</a>
          <a href="#capabilities">能力</a>
          <a href="#workflow">流程</a>
          <a href="#install">安装</a>
        </nav>
        <a className="github-link" href={REPOSITORY} target="_blank" rel="noreferrer">
          <Code2 size={16} /> GitHub <ArrowUpRight size={15} />
        </a>
        <button className="mobile-menu" onClick={() => setMenuOpen(!menuOpen)} aria-label="切换导航菜单">
          {menuOpen ? <X size={20} /> : <Menu size={20} />}
        </button>
        {menuOpen && (
          <nav className="mobile-nav" aria-label="移动端主导航">
            <a onClick={() => setMenuOpen(false)} href="#demo">直接问答</a>
            <a onClick={() => setMenuOpen(false)} href="#capabilities">能力</a>
            <a onClick={() => setMenuOpen(false)} href="#workflow">流程</a>
            <a onClick={() => setMenuOpen(false)} href="#install">安装</a>
          </nav>
        )}
      </header>

      <section id="top" className="hero section-frame">
        <div className="hero-copy reveal">
          <div className="eyebrow"><span className="eyebrow-dot" /> v1.11.0 · 中文 UI 文案审校 Skill</div>
          <h1>让每一句<br /><em>UI 文案</em>，都有规范可依。</h1>
          <div className="hero-proofline"><b>COPY-001</b><span>凭感觉写 <i>→</i> 按规则改</span></div>
          <p className="hero-lead">面向原型、截图和真实页面流程的中文文案审校工具。发现问题、给出依据、直接交付可落地的改法。</p>
          <div className="hero-actions">
            <a className="button button-vermilion release-download" href={RELEASE_DOWNLOAD}><Download size={17} /> 下载 Release · v1.11.0</a>
            <a className="button button-ink" href="#demo"><Play size={16} fill="currentColor" /> 直接检查一条文案</a>
            <a className="button button-quiet" href={REPOSITORY} target="_blank" rel="noreferrer">查看源码 <ArrowUpRight size={16} /></a>
          </div>
          <div className="hero-metadata">
            <span><ShieldCheck size={15} /> 仅基于明确规则下结论</span>
            <span><ClipboardCheck size={15} /> 支持完整审查与修改清单</span>
          </div>
        </div>

        <div className="hero-visual reveal delay-1" aria-label="校样工作台视觉示意">
          <img className="hero-art" src="assets/ui-copy-review-hero.webp" alt="校样编辑风格的文案审查工作台" />
          <div className="hero-mark"><img src="assets/ui-copy-review-logo.webp" alt="" /><span>文案校样<br /><small>UI COPY REVIEW</small></span></div>
          <div className="proof-card proof-card-top">
            <div className="proof-kicker">待检查文案 <span>01</span></div>
            <p>正在加载<span className="red-proof">...</span></p>
            <div className="proof-note"><span>×</span> 中文省略号应使用六点形式</div>
          </div>
          <div className="proof-card proof-card-bottom">
            <div className="proof-kicker">审校结论 <span>HF-PUN-05</span></div>
            <div className="proof-row"><VerdictStamp verdict="不符合" /><strong>正在加载……</strong></div>
            <p>最小改写，不改变原始业务语义。</p>
          </div>
        </div>
      </section>

      <section className="trust-strip section-frame" aria-label="Skill 基本信息">
        <span>简体中文 UI 文案</span><i />
        <span>HF- 高频规则</span><i />
        <span>SPT- 提示信息</span><i />
        <span>PX- 设计系统</span><i />
        <span>可追溯修改建议</span>
      </section>

      <section id="demo" className="demo-section section-frame">
        <div className="section-aside"><span>01</span><p>直接问答<br />DIRECT QA</p></div>
        <div className="section-content">
          <div className="section-heading">
            <div>
              <div className="eyebrow">一至五条文案，不必等待一份报告</div>
              <h2>把一条文案<br />放进规则里。</h2>
            </div>
            <p>对于少量明确的 UI 文案，Skill 不再追问 A–F 维度，也不生成冗长清单；它只回答结论、依据与最小建议。</p>
          </div>
          <div className="demo-workbench">
            <div className="input-pane">
              <div className="pane-header"><span>输入 · 1–5 条</span><span className="mono">ZH-CN</span></div>
              <label className="sr-only" htmlFor="copy-input">输入待检查文案</label>
              <textarea id="copy-input" value={sourceText} onChange={(event) => setSourceText(event.target.value)} placeholder="例如：正在加载..." />
              <div className="input-footer">
                <span>建议包含组件或场景</span>
                <button onClick={() => setHasRun(true)}><Sparkles size={15} /> 检查文案</button>
              </div>
            </div>
            <div className={`output-pane ${hasRun ? "has-run" : ""}`}>
              <div className="pane-header"><span>审校结论</span><span className="mono">LOCAL DEMO</span></div>
              <div className="answer-list">
                {answers.length === 0 ? (
                  <div className="empty-answer">输入一条文案后，结果会出现在这里。</div>
                ) : answers.map((answer, index) => (
                  <article className="answer-item" key={`${answer.source}-${index}`}>
                    <div className="answer-top"><span className="answer-index">{String(index + 1).padStart(2, "0")}</span><VerdictStamp verdict={answer.verdict} /></div>
                    <p className="answer-source">{answer.source}</p>
                    <dl><div><dt>依据</dt><dd className="mono">{answer.rule}</dd></div><div><dt>建议</dt><dd>{answer.suggestion}</dd></div></dl>
                  </article>
                ))}
              </div>
              <p className="demo-disclaimer">这是展示站的静态交互示例，不替代安装后的完整 Skill 审查。</p>
            </div>
          </div>
        </div>
      </section>

      <section id="capabilities" className="capability-section section-frame">
        <div className="capability-intro">
          <div className="section-aside"><span>02</span><p>规则资产<br />RULE ASSETS</p></div>
          <div>
            <div className="eyebrow">不只找错字，更要统一团队判断</div>
            <h2>从一句话，<br />到一套可维护的规范。</h2>
          </div>
          <img src="assets/ui-copy-review-rules.webp" alt="规则资产的编辑式索引卡视觉" />
        </div>
        <div className="capability-list">
          {capabilityRows.map(([num, title, body, code]) => (
            <article className="capability-row" key={num}>
              <span className="cap-number">{num}</span>
              <h3>{title}</h3>
              <p>{body}</p>
              <span className="rule-chip">{code}</span>
            </article>
          ))}
        </div>
      </section>

      <section id="workflow" className="workflow-section">
        <div className="section-frame workflow-grid">
          <div className="workflow-copy">
            <div className="eyebrow">从输入到可交付的修改建议</div>
            <h2>审校不是一句“建议优化”。</h2>
            <p>它应当指出哪里需要改、为什么需要改，以及哪些场景暂时无法在不改变业务语义的前提下给出唯一答案。</p>
            <a className="text-link" href={DOCUMENTATION} target="_blank" rel="noreferrer">阅读完整审查流程 <ArrowUpRight size={16} /></a>
          </div>
          <div className="workflow-steps">
            {workflowSteps.map(([num, title, body]) => (
              <article key={num}>
                <span>{num}</span><div><h3>{title}</h3><p>{body}</p></div><ChevronRight size={18} />
              </article>
            ))}
          </div>
        </div>
        <div className="workflow-art-wrap">
          <img src="assets/ui-copy-review-workflow.webp" alt="从原始文案到审校结论的编辑工作流" />
        </div>
      </section>

      <section id="install" className="install-section section-frame">
        <div className="install-grid">
          <div className="install-copy">
            <div className="section-aside"><span>03</span><p>安装与复用<br />INSTALL</p></div>
            <h2>保留完整目录，<br />让规则按需加载。</h2>
            <p>Skill 的主流程、规则库、提示词模板、回归用例和校验脚本彼此关联。请下载或克隆完整仓库，不要单独复制某一个文件。</p>
            <div className="install-actions">
              <a className="button button-vermilion release-download" href={RELEASE_DOWNLOAD}><Download size={17} /> 下载 Release · v1.11.0</a>
              <a className="button button-quiet" href={RELEASE_PAGE} target="_blank" rel="noreferrer"><BookOpen size={17} /> 查看更新说明</a>
            </div>
            <p className="release-note"><span>最新版</span> 完整 `.skill` 安装包，内含规则库、模板、校验脚本与回归用例。</p>
          </div>
          <div className="install-terminal">
            <div className="terminal-top"><span /><span /><span /><b>获取 Skill</b></div>
            <code><span className="terminal-prompt">$</span> git clone {REPOSITORY}.git<br /><span className="terminal-comment"># 保留 SKILL.md、references、docs、scripts 与 evals 目录</span></code>
            <button className="copy-button" onClick={handleCopy}>{copied ? <Check size={16} /> : <Copy size={16} />}{copied ? "已复制" : "复制命令"}</button>
          </div>
        </div>
        <div className="boundary-note"><ShieldCheck size={17} /><p><strong>使用边界：</strong>Skill 只对可见文案与已确认规则给出结论。涉及业务定义、权限、真实状态、安全、法务或品牌口径时，会标为“待确认”，而不会擅自改写。</p></div>
      </section>

      <footer className="site-footer section-frame">
        <div className="footer-brand"><img src="assets/ui-copy-review-logo.webp" alt="" /><span>文案校样</span><small>UI COPY REVIEW · v1.11.0</small></div>
        <div className="footer-links"><a href={REPOSITORY} target="_blank" rel="noreferrer"><Code2 size={15} /> GitHub</a><a href={`${REPOSITORY}/releases`} target="_blank" rel="noreferrer"><FileText size={15} /> Releases</a><a href={`${REPOSITORY}/blob/main/CONTRIBUTING.md`} target="_blank" rel="noreferrer">贡献指南 <ArrowUpRight size={14} /></a></div>
      </footer>
    </main>
  );
}
