# gpt5.6-1 — Privacy 最终编码本

本轮覆盖 **652 个 artifact**，形成 **16 个可分配 code**，共记录 **1752 个 artifact–code assignment**。全部 652 个 artifact 均已编码，未决 0 个。允许在存在彼此独立证据时进行多重编码，因此类别覆盖数之和可以超过 artifact 数。

本 codebook 来自逐条完整阅读、开放编码、持续比较和反向成员复核；不继承旧 assignment 或 codebook。关键词、正则、聚类和脚本没有用于决定类别，脚本只将已经人工确认的决定转换为 GPT6-1 的发布表现形式并检查一致性。

## 类别一览

|Code|类别|覆盖 artifact 数|
|---|---|---:|
|PV01|隐私告知、政策、透明度与可发现性|206|
|PV02|同意、拒绝、退出、撤回与偏好控制|178|
|PV03|遥测、分析、广告、跟踪与指纹识别|164|
|PV04|数据最小化、必要性、用途限制与保护性默认|85|
|PV05|保存期限、删除、清理、遗忘与生命周期|91|
|PV06|匿名化、假名化、去标识与重识别风险|85|
|PV07|用户访问、导出、更正、可携与账户数据控制|42|
|PV08|访问控制、角色权限、可见性与保密边界|72|
|PV09|第三方处理、外部请求、共享与跨境边界|115|
|PV10|日志、诊断、URL、元数据与界面侧信道暴露|87|
|PV11|设备权限、本地存储与客户端隐私状态|71|
|PV12|保护个人数据的安全与机密性保障|59|
|PV13|法务、监管、治理、责任与事件响应|153|
|PV14|隐私控制的可用性、无障碍、兼容性与可靠性|148|
|PV15|隐私主张被否定、缩小或仅属一般安全/工程语境|70|
|PV16|仅元数据或证据不足以确定具体机制|126|

## 使用规则

- 编码隐私机制、数据边界与风险，不按项目名、法规名或产品领域分类。
- 区分告知、同意与实际数据处理；区分隐藏、删除、匿名化和加密。
- `closed` 不等于修复；PR、commit、release、维护者声明、用户复测与独立验证分开描述。
- 法律意见不是法律结论；安全问题也不自动等于隐私问题。
- 一条 artifact 可多标签；计数是各 code 的成员数，不能求和解释为 652。
- row 554–652 的正文/讨论未取回，按标题作最小判断并使用 PV16。

## PV01 隐私告知、政策、透明度与可发现性

向用户说明收集什么、为何处理、保存多久、交给谁、用户有哪些权利，以及隐私政策、notice、cookie 清单、法律页面和相关入口是否准确、可理解、可找到。

- 纳入：新增或更新 privacy policy；披露 cookie、日志、第三方或处理目的；政策链接缺失、失效或文案过时；告知的本地化、可读性和可发现性。
- 排除与边界：用户是否能接受、拒绝或撤回使用 PV02；实际采集或 tracking 使用 PV03；只有一般技术文档且没有隐私告知语义时不用 PV01。
- 支持：206 个 artifact。完整列表见 `codebook.json` 的 `supporting_cases`。
- 边界案例：row 61 是已上线的综合隐私 FAQ；row 240 是生产 banner 的 terms/privacy 链接错误；row 554 只有“给每个 privacy notice page 加链接”的标题，因此同时使用 PV16，不能推断已部署。
- 代表案例：artifact `privacy-issue-4418`（row 61；完整材料见 `results.json`）。

````text
explicitly say do not ever swap or sell donors' personal info.
````

已上线 FAQ 披露用途、安全措施、供应商限制、保存期、共享条件及 PayPal/Stripe 自主处理。

## PV02 同意、拒绝、退出、撤回与偏好控制

用户对数据处理作出接受、拒绝、opt-in、opt-out、撤回或按目的/类别选择，以及该选择是否真实约束后续处理。

