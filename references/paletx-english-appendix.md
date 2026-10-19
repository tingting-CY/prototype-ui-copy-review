# PaletX 英文规则附录（按需加载）

> 本文件补充 `references/paletx-design-system-copy-spec.md` 中的英文规则；仅在采用 PaletX/ZTE 且目标界面为英语时加载。规则源自用户提供的 PaletX 英文附录摘录；原网页本次未能在线复核。项目正式术语与业务定义优先；不要将示例机械视为标准。

## 7. 向导文案（PX-WIZ）

| 规则 ID | 可判定要求 | 示例/审查动作 | 例外/说明 |
|---|---|---|---|
| PX-WIZ-01 | 向导对用户或其计算机、文档、设置等使用第二人称 `you/your`；不要让计算机或向导以第一人称自称。 | `Your settings`；避免系统作为说话者写 `I will…`。 | 用户需要选择的选项可从用户视角使用 `my`。 |
| PX-WIZ-02 | 向导页标题除问号外不使用标点，且不出现 `Wizard`。 | 检查标题本身，不将正文规则扩展到标题。 | 有批准的产品专名例外时遵循项目词表。 |
| PX-WIZ-03 | 每个向导页面都应有明确操作指令；英语指令使用祈使句。 | `Select a file`、`Enter your account name`。 | 若截图不完整或该页是纯状态/结果页，先确认页面角色，不猜缺失文案。 |
| PX-WIZ-04 | 信息反馈按钮以动词开头。 | 优先具体动作词，结合页面目标核验。 | 来源明确保留 `OK`、`Yes`、`No` 例外；不因这条规则把高风险确认按钮改成含糊的 `Yes`。 |

## 8. 告警、通知与状态消息（PX-ALM）

| 规则 ID | 可判定要求 | 示例/审查动作 | 例外/说明 |
|---|---|---|---|
| PX-ALM-01 | 告警/通知名称建议采用句子大小写；名称与描述按其语义选择恰当的词性和句式。处理建议使用祈使句。 | `Password authentication failed`；`Enter a valid password.` | 名称、代码及官方产品术语按正式写法。 |
| PX-ALM-02 | 表示出现时仍成立的当前状态，按语义使用 `be + adjective`、`be + past participle`（被动/已完成）或 `be + present participle`（进行中）。 | `The license is expired`/`License expired`；`Data is being transmitted`。 | 省略式消息可按 PX-ALM-04 省略句首冠词或系动词；需确认消息表达当前状态而非刚发生的事件。 |
| PX-ALM-03 | 表示刚发生的非持续性事件（如 fail、succeed、occur）通常用一般过去时。 | `The backup operation failed.`；`An error occurred while loading…`。 | 明确表达当前状态或产品固定句型可用相应时态。 |
| PX-ALM-04 | 告警/通知可依空间和组件语境使用省略句。可省略句首冠词、主语或系动词；常见形式包括 `Failed to…`、`Unable to…`、`… failed`、分词/形容词短语和名词短语。 | `Failed to build component types.`；`Connection tested successfully.`；`Database overload.` | 空间足够（如弹窗正文）优先完整句；短语必须自然、含义明确。不得将一般正文无差别改成电报式碎片。 |
| PX-ALM-05 | 消息用作标题或列表项时通常不加句号；问句用问号；来源不建议感叹号。完整描述句正常使用标点。若末尾是名称、代码、路径、链接等，避免句点被误认为字符串内容。 | 区分列表消息、标题、正文和可复制值。 | 组件级标点规则与 `PX-PUN-03` 合并判定。 |
| PX-ALM-06 | 消息应避免冗余表达：不重复 `alarm` 等已由组件角色表达的信息；`detected` 等若未增加有用事实可删；严重程度作为附加说明时可用括号区分。 | `Process exception alarm` → `Process exception`；`… lost (critical)`。 | 若“检测到”确为重要来源信息或用户需要识别告警类别，保留并列待确认。 |
| PX-ALM-07 | 告警、通知示例中的语态、冠词、词性及技术搭配应按实际含义修正，不将示例机械套用。 | 核验 `overload` 作名词/形容词、`authorization` 名词、事件过去时，以及技术术语。 | 附件中例句是规则说明样本；原文歧义时先确认业务含义。 |

### 告警/通知省略句型速查

