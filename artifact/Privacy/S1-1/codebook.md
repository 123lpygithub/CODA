# Privacy — S1-1

652 artifacts; 15 codes; 2183 artifact–code assignments.

Analyst-authored refinement of the existing S1-1 codebook: individual review of existing case rationales, provisional concepts, scope notes and source quotations; explicit case-ID decisions split A, C and E and screen other cases for missed memberships. Scripts serialize those decisions and validate evidence and format; no keyword classifier is used.

## Refinement scope

本轮是已有编码的细化，不是新的全量原文独立阅读实验。逐项复核 A/C/E 的既有逐例记录与引文（393 个不同案例），并筛查其他 259 个案例的既有理由与概念；对边界及补充分配查阅相关原文。未重新通读全部 652 篇原文。

本轮将原 A 拆为 A1/A2/A3，C 拆为 C1/C2，E 拆为 E1/E2，其余 8 个 code 保留。分类可重叠，父组不参与分配计数。
新增细分类以至少 30 个案例作为本轮避免碎片化的工作门槛；该门槛不是论文规定。既有 Z 的 8 条证据不足材料保留。
本轮保留全部原始文档、既有逐例理由、限定及引文。边界修正与补充分配详见 assignments.json 的 extensions.refinement_review；历史原值保留在 original_record 等扩展字段中。
提案、维护者陈述、争议与已验证行为须区分；材料涉及某机制不代表已复现缺陷、完成修复或经法律审查确认合规。

## Codebook

| Code | Name | Artifacts |
|---|---|---:|
| PRIVACY-A1 | 隐私选择界面、默认值与拒绝/撤回入口 | 151 |
| PRIVACY-A2 | 同意前门控与隐私选择的实际执行 | 124 |
| PRIVACY-A3 | 同意状态持久化、跨组件传递与审计留证 | 54 |
| PRIVACY-B | 透明告知、文档与信息可达性 | 277 |
| PRIVACY-C1 | 分析、广告与诊断遥测 | 129 |
| PRIVACY-C2 | 功能性数据访问、内容传输与服务间数据边界 | 89 |
| PRIVACY-D | 去标识、最小化与再识别 | 148 |
| PRIVACY-E1 | 留存期限、存储位置与持久化边界 | 101 |
| PRIVACY-E2 | 删除、匿名化清理、访问导出与主体请求流程 | 87 |
| PRIVACY-F | 身份、受众与访问边界 | 137 |
| PRIVACY-G | 安全保护与隐私威胁机制 | 125 |
| PRIVACY-H | 隐私控制可用性与系统兼容 | 294 |
| PRIVACY-I | 治理、责任与需求权衡 | 397 |
| PRIVACY-Y | 反例、争议或归因修正 | 62 |
| PRIVACY-Z | 内容不足或无法定位具体机制 | 8 |

## PRIVACY-A1 — 隐私选择界面、默认值与拒绝/撤回入口

面向用户呈现隐私选择、接受/拒绝/撤回入口、默认值及其可达性；包括隐私选择造成的交互障碍。

**Include:** 同意框、Cookie 横幅、分类选择、隐私设置、明确的默认开启/关闭、不可见或不可操作的选择入口。

**Exclude:** 仅有政策链接用 B；仅有后端执行用 A2；仅有同意状态的保存或交换用 A3。

**Boundary:** 8877 要求同等显著的 Reject，属于 A1；20503 只要求按同意条件加载 tracker，属于 A2。2592 的 Continue 故障仅表明通知/选择入口不可操作，不证明无同意采集。

**Examples:**

