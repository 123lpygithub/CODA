# Privacy — deepseek-1

652 artifacts; 11 codes; 1948 artifact–code assignments.

Inductive consolidation of individually authored full supplied-text reading notes, followed by explicit per-artifact assignment review. No keyword classifier or prior codebook assignments were used for consolidation.

Every supplied artifact has an assignment. Codes describe the observed work, concern, or evidence status; they do not establish that a defect was reproduced. Refer to `assignments.json` for individual reasoning, qualifications, source references and evidence.

## Scope

- Coverage refers to all supplied textual sections, not all content ever linked on the web.
- Source revision ambiguity, inaccessible context, tentative proposals and absence of execution evidence remain in individual scope notes.
- Coding is assistant-authored; it is not published human annotation, independently validated ground truth, or an experimental system run.
- All artifacts are included; unspecified work and comments without established outstanding work are retained explicitly rather than invented as defects.

Single-analyst reconstruction; not a blinded independent replicate.

## Codebook

| Code | Name | Artifacts |
|---|---|---:|
| PRIVACY-A | 同意、拒绝、撤回与偏好执行 | 190 |
| PRIVACY-B | 透明告知、文档与信息可达性 | 277 |
| PRIVACY-C | 采集、追踪与对外数据流 | 182 |
| PRIVACY-D | 去标识、最小化与再识别 | 148 |
| PRIVACY-E | 留存、删除、导出与生命周期 | 128 |
| PRIVACY-F | 身份、受众与访问边界 | 137 |
| PRIVACY-G | 安全保护与隐私威胁机制 | 125 |
| PRIVACY-H | 隐私控制可用性与系统兼容 | 294 |
| PRIVACY-I | 治理、责任与需求权衡 | 397 |
| PRIVACY-Y | 反例、争议或归因修正 | 62 |
| PRIVACY-Z | 内容不足或无法定位具体机制 | 8 |

## PRIVACY-A — 同意、拒绝、撤回与偏好执行

材料涉及用户对处理活动的选择，以及选择的默认、触发、保存、传递和实际执行。

**Include:** 事前门控、opt-in/out、分类同意、撤回、审计记录、同意协议与 Cookie 选择界面。

**Exclude:** 仅提供隐私政策而无选择用 PRIVACY-B；有横幅不等于存在拒绝或阻断。

**Examples:**

- `privacy-issue-450`: 报告指出用户刷新页面但未点击自定义提示时，Cookie 仍被写入，之后所有加载都不再出现提示；报告者认为只有用户实际点击后才应禁用提示。维护者回复“tracked internally”，没有修复或验证细节。 Evidence: `without clicking anything on the custom prompt, a cookie is planted`
- `privacy-issue-8387`: 请求为 DNN 门户增加 Cookie 同意消息，使站点符合 GDPR 的 Cookie 规则；讨论同时包含欧盟监管与 ePrivacy 指令是否明确的判断。后续关联 issue/PR 被合并并据此关闭，但本条没有部署或实际同意流程细节。 Evidence: `have to have a cookie consent form added to the site`

## PRIVACY-B — 透明告知、文档与信息可达性

材料涉及说明收集内容、目的、对象、期限、法律文本、操作路径及其可理解性。

**Include:** 政策发布/翻译、说明准确性、告知入口、数据清单、控制文档及组织对外解释。

**Exclude:** 披露承诺不当作行为已验证；链接未取得不能推其内容。

**Examples:**

- `privacy-issue-21460`: 法文服务条款仍保留英文的隐私法句子，报告者请求翻译并建议 Privacy Act 用标题大小写和斜体；维护者回复已获批准，但未提供发布验证。主题是法律文本的可读性与告知质量，不涉及实际数据流。 Evidence: `Should be translated`
- `privacy-issue-1444`: 任务要求创建订阅服务隐私通知和法律条款页面，并把旧 VPN/Relay 法律页面在指定日期重定向到新页面；正文明确法律内容尚待提供，评论仅给出 legal-docs 源文件链接。成功标准是复选框，没有完成记录，外部链接未读取。 Evidence: `Create new subscription services privacy/legal pages`

## PRIVACY-C — 采集、追踪与对外数据流

材料涉及遥测、分析、第三方资源、联网或跨系统传播的数据和元信息。

**Include:** 主动或隐式请求、IP/Referer/URL、广告标识、推送、SDK、独立退出与本地替代。

**Exclude:** 区分网络连接、数据字段、留存和接收方；静态依赖不等于实际发送。

**Examples:**

- `privacy-issue-21474`: 讨论用 db-ip.com 替代 MaxMind 的 GeoLite 数据库，以减少供应商登录/许可限制并保持 IP 地理位置能力。维护者说明 MaxMind 的账户要求是外部政策变化，建议未来按安装来源模块化并更新页面归属说明；本条没有确认实际切换或数据发送变化，且部分评论缺失。 Evidence: `can we use db-ip.com instead of maxmind.com`
- `privacy-issue-1545`: 用户询问 Twitch 客户端是否收集信息；维护者回答应用本身不收集，只有 Twitch 收集，并给出 Twitch 隐私通知链接。后续评论说明登录 Twitch 时会展示其政策。这是对数据流的解释与告知归属，外部政策内容未读取。 Evidence: `Does this app collects any information?`

