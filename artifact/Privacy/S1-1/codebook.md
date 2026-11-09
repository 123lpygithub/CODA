# Privacy — S1-1

652 artifacts; 21 codes; 2435 artifact–code assignments.

Second analyst-authored refinement of the existing Privacy S1-1 analysis. Individually review all 511 distinct case notes assigned to B/D/F/G, including rationales, concepts, scope notes and quotations; screen the remaining 141 case notes, and check source text for boundaries and added memberships. Explicit case-ID decisions split B/D/F/G into ten codes; scripts only serialize decisions and validate evidence and format.

## Refinement scope

本轮继续细化已有分析：逐项阅读 B/D/F/G 涉及的 511 个不同案例的既有理由、概念、限定与引文，筛查其余 141 个案例的既有记录，并对边界、补充分配及代表例核对相关原文。未重新通读全部 652 篇原文；这不是新一轮独立编码实验。

初始 11 类先将 A/C/E 细化到 15 类；本轮再将 B/D/F/G 细化，形成 21 个可分配 code。H/I/Y/Z 保留。父组只用于 taxonomy，不重复分配。

本轮 10 个细分类均至少有 30 条材料；30 是本轮避免碎片化的工作门槛，不是论文规定。类别可重叠，材料数不应跨类别直接求和作为独立样本数。既有 Z 的 8 条证据不足材料继续保留。

所有原文、既有逐例理由、证据与限定保留。当前修订见 assignments.json 的 extensions.refinement_review；上一轮修订见 refinement_history，原始编码见 original_record。历史字段不代表当前分配。

按实际机制修订边界，不因出现隐私法律或个人数据就自动纳入某类。提案、单方主张、已实现声明、测试与部署证据分别保留；分类不等于确认缺陷或法律合规。

## Codebook

| Code | Name | Artifacts |
|---|---|---:|
| PRIVACY-A1 | 隐私选择界面、默认值与拒绝/撤回入口 | 151 |
| PRIVACY-A2 | 同意前门控与隐私选择的实际执行 | 124 |
| PRIVACY-A3 | 同意状态持久化、跨组件传递与审计留证 | 54 |
| PRIVACY-B1 | 隐私政策与法律告知内容的建立和维护 | 82 |
| PRIVACY-B2 | 隐私告知入口、呈现、本地化与可访问性 | 115 |
| PRIVACY-B3 | 数据处理、隐私控制与风险的技术说明 | 193 |
| PRIVACY-C1 | 分析、广告与诊断遥测 | 129 |
| PRIVACY-C2 | 功能性数据访问、内容传输与服务间数据边界 | 89 |
| PRIVACY-D1 | 假名替换、哈希、扰动与精度降低 | 66 |
| PRIVACY-D2 | 字段、元数据与采集范围最小化 | 87 |
| PRIVACY-D3 | 去标识覆盖、执行质量与再识别边界 | 100 |
| PRIVACY-E1 | 留存期限、存储位置与持久化边界 | 101 |
| PRIVACY-E2 | 删除、匿名化清理、访问导出与主体请求流程 | 87 |
| PRIVACY-F1 | 角色、受众、租户与跨组件访问隔离 | 86 |
| PRIVACY-F2 | 身份关联、存在性暴露与行为可推断性 | 69 |
| PRIVACY-G1 | 加密、密钥与通信或存储的密码学保护 | 38 |
| PRIVACY-G2 | 认证、权限、攻击防护与意外披露控制 | 103 |
| PRIVACY-H | 隐私控制可用性与系统兼容 | 294 |
| PRIVACY-I | 治理、责任与需求权衡 | 397 |
| PRIVACY-Y | 反例、争议或归因修正 | 62 |
| PRIVACY-Z | 内容不足或无法定位具体机制 | 8 |

## PRIVACY-A1 — 隐私选择界面、默认值与拒绝/撤回入口

面向用户呈现隐私选择、接受/拒绝/撤回入口、默认值及其可达性；包括隐私选择造成的交互障碍。

**Include:** 同意框、Cookie 横幅、分类选择、隐私设置、明确的默认开启/关闭、不可见或不可操作的选择入口。

**Exclude:** 仅有政策链接用 B2；仅有后端执行用 A2；仅有同意状态的保存或交换用 A3。

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

## PRIVACY-B1 — 隐私政策与法律告知内容的建立和维护

围绕隐私声明、Cookie 政策、条款及相关法律告知文本的缺失、起草、修订、版本来源、模板适配和维护归属开展工作。