- `privacy-issue-8877`: Calypso 的 Cookie 组件只有 Accept and Close，用户要求在爱尔兰监管指引下增加 Reject，且不得用界面诱导接受；意大利用户也要求接受、定制、拒绝三选。该请求以重复关闭并指向 Jetpack issue 2002，但本条没有显示 Reject 已实现、合并或部署，duplicate 标签只能说明讨论被归并。 Evidence: "Add 'Reject' Option / you must give equal prominence to an option which allows the user to ‘reject’ cookies"。限定：归并为重复请求，拒绝功能实现未确认
- `privacy-issue-2259`: 用户称在 SUMO 聚焦隐私通知中用方向键导航无法到达 “opt-out” 链接；唯一评论表示在 3.1 的 Cube 设备上可正常工作，没有确认具体版本或修复。属于隐私控制入口的可达性问题。 Evidence: "impossible, afaict, to hit the \"opt-out\" link / Works for me on 3.1 on Cube."。限定：单点复测正常，未确认修复
- `privacy-issue-14123`: 需求是在注册流程加入“我已阅读并同意隐私政策”的勾选框并附政策链接。评论说明原登录页被移除，需重新决定勾选框放置位置；并指出勾选属 click-wrap（显式同意）而继续使用属 browse-wrap（默示同意），若用户不同意不应强制退出应用，而应回到首页给其再次选择机会；还强调同意框不得预选、也不能以继续使用推定同意。最后一条仍称“新用户详情页还缺这个勾选框”，说明关闭时并未落地。 Evidence: "still need the privacy policy checkbox added to the new user details fragment / You cannot pre-select a consent checkbox"。限定：明确缺失待补

## PRIVACY-A2 — 同意前门控与隐私选择的实际执行

数据处理、请求、权限或功能路径是否遵循隐私选择，以及拒绝或撤回后系统能否按该选择运行。

**Include:** 处理前阻断、opt-in/out 生效、绕过统一门控、禁用后仍发送、隐私设置关闭后功能失效及可选权限约束。

**Exclude:** 单纯出现横幅不证明门控；只保存标志用 A3。提案、残余行为和修复声明均须保留原证据状态。

**Boundary:** 11550 从旁路取得 ID 属于门控绕过；4253 禁止记住身份后生成器失败，是选择与功能执行不兼容，不编码成仍保存身份。

**Examples:**

- `privacy-issue-11550`: Prebid 的 GDPR Enforcement 模块在用户未同意 purpose 4 时不向适配器传 bidRequest.userId/userIdAsEids，但多个适配器仍从 bid.params、bidRequest.crumbs.pubcid、window 对象（Digitrust）或自家身份库等处自行取 ID，等同于绕过统一门控；议题逐一列出 deepintent、lupon、seedingAlliance、gumgum、pubmatic、rubicon、sonobi、platformio、windtalker 等文件位置。后续：QA 在处理、DigiTrust 集成被要求暂停评估破坏性改动、Rubicon 建内部单，IX 辩称其身份库自身已按 TCF/CCPA 取得同意。最终 stale 关闭，无全量修复证据。 Evidence: "Few adapters have been found populating user id values from other sources. / these two objects will not be passed to the adapters if consent is not given"。限定：部分调整进行，整体未验证
- `privacy-issue-20503`: 用户要求：未获同意前不得写 cookie，除网站基本功能所需外一个都不行，必要时宁可整段停用 OWA。维护者建议把 tracker 代码包在检查自设 consent cookie 的条件里，提问者索要示例仅得到“对任何 JS 程序员都很简单”。无内建同意机制，也无示例或验证。 Evidence: "Just wrap the tracker code in a conditional / Not handy but it's trivial for any JavaScript programmer."。限定：原则建议，未给示例
- `privacy-issue-7605`: Netlify CLI 用户在全新安装执行 --telemetry-disable 后仍观察到连接 cli.netlify.com。复现者拦截请求，看到 cli:user_telemetryDisabled 事件与 anonymousId，推测用于清除历史分析数据。维护者先称禁用后不使用遥测，随后承认该调用可能是意外或用于服务端关闭，承诺发布排除该调用的版本。争论还涉及默认开启、同意撤回与服务条款是否能替代明确同意；材料未确认版本已发布。 Evidence: "I ran `netlify --telemetry-disable` on a fresh install (`rm -rf ~/.netlify`) and it connected to `cli.netlify.com`: / \"event\": \"cli:user_telemetryDisabled\""。限定：维护者承诺发布排除调用的版本；发布未确认