## PRIVACY-D — 去标识、最小化与再识别

材料涉及减少可识别信息、匿名/假名变换、粒度降低，以及剩余关联风险或保护覆盖。

**Include:** 日志脱敏、哈希与随机映射、时间位置精度、字段遗漏、导出清洗及效果验证。

**Exclude:** 不能把 hash 自动等同匿名；仅删除整账户用 PRIVACY-E，权利/政策文本仍需 PRIVACY-B。

**Examples:**

- `privacy-issue-943`: 性能分析任务原本怀疑同步与目录查询中的伪名化、DTO 转换是瓶颈；最终结论明确写明伪名化可排除为重要性能影响，主要耗时来自含大量 join 的长 SQL，并拆出两个后续 issue。主题是隐私保护处理与系统性能的权衡。 Evidence: `especially include the pseudonymisation logic because this was already identified as a huge bottleneck`
- `privacy-issue-975`: 社区人员打开个人目录时，辖区外本不应可见的人员没有被伪名化，且过滤列表显示其无权限查看的实体关系；期望是只显示可访问人员，否则进行伪名化，过滤结果也不应暴露不可见关系。评论仅确认在 1.60.0-SNAPSHOT 验证，截图未读取。 Evidence: `persons that the user should not be allowed to see are not pseudonymized`

## PRIVACY-E — 留存、删除、导出与生命周期

材料涉及数据保存位置/时间、清除范围、主体权利、导出副本及跨阶段状态。

**Include:** 账户/内容删除、缓存与日志过期、匿名化保留、备份/归档、访问导出、偏好持久化。

**Exclude:** 界面隐藏、redact、卸载或停用不自动等同物理删除；外部副本保证另说明。

**Examples:**

- `privacy-issue-310`: 提案新增 :RemoveCookies，用正则按域名删除一个或多个域下的 Cookie；作者明确承认新增 cookies 权限会促使用户重新批准扩展，但材料没有实现、合并或部署证据。 Evidence: `remove cookies from a specific domain or from multiple domains`
- `privacy-issue-1765`: crates.io 缺少隐私通知，报告者指出 Google Analytics 与个人数据处理未告知；维护者披露会记录 IP、User-Agent、GitHub 资料和邮箱，日志原计划保留一年但审计发现超期，发布 crate 的邮箱和作者信息因法律或产品原因保留且无追溯编辑流程。讨论包含 GDPR 适用性、监管投诉、法律审查和最终统一网站隐私政策 PR；本条没有部署验证。 Evidence: `Crates.io does not currently display a privacy notice`

## PRIVACY-F — 身份、受众与访问边界

材料涉及谁能识别谁、谁能访问哪些信息，以及跨用户/角色/实例/视图的边界。

**Include:** 角色权限、资料可见性、账户关联、行为状态、消息受众、共享设备及公开索引。

**Exclude:** 不把不猜得到的 URL 当身份授权；本地保存也可能暴露给本地管理员或旁观者。

**Examples:**

- `privacy-issue-21543`: 请求新增管理员修改用户密码功能，用于帮助无法登录的用户；讨论者指出这会带来管理员接触账户凭据、模拟用户访问和未经同意干预的风险。维护者最终拒绝管理员改密能力，认为真正的问题是找回密码流程，并关闭本条。材料没有证明找回流程修复已完成。 Evidence: `no field that enable to change the user password`
- `privacy-issue-975`: 社区人员打开个人目录时，辖区外本不应可见的人员没有被伪名化，且过滤列表显示其无权限查看的实体关系；期望是只显示可访问人员，否则进行伪名化，过滤结果也不应暴露不可见关系。评论仅确认在 1.60.0-SNAPSHOT 验证，截图未读取。 Evidence: `persons that the user should not be allowed to see are not pseudonymized`

## PRIVACY-G — 安全保护与隐私威胁机制

材料以具体攻击、故障、加密、认证、权限、反指纹或通信机制讨论信息保护。

**Include:** 凭据泄露、异常路径污染、传输/静态加密、密钥、认证、权限声明、威胁模型及误报。

**Exclude:** 必须区分假设、报告、复现和反驳；安全相关标题不证明发生泄露。

**Examples:**

- `privacy-issue-352`: 完整阅读恶意属性载荷与三条评论。问题根因是用户可控属性被 html_safe 且自动链接；维护者先考虑取消自动链接，随后接受先转义输入、再保留自动链接的方案，但文本没有部署或验证记录。payload 中的 document.cookie 只是攻击示例，不能据此归为 Cookie 同意问题。 Evidence: `XSS through `.html_safe`-ing attributes`
- `privacy-issue-21543`: 请求新增管理员修改用户密码功能，用于帮助无法登录的用户；讨论者指出这会带来管理员接触账户凭据、模拟用户访问和未经同意干预的风险。维护者最终拒绝管理员改密能力，认为真正的问题是找回密码流程，并关闭本条。材料没有证明找回流程修复已完成。 Evidence: `no field that enable to change the user password`