**Include:** 创建/更新/定稿政策文本、核对法律实体与法规名称、从 legal-docs 维护副本、按实例配置政策内容、声明与实际实践同步。

**Exclude:** 仅有链接失效、布局、语言呈现或部署入口用 B2；解释具体数据行为或配置用 B3。B1 不证明政策承诺已实现。

**Boundary:** 14169 政策修订部署属于 B1，且作者承认处理清单有猜测；2406 只修 ICO 链接用 B2。14157/14160 暂停一般网站翻译仅属治理 I，不推定为隐私告知维护。

**Examples:**

- `privacy-issue-14169`: mySociety按GDPR修订隐私政策，作者承认部分收集与用途描述是educated guess，并邀请研究、传播团队核查；随后给出PR并明确已合并部署。外部员工文档未读取，不能声称处理清单已核对正确。 Evidence: "merged and deployed now"。限定：合并并部署，处理清单未独立核对
- `privacy-issue-21583`: 针对 WhatDoTheyKnow 隐私页开头“WhatDoTheyKnow is run by the charity mySociety: see more details here”提出改写，希望明确 mySociety 与 UK Citizens Online Democracy 的慈善关系，并链接到 Who makes WhatDoTheyKnow 页面以获取结构、治理及在信息专员办公室与慈善委员会的注册信息。评论一指出页面的 “General Data Protection Act” 应为 “General Data Protection Regulations”（法规名纠错）。评论二转达 Mark C 的意见：首行应改为“WhatDoTheyKnow is run by mySociety, a project of the charity UK Citizens Online Democracy.” 全部为文案提案，未见合并、上线或页面现状核对。 Evidence: "WhatDoTheyKnow is run by mySociety, a project of the charity UK Citizens Online Democracy."。限定：文案修订提案（无实施确认）
- `privacy-issue-7376`: Codebuddies缺privacy路由，贡献者贴出生成器政策全文并建templates/other/privacy.html模板，涵盖姓名邮箱用途、不追踪cookie/DNT、第三方例外、未成年营销、7工作日泄露告知与退订；但其自述问卷答案未知，页面路由与声明行为均未验证。 Evidence: "A lot of questions to answer and I don't know all the answers myself. / We do not use cookies for tracking purposes."。限定：政策文本与模板提供，部署未知

## PRIVACY-B2 — 隐私告知入口、呈现、本地化与可访问性

隐私通知、政策或 Cookie/同意告知能否在正确位置、语言、地区与平台被访问、显示和操作，以及相关页面的发布与接入。

**Include:** 页脚/注册页/应用商店链接、横幅与弹窗呈现、语言翻译、文本裁剪、屏幕阅读器、链接路由、告知页面发布与跨平台集成。

**Exclude:** 一般网站翻译不自动属于隐私告知；单纯后台机制或配置文档用 B3；仅有选择按钮而未涉及告知载体时用 A1。B2 可与 A1 同时出现。

**Boundary:** 8890 的 NVDA 横幅可访问性属于 B2；14123 隐私政策勾选框兼 A1/B2，但界面存在不证明 A2 门控生效。

**Examples:**

- `privacy-issue-1665`: 订阅设置与确认页的 “Privacy Notice” 链接标签在法语、德语、西班牙语、意大利语、荷兰语环境中仍显示英文，虽然点入后的通知正文是用户语言。修复后维护者在 Train 1.230.2 staging 复验标签已本地化；截图与 Jira 附件未读取。 Evidence: "label link is displayed in English, regardless of the user language / the Privacy Notice page is displayed in the user language"。限定：staging 复验已修复，生产部署未说明
- `privacy-issue-2406`: 报告隐私政策和各隐私通知中的 ICO 链接失效，要求统一改为 https://ico.org.uk/concerns/。无评论，未提供修复或部署确认。 Evidence: "There's a broken link on the privacy policy and each privacy notice. / https://ico.org.uk/concerns/"。限定：链接更新请求，完成未知
- `privacy-issue-8890`: Ubuntu cookie横幅在Firefox下NVDA不读，Chrome可用，导致盲人难以访问；维护者复现并关联cookie-policy的123修复，随后维护者与原报告者均确认横幅可被NVDA访问。 Evidence: "the cookie dialog now can be easily accessed by NVDA"。限定：修复并获原报告者复验

## PRIVACY-B3 — 数据处理、隐私控制与风险的技术说明