## PRIVACY-A3 — 同意状态持久化、跨组件传递与审计留证

隐私偏好或同意状态在存储、账号转换、组件或协议之间的表达、保存、传递、恢复及版本留证。

**Include:** 同意 cookie/localStorage、同意记录字段、匿名到登录迁移、版本重询、GPC/USP/TCF 信号传递及测试中的状态预置。

**Exclude:** 一般业务数据保存用 E1；只有按钮用 A1；状态传递不等于下游已正确执行 A2。没有记录需求时不推定审计机制。

**Boundary:** 8876 匿名与注册状态迁移属于 A3；9894 预置 cookie 是测试状态控制，不是强迫线上用户同意。11297 的 header 透传不证明竞价方已执行拒绝。

**Examples:**

- `privacy-issue-8876`: SAP匿名consents经X-Anonymous-Consents头全量交换并存localStorage，区分未选择、给予、撤回；登录恢复账号同意、注册迁移匿名同意、登出恢复匿名，语言变化不改状态，新版本重新提示。计划披露注册未接后端与SSR限制，主清单含修复、测试、发布、文档均勾选；2022年另有store未加载报错求助，无解决证据。 Evidence: "neither given nor withdrawn / Fix transferring anonymous consents to registered"。限定：主清单完成，后续集成报错未解决
- `privacy-issue-2286`: 用户同意已显示登记却不断再提示，多站复现；原因解释为subject varchar25过短，255及PR修复。后又有两站报告，要求另开issue，不能认定全面解决。 Evidence: "change data type of subject field to varchar(255) / Still happening for me, two different sites."。限定：关联PR关闭，后续仍报告
- `privacy-issue-11297`: 请求GPC优先覆盖USP值并允许publisher配置；咨询法律后暂决定只传header由竞价方处理，服务端另议，另一人建议publisher统一转换，JS不实施所请。 Evidence: "just pass the GPC HTTP header through the system and let bidders deal with it for now. / nothing to do on Prebid.js"。限定：暂不改JS，服务端及发布方另处理

## PRIVACY-B — 透明告知、文档与信息可达性

材料涉及说明收集内容、目的、对象、期限、法律文本、操作路径及其可理解性。

**Include:** 政策发布/翻译、说明准确性、告知入口、数据清单、控制文档及组织对外解释。

**Exclude:** 披露承诺不当作行为已验证；链接未取得不能推其内容。

**Examples:**

- `privacy-issue-21460`: 法文服务条款仍保留英文的隐私法句子，报告者请求翻译并建议 Privacy Act 用标题大小写和斜体；维护者回复已获批准，但未提供发布验证。主题是法律文本的可读性与告知质量，不涉及实际数据流。 Evidence: "Should be translated / \"privacy act\" should be title case and italicized"。限定：文案批准，发布未知
- `privacy-issue-1444`: 任务要求创建订阅服务隐私通知和法律条款页面，并把旧 VPN/Relay 法律页面在指定日期重定向到新页面；正文明确法律内容尚待提供，评论仅给出 legal-docs 源文件链接。成功标准是复选框，没有完成记录，外部链接未读取。 Evidence: "Create new subscription services privacy/legal pages / Legal docs content: still to come"。限定：发布任务，完成状态未知

## PRIVACY-C1 — 分析、广告与诊断遥测

用于使用统计、广告识别、行为追踪、会话回放、异常诊断或运营监测的数据采集与数据流讨论。

**Include:** 分析 SDK、统计 cookie、广告 ID、遥测事件、错误上报、生产日志监测服务及明确的无采集/退出争议。

