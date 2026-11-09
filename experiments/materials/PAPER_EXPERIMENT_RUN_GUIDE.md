# 当前论文实验：数据准备、启动与检查

**更新：** 最新恢复材料为 `paper-20261105-recovered`、冻结版本 v8，详见
[本轮恢复记录](DATA_RECOVERY_CONTINUATION_20261105.md)。下面的 v7 指南及已创建
运行保持有效；启动新 v8 实验时，将 profile 改为 `paper-20261105-recovered`，
所有 `--bundle` 和 `--study-manifest` 路径改为 `evidence-20261105-v8`，并使用新的
运行和监测状态文件。不要把 v7 的已有运行改绑到新材料。

此指南对应当前 `studydesign.tex`，使用 `paper-20261105-ready` 和冻结输入
`evidence-20261105-v7/`。工作目录为 `FSE27-CODA/CODA/`。
数据准备和运行创建不调用模型，也不生成评分。

## 1. 当前可以开展什么

| 数据集 | 全量案例 | 校准 pilot | 正式 formal |
| --- | ---: | ---: | ---: |
| Code errors | 557 | 113 | 444 |
| ML SATD | 856 | 169 | 687 |
| Privacy | 652 | 132 | 520 |

每个阶段分别执行三个数据集 × 三种审核设置 × 两次运行，即 18 次；两个阶段
共 36 次。S1=automatic，S2=selective，S3=full。校准运行不会把已生成的编码本
传给正式运行。Code errors 按 HumanEval task 分组，其余按仓库分组；组不跨阶段。
同一数据集／阶段的三种设置共享案例、顺序和证据快照。

SATD 有 849 条唯一定位、4 条多位置候选、3 条相关历史版本。849 条中有 5 条
使用已核验的直接父版本；输入保留版本说明。Privacy 有 635 条当前完整讨论，
16 条历史档案讨论、1 条当前部分讨论。所有案例都保留；缺失证据按论文的
unresolved / unassessable 处理，不用人工标签补造正文。

Privacy 有 7 条 issue 正文确实为空，其中 2 条也没有评论。这属于检索到空正文，
不等于下载失败；仅凭标题不能支持需要正文才能判断的结论。关联文件／讨论也
可能不可用。完整逐项缺口见 `evidence-20261105-ready-coverage.json`。

## 2. 离线检查

```bash
python scripts/prepare_paper_experiment.py
```

脚本核对冻结输入文件的 SHA-256、全部案例和分组、两个阶段的证据哈希、可引用
字段、人工标签隔离，以及实际模型配置。只读取材料，不请求模型。

进一步检查全部 36 个条件能否创建、从磁盘恢复，以及恢复后的材料是否一致：

```bash
python scripts/prepare_paper_experiment.py --check-run-creation \
  --output /tmp/coda-paper-preflight.json
```

这会使用临时运行目录，完成后删除临时运行；不会把预检用的审核者标识写入正式
实验。最新预检记录在 `evidence-20261105-v7/preflight-final.json`；
`preflight.json` 保留前一轮记录。

模型敏感性实验要求每个数据集抽取 50 条完整案例。正式池中没有已知材料缺口
的候选数为 Code errors 444、SATD 682、Privacy 412，足够抽样。这里也排除明确
关联文件缺失的案例，以及没有正文和评论的 Privacy 案例；主实验仍保留这些
案例。这些数量只证明抽样池足够，不是质量评分。

## 3. 配置并启动后端

在 `.env` 中保留实际提供商和密钥，增加：

```dotenv
CODA_EVIDENCE_PROFILE=paper-20261105-ready
CODA_RUNS_ROOT=runs/paper
CODA_LLM_RETRY_TIMEOUTS_FOREVER=true
```

论文模型分工是 Coder A=`gpt-6.1-sol`；Coder B、Context、Induction、Comparison、
Validation=`gpt-5.6-sol`。用 `scripts/check_llm_config.py` 核对角色覆盖项；
模型名称和有效密钥仍需要实际服务商支持，离线检查不能证明接口可用。

```bash
python scripts/run_local.py
```

访问 http://127.0.0.1:8003。`run_local.py` 加载 `.env`。使用下面的监测命令时，
后端必须从本目录启动，并读取上述 profile。仅在创建脚本进程中设置环境变量，
不会改变已经启动的后端。冻结实验开始后不要再次修改对应采集目录；补充材料
应另建 evidence profile、冻结版本和新运行。