对具体收集字段、用途、数据流、保留、隐私控制、能力边界或威胁作技术解释、文档化、风险告知或真实性核对。

**Include:** 实际发送/保存内容说明、默认值与开关语义、配置和 API 指引、第三方数据处理披露、风险警示、诊断材料分享说明与处理清单。

**Exclude:** 不把所有技术讨论自动算透明告知；仅有法规目标或泛化合规咨询仍用 I/Z。仅修链接或排版用 B2；政策整体建立维护另用 B1。

**Boundary:** 4216 解释策略未配置与启用后下拉框默认值的区别；3942 更新日志手机号位数文档，不代表脱敏策略改进；18560 仍未验证实际外连。

**Examples:**

- `privacy-issue-4216`: 报告指出 Microsoft 365 文档称未配置诊断数据策略时“可选和必需诊断数据都会发送”，而 ADMX 表显示默认 Neither。维护者解释 Neither 是选择 Enable 后下拉框的默认值；策略若 Disabled/Not Configured 则不创建注册表项，因此两处描述并不矛盾。截图/附件未读取，证据状态为 partial。 Evidence: "both optional and required diagnostic data are sent to Microsoft / the default setting is `Neither`"。限定：文档差异获解释，无代码变更
- `privacy-issue-3942`: Signal Desktop 0.30.0 的调试日志在上报 URL 中保留联系人手机号后三位（如 /v1/messages/+[REDACTED]123），而 Signal Android wiki 声明只显示后两位，桌面端 wiki 当时为空。报告者按“三点菜单 → Submit debug log”复现，并说明 Android 上确为两位。额外指出提交日志 UI 只说会公开张贴、却未说明张贴到哪里、如何编辑，容易让非技术用户误以为点击后还能再编辑，整体让人不敢轻易提交。维护者确认三位是设计、是文档写错，会更新文档；随后另一贡献者确认已更新该 wiki。日志脱敏程度与提交流程本身未改。 Evidence: "The three digits is by design, and we'll go update that documentation. / I have updated the mentioned wiki."。限定：文档纠正；三位脱敏按设计保留
- `privacy-issue-20596`: 需求是为会写 cookie 的两个包补充说明：在 README 写清所用 cookie 及用途，并在代码里加简短注释，帮助使用方判断是否需要向终端用户告知。作者说明实际只设一个存 AuthenticationProperties 的状态 cookie（默认名 __ActiveLogin.BankIdState / __ActiveLogin.GrandIdState，可改），其中含 RedirectUri 等，并有一个可被使用方写入任意数据的 Items 属性包。评论引欧盟指南“会话期认证 cookie 一般无需同意”，并指出若使用方在 Items 里放敏感数据责任在其自身。作者澄清目标是给开发者文档、不是给终端用户弹窗，并认可认证 cookie 可能属豁免。无文档是否合并的证据。 Evidence: "rather explain what our cookies do for developers / Authentication cookies, for the duration of a session"。限定：澄清文档范围，完成未证

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

## PRIVACY-D1 — 假名替换、哈希、扰动与精度降低

通过替换、哈希、映射、随机化、聚合或降低精度改变标识与可识别属性，同时保留部分使用价值。

**Include:** 用户/IP 假名、随机 UUID、姓名假数据替换、IP 截断、坐标/日期降精度、计数随机化、音频或 OS 指纹伪造。

**Exclude:** 直接省略或停止收集字段用 D2；运行失败、漏字段、强度/可逆性与再识别评估另用 D3。可逆加密属于 G1，不自动归去标识。

**Boundary:** 4866 网格吸附是降精度，不是随机化；1019 指纹哈希不等于匿名化，兼 D3；3871 可逆字段加密仅归 G1 等保留类别。

**Examples:**

