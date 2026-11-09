# 第二轮缺口恢复记录

本轮以 v7 为基线继续获取真实材料。新采集使用
`CODA_EVIDENCE_PROFILE=paper-20261105-recovered`，冻结为
`evidence-20261105-v8/`。没有修改原始人工标签、论文正文或旧冻结输入。

## 实际恢复结果

| 材料 | v7 | v8 |
| --- | --- | --- |
| GitHub 案例—链接记录 | 435 可用、13 部分、94 无法获取 | **437 可用、30 部分、75 无法获取** |
| 选定外部案例—链接记录 | 45 可用、25 部分、81 无法获取 | **53 可用、27 部分、71 无法获取** |
| Privacy 主讨论 | 635 当前完整、17 部分 | 635 当前完整、17 部分 |
| SATD 上下文 | 849 唯一、4 歧义、3 相关历史版本 | 数量不变；新增提交差异核查记录 |

全部 557/856/652 个案例、校准／正式分组和顺序保持不变。新增证据改变了
32 个 Privacy 案例的 agent 输入；Code errors 和 SATD 输入没有改变。

### 删除文件：18 条引用恢复为历史部分证据

通过同一仓库、同一路径的 Git 提交历史，恢复 DNN、eLabFTW、AMP、YOURLS、
docker-phantomjs、phpMyAdmin、Microsoft 365、Pi-hole、WICG、Signal iOS、
Tribler、VS Code 和 Jitsi 等文件。一个历史文件可能对应多个行号引用。

保留实际提交、原始链接、来源文件 SHA-256、提交历史响应和原引用行范围。
优先使用 raw 内容；必要时使用 GitHub REST base64 内容并验证 Git blob SHA-1，
或严格校验路径和提交的结构化 blob 原始行。原分支在案例发生时指向哪个提交
无法确认，所以这些材料保持 `partial`，不能据此声称某补救方案已部署或生效。
若原引用行范围不存在，不将其移动到猜测位置。

### 关联 issue：两个完整恢复，一个恢复 PR 材料

- `brave/brave-ios#1358`：由历史部分证据升级为可获取的当前完整讨论。
- `pichillilorenzo/flutter_inappwebview#1304`：同上。
- `matrix-org/matrix-react-sdk/issues/821`：核实其实际为 PR，补回正文、可用评论、
  review 和 patch 等材料；仍有缺失，保持部分证据。

### Bugzilla：8 个引用获取结构化原始评论

取得 bug 1568885、1056934、1807544、1081385、1807447、1807594、1812442、
1807122 的元数据和公开评论，共 **98 条公开评论**。核对 bug ID、评论所属 bug、
唯一评论 ID 和公开序号连续性。其中 7 个公开评论序列连续，1 个存在序号缺口，
继续标为部分。公开接口不保证涵盖已删除或私有评论，也不意味着原 GitHub 讨论
完整。原始 JSON 响应保留在 `archive_raw/`。

### DSpace：4 个失效 Jira 引用找到官方导入记录

| 原 Jira 编号 | 官方 GitHub 导入 | 本轮取得材料 |
| --- | --- | --- |
| DS-3653 | DSpace/DSpace#7002 | 原始导入正文、24 条公开评论 |
| DS-2081 | DSpace/DSpace#5447 | 原始导入正文；评论仍未取回 |
| DS-955 | DSpace/DSpace#4328 | 原始导入正文；评论仍未取回 |
| DS-2904 | DSpace/DSpace#6260 | 原始导入正文；评论仍未取回 |

匹配条件是官方仓库、相同 Jira key、明确的 Imported from JIRA 声明和原地址
反向链接。未用相似标题猜测迁移身份。导入完整性、Jira 附件和编辑历史未获验证，
因此四个记录均保持部分证据。重试失败不覆盖已有更丰富材料。

### Mozilla Jira：14 个同步关系单独保留

主 GitHub issue 正文明确声明与特定 Jira Task 同步。已保存这些声明和来源，
但没有将已有的 GitHub 内容重复计算成独立 Jira 内容，也没有降低对应 Jira
缺口数量。Jira 页面返回的通用应用壳不作为 issue 正文。

### 其他外部文档

补取部分 MDN、Microsoft 文档及 GDPR 页面正文。重定向页面保持部分状态，
除非能够核实它就是原引用所需材料。HTML 可见文本明确说明提取方式，不冒充
原始 Markdown。Google 部分主机当前连接失败，ICO 返回 403；保留失败记录。

## 本轮没有消除的限制

SATD 四条多位置注释已检查指定提交的真实文件 patch；仍有多个相同注释被同时
引入或移动，公开抽样行没有行号，不能唯一归属。三条相关历史版本仍不能替代
原案例的指定版本。

Privacy 16 条历史档案主讨论和 AzuraCast#2303 的当前评论计数问题未消除。
AzuraCast 当前仍只能取回 3 条评论；已存在的历史附录含 5 个评论 ID，其中两个
不在当前返回中。历史评论保留，但不能据此声称当前报告的 4 条全部已确认。

7 条主 issue 正文原本为空，其中 2 条无评论。未根据标题或人工类别生成正文。
旧仓库删除、私有／不可访问资源、二进制 7z 附件、剩余外部文档和部分迁移评论
仍是缺口。不能把历史恢复后的 `partial` 数量上升理解成数据质量退步：它们多数
来自原先完全无法获取的链接。

## 文件与运行方式

- 冻结输入：`evidence-20261105-v8/study_manifest.json` 和 `agent_inputs.json`。
- 完整缺口：`evidence-20261105-recovered-coverage.json`。
- 链接变更：`evidence-20261105-linked_artifacts-recovery-changes.json`。
- 外部变更：`evidence-20261105-external_artifacts-recovery-changes.json`。
- 逐项历史尝试：`linked_artifacts_20261105_recovered/file_history_recovery_audit.json`。
- 同步声明：相同目录的 `sync_relations/`。

```bash
python scripts/prepare_paper_experiment.py \
  --bundle experiments/materials/evidence-20261105-v8
```

前端使用新材料时，将 `.env` 的 profile 设为 `paper-20261105-recovered`，重启后端
并创建新运行。已创建的 v7 运行仍绑定 v7，不应更换其材料或冒用 v8 的来源。
需要继续 v7 运行时，使用对应的 `paper-20261105-ready` profile。

实验生成和评分未执行；这些文件记录材料获取、冻结与离线预检。

最终验证：307 项后端测试通过；v8 全部 36 个实验条件的创建／磁盘恢复通过，
且材料、顺序和设置均与冻结清单一致。v7 和 v8 分别使用对应 profile 验证通过。
预检结果在 `evidence-20261105-v8/preflight.json`；旧实验结果未重新计算。
