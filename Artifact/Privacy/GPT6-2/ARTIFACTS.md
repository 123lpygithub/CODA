# Privacy · 全部 artifact 逐条分析

阅读范围和证据限制见 [METHOD.md](METHOD.md)。原文全文在 [artifacts.jsonl](artifacts.jsonl)。

<a id="row-1"></a>
## 1. privacy-issue-310

**主题代码：** PRIVACY-E, PRIVACY-H

**开放代码：** 域名级Cookie删除；权限扩展再授权

**逐条判断：** 请求正则批量删除域Cookie，承认新增cookies权限会触发重新批准；没有实现反馈。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 提案无实施证据

**原文证据：**

位置 `879:941`：

> remove cookies from a specific domain or from multiple domains

位置 `1308:1362`：

> prompt the extension users to re-approve the extension

<a id="row-2"></a>
## 2. privacy-issue-352

**主题代码：** PRIVACY-G

**开放代码：** 不可信用户属性导致XSS；安全转义与自动链接兼容

**逐条判断：** 完整阅读恶意payload及3评论；原因是用户属性html_safe。维护者先愿放弃autolink，后接受先转义再保留链接的PR方案；cookie出现在payload不等于Cookie同意问题。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 方案获得维护者认可，未从文本确认部署

**原文证据：**

位置 `3212:3252`：

> Keeps autolinking which is frankly handy

位置 `3294:3322`：

> escapes the input beforehand

位置 `3721:3739`：

> That works for me.

<a id="row-3"></a>
## 3. privacy-issue-450

**主题代码：** PRIVACY-A, PRIVACY-H

**开放代码：** 未交互即持久化选择；提示显示状态失真

**逐条判断：** 用户未点prompt但reload后写cookie，后续提示消失；应只有交互后禁用。最后转内部跟踪，非修复确认。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 转内部跟踪

**原文证据：**

位置 `892:959`：

> without clicking anything on the custom prompt, a cookie is planted

位置 `1704:1735`：

> This is now tracked internally.

<a id="row-4"></a>
## 4. privacy-issue-21460

**主题代码：** PRIVACY-B

**开放代码：** 法律条款翻译遗漏；术语格式一致性

**逐条判断：** 法语条款残留英文Privacy Act句子，提供法译并要求专业核对；评论仅确认文案获批准。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 文案批准，部署未知

**原文证据：**

位置 `1046:1067`：

> Should be translated.

位置 `1646:1682`：

> Clementine has approved this message

<a id="row-5"></a>
## 5. privacy-issue-8387

**主题代码：** PRIVACY-A, PRIVACY-B, PRIVACY-I

**开放代码：** Cookie同意界面缺失；合规义务理解不确定；合规实施组织

**逐条判断：** 正文请求DNN Cookie consent，评论组建GDPR团队并讨论法规不确定性；记录参与者观点，不裁定其法律解释正确。末评论明确关联PR合并。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 关联PR已合并

**原文证据：**

位置 `1312:1337`：

> No cookie consent message

位置 `3537:3568`：

> Closing as the PRs were merged.

<a id="row-6"></a>
## 6. privacy-issue-21543

**主题代码：** PRIVACY-F, PRIVACY-G, PRIVACY-I

**开放代码：** 管理员接管与用户自主控制冲突；密码恢复故障；邮箱验证流程

**逐条判断：** 完整阅读15评论；管理员为排障要求改外部用户密码，引发同意/隐私争论。维护者认为应修复自助恢复而不鼓励管理员接管，明确拒绝此功能；bcrypt与截图不是独立隐私诉求。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 功能请求拒绝，恢复故障另报

**原文证据：**

位置 `8115:8219`：

> The real fix to this issue is to make sure that the "forgot my password" functionality works as expected

位置 `8075:8111`：

> Opensupports shouldn't encourage it.

<a id="row-7"></a>
## 7. privacy-issue-21474

**主题代码：** PRIVACY-H, PRIVACY-I

**开放代码：** 第三方合规变化传播依赖约束；地理数据库来源替换；账号注册负担

**逐条判断：** 全文及现有3评论已读；MaxMind因合规动机改下载/账号要求，维护者考虑模块化替换db-ip及来源署名。3/4评论可用，缺失一条，不能确认最终决定。scramble为普通动词非脱敏。

**材料可用性：** partial。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 方案讨论，部分证据

**原文证据：**

位置 `2237:2323`：

> we're trying to work around a restriction that was put upon us with very little notice

位置 `3467:3505`：

> Modularize this would be a nice thing.

<a id="row-8"></a>
## 8. privacy-issue-14099

**主题代码：** PRIVACY-G, PRIVACY-I

**开放代码：** 列加密能力缺失；框架迁移阻碍；保护措施跨组件依赖；密钥提供者适配

**逐条判断：** 57,177字符全部分段读完，86评论含重复代码均读。最初Core不支持Column Encryption Setting，企业回退Framework并担心自制加密；维护者起初无排期后进入3.0。2019-05新Microsoft.Data.SqlClient预览支持AE，但ref API遗漏、EF旧依赖及AKV provider仍需协调。随后补包和替代连接方案，末评论认定原问题已解决。cookies/beer是玩笑，不属于浏览器Cookie主题。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 原请求据维护者已解决；AKV等特定用例另跟踪

**原文证据：**

位置 `1267:1318`：

> Keyword not supported: 'column encryption setting'.

位置 `35174:35250`：

> Tests were/are run against the non-ref implementation so we didn't catch it.

位置 `57011:57098`：

> We believe the originally reported issue has been addressed in Microsoft.Data.SqlClient

<a id="row-9"></a>
## 9. privacy-issue-943

**主题代码：** PRIVACY-D, PRIVACY-I, PRIVACY-Y

**开放代码：** 保护机制性能归因待验证；权限相关假名化优化提议

**逐条判断：** 正文与2评论完整读；最初怀疑pseudonymisation bottleneck，最终正文明确排除其显著性能影响，主要SQL massive joins。保留讨论变化，不编码为已证实匿名化拖慢；TRACE是诊断手段非PII泄露。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 调查改变初始归因，后续性能分析另单

**原文证据：**

位置 `3771:3840`：

> pseudonymization can be ruled out as a relevant impact on performance

位置 `3844:3922`：

> long runtimes are mainly caused by long running SQL queries with massive joins

<a id="row-10"></a>
## 10. privacy-issue-975

**主题代码：** PRIVACY-D, PRIVACY-F

**开放代码：** 权限边界与假名化不一致；跨视图身份暴露

**逐条判断：** 社区官员在person directory看见辖区外未假名化个人，同时过滤列表泄露不该显示的关联。表单/目录规则不一致；截图为举证，非媒体元数据主题。最后评论版本验证。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 1.60.0快照验证

**原文证据：**

位置 `1312:1384`：

> persons that the user should not be allowed to see are not pseudonymized

位置 `3520:3549`：

> Validated on 1.60.0-SNAPSHOT.

<a id="row-11"></a>
## 11. privacy-issue-1019

**主题代码：** PRIVACY-D, PRIVACY-I

**开放代码：** 内容指纹与匿名化目标混淆；弱散列再识别风险；分布式密钥一致性；假名化与匿名化区分

**逐条判断：** 6评论全文；普通SHA内容指纹便比较但小输入域可穷举，带密钥散列受集群密钥一致性约束，HMAC仍可能凭密钥再识别。最终交付内容fingerprint，明确不是原匿名化目标；另一issue跟踪。不能记为匿名化功能已解决。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 内容指纹已引入，匿名化需求另跟踪

**原文证据：**

位置 `6549:6616`：

> The fingerprint processor is not intended for content anonymization

位置 `3474:3555`：

> no mechanism to ensure that the secret key was consistent across all ingest nodes

<a id="row-12"></a>
## 12. privacy-issue-1154

**主题代码：** PRIVACY-D, PRIVACY-Y

**开放代码：** 关联标识符假名化完整性疑虑

**逐条判断：** 正文担心visitorId泄露userId，但同一作者评论解释先执行manipulateRequest，visitorId由已hashed userId生成，撤回缺陷判断。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 报告者解释为非问题

**原文证据：**

位置 `1581:1616`：

> Actually, it should not be an issue

位置 `1738:1783`：

> creating a hash on the already hashed User Id

<a id="row-13"></a>
## 13. privacy-issue-1444

**主题代码：** PRIVACY-B, PRIVACY-I

**开放代码：** 订阅服务法律告知整合；旧政策链接迁移

**逐条判断：** 新增隐私/条款页并把Relay/VPN旧地址按日期redirect，评论提供source docs；正文清单未勾选且无上线确认。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 发布计划与源文档已提供，完成未知

**原文证据：**

位置 `1478:1517`：

> New legal pages are live in production.

位置 `1525:1570`：

> Existing Relay/VPN legal pages are redirected

<a id="row-14"></a>
## 14. privacy-issue-1545

**主题代码：** PRIVACY-B

**开放代码：** 应用与平台数据责任边界；收集透明度咨询

**逐条判断：** 用户问是否收集信息，回复称app本身不收集只有Twitch；后登录Twitch强制化并展示其政策。记录回复主张，不独立证明无收集。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 解释答复后建议关闭

**原文证据：**

位置 `1108:1169`：

> No the app itself does not, only Twitch collects information.

位置 `1408:1461`：

> You're now required to log into Twitch to do anything

<a id="row-15"></a>
## 15. privacy-issue-1665

**主题代码：** PRIVACY-B, PRIVACY-H

**开放代码：** 隐私入口本地化失效；修复验证后重开

**逐条判断：** 链接label固定英文但目标页语言正确；初验证仍失败而重开，之后1行修正并在1.230.2 staging确认。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** staging修复验证

**原文证据：**

位置 `1395:1483`：

> The “Privacy Notice” label link is displayed in English, regardless of the user language

位置 `3790:3829`：

> Verified this as fixed on Train 1.230.2

<a id="row-16"></a>
## 16. privacy-issue-1765

**主题代码：** PRIVACY-B, PRIVACY-C, PRIVACY-I

**开放代码：** 隐私告知长期缺失；数据盘点发现保留偏差；标识符个人数据认定争议；法律资源与治理延迟；监管投诉推动整改

**逐条判断：** 21评论完整读。GA已移除仍缺数据处理告知；律师协商与跨站统一拖延。IP是否个人数据争论，审计发现日志保存超预期，列GitHub身份/email/IP-UA及crate内容；发布者删除限制未定。末仅有政策PR待合并，不能从closed称已上线。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 政策PR提出，材料内未确认合并或发布

**原文证据：**

位置 `12789:12841`：

> our logs are being retained for longer than intended

位置 `16856:16898`：

> There is a PR open on the website repo now

位置 `16997:17034`：

> When it is merged, we will add a link

<a id="row-17"></a>
## 17. privacy-issue-1770

**主题代码：** PRIVACY-A, PRIVACY-B, PRIVACY-C, PRIVACY-D, PRIVACY-E, PRIVACY-F, PRIVACY-I

**开放代码：** 机构可定制隐私声明；明确同意及记录；数据盘点；删除与科研完整性冲突；联合身份流程绕过同意

**逐条判断：** 17评论全读；从double opt-in要求澄清单次明确操作可足够，需留确认记录（参与者意见）。声明模板可编辑，注册checkbox已实现但默认null不显示；2021反馈管理员建号经Shibboleth仍不展示，建议last_login/IDP处理，不代表全部入口已修。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 注册页机制已实现，SSO遗漏仍建议替代方案

**原文证据：**

位置 `9937:9964`：

> Ok this is now implemented.

位置 `10878:10946`：

> the privacy policy is never displayed when logging in via Shibboleth

<a id="row-18"></a>
## 18. privacy-issue-1818

**主题代码：** PRIVACY-B

**开放代码：** 隐私告知措辞准确化

**逐条判断：** location box 的Promise改Notice；评论明确Dev/Stage待review，不据closed认定生产上线。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** Dev/Stage待审

**原文证据：**

位置 `1478:1522`：

> Ready for review on both Dev and Stage envs.

<a id="row-19"></a>
## 19. privacy-issue-1830

**主题代码：** PRIVACY-B, PRIVACY-I

**开放代码：** 法律文档集中维护

**逐条判断：** 复制Privacy Notice到legal-docs，正文仅参照PR链接；无讨论不能恢复实施。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 任务提出，完成未知

**原文证据：**

位置 `65:87`：

> copy Privacy Notice to

<a id="row-20"></a>
## 20. privacy-issue-1887

**主题代码：** PRIVACY-A, PRIVACY-B

**开放代码：** 地域告知覆盖扩大

**逐条判断：** 因California新法由仅EU居民展示扩为所有访客；没有执行证据。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 任务提出，完成未知

**原文证据：**

位置 `978:993`：

> to all visitors

<a id="row-21"></a>
## 21. privacy-issue-1957

**主题代码：** PRIVACY-F, PRIVACY-G, PRIVACY-H, PRIVACY-I

**开放代码：** 新增扩展权限缺解释；权限粒度过宽

**逐条判断：** Firefox更新要求访问privacy settings，用户不解；维护者解释只读resistFingerprinting来显示notice且不能设optional，不写设置。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 权限用途解释，无权限缩减

**原文证据：**

位置 `1585:1643`：

> CB only reads that and does not write any privacy settings

<a id="row-22"></a>
## 22. privacy-issue-2024

**主题代码：** PRIVACY-B, PRIVACY-I

**开放代码：** 法律文档发布滞后

**逐条判断：** 要求将英文与12语言Firefox notice推生产；无评论或部署反馈。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 发布请求，完成未知

**原文证据：**

位置 `887:923`：

> push the following doc to production

<a id="row-23"></a>
## 23. privacy-issue-2017

**主题代码：** PRIVACY-B, PRIVACY-C

**开放代码：** 分析引入需配套透明告知；第三方服务条款约束

**逐条判断：** 最初仅网站访问分析，评论要求先准备policy，末已加GA但政策另开ticket；两项完成时间不同，不能认为同时合规。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 分析已启用，政策另单

**原文证据：**

位置 `3574:3649`：

> I have added Google Analytics and setup a new ticket for the privacy policy

<a id="row-24"></a>
## 24. privacy-issue-2005

**主题代码：** PRIVACY-B, PRIVACY-I

**开放代码：** 法律文档生产集成

**逐条判断：** Hubs Notice/ToS上生产；末称文件在bedrock submodule而关闭，未明确两个页面都live。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 已有文件确认，页面部署未知

**原文证据：**

位置 `1881:1923`：

> the files are in the submodules on bedrock

<a id="row-25"></a>
## 25. privacy-issue-2037

**主题代码：** PRIVACY-B, PRIVACY-I

**开放代码：** 第三方处理者透明度不足；法律变更职责与同步流程

**逐条判断：** 要求列出interaction data服务及政策/代码链接；8评论主要讨论如何升级legal、跨repo版本同步，末因年代及已发生政策变更关闭并称有内部流程，不证明请求的清单全部完成。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 因政策变化和新内部流程关闭

**原文证据：**

位置 `1113:1189`：

> can this contain a list (with links) to which third-party services are used?

位置 `5214:5274`：

> we've got a new internal practice for privacy policy changes

<a id="row-26"></a>
## 26. privacy-issue-2061

**主题代码：** PRIVACY-B, PRIVACY-E

**开放代码：** 保留期限告知不清；清理机制缺失；法律文档与实现边界

**逐条判断：** 询问TTL/用户修改/人工清理；早期回复称无expiration/cleanup因收集少，后称媒体移除时间已明确并改房主显式关房，不把早期状态当最终。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 据回复告知已澄清，新增考虑另单

**原文证据：**

位置 `2122:2179`：

> we do not have any expiration/cleanup mechanisms in place

位置 `2537:2595`：

> media removal from Mozilla servers is explicitly specified

<a id="row-27"></a>
## 27. privacy-issue-2102

**主题代码：** PRIVACY-C, PRIVACY-H, PRIVACY-Y

**开放代码：** 邮件跟踪被隐私保护阻断；分析事件推断

**逐条判断：** 模板全HTML已读，其隐私footer是模板背景。实际问题是opened统计缺失；维护者解释客户端阻tracking pixels且点击会回填opened，认为预期行为。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 预期行为解释，无修复

**原文证据：**

位置 `6988:7043`：

> many of which block tracking pixels for privacy reasons

位置 `7131:7169`：

> we also backfill an Email Opened event

<a id="row-28"></a>
## 28. privacy-issue-2259

**主题代码：** PRIVACY-B, PRIVACY-H

**开放代码：** 退出选择说明入口不可达

**逐条判断：** dpad无法选opt-out链接，后回复3.1 Cube可用；只确认该设备版本。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 特定设备版本无法复现

**原文证据：**

位置 `1291:1319`：

> Works for me on 3.1 on Cube.

<a id="row-29"></a>
## 29. privacy-issue-2296

**主题代码：** PRIVACY-A, PRIVACY-F, PRIVACY-H

**开放代码：** 隐私设置语义误导；新旧API迁移兼容；账户暴露与授权提示不同步

**逐条判断：** 10评论全读。维护者称关闭privacy只允许自动暴露账号，不阻ethereum.enable弹窗；用户质疑实际暴露行为与文档不符。临时兼容开关计划去掉，isApproved绕行不解决语义争议；不能写已修复。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 设计解释与绕行建议，争议未消除

**原文证据：**

位置 `5690:5731`：

> accounts are either automatically exposed

位置 `5853:5893`：

> this settings option is purely temporary

位置 `9870:9899`：

> This is really no consolation

<a id="row-30"></a>
## 30. privacy-issue-2386

**主题代码：** PRIVACY-B, PRIVACY-C

**开放代码：** 无Cookie分析仍有告知义务争议

**逐条判断：** GA无policy被报违反ToS，维护者以无Cookie/伪fingerprint/不存IP解释，报告者认为仍须披露；后仅说commit fixed，不知道通过移除GA还是补policy。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 维护者声明commit修复，具体方式未见

**原文证据：**

位置 `2640:2656`：

> Fixed in 7069917

<a id="row-31"></a>
## 31. privacy-issue-2406

**主题代码：** PRIVACY-B

**开放代码：** 监管申诉链接失效

**逐条判断：** privacy policy/notice中的ICO链接broken，请更新。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 请求，完成未知

**原文证据：**

位置 `871:939`：

> There's a broken link on the privacy policy and each privacy notice.

<a id="row-32"></a>
## 32. privacy-issue-2439

**主题代码：** PRIVACY-B, PRIVACY-H

**开放代码：** 自定义告知未生效；多语言支持不足；跨表单隐私集成未完成

**逐条判断：** comment/contact/register均仍默认文字且自定义policy链接未显示，维护者承认not fully finished。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 承认实现未完成

**原文证据：**

位置 `2088:2116`：

> it is not fully finished yet

<a id="row-33"></a>
## 33. privacy-issue-2462

**主题代码：** PRIVACY-A, PRIVACY-B, PRIVACY-E, PRIVACY-I

**开放代码：** 营销选择与透明告知；儿童同意年龄；保留期限；同意审计；手工删除流程

**逐条判断：** 正文是合规清单不只有email opt-in，含保留期限、儿童年龄地域差异、postcode识别性、集中记录删除流程；无评论，不把清单当实现。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 合规任务列表，完成未知

**原文证据：**

位置 `1430:1481`：

> Right to be forgotten (a manual process documented)

位置 `1235:1275`：

> Minimum age to register without consent.

<a id="row-34"></a>
## 34. privacy-issue-2456

**主题代码：** PRIVACY-B, PRIVACY-I

**开放代码：** 法律文档协作与发布

**逐条判断：** 隐私/条款/license需显式；与法务反复协商后final docs共享，正文三项清单含Release已勾选，区别于仅closed。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 清单声明发布完成

**原文证据：**

位置 `1020:1041`：

> Release it into MARLO

位置 `2062:2109`：

> final version of the documents that were shared

<a id="row-35"></a>
## 35. privacy-issue-2461

**主题代码：** PRIVACY-B, PRIVACY-H

**开放代码：** 本地保存与云上传边界不清；隐私告知缺产品特定信息；保存按钮语义误导

**逐条判断：** 建议明确仅Cloud Share才上传及两周保留，但作者注明only if true，不能视作实际行为。后评论称FAQ未改、质疑无解释关闭，保留未解决。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 关闭原因不明，用户报告未改

**原文证据：**

位置 `1557:1595`：

> Of course, only put that if it’s true.

位置 `3402:3447`：

> there was no change in Firefox screenshot FAQ

<a id="row-36"></a>
## 36. privacy-issue-2497

**主题代码：** PRIVACY-B, PRIVACY-I

**开放代码：** 法律文案发布同步

**逐条判断：** 两份Focus/Klar四文件单字符串更新；回复submodule已同步，生产部署预计当日，未明确完成。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 主分支同步，部署预计

**原文证据：**

位置 `1440:1485`：

> The submodule in bedrock/master is up-to-date

<a id="row-37"></a>
## 37. privacy-issue-2579

**主题代码：** PRIVACY-B, PRIVACY-I

**开放代码：** 隐私政策缺失；报告渠道阻碍改进

**逐条判断：** 贡献者提议撰写政策，说明透明度目的；维护者仅答GitHub只收BUG，非接受文案。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 按渠道范围拒绝

**原文证据：**

位置 `2411:2442`：

> Github is for BUG reports only.

<a id="row-38"></a>
## 38. privacy-issue-2620

**主题代码：** PRIVACY-B, PRIVACY-H

**开放代码：** 主页隐私入口缺失

**逐条判断：** 其他legal页有footer，主页没有；关闭因计划全面重设计，不代表当前入口已补。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 纳入主页重设计计划

**原文证据：**

位置 `2535:2593`：

> Closing this as we need to do a complete homepage redesign

<a id="row-39"></a>
## 39. privacy-issue-2592

**主题代码：** PRIVACY-A, PRIVACY-B, PRIVACY-H

**开放代码：** 告知确认交互阻塞

**逐条判断：** Privacy Notice继续按钮不可点，收集环境后原报告者称自行恢复，不知原因。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 用户确认恢复，原因未知

**原文证据：**

位置 `1953:1996`：

> No idea what changed but it is working now.

<a id="row-40"></a>
## 40. privacy-issue-2628

**主题代码：** PRIVACY-G

**开放代码：** 明文浏览活动暴露；传输保护默认设置

**逐条判断：** 最初提HTTPS-only默认关并考虑与archive合并，后分开设置，末已加Redirect HTTPS且默认开；以最后状态为准。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 功能加入且默认开启

**原文证据：**

位置 `2466:2520`：

> Added a "Redirect to HTTPS" option, now on by default.

<a id="row-41"></a>
## 41. privacy-issue-2664

**主题代码：** PRIVACY-B, PRIVACY-I

**开放代码：** 法定告知范围争议；静态网站数据收集认定

**逐条判断：** 5评论完整读，用户要求imprint/disclaimer/cookie讨论；另一参与者长篇法律解释认为静态个人站只日志无需这些，原作者接受。只记录观点，不替其背书法律准确性。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 基于参与者法律解释不实施

**原文证据：**

位置 `5224:5310`：

> We don't need an imprint, we don't need a disclaimer, and we don't need a privacy note

<a id="row-42"></a>
## 42. privacy-issue-2904

**主题代码：** PRIVACY-A, PRIVACY-B, PRIVACY-C

**开放代码：** 默认遥测未告知；自主选择与数据有用性冲突；聚合统计识别性争议

**逐条判断：** 15评论全读；维护者补文档，说明活跃设备用户数及版本、不分享第三方且少于5设备不存。用户仍要求opt-in，维护者以无人主动配置及无PII反驳；文档修复不等于默认关闭。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 文档已补，opt-in请求未采纳

**原文证据：**

位置 `2335:2384`：

> Added documentation for it at the top of the page

位置 `2436:2515`：

> If we make it opt-in instead of opt-out, surely nobody would ever configure it.

<a id="row-43"></a>
## 43. privacy-issue-2958

**主题代码：** PRIVACY-E, PRIVACY-F

**开放代码：** 自助账户删除；删除前导出提醒；共享实体引用去关联

**逐条判断：** 全清单勾选且末done。讨论澄清不能删除多人共用postal code对象，应删该用户引用及checkin加密user id；对匿名统计保留只有问题无明确裁决。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 明确完成

**原文证据：**

位置 `3123:3174`：

> remove the deleted user's **reference** to the code

位置 `3976:3988`：

> This is done

<a id="row-44"></a>
## 44. privacy-issue-3101

**主题代码：** PRIVACY-D

**开放代码：** 日志敏感数据审计；标识符替换；敏感性范围争议；持续检查需求

**逐条判断：** 明确先error+审计、希望每PR工具。分子项去xDS、CN换serial、PodIP换UID；评论区分自然人IP与PodIP并建议可扩展过滤。末据多个PR关闭但可重开，不宣称持续工具实现。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 一轮PR处理完成，持续审计仍需

**原文证据：**

位置 `1352:1380`：

> this is an on-going activity

位置 `5605:5658`：

> Closing for now with above linked (and many more) PRs

<a id="row-45"></a>
## 45. privacy-issue-3474

**主题代码：** PRIVACY-B, PRIVACY-I

**开放代码：** 儿童应用第三方数据限制；平台审核触发

**逐条判断：** Apple拒因儿童app analytics/ad分享PII或device信息，维护者转account manager/support，材料无整改。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 转专门支持

**原文证据：**

位置 `894:948`：

> your Kids Category app includes analytics, advertising

位置 `1814:1840`：

> support team will help you

<a id="row-46"></a>
## 46. privacy-issue-3577

**主题代码：** PRIVACY-D, PRIVACY-I

**开放代码：** 包元数据最小化；来源追溯与隐私取舍；可选身份字段；生态责任边界

**逐条判断：** 4评论全读。作者质疑生产/上传者姓名ID必要性与跨境义务；讨论追溯用途，认为opaqueID仍可识别，决定sometimes optional，导出剥除为建议。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 可选保留的设计共识

**原文证据：**

位置 `6898:6924`：

> Yes, sometimes, optionally

位置 `6515:6530`：

> strip on export

<a id="row-47"></a>
## 47. privacy-issue-3749

**主题代码：** PRIVACY-E

**开放代码：** 删除后的事件日志最小化；合同留存与目的限制；姓名识别性误解

**逐条判断：** 主体请求customer events，讨论能否保留删除者姓名。回复区别履约发票的必要保留与事件日志非必要姓名，建议notified customer而非email；未证实代码完成。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 给出设计指导，实施未知

**原文证据：**

位置 `3041:3134`：

> probably avoid storing the information outside of the context where it's absolutely necessary

位置 `3222:3258`：

> safer to say "notified the customer"

<a id="row-48"></a>
## 48. privacy-issue-3839

**主题代码：** PRIVACY-F, PRIVACY-G, PRIVACY-I

**开放代码：** 防意外公开研究数据；项目级保密意图；非专家可用保护

**逐条判断：** 完整12评论及代码已读；不是抵御恶意者，而是传递项目给非Git专家时阻误push。最初拒加参数后接受pre-push自动配置，考虑hook不随clone/Windows适配；末1.2.0发布。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 功能发布1.2.0

**原文证据：**

位置 `10725:10779`：

> The mechanism doesn't have to be absolutely watertight

位置 `13302:13331`：

> This feature is now available

<a id="row-49"></a>
## 49. privacy-issue-3845

**主题代码：** PRIVACY-A, PRIVACY-B, PRIVACY-C

**开放代码：** 隐私友好分析服务选择；安装标识替代设备标识；分析先行告知滞后

**逐条判断：** 完整7评论。拒GA跨站跟踪，Heap不适桌面后改Mixpanel，生成UUID而非MAC；日志声明noPII是作者主张。清单分析已完成policy未勾，席位共享是讨论不作为已实施安全缺陷。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 分析实现与测试事件完成，policy仍待办

**原文证据：**

位置 `5506:5553`：

> generate a UUID (feels less personally invasive

位置 `3196:3214`：

> Add Privacy Policy

<a id="row-50"></a>
## 50. privacy-issue-3856

**主题代码：** PRIVACY-I

**开放代码：** 数据敏感性与适用标准澄清

**逐条判断：** 原以为provider非敏感，回复确认有PII但MARS-E不适用，建议常规安全与访问控制/NIST而不做该issue专项；非声明无保护义务。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 范围澄清，无专项实施

**原文证据：**

位置 `3461:3491`：

> We have PII for some providers

位置 `3410:3457`：

> MARS-E is for exchanges and doesn't apply here.

<a id="row-51"></a>
## 51. privacy-issue-3911

**主题代码：** PRIVACY-B, PRIVACY-F, PRIVACY-I

**开放代码：** 自动PII识别需求转字段隐私；部署政策说明

**逐条判断：** 最初考虑自动输入识别与伙伴资源，后来icebox并转ToS/about页需求；末称field-level privacy已处理，不宣称自动检测实现。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 用字段级隐私替代处理

**原文证据：**

位置 `3154:3193`：

> Taken care of with field level privacy.

<a id="row-52"></a>
## 52. privacy-issue-3947

**主题代码：** PRIVACY-F

**开放代码：** 匿名发言与假名账户区分；跨帖子再识别；匿名性与限流取舍

**逐条判断：** 报告者要无作者记录而非普通匿名账号，维护者提出null authority共享账号并解释无账号无法Steem Power限流；用户确认可行但希望API/前端友好化。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 用户接受绕行，友好接口未实现

**原文证据：**

位置 `3970:4005`：

> Null authority account, works fine.

位置 `3520:3551`：

> no account means no Steem Power

<a id="row-53"></a>
## 53. privacy-issue-3976

**主题代码：** PRIVACY-E, PRIVACY-G

**开放代码：** 身份客户端存储可替换性；避免浏览器持久化

**逐条判断：** 起因同构React无法用window/storage，讨论引入隐私需求：in-memory store避免PII落浏览器。维护者说明已有WebStorageStateStore自定义入口，未确认完整SSR适配。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 已有存储扩展指导

**原文证据：**

位置 `3954:4011`：

> option of passing in a simple in-memory object as a store

位置 `4317:4365`：

> set the `userStore` on the `UserManagerSettings`

<a id="row-54"></a>
## 54. privacy-issue-4004

**主题代码：** PRIVACY-F

**开放代码：** 公开排障材料暴露参与者标识；标识长度变化兼容

**逐条判断：** 主问题worker ID超50字符；评论者实际删去公开ID并提醒PII。长度根因在用户改URL与MTurk政策变化间未确定。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 公开ID已编辑；根因未决

**原文证据：**

位置 `1867:1898`：

> don't paste worker IDs publicly

位置 `1964:1991`：

> I've redacted your comment.

<a id="row-55"></a>
## 55. privacy-issue-3993

**主题代码：** PRIVACY-B, PRIVACY-C, PRIVACY-G, PRIVACY-I, PRIVACY-Y

**开放代码：** 捆绑广告软件收集疑虑；许可文本与实际行为差异；软件分发治理边界

**逐条判断：** license写OpenCandy收集NON-PII，用户质疑trusted包。维护者依据文件/网络观察认为已移除，但不能删官方license；分发政策不把adware等同malware，双方意见仍不同。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 解释后接受关闭，未独立确认行为

**原文证据：**

位置 `2752:2802`：

> no background web request detected through fiddler

位置 `2886:2938`：

> we cannot remove that text from the included license

<a id="row-56"></a>
## 56. privacy-issue-3994

**主题代码：** PRIVACY-B, PRIVACY-F, PRIVACY-H, PRIVACY-I

**开放代码：** 儿童社区隐私指导；个人信息范围扩展；收集用途与可见性告知

**逐条判断：** 全文比较旧新FAQ/CG；从禁止可联系信息扩为可识别/找到人，包括学校社交链接；补举报索取PII、邮件opt-in用途，列公开与私有字段。正文要求他人批准，无实施确认。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 拟议文案，部分认可但发布未知

**原文证据：**

位置 `1539:1581`：

> should approve before any changes are made

位置 `4522:4565`：

> contain or request this kind of information

<a id="row-57"></a>
## 57. privacy-issue-4216

**主题代码：** PRIVACY-B, PRIVACY-Z

**开放代码：** 证据不足

**逐条判断：** 仅标题Conflicting documentation及元数据；不使用检索关键词privacy controls推导具体冲突。

**材料可用性：** metadata_only。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 无正文，无法判断

**原文证据：**

位置 `65:90`：

> Conflicting documentation

<a id="row-58"></a>
## 58. privacy-issue-4283

**主题代码：** PRIVACY-F, PRIVACY-G, PRIVACY-I

**开放代码：** 受限内容播放与所有权；外包托管责任；隐私能力受服务付费限制

**逐条判断：** 8长评论含方案全部读。直接上传需求伴随DRM/限域播放，明确任何保护可绕过。选学校自有Vimeo OAuth直传，平台不存视频，学校持有内容；privacy.embed需付费，免费不具相同限制。讨论承认UX代价但节省平台成本/用量计费复杂度；实施细节转Discord。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 方案趋向Vimeo直传，未有发布证据

**原文证据：**

位置 `12338:12381`：

> to enjoy privacy , it has to be a paid plan

位置 `7825:7886`：

> School administrators retain full ownership of video content.

<a id="row-59"></a>
## 59. privacy-issue-4254

**主题代码：** PRIVACY-B, PRIVACY-H

**开放代码：** 响应式布局使隐私入口不可访问

**逐条判断：** 200/400%缩放触移动断点，因移动端starter无用而隐藏整段，连privacy statement也消失；维护者改为可见，末给测试环境确认修复。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 修复验证

**原文证据：**

位置 `6379:6437`：

> we can hit these mobile breakpoints on desktop via zooming

位置 `6688:6708`：

> Issue has been fixed

<a id="row-60"></a>
## 60. privacy-issue-4398

**主题代码：** PRIVACY-A, PRIVACY-B, PRIVACY-C, PRIVACY-H

**开放代码：** 遥测选择入口可发现性

**逐条判断：** 安装初始dialog加文案链接设置，方便privacy controls，无实施反馈。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 请求，完成未知

**原文证据：**

位置 `992:1035`：

> so users can easily access privacy controls

<a id="row-61"></a>
## 61. privacy-issue-4418

**主题代码：** PRIVACY-B, PRIVACY-I

**开放代码：** 评级驱动告知完善；第三方用途限制；保留与共享边界披露

**逐条判断：** Charity Navigator评级要求促FAQ改，法务已审；全文新文案含供应商不能自用/再共享直销、必要期限保留及支付商各自政策。末live。编码披露而非已验证运营控制。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 文案已上线

**原文证据：**

位置 `4115:4131`：

> This is now live

位置 `2566:2628`：

> vendors receiving your information are contractually obligated

<a id="row-62"></a>
## 62. privacy-issue-4427

**主题代码：** PRIVACY-F, PRIVACY-I

**开放代码：** 关注者审批与受众限制；联邦协议信任边界；既有传播不可撤回；社交关系可见性

**逐条判断：** 保护边缘群体免于骚扰；讨论从实例内控制转向跨实例协议约束，公有订阅hub不能直接传私信。末称可关闭但联邦私帖另开议题，关注关系可见性仍被提出，不能编码成全范围完成。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 本地能力报告完成，联邦另议

**原文证据：**

位置 `7665:7734`：

> Separate issue is making private posts work across federation as well

位置 `7351:7407`：

> you couldn't really hide and protect your existing posts

位置 `8133:8168`：

> who you follow, and who follows you

<a id="row-63"></a>
## 63. privacy-issue-4429

**主题代码：** PRIVACY-F, PRIVACY-I

**开放代码：** 细粒度隐私与API完整性冲突；上游去关联替代

**逐条判断：** 请求部分资料私有和个人页面定制；维护者拒加隐私控制以免API资料不全，指出关闭游戏公开比赛资料后仍收集但不关联账号；布局转UI讨论。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 细粒度请求拒绝，提供替代设置

**原文证据：**

位置 `1548:1601`：

> the data is collected but not linked to their account

位置 `1298:1333`：

> I'd rather not add privacy controls

<a id="row-64"></a>
## 64. privacy-issue-4771

**主题代码：** PRIVACY-C, PRIVACY-D

**开放代码：** 报表IP匿名化；原始保留与统计准确性；默认隐私请求；版本兼容

**逐条判断：** 公开访问统计导致IP暴露，讨论日志级处理损失独访准确性；实现仅输出IPv4/6匿名化并保留统计。后续默认开启诉求未获确认，旧版本不识别参数需升级。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 输出匿名化已实现，默认开启未知

**原文证据：**

位置 `4044:4142`：

> This is done at the the output level so all visitors stats will continue to show accurate numbers.

位置 `6579:6626`：

> you will need to upgrade to the latest version.

<a id="row-65"></a>
## 65. privacy-issue-4797

**主题代码：** PRIVACY-D, PRIVACY-E, PRIVACY-H

**开放代码：** 历史匿名化任务可靠性；调度与进度可观测性

**逐条判断：** 历史资料匿名化数日停留进行中或计划中；维护者探问错误与数据库大小但未证实根因。另一参与者确认手动命令有效，之后任务也自行运行，不能推广成原报错根因已修复。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 部分使用者确认执行成功，根因未定

**原文证据：**

位置 `3828:3892`：

> Looks like the task I created a couple of days ago ran by itself

位置 `3894:3940`：

> without needing the command above run manually

<a id="row-66"></a>
## 66. privacy-issue-4800

**主题代码：** PRIVACY-D, PRIVACY-I

**开放代码：** 逐请求IP匿名化；协议依赖判断修正

**逐条判断：** 最初认为依赖协议和tracker变更而延期，后改称自描述事件context即可表达匿名化标志，最终迁移至enrich议题。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 设计修正并迁移，无实施确认

**原文证据：**

位置 `1971:2015`：

> We don't need to update the Tracker Protocol

位置 `2030:2103`：

> add a self-describing context to each event flagging the IP anonymization

<a id="row-67"></a>
## 67. privacy-issue-4821

**主题代码：** PRIVACY-D, PRIVACY-F, PRIVACY-I

**开放代码：** 多种数据表示匿名化遗漏；字段演进的保守默认；报表架构耦合

**逐条判断：** --anon只处理journal entries，account声明仍原名；讨论报表默认类型映射重构及字段演进，新增字段应忽略而非未经匿名化复制。未见修复验证。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 缺陷与设计讨论，完成未知

**原文证据：**

位置 `1314:1360`：

> Sounds like we anonymize journal entries only.

位置 `2372:2454`：

> if new field appears we just ignore it instead of copying it without anonymization

<a id="row-68"></a>
## 68. privacy-issue-4802

**主题代码：** PRIVACY-D, PRIVACY-I

**开放代码：** 位置时间降精度；重识别风险；地域政策差异；隐私与街道级用途权衡

**逐条判断：** 提出按城市需求模糊坐标或区域聚合，并可降时间精度；争论传感器误差与主动降精度应否区分，截断不等于有效匿名化。最后关闭并拟开更成熟方案，未实施。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 重开议题筹划，方案未定

**原文证据：**

位置 `6441:6524`：

> Even without persistent user IDs, there is some risk of reidentification or misuse.

位置 `9199:9253`：

> will open new issue(s) with more considered approaches

<a id="row-69"></a>
## 69. privacy-issue-4844

**主题代码：** PRIVACY-B, PRIVACY-F, PRIVACY-G, PRIVACY-H

**开放代码：** 诊断资料意外泄露；手工脱敏遗漏；安全导出工具需求

**逐条判断：** 完整阅读头像异常主体及39评论。隐私问题在诊断过程发生：参与者自述未脱敏密码已公开需更换，日志含完整vcard/email，难保证人工删净，改用截断截图；另建议ldap:show-config隐藏密码但域名仍需自行改。头像异常经升级与scan-app-data报告消失，不能视作脱敏工具已实现。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 主故障报告解决；隐私导出请求无确认

**原文证据：**

位置 `15973:16007`：

> Damn, anonymization was incomplete

位置 `52545:52673`：

> Is there any tool to format and/or preferably properly anonymize the log before sending it in, but without rendering it useless?

<a id="row-70"></a>
## 70. privacy-issue-4864

**主题代码：** PRIVACY-D, PRIVACY-I

**开放代码：** 多词实体匿名化；标注边界与语言形态

**逐条判断：** 学校名称应合并为一个替代标签；初版连不连续的Alice与属格也合并，讨论后限制连续tokens，后续目标重复词缺陷也获修复声明。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 实现并修正后续缺陷

**原文证据：**

位置 `3235:3294`：

> Edges will only be grouped if their tokens are consecutive.

位置 `3945:3963`：

> This is now fixed.

<a id="row-71"></a>
## 71. privacy-issue-4887

**主题代码：** PRIVACY-B, PRIVACY-C, PRIVACY-D

**开放代码：** 政策驱动分析IP匿名化配置

**逐条判断：** 政策方要求在代码中开启GA匿名IP；评论将关闭关联至1687，无运行验证内容。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 关联变更关闭，验证未见

**原文证据：**

位置 `882:912`：

> This is a request from policy.

位置 `1361:1376`：

> Closed by #1687

<a id="row-72"></a>
## 72. privacy-issue-4923

**主题代码：** PRIVACY-B, PRIVACY-H

**开放代码：** 隐私功能对外说明；上线依赖与文档验证

**逐条判断：** 为匿名化/混淆功能准备提案模板与博客材料，生产未就绪阻塞；后文案审核及功能QA通过，末负责人称已完成且无更多宣传计划。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 文档审核及QA通过，负责人报告完成

**原文证据：**

位置 `5437:5446`：

> Passed QA

位置 `6245:6313`：

> I believe this is done and we don't have plans for additional comms.

<a id="row-73"></a>
## 73. privacy-issue-4970

**主题代码：** PRIVACY-C, PRIVACY-D

**开放代码：** 分析IP匿名化开关；配置关闭语义一致性

**逐条判断：** 要求anonymizeIP可设真假并扩展至GTM；关闭时不能输出该键，末仅赞同符号不足以证明部署。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 配置要求明确，完成未证实

**原文证据：**

位置 `1722:1791`：

> if "anonymizeIP" is off then it should not be added in Analytics json

<a id="row-74"></a>
## 74. privacy-issue-4960

**主题代码：** PRIVACY-A, PRIVACY-B, PRIVACY-E, PRIVACY-I

**开放代码：** 合规需求集合；同意与拒绝；告知删除导出；最小化与安全维护

**逐条判断：** 主清单标注已完成接受/拒绝存储、告知、删除、条款与隐私声明复选框；GoogleOptOut仍未勾选。评论额外建议导出、匿名化与依赖更新，不能把这些建议都视作已实施。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 主清单完成，退出分析项未完成，附加建议未知

**原文证据：**

位置 `2043:2086`：

> Possibility to export all the personal data

位置 `1258:1291`：

> GoogleOptOut or GoogleOptOut hint

<a id="row-75"></a>
## 75. privacy-issue-5005

**主题代码：** PRIVACY-D

**开放代码：** IP匿名化遗漏请求头；跨字段一致性

**逐条判断：** 打开匿名IP后X-Forwarded-For及X-Real-Ip仍保留全IP；维护者认可两处都应处理并报告修复，待下个tag发布。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 修复声明，发布待后续

**原文证据：**

位置 `1647:1683`：

> We should do anonymization for both.

位置 `1908:1948`：

> Fixed. Will be released in the next tag.

<a id="row-76"></a>
## 76. privacy-issue-5001

**主题代码：** PRIVACY-D

**开放代码：** 匿名化目标表示保留原文；导出便利性

**逐条判断：** 目标text仍有Alice等原名，提取匿名文本需遍历边和标签二次替换；请求直接替换目标属性，未见实现答复。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 请求，完成未知

**原文证据：**

位置 `2347:2401`：

> Alice should not appear in target if i've labeled her.

<a id="row-77"></a>
## 77. privacy-issue-5063

**主题代码：** PRIVACY-B, PRIVACY-D, PRIVACY-E

**开放代码：** 默认匿名化日志覆盖；删除与匿名化术语纠正

**逐条判断：** 诉求forget-me无需额外配置覆盖默认日志；维护者明确工具不删除任何内容，实际为匿名化，并给出修复PR62。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 匿名化覆盖修复声明

**原文证据：**

位置 `2287:2316`：

> Tool does not delete anything

位置 `2319:2329`：

> Fixed with

<a id="row-78"></a>
## 78. privacy-issue-5066

**主题代码：** PRIVACY-D

**开放代码：** 匿名化工具部署配置不适配；部分处理失败

**逐条判断：** Integrator默认运行额外business-process SQL导致表缺失；日志显示日志处理完成、SQL失败，需按profile选配置，不能泛称所有匿名化均失败。末给出PR63修复。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 修复声明

**原文证据：**

位置 `2123:2174`：

> Processor execution completed. Processor : log-file

位置 `4102:4137`：

> Table "ACT_HI_ATTACHMENT" not found

<a id="row-79"></a>
## 79. privacy-issue-5061

**主题代码：** PRIVACY-D, PRIVACY-H

**开放代码：** 匿名化工具配置路径错误；发布版本验证

**逐条判断：** 默认配置路径遗漏conf目录导致启动失败；首次PR修复后alpha3仍存在，最终beta报告修复。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** beta修复声明

**原文证据：**

位置 `3449:3476`：

> This issue exists in alpha3

位置 `3667:3682`：

> Fixed with beta

<a id="row-80"></a>
## 80. privacy-issue-5087

**主题代码：** PRIVACY-D, PRIVACY-F, PRIVACY-G, PRIVACY-I

**开放代码：** 管理员信任与投票去匿名；密钥生命周期；隐私与可验证性权衡；威胁模型争论

**逐条判断：** 读完17评论：单管理员能解密单票小计，维护者承认此信任边界，建议多trustee及删除私钥以允许公开验证；反方担心私钥副本并主张不留身份票据关联，双方争论审计与改票检测。关闭因不再活跃，未改实现或确认文档更新。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 威胁边界解释与缓解建议，非修复

**原文证据：**

位置 `9712:9819`：

> if you delete the private key, then indeed the election administrator can no longer decrypt partial tallies

位置 `17142:17186`：

> good discussion, not an active issue anymore

<a id="row-81"></a>
## 81. privacy-issue-5119

**主题代码：** PRIVACY-C, PRIVACY-D

**开放代码：** 分析IP匿名化开关

**逐条判断：** 标题要求GA匿名IP开关，正文仅参考与关联议题；无评论或实施说明。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 请求，完成未知

**原文证据：**

位置 `83:138`：

> Add support for IP Address Anonymization on/off setting

<a id="row-82"></a>
## 82. privacy-issue-5123

**主题代码：** PRIVACY-D, PRIVACY-I

**开放代码：** 医疗匿名化标准更新

**逐条判断：** 标签列表停在DICOM2011，要求跟随最新标准；无说明具体新增标签或实施。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 请求，完成未知

**原文证据：**

位置 `919:990`：

> The current list of anonymization tags is based on DICOM Standard 2011.

<a id="row-83"></a>
## 83. privacy-issue-5161

**主题代码：** PRIVACY-D, PRIVACY-E

**开放代码：** 导出阶段去标识；运行保留用途；默认清洗与显式绕过

**逐条判断：** 为运行使用worker IDs而推迟匿名化到导出；最终development默认将PII换数字索引，--no-scrub保留原ID，不应称数据库不再含PII。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 开发分支实现

**原文证据：**

位置 `3136:3186`：

> The default is to replace PII with number indices.

位置 `3187:3260`：

> The `--no-scrub` flag allows you to export the data w/ worker ids intact.

<a id="row-84"></a>
## 84. privacy-issue-5329

**主题代码：** PRIVACY-A, PRIVACY-B, PRIVACY-C, PRIVACY-H

**开放代码：** 自愿遥测与易懂告知

**逐条判断：** 为兼容性收集使用站点，需要用户同意及易懂政策；指向4739和后续MetaMetrics议题，未给出实施证据。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 转交关联工作

**原文证据：**

位置 `981:1004`：

> with the user's consent

位置 `1034:1091`：

> Would require a privacy policy that's easy to understand.

<a id="row-85"></a>
## 85. privacy-issue-5452

**主题代码：** PRIVACY-E, PRIVACY-F, PRIVACY-I

**开放代码：** 关联附件删除覆盖；保守保留默认；管理员代办删除

**逐条判断：** 删除帖子仍留上传文件，维护者承认为省事保留；清单已勾选磁盘删除、保留选项及测试，用户上传索引清除划掉未勾。解释账户由管理员删除时清所有内容，排序另开。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 附件删除工作清单完成，索引子项未确认

**原文证据：**

位置 `2618:2662`：

> ACP option to preserve post uploads on purge

位置 `2278:2339`：

> all of your content (topics, posts, uploads, etc.) are purged

<a id="row-86"></a>
## 86. privacy-issue-5489

**主题代码：** PRIVACY-B, PRIVACY-E, PRIVACY-I

**开放代码：** 删除与导出权利分离；标准措辞歧义；业务流程与应用能力边界

**逐条判断：** OR允许两权择一受质疑，建议拆开或AND；讨论不强制用户界面，但客服受理仍须应用方法或程序处理。末无标准已修改的明确证据。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 需求解释达成，文本变更未知

**原文证据：**

位置 `1325:1374`：

> Export and removal do not solve the same problem.

位置 `5808:5871`：

> a method or procedure to export and/or delete user-related data

<a id="row-87"></a>
## 87. privacy-issue-5499

**主题代码：** PRIVACY-E, PRIVACY-F, PRIVACY-I

**开放代码：** 账户及关联内容删除；管理员代办替代；删除确认界面

**逐条判断：** 要求删帖子评论关注等、确认slider和按钮，说明邮件请求管理员也可能足够；清单未勾且仅stale机器人，不能据关闭认定完成。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 未完成清单，后续过期提醒

**原文证据：**

位置 `1794:1862`：

> I'd like to delete all my data, ie. posts, comments, shouts, follows

位置 `2976:3005`：

> automatically marked as stale

<a id="row-88"></a>
## 88. privacy-issue-5516

**主题代码：** PRIVACY-E, PRIVACY-I

**开放代码：** 合规功能范围；删除与法定保留冲突；第三方扩展覆盖；加密责任层

**逐条判断：** 读完15评论：初始把DB加密称硬要求被纠正；讨论订单税务保留和客户信息匿名化、客服流程、扩展及外部处理者难覆盖，各地要求解释有分歧。作者拟可选模块，最终维护者因超范围关闭，无实施。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 当前范围外拒绝

**原文证据：**

位置 `1997:2056`：

> it's not a hard requirement to encrypt customer data in db.

位置 `9106:9138`：

> Out of scope - at least for now.

<a id="row-89"></a>
## 89. privacy-issue-5546

**主题代码：** PRIVACY-B, PRIVACY-H, PRIVACY-I

**开放代码：** 权利告知与可发现性；请求处理负担

**逐条判断：** 拟用户资料页显示GDPR权利及操作步骤，同时担心增加请求量；关联PR392并说明纳入470，无具体运行验证。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 报告纳入关联变更

**原文证据：**

位置 `1332:1364`：

> maybe resulting in more requests

位置 `1860:1876`：

> Included in #470

<a id="row-90"></a>
## 90. privacy-issue-5547

**主题代码：** PRIVACY-B, PRIVACY-E, PRIVACY-F, PRIVACY-H

**开放代码：** 账户删除入口缺失；客服流程告知；开发资源限制

**逐条判断：** 用户因收费和邮件粒度要求离开，维护者解释历史可邮件删除但告知差，补FAQ作为临时方案；自助删除需求仍有效，无实际删除执行证明。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 文档补充与人工替代，自助功能未确认

**原文证据：**

位置 `3567:3602`：

> I've just added an FAQ entry for it

位置 `3703:3735`：

> That's a stop-gap option at best

<a id="row-91"></a>
## 91. privacy-issue-5569

**主题代码：** PRIVACY-E, PRIVACY-I

**开放代码：** 第三方采集内容清除；删除范围与用户通知

**逐条判断：** 为遗忘权拟移除Twitter消息，帖子内容/标题仅完全匹配推文时清空或替换日期标题，先查部署使用量并通知客户；评论确认方案需沟通，未见迁移执行。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 清理方案认可，执行未知

**原文证据：**

位置 `1394:1464`：

> Posts.content will be blanked out _when_ it matches the tweet exactly.

位置 `1131:1158`：

> We need to notify the users

<a id="row-92"></a>
## 92. privacy-issue-5577

**主题代码：** PRIVACY-A, PRIVACY-B, PRIVACY-E, PRIVACY-I

**开放代码：** 合规需求集合；独立同意；默认不勾选；条款版本与同意记录；删除导出

**逐条判断：** Epic七项均已勾选：可携带、遗忘、默认取消营销、页面版本、接受时间、解绑同意及newsletter opt-in；另有stale评论。按清单报告完成，不把wontfix标签当实质拒绝。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 清单完成声明，缺运行验证

**原文证据：**

位置 `1240:1278`：

> Unbundled consent on user registration

位置 `1303:1344`：

> Opt-in for all the users with newsletters

<a id="row-93"></a>
## 93. privacy-issue-5557

**主题代码：** PRIVACY-E, PRIVACY-I

**开放代码：** IP保留期限；历史与主表双重残留；反滥用用途权衡

**逐条判断：** 历史IP无限保留逾两百万行，讨论主表最后IP也需处理；有处罚关联不能随意删玩家，可对久未登录无处罚者删除，cron为替代。末用户感谢实现，具体最终参数未展示。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 用户确认已实现，细节范围有限

**原文证据：**

位置 `4063:4096`：

> Thank you, for implementing this.

位置 `1973:2003`：

> what about the `players` table

<a id="row-94"></a>
## 94. privacy-issue-5609

**主题代码：** PRIVACY-B, PRIVACY-E, PRIVACY-F, PRIVACY-I

**开放代码：** 公开身份再展示与同意；删除范围协商；署名与隐私冲突

**逐条判断：** 从git日志自动提取贡献者联系方式加入贡献/POM文件遭本人拒绝；维护者愿移除展示但称git历史仍留，本人接受只不出现在contrib/pom。有修复PR与后续整体完成声明，不能称历史清除。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 限定展示移除达成，整体任务报告完成

**原文证据：**

位置 `5507:5570`：

> It is fine if my information just not appear in contrib and pom

位置 `4953:4996`：

> automatically extracing it from the git log

<a id="row-95"></a>
## 95. privacy-issue-940

**主题代码：** PRIVACY-D, PRIVACY-E, PRIVACY-I

**开放代码：** 假名映射与关联性；随机ID与哈希区别；处理管线能力限制

**逐条判断：** 请求UUID增强假名安全；维护者详解稳定hash便于跨事件关联，随机ID需持久映射防字典攻击并管理重启，filebeat不能拆出identity与event双事件，建议Logstash。最终清backlog关闭未实现。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 技术澄清，积压清理关闭

**原文证据：**

位置 `4579:4640`：

> Currently processors in filebeats can not produce new events.

位置 `5028:5062`：

> Backlog grooming: Closing for now.

<a id="row-96"></a>
## 96. privacy-issue-4946

**主题代码：** PRIVACY-B, PRIVACY-C, PRIVACY-D, PRIVACY-I

**开放代码：** 分析平台合规评估；IP匿名化与限期保留；共享事件总线隔离

**逐条判断：** 分析GA/GTM与政策兼容性，提出匿名IP及18个月保留，讨论多实例共享dataLayer需特定事件名防跨账号收集。已有PR按版本分段，参与者宣称不传个人信息只是方案判断，未提供实测或独立合规验证。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 方案及PR讨论，隐私控制部署未知

**原文证据：**

位置 `6353:6394`：

> We will limit stored records to 18 months

位置 `9803:9852`：

> This is avoided by using non-generic event names.

<a id="row-97"></a>
## 97. privacy-issue-1285

**主题代码：** PRIVACY-B, PRIVACY-H, PRIVACY-I

**开放代码：** 隐私告知编写指引

**逐条判断：** 表单创建者不知如何填写隐私声明，验收清单已勾选说明用途和必要性的指引，评论认为MVP首发已完成。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 清单及评论报告完成

**原文证据：**

位置 `927:990`：

> what to do with the privacy notice, and what should be included

位置 `1418:1436`：

> Think this is done

<a id="row-98"></a>
## 98. privacy-issue-1946

**主题代码：** PRIVACY-B, PRIVACY-H, PRIVACY-I

**开放代码：** 隐私声明链接可发现性

**逐条判断：** 页脚补Kitware隐私声明链接，评论明确435修复。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 修复声明

**原文证据：**

位置 `1475:1488`：

> Fixed in #435

<a id="row-99"></a>
## 99. privacy-issue-14155

**主题代码：** PRIVACY-A, PRIVACY-B, PRIVACY-I

**开放代码：** 强制订阅与撤回权；群邮件退订冲突；运营用途与滥用防护

**逐条判断：** 请求禁止退订和免确认以免任一群成员取消全组通知；维护者因滥用及GDPR顾虑拒内建，建议未来模板可改去链接供内部用，属参与者法律判断而非已验证合规。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 功能拒绝，未来定制替代

**原文证据：**

位置 `2530:2577`：

> we could never guarantee the use of such option

位置 `2704:2733`：

> remove the subscription links

<a id="row-100"></a>
## 100. privacy-issue-20510

**主题代码：** PRIVACY-E

**开放代码：** 会话外不持久化选项

**逐条判断：** 仅标题与元数据可读，支持会话外不留存诉求；缺正文和3评论，不能判断存储类型、默认值或实现。

**材料可用性：** metadata_only。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 证据缺失，结果未知

**原文证据：**

位置 `75:133`：

> Add an option not to persist *anything* outside of session

<a id="row-101"></a>
## 101. privacy-issue-4975

**主题代码：** PRIVACY-D, PRIVACY-I

**开放代码：** 轨迹重识别；位置时间聚合；设备标识轮换；精确共享同意

**逐条判断：** 提出人口密度相关降精度、街区吸附和最少30次路线聚合；指出实时可用单车消失重现可关联行程，建议途中换ID。回复仅README加入数据处理指引，不证明上述技术措施实施。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 告知指引链接已加，技术措施未知

**原文证据：**

位置 `3226:3269`：

> scramble the bike identifiers during a trip

位置 `3945:4003`：

> link to the guidelines for handling the data in the README

<a id="row-102"></a>
## 102. privacy-issue-18826

**主题代码：** PRIVACY-A, PRIVACY-B, PRIVACY-C, PRIVACY-I

**开放代码：** 第三方遥测独立选择；首次发送时机；撤回后删除；界面与数据流验证差异

**逐条判断：** 用户信任Mozilla但不愿第三方收集，要求独立开关和清晰披露。讨论Adjust安装即发导致设置来不及，QA只验证切换而追问网络效果；最后说明Glean关闭指标后删除数据，并未明确验证所有供应商删除或首次发送修正。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 开关已提供，Glean删除说明，其他范围未证实

**原文证据：**

位置 `5917:6005`：

> When we toggle data collection off for a metric Glean receives that and deletes the data

位置 `2863:2923`：

> all of the data that is sent to Adjust has already been sent

<a id="row-103"></a>
## 103. privacy-issue-18388

**主题代码：** PRIVACY-F, PRIVACY-H, PRIVACY-Y

**开放代码：** 活动状态间接推断；历史可见信息残留；隐私预期分歧

**逐条判断：** 用户称隐藏last-seen仍从群排序估计时间；维护者解释客户端无精确隐藏时间，只持先前可见状态或可见打字/消息触发时间。用户确认第二来源但仍要求离线沉底；自动不活跃关闭，未改排序。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 机制解释，剩余界面请求未解决证据

**原文证据：**

位置 `4575:4609`：

> Yes, he saw it because of option 2

位置 `4643:4689`：

> shouldn't my name go to the bottom of the list

<a id="row-104"></a>
## 104. privacy-issue-3987

**主题代码：** PRIVACY-F, PRIVACY-G

**开放代码：** 登录失败信息隐藏

**逐条判断：** 只有标题，私密社区应模糊登录失败结果；无法确认具体暴露字段或账号枚举机制及处置。

**材料可用性：** metadata_only。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 证据缺失，结果未知

**原文证据：**

位置 `65:119`：

> Private Community should obscure login failure results

<a id="row-105"></a>
## 105. privacy-issue-7656

**主题代码：** PRIVACY-B, PRIVACY-C, PRIVACY-F

**开放代码：** 客户端标识披露；统计需求与隐私争论

**逐条判断：** 统一Status专属UA便于统计遭泄露信息质疑，提议方以通用软件信息而非个体标识辩护；最后称可识别Status客户端但链接实现细节不可见，不能断言原UA方案照搬。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 客户端识别能力报告已提供

**原文证据：**

位置 `2891:2930`：

> We now provide a way to identify Status

位置 `2176:2196`：

> it should be generic

<a id="row-106"></a>
## 106. privacy-issue-18588

**主题代码：** PRIVACY-A, PRIVACY-B

**开放代码：** 邮件用途同意；跨界面选择入口

**逐条判断：** 要用户确认活动团队可用email发congress token，在注册、设置、用户编辑提供复选框；无评论实施证据。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 请求，完成未知

**原文证据：**

位置 `1091:1173`：

> The user should be able to decide if the event-team is allowed to send him emails.

<a id="row-107"></a>
## 107. privacy-issue-12632

**主题代码：** PRIVACY-A, PRIVACY-C, PRIVACY-H

**开放代码：** 分析同意引导；既有用户迁移；选择持久化缺陷；验证范围

**逐条判断：** P3A需新用户引导、升级首启卡片及设置开关；iPhone/iPad验收多项通过但均明确重启不保留开关并另记6537。不能用PASSED概括为偏好持久化或匿名保证已验证。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 界面验收通过，重启偏好缺陷另追踪

**原文证据：**

位置 `6995:7049`：

> Switch state is not retained after the browser restart

位置 `4056:4090`：

> A flow (and UI) for existing users

<a id="row-108"></a>
## 108. privacy-issue-14048

**主题代码：** PRIVACY-G, PRIVACY-I, PRIVACY-Y

**开放代码：** 传输加密需求与既有保护澄清；严格防火墙兼容；配置告知误解；实现范围与回退可靠性

**逐条判断：** 读完46评论及配置讨论：TURN-TLS主要为穿越DPI防火墙，参与者澄清语音视频已有加密、静态secret不传输，不能编码为已证实明文泄露。turns支持最终实现并测试，但随机选服务器使需要TLS时可能选错，另开议题，单服务器是折中。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** TURN-TLS已实现，选择可靠性部分未解决

**原文证据：**

位置 `31627:31664`：

> The secret is not sent over the wire.

位置 `34136:34168`：

> I consider this partially fixed.

位置 `34209:34286`：

> the current behavior of selecting a turn server at random makes it unreliable

<a id="row-109"></a>
## 109. privacy-issue-21530

**主题代码：** PRIVACY-B

**开放代码：** 隐私法声明信息布局

**逐条判断：** 把OMB号码移入隐私法展开面板顶部；仅呈现调整，未说明收集行为改变。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 请求，完成未知

**原文证据：**

位置 `810:859`：

> Move OMB number into privacy act expansion panel.

<a id="row-110"></a>
## 110. privacy-issue-20198

**主题代码：** PRIVACY-H, PRIVACY-Z

**开放代码：** 日志配置需求；隐私关联证据不足

**逐条判断：** 仅标题支持VBMS日志可配置，不能由检索词PII推断具体泄露或脱敏要求。

**材料可用性：** metadata_only。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 证据缺失，结果未知

**原文证据：**

位置 `65:114`：

> Allow vbms logging configurations to be specified

<a id="row-111"></a>
## 111. privacy-issue-5058

**主题代码：** PRIVACY-D, PRIVACY-E, PRIVACY-I

**开放代码：** 自由文本匿名化范围；姓名指代歧义

**逐条判断：** 请求匿名工具替换评论MESSAGE_中用户信息，回复认为自由评论可指他人或同名者，不能可靠对应账号故不需删除；这是参与者范围判断，非证明姓名无识别性。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 范围请求遭反对，无实施

**原文证据：**

位置 `1748:1803`：

> I don't think we need to remove names from the comment.

<a id="row-112"></a>
## 112. privacy-issue-7524

**主题代码：** PRIVACY-F, PRIVACY-I

**开放代码：** 注册数据最小化；邮箱验证反垃圾权衡；实例自治争论

**逐条判断：** 请求无邮箱注册以免业余实例管理员收集，维护者因联邦spam外部性坚持邮箱；中途有自行改配置方案，2022再次明确拒绝取消要求。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 核心功能拒绝，外部改配置建议

**原文证据：**

位置 `2113:2173`：

> for local sign ups, e-mail will remain a required component.

位置 `4440:4475`：

> a vector for spam for everyone else

<a id="row-113"></a>
## 113. privacy-issue-7460

**主题代码：** PRIVACY-A, PRIVACY-B, PRIVACY-E, PRIVACY-H

**开放代码：** 上传选择持久化；默认行为争议；本地处理控制

**逐条判断：** 用户称扫描结果自动上传未知账号，维护者解释初始不上传但一次submit后缓存选择持续生效，可清缓存或keep-local；未回应已上传删除或说明账号归属。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 行为解释与替代控制，删除请求未回答

**原文证据：**

位置 `1746:1783`：

> If you scan once with the submit flag

位置 `1862:1878`：

> delete the cache

<a id="row-114"></a>
## 114. privacy-issue-35

**主题代码：** PRIVACY-E, PRIVACY-H

**开放代码：** cookie同意记忆与浏览器限制；追踪移除

**逐条判断：** 接受后反复提示，回复解释Safari限制客户端cookie寿命且无法确定具体期限；最后声明不再收cookie且弹窗消失，非单纯延长有效期。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 报告不再收cookie及提示消失

**原文证据：**

位置 `2320:2378`：

> We don't collect cookies and this alert no longer appears.

<a id="row-115"></a>
## 115. privacy-issue-4866

**主题代码：** PRIVACY-D

**开放代码：** API位置降精度；人口密度相关风险；稳定展示与匿名强度权衡

**逐条判断：** 要求API也遮蔽坐标，已有匿名/精度功能获认可；后续澄清为网格吸附非随机，4级约100m可能过精确，统一尺度不适混合密度；动态方案进入UX待办。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 基本功能已有，适应密度改进待办

**原文证据：**

位置 `4058:4090`：

> The function is not a randomiser

位置 `4268:4333`：

> snaps the coordinates to the nearest intersection point in a grid

<a id="row-116"></a>
## 116. privacy-issue-8286

**主题代码：** PRIVACY-E

**开放代码：** 本地轨迹保留选择；默认最小化；法律适用争议

**逐条判断：** 新增24小时滚动轨迹受质疑，要求首启询问及禁用；回复强调不外发只本地并认为GDPR不适用，该法律判断不当事实结论，最后并入3400。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 重复议题合并，无更改证据

**原文证据：**

位置 `1723:1747`：

> It stays on your device.

位置 `1957:1975`：

> duplicate of #3400

<a id="row-117"></a>
## 117. privacy-issue-8242

**主题代码：** PRIVACY-B, PRIVACY-I

**开放代码：** 第三方资源请求移除；供应链覆盖边界

**逐条判断：** 要求内置字体CSS避免联网；PR移除两个Monica自身调用，Laravel等依赖仍需上游处理，末确认5027修复，不能称完全无外部请求。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 原生调用已修复，依赖调用未处理

**原文证据：**

位置 `1767:1890`：

> I can see several instances of Google Fonts being called in Laravel and other vendor packages, but I haven't removed those.

<a id="row-118"></a>
## 118. privacy-issue-19537

**主题代码：** PRIVACY-A, PRIVACY-F, PRIVACY-H

**开放代码：** 公开身份上传默认选择；撤回偏好持久性

**逐条判断：** 密钥新增/身份编辑默认勾上传，用户上次取消后容易漏看，建议个人信息公开应opt-in；移至1847讨论。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 讨论合并，实施未知

**原文证据：**

位置 `1221:1317`：

> As personal information will be published, this should require an Opt-in rather than an Opt-out.

<a id="row-119"></a>
## 119. privacy-issue-5043

**主题代码：** PRIVACY-D, PRIVACY-I

**开放代码：** 匿名化工具跨平台执行失败

**逐条判断：** Windows不识别U参数阻止日志用户名替换，作者在EI6.2.0 snapshot确认验证。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 版本验证通过

**原文证据：**

位置 `1991:2036`：

> Verified in the latest EI 6.2.0 snapshot pack

<a id="row-120"></a>
## 120. privacy-issue-8761

**主题代码：** PRIVACY-A, PRIVACY-H, PRIVACY-I

**开放代码：** 交互前追踪cookie；必要性争议；主动客服与最小化权衡

**逐条判断：** 加载聊天组件尚未互动就设会话cookie；初提仅主动消息启用时才设置，后以返回识别和会话连续性为由短期不改；用户追问无对话何来连续性，无回答。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 短期拒改，必要性争议未解

**原文证据：**

位置 `3063:3140`：

> Closing this as the change is not something we can implement in a short term.

位置 `3346:3418`：

> Why do you need conversation continuity if the user has never interacted

<a id="row-121"></a>
## 121. privacy-issue-2271

**主题代码：** PRIVACY-B

**开放代码：** 隐私告知迁移；保留披露更新

**逐条判断：** 迁wiki至官网并改名notice，建议源码保留说明应随HTTP日志轮转现状更新；末确认页面上线，具体措辞更新未展示。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 官网页面已上线，具体文本未知

**原文证据：**

位置 `1381:1411`：

> The page is up on dartlang.org

位置 `1044:1097`：

> no longer retained beyond the HTTP log rotation times

<a id="row-122"></a>
## 122. privacy-issue-11297

**主题代码：** PRIVACY-I

**开放代码：** 全局隐私偏好信号；管辖适用与责任分配

**逐条判断：** 请求GPC优先覆盖USP值并允许publisher配置；咨询法律后暂决定只传header由竞价方处理，服务端另议，另一人建议publisher统一转换，JS不实施所请。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 暂不改JS，服务端及发布方另处理

**原文证据：**

位置 `1860:1946`：

> just pass the GPC HTTP header through the system and let bidders deal with it for now.

位置 `2151:2177`：

> nothing to do on Prebid.js

<a id="row-123"></a>
## 123. privacy-issue-8905

**主题代码：** PRIVACY-A, PRIVACY-B, PRIVACY-H

**开放代码：** 地域cookie界面差异；访问绑定同意

**逐条判断：** EU/EEA非UK要求全页遮罩且接受前不能操作，接受写两cookie；唯一评论划掉阻塞链接，无完成验证。不可把强制同意界面写成支持自由拒绝。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 请求，完成未知

**原文证据：**

位置 `1189:1276`：

> It is not possible for the user to interact with the page without accepting the cookies

<a id="row-124"></a>
## 124. privacy-issue-18429

**主题代码：** PRIVACY-B, PRIVACY-G, PRIVACY-H, PRIVACY-I

**开放代码：** 位置权限用途解释；平台后台限制；隐私信任与耗电

**逐条判断：** 起初指GPS耗电及无必要，维护者解释用低精度位置唤醒后台而非图片再定位，用户要求明确不用于跟踪；答应改善说明但未给上线证据。2019仍报耗电，另提PhotoKit替代未答，不能编码为已解决。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 用途解释与告知改进承诺，后续问题仍报

**原文证据：**

位置 `6214:6258`：

> you are not using it to track their position

位置 `6993:7083`：

> technically there's not much we can do except for allowing to disable background uploading

<a id="row-125"></a>
## 125. privacy-issue-18913

**主题代码：** PRIVACY-E

**开放代码：** 交互对象数据留存透明度

**逐条判断：** 询问InstaPy是否永久保存所互动用户资料，只有stale提醒；用户猜测暂存不是实证。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 问题未获回答

**原文证据：**

位置 `1078:1127`：

> I was wondering if any data is saved permanently.

<a id="row-126"></a>
## 126. privacy-issue-4829

**主题代码：** PRIVACY-D

**开放代码：** 邮件内部路径脱敏遗漏

**逐条判断：** 内部发信headers未替换，作者后称仍存在，维护者要求当前版本详情例子未获补充，自动过期。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 报告未解决，待复现细节

**原文证据：**

位置 `1771:1797`：

> this issue still persists.

位置 `1998:2038`：

> Need details and example in _this_ issue

<a id="row-127"></a>
## 127. privacy-issue-5457

**主题代码：** PRIVACY-E, PRIVACY-I

**开放代码：** 不活跃账户期限清理；历史归属完整性；研究档案保留边界

**逐条判断：** 提出默认关的按期合并至管理员，评论担心有投稿审核历史会污染管理员归属，限制完全无参与账号，并争论遗忘权是否要求自动删及姓名档案必要性。末无兴趣关闭。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 未实现，缺兴趣关闭

**原文证据：**

位置 `4162:4196`：

> Closing this for lack of interest.

位置 `2665:2724`：

> that data would be added to the Admin's own historical data

<a id="row-128"></a>
## 128. privacy-issue-7663

**主题代码：** PRIVACY-B, PRIVACY-C, PRIVACY-D

**开放代码：** 无cookie分析；IP匿名化与反滥用期限；隐私告知

**逐条判断：** 由GA未询问同意质疑起，维护者报告已匿名IP且不用cookie，反滥用原IP日志留30天；后拟FAQ和首页链接。技术变更有报告，法律合规与不可识别是参与者观点，FAQ上线未见。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 分析配置报告改变，告知建议待确认

**原文证据：**

位置 `1991:2061`：

> We are now running google analytics with anonymized IPs and no cookies

位置 `2132:2174`：

> short-term (30 days retention) logs of IPs

<a id="row-129"></a>
## 129. privacy-issue-5410

**主题代码：** PRIVACY-B, PRIVACY-E

**开放代码：** 日志长期保留文档

**逐条判断：** 仅标题要求记录长期保留，缺正文，不能判断期限或遗忘权具体机制。

**材料可用性：** metadata_only。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 证据缺失，结果未知

**原文证据：**

位置 `69:106`：

> Document long-term retention for logs

<a id="row-130"></a>
## 130. privacy-issue-18425

**主题代码：** PRIVACY-B, PRIVACY-F, PRIVACY-H, PRIVACY-I

**开放代码：** 管理员身份披露；帮助流程与保密权衡

**逐条判断：** 组织归属帮助文案改进延伸到是否邮件提供管理员地址，部分遮挡甚至有无管理员也遭反对，隐私支线拆出；末发布说明仅帮助文本已加，不代表披露功能上线。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 帮助文本完成，身份披露另议

**原文证据：**

位置 `7155:7181`：

> A clear help text is added

位置 `5542:5594`：

> I'm very against disclosing any level of information

<a id="row-131"></a>
## 131. privacy-issue-18644

**主题代码：** PRIVACY-B, PRIVACY-C, PRIVACY-I

**开放代码：** 文档站分析必要性争论；追踪告知；过度收集倾向

**逐条判断：** 为文档改进拟GA，评论要求告诉读者追踪，讨论人口统计及即使暂不用也想多收集；建议条款或cookie提示，最后迁移文档仓库，无部署证据。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 议题迁移

**原文证据：**

位置 `3844:3893`：

> I prefer having more data even if I don't use it.

位置 `5650:5690`：

> moved to coala-analyzer/documentation#44

<a id="row-132"></a>
## 132. privacy-issue-11387

**主题代码：** PRIVACY-I, PRIVACY-Z

**开放代码：** 法律主题未具体化

**逐条判断：** 只有ccpa标题，无法分解需求、机制或结果，不由标签推断。

**材料可用性：** metadata_only。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 证据缺失，结果未知

**原文证据：**

位置 `65:69`：

> ccpa

<a id="row-133"></a>
## 133. privacy-issue-14235

**主题代码：** PRIVACY-H

**开放代码：** 本地处理与主动上传；默认行为澄清；缓存留存不确定

**逐条判断：** 用户要求离线截图编辑、本地默认、上传opt-in及清缓存；答复离线下载已有，每次选择且不点save不上传，编辑在网站尚未正式发布所以不离线；缓存仅认为未存并索要细节。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 既有行为解释，离线编辑未提供

**原文证据：**

位置 `2640:2703`：

> If you don't click the 'save' button the image doesn't get sent

位置 `2371:2431`：

> There is no default, you have to choose an option each time.

<a id="row-134"></a>
## 134. privacy-issue-2160

**主题代码：** PRIVACY-B, PRIVACY-H

**开放代码：** 多语言隐私与法律链接配置

**逐条判断：** 提页脚加privacy/legal键及翻译，作者已有PR357；两评论都是机器人，没有合并/部署声明。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 已有提案PR，完成未知

**原文证据：**

位置 `2841:2892`：

> adding the keys as allowed keys to the `Footer.vue`

<a id="row-135"></a>
## 135. privacy-issue-8854

**主题代码：** PRIVACY-A, PRIVACY-I

**开放代码：** 客户二次用途同意；偏好画像与营销；cookie拒绝权

**逐条判断：** 希望订餐支付前同意后给配送公司订单频率餐厅金额资料用于调查推荐，另请求完单调查邮件；评论补cookie应可接受拒绝，无实施。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 请求，完成未知

**原文证据：**

位置 `853:903`：

> Client's data cannot be used by delivery companies

位置 `2099:2132`：

> **Accept** or **Decline** cookies

<a id="row-136"></a>
## 136. privacy-issue-14271

**主题代码：** PRIVACY-A, PRIVACY-B, PRIVACY-H

**开放代码：** 注册条款确认；内容与界面交付依赖

**逐条判断：** 注册复选框确认阅读条款并提GDPR，界面已有信息/链接位置但等待文案与目标页面，不等同完整条款同意上线。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 界面占位完成，内容待补

**原文证据：**

位置 `1726:1789`：

> there is now a place to put the message and a link to somewhere

<a id="row-137"></a>
## 137. privacy-issue-2133

**主题代码：** PRIVACY-B

**开放代码：** 选项页隐私告知

**逐条判断：** 仅标题要求选项页包含声明，无正文，具体内容与结果未知。

**材料可用性：** metadata_only。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 证据缺失，结果未知

**原文证据：**

位置 `65:101`：

> Options page: Include privacy notice

<a id="row-138"></a>
## 138. privacy-issue-21228

**主题代码：** PRIVACY-D, PRIVACY-E, PRIVACY-G, PRIVACY-I

**开放代码：** 本地生成替代第三方处理；客户数据跨境与删除控制；自托管预期；账单完整性权衡

**逐条判断：** 读完26评论：附件PDF用phantomjscloud而网页预览本地，暴露客户税号价格并需公网，用户质疑跨境及第三方删除保证。停附件替代又引发客户拿到不可变账单争议，最终双方确认修复且下个大版本发布，另给本地二进制Docker配置。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 本地生成修复确认，正式版本待发布

**原文证据：**

位置 `13853:13887`：

> Thank you so much for fixing this.

位置 `14140:14176`：

> it will be in our next major release

位置 `9512:9561`：

> I can't guarantee removal of their sensitive data

<a id="row-139"></a>
## 139. privacy-issue-8971

**主题代码：** PRIVACY-A, PRIVACY-B, PRIVACY-H

**开放代码：** 同意管理旧浏览器兼容；偏好存储失效

**逐条判断：** 旧IE等缺polyfill致同意组件错误；初修IE11看似有效后发现cookie不存每次全勾，再补Set确认124有效；作者自改到IE9，维护者最终确认IE10/11，IE9仅可能。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** IE10/11支持完成，IE9未确定

**原文证据：**

位置 `4744:4802`：

> the consent banner appears again, and all apps are checked

位置 `6598:6643`：

> compatible with IE10 & IE11 (and possibly IE9

<a id="row-140"></a>
## 140. privacy-issue-11529

**主题代码：** PRIVACY-A, PRIVACY-E, PRIVACY-I

**开放代码：** 删除请求跨代身份关联；法规期限

**逐条判断：** 在Glean删除ping补旧telemetry client id以涵盖历史追踪，6月期限，评论仅关联iOS与询进度，无完成确认。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 请求，完成未知

**原文证据：**

位置 `65:128`：

> Add the legacy telemetry client id to the deletion request ping

<a id="row-141"></a>
## 141. privacy-issue-3036

**主题代码：** PRIVACY-A, PRIVACY-B, PRIVACY-C, PRIVACY-H

**开放代码：** 第三方遥测告知；服务器控制与客户端刷新；默认开启争议

**逐条判断：** 解释Segment由服务器设置可关并声称不收PII，用户要求opt-in；后关闭仍DNS请求，另一用户reload后错误消失并提证书弱密钥。保留实际生效依赖与报告范围，非验证无PII。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 既有开关说明，刷新替代报告有效

**原文证据：**

位置 `4377:4424`：

> I had to reload (View->Reload) my front end app

位置 `2412:2467`：

> it should be an opt-in option instead of an opt-out one

<a id="row-142"></a>
## 142. privacy-issue-8932

**主题代码：** PRIVACY-A, PRIVACY-B, PRIVACY-H

**开放代码：** 地域cookie提示规则；跨呈现渠道一致性

**逐条判断：** 要求UK保持现状、EU/EEA全页新提示并设cookie；讨论其他地区在ORBIT无提示而Simorgh普通页全用户有、AMP仅EU/EEA，因上线捷径产生差异；末依赖3494阻塞。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 方案，依赖阻塞

**原文证据：**

位置 `2637:2708`：

> we show the cookie banner to all canonical users and only EU/EEA on AMP

位置 `2941:2951`：

> Blocked on

<a id="row-143"></a>
## 143. privacy-issue-1070

**主题代码：** PRIVACY-D, PRIVACY-E, PRIVACY-I

**开放代码：** 区块链删除约束；链下个人数据与证明；哈希假名化边界

**逐条判断：** 询问Indy合规研究，回复仅通用协作论文而无具体评估；用户建议PII链下、ZKP链上，并讨论hash是否匿名的法律技术区分，未给实现证据；转Jira。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 研究与设计建议，迁移跟踪

**原文证据：**

位置 `2588:2619`：

> only verifiers of personal data

位置 `2691:2755`：

> simple hashes are considered pseudonymization, not anonymization

<a id="row-144"></a>
## 144. privacy-issue-18911

**主题代码：** PRIVACY-A, PRIVACY-B, PRIVACY-I

**开放代码：** 注册主动同意；隐私条款确认

**逐条判断：** 要求注册前必须本人勾选政策和条款，回复判重复1338，未确认实现。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 重复合并

**原文证据：**

位置 `2795:2814`：

> mandatory checkmark

位置 `3592:3610`：

> duplicate of #1338

<a id="row-145"></a>
## 145. privacy-issue-7611

**主题代码：** PRIVACY-F, PRIVACY-G

**开放代码：** 开发项目列表暴露；本地工具网络部署边界

**逐条判断：** 站点列表在开放80/443乃至LAN让他人了解开发项目，维护者确认合并用户PR，具体控制方式未展示。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** PR已合并

**原文证据：**

位置 `1644:1666`：

> I have merged your PR!

<a id="row-146"></a>
## 146. privacy-issue-11475

**主题代码：** PRIVACY-A, PRIVACY-B, PRIVACY-I

**开放代码：** 地域合规扩展；适用地域解释

**逐条判断：** 要求AMP支持CCPA，后明确发布为扩展；用户要求全美而非加州，回复组件已支持全美，不能由此作法律适用认定。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 扩展已发布

**原文证据：**

位置 `2042:2066`：

> Released as an extension

位置 `2706:2734`：

> it will work with entire USA

<a id="row-147"></a>
## 147. privacy-issue-11975

**主题代码：** PRIVACY-F, PRIVACY-I

**开放代码：** 通知地址复用与滥用；账号存在性泄露；最小披露接口

**逐条判断：** 多用户可设他人联系方式引spam，唯一约束又可抢占地址；显示谁使用被批隐私泄露，即使布尔也可能枚举账户。最终提按现有destination主键回布尔，不显示身份；无实现确认。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 缩减披露的设计共识

**原文证据：**

位置 `2611:2645`：

> could still be a breach of privacy

位置 `3907:3931`：

> simply returns a boolean

<a id="row-148"></a>
## 148. privacy-issue-14247

**主题代码：** PRIVACY-D, PRIVACY-E

**开放代码：** 按年自动匿名化；统计用途残留地理字段

**逐条判断：** 配置X年后清姓名地址邮箱电话，姓改No longer retained，保留town/county/postcode供统计。为要求非验证，保留邮编不能推断完全不可识别。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 设计要求，实施未知

**原文证据：**

位置 `1418:1499`：

> the town/county and postcode fields are left intact for statistics and reporting.

<a id="row-149"></a>
## 149. privacy-issue-1171

**主题代码：** PRIVACY-B, PRIVACY-I, PRIVACY-Y

**开放代码：** IP衍生定位透明度；同意与合法依据争论；法律判断证据冲突

**逐条判断：** 读完19评论：发起者指地图未经同意显示精确位置，维护者称IP近似且不留存不共享；另参与者又称仅边缘服务器位置，与前述解释不一致。围绕处理定义、合法利益、扫描报告争论，作者最终自行关闭未承认特定结论，无代码修复。不把扫描10%或争议法律解释当事实。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 争论后作者关闭，技术事实部分有分歧

**原文证据：**

位置 `9962:10021`：

> it has a broad approximation of it based on your IP address

位置 `16834:16857`：

> I'm closing this issue.

<a id="row-150"></a>
## 150. privacy-issue-2240

**主题代码：** PRIVACY-A, PRIVACY-B, PRIVACY-H, PRIVACY-I

**开放代码：** 同意审计记录预期；表单门槛与重复记录权衡

**逐条判断：** 联系表勾选政策后后台无日志，用户从告知文案预期应留证；回复认为不勾不能发、已注册者已确认不需重复日志，最终明确预期行为关闭。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 按预期行为关闭

**原文证据：**

位置 `4504:4533`：

> Closed as expected Behaviour.

位置 `2692:2740`：

> If you don't confirm you can't send the message.

<a id="row-151"></a>
## 151. privacy-issue-14188

**主题代码：** PRIVACY-E, PRIVACY-F, PRIVACY-I

**开放代码：** 删除与停用区别；共有人内容保留；匿名化替代及人工受理

**逐条判断：** 要求删账号全部PII而非停用，讨论共享/公开计划及关联答案角色，转述专家意见只清姓名email且邮件受理即可。结局1489取代，不能把法律意见当验证数据全清。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 被后续议题取代

**原文证据：**

位置 `1316:1388`：

> looks like it requests the ability to disable an account, not delete it.

位置 `3125:3160`：

> related issue #1489 supersedes this

<a id="row-152"></a>
## 152. privacy-issue-2421

**主题代码：** PRIVACY-A, PRIVACY-B, PRIVACY-E, PRIVACY-H

**开放代码：** 操作文案导致意外上传；本地与云端语义；上传禁用偏好；访问与保留控制；优先级延误

**逐条判断：** 读完24评论：Save上传而Download本地造成用户多次误传敏感后台截图；维护者承认文案问题，禁上传偏好已在Nightly待60，改名PR4963推进，解释随机URL/UUID、两周自动删及员工访问边界。最后Firefox66仍显示Save，不能以中途感谢当最终修复成功。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 禁上传选项已有，改名最后仍被报告未生效

**原文证据：**

位置 `20676:20725`：

> The **"upload" button still reads "save"** for me

位置 `19176:19232`：

> our quarterly goals tend to focus on adding new features

<a id="row-153"></a>
## 153. privacy-issue-8316

**主题代码：** PRIVACY-A, PRIVACY-F, PRIVACY-G, PRIVACY-H

**开放代码：** 麦克风自主控制；可拒绝协助提示；可用性与隐私边界

**逐条判断：** 家庭会议用户难找解除静音按钮，作者明确求显眼询问弹窗非强制开麦；支线有人提课堂主持强制控制加告知，未采纳证据。最后说明主持已可ask to unmute，保留同意交互。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 询问解除静音已提供

**原文证据：**

位置 `8755:8789`：

> Moderators can now "ask to unmute"

位置 `5192:5240`：

> they can always decline, it's a conscious action

<a id="row-154"></a>
## 154. privacy-issue-20644

**主题代码：** PRIVACY-A, PRIVACY-H, PRIVACY-I

**开放代码：** 同意组件间阻塞；脚本门控误伤；表单确认提交失败

**逐条判断：** 读完16评论：原保存卡住后变前台不显示/勾选不传；初疑主题JS、表单外位置，最终一实例定位EU Cookie Law自动挡全部脚本，未登录更明显；接受弹窗刷新恢复，使用者临时关Auto Block，非GDPR插件统一修复。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 实例根因确认及配置绕过

**原文证据：**

位置 `8686:8744`：

> Confirming the popup and reloading the page got it working

位置 `8799:8843`：

> I switched Auto Block off for the time being

<a id="row-155"></a>
## 155. privacy-issue-2476

**主题代码：** PRIVACY-H, PRIVACY-Z

**开放代码：** 不可见复选框阻碍注册；隐私关联证据不足

**逐条判断：** 仅标题支持注册被不可见checkbox阻碍，无法确认框的用途是否隐私同意，不依据matched关键词补全。

**材料可用性：** metadata_only。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 证据缺失，结果未知

**原文证据：**

位置 `65:107`：

> Users cannot register - invisible checkbox

<a id="row-156"></a>
## 156. privacy-issue-4007

**主题代码：** PRIVACY-D, PRIVACY-F, PRIVACY-G

**开放代码：** 令牌数据最小化与功能耦合；身份判别字段

**逐条判断：** 去掉email/user_name希望按需从userinfo取，但email存在性被用于判断用户token导致空principal/500；维护者承认bug并给完成commit，后解释用user_id区分client token而sub可能是client_id。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 修复声明并解释设计

**原文证据：**

位置 `4816:4869`：

> Finished via e59544a60a2df62874e07a086bda1cd63d2d789e

位置 `5614:5646`：

> we use the presence of `user_id`

<a id="row-157"></a>
## 157. privacy-issue-4010

**主题代码：** PRIVACY-B, PRIVACY-D, PRIVACY-G, PRIVACY-I

**开放代码：** 文件元数据去匿名风险；证据保真与隐私冲突；接收方信任边界；易懂风险告知；处理攻击面

**逐条判断：** 读完9评论：举报文件GPS/作者元数据可识别来源，主张客户端清理；维护者因格式RCE、无法区分证据与身份元数据且无法保证全清，现阶段交受信记者处理，建议安全副本与原本并存。讨论不同国家威胁模型、PGP告知难懂、翻译负担，未来可列元数据让用户/管理员选择；无实际清理或文案部署确认。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 当前不自动清理，研究与告知改进计划

**原文证据：**

位置 `7140:7180`：

> to not remove automatically the metadata

位置 `12016:12079`：

> It is technically impossible to discern good from bad metadata.

<a id="row-158"></a>
## 158. privacy-issue-7571

**主题代码：** PRIVACY-G, PRIVACY-I, PRIVACY-Y

**开放代码：** 静态扫描泄露告警；受保护存储语境

**逐条判断：** Fortify因token写入外部位置报privacy violation；维护者认为使用Apple keychain故误报并建议联系Apple。仅双方陈述，不认定真实泄露或独立验证误报。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 维护者判疑似误报

**原文证据：**

位置 `1874:1944`：

> We believe this is false positive because we are using Apple keychain.

<a id="row-159"></a>
## 159. privacy-issue-7666

**主题代码：** PRIVACY-G, PRIVACY-Y

**开放代码：** 未经证实的账户隐私报告；问题边界与证据不足

**逐条判断：** 用户从插件错误延伸至邮箱/密码恢复及他人项目等怀疑，缺清楚复现关联；维护者认为无法识别具体问题且非AMO范围，关闭。不能将怀疑转换为证实入侵或数据泄露。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 范围外关闭，报告未证实

**原文证据：**

位置 `3401:3463`：

> doesn't really give us any idea of exactly what the problem is

<a id="row-160"></a>
## 160. privacy-issue-20437

**主题代码：** PRIVACY-A, PRIVACY-B, PRIVACY-H, PRIVACY-I

**开放代码：** cookie保存期限配置；跨地域法规解释不确定

**逐条判断：** 要求无限期限cookie改6月，后有参与者质疑通用6月法律依据；作者称公司法务告知且承认变化可能，最终确认Volto期限已可配置，不把6月当确定法律。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 期限配置已提供

**原文证据：**

位置 `4316:4364`：

> the expiration time is configurable in volto now

位置 `2942:2971`：

> Do you have sources for this?

<a id="row-161"></a>
## 161. privacy-issue-14067

**主题代码：** PRIVACY-I

**开放代码：** 合规需求发现与拆解

**逐条判断：** 仅总体需找清GDPR要求，后说明长期讨论转更大项目并会开小议题；没有具体机制完成。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 并入更大项目

**原文证据：**

位置 `891:933`：

> Need to find out all of what we have to do

位置 `1552:1579`：

> smaller issues will be made

<a id="row-162"></a>
## 162. privacy-issue-4421

**主题代码：** PRIVACY-F, PRIVACY-G, PRIVACY-H, PRIVACY-I

**开放代码：** 机器人音视频知情控制；保护缺失导致停用功能

**逐条判断：** Skype机器人群呼不再接通，维护者确认7月底禁用，因为客户端不能通知其他参加者机器人可听看；一对一仍允，群文字聊天仍可，无恢复时间。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 为隐私暂停群呼能力

**原文证据：**

位置 `4006:4094`：

> privacy controls in place to inform the participants that a bot can hear and/or see them

<a id="row-163"></a>
## 163. privacy-issue-8272

**主题代码：** PRIVACY-F, PRIVACY-I

**开放代码：** 头像按受众披露；协议能力与界面缺失；重复判定修正

**逐条判断：** 请求朋友家庭看人像其他人看替代，最初答房间头像已有但UI无且重复；后修正目标议题并质疑按用户跨房间不同于按房间，作者确认需要受众控制。无完成证据。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 需求澄清，受众控制未确认

**原文证据：**

位置 `2813:2852`：

> shown to specific users, not just rooms

位置 `1670:1699`：

> There is just no UI for this.

<a id="row-164"></a>
## 164. privacy-issue-18964

**主题代码：** PRIVACY-D, PRIVACY-I

**开放代码：** 城市轨迹接收治理；目的限制；静态数据混淆；授权及再共享；公开记录请求风险

**逐条判断：** 公开信要求LADOT说明轨迹安全存储用途与人员流程，限制访问及第三方转交，担心精准GPS时间路线再识别及公开记录法披露；唯一回复仅README加入指引，不能声称各治理控制实际落实。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 处理指引链接已添加，治理实施未验证

**原文证据：**

位置 `4933:4983`：

> Trip Data should be obfuscated when stored at rest

位置 `5721:5763`：

> Additional data sharing must be restricted

位置 `7706:7764`：

> link to the guidelines for handling the data in the README

<a id="row-165"></a>
## 165. privacy-issue-18621

**主题代码：** PRIVACY-F, PRIVACY-G

**开放代码：** 自动外链探测暴露IP；主动点击边界；内联显示选择

**逐条判断：** 最初认为两个收件者显示不同被作者纠正，两者均链接；维护者解释自动HEAD可被独特URL定位且XMPP服务器中转不直接泄露双方IP，拟opt-in显示。最终OSX beta有偏好，iOS待测试移植。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** OSX beta实现，iOS计划中

**原文证据：**

位置 `5292:5356`：

> I have added a preference to enable this in the latest OS X beta

位置 `3655:3687`：

> They don't even have to click it

<a id="row-166"></a>
## 166. privacy-issue-5548

**主题代码：** PRIVACY-E, PRIVACY-I

**开放代码：** 网页归档与遗忘权张力；项目范围限制

**逐条判断：** 请求Internet Archive保存消失活动页，回复无法强制保留且遗忘权更难，欢迎PR但预期少用；最终暂不在模板处理，将来重访网站方案。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 暂不处理

**原文证据：**

位置 `2124:2201`：

> for the time being I don't think there is much we can do on the template side

<a id="row-167"></a>
## 167. privacy-issue-1625

**主题代码：** PRIVACY-G

**开放代码：** 告知随加密备份能力更新

**逐条判断：** 将将来可选密钥备份改为现在已可用，保留只有用户恢复密钥可解及丢失风险，末明确文本完成；是声明更新，不独立验证加密。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 告知已更新

**原文证据：**

位置 `2619:2632`：

> This got done

位置 `2001:2061`：

> Users can optionally back up an encrypted copy of their keys

<a id="row-168"></a>
## 168. privacy-issue-18958

**主题代码：** PRIVACY-B, PRIVACY-H, PRIVACY-I

**开放代码：** 应用商店隐私披露；实际凭据流核查；告知入口与强制接受争论；跨平台展示

**逐条判断：** 读完17评论：AppStore要求声明，讨论Help/About及首启强制接受，后者未采纳证据。核查IDE仅会话内存存凭据，Git/SVN可能系统keychain存；生成政策后HTML内嵌失败，最终官网上线且Mac/Windows均外部浏览器打开验证。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 官网及应用链接上线并验证

**原文证据：**

位置 `12271:12377`：

> I confirmed that Moonshine now opens the Privacy Policy in a browser window/tab on both macOS and Windows.

位置 `7249:7292`：

> the entered credential stores to the memory

<a id="row-169"></a>
## 169. privacy-issue-18560

**主题代码：** PRIVACY-B, PRIVACY-C, PRIVACY-I

**开放代码：** 依赖组件外部连接透明度；概括怀疑待具体化

**逐条判断：** 询Electron用Chromium是否连Google或传数据，答复只用content及选定功能并要求具体问题，用户进一步界定任何外部连接；合并7306，未验证实际传输。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 合并讨论，实际行为未证实

**原文证据：**

位置 `4174:4189`：

> Merging this to

位置 `2869:2901`：

> mainly uses the [content module]

<a id="row-170"></a>
## 170. privacy-issue-3841

**主题代码：** PRIVACY-D, PRIVACY-E, PRIVACY-I

**开放代码：** 日志字段最小化；时间降精度；历史清理；插件替代与多表覆盖

**逐条判断：** 读完21评论：要求不留IP/UA且秒级时间降到天，保国家统计；核心偏好插件不加开关，最初插件不足，后社区给空字段hook但需兼顾yourls_url新增短链者IP，不只点击日志。历史清理及时间精度无完成证据，法律判断有争论。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 社区插件替代，核心默认未改、覆盖仍讨论

**原文证据：**

位置 `11206:11264`：

> then adding new short URLs would still record IP addresses

位置 `10313:10344`：

> make the timestamp more inexact

<a id="row-171"></a>
## 171. privacy-issue-2956

**主题代码：** PRIVACY-A, PRIVACY-B, PRIVACY-F, PRIVACY-H

**开放代码：** 公开属性前确认与风险告知

**逐条判断：** 用户属性可能PII，拟公开前确认提示；仅stale无实施。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 请求，完成未知

**原文证据：**

位置 `1064:1120`：

> add a confirmation before making a user attribute public

<a id="row-172"></a>
## 172. privacy-issue-12607

**主题代码：** PRIVACY-A, PRIVACY-H, PRIVACY-I, PRIVACY-Y

**开放代码：** 扩展覆盖浏览器隐私选择；链接检查与保护冲突；方案撤回

**逐条判断：** 2.0关追踪保护避免书签误报，审查后当天2.0.1回退；先拟opt-in重新引入，2023最终放弃改设置转提醒保护影响结果，并入109。不能把早期计划写成已实现opt-in。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 回退控制，最终改告知方案

**原文证据：**

位置 `2671:2724`：

> This change was reverted in Bookmarks Organizer 2.0.1

位置 `3356:3383`：

> Instead I will add a notice

<a id="row-173"></a>
## 173. privacy-issue-4930

**主题代码：** PRIVACY-B, PRIVACY-C, PRIVACY-D

**开放代码：** 匿名IP配置值兼容

**逐条判断：** 要求anonymizeIP值从True改Set，评论审查后明确0.9.97.12已推送，不推断外链未见具体原因。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 版本发布声明

**原文证据：**

位置 `1603:1622`：

> Pushed in 0.9.97.12

<a id="row-174"></a>
## 174. privacy-issue-17478

**主题代码：** PRIVACY-G, PRIVACY-H, PRIVACY-I

**开放代码：** cookie保护与认证兼容；隐私过滤误拦；错误提示多因混同；部分修复范围

**逐条判断：** 读完64评论包括所有配置/栈。会话cookie报错涵盖HTTPS后HTTP安全cookie、会话过期、路径探测、扩展改cookie及uBlock Cookiemonster误挡js.cookie.js，不能单一归因；有人绕过token检查并非合适隐私修复。4.9.2发布部分修复但多人仍复现，13172/15634另追踪。主体是认证可靠性，非cookie同意告知问题。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 部分修复发布，边界问题迁移

**原文证据：**

位置 `18505:18552`：

> Source seems to be Fanboy’s Cookiemonster List.

位置 `44012:44064`：

> But not all the issues, still some edge cases to fix

<a id="row-175"></a>
## 175. privacy-issue-14201

**主题代码：** PRIVACY-D, PRIVACY-G, PRIVACY-I

**开放代码：** 身份撤销所需最小数据保护；现有哈希强度再评估

**逐条判断：** 原拟增强用于撤销/防重复验证数据的加密哈希，后称现有强度好于预想暂可接受，未来移隐私/GDPR epic；无新算法变更。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 现状暂接受，未来改进另议

**原文证据：**

位置 `1370:1421`：

> the hashing system is stronger than what we thought

位置 `2015:2031`：

> it is ok for now

<a id="row-176"></a>
## 176. privacy-issue-7448

**主题代码：** PRIVACY-D, PRIVACY-I

**开放代码：** 离线地理编码；第三方位置发送最小化；平台依赖可靠性

**逐条判断：** 照片反查位置用Geocoder依赖服务且可能联网外发，实际只需国家，拟复用离线coordinates2country；已创建5093未见合并声明，风险为可能非已测。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** PR已提出，完成未知

**原文证据：**

位置 `1613:1656`：

> We only need the country, not full address.

位置 `2470:2488`：

> I created PR #5093

<a id="row-177"></a>
## 177. privacy-issue-8783

**主题代码：** PRIVACY-A, PRIVACY-E, PRIVACY-H

**开放代码：** 无cookie追踪与退出状态；CSRF保护cookie必要性；偏好记忆权衡

**逐条判断：** 用户在无cookie模式退出时见_pk_id/_pk_ses，澄清允许安全与偏好cookie；维护者检查4.0 disableCookies不应设跟踪cookie、3.14或已修，作者待升级未回结果。2022另问全局无cookie仍需SESSID，无回答。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 新版行为检查报告，用户验证及后续问题未完

**原文证据：**

位置 `3804:3841`：

> MATOMO_SESSID is needed to avoid CSRF

位置 `5541:5594`：

> there should not be any `_pk_id` or `_pk_sess` cookie

<a id="row-178"></a>
## 178. privacy-issue-3997

**主题代码：** PRIVACY-B, PRIVACY-I

**开放代码：** 隐私政策完整披露；主动被动收集；广告画像和再共享；退出方式

**逐条判断：** 全文阅读拟政策：主动联系方式支付和人口统计，自动IP浏览行为、cookie/beacon及跨站广告；披露供应商/同理念组织/伙伴/法律/交易等广泛共享，给浏览器和广告退出及联系渠道。仅新增页及页脚/About链接要求，无部署评论；不可把政策承诺当实测行为。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 政策文案提案，发布未知

**原文证据：**

位置 `6761:6837`：

> with organizations, groups or causes that we believe have similar viewpoints

位置 `8794:8870`：

> Nothing herein restricts the sharing of aggregated or anonymized information

<a id="row-179"></a>
## 179. privacy-issue-349

**主题代码：** PRIVACY-A, PRIVACY-H

**开放代码：** 拒绝偏好未记住；cookie路径冲突；反复同意提示

**逐条判断：** 两可选类别关后不断弹窗，普通窗口与私密窗口差异定位/security路径cookie遮盖根cookie；维护者提模块修复，临时删除旧路径cookie，无最终部署验证。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 根因定位及修复提案，临时绕过

**原文证据：**

位置 `3249:3331`：

> Saving preferences does not change the value of the cookie for the /security path.

位置 `3609:3628`：

> have a fix proposed

<a id="row-180"></a>
## 180. privacy-issue-240

**主题代码：** PRIVACY-E, PRIVACY-G, PRIVACY-H, PRIVACY-I

**开放代码：** 用户脚本隐私提示自动化；脚本执行权限边界；动态代码信任风险；cookie清除与内存残留；功能维护验证

**逐条判断：** 读完85评论及全部TODO。起因为去烦人隐私弹窗，发展为脚本组件，94发布基础、99补修；为防外域动态代码窃取凭据，维护者最终拒unsafe-eval，即使每脚本或编译flag亦不入官方。后续大型DOM改动致离线快照卡顿，bfcache保留JS标识使删cookie未必去关联仅假设讨论未证实；尾部仍有文件导入/界面问题，未勾TODO另开。不是实现全套cookie隐私管理。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 基础发布及部分修复，unsafe-eval拒绝，余项另议

**原文证据：**

位置 `46604:46658`：

> UserScripts in Bromite will not support `unsafe-eval`.

位置 `62723:62784`：

> please file new feature requests for the unchecked TODO items

位置 `57388:57444`：

> I don't have the elements yet to be able to say for sure

<a id="row-181"></a>
## 181. privacy-issue-21349

**主题代码：** PRIVACY-F, PRIVACY-H, PRIVACY-I

**开放代码：** 学生姓名受众权限；隐私选择默认值

**逐条判断：** 要求Privacy Center默认false FERPA开关，开启后姓名仅管理员看、普通成员显示Suppressed后改星号；讨论更正法名及界面设计，无实现验证。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 设计要求，完成未知

**原文证据：**

位置 `1155:1216`：

> only show a user's Name to Admins if this user has FERPA True

位置 `2997:3034`：

> replace a FERPA member's name with *s

<a id="row-182"></a>
## 182. privacy-issue-11289

**主题代码：** PRIVACY-H, PRIVACY-I

**开放代码：** 隐私工具规则冲突；同意管理依赖阻断；第三方列表治理

**逐条判断：** Tealium虽Essential未阻但广告名单另阻导致页面和同意管理失败，维护者解释放行只是pass-through非全局允许，给站点信任替代；作者争议TMS非广告，末称commit应修复，无用户验证。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 修复commit预期解决，验证未见

**原文证据：**

位置 `3068:3102`：

> that is only a pass-through action

位置 `5032:5050`：

> Should be fixed by

<a id="row-183"></a>
## 183. privacy-issue-18399

**主题代码：** PRIVACY-D, PRIVACY-F, PRIVACY-G, PRIVACY-H, PRIVACY-I

**开放代码：** 隐藏文件意外共享；跨平台默认一致性；可选依赖的保护范围

**逐条判断：** Windows点目录原隐被回归共享，补回排除并加+h属性检测；缺win32file导致导入失败，双方接受其可选，点目录一致必保而属性检测依赖可用性。用户测试认可后合并。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 修复测试并合并，属性保护有依赖条件

**原文证据：**

位置 `3971:4004`：

> dot directories should be hidden.

位置 `4809:4827`：

> optional win32file

位置 `5335:5363`：

> Yes this looks good, thanks.

<a id="row-184"></a>
## 184. privacy-issue-18940

**主题代码：** PRIVACY-D

**开放代码：** 日志IP最小化；既有扩展点配置

**逐条判断：** 要求去除或匿名IP，答已有Target prefix可配；作者用返回null去前缀，另一人CMS冲突后解决。未更改框架默认。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 既有配置替代获使用确认

**原文证据：**

位置 `1811:1844`：

> I am using this to remove the IP.

位置 `2149:2178`：

> those have now been resolved!

<a id="row-185"></a>
## 185. privacy-issue-13503

**主题代码：** PRIVACY-F, PRIVACY-G, PRIVACY-I, PRIVACY-Y, PRIVACY-Z

**开放代码：** 软件完整性检查与发布来源；隐私关联不足

**逐条判断：** stable9 git安装缺signature.json导致核心与应用完整性检查失败，维护者解释git发布不带该密码学签名、不推荐生产；用户混淆git签名并追问公钥，未解决。无个人信息处理问题证据。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 预期行为说明，公钥追问未解决

**原文证据：**

位置 `9837:9886`：

> The git releases are not cryptographically signed

位置 `10175:10207`：

> I can't find your '49B6898C' key

<a id="row-186"></a>
## 186. privacy-issue-2942

**主题代码：** PRIVACY-D, PRIVACY-E, PRIVACY-F, PRIVACY-G, PRIVACY-I

**开放代码：** 配置公开前去标识；身份关联与提交元数据；模板与秘密分离；人工疏漏风险

**逐条判断：** 用户要公开dotfiles但隔离域名IPv6用户名和提交身份；完整讨论从clean/smudge替换转为模板与私有JSON分离，避免漏标敏感块直接提交，含时区去除、密钥离线和加密备份。作者演示模板bootstrap成功并提交示例PR；后人选择全私有另发精选副本。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 用户方案实现并分享，非通用自动保护保证

**原文证据：**

位置 `32524:32575`：

> The values would already not be there to begin with

位置 `45896:45917`：

> I think I'm done now.

<a id="row-187"></a>
## 187. privacy-issue-3871

**主题代码：** PRIVACY-D, PRIVACY-E, PRIVACY-F, PRIVACY-G, PRIVACY-I

**开放代码：** 字段级静态加密；存量数据再加密；密钥管理延期；加密检索限制

**逐条判断：** 表单字段由持久化代理加密后入库，前端明文，管理员可按表单重处理已有数据；完成项及文档支持实现，全文检索不含加密字段且仅精确匹配，换钥与多密钥管理延期。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 功能完成并文档化，密钥管理另项

**原文证据：**

位置 `5639:5662`：

> We defer Key management

位置 `2374:2432`：

> encrypted fields won't be included in the free text search

<a id="row-188"></a>
## 188. privacy-issue-20518

**主题代码：** PRIVACY-A, PRIVACY-H, PRIVACY-I

**开放代码：** 同意前阻断内容；隐私插件兼容

**逐条判断：** 请求WP Rocket兼容WeePie获cookie批准前阻断内容；仅一句正文无讨论，关闭不证明实现。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 关闭，实施未知

**原文证据：**

位置 `892:930`：

> block content until cookie is approved

<a id="row-189"></a>
## 189. privacy-issue-3023

**主题代码：** PRIVACY-C

**开放代码：** URL敏感令牌采集；分析数据最小化；自定义采集责任

**逐条判断：** 分享临时访问URL中的秘密令牌被Umami仪表盘展示，用户要控制上报。维护者先不赞同URL放秘密，后提供自定义tracker函数，说明系统无法自动判断过滤对象；无默认过滤修复。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 提供自定义采集替代

**原文证据：**

位置 `912:984`：

> URLs contain secret tokens that shouldn't be visible via Umami dashboard

位置 `2296:2329`：

> writing your own tracker function

<a id="row-190"></a>
## 190. privacy-issue-2308

**主题代码：** PRIVACY-B, PRIVACY-Z

**开放代码：** 隐私说明更新；仅元数据可判

**逐条判断：** 仅标题Update privacy comment，能确认文档隐私说明更新请求，缺正文及四条原讨论，内容理由结果均不可判。

**材料可用性：** metadata_only。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 仅元数据，完成未知

**原文证据：**

位置 `65:87`：

> Update privacy comment

<a id="row-191"></a>
## 191. privacy-issue-8299

**主题代码：** PRIVACY-F, PRIVACY-G, PRIVACY-H, PRIVACY-I

**开放代码：** 内部消息意外外发；回复受众继承；界面语义与权限不一致

**逐条判断：** Odoo内部提及从通知回复变为普通消息邮件发给客户followers，多用户证实；维护者解释平面线程无法确定回复目标，讨论显式note按钮与配置，2021仍有人报告。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 持续报告，未见修复

**原文证据：**

位置 `2223:2293`：

> The reply has become a normal reply which is emailed to all followers.

位置 `4984:5007`：

> There is no real thread

<a id="row-192"></a>
## 192. privacy-issue-1384

**主题代码：** PRIVACY-B

**开放代码：** 隐私公告页面迁移

**逐条判断：** Zola页脚迁移任务包含Privacy Notice及其他法律页面，各项打勾；无隐私内容变更或数据处理证据。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 清单标记完成

**原文证据：**

位置 `1126:1176`：

> Privacy Notice (simple page, no specific template)

<a id="row-193"></a>
## 193. privacy-issue-8243

**主题代码：** PRIVACY-B, PRIVACY-I

**开放代码：** 插件隐私告知同步；管理者编辑控制；更新通知缺口

**逐条判断：** Facebook插件作者希望hook自动扩展隐私政策，避免插件更新遗漏；维护者担心剥夺期刊管理者文字控制，讨论建议文本、可选自动和链接插件政策。多年后过时关闭转论坛，无实现。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 过时关闭，设计未落地

**原文证据：**

位置 `2642:2700`：

> would take control out of the hands of the Journal Manager

位置 `5093:5118`：

> Closing this as outdated.

<a id="row-194"></a>
## 194. privacy-issue-8839

**主题代码：** PRIVACY-A, PRIVACY-B, PRIVACY-H, PRIVACY-I

**开放代码：** 追踪告知与退出诉求；告知替代主动选择；选择状态持久化；政策链接作用域

**逐条判断：** 初始匿名用户故事要求退出大多数追踪，后续首版要求关闭记忆、使用即接受文案、政策链接按当前社区生成及法律咨询。不能由横幅实现推断退出功能已实现，第三方不共享是建议文案声明。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 首版及修改讨论，退出机制未证实

**原文证据：**

位置 `953:987`：

> option to opt out of most tracking

位置 `2349:2399`：

> By using this site, you accept this use of cookies

<a id="row-195"></a>
## 195. privacy-issue-2286

**主题代码：** PRIVACY-A, PRIVACY-H

**开放代码：** 同意记录持久化错误；重复同意提示；修复后持续报告

**逐条判断：** 用户同意已显示登记却不断再提示，多站复现；原因解释为subject varchar25过短，255及PR修复。后又有两站报告，要求另开issue，不能认定全面解决。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 关联PR关闭，后续仍报告

**原文证据：**

位置 `4989:5038`：

> change data type of subject field to varchar(255)

位置 `5969:6013`：

> Still happening for me, two different sites.

<a id="row-196"></a>
## 196. privacy-issue-3595

**主题代码：** PRIVACY-B, PRIVACY-C, PRIVACY-I

**开放代码：** 广告链接附加环境数据；告知与同意争议；可识别性争议

**逐条判断：** Yoast广告URL携带PHP平台版本语言与活跃天数，用户担忧未告知关联referer且不能拒绝；维护者否认PII并称用于知识库推荐。合法性与可识别性争议无验证，未修改。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 维护者解释否认，关闭

**原文证据：**

位置 `1650:1689`：

> I have no way to express my non consent

位置 `2683:2759`：

> We use this data to show you the most useful knowledge base articles we can.

<a id="row-197"></a>
## 197. privacy-issue-20259

**主题代码：** PRIVACY-D

**开放代码：** 日志PII清理

**逐条判断：** 单句要求删除日志PII，无数据类型机制讨论或实现证明。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 关闭，实施未知

**原文证据：**

位置 `819:846`：

> Remove any PII from logging

<a id="row-198"></a>
## 198. privacy-issue-2130

**主题代码：** PRIVACY-A, PRIVACY-B, PRIVACY-H

**开放代码：** 隐私选择入口失效

**逐条判断：** Firefox隐私页缺数据分享选择按钮，JS topicHeaders[0] undefined被报告为可能原因；无讨论证实修复或数据实际发送状态。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 故障报告，修复未知

**原文证据：**

位置 `1583:1622`：

> TypeError: topicHeaders[0] is undefined

<a id="row-199"></a>
## 199. privacy-issue-209

**主题代码：** PRIVACY-A, PRIVACY-B, PRIVACY-H

**开放代码：** 仅告知的Cookie横幅；拒绝选项缺失；选择状态持久化

**逐条判断：** Angular请求Google服务分析cookie告知，明确只有Learn More和确认，localStorage或cookie记忆关闭；开发进行中，用户提议退出未获回复，最终自动锁定。不能标为拒绝可用或已验证合规。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 开发讨论后关闭锁定，退出未实现证据

**原文证据：**

位置 `1372:1401`：

> there is no option to decline

位置 `4069:4133`：

> Have you considered going a bit further and allowing opting out?

<a id="row-200"></a>
## 200. privacy-issue-3539

**主题代码：** PRIVACY-C, PRIVACY-D, PRIVACY-E, PRIVACY-I

**开放代码：** 软件使用遥测；持久标识可链接性；临时标识最小化

**逐条判断：** Toil希望知道使用者，已有网站GA；讨论安装遥测与GA Anonymous Client ID仍可关联设备，提议共享假ID或临时ID避免日志留存；最终不确定实施而关闭。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 暂不开展，可重开

**原文证据：**

位置 `2528:2556`：

> use completely ephemeral IDs

位置 `2808:2845`：

> Not sure that we're going to do this.

<a id="row-201"></a>
## 201. privacy-issue-4261

**主题代码：** PRIVACY-F, PRIVACY-H

**开放代码：** 历史节点退出；IP暴露控制；隐私设置持久化；界面与后台执行分离

**逐条判断：** Status要求可禁离线消息历史节点减少IP暴露。早期空API列表猜测被纠正，应阻止connect-to-mailserver；UI完成但明确未执行，后端持久化分支已更改，末条仍说需阻止实际连接。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** UI及后台部分完成，端到端禁用未证实

**原文证据：**

位置 `9511:9559`：

> Use history is not functional, only the UI works

位置 `10821:10869`：

> The last thing left to do is to actually prevent

<a id="row-202"></a>
## 202. privacy-issue-18638

**主题代码：** PRIVACY-B, PRIVACY-C, PRIVACY-H, PRIVACY-I, PRIVACY-Y

**开放代码：** 运行平台信任；开源替代选择；隐私选择文档可发现性

**逐条判断：** Betaflight用户反对Chrome依赖，要求独立应用；社区提供CLI、Chromium及源码侧载，澄清本就兼容Chromium。用户最终要README说明替代方案；不把其Chrome不安全或换Chromium确保隐私声明当事实。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 既有替代获接受，文档变更未证实

**原文证据：**

位置 `8573:8609`：

> I wasn't aware of chromium existence

位置 `8716:8778`：

> suggest Chromium instead of Chrome in the installation section

<a id="row-203"></a>
## 203. privacy-issue-13996

**主题代码：** PRIVACY-I, PRIVACY-Z

**开放代码：** GDPR需求规划

**逐条判断：** 仅提产品团队GDPR准备方向和需求讨论，无具体措施，四年后过时关闭。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 过时关闭

**原文证据：**

位置 `1193:1212`：

> Closed as obsolete.

<a id="row-204"></a>
## 204. privacy-issue-7483

**主题代码：** PRIVACY-F, PRIVACY-I

**开放代码：** 位置搜索与受众扩大；IP推断位置风险；自填资料替代

**逐条判断：** 请求按城市找棋友，有人警示IP推断并公开位置隐私风险，推荐城市队伍搜索；作者提自填城市或IP且认为担心者可用VPN。无实现，后者不能作正当性证明。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 讨论关闭，未见实现

**原文证据：**

位置 `1657:1723`：

> exposing that to users seems like a massive privacy laws violation

位置 `2223:2246`：

> info from user profiles

<a id="row-205"></a>
## 205. privacy-issue-2824

**主题代码：** PRIVACY-C, PRIVACY-D, PRIVACY-I

**开放代码：** 广告归因精度隐私权衡；时间侧信道；随机延迟与聚合保护

**逐条判断：** 要求转化窗口标签以提高广告归因精度，讨论泄露浏览器离线时长、指数长尾延迟与跨站时间关联、短会话无限延迟；后续方向为不加显著随机延迟，聚合已有scheduled_report_time并建议事件级同样加入。隐私充足只是参与者判断，未证实新增实现。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 标准设计讨论，后续方向调整

**原文证据：**

位置 `5927:5986`：

> how long it has been since the user last used their browser

位置 `12157:12204`：

> not adding substantial random delays to reports

<a id="row-206"></a>
## 206. privacy-issue-1821

**主题代码：** PRIVACY-A, PRIVACY-B, PRIVACY-H, PRIVACY-I

**开放代码：** 同意告知语言可理解性；同意记录与撤回；法律依据争议；数据访问删除规划

**逐条判断：** OpenCart横幅遮语言切换且编码/多语言错误，使用户看不懂仍需接受。讨论扩展至第三方脚本事前同意、记录撤回、删除访问队列及告知模板；维护者拒绝联系表单强制勾选。最终称已更新修复，但逐功能覆盖无法验证。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 维护者报告修复，具体覆盖不明

**原文证据：**

位置 `1167:1233`：

> The visitor is forced to accept Cookies even he doesn't understand

位置 `9512:9556`：

> im not adding agree to terms for contact us!

位置 `10362:10385`：

> been updated and fixed.

<a id="row-207"></a>
## 207. privacy-issue-21502

**主题代码：** PRIVACY-I

**开放代码：** 法规驱动上游服务变更；地理数据许可同意；依赖数据定期更新

**逐条判断：** MaxMind因其声明的CCPA要求关闭公开分发，Plan新装地理库失败；讨论开发者分发key、用户EULA配置和定期更新，先手动放数据库，后新版本接受EULA下载成功并解释文件名及缓存。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 新版本替代流程获用户确认

**原文证据：**

位置 `4779:4814`：

> I accepted the EULA in _config.yml_

位置 `5348:5374`：

> Cache is cleared on reload

<a id="row-208"></a>
## 208. privacy-issue-14134

**主题代码：** PRIVACY-I

**开放代码：** 法规更新导致客户端不兼容；登录故障排查

**逐条判断：** NMM无法连元数据服务器，答可能版本低于0.65.2受GDPR相关更新影响或误用邮箱登录，建议升级并用用户名。缺实际验证和更新细节。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 建议升级，因不活跃关闭

**原文证据：**

位置 `1583:1611`：

> due to a GDPR-related update

位置 `2060:2092`：

> Closing issue due to inactivity.

<a id="row-209"></a>
## 209. privacy-issue-1954

**主题代码：** PRIVACY-A, PRIVACY-B, PRIVACY-H, PRIVACY-I

**开放代码：** 订阅双重确认；告知与同意边界；转化优化与合规讨论

**逐条判断：** newsletter增长改版讨论去勾选框因为邮件双重确认已存在，另一人担忧法律团队审计，后续区分订阅同意与阅读政策同意；AB完成并传市场，B全流量待勾，未明确最终checkbox决策。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** AB测试完成，同意界面最终选择未明确

**原文证据：**

位置 `5516:5551`：

> All subscriptions are double opt-in

位置 `4694:4741`：

> not necessarily our Legal team's interpretation

<a id="row-210"></a>
## 210. privacy-issue-8785

**主题代码：** PRIVACY-A, PRIVACY-E, PRIVACY-H

**开放代码：** 同意状态持久化；可撤回入口；部署域名限制；跨浏览器隐私执行差异

**逐条判断：** CookieYes在staging因付费域名限制不存选择，新增Cookies重开按钮，正确域名Chrome/Firefox验证接受拒绝和GA cookie增删；Safari拒绝需刷新才改状态，低流量暂接受后关闭。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 主要浏览器验证通过，Safari限制保留

**原文证据：**

位置 `5474:5510`：

> cookie state does not change to "NO"

位置 `6989:7030`：

> We hardly have any Safari traffic anyway.

<a id="row-211"></a>
## 211. privacy-issue-18634

**主题代码：** PRIVACY-D, PRIVACY-F, PRIVACY-H

**开放代码：** 位置隐私跨界面不一致；自由文本残余标识；模糊位置再推断；科学共享隐私权衡

**逐条判断：** iNaturalist私有或模糊坐标仍在关注者dashboard显示地点文本街道，跨账户确认。维护者说明只删开头门牌且自由文本难解析、行政区交叉可能缩小模糊网格；用户主张移除通知文本保护私宅及物种而保持科学共享。后dashboard改版不再显示地点，维护者询问解决。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 改版移除显示，未见报告者复验

**原文证据：**

位置 `12349:12389`：

> these locations are no longer showing up

位置 `7233:7301`：

> information being shared that the user wasn't aware was being shared

<a id="row-212"></a>
## 212. privacy-issue-974

**主题代码：** PRIVACY-D

**开放代码：** 输出格式绕过假名化；嵌套作者字段保护

**逐条判断：** Twitter NDJSON未被CSV既有假名化覆盖；PR递归字典按作者字段应用同一hash，最后明确Fixed in151。hash假名化不等于不可重识别匿名。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 报告修复

**原文证据：**

位置 `1638:1686`：

> uses the same hash function for pseudonymization

位置 `1930:1943`：

> Fixed in #151

<a id="row-213"></a>
## 213. privacy-issue-2174

**主题代码：** PRIVACY-B, PRIVACY-H

**开放代码：** 隐私告知移动端可读性

**逐条判断：** 确认按钮遮盖信息文本，识别Pixel3 Android9后仍无法Browserstack复现，works for me关闭，无修复证据。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 无法复现关闭

**原文证据：**

位置 `1081:1127`：

> The Confirm button overlaps informational text

位置 `3064:3092`：

> close this as "works for me"

<a id="row-214"></a>
## 214. privacy-issue-7594

**主题代码：** PRIVACY-G, PRIVACY-I, PRIVACY-Y, PRIVACY-Z

**开放代码：** 系统权限声明崩溃；依赖归因疑问

**逐条判断：** 用户未主动用相机却iOS13 TCC隐私违规崩溃，怀疑DeviceKit并已加相机权限尝试；完整栈含CameraUI，但维护者解释DeviceKit相机型号是硬编码不交互，不需要权限，用户接受，真实触发源未定。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 排除被疑库解释，根因未解决

**原文证据：**

位置 `15336:15369`：

> it isn't interacting with cameras

位置 `15504:15525`：

> these are _hardcoded_

<a id="row-215"></a>
## 215. privacy-issue-4624

**主题代码：** PRIVACY-D, PRIVACY-E, PRIVACY-F, PRIVACY-I

**开放代码：** 定时内容去标识；骚扰与人肉防护；社区内容保留；删除范围告知

**逐条判断：** Lemmy提可选限时匿名旧帖评论以减跟踪骚扰并保留社区内容，时间可统一或管理员用户定；提警示网络外副本不能清除。维护者以复杂收益少拒绝。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 复杂度收益理由拒绝

**原文证据：**

位置 `2134:2171`：

> Seems too complex for little benefit.

位置 `1203:1255`：

> Allow posts to be anonymized after a period of time.

<a id="row-216"></a>
## 216. privacy-issue-18223

**主题代码：** PRIVACY-F, PRIVACY-H, PRIVACY-Y

**开放代码：** 屏幕旁观暴露；首页隐私显示控制；风险前提更正

**逐条判断：** Brave新标签top sites被担忧显示历史供旁观者看，维护者更正已是手动选择非历史；仍请求可关及分模式，2023明确可移除top sites和shield stats，其他收藏与壁纸另项。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 显示开关已提供

**原文证据：**

位置 `2130:2163`：

> Top sites are now chosen manually

位置 `4160:4214`：

> You can remove top sites and shield stats sections now

<a id="row-217"></a>
## 217. privacy-issue-6836

**主题代码：** PRIVACY-G, PRIVACY-I

**开放代码：** 泄露后会话撤销；强制密码重置；框架与运维责任

**逐条判断：** ForkCMS提数据库凭据泄漏后删除会话禁登录直至重置，强调事后加固；先列入考虑后拒绝核心实现，建议直接数据库重置密码；是假设情景非实际泄漏。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 拒绝实现，建议运维处理

**原文证据：**

位置 `1031:1061`：

> User sessions must be deleted.

位置 `3930:3971`：

> reset all the passwords thru the database

<a id="row-218"></a>
## 218. privacy-issue-6849

**主题代码：** PRIVACY-C, PRIVACY-G, PRIVACY-I

**开放代码：** 泄露密码检测；第三方请求数据暴露；输入过程最小化

**逐条判断：** Warehouse已有服务端禁用泄漏密码，拟前端检测；权衡直接HIBP请求暴露用户信息、站内代理重用或hash及键入中发送密码，提失焦再查。有人开发及结尾感谢但未明确实现路径和验证。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 开发讨论，最终机制未证实

**原文证据：**

位置 `1790:1864`：

> this would only prevent leaking our users PII via additional http requests

位置 `2020:2078`：

> sending the password to Warehouse as the user is typing it

<a id="row-219"></a>
## 219. privacy-issue-6866

**主题代码：** PRIVACY-G, PRIVACY-I

**开放代码：** 支付凭据明文存储；数据库泄露防御；配置权限与密钥分离

**逐条判断：** 支付网关改UI存数据库引出明文密钥及管理员误改，争论数据库入侵是否等同代码控制，SQL注入或备份泄漏论证促成加密认同；关联Payum存储加密与Sylius表单PR，后续仍聚焦代码覆盖配置且有decorator替代。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 关联加密PR，配置扩展仍需替代

**原文证据：**

位置 `2759:2802`：

> password stored **in plain text** in the DB

位置 `9024:9085`：

> SQL Injection, finding a backup at rest that is not encrypted

<a id="row-220"></a>
## 220. privacy-issue-7018

**主题代码：** PRIVACY-B, PRIVACY-E, PRIVACY-F, PRIVACY-G, PRIVACY-I

**开放代码：** 综合合规需求文档；最小化与保留期限；数据主体访问更正删除导出；处理者治理与泄露响应

**逐条判断：** Codalab完整规范笔记涵盖组合可识别、画像、目的来源记录、同意、敏感类别、告知、机器可读导出及自动决策退出、第三方与安全和泄露通知。均为作者概括，含过度简化法律陈述，不认定经验证法律规则或系统已有功能。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 需求知识笔记，实施未知

**原文证据：**

位置 `2046:2092`：

> Restricted to the minimum needed to do the job

位置 `6261:6278`：

> Data Breach plans

位置 `4805:4840`：

> The data should be machine readable

<a id="row-221"></a>
## 221. privacy-issue-7032

**主题代码：** PRIVACY-G, PRIVACY-I

**开放代码：** 文件传输密钥协商；恶意中继威胁；人工密钥核验负担；安全承诺与机制差距

**逐条判断：** croc初始短码SHA256被质疑离线枚举和MITM，先加公私钥仍需带外人工核验且文档弱化必要性；长讨论澄清PAKE后作者发布3.0使用PAKE，对方认可。wormhole协议互通仅考虑，不算完成；未独立审计安全保证。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** PAKE实现获回应认可，互通未完成

**原文证据：**

位置 `20420:20459`：

> I've bumped croc to 3.0 which uses PAKE

位置 `15422:15484`：

> Nowhere does it mention that public keys must be authenticated

<a id="row-222"></a>
## 222. privacy-issue-7136

**主题代码：** PRIVACY-G, PRIVACY-I

**开放代码：** 邮箱静态加密诉求；框架与业务合规责任

**逐条判断：** allauth独立邮箱模型难扩展加密，删除匿名可由用户流程控制。维护者认为GDPR非强制字段加密，业务实现告知导出删除；作者接受关闭但强调数据库副本泄漏防护。法律简化保持归因。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 解释关闭，无加密变更

**原文证据：**

位置 `1246:1315`：

> What worries me is the part where email is stored in a separate model

位置 `1981:2036`：

> business processes that you can build on top of allauth

<a id="row-223"></a>
## 223. privacy-issue-7191

**主题代码：** PRIVACY-B, PRIVACY-G, PRIVACY-H, PRIVACY-I

**开放代码：** 漏洞私下报告渠道

**逐条判断：** 请求README安全联系人以避免授权绕过和泄漏报告入公开issue；有人认领并确认维护者邮箱，缺落地验证。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 联系人确定，文档实施未直接证实

**原文证据：**

位置 `949:987`：

> reported there and not the issue queue

<a id="row-224"></a>
## 224. privacy-issue-7223

**主题代码：** PRIVACY-F, PRIVACY-G, PRIVACY-I

**开放代码：** API密钥认证设计；凭据文件权限

**逐条判断：** 空正文，讨论API key性能、URL安全ID和只允许当前用户读下载密钥，Spec Demo Docs均未勾；引用文章主张不作已实现或正确安全结论。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 设计参考，实施未知

**原文证据：**

位置 `1908:1951`：

> assign read permission to only current user

<a id="row-225"></a>
## 225. privacy-issue-7373

**主题代码：** PRIVACY-E, PRIVACY-F, PRIVACY-G, PRIVACY-H, PRIVACY-I

**开放代码：** 主密码不留存；安全与便利权衡；内存秘密风险

**逐条判断：** 用户请求浏览器会话记主密码和自动填，讨论临时缓存派生密码、可选警示及内存读取泄露，最后明确拒绝存主密码因支撑所有当前未来密码，改向其他字段自动填。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 拒绝保存主密码

**原文证据：**

位置 `5133:5188`：

> we are not going to offer a way to save master password

<a id="row-226"></a>
## 226. privacy-issue-7376

**主题代码：** PRIVACY-B, PRIVACY-I

**开放代码：** 隐私政策缺失；模板告知与实际实践核对；追踪及第三方声明；退订与泄露通知承诺

**逐条判断：** Codebuddies新增privacy路由，作者借生成器并贴完整政策，涵盖姓名邮箱用途、不追踪cookies/DNT、第三方例外、未成年营销、7工作日泄露告知与退订。贡献者不知问卷答案需负责人提供，已建模板但页面完成未直接证实；政策声明不当作实际行为验证。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 政策文本与模板提供，部署未知

**原文证据：**

位置 `2444:2513`：

> A lot of questions to answer and I don't know all the answers myself.

位置 `4518:4562`：

> We do not use cookies for tracking purposes.

<a id="row-227"></a>
## 227. privacy-issue-7564

**主题代码：** PRIVACY-D, PRIVACY-G, PRIVACY-I

**开放代码：** 日志IPv6清理遗漏

**逐条判断：** 硬件探测ifconfig日志/128静态IPv6未擦除，维护者给commit称修复，无独立复验。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 明确commit修复声明

**原文证据：**

位置 `989:1016`：

> /128 addresses are visible!

位置 `1298:1329`：

> This is now fixed by the commit

<a id="row-228"></a>
## 228. privacy-issue-7574

**主题代码：** PRIVACY-B, PRIVACY-I

**开放代码：** 第三方政策链接告知；API供应商审核约束

**逐条判断：** YouTube API配额审核要求MIT视频服务条款引用YouTube ToS、隐私页链接Google政策，限三个工作日；无评论或完成验证。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 合规审核整改请求，实施未知

**原文证据：**

位置 `1469:1512`：

> No reference/link to Google Privacy Policy.

<a id="row-229"></a>
## 229. privacy-issue-7570

**主题代码：** PRIVACY-F, PRIVACY-I

**开放代码：** 广告活动名称受众限制

**逐条判断：** 可变campaign名称存market而不进行为spec，仅所属广告主统计可见，避免向其他人公开；纯设计要求。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 设计要求，实施未知

**原文证据：**

位置 `1076:1147`：

> campaign name should only be shown for the statistics of the advertiser

<a id="row-230"></a>
## 230. privacy-issue-7630

**主题代码：** PRIVACY-D, PRIVACY-F

**开放代码：** 医疗日期残余披露；隐私设置跨组件失效

**逐条判断：** Atlas viewProfileDates=false只隐轴日期，悬浮tooltip仍显医疗日期，使公开演示可能暴露PHI；要求所有报告元素一致隐藏，无修复讨论。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 可复现故障描述，修复未知

**原文证据：**

位置 `1135:1191`：

> hovering over a data point shows the date in the tooltip

<a id="row-231"></a>
## 231. privacy-issue-7638

**主题代码：** PRIVACY-B, PRIVACY-H, PRIVACY-Y, PRIVACY-Z

**开放代码：** 地址误作搜索的隐私顾虑；隐私关联次要

**逐条判断：** Focus把802.11当地址导致乱码错误页，主要修复字符编码；把无效地址送搜索引擎仅为替代方案的潜在隐私顾虑，并非证实已外发。评论称1409修复随8.0发布。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 乱码修复声明，隐私风险仅替代方案讨论

**原文证据：**

位置 `1366:1431`：

> Or the browser could just treat invalid addresses as search terms

位置 `2122:2138`：

> fixed with #1409

<a id="row-232"></a>
## 232. privacy-issue-7659

**主题代码：** PRIVACY-B, PRIVACY-G, PRIVACY-H

**开放代码：** 麦克风权限声明缺失；系统权限检查崩溃

**逐条判断：** JUCE新Audio Application真机iOS11启动TCC隐私违规崩溃但模拟器与旧版可用，答需Projucer导出设置启用麦克风访问；未证实未授权录音或泄漏。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 提供权限配置方案

**原文证据：**

位置 `3067:3106`：

> You'll need to enable microphone access

<a id="row-233"></a>
## 233. privacy-issue-8125

**主题代码：** PRIVACY-C, PRIVACY-D, PRIVACY-F

**开放代码：** 归档元数据身份泄露；URL与请求头去除选项

**逐条判断：** yt-dlp视频info JSON中的formats和URL可能含IP标识，随归档公开；后说明所有字段可parse-metadata删除并给含headers字幕缩略图的最小别名，单开关必要性待问。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 已有通用字段删除替代

**原文证据：**

位置 `2723:2761`：

> all metadata fields can now be removed

位置 `2182:2228`：

> info json may be uploaded along with the video

<a id="row-234"></a>
## 234. privacy-issue-8271

**主题代码：** PRIVACY-A, PRIVACY-G, PRIVACY-I, PRIVACY-Y, PRIVACY-Z

**开放代码：** 剪贴板被动监测；便利功能隐私争议

**逐条判断：** PowerToys请求监测URL弹出浏览器选择，争论打扰与场景，末有人怀疑监测隐私、另一人以OS允许辩护；作者在其他工具实现而关闭，不认定PowerToys读取或泄漏。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 作者外部实现后关闭

**原文证据：**

位置 `6118:6167`：

> I was able to implement that idea in another tool

<a id="row-235"></a>
## 235. privacy-issue-8295

**主题代码：** PRIVACY-H

**开放代码：** 隐私搜索引擎选择；既有功能与阻断缺陷

**逐条判断：** Fenix要求默认提供DuckDuckGo，答能自加但另一人指出12954暂阻；最终只给添加步骤，无默认变更或阻断修复验证。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 提供操作指引，关联阻断未核实解除

**原文证据：**

位置 `1812:1847`：

> This behaviour currently blocked by

位置 `2166:2189`：

> Tap `Add search engine`

<a id="row-236"></a>
## 236. privacy-issue-8360

**主题代码：** PRIVACY-A, PRIVACY-B

**开放代码：** 必要Cookie告知

**逐条判断：** 请求说明cookie/client存储及非公开登录功能依赖，关联566关闭；并非追踪cookie退出设计。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 关联变更关闭

**原文证据：**

位置 `1108:1148`：

> logins won't work at all without cookies

位置 `1517:1531`：

> closed by #566

<a id="row-237"></a>
## 237. privacy-issue-8590

**主题代码：** PRIVACY-A, PRIVACY-B, PRIVACY-H

**开放代码：** 同意界面国际化缺口

**逐条判断：** GOV.UK cookie横幅ERB与接受拒绝JS消息需翻译，评论仍有硬编码且缺译文，关闭未说明完成。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 翻译资源缺失，完成未知

**原文证据：**

位置 `1648:1709`：

> we don't currently have translations available for this text.

<a id="row-238"></a>
## 238. privacy-issue-8755

**主题代码：** PRIVACY-B, PRIVACY-H

**开放代码：** Cookie组件配置文档

**逐条判断：** 横幅宏参数表漏secondaryButtonUrl，明确2126修复；无证据按钮失效或拒绝受损。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 文档修复

**原文证据：**

位置 `1407:1421`：

> Fixed in #2126

<a id="row-239"></a>
## 239. privacy-issue-8786

**主题代码：** PRIVACY-A, PRIVACY-B, PRIVACY-H

**开放代码：** 一键拒绝所有追踪

**逐条判断：** PWABuilder sprint要求单击Reject All并明确应拒所有cookie tracking，未见测试实现。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 明确需求，实施未知

**原文证据：**

位置 `1626:1664`：

> All cookie tracking should be rejected

<a id="row-240"></a>
## 240. privacy-issue-8813

**主题代码：** PRIVACY-B, PRIVACY-H

**开放代码：** 政策访问链接失效；基础设施路由回归

**逐条判断：** DP/cellxgene横幅隐私与条款链接返首页，内嵌团队讨论定位CloudFront仅转发d/e路径遗漏静态，建议新增路径并改三处配置。无实施证据。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 根因与修复方案讨论

**原文证据：**

位置 `954:998`：

> cookie banner's links go back to DP homepage

<a id="row-241"></a>
## 241. privacy-issue-8822

**主题代码：** PRIVACY-A, PRIVACY-B, PRIVACY-H, PRIVACY-Z

**开放代码：** 必要与可选Cookie区分；正文空缺

**逐条判断：** 仅标题要求横幅区分Optional与Essential，正文确实空且无评论，不能推断按钮执行或同意默认。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 空正文，实施未知

**原文证据：**

位置 `86:115`：

> Optional vs Essential cookies

<a id="row-242"></a>
## 242. privacy-issue-8840

**主题代码：** PRIVACY-B, PRIVACY-H, PRIVACY-I

**开放代码：** Cookie使用盘点；应用与营销站保护范围

**逐条判断：** Parabol作者认为无cookie但要确认或加政策横幅、GDPR检查，后称营销站做了应用尚未，stale关闭可重开。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 营销站已有，应用未完成

**原文证据：**

位置 `1682:1702`：

> Not for the app yet.

<a id="row-243"></a>
## 243. privacy-issue-8868

**主题代码：** PRIVACY-B, PRIVACY-H

**开放代码：** Cookie组件升级文档

**逐条判断：** 已加data-nosnippet，纯HTML使用者需手动补，要求发布说明；清单完成且4.0说明已列推荐。并非个人数据泄漏报告。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 发布说明完成

**原文证据：**

位置 `2031:2093`：

> included as a recommended change in the release notes for v4.0

<a id="row-244"></a>
## 244. privacy-issue-8885

**主题代码：** PRIVACY-B, PRIVACY-I

**开放代码：** 分析服务迁移与横幅移除；隐私政策同步缺口；跨仓库部署不一致

**逐条判断：** cellxgene获迁Plausible批准但隐私政策尚未更新，跨三仓库去横幅及自动测试维护；DP生产完成Explorer仅staging，末条仍说Explorer生产有横幅，不能一概完成。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 部分部署，Explorer生产及政策同步未证实完成

**原文证据：**

位置 `3781:3820`：

> DP: Done! No more cookie banner in prod

位置 `4080:4127`：

> Explorer still has cookie banner in prod today!

<a id="row-245"></a>
## 245. privacy-issue-8876

**主题代码：** PRIVACY-A, PRIVACY-E, PRIVACY-F, PRIVACY-H, PRIVACY-I

**开放代码：** 匿名用户同意状态；身份转换同意迁移；逐项撤回与中性默认；同意版本更新；前后端状态一致性

**逐条判断：** SAP匿名consents通过HTTP头全量交换并localStorage持久化，区分未选择/给予/撤回；登录恢复账号同意、注册迁移匿名同意、登出恢复匿名，语言不改状态，新版本重提示。详细计划指出注册未接后台及SSR限制，清单最终含修复测试发布文档全完成；2022另有人store未加载报错，无解决。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 主清单完成，后续集成求助未解决

**原文证据：**

位置 `5052:5079`：

> neither given nor withdrawn

位置 `13264:13313`：

> Fix transferring anonymous consents to registered

<a id="row-246"></a>
## 246. privacy-issue-8890

**主题代码：** PRIVACY-B, PRIVACY-H

**开放代码：** 隐私横幅屏幕阅读器可访问性

**逐条判断：** Ubuntu NVDA Firefox不读cookie对话导致盲人不能访问，Chrome可用；复现后关联cookie-policy123，维护者和原用户确认可访问。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 修复并获原报告者复验

**原文证据：**

位置 `3246:3298`：

> the cookie dialog now can be easily accessed by NVDA

<a id="row-247"></a>
## 247. privacy-issue-8911

**主题代码：** PRIVACY-A, PRIVACY-H, PRIVACY-I

**开放代码：** 同意前Cookie阻断；通用同意层

**逐条判断：** Elementor请求加载时不设cookie至按钮同意，现需第三方插件；回复引12567通用跨地区同意层，用户将查看，未确认功能发布。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 关联方案PR，实施验证未知

**原文证据：**

位置 `1701:1743`：

> disable cookies when the website is loaded

<a id="row-248"></a>
## 248. privacy-issue-8956

**主题代码：** PRIVACY-B, PRIVACY-H, PRIVACY-I

**开放代码：** 隐私告知翻译；地区内容匹配

**逐条判断：** BBC提Tigrinya翻译及UX长度，测试发现非UK文案误用于UK并另开bug、链接后空格缺失；最后Done，具体两问题验证未展示。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 报告完成

**原文证据：**

位置 `1717:1794`：

> translation on test page is showing the non-uk content, instead of UK content

位置 `2493:2497`：

> Done

<a id="row-249"></a>
## 249. privacy-issue-8975

**主题代码：** PRIVACY-A, PRIVACY-E, PRIVACY-H, PRIVACY-I

**开放代码：** 跨域同意状态冲突；重复横幅；跨站点选择传播

**逐条判断：** BBC Simorgh写www域PAL写父域产生重复cookie一同意一未同意，读写冲突反复横幅；详细跨页面复现后测试通过同域接受不再弹，.com到.co.uk仍弹而反向不弹被记录。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 目标故障验证修复，域间行为有差异

**原文证据：**

位置 `4906:4932`：

> One accepted, and one not.

位置 `6151:6188`：

> The issue this ticket fixes works now

<a id="row-250"></a>
## 250. privacy-issue-8998

**主题代码：** PRIVACY-A, PRIVACY-B, PRIVACY-H

**开放代码：** 隐私选择按钮遮挡；弹窗显示顺序

**逐条判断：** web.dev PWA安装提示遮cookie确认/更多信息按钮，请求接受cookie后再显示安装提示；无讨论实现。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 需求，实施未知

**原文证据：**

位置 `1151:1190`：

> covers the ok/more info cookies buttons

<a id="row-251"></a>
## 251. privacy-issue-9062

**主题代码：** PRIVACY-A, PRIVACY-B, PRIVACY-H, PRIVACY-I

**开放代码：** 可配置Cookie告知

**逐条判断：** Nextcloud请求可开关横幅与自定义链接文案，回复指已有论坛和两issue，没有本条实现或法律结论。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 转已有讨论关闭

**原文证据：**

位置 `1025:1066`：

> set a link or text for the Coockie Banner

<a id="row-252"></a>
## 252. privacy-issue-9096

**主题代码：** PRIVACY-A, PRIVACY-H, PRIVACY-I

**开放代码：** 同意状态编码兼容；地区策略差异

**逐条判断：** BBC EU/EEA非UK更改横幅，需要读取ckns_explicit=1或2均为接受，写入仍允许1；无测试通过声明。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 兼容规则明确，实施未知

**原文证据：**

位置 `1260:1311`：

> consider a value of 2 as also reflecting acceptance

<a id="row-253"></a>
## 253. privacy-issue-9114

**主题代码：** PRIVACY-B, PRIVACY-H, PRIVACY-I

**开放代码：** 隐私告知多语言覆盖；地区译文映射不明

**逐条判断：** BBC22服务已有译文需更新配置跑全套页面，评论问privacy未分UK/international如何映射，未答。不能推断法律文案适用相同。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 翻译更新请求，地区映射未解决

**原文证据：**

位置 `2557:2620`：

> Should i just use the same content for `uk` and `international`

<a id="row-254"></a>
## 254. privacy-issue-9246

**主题代码：** PRIVACY-A, PRIVACY-B, PRIVACY-H, PRIVACY-Z

**开放代码：** Cookie接受横幅；正文空缺

**逐条判断：** 仅标题要求EU cookie acceptance banner，无正文评论，无法细化同意拒绝阻断或实现。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 空正文，完成未知

**原文证据：**

位置 `65:99`：

> add an eu cookie acceptance banner

<a id="row-255"></a>
## 255. privacy-issue-9362

**主题代码：** PRIVACY-A, PRIVACY-B, PRIVACY-H, PRIVACY-I

**开放代码：** 分析Cookie告知；告知替代主动同意；合规依据不确定

**逐条判断：** eahub因GA要求横幅，讨论info/opt-in/opt-out后选择info并引用供应商不保证但可能足够文案。有选择决定，无真正拒绝或合规验证。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 选择纯告知方案

**原文证据：**

位置 `2093:2133`：

> Went for info as it should be sufficient

<a id="row-256"></a>
## 256. privacy-issue-9395

**主题代码：** PRIVACY-A, PRIVACY-B

**开放代码：** 注册绑定Cookie同意；隐私政策链接

**逐条判断：** qit.cloud要求注册表单说明需cookie，提交即同意并链政策，无拒绝机制或实现说明。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 需求，实施未知

**原文证据：**

位置 `1048:1089`：

> By submitting this form you're consenting

<a id="row-257"></a>
## 257. privacy-issue-9433

**主题代码：** PRIVACY-A, PRIVACY-C, PRIVACY-E, PRIVACY-I

**开放代码：** 未同意分析Cookie；隐私政策缺失报告；撤回入口缺失

**逐条判断：** 用户报告Gatsby两站GA先设cookie无横幅政策，建议组件但其撤回需删cookie或等过期；回应称不收个人数据无需同意，无实测，机器人闲置关闭。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 不活跃关闭，未修复证据

**原文证据：**

位置 `1183:1224`：

> no way for a user to revoke consent later

位置 `917:950`：

> save cookies without user consent

<a id="row-258"></a>
## 258. privacy-issue-9380

**主题代码：** PRIVACY-A, PRIVACY-B, PRIVACY-H, PRIVACY-I

**开放代码：** 性能与同意组件权衡；法律需求签核依赖

**逐条判断：** BBC弃Orbit性能不足自建canonical横幅，明确本项只Storybook不集成Article；等待已签核法律feature文件，后重复1398关闭。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 需求待签核，重复转移

**原文证据：**

位置 `2782:2834`：

> Blocked pending us getting a signed-off feature file

<a id="row-259"></a>
## 259. privacy-issue-9490

**主题代码：** PRIVACY-B, PRIVACY-C, PRIVACY-I

**开放代码：** 追踪最小化设计；子站与第三方告知范围

**逐条判断：** remote jobs主站刻意不加分析认为无价值，核查列表无cookie但WordPress博客及PayPal可能涉及；作者为博客加WP政策widget而主站保持。不能泛称全站无跟踪。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 博客告知组件添加，主站无变更

**原文证据：**

位置 `1517:1571`：

> The list area of the site uses no cookies or analytics

位置 `2752:2773`：

> I've added the widget

<a id="row-260"></a>
## 260. privacy-issue-9475

**主题代码：** PRIVACY-H

**开放代码：** Cookie组件关闭后遮挡

**逐条判断：** Jetpack关闭只移内部cookie元素而固定容器残留，挡日程星号邮件功能，已有z-index绕过；无讨论修复。是告知组件可用性缺陷非证实数据泄漏。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 故障及局部绕过，修复未知

**原文证据：**

位置 `1968:2020`：

> the `.widget_eu_cookie_law_widget` container remains

<a id="row-261"></a>
## 261. privacy-issue-9683

**主题代码：** PRIVACY-A, PRIVACY-H, PRIVACY-I

**开放代码：** 拒绝追踪导致核心功能失败；分析依赖空对象

**逐条判断：** Magento未接受cookie时GTM不建dataLayer但checkout直push报错阻结账，多人复现，作者条件包裹patch待测；企业版本转支持门户，未修复证明。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 提供patch思路，转企业支持

**原文证据：**

位置 `1485:1525`：

> TypeError: window.dataLayer is undefined

位置 `3145:3193`：

> GitHub is intended for Magento Open Source users

<a id="row-262"></a>
## 262. privacy-issue-9864

**主题代码：** PRIVACY-A, PRIVACY-C, PRIVACY-D, PRIVACY-H, PRIVACY-I

**开放代码：** IP去标识选项；同意前第三方加载；撤回执行；界面与阻断分离

**逐条判断：** Jekyll主题提出GA IP匿名PR63，先解决横幅显示仍不知怎样阻cookie，讨论回调后用户自称解决；末强调Disqus需同意才载且撤回再禁。GA匿名无需同意系用户主张；主题PR拟合并非全站合规证实。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 用户方案称解决，主题改动承诺合并

**原文证据：**

位置 `6067:6095`：

> Fixed the problem thank you!

位置 `6896:6959`：

> disable Disqus once again if the users ever revoke their choice

<a id="row-263"></a>
## 263. privacy-issue-9894

**主题代码：** PRIVACY-B, PRIVACY-H

**开放代码：** 同意横幅与测试状态一致性

**逐条判断：** bbc-a11y多次访问cookie状态不同使XPath难定位，建议测试前预设ckns_policy，关联160前置设置。涉及测试可重复性，不证明线上强制同意。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 转关联测试设置任务

**原文证据：**

位置 `2387:2458`：

> A lot of the News testing tools set the cookie before checking the page

<a id="row-264"></a>
## 264. privacy-issue-11276

**主题代码：** PRIVACY-A, PRIVACY-B, PRIVACY-C, PRIVACY-E, PRIVACY-F, PRIVACY-H, PRIVACY-I

**开放代码：** 卸载不等于数据删除；第三方清理通知缺失；平台与应用保留责任；用户强制移除控制

**逐条判断：** Teams移除按钮5秒自动启用、30秒移除不等回调；卸载app实际上隐藏tabs重装再现，第三方因缺卸载hook难清理。平台称数据在外站需其自管，setValidityState行为为防开发者阻止移除而设计；最终仍要求文档澄清，非删除修复。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 预期行为解释，清理hook未实现证据

**原文证据：**

位置 `6088:6127`：

> They are simply hidden and get re-shown

位置 `10290:10346`：

> automatically enable the "Remove" button after 5 seconds

<a id="row-265"></a>
## 265. privacy-issue-11306

**主题代码：** PRIVACY-A, PRIVACY-C, PRIVACY-I

**开放代码：** 退出选择跨服务传递；遥测作用域；法律团队待确认

**逐条判断：** FxA建议账号metrics退出传至所有RP但不与桌面移动遥测双向联动，需法律隐私确认；无评论决议。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 范围提案待确认

**原文证据：**

位置 `1280:1319`：

> confirm all this with legal and privacy

<a id="row-266"></a>
## 266. privacy-issue-11347

**主题代码：** PRIVACY-A, PRIVACY-C, PRIVACY-I

**开放代码：** 广告链路隐私信号传递；法规机制差异

**逐条判断：** Prebid视频URL需自动插入USP模块us_privacy供Google，GDPR由IMA读CMP的解释与auction请求区别仍争议；明确CCPA修复4.19发布并关闭，GDPR另6077。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** CCPA随4.19发布，GDPR另题

**原文证据：**

位置 `3898:3936`：

> Closing this issue, went out with 4.19

<a id="row-267"></a>
## 267. privacy-issue-11433

**主题代码：** PRIVACY-A, PRIVACY-B, PRIVACY-H, PRIVACY-I

**开放代码：** 地区同意配置；AMP故事集成缺陷

**逐条判断：** AMP页面与Stories共享EEA/CA提示的配置确认，Stories缺consents对象抛错，答加空对象绕过，随后明确其实框架bug无需用户改且计划修；不能停在初始looks good当完整无误。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 配置绕过提供，框架修复待做

**原文证据：**

位置 `7239:7261`：

> this is actually a bug

位置 `7293:7342`：

> There should be no changes necessary on your end.

<a id="row-268"></a>
## 268. privacy-issue-11513

**主题代码：** PRIVACY-B, PRIVACY-I, PRIVACY-Z

**开放代码：** 请求来源属性用于合规；隐私关联次要

**逐条判断：** Fastify把IP/ips/hostname改getter减少开销，参与者要求保留供GDPR/CCPA来源核实，作者确认不删；无降低采集或日志匿名要求，PR有人认领。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 设计同意，实施未知

**原文证据：**

位置 `2503:2531`：

> They should not go anywhere.

<a id="row-269"></a>
## 269. privacy-issue-11653

**主题代码：** PRIVACY-A, PRIVACY-B, PRIVACY-C, PRIVACY-H, PRIVACY-I

**开放代码：** 退出持久化与跨平台同步；地区法规分流；广告信号传递；性能与合规权衡；服务器同意判定

**逐条判断：** AMP48评论从CA地理缺口、多同意及opt-out机制探讨到本地存储可淘汰不可靠，出版者要求服务端账户/reader状态同步且先判定再载追踪。最终MVP服务端checkConsentHref与consentString、缓存重验证，退出跳出版者站，长期iframe；已dev发布及已知bug修，用户顶层geoOverride改后确认调用，末补US promptUI=null。非完整所有端或法律合规验证。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** MVP开发渠道发布，配置调用获用户确认

**原文证据：**

位置 `34788:34845`：

> new spec has been implemented and deployed to dev channel

位置 `33237:33326`：

> you need to add a link on your page that takes user to your own website to do the opt-out

<a id="row-270"></a>
## 270. privacy-issue-11986

**主题代码：** PRIVACY-A, PRIVACY-F, PRIVACY-I

**开放代码：** 发送前输入窥视；客服效率隐私权衡

**逐条判断：** Chatwoot提实时看用户尚未发送文字让客服提前答，回复应可选因各地法规风险，重复1137关闭；不是已实施监控事实。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 重复转移

**原文证据：**

位置 `1589:1636`：

> Needs to be optional as may breach privacy regs

<a id="row-271"></a>
## 271. privacy-issue-11995

**主题代码：** PRIVACY-F, PRIVACY-H

**开放代码：** 私密浏览跨应用跳转；拒绝后浏览中断；隐私默认状态更正

**逐条判断：** Fenix private tab在启用open-links-app时提示外部app，取消页面不载；讨论更正并非无提示自动外发且开关默认关，仍需取消后自动浏览或长按新tab替代，关联两建议最后迁Bugzilla。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 预期提示确认，体验改进转移未证实修复

**原文证据：**

位置 `5231:5285`：

> The default "Open links in apps" is in fact turned off

位置 `8672:8689`：

> Moved to bugzilla

<a id="row-272"></a>
## 272. privacy-issue-12039

**主题代码：** PRIVACY-I

**开放代码：** 隐私事件响应模板与组织协作

**逐条判断：** 政府云团队向其他团队搜集安全隐私事件报告模板供应用团队快速响应，评论已收资料存Compliance；登录页入口只是后续意图，非已上线。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 模板资料收集完成

**原文证据：**

位置 `2097:2143`：

> This has been saved in the Compliance section.

<a id="row-273"></a>
## 273. privacy-issue-12057

**主题代码：** PRIVACY-F, PRIVACY-H, PRIVACY-Y

**开放代码：** 错误URL意外共享；跨标签状态混淆

**逐条判断：** Fenix外部开新tab分享却取前tab URL，多用户稳定版复现且已发错链接，秘密/NSFW后果为潜在；切tab再回绕过验证，后custom tabs复现并有修复，原作者一段时间无法复现。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 开发者找到修复，原用户报告不再复现

**原文证据：**

位置 `1112:1151`：

> The PREVIOUS tab's URL is copied/shared

位置 `11040:11073`：

> I can reproduce using custom tabs

<a id="row-274"></a>
## 274. privacy-issue-12060

**主题代码：** PRIVACY-B, PRIVACY-C, PRIVACY-I

**开放代码：** 离线文档第三方请求；隐私修复兼容性回退

**逐条判断：** gpiozero要求Debian离线文档去Travis badge，初次改动破PyPI而回退且Fix标题误关；2021最终提供commit修复。不能把2016关闭认作修复。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 回退后后续commit修复

**原文证据：**

位置 `1844:1882`：

> I'm going to have to revert the change

位置 `2783:2800`：

> Fixed in a2b2b816

<a id="row-275"></a>
## 275. privacy-issue-12082

**主题代码：** PRIVACY-F, PRIVACY-G, PRIVACY-I

**开放代码：** 退群权限跨设备失步；隐蔽受众继续接收；成员列表可审计性

**逐条判断：** Signal移动退群桌面仍能收发，重新加入退出也失败；另一组证实离开者数月仍收而UI不示，维护者疑离组通知丢失并需关键日志，建议正确成员设备改群名广播状态，最终不活跃关闭。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 疑因与绕过建议，未修复验证

**原文证据：**

位置 `5749:5816`：

> fourth member who left the group months ago has continued receiving

位置 `7691:7715`：

> closed due to inactivity

<a id="row-276"></a>
## 276. privacy-issue-12176

**主题代码：** PRIVACY-C, PRIVACY-I, PRIVACY-Y

**开放代码：** 第三方追踪请求归因争议；主题插件交互

**逐条判断：** Yoast启用见DoubleClick请求，换默认主题消失，作者不确定主题或插件；维护者否认插件使用该服务，关闭未找实际来源，不能认定Yoast注入追踪。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 来源未定，维护者否认关闭

**原文证据：**

位置 `1689:1730`：

> I am not sure if this is a bug with Yoast

位置 `3275:3299`：

> it isn't from our plugin

<a id="row-277"></a>
## 277. privacy-issue-12157

**主题代码：** PRIVACY-B, PRIVACY-C

**开放代码：** 第三方传输告知准确性；仅元数据可判

**逐条判断：** 仅标题说发送Bing Maps内容说明不正确，正文两评论缺失，无法知道数据范围或修订结果。

**材料可用性：** metadata_only。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 仅元数据，完成未知

**原文证据：**

位置 `65:124`：

> Incorrect information about what is being sent to Bing Maps

<a id="row-278"></a>
## 278. privacy-issue-12195

**主题代码：** PRIVACY-B, PRIVACY-F, PRIVACY-G, PRIVACY-I

**开放代码：** 隐私标准与产品目标争议；代理绕过告知；消息持久化默认；头像删除传播；能力文档过时

**逐条判断：** uTox要求全遵TCS，维护者拒绝部分并称清单过时，否认自动接电话且称加密等已有；用户逐项追问强制proxy、头像删广播、默认不存消息等未答。不得把清单NO全当实际缺陷或维护者IP非保护信息当事实。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 标准要求争议关闭，具体能力有矛盾未审计

**原文证据：**

位置 `3660:3693`：

> The info from  is BADLY out dated

位置 `3575:3618`：

> message persistence is a feature, not a bug

<a id="row-279"></a>
## 279. privacy-issue-12191

**主题代码：** PRIVACY-C, PRIVACY-G, PRIVACY-H, PRIVACY-I

**开放代码：** 硬编码外部DNS连接；用户网络策略被忽略；回退健康检查争议

**逐条判断：** HA设置本地DNS却持续向Cloudflare DoT尝试，完整日志后出现被防火墙拒绝及超时；升级234/235暂缓均复发。维护者解释所有DNS heartbeat被阻后更频繁，建议解除防火墙或用Container；用户要求移除或仅真回退。不认定被挡请求已成功泄出查询。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 预期heartbeat解释，用户反对未修复

**原文证据：**

位置 `48447:48486`：

> There is a heartbeat to all DNS servers

位置 `47854:47897`：

> Spoke too soon, back to the same suituation

<a id="row-280"></a>
## 280. privacy-issue-12278

**主题代码：** PRIVACY-E, PRIVACY-F, PRIVACY-I

**开放代码：** 邮箱身份关联错误；历史订单受众保护；数据合并便利与隐私权衡

**逐条判断：** OFN最初提验证邮箱后管理员关联旧guest订单但用户不见，争论邮箱拼错转让虚构及商家重复记录，最终决定完全不关联旧guest与新账号，以guest标签区分另2338；不得按初始正文编码为自动合并已实施。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 决定不关联，标签界面另项

**原文证据：**

位置 `12639:12690`：

> final decision is to not associate old guest orders

位置 `14042:14066`：

> two different identities

<a id="row-281"></a>
## 281. privacy-issue-12283

**主题代码：** PRIVACY-G, PRIVACY-Y

**开放代码：** 设备状态指纹风险；功能替代减采集

**逐条判断：** Wagtail提低电量编辑提示，因Battery API仅Chrome支持且其他浏览器因指纹隐私移除而拒，建议自动保存替代；没有实际跟踪证据。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 不实现，建议自动保存

**原文证据：**

位置 `1983:2036`：

> battery status being an easy way to fingerprint users

<a id="row-282"></a>
## 282. privacy-issue-13415

**主题代码：** PRIVACY-A, PRIVACY-C, PRIVACY-I

**开放代码：** 遥测主动同意诉求

**逐条判断：** .NET工具要求有意识同意分享用量数据，重复CLI3093关闭，无默认变更证据。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 重复转移

**原文证据：**

位置 `897:946`：

> consciously agree to collect and share usage data

<a id="row-283"></a>
## 283. privacy-issue-13435

**主题代码：** PRIVACY-C, PRIVACY-F, PRIVACY-I, PRIVACY-Y

**开放代码：** 跨数据源去匿名；尊重分享偏好

**逐条判断：** odota提回放account IDs补WebAPI匿名玩家，维护者确认技术可行但故意不做因为Valve可能不赞成；不算已跟踪。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 主动拒绝重新关联

**原文证据：**

位置 `1373:1403`：

> we intentionally don't do this

<a id="row-284"></a>
## 284. privacy-issue-14019

**主题代码：** PRIVACY-B, PRIVACY-D, PRIVACY-H, PRIVACY-I

**开放代码：** 隐私配置告知；IP处理与存储责任；反垃圾功能与去标识权衡

**逐条判断：** Antispam Bee计划界面指导GDPR配置，WP core存IP而插件仍处理；有人说去IP使本地spam库失效，最后代码OR查询更正仍可比email/url。不能等同不存就不处理或完全无反垃圾能力。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 文档指导讨论，实际能力澄清

**原文证据：**

位置 `3657:3717`：

> it would still check on email and url for incoming comments.

<a id="row-285"></a>
## 285. privacy-issue-14025

**主题代码：** PRIVACY-A, PRIVACY-B, PRIVACY-H, PRIVACY-I

**开放代码：** 同意证据记录；政策变更重新同意；审计有效性争议

**逐条判断：** PMPro拟记录每次TOS勾选日期IP订单及页面，争议电子签名和证据充分性；最后已存checkout同意日期user meta，TOS更新重新索取仍需另723。法律观点非验证。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 日期记录实现，更新重同意未完成

**原文证据：**

位置 `4190:4221`：

> We now save the date of consent

位置 `4266:4299`：

> still need to ask for new consent

<a id="row-286"></a>
## 286. privacy-issue-14041

**主题代码：** PRIVACY-C, PRIVACY-I

**开放代码：** 设备广告标识采集；未来用途不限定；框架合规责任下放

**逐条判断：** Nakama请求收硬件广告ID供未来更多利用，维护者因GDPR/PrivacyShield顾虑拒绝核心，交游戏团队自定义代码。不是已采集事实。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 核心拒绝，交应用方

**原文证据：**

位置 `925:979`：

> allowing us to do more with their data at a later date

位置 `1383:1404`：

> handled by game teams

<a id="row-287"></a>
## 287. privacy-issue-14051

**主题代码：** PRIVACY-I, PRIVACY-Z

**开放代码：** 合规工具规划未细化

**逐条判断：** VirtoCommerce要求GDPR支持工具但需求故事验收均问号占位，长期无活动关闭。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 不活跃关闭

**原文证据：**

位置 `1745:1770`：

> inactive for  a long time

<a id="row-288"></a>
## 288. privacy-issue-14058

**主题代码：** PRIVACY-F, PRIVACY-I, PRIVACY-Z

**开放代码：** 数据访问角色盘点

**逐条判断：** PeeringDB确认数据库网站访问角色非注册、注册、管理员三类，未展开各类权限细节。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 角色分类获确认

**原文证据：**

位置 `1840:1864`：

> Then yes, that's correct

<a id="row-289"></a>
## 289. privacy-issue-14064

**主题代码：** PRIVACY-B, PRIVACY-C, PRIVACY-D, PRIVACY-E, PRIVACY-I

**开放代码：** 默认个人数据盘点；登录日志最小化；哈希仍可关联；URL邮箱泄漏；框架与站点责任

**逐条判断：** SilverStripe讨论Member/LoginAttempt及禁记录配置，邮箱已hash但IP仍关联账号，锁定策略隐式开日志；提清理期限用户删除及告知docs PR。重置密码URL邮箱进入分析系统另8080，最终明确该URL问题已有commit修复，其余早期设想不能全认完成。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** URL邮箱泄漏修复，文档及其他措施分别限定

**原文证据：**

位置 `4444:4529`：

> IPs to members though, so are effectively storing personally identifable information.

位置 `9323:9355`：

> that's been resolved for a while

<a id="row-290"></a>
## 290. privacy-issue-14139

**主题代码：** PRIVACY-C, PRIVACY-I

**开放代码：** 遥测字段治理注释；不必要采集移除

**逐条判断：** VSCode遥测缺GDPR注释，引出谁负责及格式指导；最终删除不再需要遥测entry，不是补注释。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 删除不必要遥测项

**原文证据：**

位置 `1642:1695`：

> Removed the telemetry entry as it is no longer needed

<a id="row-291"></a>
## 291. privacy-issue-14145

**主题代码：** PRIVACY-C, PRIVACY-D, PRIVACY-E, PRIVACY-H

**开放代码：** IP去标识与可配置停采；聊天保留期限；匿名化覆盖不足

**逐条判断：** LHC请求IP模糊、停采、定期匿名及按需处理，维护者给2.92发布/匿名文档链接；末用户称姓名邮箱电话未全匿名且找不到按龄删除全部聊天选项，无回应。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 提供匿名功能，残余数据和删除诉求未解决

**原文证据：**

位置 `3576:3631`：

> We need to anonymize all user data (name, email, phone)

<a id="row-292"></a>
## 292. privacy-issue-14156

**主题代码：** PRIVACY-D, PRIVACY-I

**开放代码：** 日志隐私清理

**逐条判断：** MSAL空正文标题要求GDPR日志清理，评论明确235在dev分支；不知字段和清理机制，也不能称已稳定发布。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 开发分支实现

**原文证据：**

位置 `1451:1474`：

> Its in MSAL dev branch.

<a id="row-293"></a>
## 293. privacy-issue-14169

**主题代码：** PRIVACY-B, PRIVACY-I

**开放代码：** 隐私政策修订部署；实际处理清单核对

**逐条判断：** mySociety按GDPR起草政策并承认部分收集用途是推测，邀研究传播团队核查；后PR明确合并部署，外部员工文档未读不能声称核对正确。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 合并并部署

**原文证据：**

位置 `1341:1380`：

> areas where I've made an educated guess

位置 `2171:2194`：

> merged and deployed now

<a id="row-294"></a>
## 294. privacy-issue-14197

**主题代码：** PRIVACY-C, PRIVACY-D, PRIVACY-E

**开放代码：** IP去标识导致位置分析取消；数据最小化功能权衡

**逐条判断：** LibCrowds统计页原去后希望恢复世界地图，GDPR改后不存真实IP，明确取消未实现地图，分析可用Jupyter，待移mapbox配置。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 取消位置地图计划

**原文证据：**

位置 `3069:3123`：

> IPs have been anonymised now, so no more location maps

<a id="row-295"></a>
## 295. privacy-issue-14209

**主题代码：** PRIVACY-B, PRIVACY-D, PRIVACY-E, PRIVACY-I

**开放代码：** 收集字段最小化；联系方式定期更正；来源差异保留；政策同步

**逐条判断：** saproto清单已停止国籍性别、自填学史删除、保留UT提供学史并半年邮件核对联系方式，末政策已更新邮件已安排；非一概删除学习历史。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 清单与政策完成，邮件已排期

**原文证据：**

位置 `1068:1124`：

> persistently save the study (history) provided by the UT

位置 `1458:1502`：

> Privacy policy updated and e-mail scheduled.

<a id="row-296"></a>
## 296. privacy-issue-14234

**主题代码：** PRIVACY-A, PRIVACY-B, PRIVACY-H, PRIVACY-I

**开放代码：** 同意证据与当时文本留存；第三方记录存储；强制勾选不等于审计

**逐条判断：** Mailchimp WP用户要IP日期及确切同意文案，早期答required可不记后解释插件将邮箱IP时间送Mailchimp存；用户仍要求当时条款快照，维护者讨论设计未实现，法律充分性双方争议。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 既有第三方记录说明，文本留存未解决

**原文证据：**

位置 `4275:4319`：

> what the consumer has agreed to at that time

位置 `3793:3855`：

> sends the email address, IP address and timestamp to MailChimp

<a id="row-297"></a>
## 297. privacy-issue-14233

**主题代码：** PRIVACY-B, PRIVACY-D, PRIVACY-H, PRIVACY-I

**开放代码：** 日志遥测隐私API文档

**逐条判断：** 要求Android ADAL Logger和Telemetry更详细GDPR javadoc，一句正文无评论，无实施或具体控制细节。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 请求，实施未知

**原文证据：**

位置 `853:909`：

> more detailed GDPR javadoc for both Logger and Telemetry

<a id="row-298"></a>
## 298. privacy-issue-14327

**主题代码：** PRIVACY-A, PRIVACY-C, PRIVACY-H, PRIVACY-I

**开放代码：** iframe同意状态传递；统一分析事件；未同意阻断

**逐条判断：** AMP iframe未知父页同意且重复追踪脚本，提postMessage委托父analytics；讨论拆成事件传递与父页阻iframe或告知禁止追踪两任务，作者认可，分13196/13197关闭。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 拆分任务，未证明实现

**原文证据：**

位置 `3689:3764`：

> blocking the iframe or informing it that it cannot perform its own tracking

<a id="row-299"></a>
## 299. privacy-issue-15229

**主题代码：** PRIVACY-H, PRIVACY-I

**开放代码：** 反指纹保护兼容；手动平台选择

**逐条判断：** Rustup浏览器平台伪装导致安装指引误判，要求手选其他OS；初认领放弃后有1300 PR，无合并验证。保护工具兼容而非跟踪实现。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 已有PR，结果未知

**原文证据：**

位置 `1061:1106`：

> if you are using anti-fingerprinting software

位置 `2762:2772`：

> See #1300.

<a id="row-300"></a>
## 300. privacy-issue-15248

**主题代码：** PRIVACY-D, PRIVACY-G, PRIVACY-Y

**开放代码：** 音频指纹扰动；保护覆盖与性能权衡；测试暴露残余指纹；隐私工具媒体兼容

**逐条判断：** CanvasBlocker57评论从AudioContext按站屏蔽/伪造到多个alpha测试，Oscillator与hash/sum曾仍稳定，随机少量点和固定首30索引兼顾性能，缓存需按测试调整，alpha3获好评后正式发布；0.5.1.0b视频失败在.1b三视频用户验证修复。勿声称所有音频指纹彻底匿名。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 功能发布，多轮测试修正及媒体回归修复

**原文证据：**

位置 `21166:21189`：

> The new release is out.

位置 `22291:22322`：

> I can now play all three videos

<a id="row-301"></a>
## 301. privacy-issue-15293

**主题代码：** PRIVACY-D, PRIVACY-G, PRIVACY-H, PRIVACY-I, PRIVACY-Y

**开放代码：** OS指纹伪装；保护措施反识别风险争议；扩展替代

**逐条判断：** ungoogled Chromium稀有OS用户要改JS平台标识，维护者认为ScriptSafe能处理无需核心修改；后参与者警告TCP/IP与伪装不一致更独特并给VPN建议，均为主张未测试。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 核心不改，推荐扩展

**原文证据：**

位置 `2370:2434`：

> I don't see any need for ungoogled-chromium to do anything here.

<a id="row-302"></a>
## 302. privacy-issue-15297

**主题代码：** PRIVACY-C, PRIVACY-D, PRIVACY-F, PRIVACY-G

**开放代码：** 客户端环境最小化；外部图片IP泄露；兼容字段保留

**逐条判断：** Mumble privacy mode控制OS版本语言等发服务器，3009实现3015拟HTTP；版本release暂留因服务器依赖，最末确认外部图支持已移除、OS发送可切，不称所有客户端字段均去除。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** OS控制及外图移除完成

**原文证据：**

位置 `3024:3063`：

> external image support has been removed

位置 `2386:2445`：

> Client version/release information is currently not removed

<a id="row-303"></a>
## 303. privacy-issue-15330

**主题代码：** PRIVACY-C, PRIVACY-D, PRIVACY-G, PRIVACY-H

**开放代码：** P2P客户端指纹最小化；匿名模式可配置性

**逐条判断：** PicoTorrent要求隐藏UA peerID但承认IP仍暴露，维护者承诺下版JSON开匿名模式、GUI以后非优先；无发布证明。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 配置功能承诺，GUI延期

**原文证据：**

位置 `2241:2311`：

> I'll add a setting to the `PicoTorrent.json` file for the next release

<a id="row-304"></a>
## 304. privacy-issue-15647

**主题代码：** PRIVACY-D, PRIVACY-G

**开放代码：** 浏览器配置指纹暴露；标准风险告知

**逐条判断：** WebRTC defaultIceServers暴露用户自配ICE列表，要求指纹警告，回复认可；无API移除或防护实现证据。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 同意添加风险标识

**原文证据：**

位置 `1449:1481`：

> Thumbprint should be added, yes.

<a id="row-305"></a>
## 305. privacy-issue-17245

**主题代码：** PRIVACY-A, PRIVACY-B, PRIVACY-C, PRIVACY-E, PRIVACY-H, PRIVACY-I

**开放代码：** 同意类别管理；前后端选择传递；第三方同意服务替代

**逐条判断：** Wagtail-Pipit曾着手管理后台cookie类别文字、Next API组件及Django中间件传批准，2023明确转第三方cookie-consent关闭，不能把自建计划当最终实现。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 转用第三方服务

**原文证据：**

位置 `2240:2285`：

> We have pivoted to using third party services

<a id="row-306"></a>
## 306. privacy-issue-17517

**主题代码：** PRIVACY-B, PRIVACY-C

**开放代码：** 追踪Cookie告知；仅元数据可判

**逐条判断：** 仅标题要求网站追踪cookie告知，缺七评论正文，不推断实际追踪机制或已通知。

**材料可用性：** metadata_only。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 仅元数据，完成未知

**原文证据：**

位置 `65:127`：

> Inform users about tracking and use of cookies on your website

<a id="row-307"></a>
## 307. privacy-issue-17553

**主题代码：** PRIVACY-A, PRIVACY-B, PRIVACY-C, PRIVACY-I

**开放代码：** 营销同意独立管理；第三方脚本事前同意；核心与站点责任边界；删除能力缺口

**逐条判断：** phpvms清单部分完成但永久删除未勾选，安装器GA可关闭；站点自加广告追踪责任有争论，邮件确认不同于营销同意，脚本阻断未确认。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 部分清单完成，脚本控制未决后陈旧关闭

**原文证据：**

位置 `968:990`：

> - [ ] Permanent delete

位置 `1750:1814`：

> There is a google analytics thing included just in the installer

位置 `8200:8235`：

> The cookie consent is already there

<a id="row-308"></a>
## 308. privacy-issue-17579

**主题代码：** PRIVACY-G, PRIVACY-H, PRIVACY-I

**开放代码：** 安全Cookie默认值；TLS终止环境边界

**逐条判断：** hapi拒绝按本地HTTP自动降低secure默认，因为反向代理可终止TLS；用户可明确isSecure=false，文档可改。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 保留安全默认值

**原文证据：**

位置 `3756:3806`：

> The default is always going to be the most secure.

<a id="row-309"></a>
## 309. privacy-issue-17597

**主题代码：** PRIVACY-A, PRIVACY-B, PRIVACY-C, PRIVACY-E, PRIVACY-I

**开放代码：** 存储用途盘点；同意设置提案；本地存储与上传区分；匿名性断言待证

**逐条判断：** sttm-web区分共享darkmode cookie与本地字体阅读设置，同时承认GA事件；参与者称匿名不可指纹化未经验证，建议分类设置和记忆拒绝状态，无实现结论。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 设置提案，必要性仍讨论

**原文证据：**

位置 `2426:2471`：

> we do get google analytics events for actions

位置 `2357:2415`：

> localStorage for other stuff (not shared with our servers)

<a id="row-310"></a>
## 310. privacy-issue-17664

**主题代码：** PRIVACY-G, PRIVACY-H, PRIVACY-I, PRIVACY-Y, PRIVACY-Z

**开放代码：** 凭证迁移；隐私关联较弱

**逐条判断：** Jira云弃用密码与cookie认证，API token可直接作为basic密码使用，无需修改连接器；仅建议文档调整。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 现有兼容性确认，文档建议

**原文证据：**

位置 `1746:1804`：

> jira-connector works with API tokens with no modification.

<a id="row-311"></a>
## 311. privacy-issue-17691

**主题代码：** PRIVACY-E, PRIVACY-G, PRIVACY-H, PRIVACY-I, PRIVACY-Y, PRIVACY-Z

**开放代码：** 认证Cookie容量兼容性；会话票据服务端存储；隐私关联较弱

**逐条判断：** 完整排查Safari登录失败，过期日期假设被否定，转Redis ITicketStore解决部分Safari；Web/API共享cookie刷新竞态另待复现，不涉及告知同意。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 部分Safari问题确认解决，刷新竞态另议

**原文证据：**

位置 `21055:21146`：

> I can confirm implementing the ITicketStore solved the problem for some versions of Safari.

<a id="row-312"></a>
## 312. privacy-issue-17694

**主题代码：** PRIVACY-A, PRIVACY-B, PRIVACY-Z

**开放代码：** Cookie政策告知；实质证据不足

**逐条判断：** 正文空，仅Cookie policy notice标题及致谢，虽完整抓取仍无法判断告知内容或实施方式。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 致谢并关闭，实施细节未知

**原文证据：**

位置 `1109:1124`：

> Thanks to @towc

<a id="row-313"></a>
## 313. privacy-issue-17763

**主题代码：** PRIVACY-B, PRIVACY-C, PRIVACY-H, PRIVACY-I

**开放代码：** 第三方资源附带Cookie；依赖选择责任

**逐条判断：** 用户询问静态网站图标服务两个cookie必要性和避免方式，Buefy称库不提供该图标可自行选择，无实际移除证明。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 解释依赖边界

**原文证据：**

位置 `1444:1491`：

> Buefy lib doesn't provide material design icons

<a id="row-314"></a>
## 314. privacy-issue-17804

**主题代码：** PRIVACY-A, PRIVACY-E, PRIVACY-H, PRIVACY-I

**开放代码：** 非必要会话范围缩减；必要Cookie法律理解争议；隐私与功能权衡

**逐条判断：** Bludit从所有访客发session改仅admin区域，前台编辑入口登录检测受影响给出显式Login代码；用户确认可用。法律豁免是参与者观点。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 缩减会话范围且用户验证

**原文证据：**

位置 `3473:3517`：

> I disabled session cookie for the front page

位置 `4568:4589`：

> Thanks! Working fine.

<a id="row-315"></a>
## 315. privacy-issue-17779

**主题代码：** PRIVACY-A, PRIVACY-H

**开放代码：** 同意交互故障；环境复现不足

**逐条判断：** Odoo10点击Cookie按钮报JsonRequest无httpsession，回复要求runbot复现以区分安装问题，无修复证据。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 待复现后关闭

**原文证据：**

位置 `970:1021`：

> 'JsonRequest' object has no attribute 'httpsession'

<a id="row-316"></a>
## 316. privacy-issue-18338

**主题代码：** PRIVACY-A, PRIVACY-F, PRIVACY-I

**开放代码：** 人员行为关联记录；用途告知与主动同意；系统间数据共享边界

**逐条判断：** 拟记录视频志愿者姓名昵称邮件与演讲关联以质量反馈，争论本地输入和Engelsystem导出；强调可变更opt-in，最后建议API定时导入tracker，无实现。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 跨系统方案建议

**原文证据：**

位置 `2548:2658`：

> are we allows to store you name, nickname and mail together with the talk you worked on to improve the quality

<a id="row-317"></a>
## 317. privacy-issue-18336

**主题代码：** PRIVACY-E, PRIVACY-F, PRIVACY-I

**开放代码：** 内容保留期限控制；联邦删除不可保证；删除与审核留证权衡；隐私设置复杂性

**逐条判断：** Mastodon逐帖/账户自动到期以减足迹画像，讨论举报留证和界面复杂；远端实例或截图无法保证删除。按重复关闭，2024指出逐帖时限差异请求重开。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 重复关闭，具体功能未证实

**原文证据：**

位置 `12502:12534`：

> it can't be a certified deletion

位置 `14013:14079`：

> this issue is not a duplicate because requesting a per-post option

<a id="row-318"></a>
## 318. privacy-issue-18402

**主题代码：** PRIVACY-C, PRIVACY-G, PRIVACY-H, PRIVACY-I

**开放代码：** 局域网发现隐私；可选网络广播控制；隐私与媒体兼容权衡；风险假设修正

**逐条判断：** ungoogled早期Google服务器依赖猜测被撤回，mDNS即使不上传也广播存在性；未测试补丁多次纠错，最终原生cast flag在官方81及其他用户验证工作，不能据此认定全部广播风险验证。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 可选flag功能验证，关闭

**原文证据：**

位置 `5455:5496`：

> My previous comment was pure speculation.

位置 `17685:17740`：

> it is the act of broadcasting itself that is the issue.

位置 `29078:29111`：

> Can confirm, it works for me too!

<a id="row-319"></a>
## 319. privacy-issue-18395

**主题代码：** PRIVACY-B, PRIVACY-C, PRIVACY-I

**开放代码：** 隐私政策可见性；服务端日志透明度；追踪指控澄清

**逐条判断：** docs.rs被要求广告追踪政策和退出，维护者说明无客户端追踪广告，服务端访问日志及基础设施IP保留仍需询问；新政策已有但全页链接待加。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 政策新增，链接完成未见直接证据

**原文证据：**

位置 `1634:1663`：

> We only have server-side logs

位置 `2551:2611`：

> I'll leave this issue open until we link to it on every page

<a id="row-320"></a>
## 320. privacy-issue-18411

**主题代码：** PRIVACY-F, PRIVACY-G, PRIVACY-H

**开放代码：** 自动填充目标错位；凭证意外披露

**逐条判断：** Keeweb全屏浏览器弹窗选项后焦点落Slack使密码写入聊天框；提出重新比对窗口标题后输入，未见实现验证。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 修复方案提出

**原文证据：**

位置 `2070:2158`：

> The proposed fix is to get window title again and run auto-type only after a comparison.

<a id="row-321"></a>
## 321. privacy-issue-18442

**主题代码：** PRIVACY-G, PRIVACY-I, PRIVACY-Y, PRIVACY-Z

**开放代码：** 诊断材料保密；私下调试证据共享；核心故障隐私关联较弱

**逐条判断：** Terraform幂等性主要由同policy多attachment竞争引起，隐私是用户拒公开调试日志并私发邮件；维护者请求无secret复现，最终切role attachment成功。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 私发诊断，配置迁移解决

**原文证据：**

位置 `2306:2344`：

> I'm not willing to paste this publicly

位置 `13224:13272`：

> I switched as well and it works great for roles.

<a id="row-322"></a>
## 322. privacy-issue-18507

**主题代码：** PRIVACY-F, PRIVACY-G, PRIVACY-I

**开放代码：** 财务数据第三方托管风险；自托管访问边界；传输加密与身份保护

**逐条判断：** Fava移动录入本为易用性，公共同步服务方案因会收全部交易遭反对后撤回，转移动表单；建议仅暴露录入路由或TLS和HTTP认证，后续讨论自动完成文件写入，无完整交付证明。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 撤回公共服务方案，表单设计推进

**原文证据：**

位置 `12145:12241`：

> This sounds like a bigger privacy issue, since the web service is getting all your transactions!

位置 `14253:14286`：

> Forget about the web service-idea

<a id="row-323"></a>
## 323. privacy-issue-18501

**主题代码：** PRIVACY-E, PRIVACY-F, PRIVACY-H, PRIVACY-I

**开放代码：** 本地历史不记录模式；隐私状态可见性；不记录与匿名区分；开发资源限制

**逐条判断：** Transportr多个搜索入口不写历史并明确状态的设计，早期称设置已试作但最终无合并因资源关闭；清应用数据丢偏好，切提供商仅隐藏，不等同精确删除；不记录不代表Tor匿名。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 未解决关闭，替代操作有损失

**原文证据：**

位置 `8024:8101`：

> privacy mode doesn't give the impression that people are completely anonymous

位置 `15960:15988`：

> Added the 'unresolved' label

<a id="row-324"></a>
## 324. privacy-issue-18522

**主题代码：** PRIVACY-C, PRIVACY-H, PRIVACY-I

**开放代码：** 后台网络访问控制；隐私范围认知冲突；错误提示替代行为控制

**逐条判断：** VSCode禁遥测后仍尝试扩展更新遭防火墙阻断，用户想禁止访问；维护者认为非隐私问题仅承诺隐藏错误，未禁止请求，不推断成功外传。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 拒绝阻止网络访问

**原文证据：**

位置 `1653:1710`：

> We will not prevent access, but omit the message instead.

<a id="row-325"></a>
## 325. privacy-issue-18510

**主题代码：** PRIVACY-F, PRIVACY-G

**开放代码：** 跨用户地址自动补全暴露；共享实例隔离；修复后回归

**逐条判断：** Nextcloud最初怀疑收件人表但发现系统accounts联系人源，NC12修复声明，手改NC11使补全全无；12.0.4关闭补全仍再现，要求新回归单。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 修复后再报回归

**原文证据：**

位置 `3993:4049`：

> there are users on my system who must not see each other

位置 `6119:6164`：

> please file a new ticket for this regression.

<a id="row-326"></a>
## 326. privacy-issue-18520

**主题代码：** PRIVACY-B, PRIVACY-C, PRIVACY-I

**开放代码：** 位置查询披露告知；崩溃报告潜在位置暴露；独立隐私政策适配

**逐条判断：** Commons Nearby向Wikidata披露位置，担忧未来错误报告坐标，提开发者用途保密约束；原WMF政策不可直接用改本项目政策，最终登录链接确认实现，不把潜在日志当已泄漏。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 政策链接已实现

**原文证据：**

位置 `12373:12418`：

> Indeed the link has already been implemented.

位置 `10593:10641`：

> Unfortunately we cannot use WMF's privacy policy

<a id="row-327"></a>
## 327. privacy-issue-18555

**主题代码：** PRIVACY-F, PRIVACY-H, PRIVACY-I

**开放代码：** 定位权限最小化；手动位置替代GPS

**逐条判断：** 天气默认位置需求含可选GPS，维护者以隐私友好拒绝定位权限，重设计采用列表首项默认，无需GPS。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 确定手动默认位置设计

**原文证据：**

位置 `1768:1813`：

> use of the location permission is not desired

<a id="row-328"></a>
## 328. privacy-issue-18585

**主题代码：** PRIVACY-B, PRIVACY-G, PRIVACY-H, PRIVACY-I

**开放代码：** 平台敏感权限用途说明；依赖归因不确定；缓存路径调整

**逐条判断：** AppStore指缺相册用途说明，FFImageLoading称无相册访问，修正Library到Caches；后用户升级仍拒，怀疑其他库，不能认定该库实际读取照片或升级解决。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 路径修正，后续拒审未解决且归因转移

**原文证据：**

位置 `4859:4902`：

> updating to 2.2.13 hasn't fixed the problem

<a id="row-329"></a>
## 329. privacy-issue-18575

**主题代码：** PRIVACY-C, PRIVACY-D, PRIVACY-I, PRIVACY-Y

**开放代码：** 随机响应遥测提案；统计代表性与信任；匿名性认知争议；隐私机制复杂性权衡

**逐条判断：** Syncthing建议RAPPOR减少文件夹大小等上报敏感性以提高参与，维护者认为无法关联个人且选择不报即可，复杂度过高，提案者接受未采纳。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 提案拒绝，维持自愿上报

**原文证据：**

位置 `6360:6406`：

> vastly overkill in complexity for our use case

<a id="row-330"></a>
## 330. privacy-issue-18600

**主题代码：** PRIVACY-G, PRIVACY-H, PRIVACY-I, PRIVACY-Y

**开放代码：** 反指纹保护兼容性；禁用Canvas优雅降级

**逐条判断：** 用户禁Canvas防指纹导致ChartJS异常连累其他脚本，维护者接受避免崩溃，最终指PR修复；不能当指纹算法改进。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 修复已报告

**原文证据：**

位置 `2196:2210`：

> Fixed in #3474

<a id="row-331"></a>
## 331. privacy-issue-18613

**主题代码：** PRIVACY-C, PRIVACY-F, PRIVACY-Y

**开放代码：** 社交组件第三方请求；跟踪暴露担忧；功能误解撤回

**逐条判断：** Jetpack图文按钮仍查Facebook计数被认为多余追踪，作者随后承认各样式都显示非零计数而撤回bug；网络请求仍存在，可过滤计数。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 缺陷判断撤回

**原文证据：**

位置 `2074:2139`：

> All button styles would have the sharing count show on the button

<a id="row-332"></a>
## 332. privacy-issue-18603

**主题代码：** PRIVACY-F, PRIVACY-H

**开放代码：** 通知内容旁观暴露；屏幕共享隐私；通知粒度控制

**逐条判断：** Yakyak希望关闭含正文toast但保留任务栏闪烁，演示共享屏幕会泄消息；拟View菜单跨平台独立于系统全局通知，无完成证明。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 独立通知设置提案

**原文证据：**

位置 `1059:1118`：

> a pop-up/toast notification appears, containing the message

<a id="row-333"></a>
## 333. privacy-issue-18830

**主题代码：** PRIVACY-A, PRIVACY-B, PRIVACY-I

**开放代码：** 双重确认同意；同意凭证记录

**逐条判断：** EspoCRM拟邮件点击记录时间IP及确认状态，以GDPR为理由；2022维护者指lead capture已实现，未核外链全部记录字段。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 维护者称lead capture实现

**原文证据：**

位置 `2557:2595`：

> It's implemented in the [lead capture]

<a id="row-334"></a>
## 334. privacy-issue-18863

**主题代码：** PRIVACY-A, PRIVACY-B, PRIVACY-H, PRIVACY-I

**开放代码：** 退出权与管理员限制；退出说明失真

**逐条判断：** SMF管理员禁止用户关闭公告但邮件仍教取消，要求删除无效说明；作者另质疑禁止退出合法性，没有修复或法律结论。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 文本一致性需求，结果未知

**原文证据：**

位置 `1360:1400`：

> Because users cannot change this setting

<a id="row-335"></a>
## 335. privacy-issue-18902

**主题代码：** PRIVACY-E, PRIVACY-F, PRIVACY-G

**开放代码：** 可移除介质明文位置暴露；个人与公共数据存储分离；本地数据责任争议

**逐条判断：** OsmAnd地图与家庭工作轨迹共目录在SD卡，用户担忧失窃提出拆分；维护者承认风险但以跨应用便利和本地责任反对，Android权限回应未直接解决拔卡读取。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 方案遭反对，无分离实现

**原文证据：**

位置 `2008:2049`：

> Even though the issue you describe exists

位置 `1596:1648`：

> keep privacy-related information in internal storage

<a id="row-336"></a>
## 336. privacy-issue-18894

**主题代码：** PRIVACY-A, PRIVACY-B, PRIVACY-H

**开放代码：** 隐私告知可配置性

**逐条判断：** GeoNode希望主题模型支持开启定制Cookies与Privacy警告，仅正文和图片链接，无评论实现证据。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 可配置告知提案

**原文证据：**

位置 `936:990`：

> turn on and customize the "Cookies & Privacy" warnings

<a id="row-337"></a>
## 337. privacy-issue-18927

**主题代码：** PRIVACY-B, PRIVACY-C, PRIVACY-H, PRIVACY-I

**开放代码：** 第三方CDN连接披露；自托管资源替代；分析数据最小化配置

**逐条判断：** VuePress WorkboxCDN向Google发IP且可能跨站关联，提local导入；GA匿名IP与SSL另议。最终alpha47 PWA generateSWConfig支持local，未证GA建议一并修复。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 本地Workbox配置已实现

**原文证据：**

位置 `7963:7980`：

> Fixed at 4640614.

位置 `2763:2789`：

> importWorkboxFrom: 'local'

<a id="row-338"></a>
## 338. privacy-issue-18955

**主题代码：** PRIVACY-A, PRIVACY-H

**开放代码：** Cookie接受拒绝入口

**逐条判断：** Elementor请求首页弹窗选择cookie，维护者称开发中并合并628，无完成证据。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 开发中并合并相关议题

**原文证据：**

位置 `1913:1971`：

> we are already working on implementing something like that

<a id="row-339"></a>
## 339. privacy-issue-18987

**主题代码：** PRIVACY-E, PRIVACY-I

**开放代码：** 日志按时间保留；容量限制不足

**逐条判断：** Docker用户要求按天轮换删除敏感日志以控制保留，容量限制不能保证期限；不求精确秒级，按重复并入36853。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 重复合并，无实现证明

**原文证据：**

位置 `949:991`：

> keeping logs only a limited amount of time

位置 `2468:2497`：

> This is a duplicate of #36853

<a id="row-340"></a>
## 340. privacy-issue-18993

**主题代码：** PRIVACY-A, PRIVACY-B, PRIVACY-H, PRIVACY-I

**开放代码：** 数据提交前政策确认；同意插件复用

**逐条判断：** Mailchimp扩展接受checkbox获免费EU opt-in附加插件指引，后续转国际地址非必填仍校验state问题，以filter临时修复，不把地址校验当同意机制。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 指向现有同意插件

**原文证据：**

位置 `1334:1378`：

> we have a free add-on that does exactly that

<a id="row-341"></a>
## 341. privacy-issue-20173

**主题代码：** PRIVACY-E, PRIVACY-F, PRIVACY-H

**开放代码：** 身份信息持久存储权衡；会话隔离与便利性

**逐条判断：** OIDC跨tab欲localStorage，需WebStorageStateStore包装；维护者因PII不推荐并建议silent renew，后用户统一UserManager配置解决登录，无泄漏报告。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 持久化配置可行，建议会话续期

**原文证据：**

位置 `2290:2343`：

> localStorage is slightly discouraged for PII reasons.

<a id="row-342"></a>
## 342. privacy-issue-20208

**主题代码：** PRIVACY-F, PRIVACY-I

**开放代码：** 避免收集订阅邮箱；RSS替代通知

**逐条判断：** Chromium dashboard邮件订阅须保存邮箱遭隐私团队顾虑，以RSS加max-items替代，避免新PII列表。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 建议RSS替代

**原文证据：**

位置 `1224:1273`：

> This would require storing a list of user emails.

<a id="row-343"></a>
## 343. privacy-issue-20235

**主题代码：** PRIVACY-C, PRIVACY-D, PRIVACY-G, PRIVACY-I

**开放代码：** 异常处理再泄漏；遥测发送前净化

**逐条判断：** VSCode已净化异常但AppInsights不认错误对象再抛错生成含PII堆栈，最初提全局禁堆栈，最终Telemetry Processor处理所有遥测称可用并计划0.15.19。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 新增遥测处理器，版本发布承诺

**原文证据：**

位置 `2100:2148`：

> It is now possible to process all telemetry data

<a id="row-344"></a>
## 344. privacy-issue-20237

**主题代码：** PRIVACY-C, PRIVACY-D, PRIVACY-G, PRIVACY-I

**开放代码：** 交互面包屑敏感内容过滤；发送前脱敏扩展点

**逐条判断：** BugSnag问排除含PII元素，无现成UI；beforeNotify遍历crumb按selector把targetText隐藏，示例方案未验证且原码语法不完整。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 提供hook过滤建议

**原文证据：**

位置 `1485:1542`：

> modify the exception payload before it is sent to Bugsnag

<a id="row-345"></a>
## 345. privacy-issue-20400

**主题代码：** PRIVACY-A, PRIVACY-B, PRIVACY-C, PRIVACY-I

**开放代码：** 默认营销共享同意质疑；法律咨询分流

**逐条判断：** Fenix默认Leanplum分享合法性被问，转Legal后要求直接邮件compliance关闭；未回答是否合规或改默认。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 转合规邮箱，无实质结论

**原文证据：**

位置 `1828:1881`：

> There is not anything that can be done in this issue.

<a id="row-346"></a>
## 346. privacy-issue-20416

**主题代码：** PRIVACY-A, PRIVACY-B, PRIVACY-H, PRIVACY-I

**开放代码：** 分类同意管理；嵌入内容事前阻断；Cookie之外终端存储；分阶段隐私实现

**逐条判断：** Decidim由告知转接受拒绝，四类必要/偏好/分析/营销；拟先全部iframe要求全类别同意，后编辑器分类，analytics单独门控；覆盖local/sessionStorage但沿用Cookie术语，清单未勾。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 方案确定，实际完成未证

**原文证据：**

位置 `5314:5382`：

> Disable all analytics scripts until the user has given their consent

位置 `7507:7554`：

> we'll keep referring to this to "Cookie policy"

<a id="row-347"></a>
## 347. privacy-issue-20435

**主题代码：** PRIVACY-B, PRIVACY-H

**开放代码：** 隐私告知组件性能兼容

**逐条判断：** Otter与Cookie插件导致大量资源加载慢超时，怀疑阻脚本后定位旧版wp_kses交互但精确原因不明，2.0双方验证恢复，不涉及绕过同意。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 升级2.0验证解决

**原文证据：**

位置 `4296:4363`：

> everything looks great with Otter 2.0, and the page loads instantly

<a id="row-348"></a>
## 348. privacy-issue-20498

**主题代码：** PRIVACY-A, PRIVACY-B, PRIVACY-C, PRIVACY-H, PRIVACY-I

**开放代码：** 告知冒充选择；嵌入视频无Cookie需求；第三方合规压力

**逐条判断：** lbry广告伙伴限期合规，最初明确只同意不拒绝banner，后来用户指出仅横幅不足、嵌入auth_token/localstorage需控制并要求无cookie版本，未见落实。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 告知方案被质疑，控制缺口未解决

**原文证据：**

位置 `2338:2389`：

> the text that says they are agreeing to the cookies

<a id="row-349"></a>
## 349. privacy-issue-20527

**主题代码：** PRIVACY-B, PRIVACY-I, PRIVACY-Z

**开放代码：** Cookie用途盘点支持告知

**逐条判断：** OWA尚未运行用户先准备法律告知，问是否用cookie，维护者仅确认是，无种类同意机制信息。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 确认使用Cookie

**原文证据：**

位置 `1639:1651`：

> Yes it does.

<a id="row-350"></a>
## 350. privacy-issue-20503

**主题代码：** PRIVACY-A, PRIVACY-C, PRIVACY-H, PRIVACY-I

**开放代码：** 同意前追踪脚本门控；实现指导不足

**逐条判断：** OWA用户要求无同意不放cookie，愿整个分析停用；建议自设consent cookie条件包裹tracker，但求例子未获，无内建完成证据。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 提供原则建议，未提供例子

**原文证据：**

位置 `1875:1918`：

> Just wrap the tracker code in a conditional

<a id="row-351"></a>
## 351. privacy-issue-20525

**主题代码：** PRIVACY-A, PRIVACY-B, PRIVACY-C, PRIVACY-H, PRIVACY-I

**开放代码：** 第三方同意方案集成

**逐条判断：** AMPforWP请求iubenda，回复插件已支持并给设置和指南，外链未核，不推出实际站点安装。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 现有集成可用声明

**原文证据：**

位置 `1460:1520`：

> already added their cookie solution for ampforwp plugin too.

<a id="row-352"></a>
## 352. privacy-issue-20209

**主题代码：** PRIVACY-C, PRIVACY-D, PRIVACY-G, PRIVACY-I

**开放代码：** 遥测PII验证；验证范围有限

**逐条判断：** VSCode重构要求错误与数据遥测无PII，dashboard登录阻塞解除后确认数据及扩展错误存在；快速浏览未见PII并预计未来另报，不是穷尽无泄漏保证。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 有限抽查未发现PII

**原文证据：**

位置 `2957:3009`：

> Quickly going through telemtry I did not see any PII

<a id="row-353"></a>
## 353. privacy-issue-20536

**主题代码：** PRIVACY-A, PRIVACY-C, PRIVACY-H

**开放代码：** 同意前SDK初始化控制；禁用设置失效报告

**逐条判断：** OneSignal指南先关闭自动init再requiresUserPrivacyConsent并接受后provideUserConsent；2020用户称关闭仍初始化且双定义错误，无回复修复。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 已有指导，后报控制可能失效

**原文证据：**

位置 `3101:3136`：

> it seems like it still initializes.

<a id="row-354"></a>
## 354. privacy-issue-20655

**主题代码：** PRIVACY-A, PRIVACY-B, PRIVACY-I, PRIVACY-Z

**开放代码：** Cookie政策内容制定；法规资料收集

**逐条判断：** comses链接法律与django插件并要求和directorate迭代内容，正文未给实际banner门控，外链不是已实现证据。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 内容制定过程，结果未知

**原文证据：**

位置 `2126:2173`：

> iterate on cookie page content with directorate

<a id="row-355"></a>
## 355. privacy-issue-20628

**主题代码：** PRIVACY-A, PRIVACY-B, PRIVACY-I

**开放代码：** 必要与偏好Cookie盘点；告知需求发现

**逐条判断：** mars拟登录和locale cookie，发现Laravel已记住我，讨论需否弹窗并决定加message；法律理解不确切、未实现验证。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 决定新增告知

**原文证据：**

位置 `3007:3045`：

> this means we should add that message.

<a id="row-356"></a>
## 356. privacy-issue-20664

**主题代码：** PRIVACY-A, PRIVACY-B, PRIVACY-H, PRIVACY-I

**开放代码：** 网站告知与库职责边界

**逐条判断：** ember-simple-auth加cookie warning被误读为强制库用户UI，作者澄清仅项目官网；无实现证明。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 澄清仅官网范围

**原文证据：**

位置 `2069:2107`：

> this is for ember-simple-auth.com only

<a id="row-357"></a>
## 357. privacy-issue-20665

**主题代码：** PRIVACY-B, PRIVACY-H, PRIVACY-I

**开放代码：** 上游隐私提示破坏内容提取；地域归因未证

**逐条判断：** RSS-Bridge Twitter feed混入Cookie跨境告知，EU原因猜测被德国可用反馈削弱，作者后称自行停止追加，无本地修复。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 现象消失后关闭

**原文证据：**

位置 `2330:2389`：

> It seems to have stopped appending messages to Twitter now.

<a id="row-358"></a>
## 358. privacy-issue-20707

**主题代码：** PRIVACY-A, PRIVACY-C, PRIVACY-I

**开放代码：** 遥测默认同意争议；部署者与终端用户边界；升级引入追踪风险；自托管分析替代

**逐条判断：** Keystone拟默认opt-out管理后台分析，用户反对开源部署隐含追踪；从官网类比转承认是他人站点，提出generator opt-in默认yes或后台首次询问、Piwik，旧讨论关闭未给实施。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 讨论结束关闭，无实现证明

**原文证据：**

位置 `17316:17376`：

> it's somebody else's and we're installing our tracking in it

位置 `19209:19251`：

> Closing this as a concluded/old discussion

<a id="row-359"></a>
## 359. privacy-issue-21175

**主题代码：** PRIVACY-B, PRIVACY-I, PRIVACY-Z

**开放代码：** 广告SDK合规集成求助

**逐条判断：** Ionic3 admob-free问EU GDPR支持，仅inactive自动回复，未具体说明同意机制。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 无人回答，陈旧关闭

**原文证据：**

位置 `909:954`：

> How To Add General Data Protection Regulation

<a id="row-360"></a>
## 360. privacy-issue-21242

**主题代码：** PRIVACY-E, PRIVACY-I

**开放代码：** 长期车况数据托管责任；云存储隐私与维护约束；功能放弃

**逐条判断：** CanZE按VIN长期电池衰减需跨手机寿命保存，开发者无法承担云保护法规维护，考虑个人Drive/IoT/MQTT；最终拒CanZE内建衰减，WiFi网关MQTT另议。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 因托管责任放弃内建功能

**原文证据：**

位置 `6120:6180`：

> we will not implement a degradation function in CanZE itself

<a id="row-361"></a>
## 361. privacy-issue-21350

**主题代码：** PRIVACY-B

**开放代码：** 收集入口隐私声明缺失

**逐条判断：** HMDA页首邮件列表注册缺Privacy Act Statement链接，仅缺陷描述无修复细节。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 结果未知

**原文证据：**

位置 `797:834`：

> Privacy Act Statement link in missing

<a id="row-362"></a>
## 362. privacy-issue-21399

**主题代码：** PRIVACY-B, PRIVACY-I, PRIVACY-Z

**开放代码：** 组织数据治理职责；隐私关联较弱

**逐条判断：** ONRR人员能力及组织规划问题将Privacy Act列在多项法规例子中，回复仅内部草稿待审；无具体个人数据机制。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 组织规划草稿

**原文证据：**

位置 `1282:1350`：

> What initiatives, laws, regulations, etc. does IDM need to adhere to

<a id="row-363"></a>
## 363. privacy-issue-21495

**主题代码：** PRIVACY-B, PRIVACY-I, PRIVACY-Z

**开放代码：** 儿童隐私合规目标；实质证据不足

**逐条判断：** Mindlogger要求COPPA合规，只有Wikipedia链接无机制或验收，不能推断监护人同意已实施。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 目标提出，细节不足

**原文证据：**

位置 `81:104`：

> Ensure COPPA Compliance

<a id="row-364"></a>
## 364. privacy-issue-21500

**主题代码：** PRIVACY-D, PRIVACY-E, PRIVACY-I

**开放代码：** 敏感轨迹去标识；分享粒度用户选择；公共健康与隐私权衡

**逐条判断：** Safeplaces拟按可识别性概率删坐标，建议居家停留时长提示，用户选客户端删减或完整给可信接触追踪员；概率定义尚受质疑，转Jira反馈非实现。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 记录需求后迁移

**原文证据：**

位置 `1591:1654`：

> Share an auto-redacted (client side) OR to share a full history

<a id="row-365"></a>
## 365. privacy-issue-21604

**主题代码：** PRIVACY-B, PRIVACY-D, PRIVACY-F, PRIVACY-G

**开放代码：** 公开元数据再披露边界；调试材料脱敏；用户账号与作品元数据区分；团队共享规范

**逐条判断：** Jupiter迁移缺元数据引发实际姓名替换，成员争论已公开论文元数据是否可Github引用；协议允许作品分发但CCID/email保护另属问题，建议团队规范。最终关闭确认展示缺陷修复，不证明隐私规范已建。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 展示问题解决，信息共享规范建议

**原文证据：**

位置 `12515:12580`：

> User data (CCID and other information that comes from CCID login)

位置 `20728:20796`：

> establish team guidelines and best practices for sharing information

<a id="row-366"></a>
## 366. privacy-issue-2172

**主题代码：** PRIVACY-A, PRIVACY-B, PRIVACY-E, PRIVACY-H, PRIVACY-I

**开放代码：** 政策版本更新再确认；必要服务与可选同意区分；登录前后同意边界

**逐条判断：** Nextcloud要求登录前ToS/PP勾选及变更随机码重确认，回复必要login cookie仅告知、额外广告同意另app；最终ToS app登录后显示不满足原登录前要求。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 导向现有登录后ToS应用

**原文证据：**

位置 `5606:5648`：

> Right now it will show the ToS after login

<a id="row-367"></a>
## 367. privacy-issue-14120

**主题代码：** PRIVACY-E, PRIVACY-H, PRIVACY-I

**开放代码：** 关联用户工单删除；非技术人员删除能力

**逐条判断：** Zammad过量导入及spam自动账号需彻底清除，UI只能关闭且慢，Rails控制台可删，GDPR推动客服无需server权限操作；并入WIP2074未完成证明。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 控制台替代，UI工作迁移

**原文证据：**

位置 `3667:3730`：

> delete old customer information without requiring server access

<a id="row-368"></a>
## 368. privacy-issue-291

**主题代码：** PRIVACY-A, PRIVACY-B, PRIVACY-C, PRIVACY-I

**开放代码：** 分析收集告知；资助方数据需求；法律审查协调

**逐条判断：** globaldothealth为资助与评估加GA，已有注册邮箱与政策接受记录，希望Cookie提示传达跟踪；BCH GA账号就绪不等于告知/门控完成。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 分析账号就绪，隐私机制未证

**原文证据：**

位置 `1302:1368`：

> loop in legal to ensure we appropriately communicate data tracking

<a id="row-369"></a>
## 369. privacy-issue-8274

**主题代码：** PRIVACY-B, PRIVACY-F, PRIVACY-G, PRIVACY-I, PRIVACY-Y

**开放代码：** 调试截图通讯录暴露；身份注册状态不确定

**逐条判断：** Signal错误入网提示未复现，维护者实际删除通讯录截图保护隐私；单勾表示号已注册但不证明本人安装，批量冒用只是作者猜测，stale关闭。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 截图已删，注册疑问未解决

**原文证据：**

位置 `3007:3069`：

> just gonna delete it now that I've seen it for privacy reasons

<a id="row-370"></a>
## 370. privacy-issue-20390

**主题代码：** PRIVACY-C, PRIVACY-H, PRIVACY-I

**开放代码：** 隐私增强视频域名；承诺未交付

**逐条判断：** lightGallery求youtube-nocookie选项并获承诺，但随后两轮stale且请求重开，没有交付证据。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 承诺后陈旧关闭

**原文证据：**

位置 `2160:2184`：

> Sure, I'll add an option

位置 `3697:3722`：

> please reopen this issue.

<a id="row-371"></a>
## 371. privacy-issue-8227

**主题代码：** PRIVACY-G, PRIVACY-H, PRIVACY-I

**开放代码：** DNS加密可配置性

**逐条判断：** Fenix求设置页DoH与桌面一致，仅重复4584回复。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 重复合并

**原文证据：**

位置 `1004:1033`：

> add option for DNS over HTTPS

<a id="row-372"></a>
## 372. privacy-issue-15131

**主题代码：** PRIVACY-G, PRIVACY-H, PRIVACY-I

**开放代码：** 反指纹时区兼容性；手动设置补偿

**逐条判断：** Firefox抗指纹统一UTC导致Nextcloud日历错时，讨论保留自动检测加UTC提示及手动覆盖，拒默认server时区；临时用其他CalDAV客户端，无实现证据。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 手动覆盖方案，替代客户端

**原文证据：**

位置 `2909:2991`：

> If we detect UTC, tell the user that this might be related to some privacy feature

<a id="row-373"></a>
## 373. privacy-issue-941

**主题代码：** PRIVACY-D, PRIVACY-F, PRIVACY-I

**开放代码：** 跨系统病例共享；可选伪名化粒度

**逐条判断：** SORMAS发送单病例/联系人UI需选接收者清理引用并序列化，可无伪名化/个人数据/全部敏感数据三层，零评论未证实现。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 共享UI需求

**原文证据：**

位置 `1446:1478`：

> pseudonymized all sensitive data

<a id="row-374"></a>
## 374. privacy-issue-4956

**主题代码：** PRIVACY-D, PRIVACY-E, PRIVACY-F, PRIVACY-I

**开放代码：** 保留账户匿名化；管理员隐私操作

**逐条判断：** Chamilo缺不删用户的匿名化选项，要求管理员列表图标，作者明确Feature implemented，但未给字段或不可逆保证。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 实现已报告

**原文证据：**

位置 `1322:1341`：

> Feature implemented

<a id="row-375"></a>
## 375. privacy-issue-217

**主题代码：** PRIVACY-E, PRIVACY-H

**开放代码：** 浏览器退出清理不完整；非Cookie存储遗漏；规则匹配行为区分

**逐条判断：** CAD灰名单重启未删localStorage/其他站点数据，维护者复现；另用户wildcard清按钮误解不代表主问题解决，完整日志显示cleanup false，最后3.7.0 Firefox发布修复。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 3.7.0发布修复

**原文证据：**

位置 `20604:20663`：

> This is included in 3.7.0 and has been released on Firefox.

<a id="row-376"></a>
## 376. privacy-issue-2566

**主题代码：** PRIVACY-H, PRIVACY-I, PRIVACY-Y

**开放代码：** 隐私扩展网站兼容；故障归因不确定

**逐条判断：** DDG扩展启用时Vivaldi Gmail加载失败，关后好；后升级重试恢复，可能扩展互扰或浏览器，不证明具体修复因果。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 用户确认恢复，原因未知

**原文证据：**

位置 `3121:3146`：

> things seems to work now.

<a id="row-377"></a>
## 377. privacy-issue-8374

**主题代码：** PRIVACY-A, PRIVACY-B, PRIVACY-I

**开放代码：** 同意记录与撤回；拒绝后服务可用性；客户端追踪盘点

**逐条判断：** alkem需研究React同意组件并列出追踪，引用规范强调事前明确用途、记录及易撤回、拒绝可服务，验收未勾无实现。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 调查需求

**原文证据：**

位置 `1613:1660`：

> Document and store consent received from users.

<a id="row-378"></a>
## 378. privacy-issue-8254

**主题代码：** PRIVACY-E, PRIVACY-F, PRIVACY-H

**开放代码：** 到期消息残留；多端保留策略不一致；修复声明与持续反例

**逐条判断：** Signal桌面跨OS群聊单聊过期不删而手机正常；5.5宣称修复又区分旧消息迁移，新清理仍5.11/5.30报告，最终stale后建议升级。不可当完整修复。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 部分修复声明，持续残留报告

**原文证据：**

位置 `10030:10089`：

> We do expect to release a change that will fix old messages

位置 `11483:11516`：

> This is still happening in 5.11.0

<a id="row-379"></a>
## 379. privacy-issue-2965

**主题代码：** PRIVACY-B, PRIVACY-C, PRIVACY-I

**开放代码：** 分析数据访问治理；无Cookie分析迁移；政策更新

**逐条判断：** Carpentries原问资助统计数据访问权，后讨论GA同意与替代；确认lesson template已改cookieless Matomo，整个组织与政策仍进行中，不能认定无所有PII。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 模板迁移完成，整体进行中

**原文证据：**

位置 `3202:3246`：

> I did so in 25a5b9f for the lesson template.

<a id="row-380"></a>
## 380. privacy-issue-18973

**主题代码：** PRIVACY-F, PRIVACY-G, PRIVACY-H

**开放代码：** 空闲退出失效；后台轮询冒充用户活动

**逐条判断：** Nextcloud30秒通知heartbeat续命阻自动退出造成旁观访问风险；早报告已设keepalive=false仍失败，最终维护者又给此配置和源码，未解释前述矛盾或用户验证。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 配置方案给出，效果存在冲突

**原文证据：**

位置 `1056:1098`：

> Notification polling kills our auto-logout

位置 `2188:2216`：

> 'session_keepalive' => false

<a id="row-381"></a>
## 381. privacy-issue-11550

**主题代码：** PRIVACY-A, PRIVACY-C, PRIVACY-I

**开放代码：** 同意执行旁路；广告标识统一来源；多方同意责任边界

**逐条判断：** Prebid通过不传userId强制purpose4，但多个adapter从params/window取绕开；DigiTrust变更暂停，部分QA/internal任务，IX声称独立库已按同意处理，stale未证全修。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 部分调整进行，整体未验证

**原文证据：**

位置 `2151:2225`：

> Few adapters have been found populating user id values from other sources.

<a id="row-382"></a>
## 382. privacy-issue-18374

**主题代码：** PRIVACY-B, PRIVACY-H

**开放代码：** 隐私设置可理解性；本地化与无障碍显示

**逐条判断：** Signal法语大字体裁掉隐私通知高级设置文字，建议UITableViewCell无限行动态高度，stale关闭无完成证据。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 布局修复建议，陈旧关闭

**原文证据：**

位置 `1152:1206`：

> This makes it hard to understand what the option does.

<a id="row-383"></a>
## 383. privacy-issue-15096

**主题代码：** PRIVACY-A, PRIVACY-C, PRIVACY-F, PRIVACY-H, PRIVACY-I

**开放代码：** 按站点授权身份披露；扩展存在性指纹；隐私默认与生态迁移；选择性披露指纹风险

**逐条判断：** MetaMask原向所有站点暴露账户和web3，提出postMessage主动连接，兼容旧Dapp并沟通分阶段上线；细粒度默认可能跨站指纹另议，MTCS握手非本范围；最终connect screen已实现关闭。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 连接授权界面已实现

**原文证据：**

位置 `1344:1432`：

> A user's accounts should never be shown to a site without the user's deliberate consent.

位置 `19136:19171`：

> With our connect screen implemented

<a id="row-384"></a>
## 384. privacy-issue-4389

**主题代码：** PRIVACY-D, PRIVACY-F, PRIVACY-G, PRIVACY-I

**开放代码：** 保护收件人PII的多因素认证；开发环境安全默认

**逐条判断：** 加拿大通知服务保存姓名邮箱电话需2FA，现有email/SMS已强制，讨论硬件或TOTP更好，最终测试也默认email开启。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 现有2FA保持开启

**原文证据：**

位置 `2804:2841`：

> On by default with Email for testing.

<a id="row-385"></a>
## 385. privacy-issue-5394

**主题代码：** PRIVACY-D, PRIVACY-E, PRIVACY-F, PRIVACY-H, PRIVACY-I

**开放代码：** 删除状态与实际清除差异；保留业务记录匿名化；删除可恢复性争议

**逐条判断：** phpvms手改deleted状态留姓名邮箱，真正X按钮有PIREP则改身份凭证否则删；作者承认误解，恢复与去标识争论，单用户cron全删非核心实现。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 澄清现有删除入口，旧状态字段遗留

**原文证据：**

位置 `5141:5226`：

> difference between the option "state = deleted" and using the delete user "X" button.

<a id="row-386"></a>
## 386. privacy-issue-2411

**主题代码：** PRIVACY-B, PRIVACY-H

**开放代码：** 隐私声明链接失效；政策归属选择

**逐条判断：** VAC福利目录footer无响应，讨论链接加拿大数字服务还是VAC自有政策，拟Airtable配置，未见修复验证。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 选定候选政策与配置方案

**原文证据：**

位置 `832:854`：

> Currently does nothing

<a id="row-387"></a>
## 387. privacy-issue-14075

**主题代码：** PRIVACY-C, PRIVACY-H, PRIVACY-I

**开放代码：** 本地行为分析与供应商遥测区分；关闭设置覆盖不足；追踪用途透明度

**逐条判断：** ElasticSuite解释订单行为留本地而Smile ping称仅域名，关tracking仍ping；承诺2.6前台同意和ping移admin，后用户仍选择禁模块因性能，无全改确认。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 重构承诺，用户禁模块替代

**原文证据：**

位置 `2253:2322`：

> I've disabled Tracking as a test, but it still pings the smile domain

<a id="row-388"></a>
## 388. privacy-issue-18391

**主题代码：** PRIVACY-C, PRIVACY-I

**开放代码：** 继承分析端点；遥测默认开启争议；匿名性与开源论据局限

**逐条判断：** Radarr初指仍向Sonarr发Piwik，转自建分析；维护者称禁IP日志且开源，用户不接受隐藏advanced默认开启，最后建议手动关。无明确端点迁移验证。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 默认遥测争议未解决，提供退出

**原文证据：**

位置 `3178:3212`：

> I specifically disabled ip logging

位置 `2713:2766`：

> enabled by default and hidden under advanced settings

<a id="row-389"></a>
## 389. privacy-issue-1423

**主题代码：** PRIVACY-B, PRIVACY-I, PRIVACY-Z

**开放代码：** 隐私告知文本更新；实质证据不足

**逐条判断：** Rally仅Google文档和PR613链接，标题更新告知但缺具体文案变化，不从外链推内容或完成。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 链接到文案与PR，细节未知

**原文证据：**

位置 `65:94`：

> Update text on privacy notice

<a id="row-390"></a>
## 390. privacy-issue-14123

**主题代码：** PRIVACY-A, PRIVACY-H

**开放代码：** 主动政策确认；界面改造导致同意遗漏

**逐条判断：** TreeTracker原登录移除后checkbox无处放，引用不可预选及拒绝返回首页，末评仍需新用户详情加checkbox，关闭不证明已加。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 明确缺失待补

**原文证据：**

位置 `3228:3305`：

> still need the privacy policy checkbox added to the new user details fragment

<a id="row-391"></a>
## 391. privacy-issue-20480

**主题代码：** PRIVACY-A, PRIVACY-E

**开放代码：** Cookie保留期限最小化；默认隐私配置；必要性争议

**逐条判断：** EE session外含一年活动访问信息等persistent cookies不可调期限或同意门控，提默认session或全不设并精细配置及拒绝日志；无实现证据。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 默认最小化方案

**原文证据：**

位置 `1711:1785`：

> There is no mechanism in EE either to adjust the duration of these cookies

<a id="row-392"></a>
## 392. privacy-issue-3851

**主题代码：** PRIVACY-B, PRIVACY-D, PRIVACY-H, PRIVACY-I

**开放代码：** 遗忘工具操作文档

**逐条判断：** WSO2 EI需集中BPMN forget-me命令参数说明，回复已链admin guide；不由文档标题推实际删除覆盖。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 管理指南链接完成

**原文证据：**

位置 `1825:1851`：

> linked to the admin guide.

<a id="row-393"></a>
## 393. privacy-issue-12223

**主题代码：** PRIVACY-D, PRIVACY-F, PRIVACY-G, PRIVACY-I

**开放代码：** 测试环境敏感资料暴露；资源权限替代隐藏链接；开发数据真实性权衡

**逐条判断：** WCA staging可登录高权账户访问公开URL内部文档，链接源码已有故应改文档权限；forms改WCA登录并panel PR修复。pending ID claim公开dump是否净化因代表性争议未定。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 文档权限及panel修复，dump争议未解

**原文证据：**

位置 `6300:6387`：

> forms for nominations, promotions, demotions, etc. have been updated to require sign-in

<a id="row-394"></a>
## 394. privacy-issue-3719

**主题代码：** PRIVACY-B, PRIVACY-C, PRIVACY-I

**开放代码：** 第三方请求IP透明度；分享计数告知遗漏

**逐条判断：** Jetpack最初称只发URL但承认IP可进对方日志，法律讨论后政策helper明确官方按钮加载及非官方Facebook/Pinterest获IP与URL；未改默认请求，只filter可关。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 告知补充完成

**原文证据：**

位置 `5119:5174`：

> we've added the following section to the privacy helper

<a id="row-395"></a>
## 395. privacy-issue-8280

**主题代码：** PRIVACY-B, PRIVACY-C, PRIVACY-I, PRIVACY-Y

**开放代码：** 遥测计划撤回；政策与实际行为不一致；旧浏览器兼容权衡

**逐条判断：** Violentmonkey政策may GA引担忧，维护者澄清浏览器统计是计划后放弃改只支持新版，政策更新仍遗段引误会，称未使用GA；2025两个游戏脚本离题与Firefox同意机制后续不当新增追踪证据。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 撤回采集计划，政策曾漏改

**原文证据：**

位置 `4795:4839`：

> I will drop the plan to collect browser info

位置 `6307:6335`：

> Violentmonkey doesn't use GA

<a id="row-396"></a>
## 396. privacy-issue-1583

**主题代码：** PRIVACY-B, PRIVACY-C, PRIVACY-I

**开放代码：** 隐私标准与竞争治理协调；同意捆绑优势争议

**逐条判断：** UA Client Hints请求与CMA标识/privacy budget、安装升级告知对齐，担忧主导商捆绑同意竞争优势；维护者认为缺可执行提案关闭，后又求版本化规范与Sandbox关联。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 因不具体关闭，协调要求未解

**原文证据：**

位置 `3351:3413`：

> It's still not clear to me how to make this request actionable

<a id="row-397"></a>
## 397. privacy-issue-2588

**主题代码：** PRIVACY-B, PRIVACY-H, PRIVACY-I

**开放代码：** 法律文档版本维护；政策发布工作流

**逐条判断：** Screenshots初拟legal repo文档及自动拉取，Legal确认可维护副本，placeholder尚等最终版；最终改外链已有文档关闭，未落实原自动部署。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 改用既有文档外链

**原文证据：**

位置 `2638:2685`：

> we're off-linking to existing documentation now

<a id="row-398"></a>
## 398. privacy-issue-14096

**主题代码：** PRIVACY-D, PRIVACY-E, PRIVACY-I

**开放代码：** API个人数据最小化；输入规范化

**逐条判断：** Zonemaster主为全API参数格式默认必选规范，GDPR旁支明确弃user_ip/user_location_info并要求后端删除，主清单全勾不直接证明数据清理执行。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 规范清单完成，删除要求

**原文证据：**

位置 `2739:2797`：

> user_ip, location data type, user_location_info deprecated

<a id="row-399"></a>
## 399. privacy-issue-1797

**主题代码：** PRIVACY-Z

**开放代码：** 数据位置疑问；仅元数据可判

**逐条判断：** Azure Data Location仅标题与元数据，缺正文五评论，不能确定驻留地域或跨境问题。

**材料可用性：** metadata_only。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 证据不足

**原文证据：**

位置 `52:78`：

> Issue title: Data Location

<a id="row-400"></a>
## 400. privacy-issue-20523

**主题代码：** PRIVACY-A, PRIVACY-B, PRIVACY-H, PRIVACY-I

**开放代码：** 必要Cookie与插件追踪边界；告知与同意判断

**逐条判断：** pretix维护者声明默认购物车登录安全语言用途无追踪，排除tracking/campaign插件；认为无需banner但未来高级管理计划，法律观点有保留。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 解释默认用途，管理功能未做

**原文证据：**

位置 `2331:2418`：

> pretix (by default) does not use cookies for any kind of tracking or profiling purposes

<a id="row-401"></a>
## 401. privacy-issue-8744

**主题代码：** PRIVACY-A, PRIVACY-H

**开放代码：** 同意界面跨浏览器可用性

**逐条判断：** Safari Cookie按钮文字裁剪因间距，建议固定width改min/max-width，不涉及后端同意执行，无完成验证。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 布局方案提出

**原文证据：**

位置 `880:920`：

> Safari's cookie banner button is clipped

<a id="row-402"></a>
## 402. privacy-issue-8322

**主题代码：** PRIVACY-D, PRIVACY-F, PRIVACY-I

**开放代码：** 投票与身份声誉关联；匿名性机制边界

**逐条判断：** Joystream拟投票绑定membership以声誉一致，但增加隐私损失；回复可另购身份和隐私资金来源，真正匿名需ZK，均建议未实施。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 关联设计权衡，匿名升级提案

**原文证据：**

位置 `2135:2206`：

> we need to upgrade the voting mechanism with some Zero-Knowledge proofs

<a id="row-403"></a>
## 403. privacy-issue-14144

**主题代码：** PRIVACY-B, PRIVACY-D, PRIVACY-I

**开放代码：** 合规需求评估；哈希个人信息认知不确定；权利功能规划

**逐条判断：** Decidim问活动日志遗忘及个人信息查看，维护者对hash是否PII仅专家观点且求第二意见，等顾问报告后分任务并入3320，未给已合规结论。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 咨询后拆分需求迁移

**原文证据：**

位置 `2295:2332`：

> I would like a second opinion on this

<a id="row-404"></a>
## 404. privacy-issue-3862

**主题代码：** PRIVACY-A, PRIVACY-B, PRIVACY-C, PRIVACY-H, PRIVACY-I

**开放代码：** 默认遥测持续告知；显式记录偏好；匿名性合规主张

**逐条判断：** Gauge每次run提醒默认采集，on/off或env均记录选择止提示，讨论匿名豁免与查看上报数据日志，nightly确认可用；不是改默认opt-in。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 告知与偏好记录nightly实现

**原文证据：**

位置 `4725:4765`：

> Fix is available in nightly  >= 30-07-18

<a id="row-405"></a>
## 405. privacy-issue-9899

**主题代码：** PRIVACY-A, PRIVACY-B, PRIVACY-E, PRIVACY-H

**开放代码：** 同意记忆与账户清理耦合；保留期限与便利权衡

**逐条判断：** nopCommerce删guest丢已关闭banner状态，提保留接受者或单独cookie；指出规模和遮挡问题，最终不内建建议延长guest保留一个月，未改为专用同意存储。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 拒绝内建，建议延长保留

**原文证据：**

位置 `3893:3935`：

> decided not to implement it out of the box

<a id="row-406"></a>
## 406. privacy-issue-11502

**主题代码：** PRIVACY-B, PRIVACY-H, PRIVACY-I

**开放代码：** 地域隐私声明入口

**逐条判断：** WooCommerce Android设置及Play Store需加California Users政策链接，具体文案明确但零评论无实现证据。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 政策链接需求

**原文证据：**

位置 `1043:1078`：

> Privacy Notice for California Users

<a id="row-407"></a>
## 407. privacy-issue-15180

**主题代码：** PRIVACY-C, PRIVACY-D, PRIVACY-G, PRIVACY-H, PRIVACY-I, PRIVACY-Y

**开放代码：** 隐私扩展自身指纹；异常跨安全上下文泄露；防护机制固有限制

**逐条判断：** CanvasBlocker多PoC利用err.name无法访问和函数length识别扩展，旧ESR停支持、新异常修；Firefox59技术问题称清除但已知像素测试因伪造本质仍检测，阈值可被更大画布绕过。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 技术检测问题改进，固有检测残留

**原文证据：**

位置 `8225:8277`：

> The "known pixel value test 10" is quite hard to fix

位置 `10062:10110`：

> Finally got rid of the technical problems there.

<a id="row-408"></a>
## 408. privacy-issue-18854

**主题代码：** PRIVACY-C, PRIVACY-G, PRIVACY-H, PRIVACY-I

**开放代码：** DNS隐私与企业策略冲突；网络行为关闭可发现性

**逐条判断：** acme.sh强制DoH遭防火墙挡、引集中解析信任争议，dnssleep跳过DNS检查靠等待传播已用户验证，120/180/300并非固定值，help不明显。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 已有等待选项可关闭DoH检查

**原文证据：**

位置 `4546:4615`：

> Using `--dnssleep 120` is the way and only way to disable doh checks.

位置 `7816:7847`：

> the value is totally arbitrary.

<a id="row-409"></a>
## 409. privacy-issue-17354

**主题代码：** PRIVACY-B, PRIVACY-H

**开放代码：** 隐私告知视觉一致性

**逐条判断：** Hajk cookie notice反主题色，正文仅未抓图片，评论按976关闭；可判视觉缺陷和关联解决，不评图中实际对比。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 按关联任务关闭

**原文证据：**

位置 `1478:1496`：

> Closed as of #976.

<a id="row-410"></a>
## 410. privacy-issue-17750

**主题代码：** PRIVACY-E, PRIVACY-H, PRIVACY-I, PRIVACY-Z

**开放代码：** Cookie持久化并发用法；隐私关联较弱

**逐条判断：** youtube-dl手设cookie想下载结束前写jar供另进程，回复不应进程共享文件，非同意或个人信息议题。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 不推荐共享Cookie文件

**原文证据：**

位置 `2897:2977`：

> You should not share the same cookie file between different youtube-dl processes

<a id="row-411"></a>
## 411. privacy-issue-3998

**主题代码：** PRIVACY-B, PRIVACY-C, PRIVACY-E, PRIVACY-I

**开放代码：** 自定义存储不能覆盖中继保留；数据驻留控制缺失；PII保留阻碍采用

**逐条判断：** Bot自建State仍DirectLine Azure加密存转发，起初猜7天后明确24小时，其他channel称代理不存；无自控地点，用户视为阻碍想自建connector，feature规划关闭。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 解释24小时保留，配置能力未实现

**原文证据：**

位置 `4670:4711`：

> Data retention in Direct Line is 24 hours

<a id="row-412"></a>
## 412. privacy-issue-18941

**主题代码：** PRIVACY-F, PRIVACY-I, PRIVACY-Y

**开放代码：** 开发平台隐私信任；匿名参与障碍；迁移成本与社区连续性

**逐条判断：** Firejail用户以微软/AWS伦理隐私及Tor验证负担要求Codeberg/Notabug，广泛指控为发言者观点未验证；维护者称验证也普通网络出现且迁移扰社区，最终留Github锁讨论。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 拒绝平台迁移

**原文证据：**

位置 `16248:16292`：

> We'll stay on github until they kick us out!

<a id="row-413"></a>
## 413. privacy-issue-18935

**主题代码：** PRIVACY-E, PRIVACY-H

**开放代码：** 编辑内容默认持久化；本地存储可配置性

**逐条判断：** vue-trix默认保存输入localStorage出乎使用者意图，维护者从Electron便利解释转接受，提交支持optional；未说明最终默认值。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 可选存储已实现

**原文证据：**

位置 `2796:2862`：

> I already updated that allows localStorage as an optional setting.

<a id="row-414"></a>
## 414. privacy-issue-11675

**主题代码：** PRIVACY-C, PRIVACY-I

**开放代码：** 法规驱动上游数据访问变更；依赖获取适配

**逐条判断：** Maxmind CCPA改需账号token使旧GeoIP下载失败，ntopng换geoipupdate依赖及指南；这是数据获取兼容非自身追踪同意修复。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 更新依赖和文档

**原文证据：**

位置 `2694:2752`：

> ntopng-data package now brings `geoipupdate` as dependency

<a id="row-415"></a>
## 415. privacy-issue-20596

**主题代码：** PRIVACY-B, PRIVACY-H, PRIVACY-I

**开放代码：** 开发者Cookie用途文档；库与使用方数据责任

**逐条判断：** ActiveLogin BankId/GrandId state cookie存AuthenticationProperties，默认重定向但自定义bag可任意数据，需求是文档助开发者判断告知，不是强制弹窗；auth豁免是讨论观点。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 澄清文档范围，完成未知

**原文证据：**

位置 `5174:5223`：

> rather explain what our cookies do for developers

<a id="row-416"></a>
## 416. privacy-issue-18397

**主题代码：** PRIVACY-E, PRIVACY-I

**开放代码：** 用户可配置内容保留；历史价值与遗忘权衡；批量删除操作负担

**逐条判断：** Mastodon自动旧帖删以减少画像及存储，争论保留标记实例策略冷归档、1/min限速；2021作者指出16529已合并，不推出所有建议或远端删保证。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 自动删除方案已报告合并

**原文证据：**

位置 `13593:13663`：

> There seems to be a solution for auto deleting merged into main branch

<a id="row-417"></a>
## 417. privacy-issue-1874

**主题代码：** PRIVACY-B, PRIVACY-I

**开放代码：** 隐私政策发布入口

**逐条判断：** Anbox Cloud需建privacy/ToS并加入legal目录，正文仅文档链接及任务，无结果。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 页面构建需求

**原文证据：**

位置 `1065:1111`：

> add them to the /legal/terms-and-policies page

<a id="row-418"></a>
## 418. privacy-issue-5424

**主题代码：** PRIVACY-D, PRIVACY-E, PRIVACY-F, PRIVACY-G, PRIVACY-I

**开放代码：** 不可变审计与删除冲突；患者数据误录补救；伪名化前置流程；细粒度访问封存

**逐条判断：** elabFTW最初维护者误解员工姓名，作者澄清实验患者ID健康数据及误录，时间戳PDF/审计无法彻底擦；建议入库前伪名和删除映射、auditor-only锁定与访问理由，法律观点争议无实现。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 流程与封存方案讨论，无解决证据

**原文证据：**

位置 `4565:4617`：

> My concerns were not related to the user of elabFTW.

位置 `9053:9109`：

> Even a ID number is personally identifiable information.

<a id="row-419"></a>
## 419. privacy-issue-7326

**主题代码：** PRIVACY-B, PRIVACY-Z

**开放代码：** 安全说明沟通；仅元数据可判

**逐条判断：** VA call center安全措辞仅标题，缺五评论，不能因检索词认定数据泄露事件。

**材料可用性：** metadata_only。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 证据不足

**原文证据：**

位置 `65:112`：

> find verbiage for site security for call center

<a id="row-420"></a>
## 420. privacy-issue-20175

**主题代码：** PRIVACY-C, PRIVACY-D, PRIVACY-F, PRIVACY-G, PRIVACY-I

**开放代码：** 错误通知PII最小化；头像关联披露

**逐条判断：** Sentry7到8邮件出现应用用户头像，维护者建议组织Enhanced Privacy缩邮件，关于当前是否Gravatar明确未确认；未证实际移除。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 现有隐私设置建议，具体行为未核

**原文证据：**

位置 `1790:1839`：

> we recommend enabling the Enhanced Privacy option

位置 `2726:2745`：

> but didn't confirm.

<a id="row-421"></a>
## 421. privacy-issue-13985

**主题代码：** PRIVACY-C, PRIVACY-E, PRIVACY-I

**开放代码：** 功能遥测用途与最小化；匿名性与标识矛盾；主动同意争议；替代统计来源

**逐条判断：** qBittorrent拟系统/功能计数却曾提机器名ID，遭侵入性反对转UUID/无需ID；不收下载内容声明并不能证匿名，讨论opt-in问卷与服务器负担，最终不计划、已有Fosshub下载统计。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 遥测提案未采纳

**原文证据：**

位置 `15156:15187`：

> I'm closing this as not planned

位置 `15004:15072`：

> some telemetry is already available from downloads served by Fosshub

<a id="row-422"></a>
## 422. privacy-issue-20424

**主题代码：** PRIVACY-A, PRIVACY-H

**开放代码：** 同意横幅关闭故障；缓存插件兼容

**逐条判断：** WP Rocket与EU Cookie Law点击OK不消失，AutoBlock替代并非总有效需excluded scripts；2022在3.1.6/3.10.6测试正常。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 新版组合验证恢复

**原文证据：**

位置 `2206:2238`：

> the message goes away correctly.

<a id="row-423"></a>
## 423. privacy-issue-8726

**主题代码：** PRIVACY-H, PRIVACY-I

**开放代码：** 同意提示屏蔽；过滤与代替接受策略区别；跨平台防护限制

**逐条判断：** Brave切Prebake到Easylist已合并并发布，Android初仅网络规则、iOS缺cosmetic，桌面部分验证好；2022Google/YouTube仍难，维护者认为IDCAC更弱隐私而不采用，未保证全面挡或同意拒绝。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 列表方案上线，平台和站点缺口保留

**原文证据：**

位置 `7428:7482`：

> Switch from "Prebake Cookie" to "Easylist Cookie" list

位置 `13411:13468`：

> its less privacy-protecting than the filter list approach

<a id="row-424"></a>
## 424. privacy-issue-21583

**主题代码：** PRIVACY-B, PRIVACY-I

**开放代码：** 数据责任主体清晰度；法规名称修订

**逐条判断：** WhatDoTheyKnow隐私页拟准确说明mySociety是UKCOD慈善项目、结构注册链接及法规名称纠正；评论为文案建议无实施确认。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 文案修订提案

**原文证据：**

位置 `2213:2303`：

> WhatDoTheyKnow is run by mySociety, a project of the charity UK Citizens Online Democracy.

<a id="row-425"></a>
## 425. privacy-issue-2063

**主题代码：** PRIVACY-A, PRIVACY-B, PRIVACY-C, PRIVACY-I

**开放代码：** 退出遥测事件边界；收集审查；用户关联事件

**逐条判断：** FirefoxReality拟hello/goodbye ping统计关闭率，团队指出退出后发送问题；event可按用户分组，审批称无新增标识不等于无标识。数据审查批准后半年复核允许合并，未见发布证明。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 审查批准可合并

**原文证据：**

位置 `6843:6857`：

> Ping approved.

位置 `4754:4780`：

> we can group pings by user

<a id="row-426"></a>
## 426. privacy-issue-1339

**主题代码：** PRIVACY-B, PRIVACY-H, PRIVACY-Z

**开放代码：** 隐私告知交互；实质证据不足

**逐条判断：** Rally隐私notice/contribution modal只有父任务和文案链接，未提供文案内容或实现。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 请求，完成不明

**原文证据：**

位置 `65:109`：

> Create the Privacy notice/contribution modal

<a id="row-427"></a>
## 427. privacy-issue-3773

**主题代码：** PRIVACY-B, PRIVACY-C, PRIVACY-I

**开放代码：** 解析服务商信任；最小收集与共享对象权衡；政策解释不确定

**逐条判断：** Bromite建议Mozilla Cloudflare DoH端点减少记录；维护者认为控制者处理者关系增加Mozilla可访问性而拒绝。此为政策解读并非已验证数据实际共享。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 因感知共享风险拒绝

**原文证据：**

位置 `3214:3281`：

> we do not need to share the data with two companies instead of one.

<a id="row-428"></a>
## 428. privacy-issue-17190

**主题代码：** PRIVACY-C, PRIVACY-I

**开放代码：** 分析数据最小化；地域排除局限；会话回放隐私

**逐条判断：** Stampy从回放搜索日志AB点击讨论到server-side API；排除EU难且VPN影响，公民海外适用说法仅属参与者观点。未来小样本回放及告知待定。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 确定架构，实施未证实

**原文证据：**

位置 `3391:3417`：

> settled on server-side API

<a id="row-429"></a>
## 429. privacy-issue-2420

**主题代码：** PRIVACY-B, PRIVACY-H, PRIVACY-Z

**开放代码：** 隐私告知入口；实质证据不足

**逐条判断：** Canonical请求加入contact us and enquiries隐私notice链接，仅标题和外链可见。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 请求，完成不明

**原文证据：**

位置 `70:109`：

> Privacy notice contact us and enquiries

<a id="row-430"></a>
## 430. privacy-issue-5472

**主题代码：** PRIVACY-A, PRIVACY-C, PRIVACY-I

**开放代码：** 默认遥测同意；退出后的收集；非公开合规调查

**逐条判断：** Flutter用户要求默认关闭及不发送退出事件，容器重建反复退出；争论CLI告知覆盖和ePrivacy。维护者调查并以敏感性关闭公开讨论，无修复证据。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 关闭议题，调查结果未公开

**原文证据：**

位置 `8581:8601`：

> we are investigating

位置 `9407:9485`：

> Due to the sensitive nature of this topic, I'm going to close this bug for now

<a id="row-431"></a>
## 431. privacy-issue-2276

**主题代码：** PRIVACY-B, PRIVACY-H

**开放代码：** 隐私告知范围；导航文案澄清

**逐条判断：** Canonical拟改导航为Data protection enquiries，并说明调查数据按privacy notice和policy处理，无完成证明。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 文案请求

**原文证据：**

位置 `941:1054`：

> Data collected from this survey will be handled in accordance with Canonical's privacy notice and privacy policy.

<a id="row-432"></a>
## 432. privacy-issue-20168

**主题代码：** PRIVACY-C, PRIVACY-D, PRIVACY-G

**开放代码：** 遥测凭证泄露；诊断次生泄露；发送前过滤

**逐条判断：** AppInsightsJS Angular OIDC URL携带id/access token，用户确认initializer清理主路径，但URL_LONG警告还含原URL。建议同一initializer禁用警告，未确认解决。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 主路径修复确认，诊断路径仅建议

**原文证据：**

位置 `2024:2084`：

> Managed to check the url path and censor as per the example.

位置 `3613:3706`：

> You can use telemetry initializer to disable this particular or all warnings from being sent.

<a id="row-433"></a>
## 433. privacy-issue-1484

**主题代码：** PRIVACY-A, PRIVACY-B, PRIVACY-C, PRIVACY-H, PRIVACY-Y

**开放代码：** 隐私控制区分；故障报告撤回

**逐条判断：** Brave欢迎页退出诊断初报无效，作者后澄清把usageping误认P3A，P3A和crash正确禁用，usageping常开符合预期。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 作者撤回故障认定

**原文证据：**

位置 `4482:4609`：

> Both `Allow privacy-preserving product analytics (P3A)` & `Automatically send diagnostic reports` are correctly being disabled.

<a id="row-434"></a>
## 434. privacy-issue-7595

**主题代码：** PRIVACY-C, PRIVACY-Y

**开放代码：** 分析注入误归因；文档与运行依赖边界

**逐条判断：** Buefy被指库注入GA，维护者解释devDependencies仅文档，作者承认检查器实际打开文档而非自己的项目。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 作者承认误报

**原文证据：**

位置 `2501:2579`：

> I somehow had my inspector open on the Buefy doc site instead of _my_ project.

<a id="row-435"></a>
## 435. privacy-issue-8872

**主题代码：** PRIVACY-A, PRIVACY-B, PRIVACY-H, PRIVACY-I

**开放代码：** 撤回同意入口可发现性；未登录持续访问；跨站集成缺口

**逐条判断：** Eclipse已上线有toolbar链接则隐藏badge否则保留机制；OpenVSX禁用bar后讨论页脚或菜单撤回，草稿第二handler失败。最终仍要求启用GA前提供撤回，未证OpenVSX修复。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 关联站修复，本议题最终落地未证实

**原文证据：**

位置 `4412:4460`：

> Yes, users should be able to revoke at any time.

位置 `10192:10302`：

> We need to allow users to revoke our cookie consent banner before we can enable Google Analytics for the site.

<a id="row-436"></a>
## 436. privacy-issue-20377

**主题代码：** PRIVACY-A, PRIVACY-B, PRIVACY-H, PRIVACY-I

**开放代码：** 同意前阻止加载；撤回同意；核心功能责任边界

**逐条判断：** Joomla用户要求核心提供脚本字体cookie事前同意、用途时长说明及撤回，所有cookie均需同意等法律说法为作者主张。维护者仅称不适合GitHub，未实施。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 渠道性关闭

**原文证据：**

位置 `2548:2579`：

> This is not an issue for github

<a id="row-437"></a>
## 437. privacy-issue-14030

**主题代码：** PRIVACY-D, PRIVACY-F, PRIVACY-G, PRIVACY-I

**开放代码：** 联合账户绑定验证；越权读取风险

**逐条判断：** WSO2无需证明外部账户控制权即绑定，提出攻击者预绑定后读取受害者输入私密资料的情景；禁用该方向绑定是临时方案，完整修复转3829。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 临时禁用方案，完整解法另议

**原文证据：**

位置 `1209:1308`：

> A user should be required to prove that they have access to both accounts before they can be linked

<a id="row-438"></a>
## 438. privacy-issue-3146

**主题代码：** PRIVACY-A, PRIVACY-B, PRIVACY-C, PRIVACY-D, PRIVACY-I

**开放代码：** 隐私查询规则；退出用户过滤；删除所需数据血缘

**逐条判断：** SQLFluff插件需求包括使用去敏视图、排除退出邮件、保留user_id便于后续删除ML数据，与一般SQL风格规则并列；已有custom rules beta，插件层未进0.4.0。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 部分能力已提供，插件扩展待推进

**原文证据：**

位置 `7283:7341`：

> Maintaining this "lineage" / backtracking info is critical

<a id="row-439"></a>
## 439. privacy-issue-4842

**主题代码：** PRIVACY-D, PRIVACY-F, PRIVACY-G, PRIVACY-I

**开放代码：** 匿名数据再识别；测试数据随机化

**逐条判断：** EvaP生产访问者可由答案分布识别匿名副本中少于两人未公开课程，要求随机答案计数且不超过投票人数。比较顺序偏置与归一化误差两方案，未见最终实施。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 方案设计

**原文证据：**

位置 `1574:1629`：

> answer counters should be set randomly on anonymization

<a id="row-440"></a>
## 440. privacy-issue-3942

**主题代码：** PRIVACY-B, PRIVACY-D, PRIVACY-H

**开放代码：** 日志部分脱敏；告知与实现一致性；提交界面可理解性

**逐条判断：** Signal桌面日志留三位号码而Android wiki称两位；维护者说三位为设计并更新wiki，未改脱敏量。作者另担心公开日志去向和编辑时机不清。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 文档纠正，三位保留

**原文证据：**

位置 `4694:4723`：

> The three digits is by design

位置 `5688:5722`：

> I have updated the mentioned wiki.

<a id="row-441"></a>
## 441. privacy-issue-13934

**主题代码：** PRIVACY-D, PRIVACY-E, PRIVACY-F, PRIVACY-I

**开放代码：** 批量消息删除；遮蔽与物理删除边界

**逐条判断：** Element请求按用户批量redact应对spam及GDPR，评论提醒内容仍在数据库；2023规范提案已落地，应用跟踪转meta920，不证明底层数据已清除。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 规范落地并转跟踪

**原文证据：**

位置 `1334:1396`：

> b-b-but event content still stays in database after redaction.

<a id="row-442"></a>
## 442. privacy-issue-133

**主题代码：** PRIVACY-A, PRIVACY-H

**开放代码：** 同意偏好持久化故障

**逐条判断：** Modrinth iOS每页重复提示，登录与否及逐项review均如此，作者确认重设计已修复；视频外链未读取。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 重设计修复确认

**原文证据：**

位置 `1692:1727`：

> This has been fixed in the redesign

<a id="row-443"></a>
## 443. privacy-issue-12723

**主题代码：** PRIVACY-A, PRIVACY-H

**开放代码：** 浏览器隐私设置兼容；临时与持久cookie区分

**逐条判断：** Sails IE禁止持久cookie而允许session时不断换session导致CSRF；解释应用session≠浏览器临时cookie，用户提供探测cookie后按请求设expires=false并确认可用，避免正常用户购物车丢失。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 用户侧兼容方案验证

**原文证据：**

位置 `12079:12123`：

> Ok so I have the following which works great

<a id="row-444"></a>
## 444. privacy-issue-14176

**主题代码：** PRIVACY-E, PRIVACY-F, PRIVACY-I

**开放代码：** 组织成员删除；删除依赖与孤立资源

**逐条判断：** NuGet要求解除组织成员删除限制，移除成员并提示最后成员导致组织孤立，连带unlist包；另问组织email删除，无正文实施确认。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 任务列明，完成未证

**原文证据：**

位置 `1002:1060`：

> Organizations that would be orphaned should be highlighted

<a id="row-445"></a>
## 445. privacy-issue-11968

**主题代码：** PRIVACY-F, PRIVACY-G, PRIVACY-H, PRIVACY-I

**开放代码：** 角色可见性限制；界面隐藏与授权边界

**逐条判断：** Telework员工仅直接表单、reviewer仅assigned tasks，讨论隐藏tabs后登录仍跳/form的缺口；最终生产验证working，但不能据此证明后端授权强度。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 生产界面流程验证

**原文证据：**

位置 `6002:6026`：

> Tested in PROD, working.

<a id="row-446"></a>
## 446. privacy-issue-8370

**主题代码：** PRIVACY-I

**开放代码：** 法规导致功能限制；第三方服务依赖

**逐条判断：** Instagram链接消息403，参与者归因为EU ePrivacy下平台限制并给text broadcast替代；后续至2023仍求解，无成功确认。未见本库隐私泄露证据。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 替代建议未验证

**原文证据：**

位置 `4983:5045`：

> Facebook has disabled some functionality such as sending links

<a id="row-447"></a>
## 447. privacy-issue-9628

**主题代码：** PRIVACY-A, PRIVACY-B, PRIVACY-E, PRIVACY-H, PRIVACY-I

**开放代码：** 可选cookie事前同意；可撤回偏好；实例化告知与控制

**逐条判断：** OFN从无告知采集到实例开关、默认禁用可选cookie、GA/Matomo选择及动态policy，后续补Matomo optout/字体/banner/文档；最终明确done working，非仅关闭。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 功能完成运行确认

**原文证据：**

位置 `12128:12179`：

> This is done and working without any reported issue

<a id="row-448"></a>
## 448. privacy-issue-3651

**主题代码：** PRIVACY-B, PRIVACY-F, PRIVACY-I, PRIVACY-Z

**开放代码：** 共享授权匹配；合规控制映射

**逐条判断：** CoreOS AC21引用组织对共享伙伴授权与信息限制匹配及决策辅助，PII只是受限信息示例；评论仅链接控制文档，不能推断系统已实施。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 标准映射，实施证据有限

**原文证据：**

位置 `957:1017`：

> Facilitates information sharing by enabling authorized users

<a id="row-449"></a>
## 449. privacy-issue-8064

**主题代码：** PRIVACY-F, PRIVACY-G, PRIVACY-I

**开放代码：** 并发标识冲突导致跨客数据暴露；复现证据与隐私冲突

**逐条判断：** PrestaShop MAX+1并发发票重号导致查看他人发票的报告，维护者未复现按模块问题关闭，多商户继续确认；作者不能分享客户录屏，2023给sleep复现及序列本地修补，2024仍报告。部分重号病例明确客户数据正常，不能全等同泄露。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 核心未确认修复，本地补丁报告

**原文证据：**

位置 `10986:11036`：

> I cannot share customer data in a screenrecording.

位置 `16429:16468`：

> We patched our prestashop by overriding

<a id="row-450"></a>
## 450. privacy-issue-8812

**主题代码：** PRIVACY-A, PRIVACY-B, PRIVACY-H, PRIVACY-I

**开放代码：** 同意界面渐进增强；必要cookie边界

**逐条判断：** GOVUK示例在JS下隐藏已同意banner、无JS重载，增加仅必要cookie客户端服务器端示例；任务复选明确完成。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 示例与反馈完成

**原文证据：**

位置 `1519:1561`：

> We've iterated/added the examples as above

<a id="row-451"></a>
## 451. privacy-issue-11528

**主题代码：** PRIVACY-G, PRIVACY-I

**开放代码：** 事件日志静态加密；默认无加密

**逐条判断：** COS计划升级lagom-pb支持journal加密并可配置encryptor，默认NoEncryption，称为合规准备而非已经完整合规。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 配置能力请求

**原文证据：**

位置 `1283:1312`：

> but default to `NoEncryption`

<a id="row-452"></a>
## 452. privacy-issue-5498

**主题代码：** PRIVACY-B, PRIVACY-F, PRIVACY-I

**开放代码：** 公开记录搜索去索引；隐私与公共透明权衡；自动抑制过宽风险

**逐条判断：** CourtListener长讨论明确保留本站/API研究访问，仅限制Google等索引；争论非先例价值、同名误伤、弱势群体、关键词误抑制及人工负担。收窄为近30年指定法院和主题，2021报告约40万去索引，跳过破产并加亲子/不当解雇，最终确认持续处理已修复；数字为参与者报告，贴出代码仅筛blocked=True不可独立验证实际规模。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 批量执行及持续机制完成报告

**原文证据：**

位置 `4770:4794`：

> Nothing's being deleted.

位置 `41746:41788`：

> I skipped doing the bankruptcy court case.

位置 `49487:49516`：

> it's finally fixed as of now.

<a id="row-453"></a>
## 453. privacy-issue-18464

**主题代码：** PRIVACY-E, PRIVACY-F, PRIVACY-I

**开放代码：** 隐藏内容搜索残留；搜索与正文访问边界

**逐条判断：** WP Job Manager隐藏已满/过期职位仍在原生搜索出现，点入过期页不显示正文；Google索引为疑问，末尾核心搜索待办未勾而sitemap已勾。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 部分任务完成，核心过滤未证实

**原文证据：**

位置 `3674:3715`：

> Filter out expired posts in core's search

<a id="row-454"></a>
## 454. privacy-issue-14066

**主题代码：** PRIVACY-C, PRIVACY-I

**开放代码：** 匿名分析需求；联系用户与匿名性张力

**逐条判断：** Aragon拟完全匿名不可追踪metrics，讨论Tor、Matomo、optin及后续活跃用户邮箱、地区、org URL指标，最终明确降低优先级关单，未证明添加分析。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 计划暂缓

**原文证据：**

位置 `5490:5525`：

> its current effort is deprioritized

<a id="row-455"></a>
## 455. privacy-issue-162

**主题代码：** PRIVACY-A, PRIVACY-B, PRIVACY-H, PRIVACY-I

**开放代码：** 跨子域同意共享；偏好管理入口迁移

**逐条判断：** Tgrade将管理按钮集中policy页，澄清首次到任意子域应提示，随后其他子域不重复，最终双方确认共享行为可用。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 用户验证通过

**原文证据：**

位置 `3210:3246`：

> Ah yes, it worked for me now as well

<a id="row-456"></a>
## 456. privacy-issue-11539

**主题代码：** PRIVACY-A, PRIVACY-C, PRIVACY-H, PRIVACY-I

**开放代码：** 广告同意信号传递；法规信号类型区分

**逐条判断：** PubMatic AMP广告需传GDPR/CCPA字符串，现缺type元数据，建议按长度区分为临时实践，正式type另有请求；感谢后关闭，非实施验证。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 接口咨询答复

**原文证据：**

位置 `2093:2153`：

> people determine the consent string type based on the length

<a id="row-457"></a>
## 457. privacy-issue-18564

**主题代码：** PRIVACY-B, PRIVACY-F, PRIVACY-G, PRIVACY-H

**开放代码：** 敏感权限用途说明；构建配置缺失

**逐条判断：** Cordova iOS10联系人访问因缺NSContactsUsageDescription崩溃，请求构建自动生成并CLI输入用途；可手填但未见自动化修复。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 手动配置可行，生成需求未证实

**原文证据：**

位置 `2633:2674`：

> I can set the value for the key manually.

<a id="row-458"></a>
## 458. privacy-issue-1811

**主题代码：** PRIVACY-A, PRIVACY-B, PRIVACY-H, PRIVACY-I

**开放代码：** 首层隐私告知入口

**逐条判断：** Klaro DPO要求cookie notice有policy链接，现配置仅modal有，后续仍求notice注入办法，无解决确认。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 未证实解决

**原文证据：**

位置 `1544:1655`：

> this parameter sets the privacy policy url for the modal window but we need a link to the policy in the notice.

<a id="row-459"></a>
## 459. privacy-issue-9335

**主题代码：** PRIVACY-A, PRIVACY-B, PRIVACY-H

**开放代码：** 地域提示适用范围；同意提示消失与关闭故障

**逐条判断：** NuGet博客banner在不适用locale出现、不能关闭却导航后消失；移到Gallery7082，不是修复证据。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 转移责任仓库

**原文证据：**

位置 `1588:1602`：

> Issue moved to

<a id="row-460"></a>
## 460. privacy-issue-3902

**主题代码：** PRIVACY-D, PRIVACY-E, PRIVACY-I

**开放代码：** 目的结束后数据最小化；关联标识再识别；归档保留期限；审计历史清除

**逐条判断：** DCAF患者结束服务后删电话姓名等但保留报告与重复服务关联；指出公开电话加公开算法可逆推身份，讨论secret salt、年龄分段、字段组合复核和清除audit日志。期限从120天到已履约30天/未履约约120天讨论，最终仅计划推进，未证部署匿名化。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 设计推进，最终实现未证

**原文证据：**

位置 `8435:8523`：

> If a person knew someone's phone number they could apply the archive ID-scramble process

位置 `10921:11009`：

> We definitely need a second pass to see if our combination of data becomes identifiable.

<a id="row-461"></a>
## 461. privacy-issue-8306

**主题代码：** PRIVACY-C, PRIVACY-I, PRIVACY-Y

**开放代码：** 第三方SDK去依赖；依赖存在与传输事实区分；项目责任争议

**逐条判断：** Fenix要求移除Google服务及附带trackers，历史传Google说法被反驳，静态类名不证明实际传输；讨论F-Droid精简build转12809，未见移除落实。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 范围争议与转向，未证修复

**原文证据：**

位置 `1716:1777`：

> Mozilla is not sending your browsing history to third parties

<a id="row-462"></a>
## 462. privacy-issue-14339

**主题代码：** PRIVACY-F, PRIVACY-I

**开放代码：** 身份与业务数据分离；框架合规责任边界；密码哈希职责

**逐条判断：** MongoAuth额外字段API先讨论冲突检查和密码必须由provider管理，后维护者以GDPR责任拒绝，申请者反驳框架应让应用决定；法律强制分离说法未独立验证。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 基于责任考量拒绝

**原文证据：**

位置 `5915:5968`：

> adding extra info to the user should be kept external

<a id="row-463"></a>
## 463. privacy-issue-3181

**主题代码：** PRIVACY-D

**开放代码：** 演示数据假名化；仅元数据证据

**逐条判断：** 仅标题可知demo mode拟假名化机构名称，无正文评论可评估范围或效果。

**材料可用性：** metadata_only。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 仅标题，结果未知

**原文证据：**

位置 `65:106`：

> Pseudonymize institute names in demo mode

<a id="row-464"></a>
## 464. privacy-issue-18769

**主题代码：** PRIVACY-B, PRIVACY-C, PRIVACY-H

**开放代码：** 外部字体泄露IP；本地资源托管；退出遥测后的外部请求

**逐条判断：** NocoDB拟字体放asset避免对Google暴露IP；后报NC_DISABLE_TELE仍有gstatic和Googleform请求，维护者追查；末称v0.104.0修复，但未逐项说明副问题。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 版本修复声明，子问题范围有限

**原文证据：**

位置 `3154:3176`：

> Fixed in ``v0.104.0``.

<a id="row-465"></a>
## 465. privacy-issue-8381

**主题代码：** PRIVACY-A, PRIVACY-C, PRIVACY-H, PRIVACY-I

**开放代码：** 广告同意信号落实；非个性化广告控制

**逐条判断：** ReactNative AdMob先建议consent库，评论指出只收集同意不能传入ad request，需personalized prop/npa=1；最终0.3.0已加。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 版本加入控制

**原文证据：**

位置 `3784:3812`：

> this is added for **v0.3.0**

<a id="row-466"></a>
## 466. privacy-issue-1965

**主题代码：** PRIVACY-B, PRIVACY-F, PRIVACY-G, PRIVACY-H, PRIVACY-I

**开放代码：** 权限告知与实际用途差异；权限最小化平台限制

**逐条判断：** CanvasBlocker请求修改隐私设置权限引疑，维护者说明仅读取resistFingerprinting显示notice、核心非必需但不能optional，不写设置；duplicate关闭。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 用途解释，权限未减少

**原文证据：**

位置 `1649:1707`：

> CB only reads that and does not write any privacy settings

<a id="row-467"></a>
## 467. privacy-issue-3790

**主题代码：** PRIVACY-B, PRIVACY-C, PRIVACY-G, PRIVACY-I, PRIVACY-Y

**开放代码：** 依赖SDK自动外传；静态与动态证据差异；医疗应用使用元数据

**逐条判断：** Quirk初静态11tracker签名明确不等于活跃，维护者称未调用；作者随后网络观察启动请求crashlytics/FB/Expo。维护者解释更新和crash服务、否认配置FB但未移除，称policy涵盖且不上传治疗thoughts；不可写成完全无追踪。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 外联报告保留，未修除依赖

**原文证据：**

位置 `3153:3227`：

> those trackers aren't just included by the framework, they are also active

<a id="row-468"></a>
## 468. privacy-issue-9441

**主题代码：** PRIVACY-A, PRIVACY-B, PRIVACY-H, PRIVACY-I

**开放代码：** 同意状态跨系统一致性；告知与同意状态区分；地域统一提示

**逐条判断：** BBC独立banner复用Orbit cookie协议，privacy表示已见而explicit需选择、policy111/000；已有policy不覆盖，全球提示获确认。POC不主动清除personalisation cookie依赖转Orbit，done后仍问期限。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 调查POC完成，清除和期限边界保留

**原文证据：**

位置 `3836:3888`：

> BUT if `ckns_policy` is already set, dont update it.

<a id="row-469"></a>
## 469. privacy-issue-2998

**主题代码：** PRIVACY-A, PRIVACY-B, PRIVACY-C, PRIVACY-D, PRIVACY-I

**开放代码：** 遥测目的与字段约束；发送前个人信息清理；用户同意与收集实现分离

**逐条判断：** odo拟用Segment/Woopra收命令OS版本错误并要求不含PII、可退出。先PR仅同意选项被重开，2021确认核心metrics完成，Route/Ingress字段未做另议；清理要求不等于逐字段已验证。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 核心指标实现，扩展字段延期

**原文证据：**

位置 `7816:7853`：

> We have all core metrics implemented.

位置 `6327:6387`：

> the PR only added a preference option to track users consent

<a id="row-470"></a>
## 470. privacy-issue-18795

**主题代码：** PRIVACY-C, PRIVACY-H, PRIVACY-I

**开放代码：** 本地资源托管；离线与隐私共同需求

**逐条判断：** A-frame离线字体/控制器模型加载慢，建议本地font URL和改build模型路径，用户确认本地改动有效；另以避免IP第三方泄露支持自包含，末称5118修复未读取PR内容。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 关联PR修复声明

**原文证据：**

位置 `3674:3727`：

> Fixed by https://github.com/aframevr/aframe/pull/5118

<a id="row-471"></a>
## 471. privacy-issue-2874

**主题代码：** PRIVACY-C, PRIVACY-D

**开放代码：** 位置统计粒度最小化；默认采集配置；不存IP导致历史不可回填

**逐条判断：** GoatCounter国家到州省需求，拒绝城市精度；地区已加入默认开启可关闭，旧数据因不存IP不可补。后提大国默认名单可自定义，最后2.0 geodb解决配置。不能把早期仅大国设想当已实现地域限制。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 地区功能完成，精细默认策略讨论

**原文证据：**

位置 `3406:3440`：

> and the IP address is never stored

位置 `5234:5257`：

> it's enabled by default

<a id="row-472"></a>
## 472. privacy-issue-14063

**主题代码：** PRIVACY-B, PRIVACY-C, PRIVACY-G, PRIVACY-I

**开放代码：** 传输加密升级；上游安全依赖；支持与配置生效边界

**逐条判断：** Nginx99评论围绕TLS1.3/OpenSSL1.1.1，合规压力与稳定发行安全维护权衡，拒非stable/backports，Alpine3.9后确认支持且需显式配置。default ssl_protocols覆盖vhost导致失败，SSLlabs不支持SNI说法被纠正；后仍Debian及旧Alpine咨询，不是所有环境修好。TLS1.2绝对不安全和GDPR必须1.3均仅参与者说法。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** Alpine支持确认，配置与发行版差异保留

**原文证据：**

位置 `54123:54175`：

> Please note that `TLSv1.3` is not enabled by default

位置 `60710:60764`：

> The default ssl_protocols overrides all virtual hosts.

<a id="row-473"></a>
## 473. privacy-issue-8188

**主题代码：** PRIVACY-F, PRIVACY-G, PRIVACY-H

**开放代码：** 运动传感器访问控制；站点权限粒度

**逐条判断：** Fenix要求全局和逐站点控制orientation/motion，倾向optin但涉及spec；最终移Bugzilla未证实现。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 迁移跟踪

**原文证据：**

位置 `1978:2056`：

> I'd expect both a way to control this for all sites and to control it per-site

<a id="row-474"></a>
## 474. privacy-issue-1836

**主题代码：** PRIVACY-C, PRIVACY-G, PRIVACY-I

**开放代码：** 传输保护与端点信任边界；搜索历史最小化

**逐条判断：** Searx请求PFS防恶意实例日志，答复明确PFS不阻止服务器读/记录查询、由reverse proxy配置；POST避URL但HTML title仍历史泄露simple主题已解。请求者想元搜索不可知query，最终解释架构需知道，非实现E2E。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 威胁模型澄清，未实现端点盲化

**原文证据：**

位置 `2540:2607`：

> Forward secrecy doesn't prevent Search Encrypt to log all requests.

<a id="row-475"></a>
## 475. privacy-issue-20560

**主题代码：** PRIVACY-A, PRIVACY-B, PRIVACY-H, PRIVACY-I

**开放代码：** 告知横幅升级为选择控制；同意驱动脚本加载

**逐条判断：** Pimcore移除Info Bar后用户要多类optin接Tag Snippet条件和twig，维护者认为应做bundle；未见replacement实现。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 扩展包建议

**原文证据：**

位置 `2582:2634`：

> That's a perfect use-case for a bundle in my opinion

<a id="row-476"></a>
## 476. privacy-issue-20481

**主题代码：** PRIVACY-B, PRIVACY-I

**开放代码：** cookie用途与保留期告知；必要性声明；跨境处理说明

**逐条判断：** Cloudflare正文文档列负载均衡、bot、缓存、等待室、限流、challenge cookies的期限用途，说明US处理、客户披露、加密bot信息及不跨站追踪声明；无评论验证，不能当独立审计结论。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 文档内容提供，发布未证

**原文证据：**

位置 `1324:1342`：

> Cloudflare Cookies

<a id="row-477"></a>
## 477. privacy-issue-2208

**主题代码：** PRIVACY-A, PRIVACY-B, PRIVACY-H, PRIVACY-I

**开放代码：** 订阅同意与告知简化；设计阶段证据

**逐条判断：** Canonical newsletter footer设计从checkbox/privacy notice到建议去掉并单字段，006方案获选ready to build；图像未取，文字能证设计选择不能证明线上删除告知。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 设计获批待构建

**原文证据：**

位置 `3599:3668`：

> We can probably get away with no check-box and privacy notice message

<a id="row-478"></a>
## 478. privacy-issue-7646

**主题代码：** PRIVACY-A, PRIVACY-B, PRIVACY-C, PRIVACY-I

**开放代码：** 默认遥测与显式同意争议；安装前告知；匿名化与接收方可识别性；下游部署退出可达性

**逐条判断：** Netdata用户举报kickstart无事前告知传GA，维护者坚持默认开只加提示并拒optin。争论开发者不可见IP≠Google未接收及匿名选项可信度，双方法律伦理断言均为观点。改进清单更新至2月示脚本/docs/website已勾，binary未勾；docker/k8s退出建议ENV/文件/helm，未见全部确认，不能写为全渠道修复。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 告知与选项部分完成，默认同意策略未改

**原文证据：**

位置 `3991:4045`：

> We do not intend however to change telemetry to opt-in

位置 `7920:7961`：

> binary packages (not sure about this one)

<a id="row-479"></a>
## 479. privacy-issue-14015

**主题代码：** PRIVACY-E, PRIVACY-F, PRIVACY-H, PRIVACY-I

**开放代码：** 数据导出与可携性；导出可用性；加密会话明文副本风险；本地保存与删除权张力

**逐条判断：** Element118可取评论逐读（历史元数据208并非同一快照），多年需求包含按房间时间格式导出、备份搜索迁移，脚本难用/加密旧史缺失。2021develop导出用户验证，下一版计划仅web/desktop无Android或持续日志；2023讨论防导出不可强制与可选加密警告应分开，后者未实现证据。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** Web导出验证，持续日志与加密导出另议

**原文证据：**

位置 `58736:58783`：

> just exported using https://develop.element.io/

位置 `64280:64338`：

> I'm asking for an encryption option and an advice to do so

<a id="row-480"></a>
## 480. privacy-issue-14262

**主题代码：** PRIVACY-B, PRIVACY-F, PRIVACY-H, PRIVACY-I

**开放代码：** 跨租户用户数据隔离；用户自主角色加入；处理告知与重复同意权衡

**逐条判断：** OJS多期刊无author角色无法投稿，从自动加默认角色改为表单角色选择/说明；隐私讨论强调同域未必同主体、管理员代注册与本人行动不同、其他作者同意，发现投稿页已有policy。四场景方案纳3575合并，不能将早期自动加入写最终。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 角色流程修复合并

**原文证据：**

位置 `28218:28267`：

> This issue was address in a PR merged with #3575.

<a id="row-481"></a>
## 481. privacy-issue-4654

**主题代码：** PRIVACY-D, PRIVACY-G

**开放代码：** 图像人脸车牌去标识；共享数据保护

**逐条判断：** Autoware提读取bag、模糊image topics重写保留其他topics，待办未勾；建议独立仓库并转org discussion，无效果或实现证明。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 方案转独立工具讨论

**原文证据：**

位置 `2101:2172`：

> It's better to create this kind of tool in its own separate repository.

<a id="row-482"></a>
## 482. privacy-issue-11602

**主题代码：** PRIVACY-C, PRIVACY-I

**开放代码：** 地理IP数据使用责任；拒绝出售请求传递；法规与依赖迁移权衡

**逐条判断：** ETLegacy历史迁移评论涉及GeoIP旧库停更、GeoLite2需账户以接收DoNotSell通知，主服务器查询并不被认为解除责任，弃功能只是建议；最终因有Legacy转换脚本而拒格式升级，不能写已删除geo功能。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 拒绝格式迁移，保留转换路径

**原文证据：**

位置 `8852:8886`：

> Moving to GeoLite2 isn't worth it.

<a id="row-483"></a>
## 483. privacy-issue-5019

**主题代码：** PRIVACY-B, PRIVACY-D, PRIVACY-H, PRIVACY-I

**开放代码：** 隐私工具文档可访问性

**逐条判断：** WSO2身份匿名化扩展文档链接不可用，评论给新链接并明确Fixed；只证文档修复，不证匿名工具算法。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 文档链接修复

**原文证据：**

位置 `1567:1576`：

> Fixed [1]

<a id="row-484"></a>
## 484. privacy-issue-1016

**主题代码：** PRIVACY-B, PRIVACY-C, PRIVACY-D, PRIVACY-E, PRIVACY-I

**开放代码：** 隐私数据清单与治理；日志去标识；工作流人员监测；默认分析争议；必要cookie与追踪区别

**逐条判断：** DSpace GDPR影响讨论转工作组；地方5.4删日志email/IP/Solr人员标识实践，bot追溯与最小化、科研provenance与劳动法冲突。GA默认关闭说法被5.x实际bean联网反证且key作用不明；必要session需同意初断言被纠正。末称v7改进将至，不是全合规完成。JIRA导入统一Participant1不等于真实单人意见。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 工作组接手，地方修改与未来核心改进

**原文证据：**

位置 `29540:29583`：

> A DSpace GDPR Working Group was established

位置 `27960:28027`：

> We actually disabled all the person related data from solr workflow

<a id="row-485"></a>
## 485. privacy-issue-4227

**主题代码：** PRIVACY-A, PRIVACY-B, PRIVACY-E, PRIVACY-H, PRIVACY-I, PRIVACY-Y

**开放代码：** 必要本地存储与同意边界；隐私设计最小化；上下文隐私控制入口

**逐条判断：** Datarequests拒大cookie popup，说明自动country/changed_saved_companies用途、本地功能数据不传及按功能链接控制；拟后者改仅交互后写。法律判断为维护者解释，未证改动上线。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 解释现设计，局部最小化计划

**原文证据：**

位置 `1431:1490`：

> We have very deliberately opted not to have a cookie popup.

<a id="row-486"></a>
## 486. privacy-issue-20629

**主题代码：** PRIVACY-A, PRIVACY-B, PRIVACY-H, PRIVACY-I

**开放代码：** 移除地域性提示；提示状态cookie最小化

**逐条判断：** 加拿大Notification要去EU告知banner及其intro cookie保留admin session；PR链接后测试证banner已去，未单独验证cookie删净。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 横幅移除验证

**原文证据：**

位置 `2781:2821`：

> Yeah, banner is gone for me when I test.

<a id="row-487"></a>
## 487. privacy-issue-7152

**主题代码：** PRIVACY-A, PRIVACY-C, PRIVACY-I

**开放代码：** 不必要广告商cookie同步；供应商同意粒度；跨页面同意互操作

**逐条判断：** Prebid AMP同步所有bidder引担忧，AMP仅布尔同意/单实例难接IAB CMP，讨论每商家目的限制未支持；server已有bidder list，转creative19传query params由publisher列告知商家。作者接受非最优临时方案，非证明全供应商同意合规。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 临时方案接受并转关联项目

**原文证据：**

位置 `11483:11567`：

> We have a non-optimal solution to ensure we have some level of consent on AMP pages.

<a id="row-488"></a>
## 488. privacy-issue-14352

**主题代码：** PRIVACY-D, PRIVACY-G, PRIVACY-I, PRIVACY-Z

**开放代码：** 去标识方法情境适用性；工具合规保证边界

**逐条判断：** ARX被问各选项GDPR指导，维护者称方法适配依数据/用途需专家选组合，无法一般推荐，非宣称任意方法即合规。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 情境性建议后关闭

**原文证据：**

位置 `1679:1770`：

> the suitability of different methods (or combination of methods) heavily depends on context

<a id="row-489"></a>
## 489. privacy-issue-18574

**主题代码：** PRIVACY-E, PRIVACY-F, PRIVACY-H

**开放代码：** 容器与评论权限不一致；搜索存在性泄露；历史数据权限迁移

**逐条判断：** Elgg登出搜comment容器get false，争论placeholder能推私密词及legacy公开转私密假设。作者实际改blog而非group隐私后确认消失；最终core修view，但无全库旧数据迁移证据。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 单例权限修复及view修复，历史全量补丁未证

**原文证据：**

位置 `11077:11130`：

> now the comment doesn't show up in the search results

位置 `11411:11449`：

> comments view is already fixed in core

<a id="row-490"></a>
## 490. privacy-issue-4381

**主题代码：** PRIVACY-B, PRIVACY-F, PRIVACY-H

**开放代码：** 公开范围即时告知；隐私控制缺失替代措施

**逐条判断：** EAHub上线无隐私控制所有profile公开，要求输入时说明；评论称edit/signup按钮下已加notice并获认可，图片未读不能复述具体文案。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 告知加入认可，未增加控制

**原文证据：**

位置 `2061:2102`：

> Added this note under the sign up button.

<a id="row-491"></a>
## 491. privacy-issue-2215

**主题代码：** PRIVACY-A, PRIVACY-B, PRIVACY-F, PRIVACY-H, PRIVACY-I

**开放代码：** 注册时隐私条款告知；服务商自定义同意

**逐条判断：** Solid POD托管需register链接policy/ToS，提出init可选有效URL、启用后checkbox必选，后明确892/869修复。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 关联PR修复确认

**原文证据：**

位置 `3115:3132`：

> This was fixed in

<a id="row-492"></a>
## 492. privacy-issue-20404

**主题代码：** PRIVACY-A, PRIVACY-H, PRIVACY-I, PRIVACY-Y

**开放代码：** 访客会话最小化；必要cookie争议；隐私与扩展兼容

**逐条判断：** Joomla tracker报错源于锁定旧讨论，正文另提访客全禁cookie；维护者指出session metadata现开关、扩展依user/session难判断需要性，作者给fake public session方案。法律争执双方归属观点，无cookie不等于绝无个人数据，末迁移非实现。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 讨论迁移，方案未落实

**原文证据：**

位置 `8773:8842`：

> most of the extensions (core and 3rd party) depend on a "user object"

<a id="row-493"></a>
## 493. privacy-issue-8244

**主题代码：** PRIVACY-D, PRIVACY-G, PRIVACY-I, PRIVACY-Y

**开放代码：** 交易匿名集有效性；公开辅助数据关联；群体隐私权衡；威胁假设随生态变化

**逐条判断：** Monero建议coinbase奖励/非奖励分环以剔不可信decoy，争论矿工暴露、complexity、ringsize和未来网络结构；coinbase非交易所。2022作者承认p2pool让普通人可花奖励输出，关键假设改变而关闭，仍5-10%未全解，非分环已实现。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 生态变化使提案不再必要

**原文证据：**

位置 `25595:25654`：

> This is no longer the case! Thank p2pool for changing this.

<a id="row-494"></a>
## 494. privacy-issue-13353

**主题代码：** PRIVACY-B, PRIVACY-C, PRIVACY-Z

**开放代码：** 分析仪表板集成；应用权限与用户权限区分；弱隐私关联

**逐条判断：** dotCMS请求GA API内嵌报表及app级权限因embed绑定用户，评论另移legacy webform；无具体隐私保护要求，不能由data sharing关键词推泄露。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 功能请求，实质隐私证据弱

**原文证据：**

位置 `1558:1592`：

> we will need app level permissions

<a id="row-495"></a>
## 495. privacy-issue-11449

**主题代码：** PRIVACY-B, PRIVACY-C, PRIVACY-H, PRIVACY-I

**开放代码：** 数据流目的地审计；DNS观测能力

**逐条判断：** OpenWPM请求cookie/请求DNS解析写SQLite以分析来源目的地和法规，721关闭声明；不是观测真实用户的隐私泄露报告。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 关联实现关闭

**原文证据：**

位置 `2501:2515`：

> Closed by #721

<a id="row-496"></a>
## 496. privacy-issue-15097

**主题代码：** PRIVACY-B, PRIVACY-C, PRIVACY-G, PRIVACY-I

**开放代码：** 外链访问去匿名风险；安全教育最小化；Tor威胁模型

**逐条判断：** SecureDrop担心警告页外链引指纹DNS/MITM/被攻站，建议简化本地说明减少分心，Tor2Web例外及文本URL；最终部分内容已去、不再计划清理，不能说全外链移除。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 部分内容移除并关闭

**原文证据：**

位置 `5543:5586`：

> Some of this content has since been removed

<a id="row-497"></a>
## 497. privacy-issue-7962

**主题代码：** PRIVACY-C, PRIVACY-F, PRIVACY-H, PRIVACY-Y

**开放代码：** 搜索建议退出失效；隐私设置回归；日志分享审慎

**逐条判断：** Fenix关建议后切引擎仍发送/显示建议，QA复现；作者更正停旧版策略为先输完整query再切引擎，迁Bugzilla未修复确认，敏感logcat未公开。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 回归确认，操作绕过并迁移

**原文证据：**

位置 `3082:3123`：

> I could reproduce the issue you described

位置 `2387:2444`：

> entering my entire query before selecting a search engine

<a id="row-498"></a>
## 498. privacy-issue-4253

**主题代码：** PRIVACY-H, PRIVACY-I

**开放代码：** 拒绝保存后功能不可用；隐私选项测试遗漏

**逐条判断：** Datarequests禁记身份导致signature null使generator完全失败，调试发现reset无条件覆盖而非默认构造问题，另开389测隐私控制。末称easy fix不是提交或验证证明。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 根因定位，修复落地未证

**原文证据：**

位置 `4213:4289`：

> We didn't think to test if things still work with modified privacy controls.

<a id="row-499"></a>
## 499. privacy-issue-4824

**主题代码：** PRIVACY-B, PRIVACY-D, PRIVACY-H, PRIVACY-I

**开放代码：** 私有字段去标识；最终验证缺失

**逐条判断：** Shanoir仅private fields标题和Neurinfo短正文，作者称本人完成待最终验证；不能推具体DICOM字段处理算法或质量。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 开发方完成，验收等待

**原文证据：**

位置 `1143:1179`：

> Waiting for final validation answers

<a id="row-500"></a>
## 500. privacy-issue-95

**主题代码：** PRIVACY-A, PRIVACY-H, PRIVACY-I

**开放代码：** 同意提示屏蔽

**逐条判断：** Brave请求可不见cookie prompts，仅duplicate10433，无本条实现或替代同意语义。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 重复转跟踪

**原文证据：**

位置 `1346:1363`：

> marking as a dupe

<a id="row-501"></a>
## 501. privacy-issue-5584

**主题代码：** PRIVACY-E, PRIVACY-F, PRIVACY-H, PRIVACY-I

**开放代码：** 完整账户内容删除；管理员中介与自助权衡

**逐条判断：** NodeBB用户要自删所有消息，维护者重视讨论上下文仅admin删除，用户20-30次人工请求负担，接受关闭。联系admin满足法律为维护者主张非认证。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 拒绝自助全删

**原文证据：**

位置 `1874:1954`：

> an administrator must do the act of deletion that removes all content for a user

<a id="row-502"></a>
## 502. privacy-issue-17464

**主题代码：** PRIVACY-B, PRIVACY-H, PRIVACY-I

**开放代码：** 隐私过滤误伤；cookie文档误屏蔽

**逐条判断：** Guzzle文档并未消失，Prebake按cookies id隐藏整节；named anchor实验有效但Sphinx重写被认为过度，提示/HTML注释待议，无最终变更确认。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 原因确认，修复方案未定

**原文证据：**

位置 `2992:3069`：

> Oh I think it's the Prebake adblock filter which hides all EU cookie notices.

<a id="row-503"></a>
## 503. privacy-issue-20319

**主题代码：** PRIVACY-Z

**开放代码：** 安全信任质疑；仅元数据证据

**逐条判断：** 仅UserVoice标题100% insecure，PII只在匹配元数据不能推具体收集泄露机制。

**材料可用性：** metadata_only。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 证据不足

**原文证据：**

位置 `65:109`：

> UserVoice Idea: 100% insecure - DO NOT TRUST

<a id="row-504"></a>
## 504. privacy-issue-12074

**主题代码：** PRIVACY-C, PRIVACY-F, PRIVACY-I

**开放代码：** 在线行为追踪最小化；用途正当性；拒绝新增监测

**逐条判断：** Discord bot拟存last online/activity粗粒度无历史防stalk，但反对跨guild在线状态收集；提案者认可过多、last message可按需查，最终关闭未新增。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 隐私顾虑下撤回

**原文证据：**

位置 `3684:3739`：

> Indeed, tracking the "online" status might be too much.

<a id="row-505"></a>
## 505. privacy-issue-20535

**主题代码：** PRIVACY-A, PRIVACY-E, PRIVACY-H, PRIVACY-I

**开放代码：** 客户端缓存保留期限；库默认约束与用户控制

**逐条判断：** Workbox建议maxAgeSeconds必填、默认最长3年或终端用户可设期限以防cache个人数据永存，法律和年限为开发者提议非既定规则，无评论实施。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 保留期API提案未证落地

**原文证据：**

位置 `1983:2020`：

> Change `maxAgeSeconds` to be required

<a id="row-506"></a>
## 506. privacy-issue-3757

**主题代码：** PRIVACY-A, PRIVACY-B, PRIVACY-C, PRIVACY-D, PRIVACY-H, PRIVACY-I

**开放代码：** 默认遥测同意；控制标签与动作一致性；收集透明度；IP传输与留存区别；下游默认策略

**逐条判断：** Cura争论默认开启SliceInfo及匿名性；维护者披露设置和mesh hash非模型，3.2按钮实际开偏好后修标签，master增信息对话框；Debian2020单独默认关闭，上游未证opt-in。IP接收/保存及法律观点有争议，不能断言绝对匿名。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 上游改进控制披露，下游默认关闭

**原文证据：**

位置 `9472:9561`：

> 3.2 will have a button that takes you to the preferences window where you can disable it.

位置 `41137:41208`：

> Our master branch now has the following dialogue with more information:

位置 `43085:43144`：

> Fwiw, I've disabled the telemetry by default now in Debian.

<a id="row-507"></a>
## 507. privacy-issue-6824

**主题代码：** PRIVACY-B, PRIVACY-F, PRIVACY-H, PRIVACY-I, PRIVACY-Y, PRIVACY-Z

**开放代码：** 本地部署隐私误解；隐私负例

**逐条判断：** 新用户把浏览器Notebook误认为远程服务器和必须联网，答复localhost在自己电脑并解释重命名；后续Lab启动和输出滚动问题未解，无实际外传证据。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 本地架构澄清

**原文证据：**

位置 `2201:2275`：

> It opens in your browser, but it is actually running on your own computer.

<a id="row-508"></a>
## 508. privacy-issue-20221

**主题代码：** PRIVACY-F, PRIVACY-H, PRIVACY-I

**开放代码：** 字段级可见性；发布时隐藏身份；权限模型简化；隐私功能验证

**逐条判断：** Ushahidi为发布核验帖子隐藏PII；起初按字段角色后改private开关，仅能编辑整帖者能见私有字段，不支持部分编辑；提交仍可填。hide author隐藏署名，非新增采集。QA修私有照片及管理员不可见等，最终确认私有字段正常；tasks改sections未采纳。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 私有字段测试通过关闭

**原文证据：**

位置 `29577:29606`：

> Private fields work perfectly

位置 `18380:18447`：

> this is not field level permissions, it's more field level locking.

<a id="row-509"></a>
## 509. privacy-issue-2895

**主题代码：** PRIVACY-B, PRIVACY-F, PRIVACY-I

**开放代码：** 发布前PII审核；表单隐私提示；图片使用许可

**逐条判断：** Mozilla内容贡献可能含PII，提议投稿及审核提示；资料bio/图片等部分勾选，描述和moderator提示未勾；2022陈旧关闭不能视全实现。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 部分提示存在，剩余陈旧关闭

**原文证据：**

位置 `2318:2393`：

> Look for personally identifiable information that should not be made public

<a id="row-510"></a>
## 510. privacy-issue-7526

**主题代码：** PRIVACY-A, PRIVACY-B, PRIVACY-F, PRIVACY-H, PRIVACY-Y

**开放代码：** 隐私模式持续性；隐私控制可理解性；跨应用链接模式

**逐条判断：** Fenix外链沿用上次private模式是预期设计；用户争论传统行为和更私密默认，最终要求明确持续状态及选择普通/私密打开，转419，非确认泄漏。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 按设计运行，UX需求转跟踪

**原文证据：**

位置 `8312:8334`：

> It's intended behavior

<a id="row-511"></a>
## 511. privacy-issue-18418

**主题代码：** PRIVACY-F, PRIVACY-G, PRIVACY-H, PRIVACY-I

**开放代码：** 学生上传公开暴露；文件URL不可猜测性；访问控制不足

**逐条判断：** Sensei测验上传进公共媒体库可直链访问；维护者承认非意图转bug，提随机URL混淆，无实施时间；随机不可猜不能等同身份授权，闭合状态不证修复。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 承认问题并提出混淆，未证实施

**原文证据：**

位置 `925:1004`：

> all files uploaded by learners as quiz answers, are stored in the media library

位置 `4407:4478`：

> Our proposed solution is to obfuscate the file url with a random string

<a id="row-512"></a>
## 512. privacy-issue-5484

**主题代码：** PRIVACY-E, PRIVACY-F, PRIVACY-H, PRIVACY-I

**开放代码：** 资料可见性自主控制；去索引与删除区别；公共记录用途冲突

**逐条判断：** WCA用户要隐藏搜索和资料但继续用服务，回应先引遗忘权人工流程，用户澄清不求删除；组织以比赛成绩用途拒绝public/private切换，称支持匿名化。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 拒绝私有资料功能，保留匿名化流程

**原文证据：**

位置 `3552:3637`：

> we support anonymizing profiles, and we don't intend to add "public/private" profiles

<a id="row-513"></a>
## 513. privacy-issue-19530

**主题代码：** PRIVACY-B, PRIVACY-G, PRIVACY-H

**开放代码：** 诊断日志提交前审阅；本地导出控制；诊断完整性与隐私

**逐条判断：** Signal无SIM通话故障排查中用户拒绝未审阅即上传；屏幕日志约8.79KiB截断，用户测试排除剪贴板限制。维护者称日志去号码/无消息及secret gist，仍不满足上传前本地检查；后用adb/CatLog排查同步锁ROM疑因，清理关闭未证修复。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 本地排查继续，日志控制需求未证解决

**原文证据：**

位置 `10840:10891`：

> I need to see what I'm sending before I publish it.

<a id="row-514"></a>
## 514. privacy-issue-9470

**主题代码：** PRIVACY-A, PRIVACY-B, PRIVACY-H

**开放代码：** Cookie提示可关闭性；响应式界面状态

**逐条判断：** VSCode docs小屏TOPICS导航不清cookie横幅；报告者一度不能复现但维护者仍复现，最终明确修复发布。涉及告知界面，不足推断同意机制合规。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 修复并发布

**原文证据：**

位置 `4492:4512`：

> Fixed and published.

<a id="row-515"></a>
## 515. privacy-issue-20609

**主题代码：** PRIVACY-A, PRIVACY-E, PRIVACY-H, PRIVACY-I

**开放代码：** 本地持久存储选择；会话级数据保留；同意后的存储切换

**逐条判断：** Shopify SDK请求sessionStorage替localStorage并随保存购物车选择迁移；卸载页面清理只是设想权宜，无实现，因不活跃关闭。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 需求陈旧关闭

**原文证据：**

位置 `1010:1081`：

> I'd like to give users the option to turn off persistent local storage.

<a id="row-516"></a>
## 516. privacy-issue-12047

**主题代码：** PRIVACY-F, PRIVACY-H, PRIVACY-Y

**开放代码：** 隐私状态反馈误导；缩略图残留；隐私负例

**逐条判断：** Signal发送者看到被裁掉片段缩略图，原文明确接收者看正确片段；后续确认会话列表仍错，非已证外发泄露，stale关闭。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 界面问题未证修复，无接收方泄露

**原文证据：**

位置 `2082:2140`：

> there is no "breach of privacy", but the UI is misleading.

<a id="row-517"></a>
## 517. privacy-issue-942

**主题代码：** PRIVACY-D, PRIVACY-F, PRIVACY-I

**开放代码：** 跨实例健康数据共享；关联对象假名化；共享范围选择

**逐条判断：** SORMAS要求病例共享连同关联接触者，并对全部应用假名化和ownership选项，另可选不分享接触者；无评论实施证据。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 功能要求，关闭但未证实现

**原文证据：**

位置 `1307:1367`：

> apply pseudonymization and ownership options on all of them.

<a id="row-518"></a>
## 518. privacy-issue-21332

**主题代码：** PRIVACY-A, PRIVACY-C, PRIVACY-G, PRIVACY-H, PRIVACY-I

**开放代码：** 同意前SDK初始化；依赖隐式数据访问；应用商店隐私审核

**逐条判断：** WebView内部Provider初始化触发包信息访问，非manifest显式权限；fork延迟初始化过小米审核，官方5.7.2+3和6beta22改首次native方法调用初始化。随后OPPO同版本仍拒，堆栈为创建WebView查com.android.webview包，不能扩大成任意全列表抓取已证或全面修好。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 延迟初始化发布，后续仍有审核失败

**原文证据：**

位置 `8804:8852`：

> Fixed with release `6.0.0-beta.22` and `5.7.2+3`

位置 `9462:9522`：

> Our application was rejected in the OPPO application market.

<a id="row-519"></a>
## 519. privacy-issue-9382

**主题代码：** PRIVACY-A, PRIVACY-B, PRIVACY-H, PRIVACY-I

**开放代码：** 隐私与Cookie告知组件；平台间提示一致性

**逐条判断：** BBC请求AMP/canonical共用banner展示组件、按钮链接样式和4个故事，条件逻辑与文章集成另PR，不能等同端到端同意功能已上线。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 组件需求，未见实施确认

**原文证据：**

位置 `1674:1733`：

> Do not integrate into the Article container in this ticket.

<a id="row-520"></a>
## 520. privacy-issue-5595

**主题代码：** PRIVACY-A, PRIVACY-B, PRIVACY-D, PRIVACY-E, PRIVACY-F, PRIVACY-H, PRIVACY-I

**开放代码：** 撤回同意工作流；删除请求人工处理；请求审计与删除冲突；响应期限提醒

**逐条判断：** Chamilo将撤回和删户分为两个可并存请求，管理员处理前仍能访问；通知DPO/管理员，记录理由日期，操作删除/匿名化/撤条款后清请求字段。多轮测试修相互覆盖，cron已加但未见独立验收，临时图标提前关闭；周数是项目规格非法律核定。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 主要流程验证，cron已实现，图标待补

**原文证据：**

位置 `17279:17295`：

> I added the cron

位置 `21526:21560`：

> I'm closing this task prematurely.

<a id="row-521"></a>
## 521. privacy-issue-5076

**主题代码：** PRIVACY-B, PRIVACY-C, PRIVACY-D, PRIVACY-I

**开放代码：** 分析服务IP去标识；配置验证

**逐条判断：** OpenLiberty在GTM设anonymizeIp true并观察collect请求aip=1确认标志启用；不等于独立验证Google处理或整体GDPR合规。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 参数配置且网络验证

**原文证据：**

位置 `1897:1976`：

> I verified that the IP anonymization property is enabled by looking for `aip=1`

<a id="row-522"></a>
## 522. privacy-issue-3720

**主题代码：** PRIVACY-A, PRIVACY-B, PRIVACY-C, PRIVACY-I

**开放代码：** 默认第三方分析；公益用途与隐私取舍；透明度补救；资源约束延迟替换

**逐条判断：** 气候罢工widget默认GA把原未用GA站用户带给Google，团队以活动网站统计和宣传价值维持opt-out；已改README披露，Matomo迁移77因截止日期人力培训推迟，无移除完成证据。无PII是维护者主张。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 保留默认分析，披露更新并另开迁移

**原文证据：**

位置 `5066:5136`：

> I've updated the README with a section about Google Analytics tracking

<a id="row-523"></a>
## 523. privacy-issue-8945

**主题代码：** PRIVACY-A, PRIVACY-H, PRIVACY-I

**开放代码：** Cookie细分控制；必要Cookie例外

**逐条判断：** Cezerin要求banner持续到接受/设置，可开关非必要cookies，系统必要不可关，作者回复released；无进一步行为测试。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 报告已发布

**原文证据：**

位置 `1498:1506`：

> released

<a id="row-524"></a>
## 524. privacy-issue-14157

**主题代码：** PRIVACY-B, PRIVACY-C, PRIVACY-I, PRIVACY-Y, PRIVACY-Z

**开放代码：** 法规压力暂停功能；隐私关联证据有限

**逐条判断：** Notebook原为机器翻译加校对且依据GA选语种，后以GDPR为由暂停；未解释具体数据或义务，不推断翻译传送个人信息。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 翻译功能因GDPR理由暂停

**原文证据：**

位置 `1406:1471`：

> Due to GDPR, we're holding off on doing any translations for now.

<a id="row-525"></a>
## 525. privacy-issue-3760

**主题代码：** PRIVACY-B, PRIVACY-C, PRIVACY-D, PRIVACY-G, PRIVACY-H, PRIVACY-I

**开放代码：** 性能诊断去标识；URL与路径身份线索；隐私与诊断效用

**逐条判断：** Firefox profiler已有网络URL上传防护但marker/source仍含URL；请求去除或保留常见域白名单，并使用户知道共享范围及工程师仍可诊断；转1802无本帖完成。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 继续另案设计

**原文证据：**

位置 `1031:1115`：

> PII is still spread across profiles as URLs are included in markers and source file.

<a id="row-526"></a>
## 526. privacy-issue-20566

**主题代码：** PRIVACY-A, PRIVACY-B, PRIVACY-H, PRIVACY-I

**开放代码：** Cookie同意开箱可用性；平台与插件责任

**逐条判断：** PrestaShop用户要求内置Cookie询问，别人提免费模块，维护者只指官方商城关闭；非新增核心功能或合规验证。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 指向插件，核心无更改

**原文证据：**

位置 `2239:2292`：

> This feature is available on the official marketplace

<a id="row-527"></a>
## 527. privacy-issue-14087

**主题代码：** PRIVACY-B, PRIVACY-C, PRIVACY-G, PRIVACY-I

**开放代码：** 跨服务事件共享；聊天副本数据最小化

**逐条判断：** Pretix webhook接RocketChat脚本发订单代码事件组织和控制台日志，作者说新订单可用并提醒扩展REST信息注意聊天中个人数据；无泄漏案例或删除机制。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 集成示例可用，扩展需注意数据范围

**原文证据：**

位置 `3384:3434`：

> be careful with personal data you save in the chat

<a id="row-528"></a>
## 528. privacy-issue-14142

**主题代码：** PRIVACY-E, PRIVACY-F, PRIVACY-I

**开放代码：** 数据盘点与关联识别；删除与财务留存冲突；个人数据访问导出；同意记录；生态协同合规

**逐条判断：** EDD71评论从免费插件路线变为接WP核心导出/擦除工具；盘点姓名邮箱IP授权URL交易关联，争论税务留存及争议期，不把法律意见定论。早期邮件过期链接支持无账户访客，后优先核心；5月18分部署/合并/测试状态，最终2.9.2/3发布初步GDPR功能，非全部扩展或整体法律合规保证。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 初步功能发布，扩展和后续另案

**原文证据：**

位置 `50230:50309`：

> EDD 2.9.2 (and subsequently 2.9.3) are released with our initial work for GDPR.

<a id="row-529"></a>
## 529. privacy-issue-18596

**主题代码：** PRIVACY-F, PRIVACY-H

**开放代码：** 资料字段权限覆盖；隐私设置执行

**逐条判断：** ChurchCRM关闭成员隐私访问仍见About Me，维护者截图表示未见问题，报告者后答No thanks不再有问题；未见代码原因或独立验证，不能具体声称修了什么。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 报告者表示不再存在

**原文证据：**

位置 `1017:1089`：

> I would expect the 'About Me' information to be treated as privacy data.

位置 `2293:2302`：

> No thanks

<a id="row-530"></a>
## 530. privacy-issue-228

**主题代码：** PRIVACY-B, PRIVACY-E, PRIVACY-F, PRIVACY-G, PRIVACY-H, PRIVACY-I, PRIVACY-Y

**开放代码：** 本地消息静态加密；数据保留选择；泄露主张被反驳

**逐条判断：** Element用户称IndexedDB明文历史并求口令/内存存储；维护者反驳加密房间事件仍按加密形式保存，引私下安全渠道；未提供验证，无证据确认所有消息明文。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 主张有争议，转安全渠道

**原文证据：**

位置 `1778:1843`：

> Element does store encrypted room events in their encrypted form.

<a id="row-531"></a>
## 531. privacy-issue-8869

**主题代码：** PRIVACY-F, PRIVACY-H

**开放代码：** Cookie控制可达性；嵌入浏览器遮挡

**逐条判断：** WP iOS Reader底栏遮住第三方网站accept/deny按钮，复现步骤设备明确，后只有认领修复，无完成文本。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 缺陷已描述，未证修复

**原文证据：**

位置 `1284:1379`：

> The bottom overlay bar gets on top of important elements like the button to accept/deny cookies

<a id="row-532"></a>
## 532. privacy-issue-5016

**主题代码：** PRIVACY-D, PRIVACY-G, PRIVACY-H

**开放代码：** 去标识保持结构；日志匿名化精度

**逐条判断：** WSO2 forgetme替用户名时连performedBy键一起删，粘贴前后log证结构坏影响后续处理；工具PR83修且产品3386升级。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 工具修复并升级集成

**原文证据：**

位置 `1340:1401`：

> Original placeholders should not be changed by anonymization.

位置 `2514:2535`：

> Version upgraded with

<a id="row-533"></a>
## 533. privacy-issue-3933

**主题代码：** PRIVACY-A, PRIVACY-C, PRIVACY-I

**开放代码：** URL个人信息第三方外发；跟踪阻断覆盖

**逐条判断：** Calypso已有URL潜在PII时阻第三方规则，HotJar漏纳要求同用isPiiUrl；只有承诺认领，关闭不证明落地。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 要求补齐阻断，未见完成确认

**原文证据：**

位置 `1106:1140`：

> We need to do the same for HotJar.

<a id="row-534"></a>
## 534. privacy-issue-3643

**主题代码：** PRIVACY-A, PRIVACY-C, PRIVACY-G, PRIVACY-I

**开放代码：** 默认遥测同意；退出后连接残留；依赖意外跟踪；诊断数据去标识；功能收益与自主权冲突

**逐条判断：** Etcher49评论审计承认网页带第三方及Sentry用户名路径/IP，承诺移除；1.5.63仍连后发现选项开着，1.5.70维护者实测退出无分析连接但仍加载推广网页。刷写可离线。默认opt-in诉求未采纳而关闭；法律/匿名/恶意软件争论为参与者观点，不抹去已承认早期PII。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 部分外连修正，仍保留默认遥测及内容连接

**原文证据：**

位置 `7759:7803`：

> The IP address of the event was also logged.

位置 `31158:31212`：

> there were connections to our static site, `balena.io`

<a id="row-535"></a>
## 535. privacy-issue-14167

**主题代码：** PRIVACY-B, PRIVACY-I, PRIVACY-Z

**开放代码：** 合规调查与准备

**逐条判断：** DOAJ指派GDPR调查并贴PDF和步骤链接，正文无具体数据控制实施或评估结论；外链未读。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 调查任务，无完成详情

**原文证据：**

位置 `889:963`：

> DOAJ will need to make its own investigations to make sure it is prepared.

<a id="row-536"></a>
## 536. privacy-issue-12109

**主题代码：** PRIVACY-F, PRIVACY-G, PRIVACY-H, PRIVACY-I

**开放代码：** 异常路径跨客户泄露；共享对象状态隔离；插件与核心责任

**逐条判断：** Magento异步邮件cron异常绕过单例TransportBuilder重置，使前一客户收下一客户订单；插件升级不兼容触发但核心应防御。2021贴try/finally reset代码并指2019提交，作者仅代码判断2.3.3-p1/2.4.2已修且无法运行复核，随后关闭。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 依据代码认定已修，缺报告者运行复验

**原文证据：**

位置 `11270:11340`：

> although I'm not able to check at the moment whether this is the case.

<a id="row-537"></a>
## 537. privacy-issue-1723

**主题代码：** PRIVACY-A, PRIVACY-B, PRIVACY-C, PRIVACY-H, PRIVACY-I

**开放代码：** 默认遥测告知；隐私用语一致性；法律审批与用户理解

**逐条判断：** Fenix onboarding未说默认遥测，用户求开关；回复卡片已法务批准，调整设置与notice用语Usage and technical data一致，最后据审批关闭，无证明加首次开关或改默认。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 批准文案方向并关闭，未证默认变更

**原文证据：**

位置 `2294:2336`：

> The onboarding card was approved by legal.

<a id="row-538"></a>
## 538. privacy-issue-2510

**主题代码：** PRIVACY-A, PRIVACY-B, PRIVACY-H, PRIVACY-I

**开放代码：** 第三方Cookie告知；组织合规流程

**逐条判断：** Helm站提交cookie portal后要求EU disclaimer，附内部步骤；无评论确认实施。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 告知要求，未证实现

**原文证据：**

位置 `973:1020`：

> this site will need a Cookie disclaimer message

<a id="row-539"></a>
## 539. privacy-issue-8988

**主题代码：** PRIVACY-B, PRIVACY-H

**开放代码：** 多语言隐私告知；翻译验证

**逐条判断：** BBC多语服务cookie/privacy banner等翻译导入验证；部分就绪，语言链接误指英文及404路由问题；尾部8语言待部署测试，不能称所有验证通过。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 部分就绪，剩余语言待测

**原文证据：**

位置 `4843:4948`：

> Will test Thai, Punjabi, Afaan Oromoo, Amharic, Tigrinya, Marathi, Telugu, Gujarati when they are on test

<a id="row-540"></a>
## 540. privacy-issue-5411

**主题代码：** PRIVACY-E, PRIVACY-F, PRIVACY-G, PRIVACY-I

**开放代码：** 公链隐私访问限制；界面隐藏不等于删除；链下存储与密钥权衡

**逐条判断：** DeSo不支持限群帖子，隐藏父帖回复仍在公开链；维护者称私有内容需链下，用户提共享密钥和MLS，末尾仅外链，无实现确认；PII不在链为参与者主张非保证。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 现架构不支持，讨论替代方案

**原文证据：**

位置 `1454:1512`：

> Of course the replies will still be in the open blockchain

位置 `2946:3000`：

> Any private content would need to be stored off chain.

<a id="row-541"></a>
## 541. privacy-issue-8843

**主题代码：** PRIVACY-A, PRIVACY-B, PRIVACY-H

**开放代码：** Cookie接受界面；仅元数据证据

**逐条判断：** 仅blockframes更新cookie接受栏标题与24评论计数，未获正文，不推测具体控制或实现。

**材料可用性：** metadata_only。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 证据不足

**原文证据：**

位置 `65:94`：

> Update cookie acceptation bar

<a id="row-542"></a>
## 542. privacy-issue-3700

**主题代码：** PRIVACY-D, PRIVACY-Y

**开放代码：** 隐私检查误报；隐私负例

**逐条判断：** 自动PII检查要求GA anonymizeIP，维护者明确bot失败并非实际问题；不编码已确认未匿名泄漏。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 自动检查误报

**原文证据：**

位置 `1242:1293`：

> Bot failure - can confirm that this is not an issue

<a id="row-543"></a>
## 543. privacy-issue-1950

**主题代码：** PRIVACY-B, PRIVACY-H

**开放代码：** 隐私告知可访问性；链接视觉对比度

**逐条判断：** Mozilla捐赠页Privacy Notice对比不达AA，改浅蓝#b7b9fa并随footer273更新；仅UI可读性改进非数据行为变化。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 随页脚更新修复

**原文证据：**

位置 `2724:2742`：

> Updated along side

<a id="row-544"></a>
## 544. privacy-issue-18351

**主题代码：** PRIVACY-A, PRIVACY-C, PRIVACY-F, PRIVACY-G, PRIVACY-H, PRIVACY-I

**开放代码：** 已读行为披露控制；隐私与通知耦合；跨客户端设置执行

**逐条判断：** Element要停发回执可按房间，早期return导致通知卡住；2019实验开关仍待服务器/spec，2020发现无兼容服务器后从labs移除，尾部拒破通知权宜并锁帖。停显示别人的回执不等于停发自己的，关闭不证完成。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 实验功能撤下，依赖通知重构

**原文证据：**

位置 `11924:12023`：

> ftr the option has been removed from labs because there's no such thing as a compatible homeserver.

<a id="row-545"></a>
## 545. privacy-issue-11413

**主题代码：** PRIVACY-A, PRIVACY-B, PRIVACY-C, PRIVACY-H, PRIVACY-I

**开放代码：** 跨系统同意信号解释；法规格式区分；无效同意验证

**逐条判断：** AMP gdpr_consent可能实为CCPA，PBS批准同义consent_string解析4字符US或TCF后填对应OpenRTB字段，无效警告忽略，与enforce范围独立；三态不足替细分。Go/Java最终报告done，旧key退役及TCF2另未来。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** Go与Java完成本案支持

**原文证据：**

位置 `11912:11937`：

> Done for both Go and Java

<a id="row-546"></a>
## 546. privacy-issue-12177

**主题代码：** PRIVACY-E, PRIVACY-F, PRIVACY-H, PRIVACY-I

**开放代码：** 自助查询身份验证；申请状态隐私；重复记录保留语义

**逐条判断：** Carpentries想自助查是否申请但公共名单会泄露，现有确认邮件不可靠，讨论登录及按邮箱查重复；定第一阶段发申请副本，重复清单已有，不能盲合并反映技能变化的新申请；无邮件副本实施确认。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 分阶段规划，重复清单已有

**原文证据：**

位置 `7747:7833`：

> For the first phase of this, we would like to send people a copy of their application.

<a id="row-547"></a>
## 547. privacy-issue-17623

**主题代码：** PRIVACY-A, PRIVACY-B, PRIVACY-C, PRIVACY-D, PRIVACY-H, PRIVACY-I

**开放代码：** 分析运行时同意门控；Cookie期限配置；第三方同意工具

**逐条判断：** Gatsby要默认停GA获同意后动态开，原作者反对框架猜地区；讨论匿名IP及session cookies，后cookieExpires已有，分享Tarteaucitron/Cookiehub方案，后者有人实测可用但服务覆盖受限；陈旧关闭无核心开关完成证据，样例法律解释非认证。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 配置与第三方方案，原核心需求未证完成

**原文证据：**

位置 `2614:2669`：

> allow to enable it at run time, rather than built time.

<a id="row-548"></a>
## 548. privacy-issue-21496

**主题代码：** PRIVACY-H, PRIVACY-Y

**开放代码：** 隐私设置与功能依赖

**逐条判断：** cactbot钓鱼位置/抛竿不更新属游戏日志，不是真实地理定位；先建议启Own Gathering Messages，后证ACT Hide Chat Log隐私设置阻模块检测；无泄漏。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 识别日志隐私开关导致功能不可用

**原文证据：**

位置 `3845:3966`：

> "Hide Chat Log (for privacy)" in the FFXIV plugin for ACT prevents the fisher module from detecting when the line is cast

<a id="row-549"></a>
## 549. privacy-issue-14060

**主题代码：** PRIVACY-G, PRIVACY-H, PRIVACY-I

**开放代码：** 传输加密配置可用性；安全配置绕行

**逐条判断：** DBeaver DB2 ssl属性设置无效，多用户确认把sslConnection与truststore串放database字段能用；truststore为本机，原作者后不用DB2不能验证最新版；法律动机一条不等于合规结论。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 用户确认配置绕行，未证核心修复

**原文证据：**

位置 `5205:5270`：

> SSL begin to work if put ssl properties into database name field.

<a id="row-550"></a>
## 550. privacy-issue-4799

**主题代码：** PRIVACY-A, PRIVACY-B, PRIVACY-C, PRIVACY-E, PRIVACY-H, PRIVACY-I

**开放代码：** 退出遥测仍外连；Referer与IP泄露；云服务与遥测边界；自托管分析替代

**逐条判断：** Netdata退出只阻GA标签仍取GTM并传referrer；cloud base URL配置用户确认停云连接，代理same-origin头可去Referer。2020计划移agent除index GTM，2021旧1.12仍连，PostHog仅demo测试。维护者称无PII与用户异议并存，不能视改自托管已完成或退出彻底。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 部分绕行验证，残余外连与迁移未全解决

**原文证据：**

位置 `8444:8518`：

> The option suggested works fine for disabling the call to `netdata.cloud`.

位置 `21249:21302`：

> We are testing this on our demo servers at the moment

<a id="row-551"></a>
## 551. privacy-issue-2892

**主题代码：** PRIVACY-A, PRIVACY-B, PRIVACY-C, PRIVACY-H, PRIVACY-I

**开放代码：** 遥测退出可发现性；系统与应用控制边界；构建版本数据差异；收集内容透明度

**逐条判断：** Winget私有构建无遥测官方构建有，起初指Windows策略引不满；维护者后给Diagnostics & feedback路径并开279独立开关，参与者据PR称Basic停winget遥测。匿名性/GDPR争论不作定论，无法把独立开关视已实现。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 系统退出路径澄清，应用开关另案

**原文证据：**

位置 `31285:31346`：

> The current client does respect machine wide privacy settings

位置 `33035:33060`：

> Opt-Out of Telemetry #279

<a id="row-552"></a>
## 552. privacy-issue-16578

**主题代码：** PRIVACY-A, PRIVACY-B, PRIVACY-C, PRIVACY-E, PRIVACY-H, PRIVACY-I

**开放代码：** 拒绝后Cookie写入；同意状态缓存；初始化竞态；严格存储执行

**逐条判断：** Prebid存30天consent hash用于ID同意变更，先辩必要cookie后6551提移至GDPR验证后。2023 CMP晚加载仍因null默认gdprApplies false写hash，共享ID受strictStorageEnforcement约束，不能把PR当全部修好。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 修补后仍有顺序缺陷与配置边界

**原文证据：**

位置 `7905:7984`：

> This fix doesn't work, at least in the case where the CMP is loaded after PBJS.

<a id="row-553"></a>
## 553. privacy-issue-12310

**主题代码：** PRIVACY-A, PRIVACY-B, PRIVACY-E, PRIVACY-F, PRIVACY-G, PRIVACY-H, PRIVACY-I

**开放代码：** 局域网DNS行为日志；管理员与使用者隐私边界；日志关闭控制；本地界面访问保护

**逐条判断：** Pi-hole默认记DNS使家人私密浏览仍可被管理员看；维护者强调本地不外传但承认部署者需告知，保留默认日志，展示下一版CLI/设置禁日志与密码保护计划。LE因范围/条款同意拒集成，TLS论述为当时参与者观点。

**材料可用性：** complete。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 保持默认日志，宣布关闭控制及密码保护

**原文证据：**

位置 `7423:7459`：

> we leave logging enabled by default.

<a id="row-554"></a>
## 554. privacy-issue-2384

**主题代码：** PRIVACY-B, PRIVACY-H

**开放代码：** 隐私告知链接；仅元数据证据

**逐条判断：** Ubuntu标题要求各notice首段末加链接，目标和实施不明。

**材料可用性：** metadata_only。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 证据不足

**原文证据：**

位置 `65:127`：

> Add link to end of first paragraph on each privacy notice page

<a id="row-555"></a>
## 555. privacy-issue-4346

**主题代码：** PRIVACY-D, PRIVACY-F, PRIVACY-G

**开放代码：** 健康标识关联风险；仅元数据证据

**逐条判断：** CWA标题要求防用户身份与上传诊断密钥关联；无32条讨论，不推具体攻击或修复。

**材料可用性：** metadata_only。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 证据不足

**原文证据：**

位置 `65:125`：

> Prevent linking of user identity and uploaded diagnosis keys

<a id="row-556"></a>
## 556. privacy-issue-302

**主题代码：** PRIVACY-H, PRIVACY-Z

**开放代码：** 反跟踪与Cookie兼容；仅元数据证据

**逐条判断：** Laravel Shopify标题含ITP/Cookie/重定向，缺74评论无法定位失败机制。

**材料可用性：** metadata_only。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 证据不足

**原文证据：**

位置 `65:106`：

> Browser Issues: ITP, Cookies, Redirection

<a id="row-557"></a>
## 557. privacy-issue-15163

**主题代码：** PRIVACY-H, PRIVACY-Z

**开放代码：** 权限策略命名；隐私关联证据有限；仅元数据证据

**逐条判断：** WebXR只问Feature Policy vr名称是否改，fingerprinting只在匹配元数据，不推测指纹机制。

**材料可用性：** metadata_only。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 证据不足

**原文证据：**

位置 `65:125`：

> Should the Feature Policy feature name be changed from "vr"?

<a id="row-558"></a>
## 558. privacy-issue-8901

**主题代码：** PRIVACY-A, PRIVACY-C

**开放代码：** 同意前第三方Cookie；仅元数据证据

**逐条判断：** Nameless标题报告同意前设第三方cookie，无触发组件或修复证据。

**材料可用性：** metadata_only。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 证据不足

**原文证据：**

位置 `65:112`：

> Third party cookies are set before user consent

<a id="row-559"></a>
## 559. privacy-issue-14310

**主题代码：** PRIVACY-C, PRIVACY-D, PRIVACY-I

**开放代码：** 遥测去标识；仅元数据证据

**逐条判断：** AzureAD标题GDPR PII/OII过滤遥测，缺字段及实现。

**材料可用性：** metadata_only。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 证据不足

**原文证据：**

位置 `65:101`：

> GDPR PII/OII Filtering for Telemetry

<a id="row-560"></a>
## 560. privacy-issue-5461

**主题代码：** PRIVACY-E, PRIVACY-I

**开放代码：** 删除与遗忘请求；仅元数据证据

**逐条判断：** Lifebank仅遗忘权标题，hold标签不说明最终实现。

**材料可用性：** metadata_only。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 证据不足

**原文证据：**

位置 `65:86`：

> Right to be Forgotten

<a id="row-561"></a>
## 561. privacy-issue-18373

**主题代码：** PRIVACY-C, PRIVACY-F

**开放代码：** 推送载荷最小化；仅元数据证据

**逐条判断：** Synapse标题要求消息内容不发推送服务器，无正文不能确认暴露范围。

**材料可用性：** metadata_only。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 证据不足

**原文证据：**

位置 `65:129`：

> We should never be sending contents of messages to push servers.

<a id="row-562"></a>
## 562. privacy-issue-9828

**主题代码：** PRIVACY-B, PRIVACY-H

**开放代码：** Cookie使用告知；仅元数据证据

**逐条判断：** Webhint要求使用Cookie横幅，不能推同意按钮或拦截功能。

**材料可用性：** metadata_only。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 证据不足

**原文证据：**

位置 `65:106`：

> Need banner telling people we use cookies

<a id="row-563"></a>
## 563. privacy-issue-11364

**主题代码：** PRIVACY-E

**开放代码：** 删除传播与副本残留；仅元数据证据

**逐条判断：** Libraries标题请求删除已删repo，缺个人信息内容和同步原因。

**材料可用性：** metadata_only。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 证据不足

**原文证据：**

位置 `65:100`：

> please remove already deleted repos

<a id="row-564"></a>
## 564. privacy-issue-7425

**主题代码：** PRIVACY-E, PRIVACY-H

**开放代码：** 批量删除登录数据；仅元数据证据

**逐条判断：** Fenix标题要删所有logins，未说明同步账户范围及实现。

**材料可用性：** metadata_only。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 证据不足

**原文证据：**

位置 `65:97`：

> Add ability to delete all logins

<a id="row-565"></a>
## 565. privacy-issue-1155

**主题代码：** PRIVACY-D, PRIVACY-H

**开放代码：** 假名化存储兼容；仅元数据证据

**逐条判断：** Snowplow Redshift要求加宽atomic.events敏感列支持假名化，算法和宽度未知。

**材料可用性：** metadata_only。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 证据不足

**原文证据：**

位置 `75:143`：

> widen sensitive columns in atomic.events to support pseudonymization

<a id="row-566"></a>
## 566. privacy-issue-12305

**主题代码：** PRIVACY-Z

**开放代码：** 默认主题隐私；仅元数据证据

**逐条判断：** Pelican标题指默认主题侵犯隐私，不能猜字体/分析等具体第三方。

**材料可用性：** metadata_only。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 证据不足

**原文证据：**

位置 `65:112`：

> Default themes should not breach users' privacy

<a id="row-567"></a>
## 567. privacy-issue-12023

**主题代码：** PRIVACY-B, PRIVACY-I

**开放代码：** 隐私事件响应准备；仅元数据证据

**逐条判断：** BCgov要求云泄露事件模板，不表示实际发生泄露。

**材料可用性：** metadata_only。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 证据不足

**原文证据：**

位置 `65:136`：

> Create cloud focused incident breach templates for privacy and security

<a id="row-568"></a>
## 568. privacy-issue-14082

**主题代码：** PRIVACY-C

**开放代码：** 崩溃诊断上报；仅元数据证据

**逐条判断：** Alva标题要崩溃发报告，未知载荷、同意与GDPR联系。

**材料可用性：** metadata_only。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 证据不足

**原文证据：**

位置 `65:112`：

> Send crashreports to a server when Alva crashes

<a id="row-569"></a>
## 569. privacy-issue-14224

**主题代码：** PRIVACY-F, PRIVACY-Z

**开放代码：** 非预期邮件发送；仅元数据证据

**逐条判断：** Openfood标题处理意外验证邮件，无22评论不能确定收件地址或同意机制。

**材料可用性：** metadata_only。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 证据不足

**原文证据：**

位置 `86:134`：

> Manage unexpected validation email sent to users

<a id="row-570"></a>
## 570. privacy-issue-11993

**主题代码：** PRIVACY-I, PRIVACY-Z

**开放代码：** 附件处理政策评审；仅元数据证据

**逐条判断：** 表单附件CCCS assembly line政策审核，未见数据流或结论，不记为发生泄露。

**材料可用性：** metadata_only。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 证据不足

**原文证据：**

位置 `65:114`：

> Attachments: Policy review of CCCS' assembly line

<a id="row-571"></a>
## 571. privacy-issue-2144

**主题代码：** PRIVACY-B

**开放代码：** 隐私政策制定；仅元数据证据

**逐条判断：** Skylines标题添加Privacy Policy，未获条款及发布证据。

**材料可用性：** metadata_only。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 证据不足

**原文证据：**

位置 `65:83`：

> Add Privacy Policy

<a id="row-572"></a>
## 572. privacy-issue-18339

**主题代码：** PRIVACY-E, PRIVACY-G

**开放代码：** 域名关联数据加密；仅元数据证据

**逐条判断：** Bitwarden标题反对Equivalent Domains明文发送/存储，缺威胁与方案细节。

**材料可用性：** metadata_only。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 证据不足

**原文证据：**

位置 `65:124`：

> Equivalent Domains should not be sent/stored as plain text.

<a id="row-573"></a>
## 573. privacy-issue-14160

**主题代码：** PRIVACY-Z

**开放代码：** 隐私关联证据有限；仅元数据证据

**逐条判断：** Notebook标题仅西语翻译，GDPR只在匹配字段，不套用其他帖的暂停理由。

**材料可用性：** metadata_only。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 证据不足

**原文证据：**

位置 `65:107`：

> Translate landing page and site to Spanish

<a id="row-574"></a>
## 574. privacy-issue-4793

**主题代码：** PRIVACY-D

**开放代码：** 日志副本去标识；仅元数据证据

**逐条判断：** WSO2标题涉及原始及临时日志替换PII，未知错误方向或修复。

**材料可用性：** metadata_only。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 证据不足

**原文证据：**

位置 `65:136`：

> Replacing the PII information in original log file and a temporary file

<a id="row-575"></a>
## 575. privacy-issue-17494

**主题代码：** PRIVACY-A, PRIVACY-H

**开放代码：** Cookie动态控制；仅元数据证据

**逐条判断：** Matomo标题要enableCookies重新启用，未见调用时机与同意验证。

**材料可用性：** metadata_only。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 证据不足

**原文证据：**

位置 `65:132`：

> JS Tracker: Add possibility to turn cookies back on,  enableCookies

<a id="row-576"></a>
## 576. privacy-issue-14241

**主题代码：** PRIVACY-C

**开放代码：** 后台使用指标；仅元数据证据

**逐条判断：** Dotmesh标题使用指标，GDPR关联和具体采集范围未知。

**材料可用性：** metadata_only。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 证据不足

**原文证据：**

位置 `65:98`：

> Dotmesh usage metrics for backend

<a id="row-577"></a>
## 577. privacy-issue-18369

**主题代码：** PRIVACY-C, PRIVACY-H

**开放代码：** 第三方地图替代；仅元数据证据

**逐条判断：** Wire标题请求Google地图改OpenStreetMap，无实现或数据流证据。

**材料可用性：** metadata_only。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 证据不足

**原文证据：**

位置 `65:120`：

> Don't use Google for maps, use Open street map instead.

<a id="row-578"></a>
## 578. privacy-issue-20666

**主题代码：** PRIVACY-A, PRIVACY-I, PRIVACY-Z

**开放代码：** Cookie法规质疑；仅元数据证据

**逐条判断：** Tribler标题指违反cookie法，缺依据不能认定违法。

**材料可用性：** metadata_only。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 证据不足

**原文证据：**

位置 `65:99`：

> Tribler 7 alpha violates cookielaw

<a id="row-579"></a>
## 579. privacy-issue-21382

**主题代码：** PRIVACY-D, PRIVACY-H

**开放代码：** 电话字段必填性；仅元数据证据

**逐条判断：** OpenCart标题涉及恢复电话必填，缺44评论不推断采用理由和最终方向。

**材料可用性：** metadata_only。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 证据不足

**原文证据：**

位置 `74:111`：

> Reverting telephone field as required

<a id="row-580"></a>
## 580. privacy-issue-3873

**主题代码：** PRIVACY-E

**开放代码：** 日志自动过期；仅元数据证据

**逐条判断：** Wellcome要求ALB/CloudFront日志过期策略，期限和实现未知。

**材料可用性：** metadata_only。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 证据不足

**原文证据：**

位置 `65:124`：

> Set up auto-expiry policies for our ALB and CloudFront logs

<a id="row-581"></a>
## 581. privacy-issue-1707

**主题代码：** PRIVACY-Z

**开放代码：** 隐私关联证据有限；仅元数据证据

**逐条判断：** Fenix仅Onboarding元任务，不能从notice匹配词补写告知内容。

**材料可用性：** metadata_only。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 证据不足

**原文证据：**

位置 `65:82`：

> [Meta] Onboarding

<a id="row-582"></a>
## 582. privacy-issue-3079

**主题代码：** PRIVACY-G, PRIVACY-H

**开放代码：** Cookie安全属性；依赖升级约束；仅元数据证据

**逐条判断：** FEC扫描报告缺SameSite，标题说Django2.1升级再看，未见验证与修复。

**材料可用性：** metadata_only。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 证据不足

**原文证据：**

位置 `75:112`：

> Cookie Without SameSite Flag Detected

<a id="row-583"></a>
## 583. privacy-issue-7990

**主题代码：** PRIVACY-B, PRIVACY-H

**开放代码：** 多语言隐私告知；仅元数据证据

**逐条判断：** Tandoor要求政策本地语言，语种和完成未知。

**材料可用性：** metadata_only。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 证据不足

**原文证据：**

位置 `65:117`：

> privacy policy to get updated to the native language

<a id="row-584"></a>
## 584. privacy-issue-11552

**主题代码：** PRIVACY-C

**开放代码：** 第三方分析集成；仅元数据证据

**逐条判断：** BBC canonical Comscore跟踪，未见CCPA控制机制。

**材料可用性：** metadata_only。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 证据不足

**原文证据：**

位置 `65:106`：

> Implement Comscore tracking for Canonical

<a id="row-585"></a>
## 585. privacy-issue-1760

**主题代码：** PRIVACY-C, PRIVACY-I

**开放代码：** 跟踪风险评价分歧；仅元数据证据

**逐条判断：** Exodus标题反对一概认为tracker坏，无讨论不能定具体例外。

**材料可用性：** metadata_only。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 证据不足

**原文证据：**

位置 `65:94`：

> Not all trackers are that bad

<a id="row-586"></a>
## 586. privacy-issue-11635

**主题代码：** PRIVACY-A, PRIVACY-I

**开放代码：** 同意目的执行默认；仅元数据证据

**逐条判断：** Prebid标题提改TCF2 Purpose4默认处理，无提议细节和决定。

**材料可用性：** metadata_only。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 证据不足

**原文证据：**

位置 `65:153`：

> Proposal to change the default handling of Purpose 4 in the TCF v2.0 enforcement updates

<a id="row-587"></a>
## 587. privacy-issue-18067

**主题代码：** PRIVACY-Z

**开放代码：** 元数据隐私；仅元数据证据

**逐条判断：** InvokeAI GUI元数据隐私问题，不能猜prompt/路径等字段。

**材料可用性：** metadata_only。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 证据不足

**原文证据：**

位置 `72:104`：

> Metadata privacy issues with GUI

<a id="row-588"></a>
## 588. privacy-issue-13979

**主题代码：** PRIVACY-E, PRIVACY-G

**开放代码：** 密码明文存储；仅元数据证据

**逐条判断：** my-thai-star标题报告泄露及明文密码，wontfix标签不能说明理由或现实攻击。

**材料可用性：** metadata_only。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 证据不足

**原文证据：**

位置 `65:116`：

> Information disclousure, password plaintext storage

<a id="row-589"></a>
## 589. privacy-issue-5412

**主题代码：** PRIVACY-E

**开放代码：** 账户删除功能；仅元数据证据

**逐条判断：** Mastodon仅删户问句，缺57评论不能推联邦删除传播范围。

**材料可用性：** metadata_only。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 证据不足

**原文证据：**

位置 `65:89`：

> Delete account function?

<a id="row-590"></a>
## 590. privacy-issue-5138

**主题代码：** PRIVACY-Z

**开放代码：** 诊断日志用途；隐私关联证据有限；仅元数据证据

**逐条判断：** Openwhyd标题生产日志找防错误，匿名化只匹配词不能推已脱敏。

**材料可用性：** metadata_only。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 证据不足

**原文证据：**

位置 `65:117`：

> Safety: find and prevent errors from production logs

<a id="row-591"></a>
## 591. privacy-issue-11473

**主题代码：** PRIVACY-A, PRIVACY-C, PRIVACY-I

**开放代码：** 未同意第三方外发；仅元数据证据

**逐条判断：** Dataverse标题指未经同意向Google发用户信息，无正文不能认定具体载荷及违法。

**材料可用性：** metadata_only。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 证据不足

**原文证据：**

位置 `65:146`：

> Dataverse violates the GDPR by sending user information to Google without consent

<a id="row-592"></a>
## 592. privacy-issue-5574

**主题代码：** PRIVACY-C, PRIVACY-E

**开放代码：** 按身份记录API行为；仅元数据证据

**逐条判断：** 服装registry要求非app API按userID入库，遗忘权关联未见，不能补删除规则。

**材料可用性：** metadata_only。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 证据不足

**原文证据：**

位置 `65:121`：

> Log all non-app API requests in the database by  user ID

<a id="row-593"></a>
## 593. privacy-issue-8877

**主题代码：** PRIVACY-A, PRIVACY-H

**开放代码：** Cookie拒绝选项；仅元数据证据

**逐条判断：** Calypso标题增加Reject，元标签duplicate支持重复关闭但不证明功能实现。

**材料可用性：** metadata_only。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 重复标签，实施未知

**原文证据：**

位置 `65:100`：

> Cookies Widget: Add 'Reject' Option

<a id="row-594"></a>
## 594. privacy-issue-18441

**主题代码：** PRIVACY-C, PRIVACY-G

**开放代码：** 隐式外部请求与Referer；仅元数据证据

**逐条判断：** OpenLayers标题明确KML overlay引maps.google.com请求及Referer泄漏，缺原因及修复详情。

**材料可用性：** metadata_only。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 证据不足

**原文证据：**

位置 `145:192`：

> resulting in data leak via Referer header field

<a id="row-595"></a>
## 595. privacy-issue-11947

**主题代码：** PRIVACY-E, PRIVACY-H

**开放代码：** 删除后搜索残留；仅元数据证据

**逐条判断：** Kotatsu清历史后搜索仍见，未知缓存位置和修复。

**材料可用性：** metadata_only。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 证据不足

**原文证据：**

位置 `65:105`：

> Cleared history still shows up in search

<a id="row-596"></a>
## 596. privacy-issue-4603

**主题代码：** PRIVACY-D

**开放代码：** 匿名化转换工具；仅元数据证据

**逐条判断：** Smartnoise仅添加transformer标题，不推算法或隐私保证。

**材料可用性：** metadata_only。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 证据不足

**原文证据：**

位置 `65:94`：

> Add anonymization transformer

<a id="row-597"></a>
## 597. privacy-issue-6840

**主题代码：** PRIVACY-G, PRIVACY-H

**开放代码：** 泄露密码检查；仅元数据证据

**逐条判断：** KeePassXC提集成Pwned Passwords，不等同自身泄漏，不猜查询协议。

**材料可用性：** metadata_only。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 证据不足

**原文证据：**

位置 `65:95`：

> Integrate with Pwned Passwords

<a id="row-598"></a>
## 598. privacy-issue-18495

**主题代码：** PRIVACY-E

**开放代码：** 删除派生文件残留；仅元数据证据

**逐条判断：** WebTorrent删除任务后poster/torrent仍在，缺存储路径与处理。

**材料可用性：** metadata_only。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 证据不足

**原文证据：**

位置 `65:120`：

> Poster and torrent is not deleted upon torrent deletion

<a id="row-599"></a>
## 599. privacy-issue-9814

**主题代码：** PRIVACY-I, PRIVACY-Z

**开放代码：** 法规准备评估；仅元数据证据

**逐条判断：** Bforartists要求检查新德语GDPR相关问题，无评估结论。

**材料可用性：** metadata_only。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 证据不足

**原文证据：**

位置 `65:138`：

> Check for the new german "Datenschutz Grundverordnung" privacy law issues

<a id="row-600"></a>
## 600. privacy-issue-694

**主题代码：** PRIVACY-E

**开放代码：** 隐私工作流记录清理；仅元数据证据

**逐条判断：** Zammad DataPrivacy任务不清理，verified仅标签，未知保留内容和修复。

**材料可用性：** metadata_only。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 证据不足

**原文证据：**

位置 `65:103`：

> DataPrivacy tasks never are cleaned up

<a id="row-601"></a>
## 601. privacy-issue-12293

**主题代码：** PRIVACY-Z

**开放代码：** 浏览历史议题；隐私关联证据有限；仅元数据证据

**逐条判断：** Monika仅Internet History标题，无法区分提案、担忧或实际读取。

**材料可用性：** metadata_only。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 证据不足

**原文证据：**

位置 `65:81`：

> Internet History

<a id="row-602"></a>
## 602. privacy-issue-8030

**主题代码：** PRIVACY-Y, PRIVACY-Z

**开放代码：** 输出差异可识别性疑虑；仅元数据证据

**逐条判断：** HandBrake同设置编码文件不同被疑隐私问题，无正文不能确认指纹或元数据来源。

**材料可用性：** metadata_only。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 证据不足

**原文证据：**

位置 `65:153`：

> Encoding with the same settings leads to differences in file, maybe even privacy problem

<a id="row-603"></a>
## 603. privacy-issue-3866

**主题代码：** PRIVACY-B, PRIVACY-D, PRIVACY-H

**开放代码：** 匿名化配置文档；仅元数据证据

**逐条判断：** WSO2标题要求BPMN说明config processors需加rdbms才匿名化库记录，有Fixed标签无正文验证。

**材料可用性：** metadata_only。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 仅标签称修复

**原文证据：**

位置 `91:192`：

> users need to add rdbms under the processors in config.json to anonymize data records in the database

<a id="row-604"></a>
## 604. privacy-issue-18635

**主题代码：** PRIVACY-H, PRIVACY-Z

**开放代码：** 网站图标下载兼容；隐私关联证据有限；仅元数据证据

**逐条判断：** KeePassXC标题下载favicon某网站失败，缺讨论不能推隐私代理或外发方式。

**材料可用性：** metadata_only。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 证据不足

**原文证据：**

位置 `65:146`：

> The way currently the favicon downloading works, doesn't work with some websites.

<a id="row-605"></a>
## 605. privacy-issue-15030

**主题代码：** PRIVACY-C, PRIVACY-D, PRIVACY-F, PRIVACY-G

**开放代码：** 图像EXIF位置披露；仅元数据证据

**逐条判断：** Signal iOS标题报告未剥精确位置EXIF，缺58评论不能确认版本/发送路径/最终修复。

**材料可用性：** metadata_only。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 证据不足

**原文证据：**

位置 `81:156`：

> Signal doesn't strip EXIF from sent images, including precise location data

<a id="row-606"></a>
## 606. privacy-issue-1810

**主题代码：** PRIVACY-B, PRIVACY-H

**开放代码：** 隐私文档来源同步；仅元数据证据

**逐条判断：** Bedrock请求从legal-docs取FPN notice/terms，无同步行为验证。

**材料可用性：** metadata_only。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 证据不足

**原文证据：**

位置 `65:145`：

> Pull Firefox Private Network privacy notice and legal terms from legal-docs repo

<a id="row-607"></a>
## 607. privacy-issue-2460

**主题代码：** PRIVACY-H

**开放代码：** 自动更新自主控制；仅元数据证据

**逐条判断：** GDevelop标题要关自动更新，未见外传内容及notice联系。

**材料可用性：** metadata_only。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 证据不足

**原文证据：**

位置 `65:108`：

> Let me turn off GDevelop automatic updates.

<a id="row-608"></a>
## 608. privacy-issue-3784

**主题代码：** PRIVACY-A, PRIVACY-F, PRIVACY-I

**开放代码：** 资料编辑同意门控；仅元数据证据

**逐条判断：** Joomla标题称可未同意编辑资料而违法，缺正文不能认定法律或授权边界。

**材料可用性：** metadata_only。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 证据不足

**原文证据：**

位置 `81:128`：

> can edit user profile without providing consent

<a id="row-609"></a>
## 609. privacy-issue-11294

**主题代码：** PRIVACY-B

**开放代码：** 实例特定隐私政策；仅元数据证据

**逐条判断：** Lemmy每实例定制policy/terms需求，未见模板责任和实施。

**材料可用性：** metadata_only。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 证据不足

**原文证据：**

位置 `65:114`：

> Custom privacy policies / terms for each instance

<a id="row-610"></a>
## 610. privacy-issue-8334

**主题代码：** PRIVACY-A, PRIVACY-C, PRIVACY-H

**开放代码：** 分析与同意集成缺口；仅元数据证据

**逐条判断：** Hugo内置GA模板不联动cookie consent，stale/outdated不证修复。

**材料可用性：** metadata_only。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 证据不足

**原文证据：**

位置 `65:136`：

> Google Analytics internal template doesn't interact with cookie consent

<a id="row-611"></a>
## 611. privacy-issue-4871

**主题代码：** PRIVACY-Z

**开放代码：** 隐私关联证据有限；仅元数据证据

**逐条判断：** BIDS EEG问答标题无匿名化细节，不补临床数据处理规则。

**材料可用性：** metadata_only。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 证据不足

**原文证据：**

位置 `65:96`：

> [EEG] Some questions about BIDS

<a id="row-612"></a>
## 612. privacy-issue-12137

**主题代码：** PRIVACY-F

**开放代码：** 搜索索引控制；仅元数据证据

**逐条判断：** 交友CMS要求阻搜索扫描索引，不推具体公开个人资料及措施。

**材料可用性：** metadata_only。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 证据不足

**原文证据：**

位置 `65:105`：

> Block Search Engine scanning/indexing...

<a id="row-613"></a>
## 613. privacy-issue-9111

**主题代码：** PRIVACY-A, PRIVACY-C, PRIVACY-H

**开放代码：** Cookie限制与分析兼容；仅元数据证据

**逐条判断：** Magento Cookie Restriction开后GA不跟踪，标题不说明同意前后，Fixed2.1/2.2仅标签。

**材料可用性：** metadata_only。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 仅标签称修复

**原文证据：**

位置 `65:141`：

> Google Universal Analytics does not track when Cookie Restriction is enabled

<a id="row-614"></a>
## 614. privacy-issue-7252

**主题代码：** PRIVACY-G

**开放代码：** 加密架构选择；仅元数据证据

**逐条判断：** Padloc仅非对称加密请求，数据对象密钥分工未知。

**材料可用性：** metadata_only。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 证据不足

**原文证据：**

位置 `65:90`：

> Use asymmetric encryption

<a id="row-615"></a>
## 615. privacy-issue-6858

**主题代码：** PRIVACY-F, PRIVACY-H

**开放代码：** 保存凭据可见性；仅元数据证据

**逐条判断：** DBeaver saved passwords view功能请求，缺身份验证条件，不直接判泄漏。

**材料可用性：** metadata_only。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 证据不足

**原文证据：**

位置 `65:85`：

> Saved passwords view

<a id="row-616"></a>
## 616. privacy-issue-17718

**主题代码：** PRIVACY-B, PRIVACY-H

**开放代码：** 隐私政策与Cookie告知；仅元数据证据

**逐条判断：** Openprescribing标题建privacy页和cookie通知，无同意和发布验证。

**材料可用性：** metadata_only。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 证据不足

**原文证据：**

位置 `65:111`：

> Create "privacy" page and cookies notification

<a id="row-617"></a>
## 617. privacy-issue-3971

**主题代码：** PRIVACY-C, PRIVACY-I

**开放代码：** 第三方服务隐私评估；仅元数据证据

**逐条判断：** Trustroots评估OneSignal，不推数据售卖或最终采纳拒绝。

**材料可用性：** metadata_only。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 证据不足

**原文证据：**

位置 `65:108`：

> Research onesignal.com privacy implications

<a id="row-618"></a>
## 618. privacy-issue-14194

**主题代码：** PRIVACY-A, PRIVACY-C

**开放代码：** 分析退出控制；仅元数据证据

**逐条判断：** Riot Android标题opt out，不知现有方法或新需求结果。

**材料可用性：** metadata_only。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 证据不足

**原文证据：**

位置 `65:85`：

> opt out of analytics

<a id="row-619"></a>
## 619. privacy-issue-4804

**主题代码：** PRIVACY-G, PRIVACY-H

**开放代码：** 网络隧道覆盖；仅元数据证据

**逐条判断：** Tribler TCP through tunnel需求，未见匿名保证和实现。

**材料可用性：** metadata_only。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 证据不足

**原文证据：**

位置 `65:108`：

> Enable TCP traffic through tunnel community

<a id="row-620"></a>
## 620. privacy-issue-8038

**主题代码：** PRIVACY-F, PRIVACY-H

**开放代码：** 隐藏文件跨视图暴露；仅元数据证据

**逐条判断：** Simple File Manager隐藏目录文件出现在Recents，缺权限与修复证据。

**材料可用性：** metadata_only。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 证据不足

**原文证据：**

位置 `65:116`：

> Files from hidden folders are visible in "Recents".

<a id="row-621"></a>
## 621. privacy-issue-11971

**主题代码：** PRIVACY-F, PRIVACY-H

**开放代码：** 别名发件身份隔离；仅元数据证据

**逐条判断：** Tutanota每邮箱sender name，tested/done仅标签，没有实际测试过程。

**材料可用性：** metadata_only。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 仅标签称完成测试

**原文证据：**

位置 `65:115`：

> Provide a way to set sender name per email address

<a id="row-622"></a>
## 622. privacy-issue-5168

**主题代码：** PRIVACY-D, PRIVACY-Z

**开放代码：** 匿名化未细化；仅元数据证据

**逐条判断：** Dax只有anonymization标题，不猜影像或标识字段。

**材料可用性：** metadata_only。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 证据不足

**原文证据：**

位置 `52:78`：

> Issue title: anonymization

<a id="row-623"></a>
## 623. privacy-issue-14358

**主题代码：** PRIVACY-Z

**开放代码：** 区域部署需求；隐私关联证据有限；仅元数据证据

**逐条判断：** Cloud-builders请求发到eu.gcr.io，GDPR仅匹配元数据，不推具体个人数据跨境。

**材料可用性：** metadata_only。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 证据不足

**原文证据：**

位置 `65:94`：

> Publish builders to eu.gcr.io

<a id="row-624"></a>
## 624. privacy-issue-6881

**主题代码：** PRIVACY-E, PRIVACY-H

**开放代码：** 离线持久数据清除；仅元数据证据

**逐条判断：** Firestore请求IndexedDB清除API，未见56评论不能声明安全擦除/登出清空。

**材料可用性：** metadata_only。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 证据不足

**原文证据：**

位置 `65:120`：

> Expose API to clear offline persistence (in IndexedDB).

<a id="row-625"></a>
## 625. privacy-issue-7435

**主题代码：** PRIVACY-E

**开放代码：** 浏览数据删除覆盖；仅元数据证据

**逐条判断：** Fenix要求删浏览数据含recently closed，缺处理细节。

**材料可用性：** metadata_only。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 证据不足

**原文证据：**

位置 `65:114`：

> Delete browsing data should clear recently closed

<a id="row-626"></a>
## 626. privacy-issue-1582

**主题代码：** PRIVACY-B, PRIVACY-Z

**开放代码：** 隐私请求文案；仅元数据证据

**逐条判断：** CWA exposure framework request改措辞，未知原文和修改。

**材料可用性：** metadata_only。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 证据不足

**原文证据：**

位置 `65:108`：

> Exposure framework request - rework wording

<a id="row-627"></a>
## 627. privacy-issue-7541

**主题代码：** PRIVACY-E, PRIVACY-F, PRIVACY-H

**开放代码：** 双方消息删除权边界；仅元数据证据

**逐条判断：** Telegram标题说clear history删对方全部而非只自发，无法判断设计/bug讨论。

**材料可用性：** metadata_only。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 证据不足

**原文证据：**

位置 `65:152`：

> "Clear history" deletes all messages from contact's history, instead of the ones I sent

<a id="row-628"></a>
## 628. privacy-issue-223

**主题代码：** PRIVACY-A, PRIVACY-B, PRIVACY-H

**开放代码：** Cookie同意提示；仅元数据证据

**逐条判断：** Algomart标题要求Cookie consent prompt，无具体交互或控制证据。

**材料可用性：** metadata_only。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 证据不足

**原文证据：**

位置 `65:98`：

> Prompt consent for use of cookies

<a id="row-629"></a>
## 629. privacy-issue-1607

**主题代码：** PRIVACY-B, PRIVACY-H

**开放代码：** 隐私法律文本翻译歧义；仅元数据证据

**逐条判断：** Mastodon条款/政策译文歧义，未知语种及文本差异。

**材料可用性：** metadata_only。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 证据不足

**原文证据：**

位置 `65:115`：

> Ambiguity of Terms and Privacy Policy translations

<a id="row-630"></a>
## 630. privacy-issue-4991

**主题代码：** PRIVACY-A, PRIVACY-I, PRIVACY-Z

**开放代码：** Cookie合规议题；仅元数据证据

**逐条判断：** Compiler Explorer仅Cookie law标题，匿名化匹配词不足确定做法。

**材料可用性：** metadata_only。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 证据不足

**原文证据：**

位置 `52:75`：

> Issue title: Cookie law

<a id="row-631"></a>
## 631. privacy-issue-5490

**主题代码：** PRIVACY-E, PRIVACY-H, PRIVACY-I

**开放代码：** 遗忘权人工控制；仅元数据证据

**逐条判断：** Galaxy标题手动控制遗忘权，无角色、审批或删除范围详情。

**材料可用性：** metadata_only。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 证据不足

**原文证据：**

位置 `72:123`：

> Implement manual control over Right to be Forgotten

<a id="row-632"></a>
## 632. privacy-issue-5602

**主题代码：** PRIVACY-I, PRIVACY-Z

**开放代码：** 一般法规合规询问；仅元数据证据

**逐条判断：** Mastodon GDPR问句，缺73评论不补联邦删除难点。

**材料可用性：** metadata_only。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 证据不足

**原文证据：**

位置 `65:81`：

> GDPR Compliance?

<a id="row-633"></a>
## 633. privacy-issue-7579

**主题代码：** PRIVACY-C, PRIVACY-H

**开放代码：** 静音控制与音频发送不一致；仅元数据证据

**逐条判断：** BBB标题报告静音仍记录并传FreeSWITCH，缺44评论不能定服务端保存范围或修复。

**材料可用性：** metadata_only。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 证据不足

**原文证据：**

位置 `65:140`：

> Mute functionality still records and transmits audio to server (FreeSWITCH)

<a id="row-634"></a>
## 634. privacy-issue-7590

**主题代码：** PRIVACY-B, PRIVACY-I

**开放代码：** 隐私政策缺失；仅元数据证据

**逐条判断：** StateOfJS标题缺policy并指GDPR违规，无正文不能认定违法或补齐。

**材料可用性：** metadata_only。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 证据不足

**原文证据：**

位置 `65:106`：

> Missing privacy policy and GDPR violation

<a id="row-635"></a>
## 635. privacy-issue-9811

**主题代码：** PRIVACY-B

**开放代码：** Cookie盘点；仅元数据证据

**逐条判断：** OFN调查列cookie，未获列表和用途。

**材料可用性：** metadata_only。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 证据不足

**原文证据：**

位置 `75:115`：

> Investigate and list cookies used by OFN

<a id="row-636"></a>
## 636. privacy-issue-11281

**主题代码：** PRIVACY-E

**开放代码：** 联系人删除；仅元数据证据

**逐条判断：** Chatwoot删联系人需求，无关联聊天处理和结果。

**材料可用性：** metadata_only。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 证据不足

**原文证据：**

位置 `65:98`：

> feat: Ability to delete a contact

<a id="row-637"></a>
## 637. privacy-issue-11537

**主题代码：** PRIVACY-C, PRIVACY-D

**开放代码：** 广告标识外发最小化；仅元数据证据

**逐条判断：** PBS标题移除user.ext.eids，未知适用条件和具体监管规则。

**材料可用性：** metadata_only。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 证据不足

**原文证据：**

位置 `65:103`：

> Privacy update: removing user.ext.eids

<a id="row-638"></a>
## 638. privacy-issue-12161

**主题代码：** PRIVACY-B, PRIVACY-C

**开放代码：** 第三方分析用途质疑；仅元数据证据

**逐条判断：** TUI image editor询问为何GA追行为，无数据范围及回应。

**材料可用性：** metadata_only。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 证据不足

**原文证据：**

位置 `65:107`：

> Why are you tracking user behavior via GA?

<a id="row-639"></a>
## 639. privacy-issue-12255

**主题代码：** PRIVACY-C, PRIVACY-H

**开放代码：** 外部字体关闭控制；仅元数据证据

**逐条判断：** Asciidoctor请求HTML停Google字体，缺具体配置答案。

**材料可用性：** metadata_only。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 证据不足

**原文证据：**

位置 `65:123`：

> please provide a solution to turn off Google fonts in HTML

<a id="row-640"></a>
## 640. privacy-issue-14033

**主题代码：** PRIVACY-I, PRIVACY-Z

**开放代码：** 合规工具支持；仅元数据证据

**逐条判断：** GiveWP GDPR工具epic，不能补导出/删除等未见范围。

**材料可用性：** metadata_only。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 证据不足

**原文证据：**

位置 `65:111`：

> feat: add tools to assist with GDPR compliance

<a id="row-641"></a>
## 641. privacy-issue-18587

**主题代码：** PRIVACY-E, PRIVACY-H

**开放代码：** 图片本地托管；仅元数据证据

**逐条判断：** CodiMD请求本地文件系统存上传图，未见第三方现状或最终实现。

**材料可用性：** metadata_only。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 证据不足

**原文证据：**

位置 `65:110`：

> support local filesystem for uploading images

<a id="row-642"></a>
## 642. privacy-issue-18693

**主题代码：** PRIVACY-I, PRIVACY-Z

**开放代码：** 应用商店隐私条款争议；仅元数据证据

**逐条判断：** OneSignal Cordova标题Google Play条款违例，PII仅匹配词不能推具体采集。

**材料可用性：** metadata_only。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 证据不足

**原文证据：**

位置 `65:101`：

> Google Play Developer Term Violation

<a id="row-643"></a>
## 643. privacy-issue-20638

**主题代码：** PRIVACY-B, PRIVACY-C

**开放代码：** 分析收集透明度；仅元数据证据

**逐条判断：** StudioLibrary标题hidden analytics，未见实际行为或告知回应。

**材料可用性：** metadata_only。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 证据不足

**原文证据：**

位置 `65:99`：

> About hidden analytics collection.

<a id="row-644"></a>
## 644. privacy-issue-4038

**主题代码：** PRIVACY-H, PRIVACY-Z

**开放代码：** 隐私控制粒度；仅元数据证据

**逐条判断：** Webtrees标题更细控制，无字段/角色/默认要求细节。

**材料可用性：** metadata_only。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 证据不足

**原文证据：**

位置 `65:121`：

> Feature Request: Slightly more granular privacy controls

<a id="row-645"></a>
## 645. privacy-issue-5536

**主题代码：** PRIVACY-D

**开放代码：** 诊断日志PII盘点；仅元数据证据

**逐条判断：** Actions runner探索要清何类PII，无具体字段或清理结果。

**材料可用性：** metadata_only。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 证据不足

**原文证据：**

位置 `65:139`：

> Explore what kind of "PII" needs scrubbing from the runner diagnostic logs

<a id="row-646"></a>
## 646. privacy-issue-7605

**主题代码：** PRIVACY-A, PRIVACY-C

**开放代码：** 拒绝遥测后外连；仅元数据证据

**逐条判断：** Netlify标题拒绝后仍连遥测服务器，无载荷及原因详情。

**材料可用性：** metadata_only。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 证据不足

**原文证据：**

位置 `65:148`：

> netlify still connects to telemetry server when user does not consent to telemetry!

<a id="row-647"></a>
## 647. privacy-issue-12010

**主题代码：** PRIVACY-D, PRIVACY-H

**开放代码：** 导出元数据最小化；仅元数据证据

**逐条判断：** Darktable JXL导出所有元数据，未知设置、敏感字段及修复。

**材料可用性：** metadata_only。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 证据不足

**原文证据：**

位置 `65:91`：

> JXL exporting all metadata

<a id="row-648"></a>
## 648. privacy-issue-18972

**主题代码：** PRIVACY-C, PRIVACY-H, PRIVACY-I

**开放代码：** 静态资源本地托管；仅元数据证据

**逐条判断：** Minimal Mistakes FontAwesome本地安装需求伴GDPR动机，未见实现。

**材料可用性：** metadata_only。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 证据不足

**原文证据：**

位置 `65:129`：

> Include FontAwesome for local install on server / GDPR EU issues

<a id="row-649"></a>
## 649. privacy-issue-3074

**主题代码：** PRIVACY-D, PRIVACY-G

**开放代码：** 日志秘密排除；仅元数据证据

**逐条判断：** 税务法院要求不记录user secrets，不推已发生凭据泄漏。

**材料可用性：** metadata_only。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 证据不足

**原文证据：**

位置 `65:100`：

> Ensure user secrets are not logged.

<a id="row-650"></a>
## 650. privacy-issue-14184

**主题代码：** PRIVACY-B, PRIVACY-H

**开放代码：** 反跟踪能力文档；仅元数据证据

**逐条判断：** CanIUse请求navigator.doNotTrack及DNT支持表，不等于执行用户DNT偏好。

**材料可用性：** metadata_only。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 证据不足

**原文证据：**

位置 `65:114`：

> Add `navigator.doNotTrack` and DNT support tables

<a id="row-651"></a>
## 651. privacy-issue-5616

**主题代码：** PRIVACY-E, PRIVACY-Z

**开放代码：** 用户删除问题；仅元数据证据

**逐条判断：** Django-machina仅删用户问题标题，原因及数据关联未知。

**材料可用性：** metadata_only。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 证据不足

**原文证据：**

位置 `65:85`：

> Deleting users issue

<a id="row-652"></a>
## 652. privacy-issue-5617

**主题代码：** PRIVACY-I, PRIVACY-Z

**开放代码：** 合规扩展询问；仅元数据证据

**逐条判断：** UAA GDPR extension问句，遗忘权只匹配元数据不能补接口功能。

**材料可用性：** metadata_only。全部可用材料文本；外部链接、图片、附件未取得。

**结果与限度：** 证据不足

**原文证据：**

位置 `65:90`：

> GDPR extension for UAA ??

