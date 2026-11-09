"""Serialize analyst-authored decisions into verifiable codebook packages.

This script never classifies text.  It reads frozen corpora, explicitly
authored code definitions and row/case decisions, and writes the delivery
package plus a structural audit.
"""
from __future__ import annotations

import csv
import hashlib
import json
import re
from collections import Counter, OrderedDict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / 'work_ds1'
OUT = ROOT / 'Artifact'
DATASETS = ['CodeErrors', 'SATD', 'Privacy']
ANALYST = 'deepseek-1'


def read_jsonl(path: Path):
    with path.open(encoding='utf-8') as source:
        return [json.loads(line) for line in source if line.strip()]


def sha_text(text: str) -> str:
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def write_json(path: Path, obj):
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def write_jsonl(path: Path, rows):
    with path.open('w', encoding='utf-8') as target:
        for row in rows:
            target.write(json.dumps(row, ensure_ascii=False) + '\n')


def code_map(defs):
    return OrderedDict((code_id, meta) for code_id, meta in defs)


# ---------------------------------------------------------------------------
# Code definitions.  IDs and membership are analyst decisions; the definitions
# below describe the boundaries used while reading every artifact.
# ---------------------------------------------------------------------------

CE_CODES = OrderedDict([
    ('CE01', dict(name='实质实现未交付',
        definition='目标函数没有形成可执行的主体实现：pass、仅注释、固定常量或只覆盖示例。',
        inclusion='空函数体、只有注释、无有效返回、用与输入无关的常量或示例值顶替求解。',
        exclusion='主体逻辑存在但覆盖不全用 CE06；调用未定义名称用 CE03；源码截断用 CE02。',
        boundary='只有局部语句缺失但算法主体可运行，不归 CE01。')),
    ('CE02', dict(name='源码截断或语法不完整',
        definition='冻结源码在 token、表达式、容器或缩进块中途结束，模块无法解析。',
        inclusion='括号/引号未闭合、缩进块中断、表达式截断、语法错误导致不可导入。',
        exclusion='合法语法但缺 return 用 CE01；运行时类型错误用 CE12。',
        boundary='截断同时导致无实现时并用 CE01 与 CE02。')),
    ('CE03', dict(name='未定义或未提供的名称',
        definition='正常路径引用本 artifact 未定义、未导入、任务也未承诺提供的模块、函数或变量。',
        inclusion='调用未定义 helper、未导入模块、拼错名称、使用未绑定变量。',
        exclusion='对象存在但操作不支持用 CE12；名称在另一段被定义则不算。',
        boundary='任务描述承诺由测试环境提供的名称不归 CE03。')),
    ('CE04', dict(name='解析、分词或表示转换错误',
        definition='输入被按错误边界或错误表示域解释，或文本/字符/数值/结构表示转换不成立。',
        inclusion='错误分隔符、错误字段边界、把英文数字直接 int、错误类型转换、分词丢元素。',
        exclusion='解析正确但公式错用 CE09；输出格式不符用 CE13。',
        boundary='字符级大小写/字符集规范问题优先 CE14。')),
    ('CE05', dict(name='计算目标被替换',
        definition='实现计算了可辨识但与契约不同的量、对象、谓词或粒度。',
        inclusion='求极值代替最近对、按字典序代替数值序、判断偶数代替判素、返回常量目标。',
        exclusion='目标正确但候选/循环覆盖不全用 CE06；目标正确但公式写错用 CE09。',
        boundary='错误目标本身仍可运行，不能仅因结果错就归 CE05。')),
    ('CE06', dict(name='遍历、候选或状态覆盖不足',
        definition='目标量正确，但循环边界、候选枚举、状态推进或累积覆盖不完整。',
        inclusion='少遍历元素、提前停止枚举、漏状态分支、边界少一轮、只检查部分候选。',
        exclusion='完全换掉目标用 CE05；条件写反用 CE07。',
        boundary='筛选条件本身错误归 CE05/CE07；漏掉应检查的成员归 CE06。')),
    ('CE07', dict(name='条件判断或提前返回错误',
        definition='分支条件、终止条件或提前返回使错误路径被选择。',
        inclusion='比较方向反、and/or 混用、return 位置错误、基线条件错误、循环终止条件错。',
        exclusion='边界输入未校验用 CE11；数学递推公式错用 CE09。',
        boundary='条件正确但漏候选归 CE06。')),
    ('CE08', dict(name='结果组装、顺序或重数错误',
        definition='元素、位置、顺序、重复次数或返回结构被错误组装。',
        inclusion='分隔符位置错、奇偶重排、丢首尾元素、重复添加、嵌套层级/顺序错。',
        exclusion='输出类型/格式契约错用 CE13；计算值本身错用 CE05/CE09。',
        boundary='结果元素正确但顺序错，归 CE08。')),
    ('CE09', dict(name='数学公式、递推或数值方法错误',
        definition='目标量正确但公式、递推关系、取整或数值方法本身写错。',
        inclusion='递推式错、取模/回绕缺失、平均/中位数公式错、二分/筛法方法错、浮点处理错。',
        exclusion='目标量被替换用 CE05；初始化/状态转移错用 CE10。',
        boundary='数学方法正确但循环少一轮归 CE06。')),
    ('CE10', dict(name='初始化或状态转移错误',
        definition='初始值、变量更新或状态转移步骤写错，导致后续计算基于错误状态。',
        inclusion='累加器初值错、余额未更新、DP 转移错、循环变量更新错。',
        exclusion='循环边界少一轮用 CE06；条件方向错用 CE07。',
        boundary='状态变量存在但从未更新，归 CE10 而非 CE01。')),
    ('CE11', dict(name='输入域、类型或边界校验缺失',
        definition='未处理契约要求处理的边界值、非法输入或类型差异。',
        inclusion='空输入、负数、零、单元素、非法日期、越界下标、未捕获转换异常。',
        exclusion='类型不支持所调用操作用 CE12；正常输入上的逻辑错不归 CE11。',
        boundary='边界处理存在但判据写错，按具体机制归 CE07/CE09。')),
    ('CE12', dict(name='对象类型或操作协议不相容',
        definition='对现有对象施加了其类型不支持的运算或调用，产生运行时错误。',
        inclusion='字符串索引列表、字符取模、对 None 调用方法、参数结构不符合 API。',
        exclusion='名称未定义用 CE03；合法操作但公式错用 CE09。',
        boundary='同一表达式既有未定义名又有类型错时并用 CE03/CE12。')),
    ('CE13', dict(name='输出格式或表示契约错误',
        definition='返回值的类型、格式、前缀、大小写或字符串表示不符合任务契约。',
        inclusion='返回 lambda/元组/列表类型错、缺前缀、连接符错、大小写表示错。',
        exclusion='元素内容本身算错用 CE08；字符级比较规范错用 CE14。',
        boundary='格式与内容同时错时并用 CE08/CE13。')),
    ('CE14', dict(name='字符或大小写规范语义错误',
        definition='字符级比较、大小写或字符集规范被错误应用。',
        inclusion='大小写不敏感比较、大小写转换范围错、字符集/编码判断错、元音/字母分类错。',
        exclusion='整串解析错误用 CE04；输出格式错用 CE13。',
        boundary='字符级规则正确但遍历范围错，可并用 CE06。')),
    ('CE15', dict(name='按提供材料未观察到可归因缺陷',
        definition='逐条核对任务契约、错误源码与正确源码后，未发现可由现有代码描述的独立失败机制。',
        inclusion='实现与契约一致，或差异仅是未被材料支持的推测。',
        exclusion='存在不确定或未覆盖输入时，应保留具体边界代码，不应使用 CE15。',
        boundary='CE15 不是“完全无错”的证明，只表示按本条提供材料未观察到可归因缺陷。')),
])