**Exclude:** 与统计诊断无关的功能请求或内容传播用 C2；不能从通用第三方依赖、cookie 一词或法律标题推断追踪。

**Boundary:** 3845 Mixpanel 事件属于 C1；18441 默认图标的 Referer 请求属于 C2。20527 明确提问 Open Web Analytics 的 cookie，但没有给出用途字段或同意实现。

**Examples:**

- `privacy-issue-3845`: 项目原无追踪，讨论 Google Analytics、Heap、Mixpanel、Fathom 后选择 Mixpanel，记录启动开发服务器、构建、测试等事件。为安装生成并本地保存 UUID，而不是读取 MAC 等设备标识；作者认为不含 PII，但仍承诺补隐私政策。清单显示分析 saga/service 和 Mixpanel 已接好，隐私政策仍未完成。 Evidence: "Right now, Guppy has no tracking at all / we still aren't collecting any personally-identifiable information"。限定：分析已接入，隐私政策未完成
- `privacy-issue-20235`: VSCode 已对异常做脱敏，但 ApplicationInsights 的 trackException 在传入对象不是 Error 时会抛新错误，从而把含 PII 的堆栈带出。维护者提出可加全局 DoNotLogStackTraces 开关（默认 false），最终方案是引入 Telemetry Processor 让调用方在发送前处理全部遥测，称随 v0.15.19 发布。材料只有承诺，无发布后验证。 Evidence: "leaking stack traces that include PII / It is now possible to process all telemetry data"。限定：遥测处理器方案，随版本发布承诺
- `privacy-issue-12161`: tui.image-editor 被指默认向 Google Analytics 发送用户交互，文档未说明。维护者给出 usageStatistics: false 的关闭方式；报告人确认可关闭，但主张应默认关闭并在文档中披露。另一参与者同意默认关闭。issue 因不活跃自动关闭，未见默认值或文档变更。 Evidence: "your library seems to be tracking the user interactions and posting them to your Google Analytics account. / You can add `usageStatistics: false` param to the image editor arguments when you initialize it."。限定：存在关闭参数；默认关闭与文档披露未落地

## PRIVACY-C2 — 功能性数据访问、内容传输与服务间数据边界

围绕应用功能的数据或传感器访问、资源请求、消息内容分发及跨系统传播，关注数据、元信息与接收方边界。

**Include:** 字体/图标/链接预览、IP/Referer、地理位置访问、健康数据共享、推送正文、消息转发、第三方处理与离线替代。

**Exclude:** 只更换供应商许可或部署地点而未说明个人数据流不纳入；单纯同意信号用 A3。明确分析目的另用 C1；同时涉及诊断和服务外发可兼码。

**Boundary:** 18441 Referer、18373 推送正文属于 C2；18429 是本地低精度位置访问用于后台唤醒，不能写成坐标已外发；7448 是潜在联网风险与离线方案，不是已测泄露。

**Examples:**

- `privacy-issue-18441`: 用户报告即使 KML 没有任何点，OpenLayers 仍请求 maps.google.com 的默认图钉图片，且当前地图路径可能含机密数据，会经 Referer 发送给 Google。建议无标记时不请求、无显式图标时使用本地默认图标，并在需要时由样式显式指定 Google 图标。材料只有自动 stale 评论，没有原因确认、代码修改或复测。 Evidence: "OpenLayers is making an unexpected request to https://maps.google.com/mapfiles/kml/pushpin/ylw-pushpin.png / this is getting sent to Google via the Referer header field"。限定：报告外连与 Referer 风险，未见修复
- `privacy-issue-18373`: Synapse 要求推送通知不向 APNS/GCM 发送消息明文，改为唤醒客户端后经 Matrix 取内容并可用 E2E 加密。后续确认 event_id_only 与 include_content 配置可避免明文；维护者解释默认 true 的兼容取舍，并称已足够解决后关闭。 Evidence: "We simply shouldn't be ever sending the plain text of push notifications to APNS or GCM / Setting this to `false` makes Synapse withhold the content"。限定：维护者称已足够解决并关闭；默认值未改
- `privacy-issue-18621`: 最初认为两个收件者显示不同被作者纠正，两者均链接；维护者解释自动HEAD可被独特URL定位且XMPP服务器中转不直接泄露双方IP，拟opt-in显示。最终OSX beta有偏好，iOS待测试移植。 Evidence: "it makes a http head call automatically for every link to check if it is an image."。限定：OSX beta实现，iOS计划中

