"""Explicit, auditable corrections found during the final semantic re-read.

This script edits only analyst-authored decision files. It never classifies by
keyword: each changed row is listed with its rule and the rationale used while
reading the full frozen comment/issue text.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / 'work_ds1'
DEC = WORK / 'decisions'


def read_jsonl(path):
    return [json.loads(line) for line in path.open(encoding='utf-8') if line.strip()]


def write_jsonl(path, rows):
    with path.open('w', encoding='utf-8') as target:
        for row in rows:
            target.write(json.dumps(row, ensure_ascii=False) + '\n')


def set_satd(row, codes, open_codes, memo):
    row['code_ids'] = codes
    row['open_codes'] = open_codes
    row['memo'] = memo


def main():
    satd = read_jsonl(DEC / 'satd_redo.jsonl')
    by_row = {row['row']: row for row in satd}

    # --- SATD: align explanatory prose and low-information TODOs with definitions.
    # Pure explanations do not assert a debt action; SATD-12 is for documentation
    # that should be added or corrected.  Keep the object in the memo and flag it
    # as a negative/limit case rather than inventing a mechanism.
    explanation_rows = {
        56: '循环移位是正确相位的必要条件；这是原理解释，不是要求补文档。',
        106: '注释说明代码适用于 EpisodicReplayBuffer；这是适用范围解释，不是待补文档。',
        130: '解释 Python 3 中 list 调用的转换作用，没有待偿还动作。',
        142: '说明该处理对 SysEx 事件正确性是必要的，没有待偿还动作。',
        143: '说明 TestWikiCorpus 类是测试所需，属于测试前提解释，不是待写文档。',
        144: '说明该对象供命令补全与帮助使用，属于必要性解释。',
        169: '说明 squeeze 用于得到一维张量，没有待偿还动作。',
        171: '解释条件用于保护 cast；虽含防御性条件，但注释本身是必要性解释。',
        175: '解释 pre-activation 变体缺少 batch norm，故需要该处理。',
        176: '说明该调用用于更新 loss history，没有待偿还动作。',
        364: '说明该代码目前被 async_fit 依赖，属于必要性解释。',
        728: '说明单内容词分支何时发生，属于分支条件解释。',
        855: '说明重新缓存是为了获得 mozci 版本，属于流程解释。',
    }
    for n, memo in explanation_rows.items():
        row = by_row[n]
        # 171's SATD-03 defensive boundary is retained; only its documentation
        # code is removed.
        codes = [c for c in row['code_ids'] if c != 'SATD-12']
        codes.append('SATD-17')
        set_satd(row, codes, ['解释性注释，未提出待偿还动作', *row['open_codes']], memo + ' 按“解释性注释”保留为 SATD-17，而非归入补文档。')

    # Low-information object/action fragments: cannot determine a mechanism.
    low_info = {
        371: ('待修改', 'TODO 仅写 to be modified，没有可辨识的修改对象或机制。'),
        436: ('accurate Value', 'TODO 仅写 accurate Value，无法确定要修正哪个值或何种正确性风险。'),
        587: ('list', 'TODO 仅写 list，无法确定对象是字段、容器还是序列化表示。'),
        607: ('模型精度', 'TODO 仅写 Model Precision，无法确定是精度评估、数值精度还是模型配置。'),
        653: ('refine', 'TODO 仅写 refine，无法确定重构、实现还是文档动作。'),
        704: ('deep 9 的处理', 'TODO 仅写 something if deep 9，无法确定条件、动作或机制。'),
    }
    for n, (open_code, memo) in low_info.items():
        row = by_row[n]
        set_satd(row, ['SATD-17'], [open_code], memo)

    # Explicit capability addition, not an algorithmic/data-assumption issue.
    set_satd(by_row[44], ['SATD-04'], ['Hebrew-to-Aramaic 转换器'],
             'TODO 明确要求新增 Hebrew-to-Aramaic 转换器；这是缺失能力补全，不是算法或数据假设问题。')

    # Regex refinement is a quality improvement with a named object; it is not
    # evidence of a temporary workaround or hard-coded hack.
    set_satd(by_row[301], ['SATD-02'], ['改进正则表达式'],
             'TODO 明确要求改进该处用于切分 choice 的正则；这是具体解析正确性改进，不是临时绕行。')

    # "better way to generate scope names" is structural/design improvement,
    # not a hard-coded workaround.
    set_satd(by_row[412], ['SATD-01'], ['scope 命名生成方式'],
             'TODO 要求设计更好的 scope 名称生成方式，属命名与结构设计重构。')

    # run-on/split describes an unimplemented module capability rather than a
    # demonstrated defect.
    set_satd(by_row[689], ['SATD-04'], ['run-on 与 split 模块'],
             '模块顶部 TODO 指出 run-on 与 split 能力尚未实现；注释没有说明现有输出错误或复现，按功能补全而非已证缺陷。')

    write_jsonl(DEC / 'satd_redo.jsonl', satd)

    # --- Privacy: keep PRIVACY-Y only where the full material weakens, rebuts,
    # or materially limits the original privacy claim.
    privacy = read_jsonl(DEC / 'privacy_redo.jsonl')
    pby = {row['row']: row for row in privacy}
    remove_y = {
        159: '维护者仅表示无法定位问题并关闭，没有对原判断给出可核对的反驳；属于报告未证实，不足以单独支持“反例”。',
        524: '材料只说明因 GDPR 暂停翻译功能，没有证据削弱或修正某个具体隐私判断；属于治理约束，不应仅凭“未外传”推测加 Y。',
        602: '评论只是追问是否指编码时间等元数据，未确认也无材料反驳风险；属于风险未定而非反例。',
    }
    for n, reason in remove_y.items():
        row = pby[n]
        row['code_ids'] = [c for c in row['code_ids'] if c != 'PRIVACY-Y']
        if row['code_ids'] == ['PRIVACY-Z']:
            pass
        row['memo'] = row['memo'] + ' ' + reason
    write_jsonl(DEC / 'privacy_redo.jsonl', privacy)

    print('SATD changed rows:', sorted(set(explanation_rows) | set(low_info) | {44, 301, 412, 689}))
    print('Privacy Y removals:', sorted(remove_y))
    print('SATD rows:', len(satd), 'Privacy rows:', len(privacy))


if __name__ == '__main__':
    main()