- `privacy-issue-4866`: 要求API也遮蔽坐标，已有匿名/精度功能获认可；后续澄清为网格吸附非随机，4级约100m可能过精确，统一尺度不适混合密度；动态方案进入UX待办。 Evidence: "The function is not a randomiser / snaps the coordinates to the nearest intersection point in a grid"。限定：基本功能已有，适应密度改进待办
- `privacy-issue-4842`: #1287 的后续：在匿名化时打乱评教结果。动机是拥有生产权限者可能在匿名化数据里识别未发布课程（少于两名参与者投票才不发布），并借其他课程的答案分布反推，从而去匿名化贡献者姓名；因此决定匿名化时随机化答案计数，同时要求每题答案总数大致不变，且任何一项计数不得超过该课程投票人数。讨论给出两版实现：一是先汇总答案总数，再按 RatingAnswerCounters 逐个取 0 到剩余数的随机值分配，实现简单但对靠前的计数项系统性偏高；二是先给每项一个 0..票数的随机数，再按因子缩放回原总数并均匀分摊误差，分布更均匀但需额外清理。正文无评论，无实现或合并证据。 Evidence: "it is better to randomize answers / answer counters should be set randomly on anonymization."。限定：方案设计讨论（两版实现取舍），无实现证据
- `privacy-issue-4603`: SmartNoise 提议新增匿名化 transformer：用户传入按字段生成假数据的函数或 Faker provider，变换时清洗真实 PII，反向变换时生成假值。维护者建议派生 ColumnTransformer，并讨论训练集不应学习假 PII、单列 PII 的 1→n/ n→1 变换以及返回 None 的处理。作者随后称 AnonymizationTransformer 已实现、测试并合并，TableTransformer 使用测试和 PII 推断也完成，最后修复文档构建。该实现降低可识别性，但材料没有给出匿名性证明或再识别评估。 Evidence: "The `AnonymizationTransformer` itself is implemented, tested and merged. / Thanks @joshua-oss for implementing the tests and basic PII inference in #515."。限定：组件与集成测试已合并，文档已修复

## PRIVACY-D2 — 字段、元数据与采集范围最小化

通过不收集、不保存、不发送、过滤或移除非必要数据字段、内容或元信息来减少数据暴露。

**Include:** 日志/遥测字段清理、EXIF/URL/凭据去除、只保留必要字段、缩小位置或传感器采集范围、避免新增身份存储与最小权限设计。

**Exclude:** 假名或扰动算法用 D1；专门的主体删除或生命周期流程用 E2，可同时注明字段最小化。仅加密或身份认证不等于最小化。

**Boundary:** 15030 默认删除非方向 EXIF 属于 D2；4389 只讨论 2FA，移除旧 D；18391 不记录 IP 是最小化声明，不是接收方完全未见 IP 的证明。

**Examples:**

- `privacy-issue-15030`: 报告称 Signal iOS 2.10.1 发送图片时保留 EXIF 与精确 GPS，要求至少移除位置。讨论指出 Android 仅因缩放偶然清除，iOS 用 PHAsset 保留原始数据；维护者提出在 SignalAttachment 统一处理，先增加可选移除，随后提交改为默认始终移除除方向外的元数据。2020 年评论用提交与源码确认功能存在，但开发团队多年未显式更新或关闭 issue，最终由 stale bot 关闭；材料同时有“已默认清除”的代码证据和“缺少正式验收”的治理缺口。 Evidence: "Signal for iOS includes EXIF data in sent images, including precise GPS data if present. / We'd consider a PR which strips out non-orientation exif metadata by default"。限定：默认元数据清除已由提交/源码支持，issue 由 stale bot 关闭
- `privacy-issue-14209`: saproto清单停止保存国籍与性别、删除用户自填学习史、保留UT提供的学习史并每半年邮件核对联系方式；评论称隐私政策已更新、邮件已排期。并非一概删除学习历史。 Evidence: "persistently save the study (history) provided by the UT / Privacy policy updated and e-mail scheduled."。限定：清单与政策完成，邮件已排期
- `privacy-issue-3074`: 税务法院要求避免日志泄露可冒用身份的凭据，验收包括不记录 JWT、明确允许记录的用户字段、发往 AWS 外服务的数据不含 PII。评论先讨论日志字段规范，后缩小到 access token 与 Authorization bearer token；最终称过滤已实现，且法院环境不向 Honeybadger 等外部服务发送数据，票据完成。AWS token 等剩余问题在另一票据。 Evidence: "Ensure user secrets are not logged. / JWT tokens are not logged."。限定：访问令牌与 bearer token 过滤已实现；票据完成

## PRIVACY-D3 — 去标识覆盖、执行质量与再识别边界

围绕去标识能否正确执行、覆盖全部字段/格式/副本、维持数据结构或效用，以及残余可识别性、关联攻击和保护声明的适用边界展开评估。

**Include:** 漏字段/格式/嵌套/临时文件、工具配置或运行失败、脱敏验证、可逆推哈希、组合识别、算法强度/适用性、性能与效用取舍。

