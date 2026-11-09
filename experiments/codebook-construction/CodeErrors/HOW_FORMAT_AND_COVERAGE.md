# GPT6-1 与 HOW 输出形式及全量覆盖核查

## 结论

GPT6-1 的分类树使用 HOW 公开材料的节点格式，逐材料结果沿用其中 TnT-LLM 的核心结构，并扩展了多标签、未决状态和来源记录。它不是两种 HOW 方法的全部输出逐字段完全相同，也不意味着执行了 HOW 的生成方法。

全部 557 个 artifact 均有记录：557 个均已编码、无未决；687 条原始记录全部可追溯。结构覆盖检查不能证明每个语义判断正确，也不能单独证明类别体系已充分。

## 核查依据

公开材料：[Zenodo 10.5281/zenodo.21388470](https://zenodo.org/records/21388470)。实际下载核查的 `SETaxo-Replication.zip` 为 22,114,688 bytes，MD5 为 `c6eb67c7e17b3e0552b2b8868555c5ce`，与归档记录一致。

核查路径包括：

- `examples/tnt-llm.json` 和 `examples/climb.json`：生成的分类树示例。
- `methods/tnt-llm/src/taxonomy_generator/output.py`：TnT-LLM 输出实现。
- `methods/CLIMB/src/taxonomy_generator/output.py` 与 `taxonomy.py`：CLIMB 输出包、树转换及逐材料分配实现。
- `ARTIFACT_ABSTRACT.md`：说明公开包包含示例分类树，没有发布原实验的原始运行和论文结果表。

因此这里依据真实公开的示例和输出程序比较格式，不能声称逐一比较过 HOW 所有原实验的生成结果。相关上游文件和来源保存在 `shared/how-format/`。

## 一样和不同的部分

|项目|HOW 公开实现/示例|GPT6-1|判断|
|---|---|---|---|
|树节点|`category`、`description`、`layer`、`children`|相同四个字段，Root 为 layer 0|节点结构相同。|
|类别组织|父类别和子类别构成层级|4 个导航父节点，17 个可分配 code|层级形式相同；父节点在本结果中只作导航。|
|输出包|`metadata` 与 `results`|相同；metadata 含 taxonomy_structure|结构沿用。|
|TnT-LLM 逐条结果|id、document、summary、category、category_description|保留全部五项，另加 categories、code_ids、status、source_error_ids|核心字段一致，存在扩展。|
|CLIMB 逐条结果|由 taxonomy.py 构造，含 id、document、category、category_description；该路径的 document 截到 200 字符，没有 summary 字段|完整材料文本并含 summary|不能说与 CLIMB 逐字段完全相同。|
|summary 含义|TnT-LLM 的材料摘要|本结果存编码判断说明|字段名一致，语义用途不同。|
|单例分类|公开格式使用 category 字符串|categories/code_ids 可含多个标签，category 仅取首个作为兼容显示|只读 category 会丢失多标签；首个标签不代表唯一根因。|
|处理状态|不能从示例推出统一的未决处理约定|全部 557 项为 coded；393、729 保留由初次未决到完成编码的补充记录|状态和决策追溯属于扩展。|
|定义和边界|树保留类别名和描述|codebook.json 另含纳入、排除、支持案例和代表证据|比树形展示提供更多审阅信息。|
|模型运行元数据|程序支持保存模型、温度、seed、调用与资源信息|会话分析，无独立 API 运行记录；未采集字段为 null|保存形式相似，实验来源不同。|

`codebook.md` 是方便阅读的扩充说明。与 HOW 的树形分类体系最接近的文件是 `GPT6-1/taxonomy.json`；与 TnT-LLM 的逐材料输出最接近的是 `GPT6-1/results.json`。进行完整多标签统计应使用 `assignments.json`。

## 覆盖如何计算

重新读取原始 `llm_code_error_semantic.json`，按 `(task_id, model, incorrect_code)` 复算分组，而不是只相信结果文件中写的 557。

|核查项|结果|
|---|---:|
|源记录|687|
|复算得到的 artifact|557|
|assignments.json 唯一案例|557|
|results.json 唯一案例|557|
|原文 cases 文件|557|
|初次观察与 round1-map|各 557 条|
|缺失/多余/重复案例|均为 0|
|任务|150|
|已编码|557 / 557，100%|
|未决|0|
|有 1 个 code|403|
|有 2 个 code|137|
|有 3 个 code|16|
|有 4 个 code|1|
|有 0 个 code（未决）|0|
|分配总数|729|

每个原始 ID 仅归入一个 artifact。全部 source_ids 与 687 条原始记录逐项对应；题目、源模型、生成代码、参考代码、任务和来源文件均逐字段核对。每个类别的 supporting_case_ids 与逐例分配反向一致，所有证据原文和哈希一致。17 个叶子 code 加 4 个导航节点，合计 21 个非 Root 节点；不能直接把这个数与只计叶子的 17 混用。

393 根据有效输入反例归入 C08；729 根据官方混合长度测试、题目的长度优先规则和两个参考实现归入 C14。题目中的等长表述冲突仍在 scope_note 中保留。补充判断、执行结果和官方测试存于 shared，其他 555 个案例记录经变更前散列确认完全一致。

## 删除与保留边界

按本次要求删除第二轮结果目录、第二轮 map、第二轮定义、复查展示文件、专用复查脚本以及两轮比较文档。生成器和校验器只处理第一轮。共享材料中的真实执行诊断保留并标明是后续复核；它们不作为第二份编码本，本次按要求只补充 393、729 两个原未决案例，未改变类别定义或其余分配。

详细机器检查结果见 `coverage_audit.json`。这些检查证明来源追溯和输出结构完整；尚不构成人工质量评分、独立编码员一致性或正式 CODA 实验结果。