| 功能 | 可用结构示例 | 审查要点 |
|---|---|---|
| 成功 | `The desktop was restarted successfully.`；`Connection tested successfully.` | 选择完整句或简短结果表达，确保表达真实完成。 |
| 失败/无法完成 | `Failed to build component types.`；`Unable to determine the log source.`；`Password authentication failed.` | 处理建议另起祈使句；不得编造失败原因。 |
| 超时 | `Query timed out.`；名词短语 `Response timeout.` | 按句子或短语语境选择形式。 |
| 错误/异常 | `An unknown error has occurred.`；`An error occurred while loading…` | 当前结果与刚发生事件使用相符时态。 |
| 权限 | `You do not have permission to…`；`You are not authorized to…` | 使用产品批准的权限术语，不混淆授权与技术可用状态。 |
| 进行中 | `Loading…`、`Querying…`、`Connecting…`、`Processing…` | 仅用于真实进行中状态，遵循 `PX-PUN-04`。 |

## 9. 计数器与指标名称（PX-CTR）

| 规则 ID | 可判定要求 | 示例/审查动作 | 例外/说明 |
|---|---|---|---|
| PX-CTR-01 | 计数器名称建议采用句子大小写；句首 `the` 可省略。明确这是数量还是次数，再选择结构。 | `Number of call attempts`；`Number of successful RRC connection establishments`。 | 遵循项目已批准的指标命名系统。 |
| PX-CTR-02 | `Number of + 可数名词复数`；计数技术动作时可将动作名词作为可数对象表达。 | `Number of eNodeBs`、`Number of successful handovers`。 | 专业术语如 `handover`、`setup`、`establishment`、`connection` 的可数性需结合领域词表。 |
| PX-CTR-03 | “次数”可按含义使用 `Number of [plural action nouns]` 或 `Number of times that + clause`；如中英表达习惯不同，可在不改变统计口径前提下调整结构。 | `Number of times that the device reported an alarm`。 | 不把计量对象由事件次数改成实体数量；歧义时待确认。 |
| PX-CTR-04 | 修饰语应放在能清楚限定对象/动作的位置；表示当前可用等状态时用副词修饰形容词；注意单复数和缩写正式形态。 | `Number of currently available eNodeBs`；`Number of uplink TBs scheduled for PCC UEs`。 | 领域大小写及缩写按技术术语表。 |
| PX-CTR-05 | 时间、数据量等物理量使用清楚的量纲表达，如 `Duration of…`、`Bytes of…`；避免不自然的 `Times of…` 表“次数”。 | 对照指标定义和数据单位。 | 未提供指标定义、分子/分母或统计窗口时不得改写其口径。 |
| PX-CTR-06 | 本规范样例对描述统计器功能倾向一般现在时；若项目实际定义为已发生事件统计，应按指标语义确定时态。 | 对照数据定义，不只按英语惯例改时态。 | 来源指出其他企业可能使用过去时/现在完成时，属于实现差异而非普遍错误。 |

## 10. 英文术语与动词/状态区分（PX-LEX）

| 规则 ID | 可判定要求 | 来源术语/用法示例 | 例外/说明 |
|---|---|---|---|
| PX-LEX-01 | 登录/注销作动作按钮时用动词短语 `Log In` / `Log Out`；作名词标题/概念时用 `login` / `logout`，按来源大小写系统处理。 | `Log In` 按钮；`Login settings` 标题。 | 如产品词表固定为 `Sign in`，遵循已批准术语并全局一致。 |
| PX-LEX-02 | `Show` 常用于界面内 Show/Hide 控制；`display` 多用于描述性正文，需结合对象和句法选择。 | `Show details`；正文 `The result is displayed…`。 | 不将词语映射当成无条件替换规则。 |
| PX-LEX-03 | `New` 通常用于新建虚拟对象；将既有设备/实体接入系统通常使用 `Connect`，避免混淆创建与接入。 | `New task` vs `Connect a device`。 | 以实际业务动作定义为准。 |
| PX-LEX-04 | `Access` 表示取得访问/连接通路或访问资源，不用于“把设备连接到网络”的动作；该动作通常用 `Connect`。 | `Access the database/network`；`Connect the device to the network`。 | 技术产品官方术语优先。 |
| PX-LEX-05 | 区分动作动词与状态词：按钮用 `Enable`/`Disable`、`Activate`、`Suspend` 等动作；状态用 `Enabled`/`Disabled`、`Activated`、`Suspended`。`Active` 描述运行/打开状态，`Activated` 可表达经过激活动作后的状态。 | 入口与状态标签分别核对。 | 必须以控件真实行为和状态定义为依据。 |
| PX-LEX-06 | 常用产品动词和术语按术语表统一，保留词性及含义差异。 | 例如 `Back Up` 作动词、`Backup` 作名词/形容词；`Operate` 作动词、`Operation` 作名词；`Modify`、`Edit`、`Change` 不无差别互换。 | 下表列出的来源术语是候选标准，不得替代项目术语表或业务确认。 |
| PX-LEX-07 | 短控件可按语境用简洁词，说明句需给出自然语法结构。 | `Details` 作标题；正文使用 `Details of…`；`Max`/`Min` 仅在上下文明确时替代 `Maximum`/`Minimum`。 | 缩写、大小写及空格需遵循 `PX-ENG`。 |