## PRIVACY-D — 去标识、最小化与再识别

材料涉及减少可识别信息、匿名/假名变换、粒度降低，以及剩余关联风险或保护覆盖。

**Include:** 日志脱敏、哈希与随机映射、时间位置精度、字段遗漏、导出清洗及效果验证。

**Exclude:** 不能把 hash 自动等同匿名；仅删除整账户用 PRIVACY-E2，权利/政策文本仍需 PRIVACY-B。

**Examples:**

- `privacy-issue-943`: 性能分析任务原本怀疑同步与目录查询中的伪名化、DTO 转换是瓶颈；最终结论明确写明伪名化可排除为重要性能影响，主要耗时来自含大量 join 的长 SQL，并拆出两个后续 issue。主题是隐私保护处理与系统性能的权衡。 Evidence: "especially include the pseudonymisation logic because this was already identified as a huge bottleneck / pseudonymization can be ruled out as a relevant impact on performance"。限定：分析完成，后续优化拆单
- `privacy-issue-975`: 社区人员打开个人目录时，辖区外本不应可见的人员没有被伪名化，且过滤列表显示其无权限查看的实体关系；期望是只显示可访问人员，否则进行伪名化，过滤结果也不应暴露不可见关系。评论仅确认在 1.60.0-SNAPSHOT 验证，截图未读取。 Evidence: "persons that the user should not be allowed to see are not pseudonymized / should only see the persons on the directory that they have access to"。限定：QA 验证通过，部署状态未在文本说明

## PRIVACY-E1 — 留存期限、存储位置与持久化边界

业务数据、日志、凭据、缓存或 cookie 保存多久、保存在哪里以及是否持久化的设计与实际边界。

**Include:** 期限与自动过期、超期保留、内存/浏览器/服务端/外部存储、日志与缓存持久化、备份及默认保存策略。

**Exclude:** 同意状态的语义与跨组件传递用 A3；若同时讨论存储介质、保存期限或持久化策略可兼 E1。具体清除、删除、访问或导出流程用 E2；可见性变更不等于留存变化。

**Boundary:** 3873 日志 14 天建议与3998 通道 24 小时留存属于 E1；20437 期限可配置不确立统一法律上限；18902 本地 SD 卡存储不等于数据已离开设备。

**Examples:**

- `privacy-issue-3873`: Wellcome 平台指出 ALB/CloudFront 日志含用户 IP，按 DPA/GDPR 属个人数据，建议约 14 天自动过期，因为团队很少查看。材料只有明确留存任务，没有过期策略部署或删除验证。 Evidence: "They include user IP addresses, which count as personally identifiable information / We should auto-expire them after 14 days or similar"。限定：留存期限要求，实施未证
- `privacy-issue-3998`: 用户要求含 PII 的消息不得落在任何微软库中，因此自建 BotState；但通过 DirectLine 取消息时其代码不被调用，消息仍能取到，怀疑被 Hub 存储。维护者澄清 bot state API 只存机器人内部跟踪信息，DirectLine 是通道，用加密的 Azure 表存储做“存储转发”以便客户端随时拉取，不使用 bot state；其他通道只做代理不存储。留存量先被猜成 7 天，后明确为 24 小时，并称已收到缩短/取消的请求在评估。用户表示 24 小时也无法接受，考虑自写 connector 绕过。最终以“新功能方向不适合留在 GitHub”关闭。 Evidence: "Data retention in Direct Line is 24 hours / It does not use the bot state api."。限定：解释24小时保留，配置能力未实现
- `privacy-issue-18902`: OsmAnd 把 XML 配置档（家/工作地点、收藏、轨迹、历史）与地图存在同一外部 SD 卡目录，若为 FAT32 可拔卡读取，提出把隐私数据留内部存储并可分别选择路径。维护者承认问题存在但反对，称数据未离开设备故与 GDPR 无关、责任在机主，且 Android 7 起应用无权读整卡；提议者反驳本地存储同样受隐私法约束，并质疑“地图位置”与“个人数据”被强制绑定。无实现。 Evidence: "Even though the issue you describe exists / keep privacy-related information in internal storage"。限定：方案遭反对，无分离实现