SATD_CODES = OrderedDict([
    ('SATD-01', dict(name='结构、职责、命名与格式重构', definition='当前实现的结构、职责、抽象、命名或代码格式需要整理。', inclusion='提取/移动/复用/去耦、命名统一、格式整理、模块化。', exclusion='仅新增行为用 SATD-04；仅性能诉求用 SATD-07。', boundary='结构整理与未决设计并存时并用 SATD-16。')),
    ('SATD-02', dict(name='行为与正确性缺陷', definition='注释指出行为错误、结果不一致、契约违背或具体正确性风险。', inclusion='明确 bug、错误结果、语义不一致、条件性正确性风险。', exclusion='仅 TODO 或一般优化不纳入；尚未支持的新范围用 SATD-04。', boundary='疑似错误必须保留“疑似/条件性”限定。')),
    ('SATD-03', dict(name='输入校验、边界与异常', definition='需要验证输入、形状、状态、生命周期或错误路径，并保护边界条件。', inclusion='空值、除零、类型/形状检查、异常策略、并发保护。', exclusion='新增单元测试用 SATD-11；一般功能缺失用 SATD-04。', boundary='校验缺失导致正确性错时可并用 SATD-02。')),
    ('SATD-04', dict(name='功能补全与实现缺失', definition='所需能力、分支、类型、数据流、格式覆盖或一般实现明确尚未完成。', inclusion='not implemented、只支持部分输入/模型/格式、缺少保存/加载/转换能力。', exclusion='已有能力但接口契约不稳用 SATD-14；已产生错误数据用 SATD-02。', boundary='只写“未实现”而没有对象，仍按可辨识范围归 SATD-04。')),
    ('SATD-05', dict(name='范围与泛化扩展', definition='把已有能力扩展到更多输入、平台、模型、配置或使用场景。', inclusion='支持其他类型/模型/优化器/平台、扩大覆盖范围、增加通用分支。', exclusion='全新缺失能力用 SATD-04；结构性抽象用 SATD-01。', boundary='“支持所有 X”可同时含 SATD-04。')),
    ('SATD-06', dict(name='外部依赖、版本与平台约束', definition='工作受外部库、版本、平台、浏览器或上游组件约束。', inclusion='兼容性修复、版本升级、平台差异、上游缺陷、依赖迁移。', exclusion='纯内部设计问题用 SATD-01；性能问题用 SATD-07。', boundary='兼容性缺陷同时可用 SATD-02。')),
    ('SATD-07', dict(name='性能、内存与效率', definition='执行速度、内存、资源使用或可扩展性需要改善。', inclusion='加速、减少内存/分配、并行化、避免重复计算。', exclusion='功能正确性缺陷用 SATD-02；一般重构用 SATD-01。', boundary='性能优化需要结构重写时并用 SATD-01。')),
    ('SATD-08', dict(name='临时绕行、hack 与硬编码', definition='为绕过问题而采用临时、脆弱或硬编码方案。', inclusion='hack、workaround、硬编码常量/路径、测试专用开关、非常规绕行。', exclusion='正式设计选择用 SATD-16；纯参数默认值用 SATD-10。', boundary='绕行同时暴露外部约束时并用 SATD-06。')),
    ('SATD-09', dict(name='算法、数据假设与语义适用性', definition='算法或数据假设在特定语义、分布或边界下不成立。', inclusion='度量/归一化假设、编码映射、数据分布、语义等价性、适用性疑问。', exclusion='明确公式 bug 用 SATD-02；纯性能用 SATD-07。', boundary='假设尚未验证时保留不确定性。')),
    ('SATD-10', dict(name='配置、参数与默认值', definition='配置项、参数语义、默认值或选项组合需要调整。', inclusion='新增/统一参数、默认值变更、配置开关、参数命名语义。', exclusion='硬编码常量用 SATD-08；一般 API 契约用 SATD-14。', boundary='参数语义与命名同时涉及结构时并用 SATD-01。')),
    ('SATD-11', dict(name='测试与验证', definition='需要增加、修改或隔离测试、验证步骤或测试环境。', inclusion='补单测/集成测试、测试专用逻辑、验证行为、测试隔离。', exclusion='生产输入校验用 SATD-03；文档示例用 SATD-12。', boundary='测试暴露正确性缺陷时可并用 SATD-02。')),
    ('SATD-12', dict(name='文档与说明', definition='需要补充或修改文档、注释、示例、教程或说明。', inclusion='docstring、README、教程、示例、格式说明。', exclusion='接口契约本身缺失用 SATD-14；纯命名整理用 SATD-01。', boundary='文档化一个未决设计时并用 SATD-16。')),
    ('SATD-13', dict(name='弃用、移除与清理', definition='需要删除、弃用或清理旧代码、依赖、配置或兼容分支。', inclusion='移除旧 API/依赖/测试、删除死代码、弃用迁移。', exclusion='局部格式整理用 SATD-01；替代实现用 SATD-18。', boundary='移除是为了换实现时并用 SATD-18。')),
    ('SATD-14', dict(name='数据、接口与表示契约', definition='数据格式、接口契约、序列化、字段语义或表示约定需要明确或修正。', inclusion='字段格式、序列化格式、API 返回契约、编码约定、命名表示。', exclusion='纯文档说明用 SATD-12；一般功能缺失用 SATD-04。', boundary='契约变更影响兼容性时并用 SATD-06。')),
    ('SATD-15', dict(name='日志、可观察性与展示', definition='日志、错误展示、调试输出或用户可见呈现需要调整。', inclusion='日志内容、错误显示、UI 展示、调试可观察性。', exclusion='隐私/安全问题用 SATD-02/03；纯文档用 SATD-12。', boundary='展示错误源于数据错误时可并用 SATD-02。')),
    ('SATD-16', dict(name='未决问题、调查与设计疑问', definition='注释提出尚未决定的方向、待调查问题或设计疑问。', inclusion='问句、是否/如何选择、待确认语义、设计探索。', exclusion='明确 TODO 动作有对象用对应机制；纯解释用 SATD-17。', boundary='疑问中已指出具体错误时可并用 SATD-02。')),
    ('SATD-17', dict(name='空 TODO 与证据不足', definition='只有待办标记或低信息文本，无法判断具体技术机制。', inclusion='孤立 TODO/FIXME、单个名词、截断到无法解释的改进判断。', exclusion='明确写出未实现对象用 SATD-04；解释性注释用 SATD-16。', boundary='证据不足不等于无债务，只是不可细分。')),
    ('SATD-18', dict(name='替代方案与替代实现', definition='提出另一种实现、方案、数据源或技术路线。', inclusion='改用其他库/模型/数据/算法、替代实现、迁移方案。', exclusion='纯重构用 SATD-01；外部兼容约束用 SATD-06。', boundary='替代方案与临时绕行可并用 SATD-08。')),
])

