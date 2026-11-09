# SATD / Privacy 与当前论文要求核对及 v10 恢复

日期：2026-11-06（北京时间）。本轮未修改论文、人工参考标签、既有运行和 Code errors 两份 codebook。

## 对照当前正文的判断

当前 `studydesign.tex` 的 ML SATD 表述是：

> We use the manually coded sample, treating a comment and its recoverable source-code context as one case.

Privacy 的表述是：

> A CODA case comprises an issue and its discussion, with linked development artifacts included when available.

因此，不能把“所有历史网页和引用百分之百恢复”作为正文没有承诺的前提，也不能把缺少的主讨论隐去。SATD 已具备全部 856 条发布注释及可查看的上下文（含多候选与明确标注的其他版本），符合 recoverable context 的材料范围。仍不能声称 856 条都在原指针处唯一定位。Privacy 已有 652 条正文与当前/历史讨论材料，符合案例构成，但 17 条主讨论尚未证明完整；若将论文理解为所有案例具有完整讨论，目前不能无条件确认。关联材料明确限定 when available，无法访问的链接不单独构成样本不符合的证明，但依赖其内容的结论不能强行判定。

不建议仅为减少缺口数删除案例或改动论文。按相同证据冻结 S1/S2/S3，在编码、人工审核和质量评估中保留证据不足状态。不能将技术预检通过当作已经完成实验或验证了论文结果。

## 本轮具体恢复

建立新目录和 profile `paper-20261106-v10`，保留 v9 不变。

1. 重试 17 条 Privacy 主讨论。公开接口仍返回删除、不可访问或数量不一致；未用更少内容替换已有历史证据。
2. 对四个评论数量疑难案例重新查询独立的公开事件缓存，未发现此前未保存的新评论。
3. 从引用的原始 7z 附件取得 53 个源码文件，共 466,501 字节；下载附件 88,478 字节。检查路径、符号链接和大小，在隔离目录解包，不运行内容。原压缩文件、逐文件 SHA-256 和完整文本保留。因引用的是可变分支且历史等同性未知，标记 partial；大文本展示仍有明确截断提示。
4. 恢复 Bromite history patch、Prebid cookieSync 文档、Magento GoogleAnalytics 模板、Flutter 插件 AndroidManifest、Prebid userId 源码的历史版本。
5. 将先前作为 Microsoft 官方外部文档恢复的两个同路径历史文件，正确关联到原 GitHub 引用。保留 Microsoft/MicrosoftDocs 原始与恢复地址、版本和证据关系，未当成当时版本完全相同。
6. 取得全部七条 SATD 疑难记录的提交 API 及文件 diff。对多位置和版本差异给出新的直接核验说明，接入 agent 可见的上下文说明；没有猜测唯一位置。

GitHub 页面 diff 的直接下载超时后，使用同一提交 SHA 的 GitHub REST 响应完成 SATD 核查。Google 外部页面本轮连接仍超时，ICO 仍返回 403。未绕过私有仓库或登录权限，也未向作者发送消息。

## 实际覆盖变化

| 指标 | v9 | v10 |
|---|---:|---:|
| SATD 发布案例 | 856 | 856 |
| SATD 可用 / 多位置 / 历史部分 | 849 / 4 / 3 | 849 / 4 / 3 |
| Privacy 案例 | 652 | 652 |
| Privacy 当前完整 / 部分主讨论 | 635 / 17 | 635 / 17 |
| GitHub 案例—链接：可用 / 部分 / 无法获取 | 437 / 54 / 51 | 437 / 62 / 43 |
| 外部案例—链接：可用 / 部分 / 无法获取 | 55 / 31 / 65 | 55 / 31 / 65 |

恢复 8 条原本不可获取的 GitHub 案例—链接记录。新增和更新内容改变 7 个 SATD 案例、8 个 Privacy 案例的实际输入；Code errors 输入未改变。所有案例 ID、顺序、分组与校准/正式分配均保持不变。链接数不是缺失案例数。

### SATD 剩余问题

- Netharn、Nalaf、scikit-learn 的差异记录均显示多个相同注释；SharedNN 的变更包含多个新增和一个移除位置，不能确定唯一来源。继续提供全部候选。
- Catalyst 与 Lightning 的返回 patch 没有发布完整目标注释；仅凭 patch 不证明所有历史文件都没有，结合此前全文匹配仍维持 historical_partial。
- Paysage patch 明确删除较短版本的注释，不含 `as needed`，不能把它当作完整发布文本的唯一定位。

这些状态是公开材料的身份/版本限制，并非未读取 7 条案例。

### Privacy 主讨论的必要澄清

AzuraCast#2303 当前接口返回 3 条、计数为 4。但原有历史 supplement 已提供 5 个不同评论 ID：575720226、575806220、575807483、575902599、576008003。当前输入包含该 supplement，不能说 agent 只看到了三条评论；也不能由历史数量更多推断完整。

Taiga#1462 保留 1 条、预期 2；Azure docs#18548 保留 3 条、预期 4；Blockframes#6556 保留 17 条、预期 24。重新查档未新增。另有历史-only 主讨论即使数量匹配，也不能验证被删除/编辑的全部内容。

## 文件及使用

- `evidence-20261106-v10/study_manifest.json`：新冻结版本，继承原分组分配。
- `evidence-20261106-v10/agent_inputs.json`：精确 agent 输入。
- `evidence-20261106-v10/evidence_audit.json`：输入变化与校验和。
- `evidence-20261106-v10-coverage.json`：逐项剩余缺口。
- `evidence-20261106-v10-recovery/`：联网尝试、SATD 提交核验、附件原件与解包源码、重新查档结果。
- `recovery-v10-collection-scripts/`：采集脚本；仅用于本次 v10 创建阶段，冻结后不要直接重跑覆盖。

新建分析前设置 `CODA_EVIDENCE_PROFILE=paper-20261106-v10`，重启后端并新建 run。已有运行保持原输入。默认未设置 profile 的旧视图不自动使用本次材料；README 与 `.env.example` 已更新到 v10。

```bash
python scripts/prepare_paper_experiment.py --bundle experiments/materials/evidence-20261106-v10
```

## 验证与实际限制

38 项相关单元测试通过。完整适配器核查通过：856 条 SATD 与 652 条 Privacy 身份、散列、上下文和证据字段可加载；人工标签仍隔离。36 个校准/正式、数据集、审核设置与重复组合的临时创建及磁盘恢复全部通过；预检记录见新 bundle 的 `preflight.json`。本轮不调用付费模型，不重新计算实验结果。

后续若要声称完整重建原研究阅读材料，仍需要能够验证的原作者讨论快照或未覆盖的档案，以及 SATD 最终抽样记录与唯一源码位置的对应关系。公开源本轮没有提供这些信息。不能承诺继续重复相同下载就一定能消除这些缺口。