## PRIVACY-E2 — 删除、匿名化清理、访问导出与主体请求流程

围绕清除、遗忘、去关联、主体访问或导出副本的操作流程、范围、限制及跨副本传播。

**Include:** 账户/消息/cookie/cache 删除、卸载清理、匿名化代替删除、redaction 残留、下载数据、主体访问与删除请求。

**Exclude:** 一般字段脱敏和再识别用 D；只有保存时间/位置用 E1；界面隐藏和停用不能自动视为删除。

**Boundary:** 2958 同时下载与关户属于 E2；13934 明确 redaction 后数据库仍留内容，必须保留删除不完整的限定；18464 搜索可见性不属于删除。

**Examples:**

- `privacy-issue-2958`: 任务要求用户可自行关闭账户并清除私密信息，清单包括设置入口、删除页、反馈、删除前下载数据，以及移除邮箱、密码、用户名、生日和邮编；讨论区分可保留的共享邮编记录与必须删除的用户引用，最终评论称完成。 Evidence: "allow them to remove their private information and close their account / Suggest that the user download their data before they delete their account"。限定：标记完成，未运行删除流程验证
- `privacy-issue-13934`: 圣诞期间 FN spambot 攻击后出现大量批量 redaction 需求，并认为 GDPR 也需要。当前范围定为 redact all messages from this user，另一议题负责多选消息。评论警告：redaction 只是替换事件内容，事件内容仍留在数据库，因此不等于彻底删除，并链接 Synapse 相关讨论。2018 年补充关联的 GDPR 议题与 riot-web 议题。2022 年有人追问进展，答复参见 matrix-spec-proposals PR #2244，并因该规范 PR 已落地而把议题转到 element-meta#920 关闭。规范层推进，本仓库功能完成情况未验证。 Evidence: "event content still stays in database after redaction. / redact all messages from this user"。限定：规范推进并转移跟踪；删除后数据残留问题未解
- `privacy-issue-6881`: Firebase 请求暴露清除 IndexedDB 离线持久化的 API。维护者说明持久化假设 OS 用户即实际用户，不适合共享账户；安全规则不能充当本地缓存过滤器；手工改 IndexedDB 可能破坏缓存。垃圾回收在 5.7.0，clearPersistence() 在 v6.2.0 发布。属本地留存与生命周期控制，并有明确残余风险说明。 Evidence: "Expose API to clear offline persistence (in IndexedDB). / clearPersistence()"。限定：clearPersistence 在 v6.2.0 发布；共享账户风险未消除

## PRIVACY-F — 身份、受众与访问边界

材料涉及谁能识别谁、谁能访问哪些信息，以及跨用户/角色/实例/视图的边界。

**Include:** 角色权限、资料可见性、账户关联、行为状态、消息受众、共享设备及公开索引。

**Exclude:** 不把不猜得到的 URL 当身份授权；本地保存也可能暴露给本地管理员或旁观者。

**Examples:**