**Exclude:** 只描述转换或字段移除且没有质量/覆盖/识别边界讨论时用 D1/D2；一般隐私争议不自动归 D3；仅同意或删除失败仍按 A/E。

**Boundary:** 5005 开启匿名 IP 后 headers 仍留完整 IP，兼 D1/D3；11947 搜索建议与历史删除争议未说明去标识机制，归保留的 E/Y/H，不延续旧 D。

**Examples:**

- `privacy-issue-5005`: 打开匿名IP后X-Forwarded-For及X-Real-Ip仍保留全IP；维护者认可两处都应处理并报告修复，待下个tag发布。 Evidence: "We should do anonymization for both. / Fixed. Will be released in the next tag."。限定：修复声明，发布待后续
- `privacy-issue-974`: Twitter NDJSON未被CSV既有假名化覆盖；PR递归字典按作者字段应用同一hash，最后明确Fixed in151。hash假名化不等于不可重识别匿名。 Evidence: "uses the same hash function for pseudonymization"。限定：报告修复
- `privacy-issue-3902`: DCAF患者结束服务后删电话姓名等但保留报告与重复服务关联；指出公开电话加公开算法可逆推身份，讨论secret salt、年龄分段、字段组合复核和清除audit日志。期限从120天到已履约30天/未履约约120天讨论，最终仅计划推进，未证部署匿名化。 Evidence: "If a person knew someone's phone number they could apply the archive ID-scramble process / We definitely need a second pass to see if our combination of data becomes identifiable."。限定：设计推进，最终实现未证

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

**Exclude:** 一般字段脱敏和再识别用 D1/D2/D3；只有保存时间/位置用 E1；界面隐藏和停用不能自动视为删除。

**Boundary:** 2958 同时下载与关户属于 E2；13934 明确 redaction 后数据库仍留内容，必须保留删除不完整的限定；18464 搜索可见性不属于删除。

**Examples:**

- `privacy-issue-2958`: 任务要求用户可自行关闭账户并清除私密信息，清单包括设置入口、删除页、反馈、删除前下载数据，以及移除邮箱、密码、用户名、生日和邮编；讨论区分可保留的共享邮编记录与必须删除的用户引用，最终评论称完成。 Evidence: "allow them to remove their private information and close their account / Suggest that the user download their data before they delete their account"。限定：标记完成，未运行删除流程验证
- `privacy-issue-13934`: 圣诞期间 FN spambot 攻击后出现大量批量 redaction 需求，并认为 GDPR 也需要。当前范围定为 redact all messages from this user，另一议题负责多选消息。评论警告：redaction 只是替换事件内容，事件内容仍留在数据库，因此不等于彻底删除，并链接 Synapse 相关讨论。2018 年补充关联的 GDPR 议题与 riot-web 议题。2022 年有人追问进展，答复参见 matrix-spec-proposals PR #2244，并因该规范 PR 已落地而把议题转到 element-meta#920 关闭。规范层推进，本仓库功能完成情况未验证。 Evidence: "event content still stays in database after redaction. / redact all messages from this user"。限定：规范推进并转移跟踪；删除后数据残留问题未解
- `privacy-issue-6881`: Firebase 请求暴露清除 IndexedDB 离线持久化的 API。维护者说明持久化假设 OS 用户即实际用户，不适合共享账户；安全规则不能充当本地缓存过滤器；手工改 IndexedDB 可能破坏缓存。垃圾回收在 5.7.0，clearPersistence() 在 v6.2.0 发布。属本地留存与生命周期控制，并有明确残余风险说明。 Evidence: "Expose API to clear offline persistence (in IndexedDB). / clearPersistence()"。限定：clearPersistence 在 v6.2.0 发布；共享账户风险未消除

## PRIVACY-F1 — 角色、受众、租户与跨组件访问隔离

谁可以看到、取得、修改或接收数据，以及角色、群组、实例、设备、视图或输出目标之间的权限和受众隔离。

**Include:** 字段/资料可见性、管理员权限、跨用户内容泄露、私密群组、联邦受众、通知/导出目标、访问角色盘点和凭据使用目标。

**Exclude:** 身份存在性、资料关联和行为推断用 F2；纯存储位置或网络连接选择不自动归 F1。隐藏界面、随机 URL 或公开链接不等于有效授权。

**Boundary:** 18418 随机文件 URL 不等于授权；12082 退群后桌面仍接收是受众隔离问题；8869 仅按钮遮挡，无访问授权机制，保留 A1/H。