## PRIVACY-H — 隐私控制可用性与系统兼容

材料涉及控制能否被理解和操作，或隐私保护与框架、平台、功能、数据流之间的适配。

**Include:** 界面遮挡、可访问性、配置绕行、跨端状态、隐私开关功能副作用、测试与依赖集成。

**Exclude:** UI 测试成功不保证后端阻断；功能兼容问题不能一概视为隐私泄漏。

**Examples:**

- `privacy-issue-310`: 提案新增 :RemoveCookies，用正则按域名删除一个或多个域下的 Cookie；作者明确承认新增 cookies 权限会促使用户重新批准扩展，但材料没有实现、合并或部署证据。 Evidence: `remove cookies from a specific domain or from multiple domains`
- `privacy-issue-1957`: 用户询问扩展更新为何请求访问隐私设置；维护者解释该权限只用于读取并显示 privacy.resistFingerprinting 的提示，不写入隐私设置，且平台不允许把该权限设为可选。这是权限范围与用户可理解性的问题，代码搜索链接未读取。 Evidence: `required access to my privacy settings`

## PRIVACY-I — 治理、责任与需求权衡

材料涉及合规解释、组织职责、开发范围、生态依赖、资源优先级或用途与隐私的取舍。

**Include:** 监管/平台审核驱动、控制者/供应商分工、请求受理、评估、标准与开发决策。

**Exclude:** 记录参与者法律判断而不认证其正确；计划、合并、部署、验收分别处理。

**Examples:**

- `privacy-issue-8387`: 请求为 DNN 门户增加 Cookie 同意消息，使站点符合 GDPR 的 Cookie 规则；讨论同时包含欧盟监管与 ePrivacy 指令是否明确的判断。后续关联 issue/PR 被合并并据此关闭，但本条没有部署或实际同意流程细节。 Evidence: `have to have a cookie consent form added to the site`
- `privacy-issue-21474`: 讨论用 db-ip.com 替代 MaxMind 的 GeoLite 数据库，以减少供应商登录/许可限制并保持 IP 地理位置能力。维护者说明 MaxMind 的账户要求是外部政策变化，建议未来按安装来源模块化并更新页面归属说明；本条没有确认实际切换或数据发送变化，且部分评论缺失。 Evidence: `can we use db-ip.com instead of maxmind.com`

## PRIVACY-Y — 反例、争议或归因修正

完整材料削弱、反驳或限定了最初隐私问题判断，或显示原风险归因/目标发生改变。

**Include:** 误报、用户撤回、无外发证据、实际行为不同、争议未定及保护并未达原目标。

**Exclude:** 不是统一的无风险标签；仍可并存真实残余风险，具体原因见备忘录。

**Examples:**

- `privacy-issue-1154`: 报告者担心启用 UserId 伪名化后 visitorId 仍会间接泄露 UserId；维护者解释 privacy manager 的 manipulateRequest 在生成 visitorId 前执行，因此 visitorId 基于已哈希的 UserId 生成，原问题不成立。文本只给出机制解释，没有外部代码复核。 Evidence: `the visitorId would still kind of leak the userId`
- `privacy-issue-2664`: 提出者担心德国及欧洲法律要求 imprint、外链免责声明并讨论 Cookie；回复者依据 TMG/RStV 论证非商业、纯个人静态信息站不需要 imprint，免责声明往往无效，站点无 Cookie 代码且只产生合法服务器日志，因此也无需隐私说明。结论是当前形态无需新增，网站性质变化时再议。 Evidence: `This website does not need an imprint in its current form`

## PRIVACY-Z — 内容不足或无法定位具体机制

可用材料不足以支持任何具体隐私机制，或仅有无法还原语境的外链、占位文本与泛化标题。

**Include:** 空正文、只有外链/占位符、标题也无法定位隐私机制，以及现有讨论未提供可归因对象或行为的条目。

**Exclude:** 正文可读但隐私关联较弱时，应按实际涉及的主题编码；证据可用性是独立字段，不应仅靠 PRIVACY-Z 表达。

**Examples:**

- `privacy-issue-1830`: 正文只有一句“à la”加一个 mozilla/legal-docs PR 链接，没有可读的隐私通知内容、处理活动或实施说明；无评论，外部 PR 未读取，无法定位具体机制。 Evidence: `à la https://github.com/mozilla/legal-docs/pull/1021/files`
- `privacy-issue-11387`: 正文只有占位反馈，评论要求说明具体缺什么后关闭；无法确定具体法律文本或数据机制。 Evidence: `[Enter feedback here]`

