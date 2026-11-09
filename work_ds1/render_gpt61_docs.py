"""Render GPT6-1-layout codebook.md for deepseek-1 exports."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'Artifact'
ANALYST = 'deepseek-1'
DATASETS = ['CodeErrors', 'SATD', 'Privacy']


def read_jsonl(path):
    return [json.loads(line) for line in path.open(encoding='utf-8') if line.strip()]


def render(dataset):
    base = OUT / dataset / ANALYST
    book = json.loads((base / 'codebook.json').read_text(encoding='utf-8'))
    assignments = json.loads((base / 'assignments.json').read_text(encoding='utf-8'))
    codes = book['codes']
    lines = []
    if dataset == 'CodeErrors':
        lines.append(f'# {ANALYST} — Code errors 最终编码本')
        lines.append('')
        lines.append(f'本轮覆盖 **{len(assignments)} 份生成代码、{book["metadata"]["source_records"]} 条来源记录、{book["metadata"]["tasks"]} 个任务**。共有 **{len(codes)} 个可分配 code**；分组不是额外编码。允许针对独立缺陷进行多重编码，因此类别覆盖数之和可以超过案例数。')
        lines.append('')
        lines.append('这是单个 AI 编码者的逐条完整阅读与归纳，未使用原始人工类别作为模板，也未经过人工审核。所有案例均已编码，没有未决案例。完整方法与限制见 `METHOD.md`。')
        lines.append('')
        lines.append('## 类别一览')
        lines.append('')
        lines.append('|Code|类别|英文名称|覆盖案例数|')
        lines.append('|---|---|---|---:|')
        for c in codes:
            lines.append(f'|{c["id"]}|{c["name_zh"]}|{c["name"]}|{c["case_count"]}|')
        lines.append('')
        lines.append('## 使用规则')
        lines.append('')
        lines.append('以交付代码中的可观察失败机制为单位，不推断模型的心理原因。优先选择能准确解释证据的具体类别；只有存在不同证据支持的不同缺陷时才多重编码。题目约束优先，参考实现用于理解而非要求相同算法。')
        lines.append('')
        for c in codes:
            lines.append(f'## {c["id"]} {c["name_zh"]}')
            lines.append('')
            lines.append(f'**{c["name"]}**')
            lines.append('')
            lines.append(c['definition'])
            lines.append('')
            lines.append(f'- 纳入：{c["inclusion"]}')
            lines.append(f'- 排除与边界：{c["exclusion"]}')
            lines.append(f'- 支持：{c["case_count"]} 份代码。完整列表见 `codebook.json` 的 `supporting_case_ids`。')
            ev = c.get('representative_evidence')
            if ev:
                lines.append(f'- 代表案例：`{ev["case_id"]}`，字符区间 {ev["start_char"]}:{ev["end_char"]}。')
                lines.append('')
                lines.append('```text')
                lines.append(ev['quote'][:1200])
                lines.append('```')
                lines.append('')
                lines.append(ev['interpretation'])
            lines.append('')
        lines.append('## 随附文件')
        lines.append('')
        lines.append('`taxonomy.json` 是分类树；`results.json` 是 metadata/results 风格结果包；`codebook.json` 保存完整定义、支持案例和代表证据；`assignments.json`/`.csv` 保存逐例编码；`METHOD.md` 记录范围与方法。')
    else:
        lines.append(f'# {dataset} — {ANALYST}')
        lines.append('')
        lines.append(f'{len(assignments)} artifacts; {len(codes)} codes; {book["metadata"]["assignment_count"]} artifact–code assignments.')
        lines.append('')
        lines.append(book['metadata']['method'])
        lines.append('')
        lines.append('Every supplied artifact has an assignment. Codes describe the observed work, concern, or evidence status; they do not establish that a defect was reproduced. Refer to `assignments.json` for individual reasoning, qualifications, source references and evidence.')
        lines.append('')
        lines.append('## Scope')
        lines.append('')
        for limit in book['metadata']['limits']:
            lines.append(f'- {limit}')
        lines.append('')
        lines.append(book['metadata']['independence'])
        lines.append('')
        lines.append('## Codebook')
        lines.append('')
        lines.append('| Code | Name | Artifacts |')
        lines.append('|---|---|---:|')
        for c in codes:
            lines.append(f'| {c["code_id"]} | {c["name"]} | {c["artifact_count"]} |')
        lines.append('')
        by_id = {a['case_id']: a for a in assignments}
        for c in codes:
            lines.append(f'## {c["code_id"]} — {c["name"]}')
            lines.append('')
            lines.append(c['definition'])
            lines.append('')
            lines.append(f'**Include:** {c["inclusion_criteria"]}')
            lines.append('')
            lines.append(f'**Exclude:** {c["exclusion_criteria"]}')
            lines.append('')
            examples = c['supporting_cases'][:2]
            if examples:
                lines.append('**Examples:**')
                lines.append('')
                for artifact_id in examples:
                    a = by_id.get(artifact_id)
                    if not a:
                        continue
                    quote = a['evidence'][0]['quote'] if a.get('evidence') else ''
                    quote = quote.replace('\n', ' ')[:220]
                    lines.append(f'- `{artifact_id}`: {a["rationale"]} Evidence: `{quote}`')
                lines.append('')
    (base / 'codebook.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')


def main():
    for dataset in DATASETS:
        render(dataset)
        print('rendered', dataset)


if __name__ == '__main__':
    main()