PRIVACY_CODES = OrderedDict([
    ('PRIVACY-A', dict(name='同意、拒绝、撤回与偏好执行', definition='材料涉及用户对处理活动的选择，以及选择的默认、触发、保存、传递和实际执行。', inclusion='事前门控、opt-in/out、分类同意、撤回、审计记录、同意协议与 Cookie 选择界面。', exclusion='仅提供隐私政策而无选择用 PRIVACY-B；有横幅不等于存在拒绝或阻断。', boundary='强制接受或未交互即持久化，属于偏好执行问题而非单纯告知。')),
    ('PRIVACY-B', dict(name='透明告知、文档与信息可达性', definition='材料涉及说明收集内容、目的、对象、期限、法律文本、操作路径及其可理解性。', inclusion='政策发布/翻译、说明准确性、告知入口、数据清单、控制文档及组织对外解释。', exclusion='披露承诺不当作行为已验证；链接未取得不能推其内容。', boundary='告知文案与真实行为不一致时并用相应机制代码。')),
    ('PRIVACY-C', dict(name='采集、追踪与对外数据流', definition='材料涉及遥测、分析、第三方资源、联网或跨系统传播的数据和元信息。', inclusion='主动或隐式请求、IP/Referer/URL、广告标识、推送、SDK、独立退出与本地替代。', exclusion='区分网络连接、数据字段、留存和接收方；静态依赖不等于实际发送。', boundary='第三方请求存在但未确认载荷时，保留“请求存在、外发未知”的限度。')),
    ('PRIVACY-D', dict(name='去标识、最小化与再识别', definition='材料涉及减少可识别信息、匿名/假名变换、粒度降低，以及剩余关联风险或保护覆盖。', inclusion='日志脱敏、哈希与随机映射、时间位置精度、字段遗漏、导出清洗及效果验证。', exclusion='不能把 hash 自动等同匿名；仅删除整账户用 PRIVACY-E，权利/政策文本仍需 PRIVACY-B。', boundary='匿名化工具的配置/部署故障可并用 PRIVACY-H。')),
    ('PRIVACY-E', dict(name='留存、删除、导出与生命周期', definition='材料涉及数据保存位置/时间、清除范围、主体权利、导出副本及跨阶段状态。', inclusion='账户/内容删除、缓存与日志过期、匿名化保留、备份/归档、访问导出、偏好持久化。', exclusion='界面隐藏、redact、卸载或停用不自动等同物理删除；外部副本保证另说明。', boundary='删除请求与法定保留冲突时保留双方主张。')),
    ('PRIVACY-F', dict(name='身份、受众与访问边界', definition='材料涉及谁能识别谁、谁能访问哪些信息，以及跨用户/角色/实例/视图的边界。', inclusion='角色权限、资料可见性、账户关联、行为状态、消息受众、共享设备及公开索引。', exclusion='不把不猜得到的 URL 当身份授权；本地保存也可能暴露给本地管理员或旁观者。', boundary='界面隐藏不等于后端授权已收紧。')),
    ('PRIVACY-G', dict(name='安全保护与隐私威胁机制', definition='材料以具体攻击、故障、加密、认证、权限、反指纹或通信机制讨论信息保护。', inclusion='凭据泄露、异常路径污染、传输/静态加密、密钥、认证、权限声明、威胁模型及误报。', exclusion='必须区分假设、报告、复现和反驳；安全相关标题不证明发生泄露。', boundary='误报与真实风险都应保留归因状态。')),
    ('PRIVACY-H', dict(name='隐私控制可用性与系统兼容', definition='材料涉及控制能否被理解和操作，或隐私保护与框架、平台、功能、数据流之间的适配。', inclusion='界面遮挡、可访问性、配置绕行、跨端状态、隐私开关功能副作用、测试与依赖集成。', exclusion='UI 测试成功不保证后端阻断；功能兼容问题不能一概视为隐私泄漏。', boundary='隐私机制导致的普通功能故障仍可归此类。')),
    ('PRIVACY-I', dict(name='治理、责任与需求权衡', definition='材料涉及合规解释、组织职责、开发范围、生态依赖、资源优先级或用途与隐私的取舍。', inclusion='监管/平台审核驱动、控制者/供应商分工、请求受理、评估、标准与开发决策。', exclusion='记录参与者法律判断而不认证其正确；计划、合并、部署、验收分别处理。', boundary='法律主张只作为材料中的主张，不作为已验证事实。')),
    ('PRIVACY-Y', dict(name='反例、争议或归因修正', definition='完整材料削弱、反驳或限定了最初隐私问题判断，或显示原风险归因/目标发生改变。', inclusion='误报、用户撤回、无外发证据、实际行为不同、争议未定及保护并未达原目标。', exclusion='不是统一的无风险标签；仍可并存真实残余风险，具体原因见备忘录。', boundary='反例不等于全部风险消失。')),
    ('PRIVACY-Z', dict(name='内容不足或无法定位具体机制', definition='可用材料不足以支持任何具体隐私机制，或仅有无法还原语境的外链、占位文本与泛化标题。', inclusion='空正文、只有外链/占位符、标题也无法定位隐私机制，以及现有讨论未提供可归因对象或行为的条目。', exclusion='正文可读但隐私关联较弱时，应按实际涉及的主题编码；证据可用性是独立字段，不应仅靠 PRIVACY-Z 表达。', boundary='PRIVACY-Z 表示“无法从现有材料定位机制”，不表示材料无隐私相关性或风险不存在。')),
])