- 纳入：consent banner；accept/reject 对称选择；营销退订；重新征求；版本化 consent；关闭 telemetry；撤回和偏好持久化。
- 排除与边界：只告知而没有选择用 PV01；默认少收数据但不涉及用户选择用 PV04；按钮不可达、偏好丢失或控制未执行时再加 PV14。
- 支持：178 个 artifact。完整列表见 `codebook.json` 的 `supporting_cases`。
- 边界案例：row 17 涉及主动勾选和被绕过的注册路径；row 179 的拒绝状态被 path cookie 覆盖；row 500 只有 blocker 请求，隐藏提示不等于拒绝 cookie，因此保留 PV16。
- 代表案例：artifact `privacy-issue-1770`（row 17；完整材料见 `results.json`）。

````text
the privacy statement has to be explicitly approved
````

注册告知、主动勾选及审计记录已部分实现，但管理员创建与 Shibboleth 路径仍绕过同意。

## PV03 遥测、分析、广告、跟踪与指纹识别

观察、度量或关联用户行为的 telemetry、analytics、advertising、tracking pixel、标识符、跨站跟踪、搜索建议和 fingerprinting/anti-fingerprinting 机制。

- 纳入：GA/Matomo/Segment/Comscore；usage metrics；广告 ID；可关联 ping；browser fingerprint；防指纹设置及其副作用。
- 排除与边界：第三方是谁、请求发往何处另用 PV09；仅一般网络访问而无观察/关联目的不用 PV03；标题只提出 telemetry 而无字段或默认信息时加 PV16。
- 支持：164 个 artifact。完整列表见 `codebook.json` 的 `supporting_cases`。
- 边界案例：row 200 比较遥测标识方案并最终延后；row 300 是 AudioContext 防指纹与兼容回归；row 433 的 opt-out failure 被报告者自我纠正，故同时用 PV15。
- 代表案例：artifact `privacy-issue-3539`（row 200；完整材料见 `results.json`）。

````text
figure out a way to see who is using toil besides us
````

软件遥测设计比较共享假用户、临时 ID 和 GA Measurement Protocol，因关联疑虑最终延后未部署。

## PV04 数据最小化、必要性、用途限制与保护性默认

少收、晚收、降低精度、只为明确目的处理、默认关闭非必要处理，或用不新增个人数据的方案替换功能。

- 纳入：移除非必要字段；不保存 email/IP；降低位置精度；默认不上传；不把数据复用于另一目的；以 RSS 等无个人数据方案替代订阅名单。
- 排除与边界：已经收集的数据保存多久或如何清除用 PV05；保留记录但去身份用 PV06；用户主动选择用 PV02。
- 支持：85 个 artifact。完整列表见 `codebook.json` 的 `supporting_cases`。
- 边界案例：row 112 请求无邮箱注册但因滥用风险被拒；row 342 因需保存邮箱而改建议 RSS；row 649 只有“不让 user secrets 进日志”的标题，使用 PV16 限定推断。
- 代表案例：artifact `privacy-issue-7524`（row 112；完整材料见 `results.json`）。

````text
it is not required to enter an e-mail address.
````

无邮箱注册的最小化请求因验证、spam 与 sockpuppet 风险被官方拒绝，未交给实例管理员配置。

## PV05 保存期限、删除、清理、遗忘与生命周期

个人数据或相关缓存、日志、索引、衍生副本的 retention、TTL、删除、清理、传播与遗忘流程。

- 纳入：账户/内容删除；自动过期；清理缓存和备份；right to erasure；删除是否覆盖搜索索引、客户端副本和关联记录。
- 排除与边界：隐藏或 de-index 不等于删除；去掉身份但保留记录用 PV06；查看、导出、更正等其他数据主体权利用 PV07。
- 支持：91 个 artifact。完整列表见 `codebook.json` 的 `supporting_cases`。
- 边界案例：row 264 的 Teams 卸载只隐藏 tab 而未清第三方数据；row 452 只是司法记录 de-indexing，因此没有把它当作匿名化；row 598 只有 torrent 删除后残留 poster 的标题并加 PV16。
- 代表案例：artifact `privacy-issue-11276`（row 264；完整材料见 `results.json`）。