- `privacy-issue-21543`: 请求新增管理员修改用户密码功能，用于帮助无法登录的用户；讨论者指出这会带来管理员接触账户凭据、模拟用户访问和未经同意干预的风险。维护者最终拒绝管理员改密能力，认为真正的问题是找回密码流程，并关闭本条。材料没有证明找回流程修复已完成。 Evidence: "no field that enable to change the user password / directly access/simulate access to a user account without his consent is questionable"。限定：功能请求拒绝，转查找回密码故障
- `privacy-issue-975`: 社区人员打开个人目录时，辖区外本不应可见的人员没有被伪名化，且过滤列表显示其无权限查看的实体关系；期望是只显示可访问人员，否则进行伪名化，过滤结果也不应暴露不可见关系。评论仅确认在 1.60.0-SNAPSHOT 验证，截图未读取。 Evidence: "persons that the user should not be allowed to see are not pseudonymized / should only see the persons on the directory that they have access to"。限定：QA 验证通过，部署状态未在文本说明

## PRIVACY-G — 安全保护与隐私威胁机制

材料以具体攻击、故障、加密、认证、权限、反指纹或通信机制讨论信息保护。

**Include:** 凭据泄露、异常路径污染、传输/静态加密、密钥、认证、权限声明、威胁模型及误报。

**Exclude:** 必须区分假设、报告、复现和反驳；安全相关标题不证明发生泄露。

**Examples:**

- `privacy-issue-352`: 完整阅读恶意属性载荷与三条评论。问题根因是用户可控属性被 html_safe 且自动链接；维护者先考虑取消自动链接，随后接受先转义输入、再保留自动链接的方案，但文本没有部署或验证记录。payload 中的 document.cookie 只是攻击示例，不能据此归为 Cookie 同意问题。 Evidence: "XSS through `.html_safe`-ing attributes / escapes the input beforehand"。限定：修复方案获维护者认可，部署未从文本确认
- `privacy-issue-21543`: 请求新增管理员修改用户密码功能，用于帮助无法登录的用户；讨论者指出这会带来管理员接触账户凭据、模拟用户访问和未经同意干预的风险。维护者最终拒绝管理员改密能力，认为真正的问题是找回密码流程，并关闭本条。材料没有证明找回流程修复已完成。 Evidence: "no field that enable to change the user password / directly access/simulate access to a user account without his consent is questionable"。限定：功能请求拒绝，转查找回密码故障

## PRIVACY-H — 隐私控制可用性与系统兼容

材料涉及控制能否被理解和操作，或隐私保护与框架、平台、功能、数据流之间的适配。

**Include:** 界面遮挡、可访问性、配置绕行、跨端状态、隐私开关功能副作用、测试与依赖集成。

**Exclude:** UI 测试成功不保证后端阻断；功能兼容问题不能一概视为隐私泄漏。

**Examples:**

- `privacy-issue-310`: 提案新增 :RemoveCookies，用正则按域名删除一个或多个域下的 Cookie；作者明确承认新增 cookies 权限会促使用户重新批准扩展，但材料没有实现、合并或部署证据。 Evidence: "remove cookies from a specific domain or from multiple domains / we would have to grant the `cookies` permission"。限定：功能提案，未见实施证据
- `privacy-issue-1957`: 用户询问扩展更新为何请求访问隐私设置；维护者解释该权限只用于读取并显示 privacy.resistFingerprinting 的提示，不写入隐私设置，且平台不允许把该权限设为可选。这是权限范围与用户可理解性的问题，代码搜索链接未读取。 Evidence: "required access to my privacy settings / needed to display the notice for privacy.resistFingerprinting"。限定：权限用途获解释，未独立验证代码

## PRIVACY-I — 治理、责任与需求权衡

材料涉及合规解释、组织职责、开发范围、生态依赖、资源优先级或用途与隐私的取舍。

**Include:** 监管/平台审核驱动、控制者/供应商分工、请求受理、评估、标准与开发决策。

**Exclude:** 记录参与者法律判断而不认证其正确；计划、合并、部署、验收分别处理。

**Examples:**