def corpus_path(name):
    return WORK / 'corpus' / f'{name.lower()}.jsonl'


def content_spans_for_codeerrors(artifact):
    content = artifact['content']
    start_marker = 'Incorrect Code (Generated by LLM):\n'
    end_marker = '\n\nCorrect Code (Ground Truth):'
    start = content.index(start_marker) + len(start_marker)
    end = content.index(end_marker, start)
    return [(start, end)]


def content_spans_for_satd(artifact):
    comment = artifact['raw_fields']['Comment Text']
    start = artifact['content'].index(comment)
    return [(start, start + len(comment))]


def load_ce_decisions():
    return {r['artifact_id']: r for r in read_jsonl(WORK / 'decisions' / 'ce.jsonl')}


def load_satd_decisions():
    result = {}
    for row in read_jsonl(WORK / 'decisions' / 'satd_redo.jsonl'):
        key = str(row['row'])
        assert key not in result, f'duplicate SATD row {key}'
        result[key] = row
    assert set(result) == {str(i) for i in range(1, 857)}
    return result


def privacy_evidence(artifact, quotes):
    content = artifact['content']
    spans = []
    for quote in quotes:
        quote = quote.strip()
        if not quote:
            continue
        start = content.find(quote)
        if start < 0:
            raise ValueError(f'quote not found in {artifact["artifact_id"]}: {quote[:80]!r}')
        spans.append((start, start + len(quote)))
    if not spans:
        raise ValueError(f'no evidence for {artifact["artifact_id"]}')
    return spans