### 附件术语清单（审查时按语境和项目词表取用）

| 功能/概念 | 来源建议用法 | 语境提醒 |
|---|---|---|
| 登录/注销 | `Log In` / `Log Out`；名词 `login` / `logout` | 区分动作与名词。 |
| 显示/隐藏 | `Show` / `Hide`；描述语境可用 `display` | 按 UI 控件或正文选择。 |
| 新建/接入 | `New` / `Connect` | 凭空创建对象与连接既有实体不同。 |
| 查询/查看/查找 | `Query` / `View` / `Find` | 按查询数据、查看内容、定位项目区分。 |
| 修改/更改/编辑 | `Modify` / `Change` / `Edit` | 不视作同义词；如 `Change Password`。 |
| 删除/移除/清除 | `Delete` / `Remove` / `Clear` | 数据后果不同，须确认。 |
| 设置/配置/应用 | `Settings`、`Set…` / `Configure` / `Apply` | 标题名词与按钮动作区分。 |
| 启用/禁用/激活 | `Enable`/`Enabled`、`Disable`/`Disabled`、`Activate`/`Activated` | 动作与当前状态区分。 |
| 开始/暂停/继续/结束 | `Start` / `Pause` / `Resume` / `Stop` | 按真实状态转换选择。 |
| 完成/成功/失败 | `Done` / `Succeeded` / `Failed` | 状态、动作、反馈分别处理。 |
| 导入/导出/备份/恢复 | `Import` / `Export` / `Back Up`（动词）/ `Restore` | `backup` 作名词时不拆写。 |
| 选择/全选/清空选择 | `Select` / `Select All` / `Clear All` | Clear all 的对象需明确。 |
| 折叠/展开/放大/缩小 | `Collapse` / `Expand` / `Zoom In` / `Zoom Out` | 保持平行。 |
| 下一步/上一步/前进/后退 | `Next` / `Previous`；`Forward` / `Backward` | 不混淆流程导航与空间移动。 |
| 最大化/最小化/全屏 | `Maximize` / `Minimize` / `Full Screen` / `Exit Full Screen` | 按组件和产品既定术语。 |
| 高级设置/详细信息/管理 | `Advanced Settings` / `Details` / `… Management` | 按组件规则省略冗余词。 |
| 可选/已选/默认/状态 | `Available` / `Selected` / `Default` / `Status` | 需与真实状态语义一致。 |
| 用户/客户端/服务器/数据库 | `User` / `Client` / `Server` / `Database`（或批准缩写 `DB`） | 缩写仅在受众熟知并获准时用。 |
| 地址/序号/任务标识 | `Address`（`Addr.`仅限批准缩写）/ `Number`（`No.`仅限批准缩写）/ `Task ID` | 不随意造缩写。 |
| 空值/有效/无效/异常 | `null` / `Valid` / `Invalid` / `Abnormal` | `null` 是技术空值，不总等同于空白。 |
| 正常/活动/不活动/忙/闲 | `Normal` / `Active` / `Inactive` / `Busy` / `Idle` | 依产品状态定义。 |
| 在用/过期/挂起 | `Used` 或 `In Service` / `Expired` / `Suspend`（动作）、`Suspended`（状态） | 适用范围需由术语表澄清。 |
| 权限/公开/共享/私有 | `authorized` / `public` / `shared` / `private` | 特别核对访问权限和可编辑范围，不扩展业务含义。 |
| 确定/取消/提交/关闭/返回 | `OK` / `Cancel` / `Submit` / `Close` / `Back` | 操作按钮需符合实际动作；高风险按钮不能仅靠 OK。 |
| 时间字段 | `Start Time`/`From`，`End Time`/`To`，`Stop Time`/`To` | From/To 需同页定义一致，End 与 Stop 不混为一谈。 |
| 连接/访问/获取 | `Connect` / `Access` / `Obtain` | 物理/网络连接、取得访问权限和取得对象各异。 |
| 计数/边界 | `Number of…` / `Total` / `Max` / `Min` | 统计数量与上限/下限区分。 |

## 11. 英文提示句型（PX-PAT）

以下为附件中的已提炼句式库，须先确认实际含义、组件和业务定义，再作为建议表达；例句不是无条件替换模板。用表内 `PX-PAT-` 编号引用具体类别。