- `privacy-issue-8387`: 请求为 DNN 门户增加 Cookie 同意消息，使站点符合 GDPR 的 Cookie 规则；讨论同时包含欧盟监管与 ePrivacy 指令是否明确的判断。后续关联 issue/PR 被合并并据此关闭，但本条没有部署或实际同意流程细节。 Evidence: "have to have a cookie consent form added to the site / compliant with GDPR Cookie regulatory rules"。限定：关联 PR 已合并，部署未验证
- `privacy-issue-21474`: 讨论用 db-ip.com 替代 MaxMind 的 GeoLite 数据库，以减少供应商登录/许可限制并保持 IP 地理位置能力。维护者说明 MaxMind 的账户要求是外部政策变化，建议未来按安装来源模块化并更新页面归属说明；本条没有确认实际切换或数据发送变化，且部分评论缺失。 Evidence: "can we use db-ip.com instead of maxmind.com / behind a login-wall"。限定：讨论与设计方向，实施未知

## PRIVACY-Y — 反例、争议或归因修正

完整材料削弱、反驳或限定了最初隐私问题判断，或显示原风险归因/目标发生改变。

**Include:** 误报、用户撤回、无外发证据、实际行为不同、争议未定及保护并未达原目标。

**Exclude:** 不是统一的无风险标签；仍可并存真实残余风险，具体原因见备忘录。

**Examples:**

- `privacy-issue-1154`: 报告者担心启用 UserId 伪名化后 visitorId 仍会间接泄露 UserId；维护者解释 privacy manager 的 manipulateRequest 在生成 visitorId 前执行，因此 visitorId 基于已哈希的 UserId 生成，原问题不成立。文本只给出机制解释，没有外部代码复核。 Evidence: "the visitorId would still kind of leak the userId / `manipulateRequest` in privacy manager \"request processor\" is executed before getting the visitor Id."。限定：维护者解释后按 worksforme 关闭
- `privacy-issue-2664`: 提出者担心德国及欧洲法律要求 imprint、外链免责声明并讨论 Cookie；回复者依据 TMG/RStV 论证非商业、纯个人静态信息站不需要 imprint，免责声明往往无效，站点无 Cookie 代码且只产生合法服务器日志，因此也无需隐私说明。结论是当前形态无需新增，网站性质变化时再议。 Evidence: "This website does not need an imprint in its current form / There is no code that could even create cookies"。限定：按当前静态站性质判定无需新增

## PRIVACY-Z — 内容不足或无法定位具体机制

可用材料不足以支持任何具体隐私机制，或仅有无法还原语境的外链、占位文本与泛化标题。

**Include:** 空正文、只有外链/占位符、标题也无法定位隐私机制，以及现有讨论未提供可归因对象或行为的条目。

**Exclude:** 正文可读但隐私关联较弱时，应按实际涉及的主题编码；证据可用性是独立字段，不应仅靠 PRIVACY-Z 表达。

**Examples:**

- `privacy-issue-1830`: 正文只有一句“à la”加一个 mozilla/legal-docs PR 链接，没有可读的隐私通知内容、处理活动或实施说明；无评论，外部 PR 未读取，无法定位具体机制。 Evidence: "à la https://github.com/mozilla/legal-docs/pull/1021/files"。限定：内容不足，无法判断
- `privacy-issue-11387`: 正文只有占位反馈，评论要求说明具体缺什么后关闭；无法确定具体法律文本或数据机制。 Evidence: "[Enter feedback here] / Could you please clarify what exactly is missing or needs modification"。限定：证据缺失，结果未知

## Original scope qualifications

Coverage refers to all supplied textual sections, not all content ever linked on the web.
Source revision ambiguity, inaccessible context, tentative proposals and absence of execution evidence remain in individual scope notes.
Coding is assistant-authored; it is not published human annotation, independently validated ground truth, or an experimental system run.
All artifacts are included; unspecified work and comments without established outstanding work are retained explicitly rather than invented as defects.