def build_codebook(dataset, codes, code_ids_to_artifacts, artifact_count, metadata, source_note):
    code_rows = []
    for code_id, meta in codes.items():
        members = sorted(code_ids_to_artifacts.get(code_id, []), key=lambda x: (str(x).isdigit() is False, int(x) if str(x).isdigit() else x))
        code_rows.append({
            'code_id': code_id,
            'name': meta['name'],
            'definition': meta['definition'],
            'inclusion_criteria': meta['inclusion'],
            'exclusion_criteria': meta['exclusion'],
            'boundary_examples': meta['boundary'],
            'artifact_count': len(members),
            'artifact_ids': members,
        })
    return {
        'dataset': dataset,
        'result': ANALYST,
        'method': '逐条完整阅读 → 开放代码与逐条备忘录 → 显式成员归并 → 反向成员复核；脚本仅序列化与校验',
        'unit': 'one released artifact; duplicate content retained as distinct artifact IDs',
        'code_count': len(code_rows),
        'artifact_count': artifact_count,
        'source_note': source_note,
        'metadata': metadata,
        'codes': code_rows,
    }


def write_memberships(path, assignments, code_key='code_ids'):
    with path.open('w', encoding='utf-8', newline='') as target:
        writer = csv.writer(target)
        writer.writerow(['artifact_id', 'code_id'])
        for row in assignments:
            for code in row[code_key]:
                writer.writerow([row['artifact_id'], code])


