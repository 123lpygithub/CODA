# Code errors — two preserved codebooks

两份结果分别保存，互不覆盖。`GPT6-1` 已从修改前归档完整恢复；本次新生成的结果改记为 `GPT6-2`。

| 结果 | artifact | code | artifact–code 分配 | 说明 |
|---|---:|---:|---:|---|
| [GPT6-1](GPT6-1/codebook.md) | 557 | 17 | 729 | 上一份结果，文件原样恢复 |
| [GPT6-2](GPT6-2/codebook.md) | 557 | 13 | 706 | 本次重新阅读材料生成的结果 |

- 第一份的说明见 [GPT6-1_README.md](GPT6-1_README.md)，原始共享材料和审计文件保留在根目录 `shared/`、`coverage_audit.json`、`validation.json`。
- 第二份的说明见 [GPT6-2/README.md](GPT6-2/README.md)，其材料、观察、映射和审计记录单独保存在 `GPT6-2/shared/` 和 `GPT6-2/coverage_audit.json`，不与第一份混用。
- 两份的案例编号可对应，但类别编号各自独立，不能把相同 C 编号视为同一类别。
- GPT6-2 的案例 729 保留题目范围冲突所导致的条件性判断；两份结果的不同解释和原有证据分别保留。
- 这两个名称是结果标签，不表示两位独立编码员或经过验证的 API 型号。第二份不声称盲法独立实验。

`restoration_audit.json` 记录归档位置和恢复校验。`SHA256SUMS` 覆盖当前两份结果。旧版构建脚本仅用于第一份，可能重写根目录说明或清单；请勿以它生成第二份。