| 规则 ID | 语义 | 来源句型示例 | 应核对的差异 |
|---|---|---|---|
| PX-PAT-01 | 存在/不存在 | `xxx already exists.` / `xxx does not exist.` | 对象名称、时态及是否实际存在。 |
| PX-PAT-02 | 无法操作/空值 | `Cannot…`；`xxx cannot be null.` | 具体动作、值是否可空以及可执行下一步。 |
| PX-PAT-03 | 不唯一/不匹配 | `xxx must be unique.`；`Time zone value mismatch.` / `The time zone value does not match.` | 短语或完整句的组件差异。 |
| PX-PAT-04 | 无效/越界 | `xxx is invalid.`；`xxx is out of range.` | 区分无效格式与合法范围之外。 |
| PX-PAT-05 | 达到上限/超过门限 | `xxx has reached the maximum.`；`xxx exceeds the threshold.` | 数值关系与阈值定义不可更改。 |
| PX-PAT-06 | 超时 | `Ping timed out.`；短语 `Response timeout.`；`Timeout when querying…` | 句子、名词短语和带修饰语表达对应不同组件。 |
| PX-PAT-07 | 成功/失败 | `Succeeded in doing…`（即时提示示例）；`Failed to…`；`xxx succeeded/failed.`；`xxx has been successfully done.` | 选择主动/被动、事件/结果与语气，遵循 `PX-ALM`。 |
| PX-PAT-08 | 错误 | `xxx error` / `Error in…`；`An error occurred during…`；`An error occurred while…` | 错误对象及过程清楚；原因未确认时不要补造。 |
| PX-PAT-09 | 大小关系 | `larger than or equal to` / `smaller than or equal to` | 数学关系和边界含等号的语义必须准确。 |
| PX-PAT-10 | 操作确认 | `The operation will… Are you sure you want to continue?` | 明确后果和对象；保留高风险信息，不仅机械使用模板。 |
| PX-PAT-11 | 无结果/无可操作项 | `No matching results.`；`No data to print/save.`；`No record to activate.` | 按具体动作、对象、搜索结果状态区分；附件中的 `No matched…` 需先做自然度审查，不机械复制。 |
| PX-PAT-12 | 可用性/权限 | `No xxx is available.`（句子）/ `No xxx available.`（短语）；`You are not authorized to…` | 单复数、权限状态及完整句/短语组件语境。 |
| PX-PAT-13 | 检查/输入/选择/指定 | `Check/Verify…`；`Enter…`；`Select…`；`Specify…` | 选最具体的动作动词，并与字段/错误状态相配。 |
| PX-PAT-14 | 顺序/前置动作 | `Do xxx first.`；`Do xxx before doing xxx.` | 明确先后顺序，不改动流程。 |
| PX-PAT-15 | 范围/数量上限/常见事实 | `from…to…`；`between…and…`；`At most… can be selected.`；`xxx is busy. Please try again later.` | 边界是否包含必须依据业务定义；数量、对象、状态和建议必须有事实支撑。 |

源附件中的若干英文例句存在可疑搭配、语义错译或不自然表达（如 `No matched result`、`You have no right to…`、`Times of…`、部分比较级或条件范围示例）。审查时应遵循更明确的 PX 语法、术语和语义规则，不能把这些原始样例当成推荐标准；必要时标记“来源示例待维护”，并提出规范维护项。

## 12. 英文界面压缩与修饰语（PX-UI）

| 规则 ID | 可判定要求 | 示例/审查动作 | 例外/说明 |
|---|---|---|---|
| PX-UI-01 | 英文通常比中文占用更多版面；双语产品应检查文案被截断、布局拥挤或信息密度失衡。 | 根据界面截图/设计稿报告具体截断文本，不从字符串长度推断实际布局失败。 | 纯文案清单无布局证据时只提示风险，不判视觉缺陷。 |
| PX-UI-02 | 在不损失用户决策所需含义时，可省略次要、重复或上下文显而易见的信息，采用读者熟悉且获准的缩写，或改用更简洁的词组结构。 | `Query by User-Defined Conditions` → `Query by Conditions`（仅在上下文确实明确时）；`logs of the invocation` → `invocation logs`。 | 不得删减否定、条件、风险、权限、对象区分、限制或法定信息；不创造缩写。 |
| PX-UI-03 | 英文定语结构须避免歧义。形容词通常描述性质；名词作定语关系多义；现在分词可表主动/进行或关联动作；过去分词通常表被动/完成。 | 对 `English teacher` 等多义组合，改用明确释义；核对修饰对象、语态与时间。 | 技术复合术语以正式词表为准；不把机械语法转换当作必须改写。 |