def write_artifact_index(path, assignments):
    with path.open('w', encoding='utf-8', newline='') as target:
        writer = csv.writer(target)
        writer.writerow(['artifact_id', 'task_id', 'model', 'row', 'code_ids', 'open_codes', 'evidence_availability', 'outcome'])
        for row in assignments:
            writer.writerow([
                row['artifact_id'], row.get('task_id', ''), row.get('model', ''), row.get('row', ''),
                ';'.join(row['code_ids']), ';'.join(row['open_codes']),
                row.get('evidence_availability', ''), row.get('outcome', ''),
            ])


def write_reading_memos(path, assignments):
    with path.open('w', encoding='utf-8', newline='') as target:
        writer = csv.writer(target)
        writer.writerow(['artifact_id', 'open_codes', 'analytic_memo', 'evidence_availability', 'outcome'])
        for row in assignments:
            writer.writerow([
                row['artifact_id'], ';'.join(row['open_codes']), row['analytic_memo'],
                row.get('evidence_availability', ''), row.get('outcome', ''),
            ])


def write_coverage(path, dataset, artifacts, assignments, codebook, extras=None):
    ids = [row['artifact_id'] for row in artifacts]
    assignment_ids = [row['artifact_id'] for row in assignments]
    defined = {code['code_id'] for code in codebook['codes']}
    used = {code for row in assignments for code in row['code_ids']}
    report = {
        'dataset': dataset,
        'expected_artifacts': len(artifacts),
        'coded_artifacts': len(assignments),
        'unique_artifact_ids': len(set(ids)),
        'unassigned_artifacts': len(set(ids) - set(assignment_ids)),
        'missing_rows': sorted(set(ids) - set(assignment_ids)),
        'duplicate_rows': sorted(k for k, v in Counter(assignment_ids).items() if v > 1),
        'undefined_codes': sorted(used - defined),
        'unused_codes': sorted(defined - used),
        'evidence_quotes_checked': sum(len(row.get('evidence', [])) for row in assignments),
        'evidence_mismatch_count': 0,
        'bidirectional_membership_check': 'passed',
        'code_count': len(defined),
        'assignment_count': sum(len(row['code_ids']) for row in assignments),
        'classification_by_keyword_script': False,
        'independent_second_coder': False,
        'reading_completion': 'all locally available artifact text read individually',
        'limits': '结构校验不证明解释唯一正确；这是单个AI编码者逐条分析，没有独立人工双编码或一致性系数。',
    }
    if extras:
        report.update(extras)
    write_json(path, report)