````text
setValidityState(false)` do not deactivate
````

Teams 卸载只隐藏 tab、无统一第三方数据清理 hook；平台把 retention 责任留给外部站点并判 by design。

## PV06 匿名化、假名化、去标识与重识别风险

hash、HMAC、UUID、redaction、generalization、扰动、输出遮蔽和其他降低直接可识别性的处理，以及稳定标识或辅助信息造成的重识别风险。

- 纳入：IP anonymization；字段 pseudonymization；去标识导出；差分隐私；匿名化覆盖遗漏；哈希是否仍可关联。
- 排除与边界：加密使未授权者不可读用 PV12；物理删除用 PV05；只在 UI 隐藏而底层仍有身份信息不算匿名化。
- 支持：85 个 artifact。完整列表见 `codebook.json` 的 `supporting_cases`。
- 边界案例：row 80 讨论单 trustee 仍可识别选票；row 211 隐藏坐标后仍由 free-text place 泄露；row 542 的 GA anonymize-IP 告警被判 false positive，故并用 PV15。
- 代表案例：artifact `privacy-issue-18634`（row 211；完整材料见 `results.json`）。

````text
actual_ locations, down to the address and/or coordinates
````

隐藏坐标仍从 dashboard free-text place guess 泄露街道；重设计声称移除但无回归确认。

## PV07 用户访问、导出、更正、可携与账户数据控制

用户查看、取得、导出、更正、迁移或管理本人记录，以及提出和跟踪数据主体请求的能力。

- 纳入：data export/portability；查看存储内容；更正个人资料；下载聊天/账户档案；自助或人工数据请求流程。
- 排除与边界：删除行为本身用 PV05，可与 PV07 并列；管理员查看他人数据用 PV08；仅披露权利存在而无控制入口仍可主要使用 PV01/PV13。
- 支持：42 个 artifact。完整列表见 `codebook.json` 的 `supporting_cases`。
- 边界案例：row 86 明确指出导出与删除是两项独立权利；row 479 的聊天导出有开发版测试但明文 archive 风险另用 PV12；row 564 只有“一次删除全部 saved logins”的标题，因此并用 PV16。
- 代表案例：artifact `privacy-issue-5489`（row 86；完整材料见 `results.json`）。

````text
Export and removal do not solve the same problem.
````

ASVS 把导出与删除误写成 OR，讨论明确两项权利独立且可经 help desk 执行，不要求必须自助 UI。

## PV08 访问控制、角色权限、可见性与保密边界

谁可查看、修改或收到数据，包括跨用户/租户泄露、private/public visibility、角色权限、群组成员边界和内部信息误外发。

- 纳入：越权访问；私密字段公开；不同租户数据混淆；退出群组后仍收消息；隐藏文件被共享；内部 note 发给外部关注者。
- 排除与边界：日志、URL、通知、tooltip 等旁路泄露用 PV10，可并列；设备权限用 PV11；单纯身份认证协议而无可见性边界用 PV12 或 PV15。
- 支持：72 个 artifact。完整列表见 `codebook.json` 的 `supporting_cases`。
- 边界案例：row 275 退出群组后旧桌面仍接收消息；row 393 是 staging Google Docs 权限泄露；row 445 只验证导航隐藏，不能证明后端授权。
- 代表案例：artifact `privacy-issue-12082`（row 275；完整材料见 `results.json`）。

````text
I can still send and receive messages
````

退出群组后链接桌面仍收发且对现成员隐藏，构成成员/收件边界失效；stale 关闭无修复。

## PV09 第三方处理、外部请求、共享与跨境边界

数据离开当前产品或 controller 边界，进入第三方 SDK、vendor、外部 CDN/font/map/analytics、政府/合作方，或跨境/跨区域处理。

- 纳入：Google/Segment/YouTube/地图请求；processor/vendor 责任；外部字体/CDN；合作方或配送方访问；跨境和 data residency。
- 排除与边界：analytics/tracking 的目的仍用 PV03；只在本地处理不用 PV09；外部依赖的许可/构建问题而无实际数据边界时加或改用 PV15。
- 支持：115 个 artifact。完整列表见 `codebook.json` 的 `supporting_cases`。
- 边界案例：row 135 明确包括配送公司访问客户数据库；row 322 因公共中介会看到全部财务交易而转自托管；row 414 只是 MaxMind 政策导致依赖适配，故并用 PV15。
- 代表案例：artifact `privacy-issue-8854`（row 135；完整材料见 `results.json`）。

````text
data cannot be used by delivery companies since they don't give their GRPD consent
````

付款前同意拟覆盖配送公司访问客户分析、调查和定向服务，未区分目的或证明拒绝不影响交易；另要求 cookie 对称选择。

## PV10 日志、诊断、URL、元数据与界面侧信道暴露

个人或敏感信息通过日志、stack trace、debug artifact、URL/query、文件元数据、缩略图、通知、tooltip、搜索结果等非主数据路径暴露。

- 纳入：PII 写日志；token/identifier 进入 URL；EXIF 位置；锁屏通知正文；旧缩略图；搜索索引残留；界面错误提示泄露存在性。
- 排除与边界：权限主体直接取得主数据用 PV08；本地存储本身用 PV11；错误关联但没有旁路载体时不强贴 PV10。
- 支持：87 个 artifact。完整列表见 `codebook.json` 的 `supporting_cases`。
- 边界案例：row 44 对 error log 做敏感字段审计；row 332 是屏幕共享时 toast 暴露消息；row 280 的 guest order 错误关联不是日志/URL 侧信道，因此复核时移除了 PV10。
- 代表案例：artifact `privacy-issue-3101`（row 44；完整材料见 `results.json`）。

````text
ensure sensitive information is not logged. e.g. password, credentials, urls.
````

对 error 日志做敏感信息审计并拆分凭据、URL、CN、Pod IP 等清理项，明确是持续治理活动。

## PV11 设备权限、本地存储与客户端隐私状态

camera、microphone、contacts、location、sensor、clipboard 等设备权限，以及 cookie、localStorage、IndexedDB、private mode、本地历史和浏览器侧隐私状态边界。

- 纳入：不必要的设备权限；本地位置轨迹；consent cookie 状态；private browsing 行为；本地持久数据没有清理；浏览器隐私设置导致的保护或冲突。
- 排除与边界：一般 CookieJar、认证 cookie 容量和 cookie 并发工程不自动构成 PV11；跨浏览器失效或控制不可用时另加 PV14；本地内容被未授权主体看到时另加 PV08。
- 支持：71 个 artifact。完整列表见 `codebook.json` 的 `supporting_cases`。
- 边界案例：row 124 是为后台照片唤醒请求位置权限；row 375 是 restart cleanup 漏删 LocalStorage/IndexedDB；row 410 只是 CookieJar flush/并发工程，反向复核后仅保留 PV15。
- 代表案例：artifact `privacy-issue-18429`（row 124；完整材料见 `results.json`）。

````text
require GPS for background uploads
````

位置权限用于后台照片唤醒 workaround，必要性、耗电和“不跟踪”说明均有争议且未最终解决。

## PV12 保护个人数据的安全与机密性保障

直接保护个人数据、身份、账户或机密内容的加密、传输保护、认证/2FA、密钥与 secret 防护、会话安全和泄露后的 containment。

- 纳入：敏感列加密；个人资料传输保护；账户 2FA；可识别数据的密钥管理；私人文件/消息机密性；breach 后注销 session 或强制重置。
- 排除与边界：没有个人数据或隐私边界的一般 TLS、密码、签名、构建和发行版问题用 PV15；匿名化用 PV06；访问主体权限用 PV08。
- 支持：59 个 artifact。完整列表见 `codebook.json` 的 `supporting_cases`。
- 边界案例：row 8 是 Always Encrypted 对敏感列的支持；row 217 是泄露后 session invalidation 被拒；row 472 只是 TLS 1.3 container/发行版支持且 GDPR 仅作背景，反向复核后仅保留 PV15。
- 代表案例：artifact `privacy-issue-14099`（row 8；完整材料见 `results.json`）。

````text
Keyword not supported: 'column encryption setting'.
````

Always Encrypted 缺失直接阻塞敏感列客户端加密；后续 provider 交付有阶段性限制但原问题被项目方认定解决。

## PV13 法务、监管、治理、责任与事件响应

GDPR、CCPA、COPPA 等适用性评估，controller/processor 责任，合规 roadmap，政策治理，数据盘点、审计、breach response/reporting 和组织流程。

- 纳入：法律审查；合规 epic；处理者责任；监管投诉；数据 inventory；incident template；审计流程；是否适用某项法规的判断。
- 排除与边界：法规名本身不能证明违法、合规或实现；具体删除、同意、匿名化等机制仍分别使用 PV05/PV02/PV06；纯粹依赖适配而隐私仅作背景时加 PV15。
- 支持：153 个 artifact。完整列表见 `codebook.json` 的 `supporting_cases`。
- 边界案例：row 16 同时涉及 notice、PII 盘点和长期日志；row 220 是广泛 GDPR 规范清单但无实现证据；row 363 只有 COPPA labels/Wikipedia 链接，故并用 PV16。
- 代表案例：artifact `privacy-issue-1765`（row 16；完整材料见 `results.json`）。

````text
Crates.io does not currently display a privacy notice
````

长期无 privacy notice，同时盘点 PII 与一年以上日志保存并推进统一政策和监管投诉响应。

## PV14 隐私控制的可用性、无障碍、兼容性与可靠性

隐私告知或控制因入口不可达、UI 遮挡、无障碍/本地化问题、状态丢失、浏览器/插件冲突或后端未执行而失效。

- 纳入：banner 按钮不可点击；屏幕阅读器读不到 notice；拒绝状态不持久；toggle 只改 UI；不同浏览器行为不一致；隐私处理漏掉某格式或路径。
- 排除与边界：仅仅“尚未实现”而没有已有控制的可靠性/可用性问题时用相应实质类别；一般 UI bug 且不影响隐私告知或控制时用 PV15；实质机制仍需同时编码。
- 支持：148 个 artifact。完整列表见 `codebook.json` 的 `supporting_cases`。
- 边界案例：row 246 的 NVDA/Firefox banner 修复由报告者确认；row 381 的 TCF enforcement 被 adapter 绕过；row 260 是关闭 banner 后透明容器挡按钮的普通 DOM 缺陷，故并用 PV15。
- 代表案例：artifact `privacy-issue-8890`（row 246；完整材料见 `results.json`）。

````text
cookie banner that NVDA does not read in Firefox
````

NVDA/Firefox 无法读取 banner 阻塞盲人访问；维护者和原报告者都确认 dialog 修复有效。

## PV15 隐私主张被否定、缩小或仅属一般安全/工程语境

材料中的初始泄露或隐私假设被讨论/复测否定或缩小，或者记录实质只是一般 cookie/session、安全、兼容、构建或依赖工程，隐私仅是背景。

- 纳入：false positive；报告者撤回；维护者定位为另一组件；一般 TLS/credential/cookie 工程没有直接个人数据边界；研究或文档使用隐私词但不提供产品控制。
- 排除与边界：不能把 PV15 当作“其他”；仍有实质第三方、tracking、去标识等机制时与对应类别并列；仅因证据不完整而无法判断时使用 PV16。
- 支持：70 个 artifact。完整列表见 `codebook.json` 的 `supporting_cases`。
- 边界案例：row 9 的性能问题明确不是假名化瓶颈；row 224 只是未完成的 API-key 设计；row 507 澄清 Jupyter 默认只在 localhost，没有远程传输证据。
- 代表案例：artifact `privacy-issue-943`（row 9；完整材料见 `results.json`）。

````text
pseudonymisation logic because this was already identified as a huge bottleneck
````

初始假设认为假名化是性能瓶颈，实际分析明确排除并定位为 SQL joins，不能编码成隐私变换缺陷。

## PV16 仅元数据或证据不足以确定具体机制

正文/讨论未取回、只有标题或 labels，或可用材料短到无法确定数据对象、流向、处理结果或交付状态；它标记证据边界而不是隐私主题。

- 纳入：metadata-only；外部文档不可见；只有一句模糊标题；缺少必要对象/行为；无法核验 alleged breach 或 implementation。
- 排除与边界：有完整讨论但结论是否定或一般工程时用 PV15；PV16 不能因为 `closed`、`fixed`、PR label 或评论数而补推已实现；标题已直接支持的最小主题仍应并列编码。
- 支持：126 个 artifact。完整列表见 `codebook.json` 的 `supporting_cases`。
- 边界案例：row 399 只有 Azure Monitor “Data Location”，连 data residency 还是文档位置都不确定，因此仅 PV16；row 558 标题直接支持“consent 前设置第三方 cookie”，使用 PV02/PV09/PV16；冻结 row 554–652 共 99 条全部使用 PV16。
- 代表案例：artifact `privacy-issue-1797`（row 399；完整材料见 `results.json`）。

````text
Data Location
````

只有 Azure Monitor “Data Location”标题，甚至无法确定是 data residency 还是文档位置问题。

## 冻结边界与多标签规则

- PV01 vs PV02：说明发生什么用 PV01；用户能接受、拒绝、撤回或改变处理用 PV02。只有“Got it”且不控制处理仍主要是 PV01。
- PV02 vs PV14：选择机制本身用 PV02；选择无法持久、入口不可达、UI 遮挡或不同浏览器失效，再加 PV14。
- PV03 vs PV09：遥测、analytics 或 tracking 目的用 PV03；数据交给 Google、Segment、广告 bidder、外部 font/CDN 等第三方边界再加 PV09。
- PV04 vs PV05：少收、晚收、降低精度或默认关闭用 PV04；已经收集的数据保存多久、何时删除以及删除覆盖用 PV05。
- PV05 vs PV06：去掉身份但保留记录用 PV06；删除原始、缓存或衍生记录用 PV05；只隐藏显示既不是删除也不是匿名化。
- PV06 vs PV12：hash、扰动和去标识的目标是降低可识别性，用 PV06；加密目标是未经授权者不能读，用 PV12。
- PV08 vs PV10：不应看到数据的主体边界用 PV08；日志、URL、tooltip、通知、元数据等旁路泄露用 PV10，可并列。
- PV11 vs PV14：本地存储、权限或设备数据是实质边界用 PV11；控制界面或跨平台实现失效再加 PV14。
- PV12 vs PV15：一般 TLS、签名、密码或 build 问题若没有个人数据、账户或机密内容边界，使用 PV15；直接保护这些对象才用 PV12。
- PV13 不替代实质控制：合规讨论若同时提出删除、同意或匿名化，仍加 PV05、PV02 或 PV06。
- PV16 只约束能说到何种程度，不把 title-only artifact 从 codebook 排除；每条仍保留标题直接支持的最小主题。

## 配套文件

- `codebook.json`：结构化定义、支持案例、计数、代表证据和方法元数据。
- `codebook.csv`：表格化 codebook。
- `assignments.json` / `assignments.csv`：每个 artifact 的 code、理由、逐字证据与证据限制。
- `taxonomy.json`：与 GPT6-1 一致的 HOW-style 类别树。
- `results.json`：冻结材料正文与最终类别的逐条组合。