## 4. 创建并执行一个匹配实验条件

下面直接通过后端创建第一个 Code errors 校准条件，并定时检查、恢复处理：

```bash
python scripts/watch_coda_run.py \
  --dataset llm_code_error_semantic --review-mode automatic \
  --study-manifest experiments/materials/evidence-20261105-v7/study_manifest.json \
  --study-phase pilot --replicate-index 1 \
  --comparison-block-id coda-evidence-20261105-v7:pilot:llm_code_error_semantic:r1 \
  --language en --interval 30 \
  --state runs/paper/monitors/pilot-code-s1-r1.json
```

监测状态文件固定记录 run ID。重启监测时复用同一个 `--state`，避免重复创建。
传输超时和暂时性连接错误按现有监测规则重试；人工审核、上下文请求和非传输
错误需要实际处理，不会被重试伪装为已接受。完成后导出 RQ1 材料和 RQ2 日志指标。

其他条件使用相同命令，替换数据集、阶段、配置、replicate 和状态文件；
comparison block 对同一数据集／阶段／重复下的 S1/S2/S3 保持相同。

如果需要先创建、后从前端或监测脚本启动，可以使用：

```bash
python scripts/prepare_paper_experiment.py --create-run \
  --dataset llm_code_error_semantic --phase pilot \
  --review-mode automatic --replicate 1 --runs-root runs/paper
```

该命令只创建条件，并输出对应 `--run-id` 监测命令；执行前核对角色模型与论文
一致。不要为同一条件反复创建新 run；保存输出的 run ID。

本轮已创建的 SATD 校准 S1 第一次运行是 `run-60deee5af9d7`，包含完整的 169 条
校准材料，保存在 `runs/paper/run-60deee5af9d7/`。状态为 `not_started`，尚未调用模型。
后端按本指南配置启动后，可以直接继续这条运行：

```bash
python scripts/watch_coda_run.py --run-id run-60deee5af9d7 \
  --state runs/paper/monitors/run-60deee5af9d7.json --language en
```

## 5. S2 / S3 的人工任务

将 `--review-mode` 设为 `selective` 或 `full`，并提供实际已分配的
`--participant-id`。六位正式参与者按论文规定分配不同数据集的 S2/S3 任务，
两个配置的材料和执行条件保持一致。不要用预检标识代替真实参与者。

监测遇到 Initial / Triggered / Final Review 或待补上下文时让出执行。
研究者在前端审阅定义、证据和影响，提交决定与理由，再用同一状态文件继续。
S2/S3 的人工操作、主动用时、等待与返工必须实际记录。

当前按已确认的项目要求使用单 artifact 迭代 batch，并跳过这类 batch 的 10%
未触发抽查。**当前论文仍写按 batch 向上取整抽查，因此这一项不是逐字一致。**
本轮保持论文不动，预检报告记录这项已知例外，不能在报告实验时声称执行了
向上取整抽查。初始化归纳分批与迭代 batch 是不同设置。

## 6. 从运行结果得到 RQ1 / RQ2

1. 完成 18 个校准运行。两位独立研究者和五个候选评价模型按当前论文的量规
   评同一批编码本及抽样分配。计算各数据集／维度一致性，再冻结最终三个评价模型。
2. 完成 18 个正式运行。输出编码本、逐案例分配、证据、未解决事项和审核日志；
   保持每次运行及其输入哈希可追踪。
3. RQ1：使用选定评价模型独立评分，分别汇总清晰度、类别边界、有意义覆盖和
   逐分配证据支持。缺失必要材料的分配记 unassessable，不能按 0 分或完全支持处理。
4. RQ2：从实际日志汇总模型使用量、运行时间、人工审核量及人工时间等论文所需指标。
   输入准备和离线运行创建都不能提供这些实验结果。

已有评价和汇总命令包括 `export_evaluation.py`、`export_evaluator_targets.py`、
`run_llm_evaluator.py`、`summarize_evaluator_calibration.py`、
`summarize_rq1_scores.py`。执行各命令的 `--help` 查看当前必需的材料路径。
以新的运行输出重新评分；原有论文表格和旧结果不会因本次数据恢复自动更新。