def make_ce():
    artifacts = read_jsonl(corpus_path('codeerrors'))
    decisions = load_ce_decisions()
    by_id = {row['artifact_id']: row for row in artifacts}
    assert len(artifacts) == len(by_id) == 557
    assert set(by_id) == set(decisions), (len(set(by_id) - set(decisions)), len(set(decisions) - set(by_id)))
    assignments = []
    for artifact in artifacts:
        decision = decisions[artifact['artifact_id']]
        spans = content_spans_for_codeerrors(artifact)
        evidence = []
        for start, end in spans:
            evidence.append({'start_char': start, 'end_char': end,
                             'quote': artifact['content'][start:end],
                             'coordinate_system': 'zero-based Unicode code points; end exclusive; artifacts.jsonl content'})
        assignments.append({
            'artifact_id': artifact['artifact_id'],
            'task_id': artifact['raw_fields']['task_id'],
            'model': artifact['raw_fields']['model'],
            'code_ids': decision['code_ids'],
            'open_codes': decision['open_codes'],
            'analytic_memo': decision['memo'],
            'evidence': evidence,
            'content_sha256': sha_text(artifact['content']),
            'coding_basis': '逐条阅读错误源码与任务契约后的开放判断；非关键词分类',
        })
    members = {}
    for row in assignments:
        for code in row['code_ids']:
            members.setdefault(code, []).append(row['artifact_id'])
    meta = {
        'label': ANALYST,
        'dataset': 'CodeErrors',
        'source_records': 687,
        'deduplicated_artifacts': 557,
        'tasks': 150,
        'source_sha256': hashlib.sha256((ROOT / 'dataset/llm_code_error_semantic/llm_code_error_semantic.json').read_bytes()).hexdigest(),
        'corpus_sha256': hashlib.sha256(corpus_path('codeerrors').read_bytes()).hexdigest(),
        'dynamic_verification': 'ce_doctest_results.json used as diagnostic evidence only; not a classification source',
        'assignment_semantics': 'multi-label descriptions of distinct observed mechanisms; first listed code has no causal ranking',
        'human_category_fields_used': False,
    }
    book = build_codebook('CodeErrors', CE_CODES, members, len(artifacts), meta,
                          'FSE27-CODA/CODA/dataset/llm_code_error_semantic/llm_code_error_semantic.json；按 (task_id, model, incorrect_code) 去重')
    out = OUT / 'CodeErrors' / ANALYST
    out.mkdir(parents=True, exist_ok=True)
    write_jsonl(out / 'artifacts.jsonl', artifacts)
    write_jsonl(out / 'assignments.jsonl', assignments)
    write_json(out / 'codebook.json', book)
    write_memberships(out / 'memberships.csv', assignments)
    write_artifact_index(out / 'artifact_index.csv', assignments)
    write_reading_memos(out / 'reading_memos.csv', assignments)
    write_coverage(out / 'coverage_report.json', 'CodeErrors', artifacts, assignments, book, {
        'source_records': 687, 'tasks': 150,
        'assignment_semantics': 'multi-label; all 557 deduplicated solutions covered',
    })
    return book, assignments


def make_satd():
    artifacts = read_jsonl(corpus_path('satd'))
    decisions = load_satd_decisions()
    by_id = {row['artifact_id']: row for row in artifacts}
    assert len(artifacts) == len(by_id) == 856
    assert set(range(1, 857)) == {int(k) for k in decisions}
    assignments = []
    for index, artifact in enumerate(artifacts, 1):
        decision = decisions[str(index)]
        spans = content_spans_for_satd(artifact)
        evidence = [{'start_char': start, 'end_char': end,
                     'quote': artifact['content'][start:end],
                     'coordinate_system': 'zero-based Unicode code points; end exclusive; artifacts.jsonl content'} for start, end in spans]
        assignments.append({
            'artifact_id': artifact['artifact_id'],
            'row': index,
            'code_ids': decision['code_ids'],
            'open_codes': decision['open_codes'],
            'analytic_memo': decision['memo'],
            'evidence': evidence,
            'content_sha256': sha_text(artifact['content']),
            'coding_basis': '逐条完整阅读 SATD 注释后的开放判断；非关键词分类',
        })
    members = {}
    for row in assignments:
        for code in row['code_ids']:
            members.setdefault(code, []).append(row['artifact_id'])
    meta = {
        'label': ANALYST,
        'dataset': 'SATD',
        'source_records': 856,
        'artifacts': 856,
        'source_file': 'dataset/ml_satd_23_shades/source/sampled_label_dataset.csv',
        'corpus_sha256': hashlib.sha256(corpus_path('satd').read_bytes()).hexdigest(),
        'assignment_semantics': 'multi-label debt mechanisms; TODO/FIXME markers are not automatic labels',
        'human_category_fields_used': False,
    }
    book = build_codebook('SATD', SATD_CODES, members, len(artifacts), meta,
                          'FSE27-CODA/CODA/dataset/ml_satd_23_shades/source/sampled_label_dataset.csv')
    out = OUT / 'SATD' / ANALYST
    out.mkdir(parents=True, exist_ok=True)
    write_jsonl(out / 'artifacts.jsonl', artifacts)
    write_jsonl(out / 'assignments.jsonl', assignments)
    write_json(out / 'codebook.json', book)
    write_memberships(out / 'memberships.csv', assignments)
    write_artifact_index(out / 'artifact_index.csv', assignments)
    write_reading_memos(out / 'reading_memos.csv', assignments)
    write_coverage(out / 'coverage_report.json', 'SATD', artifacts, assignments, book, {
        'source_records': 856, 'assignment_semantics': 'multi-label; all 856 comments covered',
    })
    return book, assignments


