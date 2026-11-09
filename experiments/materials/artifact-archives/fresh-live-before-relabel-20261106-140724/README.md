# Code errors: fresh full-corpus inductive codebook

本次结果从 Code errors 原始材料重新分析生成：**557 个 artifact、150 个任务、687 条原始记录，归纳为 13 个 code**。每个 artifact 都有编码，共 706 条 artifact–code 分配；134 个 artifact 有多个不同机制的编码。这里只提供一份新的 `GPT6-1` 结果。

先阅读 [完整 codebook](GPT6-1/codebook.md)，逐例核查使用 [assignments.csv](GPT6-1/assignments.csv) 或包含原文证据位置的 [assignments.json](GPT6-1/assignments.json)。

| 文件 | 内容 |
|---|---|
| `GPT6-1/codebook.md` | 13 个类别的定义、纳入/排除规则、中文名称、代表案例和数量 |
| `GPT6-1/codebook.json` / `.csv` | 完整编码本及全部支持案例 ID |
| `GPT6-1/assignments.json` / `.csv` | 全部 557 个 artifact 的编码、理由、原始记录对应关系及解释范围 |
| `GPT6-1/taxonomy.json` | 仿照 HOW 公开材料的分类树格式 |
| `GPT6-1/results.json` | 仿照 HOW 的 `metadata/results` 格式，保留完整材料和多标签扩展 |
| `GPT6-1/observations.jsonl` | 归并前的逐例观察 |
| `GPT6-1/reading_log.json` | 15 组阅读视图与全部案例的对应关系 |
| `GPT6-1/memos.md` | 合并理由、类别边界和有歧义案例的处理 |
| `GPT6-1/diagnostics.json` | 30 个输入、26 个案例的原程序运行核查 |
| `GPT6-1/syntax_audit.json` | 全部程序的语法检查 |
| `GPT6-1/method.json` | 实际执行方法和来源信息 |
| `shared/corpus.json` | 本次使用的完整材料，不含原人工类别 |
| `shared/input/` | 完整分批阅读材料及输入清单 |
| `shared/mapping.tsv` | 人工逐项编写的案例—类别映射，不是关键词分类规则 |
| `coverage_audit.json` | 覆盖、证据、ID 一致性检查结果 |

采用“完整阅读 → 逐例观察 → 跨案例归并 → 全量分配 → 边界复核和定点运行验证”的方式。没有预设类别数量，没有把题目名作为类别，也没有按人工 codebook 的类别数凑数。同一个任务中的公共题目与参考实现只展示一次，相同可执行结构通过引用定位，原文完整保存。

**覆盖说明：**687 条原记录按 `(task_id, model, incorrect_code)` 合为 557 个 artifact，所有原始 ID 都保留。案例 729 已编码，但其排序问题取决于题目中存在冲突的输入范围假设，不能当作无条件成立的错误。它在逐例结果中明确标注为 `coded_conditional_on_specification`，没有被跳过或虚构结论。

**来源说明：**这是当前助手的一次源码重读分析，不是 CODA 应用的一次运行，也不是两位独立编码员的结果。会话中的已有知识无法被真正清除，因此不声称盲法独立实验。旧 codebook 没有作为本次分类输入，原人工 category 字段未进入分析材料。`GPT6-1` 是用户使用的结果标签，不作为实际 API 模型型号的证明。

HOW 格式对应关系见 [HOW_FORMAT.md](HOW_FORMAT.md)。旧 Artifact 在替换前完整归档；位置记于 `archive_manifest.json`。本次没有提交或推送 Git，也没有修改论文或程序实现。