**Examples:**

- `privacy-issue-20221`: Ushahidi为发布核验帖子隐藏PII；起初按字段角色后改private开关，仅能编辑整帖者能见私有字段，不支持部分编辑；提交仍可填。hide author隐藏署名，非新增采集。QA修私有照片及管理员不可见等，最终确认私有字段正常；tasks改sections未采纳。 Evidence: "Private fields work perfectly / this is not field level permissions, it's more field level locking."。限定：私有字段测试通过关闭
- `privacy-issue-12082`: Signal移动端退群后桌面端仍显示群并可收发，重新加入再退出仍复现；另一组成员证实已离群数月者持续在桌面收消息，界面不提示其仍在受众中。维护者怀疑离组通知未到所有设备，索要关键时刻日志并建议用正确成员设备改群名广播状态，最终不活跃关闭，无修复验证。 Evidence: "fourth member who left the group months ago has continued receiving / closed due to inactivity"。限定：疑因与绕过建议，未修复验证
- `privacy-issue-18418`: Sensei测验上传进公共媒体库可直链访问；维护者承认非意图转bug，提随机URL混淆，无实施时间；随机不可猜不能等同身份授权，闭合状态不证修复。 Evidence: "all files uploaded by learners as quiz answers, are stored in the media library / Our proposed solution is to obfuscate the file url with a random string"。限定：承认问题并提出混淆，未证实施

## PRIVACY-F2 — 身份关联、存在性暴露与行为可推断性

身份、账号、设备或行为记录如何被关联、枚举或呈现给观察者，包括资料合并、活动状态、公开索引和本地历史带来的识别风险。

**Include:** 邮箱/订单/账号绑定、匿名资料与署名、账户枚举、行为状态和已读回执、公开索引、共享终端历史、稳定客户端标识与活动关联。

**Exclude:** 一般角色权限用 F1；单纯浏览器存储适配用 E1/H；仅与个人数据相关但没有关联或推断机制时不纳入。算法去标识另用 D。

**Boundary:** 11975 即使只返回地址存在的布尔值，也可能被用来枚举账号；12278 最终拒绝旧订单自动关联；3976 仅替换 userStore，没有身份关系或受众变更。

**Examples:**

- `privacy-issue-11975`: 多用户可设他人联系方式引spam，唯一约束又可抢占地址；显示谁使用被批隐私泄露，即使布尔也可能枚举账户。最终提按现有destination主键回布尔，不显示身份；无实现确认。 Evidence: "could still be a breach of privacy / simply returns a boolean"。限定：缩减披露的设计共识
- `privacy-issue-12278`: OFN最初设想确认邮箱后把旧guest订单关联新用户但用户不可见，争论邮箱拼错、地址转让或虚构以及商家重复记录；最终决定完全不关联旧guest与新账号，只以guest标签区分身份并另开2338。不能按初始正文写成自动合并已实施。 Evidence: "final decision is to not associate old guest orders / two different identities"。限定：决定不关联，标签另项
- `privacy-issue-18388`: 用户称隐藏last-seen仍从群排序估计时间；维护者解释客户端无精确隐藏时间，只持先前可见状态或可见打字/消息触发时间。用户确认第二来源但仍要求离线沉底；自动不活跃关闭，未改排序。 Evidence: "Yes, he saw it because of option 2 / shouldn't my name go to the bottom of the list"。限定：机制解释，剩余界面请求未解决证据

## PRIVACY-G1 — 加密、密钥与通信或存储的密码学保护

通过加密、密钥、密码派生、签名或安全传输协议保护数据，及其信任边界、配置、默认值和替代架构。

**Include:** TLS/HTTPS/DoH、静态/字段/端到端加密、PAKE/PBKDF2/HMAC、密钥备份和管理、密码学签名完整性及弱加密争议。

**Exclude:** 权限声明、登录会话、XSS、日志暴露与指纹防护本身用 G2；只有随机 ID/哈希去标识且无密码学安全边界时用 D1/D3。

**Boundary:** 3871 密文入库而前端仍见明文，非所有使用方均无法解密；14048 TURN-TLS 主要为防火墙兼容，语音视频已有加密；13503 是发布签名完整性，没有个人数据泄露证据。

**Examples:**