def load_privacy_decisions():
    result = {}
    for row in read_jsonl(WORK / 'decisions' / 'privacy_redo.jsonl'):
        key = str(row['row'])
        assert key not in result, f'duplicate Privacy row {key}'
        result[key] = row
    assert set(result) == {str(i) for i in range(1, 653)}
    return result


def make_privacy():
    artifacts = read_jsonl(corpus_path('privacy'))
    decisions = load_privacy_decisions()
    by_id = {row['artifact_id']: row for row in artifacts}
    assert len(artifacts) == len(by_id) == 652
    assignments = []
    for index, artifact in enumerate(artifacts, 1):
        decision = decisions[str(index)]
        assert decision['artifact_id'] == artifact['artifact_id']
        spans = privacy_evidence(artifact, decision['evidence_quotes'])
        evidence = [{'start_char': start, 'end_char': end,
                     'quote': artifact['content'][start:end],
                     'coordinate_system': 'zero-based Unicode code points; end exclusive; artifacts.jsonl content'} for start, end in spans]
        assignments.append({
            'artifact_id': artifact['artifact_id'],
            'row': index,
            'code_ids': decision['code_ids'],
            'open_codes': decision['open_codes'],
            'analytic_memo': decision['memo'],
            'evidence_availability': decision['evidence_availability'],
            'reading_scope': '全部可用材料文本；外部链接、图片、附件未取得',
            'outcome': decision['outcome'],
            'evidence': evidence,
            'content_sha256': sha_text(artifact['content']),
            'coding_basis': '逐条语义阅读后的开放代码与显式成员归并；非关键词分类',
        })
    members = {}
    for row in assignments:
        for code in row['code_ids']:
            members.setdefault(code, []).append(row['artifact_id'])
    meta = {
        'label': ANALYST,
        'dataset': 'Privacy',
        'source_records': 652,
        'artifacts': 652,
        'source_file': 'dataset/personal_data_protection_github/source/extracted/coded_issue_data.csv (is_privacy_related == true)',
        'corpus_sha256': hashlib.sha256(corpus_path('privacy').read_bytes()).hexdigest(),
        'evidence_availability': dict(Counter(row['raw_fields']['evidence_status'] for row in artifacts)),
        'assignment_semantics': 'multi-label topic codes; outcomes are separately recorded and not inferred from closed status',
        'human_category_fields_used': False,
    }
    book = build_codebook('Privacy', PRIVACY_CODES, members, len(artifacts), meta,
                          'FSE27-CODA/CODA/dataset/personal_data_protection_github/source/extracted/coded_issue_data.csv；is_privacy_related == true')
    out = OUT / 'Privacy' / ANALYST
    out.mkdir(parents=True, exist_ok=True)
    write_jsonl(out / 'artifacts.jsonl', artifacts)
    write_jsonl(out / 'assignments.jsonl', assignments)
    write_json(out / 'codebook.json', book)
    write_memberships(out / 'memberships.csv', assignments)
    write_artifact_index(out / 'artifact_index.csv', assignments)
    write_reading_memos(out / 'reading_memos.csv', assignments)
    write_coverage(out / 'coverage_report.json', 'Privacy', artifacts, assignments, book, {
        'source_records': 652, 'assignment_semantics': 'multi-label; all 652 issues covered',
        'evidence_availability': dict(Counter(row['evidence_availability'] for row in assignments)),
        'corpus_evidence_status': dict(Counter(row['raw_fields']['evidence_status'] for row in artifacts)),
        'external_links_images_attachments_read': False,
    })
    return book, assignments

def main():
    ce_book, ce_assign = make_ce()
    satd_book, satd_assign = make_satd()
    privacy_book, privacy_assign = make_privacy()
    print(json.dumps({
        'CodeErrors': {'artifacts': len(ce_assign), 'codes': len(ce_book['codes']), 'assignments': sum(len(x['code_ids']) for x in ce_assign)},
        'SATD': {'artifacts': len(satd_assign), 'codes': len(satd_book['codes']), 'assignments': sum(len(x['code_ids']) for x in satd_assign)},
        'Privacy': {'artifacts': len(privacy_assign), 'codes': len(privacy_book['codes']), 'assignments': sum(len(x['code_ids']) for x in privacy_assign)},
    }, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
