# en-US 本地化审查回归用例

用于验证共用框架和 `en-us-localization-rules.md`。测试不是新增产品规范；若项目规则另有规定，按规则优先级调整预期。除特别说明外，报告语言为简体中文、locale 为 `en-US`。预期要点是最低验收标准，不限制报告措辞。

## 用例

| ID | 输入 / 语境 | 预期判定 | 预期规则与行为 |
|---|---|---|---|
| T01 | 页面标题：`Account Settings`，页面同类标题均为 Title Case，项目未给大小写规范。 | 不判硬错；可不提或列建议统一。 | 不将 Title Case 偏好冒充规则；EN-US-TERM-01a。 |
| T02 | 字段标签 `Email address`；placeholder `name@example.com`；无代码信息。 | 当前可见文案合适，不推断无障碍实现缺陷。 | 标签/示例语境判断；EN-US-CMP-01c。 |
| T03 | 按钮 `Save changes.` | 若项目无例外，建议去掉句号，通常 P2。 | 按钮短控件标点；EN-US-PUN-01a。 |
| T04 | 错误正文 `Your changes was saved.`；目标状态为成功保存。 | 判语法错误，建议 `Your changes were saved.` 或更简洁的 `Changes saved.`（需贴合语气）。 | EN-US-GRAM-01a；状态真实无冲突。 |
| T05 | 中文“正在保存”；按钮/状态 `Saving…`。 | 符合；不能要求逐字译为完整句。 | 进行中状态和省略号语境；EN-US-STA-01a、EN-US-PUN-01d。 |
| T06 | 中文“保存成功”；toast `Save`。 | 标记动作/结果错位，给结果态最小改写，如 `Saved`。 | EN-US-STA-01a；组件语境。 |
| T07 | 英文 `No results found.`，中文源文“加载失败，请重试”。 | P1 语义状态差异：搜索无结果 vs 加载失败；不只做风格润色。 | EN-US-STA-01b、EN-US-BI-01a；保留错误真实状态并确认重试路径。 |
| T08 | 中文“最多上传 10 个文件”；英文 `Upload up to 10 files.` | 语义匹配且自然，判通过。 | EN-US-BI-01a。 |
| T09 | 中文“最多上传 10 个文件”；英文 `Upload 10 files.` | 指示精确数量而非上限，判语义差异；建议 `Upload up to 10 files.` | EN-US-BI-01a；不遗漏限制。 |
| T10 | 中文“删除后不可恢复。是否删除项目？”；英文 `This project will be deleted and cannot be restored. Delete?`，按钮 `Delete project`。 | 英文可理解；若要求更自然/完整，可建议 `Are you sure you want to delete this project? This action can't be undone.`，但不要因 `can't` 或短问句本身判错。 | EN-US-CMP-01d、EN-US-BI-01b；风险内容已保留。 |
| T11 | 地区明确美国；拼写 `Your favourite color`。 | 标出 `favourite` 非 en-US 常规拼写，建议 `favorite`；不要改 `color`。 | EN-US-LOC-01a。 |
| T12 | 项目术语表指定产品功能名 `Favourites`，英文 UI 与之相同。 | 按项目正式术语保留；不得仅因英式拼法判错。 | 项目词表优先于 EN-US-LOC-01a。 |
| T13 | 日期 `03/04/2026`，受众同时包括美国与英国，界面未标 locale。 | 标日期歧义/需确认；建议月份文字或 locale 化格式，不擅自确定是 3 月 4 日还是 4 月 3 日。 | EN-US-NUM-01a、EN-US-BI-01c。 |
| T14 | 面向美国单一用户群，既定日期格式为 `MM/DD/YYYY`，示例 `10/19/2026`。 | 不将该格式判错；若其他页面格式混乱才建议统一。 | 项目格式优先，EN-US-NUM-01a。 |
| T15 | 金额 `12.50`，没有币种信息；建议改为 `$12.50`。 | 不擅自补币种；列待确认金额币种/来源。 | EN-US-NUM-01d；禁止添加业务事实。 |
| T16 | 中文“移除成员”（仅解除工作区关系）；按钮 `Delete member`，无业务定义。 | 识别动作可能造成更强永久删除含义，标 P1/待确认，不直接断言数据删除；请求确认“移除”与“删除”实际后果。 | EN-US-TERM-01b、EN-US-BI-01a。 |
| T17 | 空状态：无搜索匹配 `No results`；另一组件网络失败 `Failed to load results. Try again.` | 两种状态区分正确。 | EN-US-CMP-01f、EN-US-STA-01b。 |
| T18 | 用户仅给 `No results`，问是否自然，未提供组件或源文；单条 QA。 | 按单条直接问答简答，不发 A–F 菜单；说明作为空结果文案通常自然，但需上下文确认是否是搜索结果。 | 共用单条 QA 协议；必要时“待确认”。 |
| T19 | 用户说“检查这些英文”，无 locale；文本含 `10/11/2026` 和 `colour`。 | 先询问目标语言地区或说明影响；不能直接按 en-US 改写。 | locale 边界；EN-US-LOC-01a、EN-US-NUM-01a。 |
| T20 | 链接 `Click here`，旁边唯一可见句为 `Read the privacy policy`，链接目标就是政策；无屏幕阅读器信息。 | 可以建议链接文本直接命名目标；不声称已证明代码无障碍失败。 | EN-US-A11Y-01a；区分文本审查与实现审查。 |
| T21 | 错误 `You entered the wrong email.`，表单校验明确说格式无效。 | 建议中性且具体的 `Enter a valid email address.`；避免责备。 | EN-US-CMP-01e、EN-US-TONE-01a。 |
| T22 | `Your data is always safe with us.`，项目未提供安全保证依据。 | 识别未经证实的绝对承诺，列待确认/高风险，不自行弱化为既定事实。 | EN-US-TONE-01b。 |
| T23 | placeholder 为 `MM/DD/YYYY`，校验错误要求 `DD/MM/YYYY`。 | 判格式冲突并指出实际可接受格式需产品确认，修正前后文一致。 | EN-US-CMP-01c、EN-US-NUM-01a。 |
| T24 | `Click “Save”, to continue.` | 英文标点位置及多余逗号问题；建议 `Click “Save” to continue.` 或按项目引号规则。 | EN-US-PUN-01a/b/c；不得用中文引号规则判定。 |
| T25 | 中文源文“你没有权限查看此报表”；英文 `This report is unavailable.` | 不能确认是无权限还是不可用；列 P1/待确认，并要求确定真实状态，避免猜成 `You don't have permission...`。 | EN-US-BI-01a、EN-US-STA-01b。 |
| T26 | 按钮 `Submit` 用于提交付款；用户要求避免改变业务口径但未提供付款是否最终扣款。 | 建议明确动作需待确认按钮业务语义/风险；不擅自改成 `Pay now`。 | EN-US-CMP-01b、共用证据边界。 |
| T27 | 已确认按 PaletX 审查；页面标题 `Network settings`，组件为窗口标题。 | 按 PX 标题大小写规则建议为 `Network Settings`；不得用通用 sentence case 建议覆盖。 | `PX-ENG-02` 高于 `EN-US-TERM-01a`。 |
| T28 | 已确认按 PaletX 审查；页面显示 `2026-10-19 09:05:00 AM`，来源明确指定系统使用 24 小时制。 | 建议去掉 AM 并保持时刻不变：`2026-10-19 09:05:00`；不使用“美国常见 12 小时制”推翻 PX。 | `PX-DAT-01` 高于 `EN-US-NUM-01b`；不得凭空更改时刻。 |
| T29 | 已确认按 PaletX 审查；完整错误说明 `File integrity check failed.` | 完整说明保留句号；不能套用对话框标题/按钮“不加句号”的组件规则。 | `PX-PUN-03`、`EN-US-PUN-01a`。 |
| T30 | 已确认按 PaletX 审查；提示 `Searching…` 对应正在搜索。 | 可用进行中省略号；不要求删除，且不能用省略号替代风险说明。 | `PX-PUN-04` 与 `EN-US-STA-01a`。 |
| T31 | 向导页标题 `Import Wizard!`；界面类型确认是向导。 | 按 `PX-WIZ-02` 删除标点并避免标题含 `Wizard`，例如 `Import`；若具体页面任务含义不足，先确认，不机械改写。 | `PX-WIZ-02`；标题建议不能损失任务辨识度。 |
| T32 | 向导页面只有说明句 `Your file is ready.`，缺少任何页面操作指令。 | 按 `PX-WIZ-03` 指出需有祈使句操作指令；根据实际下一步待补充，不猜按钮文本。 | `PX-WIZ-03`。 |
| T33 | 告警名 `EMS agent stops exceptionally`，语境是代理刚刚停止。 | 指出事件过去时不当，建议按真实技术语义改为 `The EMS agent stopped unexpectedly.`；确认 `unexpectedly` 是否准确。 | `PX-ALM-03`、`PX-ALM-07`；不把来源旧例 `exceptionally` 机械视为地道推荐。 |
| T34 | 错误通知 `Password authentication failed. Enter a valid password.` | 两句结构可用：事件失败 + 祈使建议；前提是已知密码无效且可由用户修正。 | `PX-ALM-01`、`PX-ALM-04`。 |
| T35 | 告警列表项 `Connection tested successfully.` | 可作为省略主语/系动词的通知短句；若弹窗正文空间充分可建议完整句，但不是绝对语法错误。 | `PX-ALM-04/05`。 |
| T36 | 计数器原文“当前可用 eNodeB 数目”，英文 `Number of current available eNodeB`。 | 建议 `Number of currently available eNodeBs`；需确认项目缩写的复数格式。 | `PX-CTR-02`、`PX-CTR-04`。 |
| T37 | “成功建立 RRC 连接次数”译为 `Number of RRC Connection Release`。 | 指出事件含义冲突（建立 vs 释放）、可数名词复数和动作名词表达问题；不只润色冠词。 | `PX-CTR-02/03`、双语语义规则。 |
| T38 | 按 PaletX 审查；翻译把设备接入网络写作 `Access the device to the network`。 | 依据 `PX-LEX-04` 指出 `Access` 不表示把设备接入网络；核实真实动作后建议使用 `Connect the device to the network`。 | `PX-LEX-03/04`。 |
| T39 | 按 PaletX 审查；按钮写 `Enabled`，点击后会打开功能开关。 | 按动作/状态区分建议改为 `Enable`；若控件显示的是当前状态而非操作按钮则保留状态形式。 | `PX-LEX-05`；依组件语境判断。 |
| T40 | 因空间紧张，把警告“删除后将永久移除所有项目且无法恢复”压缩为 `Delete items.` | 不允许仅为缩短而删掉范围和不可恢复风险；报告语义/风险损失并给保留关键信息的短版本或待确认。 | `PX-UI-02` 与高风险共用规则。 |
| T41 | 附件例句 `No matched result.` 作为空结果文案，未提供项目术语要求。 | 不机械把该原句当成规范范例；可建议更自然的表达（如 `No matching results.`），标注属于语法/自然度改进。 | `PX-PAT-11` 附件例句维护提醒、`EN-US-GRAM-01b`。 |
| T42 | 计数范围说明 `between 0 and 63`，业务仅给出闭区间 `[0, 63]`。 | 不采用附件对 between 不含端点的释义写法；建议明确 `from 0 to 63, inclusive` 或待确认产品惯例。 | `PX-PAT-15`；不可更改边界包含性。 |

## 验收清单

- 未确认 locale 时不假设 en-US；仅 locale 明确后加载本规则包。
- 明确采用 PaletX 时，加载 `PX-` 规则；同一问题与通用 `EN-US-` 建议冲突时以已确认且适用的 `PX-` 为准。
- 不把英语自然重组当成中英不一致；不把拼写/标题大小写偏好误报为硬规则。
- 至少覆盖按钮、标题、字段/placeholder、对话框、错误、空状态、进行中和成功状态的组件差异。
- 对日期/金额/单位不猜地区、币种、换算或真实值；对否定、数量、权限、风险和状态差异明确指出。
- 不根据纯文案断言不可见的代码实现；未能验证的业务信息标待确认。
- 用户提供的源规则例句若存在不自然英语、技术语义错译或彼此冲突，应遵循明确规则与项目术语，标记例句待维护，而不是把例句机械升级为标准。
- 单条 QA 不输出完整报告、COPY 编号或 UC 表；完整审查遵循共用模板。

执行型用例见 evals.json；使用 scripts/evaluate_outputs.py 检查真实模型输出。包含默认审查、地区未知、业务待确认、双语清单与 PX 优先级。
