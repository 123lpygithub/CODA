# 第三轮原始材料恢复（v9）

本轮继续按原研究的材料范围获取真实正文、评论与关联源码，冻结为
`evidence-20261105-v9/`，profile 为 `paper-20261105-v9`。
v8、原始人工标签、已有运行和实验结果均未覆盖。

## 与原研究的对应关系

Privacy 原研究（https://doi.org/10.1007/s10664-025-10742-x）阅读完整 issue，并在必要时查阅其链接的提交、其他讨论和政策材料。因此本轮继续恢复明确引用的材料，而不是从标题、关闭状态或人工编码推测讨论内容。当前页面、历史文件和官方迁移副本分别标明，均不保证等同于作者 2023 年采集时的页面。

ML SATD 原研究（https://doi.org/10.1145/3540250.3549088）使用抽样注释并查看源码上下文。公开表格提供仓库、路径和提交，但没有唯一行号。本轮重试三个历史部分案例的指定提交，均取得真实文件和 Software Heritage 提交元数据；完整发布注释在这三个文件中仍无匹配，因而没有升级证据状态。提交 diff 的本轮重试超时。四条多位置注释也保持歧义状态。

## 实际变化

| 材料 | v8 | v9 |
| --- | --- | --- |
| GitHub 案例—链接记录 | 437 可用、30 部分、75 无法获取 | 437 可用、54 部分、51 无法获取 |
| 外部案例—链接记录 | 53 可用、27 部分、71 无法获取 | 55 可用、31 部分、65 无法获取 |
| Privacy 主讨论 | 635 当前完整、17 部分 | 不变 |
| SATD 上下文 | 849 可用、4 歧义、3 历史部分 | 不变 |

这些链接数不是缺失案例数，同一案例可能包含多个链接。新增材料改变了 21 个 Privacy 案例的 agent 输入。557 个 Code errors、856 个 SATD、652 个 Privacy 案例的编号、顺序、分组和校准／正式分配保持不变。

### DSpace 官方迁移讨论

- DS-2081 → DSpace/DSpace#5447：补回 6 条评论。
- DS-955 → DSpace/DSpace#4328：补回 5 条评论。
- DS-2904 → DSpace/DSpace#6260：补回 5 条评论。
- DS-3653 → DSpace/DSpace#7002：重新确认已有 24 条评论。

核对原 Jira key、原地址反向链接、Imported from JIRA 声明、GitHub issue 编号、评论所属 issue、唯一 ID 和接口报告数量。新增 16 条评论；迁移前附件、编辑历史和导入完整性未确认，因此仍为部分证据。

### GitHub 历史文件

24 条原本无法获取的引用恢复为历史部分证据，涉及 cookie 提示脚本、BBC 同意横幅、Nextcloud 通知、AMP、Application Insights、PKP 授权逻辑等。按同一仓库、同一路径查询提交历史，从该提交或其明确父提交读取原文；保留提交 SHA、完整正文及 SHA-256。不把原行号移动到猜测位置，不把历史代码解释为已部署结果。

### 官方文档

- MDN Array.from 与 dns.resolve：原引用地址正文可用。
- MDN File System Access API：取得跳转后的 File System API 页面，保持部分。
- Azure Monitor 数据位置：恢复官方 MicrosoftDocs/azure-docs 原路径历史 Markdown，未使用跳转后的产品概览替代。
- Face 实时视频分析：恢复官方源文件的历史 Markdown。
- W3C Feature Policy：原页面明确指向 Permissions Policy，取得后继规范；它不是原规范历史版本，保持部分。

## 剩余缺口

Privacy 的 16 条主讨论仅有历史档案，AzuraCast#2303 当前评论计数仍不一致；本轮没有改变这些记录。51 条 GitHub 引用和 65 条外部引用仍无法取得可用内容。失败包括删除／不可访问仓库、Google 连接超时、ICO 403、Mozilla Jira 404／附件 403、Chromium 页面没有可读正文，以及未处理的二进制附件。部分 GitHub 请求在本轮后期受到 API 配额限制。

`available` 表示可获取范围内的材料通过相应检查，不表示历史版本等同、所有解释正确或原论文实验已复现。

## 文件和复用

- `evidence-20261105-v9/study_manifest.json`：冻结编号、分配及内容散列。
- `evidence-20261105-v9/agent_inputs.json`：确切 agent 输入。
- `evidence-20261105-v9/evidence_audit.json`：与 v8 的输入变化。
- `evidence-20261105-v9-coverage.json`：完整剩余缺口。
- `evidence-20261105-v9-changes.json`：逐链接新增内容和来源。
- `recovery-v9-collection-scripts/`：本轮采集脚本存档，保留当次路径；不建议直接重跑覆盖已冻结目录。
- `dataset/personal_data_protection_github/source/linked_artifacts_20261105_v9/`：原始响应、SHA-256、逐案例关联材料及本轮各项 audit。

新建运行时选择 `CODA_EVIDENCE_PROFILE=paper-20261105-v9` 并重启后端；现有运行仍应使用创建时的材料版本。本轮没有启动付费模型运行或重新计算实验结果。

## 验证

41 项相关单元测试通过；适配器完成全量身份、散列和关联快照检查；84 份保留的 archive_raw 响应通过 SHA-256 复核。36 个实验条件全部通过创建／磁盘恢复预检；结果保存在 `evidence-20261105-v9/preflight.json`。
