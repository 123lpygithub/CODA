# Code errors：GPT6-1 全量归纳编码结果

本目录保留第一轮结果 **GPT6-1**。第二轮曾接触第一轮结果，已按要求删除其编码本、逐例分配、类别定义、复查材料及比较文档；生成脚本只生成第一轮。

## 结果和覆盖范围

|项目|数量|
|---|---:|
|原始 Error ID 记录|687|
|不同生成解答案例（artifact）|557|
|编程任务|150|
|已记录分析和处理状态的 artifact|557|
|已有至少一个 code 的 artifact|557|
|明确未决的 artifact|0|
|可分配 code|17|
|导航分组|4|
|多标签分配总数|729|

从 [GPT6-1/codebook.md](GPT6-1/codebook.md) 开始阅读。[coverage_audit.json](coverage_audit.json) 可复核全量覆盖；[HOW_FORMAT_AND_COVERAGE.md](HOW_FORMAT_AND_COVERAGE.md) 解释与 HOW 的格式关系。

“覆盖 557 个 artifact”指全部都有原文、分析说明和处理状态。全部 557 个已编码。393、729 两个初次未决案例已通过补充源码诊断和官方测试分别归入 C08、C14。17 个 code 在 4 个导航分组下，HOW 树包含 21 个非 Root 节点。

## 材料和分析方式

原数据包含 687 条记录。以 `(task_id, model, incorrect_code)` 分组，得到 557 份生成解答，以每组最小 Error ID 作为 case_id，保留全部 source_ids。相同代码来自不同源模型时仍为不同案例。按任务升序整理材料，对每个案例保存具体观察，再比较可重复的失败机制、定义边界并分配 code。人工 category 和人工 taxonomy 没有作为归纳模板；题目、生成代码和参考实现保留。参考实现用于理解要求，不要求生成代码采用同一算法。

这是助手会话中的分析产物，尚未经过人工审核；没有配套的独立模型 API 运行日志。`GPT6-1` 是结果标识，原始生成参数、token 和费用没有采集。它不能直接替代 CODA 多 agent 系统的正式运行结果。

共享的 29 个执行诊断和全量语法检查用于辅助复核。它们不构成全部 557 个案例的动态测试。另外对 393、729 两个初次未决案例进行了补充核查，取得官方 HumanEval 原始测试并执行原码；最终结果已应用这两项补充决策，初次观察与 map 保留用于追溯。详见 [DATA_NOTES.md](DATA_NOTES.md)。

## 文件

|文件|用途|
|---|---|
|`GPT6-1/codebook.md`|可读编码本：17 个类别、定义、纳入/排除、代表案例。|
|`GPT6-1/codebook.json` / `.csv`|完整定义、稳定 ID、所有支持案例。|
|`GPT6-1/taxonomy.json`|HOW 节点结构的分类树：Root → 导航分组 → code。|
|`GPT6-1/results.json`|沿用 HOW TnT-LLM 的 metadata/results 结构，附加多标签和未决状态。|
|`GPT6-1/assignments.json` / `.csv`|逐例分配、判断说明、原文证据、来源 ID；多标签分析应使用此文件。|
|`GPT6-1/metadata.json`|范围、方法、阅读顺序与数据哈希。|
|`shared/corpus.json` / `shared/cases/`|557 份完整材料，移除人工类别字段。|
|`shared/observations-1.tsv` / `shared/round1-map.txt`|557 个案例的初次观察和编码决策。|
|`shared/pending_case_resolutions.json`|393、729 的补充编码与证据；生成时覆盖这两个初始未决状态。|
|`shared/pending_case_verification.json` / `shared/humaneval-evidence/`|两项原码执行结果及官方测试来源。|
|`shared/code_definitions.tsv`|17 个第一轮类别的源定义。|
|`shared/reading-*.txt`|初次阅读使用的材料编排；原文以 corpus/cases 为准。|
|`shared/witness_results.json` / `shared/syntax_audit.json`|诊断执行和全量语法检查。|
|`shared/how-format/`|HOW 公开示例、输出实现、来源和许可。|
|`validation.json` / `coverage_audit.json` / `SHA256SUMS`|汇总、详细覆盖检查和文件散列。|

## 复核

在 CODA 目录运行 Python 3.10+：

```bash
python Artifact/shared/build_artifacts.py
python Artifact/shared/audit_outputs.py
```

这些脚本使用已保存的定义、第一轮 map 和两项补充决策生成文件、校验全部材料，不重新进行模型归纳。需要重新执行已有诊断时可运行 `python Artifact/shared/verify_witnesses.py`，之后再运行以上两个命令。两项补充案例的专门诊断可用 `python Artifact/shared/verify_pending_cases.py` 复跑。所有程序仅使用标准库。