- `privacy-issue-3871`: 表单字段由持久化代理加密后入库，前端明文，管理员可按表单重处理已有数据；完成项及文档支持实现，全文检索不含加密字段且仅精确匹配，换钥与多密钥管理延期。 Evidence: "The Form Runner \"front-end\" will always see unencrypted data / We defer Key management"。限定：功能完成并文档化，密钥管理另项
- `privacy-issue-7032`: croc初始短码SHA256被质疑离线枚举和MITM，先加公私钥仍需带外人工核验且文档弱化必要性；长讨论澄清PAKE后作者发布3.0使用PAKE，对方认可。wormhole协议互通仅考虑，不算完成；未独立审计安全保证。 Evidence: "I've bumped croc to 3.0 which uses PAKE / Nowhere does it mention that public keys must be authenticated"。限定：PAKE实现获回应认可，互通未完成
- `privacy-issue-7252`: 用户担心服务器上的数据库文件以口令派生密钥对称加密，服务端泄露后可离线字典攻击，建议每台设备用密钥对，并以多公钥加密文件。维护者说明使用 PBKDF2 做密钥拉伸、弱口令提示，认为非对称方案对大文件性能差、复杂度高，且密钥交换与多设备授权会引入新问题；还提到渗透测试曾审查现有方案。讨论澄清 2048 位 RSA 与 128 位 AES 的强度类比，以及盐/彩虹表问题。最终决定不改加密架构，报告未证明现有方案被攻破。 Evidence: "We're using [PBKDF2] / my decision remains to not change anything about the encryption scheme right now."。限定：维持现有加密方案，风险被部分限定

## PRIVACY-G2 — 认证、权限、攻击防护与意外披露控制

围绕认证会话、平台敏感权限、攻击面、意外信息披露、指纹防护或安全报告处理采取或讨论控制。

**Include:** 2FA、凭据/会话撤销、CSRF/XSS、防误发/误填、SDK 权限初始化、日志 secret、反指纹与网络广播控制、泄露防护与风险误报。

**Exclude:** 仅涉及合法受众设计不自动归安全缺陷；密码学保护用 G1；不能把权限崩溃、静态告警、单方指控或 hypothetical 威胁写成已证实泄露。

**Boundary:** 352 XSS 输入转义属于 G2，不由 payload 的 document.cookie 推断同意；7594 权限崩溃未证实摄像头被使用；12057 错误 URL 共享兼 F1/G2，修复状态仍有限定。

**Examples:**

- `privacy-issue-352`: 完整阅读恶意属性载荷与三条评论。问题根因是用户可控属性被 html_safe 且自动链接；维护者先考虑取消自动链接，随后接受先转义输入、再保留自动链接的方案，但文本没有部署或验证记录。payload 中的 document.cookie 只是攻击示例，不能据此归为 Cookie 同意问题。 Evidence: "XSS through `.html_safe`-ing attributes / escapes the input beforehand"。限定：修复方案获维护者认可，部署未从文本确认
- `privacy-issue-4389`: 因系统要保存姓名、邮箱、电话等个人信息，要求登录启用 2FA 以满足隐私与安全控制：询问是否默认开启、能否用 SMS、开发测试期间能否关闭。回复称应用已强制使用邮件链接或短信 2FA；有人指出邮件/短信是最不安全的选项，建议 Yubikey 或 TOTP；最终结论是默认用邮件、在测试期保持开启。未讨论 2FA 与最小化、留存的关系。 Evidence: "The app already enforces 2fa email links or sms"。限定：现有2FA保持开启
- `privacy-issue-3079`: Tenable 扫描发现生产环境的 csrftoken 未正确设置 SameSite；Secure 项被拆到另一 issue。团队因旧版 Django 缺少能力而阻塞，2020-02-28 升级至 2.2.10 并部署 dev 后，称 dev 与 stage 均已验证 CSRF token 为 Lax，生产计划随 11.5 发布生效。该 issue 后来被重新打开，2021-03 评论称 CSRF token 已设置并已修复；材料没有附生产响应头或回归测试，法律/风险判断均为讨论观点。 Evidence: "I verified that the CSRF token is now being set to `Lax` in both  `dev` and `stage` spaces. / Samesite flag is set on the CSRF token, this is remediated"。限定：开发与预发已验证 Lax，生产修复由后续评论确认

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

## Scope qualifications

仅覆盖已提供的文本；没有重新抓取外链、截图或附件。既有 partial/complete、来源时间差和实现未验证等限定保留。编码由助手撰写，未标注为人类审定或独立验证真值。
