# SATD / S3-2

Schema: `coda.artifact.v1`. Artifacts: **856**; codes: **18**; artifact–code assignments: **1546**.

This package uses the common seven-file format. All existing coding decisions, evidence and limitations are preserved. Additional source-specific fields are retained in `extensions`; original codebook text is retained in `codebook.json` metadata extensions and the local pre-conversion backup.

## Scope and method

full available text reading → open coding → authored explicit multi-label consolidation

Mechanical format validation does not establish independent semantic accuracy.

## Codes

| Code | Name | Artifacts |
|---|---|---:|
| SATD-A | 结构、职责与表示重构 | 216 |
| SATD-B | 行为、数学或接口正确性 | 74 |
| SATD-C | 校验、边界、异常与状态保护 | 67 |
| SATD-D | 行为实现或工作流补全 | 156 |
| SATD-E | 支持范围与泛化不足 | 106 |
| SATD-F | 外部依赖、版本与平台约束 | 77 |
| SATD-G | 性能、内存与执行资源 | 48 |
| SATD-H | 临时绕行与硬适配 | 44 |
| SATD-I | 算法与数据假设适用性 | 112 |
| SATD-J | 配置、参数与默认行为 | 76 |
| SATD-K | 测试与验证工作 | 61 |
| SATD-L | 说明、文档与理解缺口 | 26 |
| SATD-M | 冗余、弃用与条件性清理 | 61 |
| SATD-N | 持久化、序列化与数据表示契约 | 41 |
| SATD-O | 显示、日志与运行可观察性 | 25 |
| SATD-Q | 尚未裁决的设计或诊断 | 244 |
| SATD-U | 材料不足以细化待办 | 86 |
| SATD-V | 未明确承认待偿还问题 | 26 |

## SATD-A — 结构、职责与表示重构

当前实现的模块边界、职责归属、抽象、命名、代码格式或内部表示被要求调整，或存在具体的结构替代候选。

- Include: 明确提取、移动、复用、去耦、命名统一、格式整理或内部表示替代；可与未决设计并用。
- Exclude: 仅新增行为而无结构变化用 D；单纯执行速度诉求用 G。
- Boundary/examples: See original entry and representative evidence in codebook.json.
- Supporting artifacts: 216; complete membership in `supporting_cases`.

````json
[
  {
    "artifact_id": "23shades-0001-aahiieiig",
    "row": 1,
    "open_codes": [
      "共享逻辑组织待重构"
    ],
    "analytic_memo": "多个算法共用函数，作者明确承诺后续重构；不是模型算法本身未实现。",
    "evidence": [
      {
        "quote": "''' || Functions used by more than one algorithm || TODO refactor properly later || '''",
        "start_char": 135,
        "end_char": 222,
        "coordinate_system": "zero-based Unicode code points; end exclusive; artifacts.jsonl content"
      }
    ]
  },
  {
    "artifact_id": "23shades-0003-aaejjbhji",
    "row": 3,
    "open_codes": [
      "容器选择待简化"
    ],
    "analytic_memo": "作者指出空字典也能满足需求；句子截断，替代方案的完整限制不明。",
    "evidence": [
      {
        "quote": "!TODO: An empty dictionary would actually also do here ... despite the fact that",
        "start_char": 128,
        "end_char": 208,
        "coordinate_system": "zero-based Unicode code points; end exclusive; artifacts.jsonl content"
      }
    ]
  },
  {
    "artifact_id": "23shades-0006-aaahbghib",
    "row": 6,
    "open_codes": [
      "文本处理临时实现待替换"
    ],
    "analytic_memo": "作者希望用正则或其他方案替代 hack，未提供具体处理内容。",
    "evidence": [
      {
        "quote": "# hackier; fixme to use regex or something",
        "start_char": 127,
        "end_char": 169,
        "coordinate_system": "zero-based Unicode code points; end exclusive; artifacts.jsonl content"
      }
    ]
  }
]
````

## SATD-B — 行为、数学或接口正确性

注释指出行为错误、结果不一致、契约违背或具体正确性风险。

- Include: 明确错误与有对象的疑似错误均纳入，但备忘录必须区分确定、疑问和条件性。
- Exclude: 仅 TODO 或一般优化不纳入；尚未支持的新范围用 E。
- Boundary/examples: See original entry and representative evidence in codebook.json.
- Supporting artifacts: 74; complete membership in `supporting_cases`.

````json
[
  {
    "artifact_id": "23shades-0004-aaejjacgf",
    "row": 4,
    "open_codes": [
      "数值容器容量不足"
    ],
    "analytic_memo": "US 无法容纳某些完整数值；不推断 US 具体类型或位宽。",
    "evidence": [
      {
        "quote": "!TODO: In some cases; US is not enough to hold the complete number",
        "start_char": 145,
        "end_char": 211,
        "coordinate_system": "zero-based Unicode code points; end exclusive; artifacts.jsonl content"
      }
    ]
  },
  {
    "artifact_id": "23shades-0007-aaaegfgeb",
    "row": 7,
    "open_codes": [
      "变换顺序待调整"
    ],
    "analytic_memo": "要求 concat 前 reverse bw；bw 含义缺失，不推断具体网络结构。",
    "evidence": [
      {
        "quote": "# reverse bw; before concat TODO",
        "start_char": 128,
        "end_char": 160,
        "coordinate_system": "zero-based Unicode code points; end exclusive; artifacts.jsonl content"
      }
    ]
  },
  {
    "artifact_id": "23shades-0030-aaedcebdc",
    "row": 30,
    "open_codes": [
      "预测接口行为错误"
    ],
    "analytic_memo": "作者明确称 bug，predict_proba 不应 change；具体改变对象截断。",
    "evidence": [
      {
        "quote": "[todo]: this is a bug; predict_proba should not change",
        "start_char": 130,
        "end_char": 184,
        "coordinate_system": "zero-based Unicode code points; end exclusive; artifacts.jsonl content"
      }
    ]
  }
]
````

## SATD-C — 校验、边界、异常与状态保护

需要验证输入、形状、状态、生命周期或错误路径，并保护共享状态及边界条件。

- Include: 空值、除零、类型形状检查、并发锁、异常策略、完整性检查以及相关待验证风险。
- Exclude: 新增单元测试用 K；train/test 数据划分本身不属测试。
- Boundary/examples: See original entry and representative evidence in codebook.json.
- Supporting artifacts: 67; complete membership in `supporting_cases`.

````json
[
  {
    "artifact_id": "23shades-0048-aagaijehb",
    "row": 48,
    "open_codes": [
      "参数兼容检查缺失"
    ],
    "analytic_memo": "未来需要验证参数间兼容性。",
    "evidence": [
      {
        "quote": "\\/\\/TODO in future add arguments compatibility check",
        "start_char": 122,
        "end_char": 174,
        "coordinate_system": "zero-based Unicode code points; end exclusive; artifacts.jsonl content"
      }
    ]
  },
  {
    "artifact_id": "23shades-0062-aagachfba",
    "row": 62,
    "open_codes": [
      "重复项检查缺失"
    ],
    "analytic_memo": "应检查 variation 是否已存在。",
    "evidence": [
      {
        "quote": "else:  # TODO check that the variation wasn't already in there",
        "start_char": 138,
        "end_char": 200,
        "coordinate_system": "zero-based Unicode code points; end exclusive; artifacts.jsonl content"
      }
    ]
  },
  {
    "artifact_id": "23shades-0063-aaaedhbbd",
    "row": 63,
    "open_codes": [
      "输入类型契约待保证"
    ],
    "analytic_memo": "需保证传给 _pool.step 的是 ndarray。",
    "evidence": [
      {
        "quote": "Ensure we're really passing an ndarray to _pool.step()",
        "start_char": 126,
        "end_char": 180,
        "coordinate_system": "zero-based Unicode code points; end exclusive; artifacts.jsonl content"
      }
    ]
  }
]
````

## SATD-D — 行为实现或工作流补全

存在待增加、启用、补齐或扩展的计算、数据处理、持久化或交互行为。

- Include: 具体功能待办与明确 implement/incomplete 即使指代缺失；范围不足可并 E。
- Exclude: 只有名称和 TODO 且不知动作时用 U；不把链接中的功能认作已读证据。
- Boundary/examples: See original entry and representative evidence in codebook.json.
- Supporting artifacts: 156; complete membership in `supporting_cases`.

````json
[
  {
    "artifact_id": "23shades-0008-aagcbjjcd",
    "row": 8,
    "open_codes": [
      "验证与测试数据处理不完整"
    ],
    "analytic_memo": "landmarks 只未扩展到 validation/test；明确因当日疲劳推迟，不是单元测试缺失。",
    "evidence": [
      {
        "quote": "# TODO : load landmarks in validation and test set also. I'm too sleepy to do it today -_- zzz... zzz...",
        "start_char": 155,
        "end_char": 259,
        "coordinate_system": "zero-based Unicode code points; end exclusive; artifacts.jsonl content"
      }
    ]
  },
  {
    "artifact_id": "23shades-0012-aafaehach",
    "row": 12,
    "open_codes": [
      "缺省命名行为待补充"
    ],
    "analytic_memo": "name 缺失时拟采用 functionality.__name__。",
    "evidence": [
      {
        "quote": "# TODO: Set name (using \\\"functionality.__name__\\\") if name is None",
        "start_char": 169,
        "end_char": 236,
        "coordinate_system": "zero-based Unicode code points; end exclusive; artifacts.jsonl content"
      }
    ]
  },
  {
    "artifact_id": "23shades-0021-aadbhiccj",
    "row": 21,
    "open_codes": [
      "工作流组件集成缺失"
    ],
    "analytic_memo": "Frontend 和 Model 尚待纳入该 workflow。",
    "evidence": [
      {
        "quote": "@todo integrate Frontend and Model to that workflow",
        "start_char": 122,
        "end_char": 173,
        "coordinate_system": "zero-based Unicode code points; end exclusive; artifacts.jsonl content"
      }
    ]
  }
]
````

## SATD-E — 支持范围与泛化不足

实现仅覆盖部分输入、类型、模型、格式、设备或场景，需扩展或核实覆盖。

- Include: 明确缺少的类型/分支/模型族及可辨识的覆盖疑问。
- Exclude: 没有覆盖对象的一般改进不纳入；版本或外部 API 限制另加 F。
- Boundary/examples: See original entry and representative evidence in codebook.json.
- Supporting artifacts: 106; complete membership in `supporting_cases`.

````json
[
  {
    "artifact_id": "23shades-0013-aaebbeedd",
    "row": 13,
    "open_codes": [
      "分支支持不全"
    ],
    "analytic_memo": "其他 bases 尚未被处理；不推断 bases 是数制还是父类。",
    "evidence": [
      {
        "quote": "## elif (): ## FIXME: handle other bases here",
        "start_char": 117,
        "end_char": 162,
        "coordinate_system": "zero-based Unicode code points; end exclusive; artifacts.jsonl content"
      }
    ]
  },
  {
    "artifact_id": "23shades-0015-aaibjbide",
    "row": 15,
    "open_codes": [
      "模型行为覆盖不全"
    ],
    "analytic_memo": "需对全部模型加入 intercept；intercept 的具体语义不明。",
    "evidence": [
      {
        "quote": "## TODO: intercept for all models",
        "start_char": 131,
        "end_char": 164,
        "coordinate_system": "zero-based Unicode code points; end exclusive; artifacts.jsonl content"
      }
    ]
  },
  {
    "artifact_id": "23shades-0016-aadfachjd",
    "row": 16,
    "open_codes": [
      "优化器支持不全"
    ],
    "analytic_memo": "当前只支持 SGD，希望增加其他训练优化器；不属于执行性能证据。",
    "evidence": [
      {
        "quote": "##TODO add optimizers other than SGD",
        "start_char": 145,
        "end_char": 181,
        "coordinate_system": "zero-based Unicode code points; end exclusive; artifacts.jsonl content"
      }
    ]
  }
]
````

## SATD-F — 外部依赖、版本与平台约束

修改受外部库、版本、后端、平台或调用者契约制约。

- Include: 兼容迁移、上游缺陷绕行、版本成熟后清理、依赖声明及跨框架接口适配。
- Exclude: 不能仅由库名出现判断存在债务；正常兼容说明应并 V。
- Boundary/examples: See original entry and representative evidence in codebook.json.
- Supporting artifacts: 77; complete membership in `supporting_cases`.

````json
[
  {
    "artifact_id": "23shades-0019-aaigjhibg",
    "row": 19,
    "open_codes": [
      "兼容性待修复"
    ],
    "analytic_memo": "只给 fix compatibility，版本和对象缺失。",
    "evidence": [
      {
        "quote": "((); 0); # TODO(sonots): Fix compatibility",
        "start_char": 155,
        "end_char": 197,
        "coordinate_system": "zero-based Unicode code points; end exclusive; artifacts.jsonl content"
      }
    ]
  },
  {
    "artifact_id": "23shades-0020-aaigjhiah",
    "row": 20,
    "open_codes": [
      "兼容性待修复"
    ],
    "analytic_memo": "与前条文本一致但保留独立 artifact；兼容对象不明。",
    "evidence": [
      {
        "quote": "((); 0); # TODO(sonots): Fix compatibility",
        "start_char": 160,
        "end_char": 202,
        "coordinate_system": "zero-based Unicode code points; end exclusive; artifacts.jsonl content"
      }
    ]
  },
  {
    "artifact_id": "23shades-0037-aajffhihe",
    "row": 37,
    "open_codes": [
      "语法支持不全",
      "编译路径性能改进"
    ],
    "analytic_memo": "unparse 只支持列举的语法结构；拟转 _ast 因编译约快六倍，两项均有明确依据。",
    "evidence": [
      {
        "quote": "\\\"\\\"\\\" Turn compiler.ast structures back into executable python code. ||  ||     The unparse method takes a compiler.ast tree and transforms it back into ||     valid python code.  It is incomplete and currently only works for ||     import statements; function calls; function definitions; assignments; and ||     basic expressions. ||  ||     Inspired by python-2.5-svn\\/Demo\\/parser\\/unparse.py ||  ||     fixme: We may want to move to using _ast trees because the compiler for ||            them is about 6 times faster than compiler.compile. || \\\"\\\"\\\"",
        "start_char": 148,
        "end_char": 704,
        "coordinate_system": "zero-based Unicode code points; end exclusive; artifacts.jsonl content"
      }
    ]
  }
]
````

## SATD-G — 性能、内存与执行资源

材料明确涉及执行开销、复杂度、内存、并行或性能测量与比较。

- Include: 已有瓶颈、候选优化和待测性能分开记述；并发执行约束也可纳入。
- Exclude: 训练 optimizer 名称不自动等于性能优化；未经测量不写已提速。
- Boundary/examples: See original entry and representative evidence in codebook.json.
- Supporting artifacts: 48; complete membership in `supporting_cases`.

````json
[
  {
    "artifact_id": "23shades-0037-aajffhihe",
    "row": 37,
    "open_codes": [
      "语法支持不全",
      "编译路径性能改进"
    ],
    "analytic_memo": "unparse 只支持列举的语法结构；拟转 _ast 因编译约快六倍，两项均有明确依据。",
    "evidence": [
      {
        "quote": "\\\"\\\"\\\" Turn compiler.ast structures back into executable python code. ||  ||     The unparse method takes a compiler.ast tree and transforms it back into ||     valid python code.  It is incomplete and currently only works for ||     import statements; function calls; function definitions; assignments; and ||     basic expressions. ||  ||     Inspired by python-2.5-svn\\/Demo\\/parser\\/unparse.py ||  ||     fixme: We may want to move to using _ast trees because the compiler for ||            them is about 6 times faster than compiler.compile. || \\\"\\\"\\\"",
        "start_char": 148,
        "end_char": 704,
        "coordinate_system": "zero-based Unicode code points; end exclusive; artifacts.jsonl content"
      }
    ]
  },
  {
    "artifact_id": "23shades-0086-aaicdjedb",
    "row": 86,
    "open_codes": [
      "并行资源配置未利用"
    ],
    "analytic_memo": "指出此处也可用 n_jobs。",
    "evidence": [
      {
        "quote": "FIXME: can use n_jobs here too",
        "start_char": 133,
        "end_char": 163,
        "coordinate_system": "zero-based Unicode code points; end exclusive; artifacts.jsonl content"
      }
    ]
  },
  {
    "artifact_id": "23shades-0109-aaibiggcj",
    "row": 109,
    "open_codes": [
      "协方差表示不利缓存"
    ],
    "analytic_memo": "作者认为当前 covars representation 会损害 caching。",
    "evidence": [
      {
        "quote": "FIXME: this representation of covars is going to lose for caching",
        "start_char": 126,
        "end_char": 191,
        "coordinate_system": "zero-based Unicode code points; end exclusive; artifacts.jsonl content"
      }
    ]
  }
]
````

## SATD-H — 临时绕行与硬适配

当前依靠临时补丁、占位值、硬编码或脆弱约定实现行为。

- Include: 明确 hack/workaround 的语义，以及固定值替代真实数据、依赖未公开约定的补偿。
- Exclude: 普通常量或仅描述必要操作不自动构成临时债务。
- Boundary/examples: See original entry and representative evidence in codebook.json.
- Supporting artifacts: 44; complete membership in `supporting_cases`.

````json
[
  {
    "artifact_id": "23shades-0005-aaebbecaa",
    "row": 5,
    "open_codes": [
      "布局缺陷的临时绕行"
    ],
    "analytic_memo": "justify-content 失效导致采用 SVG 居中 hack；问题在显示布局。",
    "evidence": [
      {
        "quote": "# Hack to center SVG as justify-content is broken:",
        "start_char": 115,
        "end_char": 165,
        "coordinate_system": "zero-based Unicode code points; end exclusive; artifacts.jsonl content"
      }
    ]
  },
  {
    "artifact_id": "23shades-0006-aaahbghib",
    "row": 6,
    "open_codes": [
      "文本处理临时实现待替换"
    ],
    "analytic_memo": "作者希望用正则或其他方案替代 hack，未提供具体处理内容。",
    "evidence": [
      {
        "quote": "# hackier; fixme to use regex or something",
        "start_char": 127,
        "end_char": 169,
        "coordinate_system": "zero-based Unicode code points; end exclusive; artifacts.jsonl content"
      }
    ]
  },
  {
    "artifact_id": "23shades-0046-aafchcgjg",
    "row": 46,
    "open_codes": [
      "缺失置信度以常数代替"
    ],
    "analytic_memo": "上游未提供 confidence，临时填 1；不能当作真实置信度。",
    "evidence": [
      {
        "quote": "\\\"confidence\\\": 1  # todo discussion confidence from GNormPlus is not provided so just putting in here 1",
        "start_char": 115,
        "end_char": 219,
        "coordinate_system": "zero-based Unicode code points; end exclusive; artifacts.jsonl content"
      }
    ]
  }
]
````

## SATD-I — 算法与数据假设适用性

具体数学、数据、形状、初始化或启发式假设需要确认、限制或调整。

- Include: 模型选择、占位训练目标、阈值依据、尺度/索引/分布假设及信息损失权衡。
- Exclude: 不把疑问当已证错误；仅出现模型代码且无可定位待办用 U。
- Boundary/examples: See original entry and representative evidence in codebook.json.
- Supporting artifacts: 112; complete membership in `supporting_cases`.

````json
[
  {
    "artifact_id": "23shades-0046-aafchcgjg",
    "row": 46,
    "open_codes": [
      "缺失置信度以常数代替"
    ],
    "analytic_memo": "上游未提供 confidence，临时填 1；不能当作真实置信度。",
    "evidence": [
      {
        "quote": "\\\"confidence\\\": 1  # todo discussion confidence from GNormPlus is not provided so just putting in here 1",
        "start_char": 115,
        "end_char": 219,
        "coordinate_system": "zero-based Unicode code points; end exclusive; artifacts.jsonl content"
      }
    ]
  },
  {
    "artifact_id": "23shades-0050-aabcjdaea",
    "row": 50,
    "open_codes": [
      "训练误差缩放假设"
    ],
    "analytic_memo": "零和游戏与两个值导致 error 乘二的注释；未明确说这种做法错误，需保留不确定性。",
    "evidence": [
      {
        "quote": "all games are zero sum that are trained and because 2 values; x2 the error.  XXX",
        "start_char": 137,
        "end_char": 217,
        "coordinate_system": "zero-based Unicode code points; end exclusive; artifacts.jsonl content"
      }
    ]
  },
  {
    "artifact_id": "23shades-0054-aadaieabb",
    "row": 54,
    "open_codes": [
      "固定标签长度假设",
      "接受钩子缺失"
    ],
    "analytic_memo": "当前假定四字节 magic label，拟加 _accept hook。",
    "evidence": [
      {
        "quote": "assuming a 4-byte magic label (FIXME: add \\\"_accept\\\" hook)",
        "start_char": 164,
        "end_char": 223,
        "coordinate_system": "zero-based Unicode code points; end exclusive; artifacts.jsonl content"
      }
    ]
  }
]
````

## SATD-J — 配置、参数与默认行为

参数可配置性、参数语义、默认值或配置传播存在待改事项。

- Include: 硬编码转参数、开关、默认策略、参数缺失/未生效及有对象的配置决策。
- Exclude: 仅重命名一般局部变量用 A；测试数据中的参数不必然是产品配置。
- Boundary/examples: See original entry and representative evidence in codebook.json.
- Supporting artifacts: 76; complete membership in `supporting_cases`.

````json
[
  {
    "artifact_id": "23shades-0011-aageijaai",
    "row": 11,
    "open_codes": [
      "参数可训练性待决策"
    ],
    "analytic_memo": "询问 gains/biases 是否应可训练，保留设计疑问。",
    "evidence": [
      {
        "quote": "# TODO: do we want gains\\/biases to be trainable?",
        "start_char": 139,
        "end_char": 188,
        "coordinate_system": "zero-based Unicode code points; end exclusive; artifacts.jsonl content"
      }
    ]
  },
  {
    "artifact_id": "23shades-0012-aafaehach",
    "row": 12,
    "open_codes": [
      "缺省命名行为待补充"
    ],
    "analytic_memo": "name 缺失时拟采用 functionality.__name__。",
    "evidence": [
      {
        "quote": "# TODO: Set name (using \\\"functionality.__name__\\\") if name is None",
        "start_char": 169,
        "end_char": 236,
        "coordinate_system": "zero-based Unicode code points; end exclusive; artifacts.jsonl content"
      }
    ]
  },
  {
    "artifact_id": "23shades-0022-aahdfibcf",
    "row": 22,
    "open_codes": [
      "测试专用参数残留"
    ],
    "analytic_memo": "TODO 指出 nrows 仅用于测试；应关注参数用途，但未说明删除或替代方案，保留待办意图与处置不确定性。",
    "evidence": [
      {
        "quote": "@todo nrows is for testing only!",
        "start_char": 150,
        "end_char": 182,
        "coordinate_system": "zero-based Unicode code points; end exclusive; artifacts.jsonl content"
      }
    ]
  }
]
````

## SATD-K — 测试与验证工作

需要新增、启用、更新、扩展或修复测试，以及显式核验行为或性能的工作。

- Include: 断言不足、设备无关测试、版本复验及明确测试/比较活动；注明是否只是待核验。
- Exclude: 数据集 validation/test 不等于测试代码；判别某类型的 test 仅用 C。
- Boundary/examples: See original entry and representative evidence in codebook.json.
- Supporting artifacts: 61; complete membership in `supporting_cases`.

````json
[
  {
    "artifact_id": "23shades-0038-aaeiaheab",
    "row": 38,
    "open_codes": [
      "测试缺失",
      "实现清理待办"
    ],
    "analytic_memo": "MdC 到 Unicode 转换需要增加测试与清理代码。",
    "evidence": [
      {
        "quote": "\\\"\\\"\\\"Convert MdC transliterated text to Unicode. ||  || TODO: Add tests and clean up. || \\\"\\\"\\\"",
        "start_char": 116,
        "end_char": 212,
        "coordinate_system": "zero-based Unicode code points; end exclusive; artifacts.jsonl content"
      }
    ]
  },
  {
    "artifact_id": "23shades-0040-aaeiahgad",
    "row": 40,
    "open_codes": [
      "外部依赖移除待办",
      "测试缺失"
    ],
    "analytic_memo": "Unicode 转换模块拟移除 regex 依赖并增加测试。",
    "evidence": [
      {
        "quote": "\\\"\\\"\\\"Converts legacy encodings into Unicode. ||  || TODO: Rm regex dependency || TODO: Add tests || \\\"\\\"\\\"",
        "start_char": 132,
        "end_char": 239,
        "coordinate_system": "zero-based Unicode code points; end exclusive; artifacts.jsonl content"
      }
    ]
  },
  {
    "artifact_id": "23shades-0072-aaidadhdg",
    "row": 72,
    "open_codes": [
      "测试跳过机制使用受限"
    ],
    "analytic_memo": "希望使用 _skip_test，但 if we could 表示约束未解决。",
    "evidence": [
      {
        "quote": "FIXME _skip_test should be used here (if we could)",
        "start_char": 134,
        "end_char": 184,
        "coordinate_system": "zero-based Unicode code points; end exclusive; artifacts.jsonl content"
      }
    ]
  }
]
````

## SATD-L — 说明、文档与理解缺口

文档、教程、引用、说明或对实现含义的理解不足。

- Include: 缺 docstring、陈旧说明、为何存在的解释、未理解的参数/变量。
- Exclude: 日志及运行诊断主要用 O；不能把所有设计疑问都当文档缺失。
- Boundary/examples: See original entry and representative evidence in codebook.json.
- Supporting artifacts: 26; complete membership in `supporting_cases`.

````json
[
  {
    "artifact_id": "23shades-0018-aajcabgbe",
    "row": 18,
    "open_codes": [
      "教程材料待补充"
    ],
    "analytic_memo": "认为现有内容可转成生成 phantoms 的教程。",
    "evidence": [
      {
        "quote": "#TODO: this can become a nice tutorial for generating phantoms",
        "start_char": 117,
        "end_char": 179,
        "coordinate_system": "zero-based Unicode code points; end exclusive; artifacts.jsonl content"
      }
    ]
  },
  {
    "artifact_id": "23shades-0032-aaejahaed",
    "row": 32,
    "open_codes": [
      "文档缺失"
    ],
    "analytic_memo": "doc 占位待写。",
    "evidence": [
      {
        "quote": "\\\"\\\"\\\" || .. todo:: ||     doc || \\\"\\\"\\\"",
        "start_char": 123,
        "end_char": 163,
        "coordinate_system": "zero-based Unicode code points; end exclusive; artifacts.jsonl content"
      }
    ]
  },
  {
    "artifact_id": "23shades-0033-aadhcadac",
    "row": 33,
    "open_codes": [
      "模块说明缺失"
    ],
    "analytic_memo": "hyperband synopsis 与长描述为 TODO，占位文档未完成。",
    "evidence": [
      {
        "quote": "\\\"\\\"\\\" || :mod:`orion.algo.hyperband.hyperband -- TODO || ================================================= ||  || .. module:: hyperband ||     :platform: Unix ||     :synopsis: TODO ||  || TODO: Write long description || \\\"\\\"\\\"",
        "start_char": 130,
        "end_char": 358,
        "coordinate_system": "zero-based Unicode code points; end exclusive; artifacts.jsonl content"
      }
    ]
  }
]
````

## SATD-M — 冗余、弃用与条件性清理

存在待删除的过渡、重复、未用或弃用逻辑，或其必要性尚待判断。

- Include: 版本到期清理、替代能力就绪再删、重复参数、疑似无用代码；保留条件。
- Exclude: 不能把 probably unnecessary 记为已确认无用或已删除。
- Boundary/examples: See original entry and representative evidence in codebook.json.
- Supporting artifacts: 61; complete membership in `supporting_cases`.

````json
[
  {
    "artifact_id": "23shades-0038-aaeiaheab",
    "row": 38,
    "open_codes": [
      "测试缺失",
      "实现清理待办"
    ],
    "analytic_memo": "MdC 到 Unicode 转换需要增加测试与清理代码。",
    "evidence": [
      {
        "quote": "\\\"\\\"\\\"Convert MdC transliterated text to Unicode. ||  || TODO: Add tests and clean up. || \\\"\\\"\\\"",
        "start_char": 116,
        "end_char": 212,
        "coordinate_system": "zero-based Unicode code points; end exclusive; artifacts.jsonl content"
      }
    ]
  },
  {
    "artifact_id": "23shades-0058-aaahbfbhe",
    "row": 58,
    "open_codes": [
      "疑似废弃逻辑"
    ],
    "analytic_memo": "作者询问是否 deprecate，认为可能不再需要；尚未裁决。",
    "evidence": [
      {
        "quote": "DEPRICATE? I don't think this is needed anymore",
        "start_char": 123,
        "end_char": 170,
        "coordinate_system": "zero-based Unicode code points; end exclusive; artifacts.jsonl content"
      }
    ]
  },
  {
    "artifact_id": "23shades-0080-aaidbchej",
    "row": 80,
    "open_codes": [
      "版本迁移后的测试清理"
    ],
    "analytic_memo": "当 0.26 默认 square_distances=True 后删除特定测试；不是普遍测试不足。",
    "evidence": [
      {
        "quote": "FIXME remove test when square_distances=True becomes the default in 0.26",
        "start_char": 142,
        "end_char": 214,
        "coordinate_system": "zero-based Unicode code points; end exclusive; artifacts.jsonl content"
      }
    ]
  }
]
````

## SATD-N — 持久化、序列化与数据表示契约

涉及保存/恢复、格式、输出表示、索引或跨阶段传递的数据结构。

- Include: 序列化失败、格式替换、检查点、模型保存、稳定索引、输出元信息。
- Exclude: 一般内部抽象变化用 A；未说明格式的泛化待办不必纳入。
- Boundary/examples: See original entry and representative evidence in codebook.json.
- Supporting artifacts: 41; complete membership in `supporting_cases`.

````json
[
  {
    "artifact_id": "23shades-0035-aahfiaifg",
    "row": 35,
    "open_codes": [
      "序列化格式不符"
    ],
    "analytic_memo": "CSV corpus 实际仍输出 SVMLight，作者邀请修改。",
    "evidence": [
      {
        "quote": "\\\"\\\"\\\" || Corpus in CSV format. TODO: still serializes to SVMLight format; feel free to change this. || \\\"\\\"\\\"",
        "start_char": 132,
        "end_char": 242,
        "coordinate_system": "zero-based Unicode code points; end exclusive; artifacts.jsonl content"
      }
    ]
  },
  {
    "artifact_id": "23shades-0045-aajdcegja",
    "row": 45,
    "open_codes": [
      "差异格式契约未定义"
    ],
    "analytic_memo": "diff 格式需要定义并文档化；版本转换已由 nbformat 处理，不能误码为版本支持缺失。",
    "evidence": [
      {
        "quote": "\\\"\\\"\\\"Tools for diffing notebooks. ||  || All diff tools here currently assumes the notebooks have already been || converted to the same format version; currently v4 at time of writing. || Up- and down-conversion is handled by nbformat. ||  || FIXME: Define and document diff format. || \\\"\\\"\\\"",
        "start_char": 132,
        "end_char": 425,
        "coordinate_system": "zero-based Unicode code points; end exclusive; artifacts.jsonl content"
      }
    ]
  },
  {
    "artifact_id": "23shades-0054-aadaieabb",
    "row": 54,
    "open_codes": [
      "固定标签长度假设",
      "接受钩子缺失"
    ],
    "analytic_memo": "当前假定四字节 magic label，拟加 _accept hook。",
    "evidence": [
      {
        "quote": "assuming a 4-byte magic label (FIXME: add \\\"_accept\\\" hook)",
        "start_char": 164,
        "end_char": 223,
        "coordinate_system": "zero-based Unicode code points; end exclusive; artifacts.jsonl content"
      }
    ]
  }
]
````

## SATD-O — 显示、日志与运行可观察性

展示、图表、告警、日志或运行时间反馈需要改善。

- Include: 显示错误、绘图功能、日志等级/范围、警告与测量信息。
- Exclude: 日志里有测试输出不代表测试充分；缺断言应并 K。
- Boundary/examples: See original entry and representative evidence in codebook.json.
- Supporting artifacts: 25; complete membership in `supporting_cases`.

````json
[
  {
    "artifact_id": "23shades-0059-aacjfgieb",
    "row": 59,
    "open_codes": [
      "换行渲染异常"
    ],
    "analytic_memo": "双换行似乎影响显示；原因不明。",
    "evidence": [
      {
        "quote": "Double newlines seem to mess with the rendering",
        "start_char": 122,
        "end_char": 169,
        "coordinate_system": "zero-based Unicode code points; end exclusive; artifacts.jsonl content"
      }
    ]
  },
  {
    "artifact_id": "23shades-0088-aahedijdj",
    "row": 88,
    "open_codes": [
      "显示内容待隐藏"
    ],
    "analytic_memo": "don't show 的对象只有转义斜杠，展示意图可见但细节不足。",
    "evidence": [
      {
        "quote": "FIXME: don't show \\/",
        "start_char": 136,
        "end_char": 156,
        "coordinate_system": "zero-based Unicode code points; end exclusive; artifacts.jsonl content"
      }
    ]
  },
  {
    "artifact_id": "23shades-0202-aafdacejd",
    "row": 202,
    "open_codes": [
      "可视化边界待平滑"
    ],
    "analytic_memo": "要求 smoother visualization bounds。",
    "evidence": [
      {
        "quote": "TODO -- instead; smoother visualization bounds (at MAG)",
        "start_char": 170,
        "end_char": 225,
        "coordinate_system": "zero-based Unicode code points; end exclusive; artifacts.jsonl content"
      }
    ]
  }
]
````

## SATD-Q — 尚未裁决的设计或诊断

作者仍在询问必要性、原因、替代方案、效果或正确性，尚无明确裁决。

- Include: 保留问句、maybe、待核实、对象不完整的一般改进，不升级为确认缺陷。
- Exclude: 明确待实现且无选择疑问不必加；此为认识状态代码，不替代具体主题。
- Boundary/examples: See original entry and representative evidence in codebook.json.
- Supporting artifacts: 244; complete membership in `supporting_cases`.

````json
[
  {
    "artifact_id": "23shades-0010-aaaedagad",
    "row": 10,
    "open_codes": [
      "元数据字段改写待定"
    ],
    "analytic_memo": "name/index/uuid 可能需要重写；是候选修改而非已确认错误。",
    "evidence": [
      {
        "quote": "# TODO May want to rewrite name; index; uuid; etc.",
        "start_char": 147,
        "end_char": 197,
        "coordinate_system": "zero-based Unicode code points; end exclusive; artifacts.jsonl content"
      }
    ]
  },
  {
    "artifact_id": "23shades-0011-aageijaai",
    "row": 11,
    "open_codes": [
      "参数可训练性待决策"
    ],
    "analytic_memo": "询问 gains/biases 是否应可训练，保留设计疑问。",
    "evidence": [
      {
        "quote": "# TODO: do we want gains\\/biases to be trainable?",
        "start_char": 139,
        "end_char": 188,
        "coordinate_system": "zero-based Unicode code points; end exclusive; artifacts.jsonl content"
      }
    ]
  },
  {
    "artifact_id": "23shades-0022-aahdfibcf",
    "row": 22,
    "open_codes": [
      "测试专用参数残留"
    ],
    "analytic_memo": "TODO 指出 nrows 仅用于测试；应关注参数用途，但未说明删除或替代方案，保留待办意图与处置不确定性。",
    "evidence": [
      {
        "quote": "@todo nrows is for testing only!",
        "start_char": 150,
        "end_char": 182,
        "coordinate_system": "zero-based Unicode code points; end exclusive; artifacts.jsonl content"
      }
    ]
  }
]
````

## SATD-U — 材料不足以细化待办

可用注释只有标记、名称、外链或被截断的指代，不能可靠定位待改机制。

- Include: 空 TODO/FIXME、没有动作的对象名、未获取外链以及关键句尾缺失。
- Exclude: 已明确 implement/refactor 可编码其一般方向；不得据周边名称补造机制。
- Boundary/examples: See original entry and representative evidence in codebook.json.
- Supporting artifacts: 86; complete membership in `supporting_cases`.

````json
[
  {
    "artifact_id": "23shades-0002-aaehidhih",
    "row": 2,
    "open_codes": [
      "证据不足"
    ],
    "analytic_memo": "只有 TODO，不能确定工作对象。",
    "evidence": [
      {
        "quote": "!TODO",
        "start_char": 140,
        "end_char": 145,
        "coordinate_system": "zero-based Unicode code points; end exclusive; artifacts.jsonl content"
      }
    ]
  },
  {
    "artifact_id": "23shades-0014-aadbjfiab",
    "row": 14,
    "open_codes": [
      "证据不足"
    ],
    "analytic_memo": "空 TODO。",
    "evidence": [
      {
        "quote": "## TODO:",
        "start_char": 194,
        "end_char": 202,
        "coordinate_system": "zero-based Unicode code points; end exclusive; artifacts.jsonl content"
      }
    ]
  },
  {
    "artifact_id": "23shades-0023-aajffebhi",
    "row": 23,
    "open_codes": [
      "证据不足"
    ],
    "analytic_memo": "空 TODO。",
    "evidence": [
      {
        "quote": "@TODO:",
        "start_char": 134,
        "end_char": 140,
        "coordinate_system": "zero-based Unicode code points; end exclusive; artifacts.jsonl content"
      }
    ]
  }
]
````

## SATD-V — 未明确承认待偿还问题

材料主要解释现有操作、必要性、约束或已成立行为，没有明确待办或负面判断。

- Include: 说明性注释、正常兼容用途、现有补偿效果；可与其实际主题并存。
- Exclude: 明确未完成、错误或质量不足不归本类；不是宣称整个仓库无技术债。
- Boundary/examples: See original entry and representative evidence in codebook.json.
- Supporting artifacts: 26; complete membership in `supporting_cases`.

````json
[
  {
    "artifact_id": "23shades-0050-aabcjdaea",
    "row": 50,
    "open_codes": [
      "训练误差缩放假设"
    ],
    "analytic_memo": "零和游戏与两个值导致 error 乘二的注释；未明确说这种做法错误，需保留不确定性。",
    "evidence": [
      {
        "quote": "all games are zero sum that are trained and because 2 values; x2 the error.  XXX",
        "start_char": 137,
        "end_char": 217,
        "coordinate_system": "zero-based Unicode code points; end exclusive; artifacts.jsonl content"
      }
    ]
  },
  {
    "artifact_id": "23shades-0056-aaeeibecj",
    "row": 56,
    "open_codes": [
      "信号相位处理说明"
    ],
    "analytic_memo": "circular shift 被描述为正确相位所需；未表述待偿还债务，不强制归为错误。",
    "evidence": [
      {
        "quote": "circular shift the signal (needed for correct phase)",
        "start_char": 116,
        "end_char": 168,
        "coordinate_system": "zero-based Unicode code points; end exclusive; artifacts.jsonl content"
      }
    ]
  },
  {
    "artifact_id": "23shades-0057-aajffjdic",
    "row": 57,
    "open_codes": [
      "按需构造行为说明"
    ],
    "analytic_memo": "按参数空间需要构造 grids/weights，未明确欠缺或问题。",
    "evidence": [
      {
        "quote": "Construct grids and weights if needed for parameter space",
        "start_char": 160,
        "end_char": 217,
        "coordinate_system": "zero-based Unicode code points; end exclusive; artifacts.jsonl content"
      }
    ]
  }
]
````

## Files

- `codebook.md`, `codebook.json`, `codebook.csv`: definitions and complete reverse memberships.
- `assignments.json`, `assignments.csv`: one record per artifact, including decisions and evidence.
- `taxonomy.json`: category tree with every code as a leaf.
- `results.json`: supplied full documents aligned to their assignments.

## Original codebook

The original codebook text below preserves run-specific scope, combination rules and qualifications. Links and filenames in that historical text describe the original package; use the seven files above for the normalized interface. The exact original text is also stored in metadata extensions.

# SATD Codebook — 结果 2（逐条阅读重建）

覆盖 856 个 artifact，18 个多标签代码。详见 [方法与边界](METHOD.md)、[逐条分析](ARTIFACTS.md) 和 [覆盖校验](coverage_report.json)。

代码与细分开放代码同时保留。以下成员列表包含本数据集每条记录；同一记录可属于多个代码。

|代码|名称|成员数|
|---|---|---:|
|SATD-A|结构、职责与表示重构|216|
|SATD-B|行为、数学或接口正确性|74|
|SATD-C|校验、边界、异常与状态保护|67|
|SATD-D|行为实现或工作流补全|156|
|SATD-E|支持范围与泛化不足|106|
|SATD-F|外部依赖、版本与平台约束|77|
|SATD-G|性能、内存与执行资源|48|
|SATD-H|临时绕行与硬适配|44|
|SATD-I|算法与数据假设适用性|112|
|SATD-J|配置、参数与默认行为|76|
|SATD-K|测试与验证工作|61|
|SATD-L|说明、文档与理解缺口|26|
|SATD-M|冗余、弃用与条件性清理|61|
|SATD-N|持久化、序列化与数据表示契约|41|
|SATD-O|显示、日志与运行可观察性|25|
|SATD-Q|尚未裁决的设计或诊断|244|
|SATD-U|材料不足以细化待办|86|
|SATD-V|未明确承认待偿还问题|26|

## SATD-A · 结构、职责与表示重构

**定义：** 当前实现的模块边界、职责归属、抽象、命名、代码格式或内部表示被要求调整，或存在具体的结构替代候选。

**纳入：** 明确提取、移动、复用、去耦、命名统一、格式整理或内部表示替代；可与未决设计并用。

**排除与边界：** 仅新增行为而无结构变化用 D；单纯执行速度诉求用 G。

**例证：**

- [23shades-0001-aahiieiig](ARTIFACTS.md#row-1)：多个算法共用函数，作者明确承诺后续重构；不是模型算法本身未实现。
- [23shades-0003-aaejjbhji](ARTIFACTS.md#row-3)：作者指出空字典也能满足需求；句子截断，替代方案的完整限制不明。
- [23shades-0006-aaahbghib](ARTIFACTS.md#row-6)：作者希望用正则或其他方案替代 hack，未提供具体处理内容。

**全部成员（逐条证据在链接中）：**

[23shades-0001-aahiieiig](ARTIFACTS.md#row-1), [23shades-0003-aaejjbhji](ARTIFACTS.md#row-3), [23shades-0006-aaahbghib](ARTIFACTS.md#row-6), [23shades-0009-aagdfgjig](ARTIFACTS.md#row-9), [23shades-0017-aaffedgad](ARTIFACTS.md#row-17), [23shades-0025-aajffcjii](ARTIFACTS.md#row-25), [23shades-0026-aajffcjfa](ARTIFACTS.md#row-26), [23shades-0028-aajfejeha](ARTIFACTS.md#row-28), [23shades-0029-aajfejjdb](ARTIFACTS.md#row-29), [23shades-0075-aagdagdia](ARTIFACTS.md#row-75), [23shades-0076-aajfajibh](ARTIFACTS.md#row-76), [23shades-0081-aaaedbhaj](ARTIFACTS.md#row-81), [23shades-0082-aajdcijhj](ARTIFACTS.md#row-82), [23shades-0092-aaeeieida](ARTIFACTS.md#row-92), [23shades-0097-aajhbhjgb](ARTIFACTS.md#row-97), [23shades-0120-aaeihdgig](ARTIFACTS.md#row-120), [23shades-0132-aaeiefagi](ARTIFACTS.md#row-132), [23shades-0154-aajdcgijh](ARTIFACTS.md#row-154), [23shades-0158-aahgacfhf](ARTIFACTS.md#row-158), [23shades-0163-aafbdjhfg](ARTIFACTS.md#row-163), [23shades-0174-aafbhcbbi](ARTIFACTS.md#row-174), [23shades-0177-aahgdgida](ARTIFACTS.md#row-177), [23shades-0197-aadbceejg](ARTIFACTS.md#row-197), [23shades-0198-aajeiegcd](ARTIFACTS.md#row-198), [23shades-0203-aahibhdeh](ARTIFACTS.md#row-203), [23shades-0209-aaihfgcij](ARTIFACTS.md#row-209), [23shades-0217-aaidehfjf](ARTIFACTS.md#row-217), [23shades-0222-aahdficjf](ARTIFACTS.md#row-222), [23shades-0246-aafehehgb](ARTIFACTS.md#row-246), [23shades-0250-aafchcgdb](ARTIFACTS.md#row-250), [23shades-0251-aagjigcgd](ARTIFACTS.md#row-251), [23shades-0252-aafeifgfi](ARTIFACTS.md#row-252), [23shades-0253-aaebaidgd](ARTIFACTS.md#row-253), [23shades-0254-aagigfafa](ARTIFACTS.md#row-254), [23shades-0255-aafegjchi](ARTIFACTS.md#row-255), [23shades-0269-aafehiefj](ARTIFACTS.md#row-269), [23shades-0278-aahhdabij](ARTIFACTS.md#row-278), [23shades-0301-aagacdjjd](ARTIFACTS.md#row-301), [23shades-0303-aahciidhf](ARTIFACTS.md#row-303), [23shades-0307-aajcfhiga](ARTIFACTS.md#row-307), [23shades-0308-aaaecigij](ARTIFACTS.md#row-308), [23shades-0310-aafadaiij](ARTIFACTS.md#row-310), [23shades-0311-aadbcjahd](ARTIFACTS.md#row-311), [23shades-0312-aahddgaji](ARTIFACTS.md#row-312), [23shades-0313-aadfjejae](ARTIFACTS.md#row-313), [23shades-0314-aadfcfhgh](ARTIFACTS.md#row-314), [23shades-0325-aadfjfbei](ARTIFACTS.md#row-325), [23shades-0326-aaeadhaac](ARTIFACTS.md#row-326), [23shades-0328-aadgecacc](ARTIFACTS.md#row-328), [23shades-0329-aaaedaiaa](ARTIFACTS.md#row-329), [23shades-0330-aaheeahhj](ARTIFACTS.md#row-330), [23shades-0336-aafehbbbf](ARTIFACTS.md#row-336), [23shades-0337-aaebaidjj](ARTIFACTS.md#row-337), [23shades-0339-aaifefdce](ARTIFACTS.md#row-339), [23shades-0340-aaebjbdgg](ARTIFACTS.md#row-340), [23shades-0342-aajceeeid](ARTIFACTS.md#row-342), [23shades-0347-aaahgiacg](ARTIFACTS.md#row-347), [23shades-0351-aajbebjea](ARTIFACTS.md#row-351), [23shades-0353-aafehgfdb](ARTIFACTS.md#row-353), [23shades-0354-aagfabaij](ARTIFACTS.md#row-354), [23shades-0358-aajajbadj](ARTIFACTS.md#row-358), [23shades-0367-aadfjffba](ARTIFACTS.md#row-367), [23shades-0373-aagcjhcea](ARTIFACTS.md#row-373), [23shades-0375-aafeihffh](ARTIFACTS.md#row-375), [23shades-0377-aafchfjcg](ARTIFACTS.md#row-377), [23shades-0380-aahddgbgf](ARTIFACTS.md#row-380), [23shades-0381-aagcicfdi](ARTIFACTS.md#row-381), [23shades-0389-aagachejb](ARTIFACTS.md#row-389), [23shades-0393-aaghajbbe](ARTIFACTS.md#row-393), [23shades-0396-aaggjhfeh](ARTIFACTS.md#row-396), [23shades-0397-aahjideha](ARTIFACTS.md#row-397), [23shades-0401-aaegacgid](ARTIFACTS.md#row-401), [23shades-0402-aagibhhbe](ARTIFACTS.md#row-402), [23shades-0404-aahfghdbg](ARTIFACTS.md#row-404), [23shades-0412-aadbbhbgg](ARTIFACTS.md#row-412), [23shades-0415-aajahjjch](ARTIFACTS.md#row-415), [23shades-0416-aaiibahhd](ARTIFACTS.md#row-416), [23shades-0417-aajefdiii](ARTIFACTS.md#row-417), [23shades-0420-aadhgacdi](ARTIFACTS.md#row-420), [23shades-0423-aagifdbgf](ARTIFACTS.md#row-423), [23shades-0424-aadbacfge](ARTIFACTS.md#row-424), [23shades-0433-aaiiccdhb](ARTIFACTS.md#row-433), [23shades-0434-aaifgcjac](ARTIFACTS.md#row-434), [23shades-0446-aaedjcbec](ARTIFACTS.md#row-446), [23shades-0459-aafafahih](ARTIFACTS.md#row-459), [23shades-0470-aaedhgdgd](ARTIFACTS.md#row-470), [23shades-0471-aageachcc](ARTIFACTS.md#row-471), [23shades-0472-aaffdcfdh](ARTIFACTS.md#row-472), [23shades-0473-aagacefai](ARTIFACTS.md#row-473), [23shades-0474-aaeebgdbh](ARTIFACTS.md#row-474), [23shades-0483-aagbdjfdj](ARTIFACTS.md#row-483), [23shades-0487-aahgfihag](ARTIFACTS.md#row-487), [23shades-0494-aajfbgjhi](ARTIFACTS.md#row-494), [23shades-0496-aaeedfhcd](ARTIFACTS.md#row-496), [23shades-0499-aadajcbia](ARTIFACTS.md#row-499), [23shades-0500-aaeiedggi](ARTIFACTS.md#row-500), [23shades-0501-aaedhahfd](ARTIFACTS.md#row-501), [23shades-0502-aaidjgfeg](ARTIFACTS.md#row-502), [23shades-0506-aaeieejja](ARTIFACTS.md#row-506), [23shades-0509-aaacggdch](ARTIFACTS.md#row-509), [23shades-0511-aahidaefh](ARTIFACTS.md#row-511), [23shades-0521-aaiiiajei](ARTIFACTS.md#row-521), [23shades-0526-aagejejha](ARTIFACTS.md#row-526), [23shades-0556-aadhfidia](ARTIFACTS.md#row-556), [23shades-0557-aajejbfha](ARTIFACTS.md#row-557), [23shades-0561-aaegihffd](ARTIFACTS.md#row-561), [23shades-0566-aaiffabhh](ARTIFACTS.md#row-566), [23shades-0574-aaideghdd](ARTIFACTS.md#row-574), [23shades-0575-aaejcccgj](ARTIFACTS.md#row-575), [23shades-0578-aaeiefhaa](ARTIFACTS.md#row-578), [23shades-0579-aagcdfcie](ARTIFACTS.md#row-579), [23shades-0580-aaffdhejj](ARTIFACTS.md#row-580), [23shades-0581-aaeieedge](ARTIFACTS.md#row-581), [23shades-0582-aagbdibae](ARTIFACTS.md#row-582), [23shades-0593-aadbehbcf](ARTIFACTS.md#row-593), [23shades-0594-aafbjgjcd](ARTIFACTS.md#row-594), [23shades-0600-aafhihecd](ARTIFACTS.md#row-600), [23shades-0602-aahidaegb](ARTIFACTS.md#row-602), [23shades-0603-aahgegeef](ARTIFACTS.md#row-603), [23shades-0609-aagcdcjae](ARTIFACTS.md#row-609), [23shades-0610-aaegfjdjb](ARTIFACTS.md#row-610), [23shades-0612-aagfbfdbb](ARTIFACTS.md#row-612), [23shades-0617-aafigfjii](ARTIFACTS.md#row-617), [23shades-0619-aaffecghg](ARTIFACTS.md#row-619), [23shades-0632-aaiffchcj](ARTIFACTS.md#row-632), [23shades-0633-aagcdfdia](ARTIFACTS.md#row-633), [23shades-0634-aaebhhdjf](ARTIFACTS.md#row-634), [23shades-0638-aaghjajha](ARTIFACTS.md#row-638), [23shades-0640-aaghjahhi](ARTIFACTS.md#row-640), [23shades-0641-aaefghgda](ARTIFACTS.md#row-641), [23shades-0644-aaibjebjh](ARTIFACTS.md#row-644), [23shades-0650-aagejhgfd](ARTIFACTS.md#row-650), [23shades-0651-aagfjdjeg](ARTIFACTS.md#row-651), [23shades-0652-aadbaaejd](ARTIFACTS.md#row-652), [23shades-0657-aajdbjejb](ARTIFACTS.md#row-657), [23shades-0658-aafeaihbg](ARTIFACTS.md#row-658), [23shades-0670-aaeeijdhi](ARTIFACTS.md#row-670), [23shades-0671-aaedghfjd](ARTIFACTS.md#row-671), [23shades-0672-aagahbjib](ARTIFACTS.md#row-672), [23shades-0673-aaiecbahd](ARTIFACTS.md#row-673), [23shades-0674-aagiejcbj](ARTIFACTS.md#row-674), [23shades-0676-aaicjgced](ARTIFACTS.md#row-676), [23shades-0677-aaefecjfa](ARTIFACTS.md#row-677), [23shades-0678-aafeaiffi](ARTIFACTS.md#row-678), [23shades-0679-aaefbfhbj](ARTIFACTS.md#row-679), [23shades-0681-aaibgbejh](ARTIFACTS.md#row-681), [23shades-0683-aaeihdfda](ARTIFACTS.md#row-683), [23shades-0684-aaiejaeea](ARTIFACTS.md#row-684), [23shades-0686-aagbiaaje](ARTIFACTS.md#row-686), [23shades-0688-aafibegea](ARTIFACTS.md#row-688), [23shades-0689-aaacjhcjh](ARTIFACTS.md#row-689), [23shades-0693-aajacfjhb](ARTIFACTS.md#row-693), [23shades-0694-aaidhabjj](ARTIFACTS.md#row-694), [23shades-0695-aaeeihicj](ARTIFACTS.md#row-695), [23shades-0699-aaffeacij](ARTIFACTS.md#row-699), [23shades-0700-aaeejihee](ARTIFACTS.md#row-700), [23shades-0701-aaefaahhg](ARTIFACTS.md#row-701), [23shades-0702-aahcjejhi](ARTIFACTS.md#row-702), [23shades-0706-aaidjfjdb](ARTIFACTS.md#row-706), [23shades-0707-aaeiefjai](ARTIFACTS.md#row-707), [23shades-0708-aahjejchc](ARTIFACTS.md#row-708), [23shades-0711-aafbjiedd](ARTIFACTS.md#row-711), [23shades-0712-aajaighgc](ARTIFACTS.md#row-712), [23shades-0713-aaahbbdbf](ARTIFACTS.md#row-713), [23shades-0724-aaidgiiag](ARTIFACTS.md#row-724), [23shades-0725-aahicjieh](ARTIFACTS.md#row-725), [23shades-0731-aafiggaje](ARTIFACTS.md#row-731), [23shades-0734-aaifdieif](ARTIFACTS.md#row-734), [23shades-0738-aagaeeefj](ARTIFACTS.md#row-738), [23shades-0739-aaibgjddj](ARTIFACTS.md#row-739), [23shades-0742-aahedhicb](ARTIFACTS.md#row-742), [23shades-0744-aaefediad](ARTIFACTS.md#row-744), [23shades-0747-aafighdeg](ARTIFACTS.md#row-747), [23shades-0748-aaidaidid](ARTIFACTS.md#row-748), [23shades-0749-aaihgdiif](ARTIFACTS.md#row-749), [23shades-0753-aaeejgbaa](ARTIFACTS.md#row-753), [23shades-0754-aafibabbi](ARTIFACTS.md#row-754), [23shades-0755-aahdfaija](ARTIFACTS.md#row-755), [23shades-0756-aahegjjea](ARTIFACTS.md#row-756), [23shades-0757-aajdcfhjb](ARTIFACTS.md#row-757), [23shades-0758-aagfbieab](ARTIFACTS.md#row-758), [23shades-0760-aajbhfbhg](ARTIFACTS.md#row-760), [23shades-0761-aaffdjjaa](ARTIFACTS.md#row-761), [23shades-0762-aaedhjhei](ARTIFACTS.md#row-762), [23shades-0765-aaffdgbgi](ARTIFACTS.md#row-765), [23shades-0768-aaahbfbgd](ARTIFACTS.md#row-768), [23shades-0774-aafhiicbj](ARTIFACTS.md#row-774), [23shades-0778-aajfbhgdi](ARTIFACTS.md#row-778), [23shades-0779-aajffiiac](ARTIFACTS.md#row-779), [23shades-0788-aahiebjbd](ARTIFACTS.md#row-788), [23shades-0810-aajficjje](ARTIFACTS.md#row-810), [23shades-0811-aahciiijc](ARTIFACTS.md#row-811), [23shades-0812-aahciiijc](ARTIFACTS.md#row-812), [23shades-0813-aajgefiaf](ARTIFACTS.md#row-813), [23shades-0817-aajfiegif](ARTIFACTS.md#row-817), [23shades-0821-aajgcfgdg](ARTIFACTS.md#row-821), [23shades-0822-aahjfbdfa](ARTIFACTS.md#row-822), [23shades-0824-aajghfgdd](ARTIFACTS.md#row-824), [23shades-0825-aaicfehca](ARTIFACTS.md#row-825), [23shades-0828-aajcadhbi](ARTIFACTS.md#row-828), [23shades-0830-aajfigjji](ARTIFACTS.md#row-830), [23shades-0834-aajgfdhgh](ARTIFACTS.md#row-834), [23shades-0835-aajghfhbf](ARTIFACTS.md#row-835), [23shades-0836-aajfhhbig](ARTIFACTS.md#row-836), [23shades-0839-aaicgfbda](ARTIFACTS.md#row-839), [23shades-0840-aaeidjejd](ARTIFACTS.md#row-840), [23shades-0843-aahjgeiic](ARTIFACTS.md#row-843), [23shades-0844-aaibicege](ARTIFACTS.md#row-844), [23shades-0847-aagbgfjfe](ARTIFACTS.md#row-847), [23shades-0848-aahiefidd](ARTIFACTS.md#row-848), [23shades-0849-aaibjdjdc](ARTIFACTS.md#row-849), [23shades-0850-aahighbdb](ARTIFACTS.md#row-850), [23shades-0852-aaibijdfi](ARTIFACTS.md#row-852), [23shades-0853-aaeigcjdd](ARTIFACTS.md#row-853), [23shades-0854-aaeieedfd](ARTIFACTS.md#row-854), [23shades-0856-aaicaiffi](ARTIFACTS.md#row-856)

## SATD-B · 行为、数学或接口正确性

**定义：** 注释指出行为错误、结果不一致、契约违背或具体正确性风险。

**纳入：** 明确错误与有对象的疑似错误均纳入，但备忘录必须区分确定、疑问和条件性。

**排除与边界：** 仅 TODO 或一般优化不纳入；尚未支持的新范围用 E。

**例证：**

- [23shades-0004-aaejjacgf](ARTIFACTS.md#row-4)：US 无法容纳某些完整数值；不推断 US 具体类型或位宽。
- [23shades-0007-aaaegfgeb](ARTIFACTS.md#row-7)：要求 concat 前 reverse bw；bw 含义缺失，不推断具体网络结构。
- [23shades-0030-aaedcebdc](ARTIFACTS.md#row-30)：作者明确称 bug，predict_proba 不应 change；具体改变对象截断。

**全部成员（逐条证据在链接中）：**

[23shades-0004-aaejjacgf](ARTIFACTS.md#row-4), [23shades-0007-aaaegfgeb](ARTIFACTS.md#row-7), [23shades-0030-aaedcebdc](ARTIFACTS.md#row-30), [23shades-0034-aaibjcgbi](ARTIFACTS.md#row-34), [23shades-0035-aahfiaifg](ARTIFACTS.md#row-35), [23shades-0055-aafeacaha](ARTIFACTS.md#row-55), [23shades-0059-aacjfgieb](ARTIFACTS.md#row-59), [23shades-0074-aajfadgji](ARTIFACTS.md#row-74), [23shades-0100-aafidfjjc](ARTIFACTS.md#row-100), [23shades-0101-aagfjecej](ARTIFACTS.md#row-101), [23shades-0102-aajeddgaa](ARTIFACTS.md#row-102), [23shades-0131-aaffecjha](ARTIFACTS.md#row-131), [23shades-0162-aaifgcjei](ARTIFACTS.md#row-162), [23shades-0170-aaigfaibj](ARTIFACTS.md#row-170), [23shades-0201-aaffefhhb](ARTIFACTS.md#row-201), [23shades-0217-aaidehfjf](ARTIFACTS.md#row-217), [23shades-0239-aaggfgbbj](ARTIFACTS.md#row-239), [23shades-0274-aaebjhccj](ARTIFACTS.md#row-274), [23shades-0283-aahiifcef](ARTIFACTS.md#row-283), [23shades-0296-aahiigecd](ARTIFACTS.md#row-296), [23shades-0365-aaebabejj](ARTIFACTS.md#row-365), [23shades-0368-aafchdiaf](ARTIFACTS.md#row-368), [23shades-0372-aadfcefca](ARTIFACTS.md#row-372), [23shades-0384-aahcgeaed](ARTIFACTS.md#row-384), [23shades-0387-aahiiejjd](ARTIFACTS.md#row-387), [23shades-0395-aaggjcebg](ARTIFACTS.md#row-395), [23shades-0411-aaiafgfcj](ARTIFACTS.md#row-411), [23shades-0419-aadheehad](ARTIFACTS.md#row-419), [23shades-0436-aafadcigh](ARTIFACTS.md#row-436), [23shades-0451-aaifgfeag](ARTIFACTS.md#row-451), [23shades-0460-aagfecjfe](ARTIFACTS.md#row-460), [23shades-0484-aabgdhcid](ARTIFACTS.md#row-484), [23shades-0507-aafbciiij](ARTIFACTS.md#row-507), [23shades-0508-aafhhaijc](ARTIFACTS.md#row-508), [23shades-0512-aaicabdbe](ARTIFACTS.md#row-512), [23shades-0517-aafafcgbj](ARTIFACTS.md#row-517), [23shades-0539-aaheefgfd](ARTIFACTS.md#row-539), [23shades-0543-aahggbife](ARTIFACTS.md#row-543), [23shades-0544-aaedabagi](ARTIFACTS.md#row-544), [23shades-0549-aaeieddbj](ARTIFACTS.md#row-549), [23shades-0554-aahjdcjgg](ARTIFACTS.md#row-554), [23shades-0559-aafdibbge](ARTIFACTS.md#row-559), [23shades-0574-aaideghdd](ARTIFACTS.md#row-574), [23shades-0586-aagdaagij](ARTIFACTS.md#row-586), [23shades-0613-aadhcgief](ARTIFACTS.md#row-613), [23shades-0618-aaebbbhhb](ARTIFACTS.md#row-618), [23shades-0622-aagagihei](ARTIFACTS.md#row-622), [23shades-0623-aahijjdcb](ARTIFACTS.md#row-623), [23shades-0625-aaefhdgid](ARTIFACTS.md#row-625), [23shades-0626-aadajbgbb](ARTIFACTS.md#row-626), [23shades-0627-aaidgcaed](ARTIFACTS.md#row-627), [23shades-0649-aaeidhcjb](ARTIFACTS.md#row-649), [23shades-0675-aadagdejg](ARTIFACTS.md#row-675), [23shades-0688-aafibegea](ARTIFACTS.md#row-688), [23shades-0696-aaiihdfjc](ARTIFACTS.md#row-696), [23shades-0709-aaedaedaa](ARTIFACTS.md#row-709), [23shades-0712-aajaighgc](ARTIFACTS.md#row-712), [23shades-0726-aadejjjdj](ARTIFACTS.md#row-726), [23shades-0729-aafafjdeg](ARTIFACTS.md#row-729), [23shades-0732-aahjacheg](ARTIFACTS.md#row-732), [23shades-0740-aagdjibjh](ARTIFACTS.md#row-740), [23shades-0773-aahgddjfi](ARTIFACTS.md#row-773), [23shades-0774-aafhiicbj](ARTIFACTS.md#row-774), [23shades-0775-aahjejdja](ARTIFACTS.md#row-775), [23shades-0803-aaichjjjg](ARTIFACTS.md#row-803), [23shades-0815-aajfiebah](ARTIFACTS.md#row-815), [23shades-0819-aageebhag](ARTIFACTS.md#row-819), [23shades-0820-aajggjjdf](ARTIFACTS.md#row-820), [23shades-0831-aajghfcje](ARTIFACTS.md#row-831), [23shades-0832-aajfibdif](ARTIFACTS.md#row-832), [23shades-0837-aaicicaia](ARTIFACTS.md#row-837), [23shades-0839-aaicgfbda](ARTIFACTS.md#row-839), [23shades-0850-aahighbdb](ARTIFACTS.md#row-850), [23shades-0851-aajgdbgid](ARTIFACTS.md#row-851)

## SATD-C · 校验、边界、异常与状态保护

**定义：** 需要验证输入、形状、状态、生命周期或错误路径，并保护共享状态及边界条件。

**纳入：** 空值、除零、类型形状检查、并发锁、异常策略、完整性检查以及相关待验证风险。

**排除与边界：** 新增单元测试用 K；train/test 数据划分本身不属测试。

**例证：**

- [23shades-0048-aagaijehb](ARTIFACTS.md#row-48)：未来需要验证参数间兼容性。
- [23shades-0062-aagachfba](ARTIFACTS.md#row-62)：应检查 variation 是否已存在。
- [23shades-0063-aaaedhbbd](ARTIFACTS.md#row-63)：需保证传给 _pool.step 的是 ndarray。

**全部成员（逐条证据在链接中）：**

[23shades-0048-aagaijehb](ARTIFACTS.md#row-48), [23shades-0062-aagachfba](ARTIFACTS.md#row-62), [23shades-0063-aaaedhbbd](ARTIFACTS.md#row-63), [23shades-0079-aahhbbhjc](ARTIFACTS.md#row-79), [23shades-0114-aafeaaejc](ARTIFACTS.md#row-114), [23shades-0200-aadhaidcc](ARTIFACTS.md#row-200), [23shades-0205-aaiibgbdc](ARTIFACTS.md#row-205), [23shades-0219-aaeefiahb](ARTIFACTS.md#row-219), [23shades-0227-aagfchifa](ARTIFACTS.md#row-227), [23shades-0232-aaeibhbhc](ARTIFACTS.md#row-232), [23shades-0235-aaebjiiah](ARTIFACTS.md#row-235), [23shades-0258-aagchjdcj](ARTIFACTS.md#row-258), [23shades-0259-aajbgadgf](ARTIFACTS.md#row-259), [23shades-0260-aadfcehfi](ARTIFACTS.md#row-260), [23shades-0261-aaaiefadd](ARTIFACTS.md#row-261), [23shades-0262-aafciifib](ARTIFACTS.md#row-262), [23shades-0263-aadbfihhc](ARTIFACTS.md#row-263), [23shades-0266-aaedhfhae](ARTIFACTS.md#row-266), [23shades-0273-aaebjbbei](ARTIFACTS.md#row-273), [23shades-0323-aaffbcfif](ARTIFACTS.md#row-323), [23shades-0370-aafeghegj](ARTIFACTS.md#row-370), [23shades-0382-aaffbchga](ARTIFACTS.md#row-382), [23shades-0383-aajdbcadb](ARTIFACTS.md#row-383), [23shades-0398-aajabjhjb](ARTIFACTS.md#row-398), [23shades-0439-aaeeicdeh](ARTIFACTS.md#row-439), [23shades-0451-aaifgfeag](ARTIFACTS.md#row-451), [23shades-0475-aahjabdbh](ARTIFACTS.md#row-475), [23shades-0476-aaeigccaj](ARTIFACTS.md#row-476), [23shades-0477-aafibaccg](ARTIFACTS.md#row-477), [23shades-0478-aahdfbbhc](ARTIFACTS.md#row-478), [23shades-0479-aahhdgbbd](ARTIFACTS.md#row-479), [23shades-0480-aaeiedgfj](ARTIFACTS.md#row-480), [23shades-0481-aaeifhdjh](ARTIFACTS.md#row-481), [23shades-0482-aaebhaafj](ARTIFACTS.md#row-482), [23shades-0485-aafhihfed](ARTIFACTS.md#row-485), [23shades-0497-aaeidiecf](ARTIFACTS.md#row-497), [23shades-0517-aafafcgbj](ARTIFACTS.md#row-517), [23shades-0518-aaaegjcch](ARTIFACTS.md#row-518), [23shades-0531-aaffefcib](ARTIFACTS.md#row-531), [23shades-0532-aahddjbah](ARTIFACTS.md#row-532), [23shades-0537-aaeidjjhd](ARTIFACTS.md#row-537), [23shades-0549-aaeieddbj](ARTIFACTS.md#row-549), [23shades-0552-aabfjgehb](ARTIFACTS.md#row-552), [23shades-0554-aahjdcjgg](ARTIFACTS.md#row-554), [23shades-0562-aaeiefhcb](ARTIFACTS.md#row-562), [23shades-0567-aadbcjbcc](ARTIFACTS.md#row-567), [23shades-0596-aagbdjhgb](ARTIFACTS.md#row-596), [23shades-0598-aahiijgjf](ARTIFACTS.md#row-598), [23shades-0610-aaegfjdjb](ARTIFACTS.md#row-610), [23shades-0611-aajejahfe](ARTIFACTS.md#row-611), [23shades-0621-aaeiefhcd](ARTIFACTS.md#row-621), [23shades-0639-aaecjeidf](ARTIFACTS.md#row-639), [23shades-0647-aaidbfgae](ARTIFACTS.md#row-647), [23shades-0692-aajcfiaid](ARTIFACTS.md#row-692), [23shades-0703-aagaahfid](ARTIFACTS.md#row-703), [23shades-0741-aaigbchde](ARTIFACTS.md#row-741), [23shades-0764-aadiicibd](ARTIFACTS.md#row-764), [23shades-0773-aahgddjfi](ARTIFACTS.md#row-773), [23shades-0791-aahgcaaac](ARTIFACTS.md#row-791), [23shades-0797-aafafjdfg](ARTIFACTS.md#row-797), [23shades-0809-aajfhgecg](ARTIFACTS.md#row-809), [23shades-0815-aajfiebah](ARTIFACTS.md#row-815), [23shades-0821-aajgcfgdg](ARTIFACTS.md#row-821), [23shades-0843-aahjgeiic](ARTIFACTS.md#row-843), [23shades-0847-aagbgfjfe](ARTIFACTS.md#row-847), [23shades-0848-aahiefidd](ARTIFACTS.md#row-848), [23shades-0854-aaeieedfd](ARTIFACTS.md#row-854)

## SATD-D · 行为实现或工作流补全

**定义：** 存在待增加、启用、补齐或扩展的计算、数据处理、持久化或交互行为。

**纳入：** 具体功能待办与明确 implement/incomplete 即使指代缺失；范围不足可并 E。

**排除与边界：** 只有名称和 TODO 且不知动作时用 U；不把链接中的功能认作已读证据。

**例证：**

- [23shades-0008-aagcbjjcd](ARTIFACTS.md#row-8)：landmarks 只未扩展到 validation/test；明确因当日疲劳推迟，不是单元测试缺失。
- [23shades-0012-aafaehach](ARTIFACTS.md#row-12)：name 缺失时拟采用 functionality.__name__。
- [23shades-0021-aadbhiccj](ARTIFACTS.md#row-21)：Frontend 和 Model 尚待纳入该 workflow。

**全部成员（逐条证据在链接中）：**

[23shades-0008-aagcbjjcd](ARTIFACTS.md#row-8), [23shades-0012-aafaehach](ARTIFACTS.md#row-12), [23shades-0021-aadbhiccj](ARTIFACTS.md#row-21), [23shades-0036-aaibigjdc](ARTIFACTS.md#row-36), [23shades-0043-aaehiefac](ARTIFACTS.md#row-43), [23shades-0044-aaeibhiie](ARTIFACTS.md#row-44), [23shades-0049-aagaggihd](ARTIFACTS.md#row-49), [23shades-0054-aadaieabb](ARTIFACTS.md#row-54), [23shades-0061-aagfgggge](ARTIFACTS.md#row-61), [23shades-0084-aajdcifej](ARTIFACTS.md#row-84), [23shades-0093-aaffafejc](ARTIFACTS.md#row-93), [23shades-0094-aadaidhdg](ARTIFACTS.md#row-94), [23shades-0101-aagfjecej](ARTIFACTS.md#row-101), [23shades-0105-aafahfcgh](ARTIFACTS.md#row-105), [23shades-0121-aadhbadhi](ARTIFACTS.md#row-121), [23shades-0123-aagfeiiaj](ARTIFACTS.md#row-123), [23shades-0140-aaiijdebd](ARTIFACTS.md#row-140), [23shades-0157-aafejhiea](ARTIFACTS.md#row-157), [23shades-0159-aajbiahbe](ARTIFACTS.md#row-159), [23shades-0206-aaegahgbf](ARTIFACTS.md#row-206), [23shades-0212-aahhiefcg](ARTIFACTS.md#row-212), [23shades-0213-aahhiidji](ARTIFACTS.md#row-213), [23shades-0214-aafhjjgee](ARTIFACTS.md#row-214), [23shades-0217-aaidehfjf](ARTIFACTS.md#row-217), [23shades-0225-aaidcjdhd](ARTIFACTS.md#row-225), [23shades-0226-aafdjfjab](ARTIFACTS.md#row-226), [23shades-0229-aadfjchjf](ARTIFACTS.md#row-229), [23shades-0230-aahjecdhj](ARTIFACTS.md#row-230), [23shades-0233-aagaagfeh](ARTIFACTS.md#row-233), [23shades-0234-aahiihjjg](ARTIFACTS.md#row-234), [23shades-0237-aafcgegjb](ARTIFACTS.md#row-237), [23shades-0240-aagaagfeg](ARTIFACTS.md#row-240), [23shades-0241-aajfahgcg](ARTIFACTS.md#row-241), [23shades-0244-aafhgihee](ARTIFACTS.md#row-244), [23shades-0245-aafehehfi](ARTIFACTS.md#row-245), [23shades-0248-aagjjacbh](ARTIFACTS.md#row-248), [23shades-0264-aahjaaihb](ARTIFACTS.md#row-264), [23shades-0265-aaejhfaai](ARTIFACTS.md#row-265), [23shades-0267-aajgajdca](ARTIFACTS.md#row-267), [23shades-0268-aadfdgaei](ARTIFACTS.md#row-268), [23shades-0272-aagjifffj](ARTIFACTS.md#row-272), [23shades-0276-aaadbjbdj](ARTIFACTS.md#row-276), [23shades-0277-aahiiefbi](ARTIFACTS.md#row-277), [23shades-0287-aagdffgjh](ARTIFACTS.md#row-287), [23shades-0297-aafhgjiha](ARTIFACTS.md#row-297), [23shades-0298-aafhhaidh](ARTIFACTS.md#row-298), [23shades-0299-aahiiegbc](ARTIFACTS.md#row-299), [23shades-0300-aaejhiaeb](ARTIFACTS.md#row-300), [23shades-0302-aahiiggad](ARTIFACTS.md#row-302), [23shades-0306-aafchbaid](ARTIFACTS.md#row-306), [23shades-0343-aaadbhidf](ARTIFACTS.md#row-343), [23shades-0344-aafejacii](ARTIFACTS.md#row-344), [23shades-0345-aafagebef](ARTIFACTS.md#row-345), [23shades-0346-aahiiefbj](ARTIFACTS.md#row-346), [23shades-0349-aagciihdj](ARTIFACTS.md#row-349), [23shades-0350-aadfcfcca](ARTIFACTS.md#row-350), [23shades-0355-aajgdiheg](ARTIFACTS.md#row-355), [23shades-0356-aaeidhdde](ARTIFACTS.md#row-356), [23shades-0362-aahchacde](ARTIFACTS.md#row-362), [23shades-0374-aahiiffci](ARTIFACTS.md#row-374), [23shades-0387-aahiiejjd](ARTIFACTS.md#row-387), [23shades-0399-aaijchbde](ARTIFACTS.md#row-399), [23shades-0400-aaigebhce](ARTIFACTS.md#row-400), [23shades-0407-aaijdefji](ARTIFACTS.md#row-407), [23shades-0408-aaijddhbj](ARTIFACTS.md#row-408), [23shades-0409-aaijddeia](ARTIFACTS.md#row-409), [23shades-0410-aaijddddf](ARTIFACTS.md#row-410), [23shades-0437-aaeacgafj](ARTIFACTS.md#row-437), [23shades-0441-aaefegech](ARTIFACTS.md#row-441), [23shades-0442-aabgdbaje](ARTIFACTS.md#row-442), [23shades-0443-aaeabdbie](ARTIFACTS.md#row-443), [23shades-0444-aaeabdbjb](ARTIFACTS.md#row-444), [23shades-0445-aaeaacdga](ARTIFACTS.md#row-445), [23shades-0447-aaecjghji](ARTIFACTS.md#row-447), [23shades-0448-aafhedifh](ARTIFACTS.md#row-448), [23shades-0449-aajdcigce](ARTIFACTS.md#row-449), [23shades-0455-aaeiibiib](ARTIFACTS.md#row-455), [23shades-0461-aaidhjgaj](ARTIFACTS.md#row-461), [23shades-0465-aahddhhhe](ARTIFACTS.md#row-465), [23shades-0466-aahddhiba](ARTIFACTS.md#row-466), [23shades-0468-aagaidebh](ARTIFACTS.md#row-468), [23shades-0469-aaahbfbig](ARTIFACTS.md#row-469), [23shades-0488-aaahbjgif](ARTIFACTS.md#row-488), [23shades-0491-aadggcdfe](ARTIFACTS.md#row-491), [23shades-0493-aagbjbdaa](ARTIFACTS.md#row-493), [23shades-0495-aafjhfhii](ARTIFACTS.md#row-495), [23shades-0505-aadgfccbh](ARTIFACTS.md#row-505), [23shades-0510-aadjgaaid](ARTIFACTS.md#row-510), [23shades-0512-aaicabdbe](ARTIFACTS.md#row-512), [23shades-0516-aajegiabc](ARTIFACTS.md#row-516), [23shades-0519-aajfiibhb](ARTIFACTS.md#row-519), [23shades-0533-aahdfajdh](ARTIFACTS.md#row-533), [23shades-0534-aaeebgfej](ARTIFACTS.md#row-534), [23shades-0535-aaebchhbi](ARTIFACTS.md#row-535), [23shades-0536-aaeidieej](ARTIFACTS.md#row-536), [23shades-0542-aagbabhfa](ARTIFACTS.md#row-542), [23shades-0546-aaiejgdgf](ARTIFACTS.md#row-546), [23shades-0548-aajgceiba](ARTIFACTS.md#row-548), [23shades-0550-aaahcdafe](ARTIFACTS.md#row-550), [23shades-0551-aajdbhhhh](ARTIFACTS.md#row-551), [23shades-0553-aadgfdibb](ARTIFACTS.md#row-553), [23shades-0555-aaeidjhhg](ARTIFACTS.md#row-555), [23shades-0564-aafjicajb](ARTIFACTS.md#row-564), [23shades-0565-aajfdefij](ARTIFACTS.md#row-565), [23shades-0566-aaiffabhh](ARTIFACTS.md#row-566), [23shades-0568-aafbihhej](ARTIFACTS.md#row-568), [23shades-0569-aahhhfjei](ARTIFACTS.md#row-569), [23shades-0570-aagaghfef](ARTIFACTS.md#row-570), [23shades-0572-aaachjhaj](ARTIFACTS.md#row-572), [23shades-0583-aaiecfecg](ARTIFACTS.md#row-583), [23shades-0609-aagcdcjae](ARTIFACTS.md#row-609), [23shades-0615-aabgddhjh](ARTIFACTS.md#row-615), [23shades-0616-aafcachjb](ARTIFACTS.md#row-616), [23shades-0622-aagagihei](ARTIFACTS.md#row-622), [23shades-0625-aaefhdgid](ARTIFACTS.md#row-625), [23shades-0626-aadajbgbb](ARTIFACTS.md#row-626), [23shades-0628-aaifedeec](ARTIFACTS.md#row-628), [23shades-0629-aaeajfcic](ARTIFACTS.md#row-629), [23shades-0630-aaeigcjfb](ARTIFACTS.md#row-630), [23shades-0631-aaecaicdb](ARTIFACTS.md#row-631), [23shades-0635-aaedbcjji](ARTIFACTS.md#row-635), [23shades-0636-aaibjdfgf](ARTIFACTS.md#row-636), [23shades-0638-aaghjajha](ARTIFACTS.md#row-638), [23shades-0642-aahcigdjj](ARTIFACTS.md#row-642), [23shades-0646-aagaijdhc](ARTIFACTS.md#row-646), [23shades-0654-aagbifedh](ARTIFACTS.md#row-654), [23shades-0675-aadagdejg](ARTIFACTS.md#row-675), [23shades-0682-aaejbieif](ARTIFACTS.md#row-682), [23shades-0687-aagbjaigc](ARTIFACTS.md#row-687), [23shades-0696-aaiihdfjc](ARTIFACTS.md#row-696), [23shades-0698-aagdjigjj](ARTIFACTS.md#row-698), [23shades-0710-aaeiiihac](ARTIFACTS.md#row-710), [23shades-0714-aaadhcgbc](ARTIFACTS.md#row-714), [23shades-0715-aaeiedfaj](ARTIFACTS.md#row-715), [23shades-0716-aacjgagdb](ARTIFACTS.md#row-716), [23shades-0743-aahgffjcf](ARTIFACTS.md#row-743), [23shades-0746-aajgdgaed](ARTIFACTS.md#row-746), [23shades-0755-aahdfaija](ARTIFACTS.md#row-755), [23shades-0756-aahegjjea](ARTIFACTS.md#row-756), [23shades-0767-aaiefdgde](ARTIFACTS.md#row-767), [23shades-0770-aadhddfhh](ARTIFACTS.md#row-770), [23shades-0780-aaididbfa](ARTIFACTS.md#row-780), [23shades-0782-aaahbahcg](ARTIFACTS.md#row-782), [23shades-0783-aagbcgbif](ARTIFACTS.md#row-783), [23shades-0786-aahddigdj](ARTIFACTS.md#row-786), [23shades-0787-aafhfhjbf](ARTIFACTS.md#row-787), [23shades-0789-aahicagej](ARTIFACTS.md#row-789), [23shades-0790-aahicaeda](ARTIFACTS.md#row-790), [23shades-0793-aahefcehd](ARTIFACTS.md#row-793), [23shades-0804-aajgccaef](ARTIFACTS.md#row-804), [23shades-0805-aajfiefig](ARTIFACTS.md#row-805), [23shades-0816-aajgefjja](ARTIFACTS.md#row-816), [23shades-0817-aajfiegif](ARTIFACTS.md#row-817), [23shades-0833-aajggbgdc](ARTIFACTS.md#row-833), [23shades-0838-aaeidjach](ARTIFACTS.md#row-838), [23shades-0845-aaibjdjdj](ARTIFACTS.md#row-845)

## SATD-E · 支持范围与泛化不足

**定义：** 实现仅覆盖部分输入、类型、模型、格式、设备或场景，需扩展或核实覆盖。

**纳入：** 明确缺少的类型/分支/模型族及可辨识的覆盖疑问。

**排除与边界：** 没有覆盖对象的一般改进不纳入；版本或外部 API 限制另加 F。

**例证：**

- [23shades-0013-aaebbeedd](ARTIFACTS.md#row-13)：其他 bases 尚未被处理；不推断 bases 是数制还是父类。
- [23shades-0015-aaibjbide](ARTIFACTS.md#row-15)：需对全部模型加入 intercept；intercept 的具体语义不明。
- [23shades-0016-aadfachjd](ARTIFACTS.md#row-16)：当前只支持 SGD，希望增加其他训练优化器；不属于执行性能证据。

**全部成员（逐条证据在链接中）：**

[23shades-0013-aaebbeedd](ARTIFACTS.md#row-13), [23shades-0015-aaibjbide](ARTIFACTS.md#row-15), [23shades-0016-aadfachjd](ARTIFACTS.md#row-16), [23shades-0024-aaeibiccf](ARTIFACTS.md#row-24), [23shades-0037-aajffhihe](ARTIFACTS.md#row-37), [23shades-0039-aaehiecae](ARTIFACTS.md#row-39), [23shades-0049-aagaggihd](ARTIFACTS.md#row-49), [23shades-0068-aaagiadgf](ARTIFACTS.md#row-68), [23shades-0077-aaicecaej](ARTIFACTS.md#row-77), [23shades-0099-aaibjjjbc](ARTIFACTS.md#row-99), [23shades-0105-aafahfcgh](ARTIFACTS.md#row-105), [23shades-0125-aaahbjjic](ARTIFACTS.md#row-125), [23shades-0126-aaeiedjia](ARTIFACTS.md#row-126), [23shades-0131-aaffecjha](ARTIFACTS.md#row-131), [23shades-0170-aaigfaibj](ARTIFACTS.md#row-170), [23shades-0200-aadhaidcc](ARTIFACTS.md#row-200), [23shades-0206-aaegahgbf](ARTIFACTS.md#row-206), [23shades-0211-aajeacdfg](ARTIFACTS.md#row-211), [23shades-0212-aahhiefcg](ARTIFACTS.md#row-212), [23shades-0213-aahhiidji](ARTIFACTS.md#row-213), [23shades-0214-aafhjjgee](ARTIFACTS.md#row-214), [23shades-0224-aadajefje](ARTIFACTS.md#row-224), [23shades-0229-aadfjchjf](ARTIFACTS.md#row-229), [23shades-0237-aafcgegjb](ARTIFACTS.md#row-237), [23shades-0241-aajfahgcg](ARTIFACTS.md#row-241), [23shades-0244-aafhgihee](ARTIFACTS.md#row-244), [23shades-0247-aahiiegaf](ARTIFACTS.md#row-247), [23shades-0267-aajgajdca](ARTIFACTS.md#row-267), [23shades-0268-aadfdgaei](ARTIFACTS.md#row-268), [23shades-0285-aaacggdfb](ARTIFACTS.md#row-285), [23shades-0290-aaebieajg](ARTIFACTS.md#row-290), [23shades-0291-aaebiddhj](ARTIFACTS.md#row-291), [23shades-0292-aaebieaia](ARTIFACTS.md#row-292), [23shades-0294-aaebjigjj](ARTIFACTS.md#row-294), [23shades-0295-aadghcged](ARTIFACTS.md#row-295), [23shades-0300-aaejhiaeb](ARTIFACTS.md#row-300), [23shades-0302-aahiiggad](ARTIFACTS.md#row-302), [23shades-0319-aafdjgjfa](ARTIFACTS.md#row-319), [23shades-0324-aajcjfcfc](ARTIFACTS.md#row-324), [23shades-0356-aaeidhdde](ARTIFACTS.md#row-356), [23shades-0362-aahchacde](ARTIFACTS.md#row-362), [23shades-0367-aadfjffba](ARTIFACTS.md#row-367), [23shades-0368-aafchdiaf](ARTIFACTS.md#row-368), [23shades-0370-aafeghegj](ARTIFACTS.md#row-370), [23shades-0379-aaecjdbfd](ARTIFACTS.md#row-379), [23shades-0398-aajabjhjb](ARTIFACTS.md#row-398), [23shades-0416-aaiibahhd](ARTIFACTS.md#row-416), [23shades-0437-aaeacgafj](ARTIFACTS.md#row-437), [23shades-0439-aaeeicdeh](ARTIFACTS.md#row-439), [23shades-0441-aaefegech](ARTIFACTS.md#row-441), [23shades-0447-aaecjghji](ARTIFACTS.md#row-447), [23shades-0450-aaegfadac](ARTIFACTS.md#row-450), [23shades-0453-aaefagffe](ARTIFACTS.md#row-453), [23shades-0454-aaefgiijg](ARTIFACTS.md#row-454), [23shades-0455-aaeiibiib](ARTIFACTS.md#row-455), [23shades-0456-aaicfaced](ARTIFACTS.md#row-456), [23shades-0460-aagfecjfe](ARTIFACTS.md#row-460), [23shades-0477-aafibaccg](ARTIFACTS.md#row-477), [23shades-0481-aaeifhdjh](ARTIFACTS.md#row-481), [23shades-0491-aadggcdfe](ARTIFACTS.md#row-491), [23shades-0495-aafjhfhii](ARTIFACTS.md#row-495), [23shades-0498-aagbggddc](ARTIFACTS.md#row-498), [23shades-0499-aadajcbia](ARTIFACTS.md#row-499), [23shades-0510-aadjgaaid](ARTIFACTS.md#row-510), [23shades-0535-aaebchhbi](ARTIFACTS.md#row-535), [23shades-0536-aaeidieej](ARTIFACTS.md#row-536), [23shades-0548-aajgceiba](ARTIFACTS.md#row-548), [23shades-0550-aaahcdafe](ARTIFACTS.md#row-550), [23shades-0551-aajdbhhhh](ARTIFACTS.md#row-551), [23shades-0553-aadgfdibb](ARTIFACTS.md#row-553), [23shades-0554-aahjdcjgg](ARTIFACTS.md#row-554), [23shades-0555-aaeidjhhg](ARTIFACTS.md#row-555), [23shades-0562-aaeiefhcb](ARTIFACTS.md#row-562), [23shades-0583-aaiecfecg](ARTIFACTS.md#row-583), [23shades-0599-aajajcaie](ARTIFACTS.md#row-599), [23shades-0606-aahicghci](ARTIFACTS.md#row-606), [23shades-0610-aaegfjdjb](ARTIFACTS.md#row-610), [23shades-0615-aabgddhjh](ARTIFACTS.md#row-615), [23shades-0621-aaeiefhcd](ARTIFACTS.md#row-621), [23shades-0628-aaifedeec](ARTIFACTS.md#row-628), [23shades-0629-aaeajfcic](ARTIFACTS.md#row-629), [23shades-0630-aaeigcjfb](ARTIFACTS.md#row-630), [23shades-0631-aaecaicdb](ARTIFACTS.md#row-631), [23shades-0639-aaecjeidf](ARTIFACTS.md#row-639), [23shades-0646-aagaijdhc](ARTIFACTS.md#row-646), [23shades-0649-aaeidhcjb](ARTIFACTS.md#row-649), [23shades-0652-aadbaaejd](ARTIFACTS.md#row-652), [23shades-0664-aahidajgj](ARTIFACTS.md#row-664), [23shades-0675-aadagdejg](ARTIFACTS.md#row-675), [23shades-0682-aaejbieif](ARTIFACTS.md#row-682), [23shades-0714-aaadhcgbc](ARTIFACTS.md#row-714), [23shades-0715-aaeiedfaj](ARTIFACTS.md#row-715), [23shades-0716-aacjgagdb](ARTIFACTS.md#row-716), [23shades-0740-aagdjibjh](ARTIFACTS.md#row-740), [23shades-0743-aahgffjcf](ARTIFACTS.md#row-743), [23shades-0746-aajgdgaed](ARTIFACTS.md#row-746), [23shades-0767-aaiefdgde](ARTIFACTS.md#row-767), [23shades-0770-aadhddfhh](ARTIFACTS.md#row-770), [23shades-0786-aahddigdj](ARTIFACTS.md#row-786), [23shades-0805-aajfiefig](ARTIFACTS.md#row-805), [23shades-0807-aahjfbiha](ARTIFACTS.md#row-807), [23shades-0827-aaeiedacj](ARTIFACTS.md#row-827), [23shades-0833-aajggbgdc](ARTIFACTS.md#row-833), [23shades-0838-aaeidjach](ARTIFACTS.md#row-838), [23shades-0845-aaibjdjdj](ARTIFACTS.md#row-845), [23shades-0851-aajgdbgid](ARTIFACTS.md#row-851)

## SATD-F · 外部依赖、版本与平台约束

**定义：** 修改受外部库、版本、后端、平台或调用者契约制约。

**纳入：** 兼容迁移、上游缺陷绕行、版本成熟后清理、依赖声明及跨框架接口适配。

**排除与边界：** 不能仅由库名出现判断存在债务；正常兼容说明应并 V。

**例证：**

- [23shades-0019-aaigjhibg](ARTIFACTS.md#row-19)：只给 fix compatibility，版本和对象缺失。
- [23shades-0020-aaigjhiah](ARTIFACTS.md#row-20)：与前条文本一致但保留独立 artifact；兼容对象不明。
- [23shades-0037-aajffhihe](ARTIFACTS.md#row-37)：unparse 只支持列举的语法结构；拟转 _ast 因编译约快六倍，两项均有明确依据。

**全部成员（逐条证据在链接中）：**

[23shades-0019-aaigjhibg](ARTIFACTS.md#row-19), [23shades-0020-aaigjhiah](ARTIFACTS.md#row-20), [23shades-0037-aajffhihe](ARTIFACTS.md#row-37), [23shades-0040-aaeiahgad](ARTIFACTS.md#row-40), [23shades-0052-aaahbjdic](ARTIFACTS.md#row-52), [23shades-0067-aagbghgdd](ARTIFACTS.md#row-67), [23shades-0087-aaiehhaec](ARTIFACTS.md#row-87), [23shades-0091-aagbejage](ARTIFACTS.md#row-91), [23shades-0108-aaeieagib](ARTIFACTS.md#row-108), [23shades-0120-aaeihdgig](ARTIFACTS.md#row-120), [23shades-0130-aaijaggcb](ARTIFACTS.md#row-130), [23shades-0141-aadbcebbh](ARTIFACTS.md#row-141), [23shades-0146-aafedbhaj](ARTIFACTS.md#row-146), [23shades-0147-aafedbhaj](ARTIFACTS.md#row-147), [23shades-0166-aahcgjcji](ARTIFACTS.md#row-166), [23shades-0167-aagiehhgb](ARTIFACTS.md#row-167), [23shades-0172-aaahfegjh](ARTIFACTS.md#row-172), [23shades-0249-aafbjfdjh](ARTIFACTS.md#row-249), [23shades-0254-aagigfafa](ARTIFACTS.md#row-254), [23shades-0259-aajbgadgf](ARTIFACTS.md#row-259), [23shades-0324-aajcjfcfc](ARTIFACTS.md#row-324), [23shades-0341-aaecghdag](ARTIFACTS.md#row-341), [23shades-0348-aajajehgf](ARTIFACTS.md#row-348), [23shades-0362-aahchacde](ARTIFACTS.md#row-362), [23shades-0379-aaecjdbfd](ARTIFACTS.md#row-379), [23shades-0392-aaghbecie](ARTIFACTS.md#row-392), [23shades-0393-aaghajbbe](ARTIFACTS.md#row-393), [23shades-0397-aahjideha](ARTIFACTS.md#row-397), [23shades-0398-aajabjhjb](ARTIFACTS.md#row-398), [23shades-0415-aajahjjch](ARTIFACTS.md#row-415), [23shades-0416-aaiibahhd](ARTIFACTS.md#row-416), [23shades-0446-aaedjcbec](ARTIFACTS.md#row-446), [23shades-0453-aaefagffe](ARTIFACTS.md#row-453), [23shades-0458-aaeggadce](ARTIFACTS.md#row-458), [23shades-0474-aaeebgdbh](ARTIFACTS.md#row-474), [23shades-0476-aaeigccaj](ARTIFACTS.md#row-476), [23shades-0499-aadajcbia](ARTIFACTS.md#row-499), [23shades-0511-aahidaefh](ARTIFACTS.md#row-511), [23shades-0528-aagejdfdj](ARTIFACTS.md#row-528), [23shades-0543-aahggbife](ARTIFACTS.md#row-543), [23shades-0560-aaifhghej](ARTIFACTS.md#row-560), [23shades-0580-aaffdhejj](ARTIFACTS.md#row-580), [23shades-0586-aagdaagij](ARTIFACTS.md#row-586), [23shades-0619-aaffecghg](ARTIFACTS.md#row-619), [23shades-0640-aaghjahhi](ARTIFACTS.md#row-640), [23shades-0641-aaefghgda](ARTIFACTS.md#row-641), [23shades-0645-aadbbbcgh](ARTIFACTS.md#row-645), [23shades-0659-aaidbebab](ARTIFACTS.md#row-659), [23shades-0664-aahidajgj](ARTIFACTS.md#row-664), [23shades-0667-aahjgdcge](ARTIFACTS.md#row-667), [23shades-0673-aaiecbahd](ARTIFACTS.md#row-673), [23shades-0675-aadagdejg](ARTIFACTS.md#row-675), [23shades-0676-aaicjgced](ARTIFACTS.md#row-676), [23shades-0681-aaibgbejh](ARTIFACTS.md#row-681), [23shades-0682-aaejbieif](ARTIFACTS.md#row-682), [23shades-0683-aaeihdfda](ARTIFACTS.md#row-683), [23shades-0688-aafibegea](ARTIFACTS.md#row-688), [23shades-0713-aaahbbdbf](ARTIFACTS.md#row-713), [23shades-0723-aaeacgjbc](ARTIFACTS.md#row-723), [23shades-0730-aaiheabif](ARTIFACTS.md#row-730), [23shades-0738-aagaeeefj](ARTIFACTS.md#row-738), [23shades-0740-aagdjibjh](ARTIFACTS.md#row-740), [23shades-0761-aaffdjjaa](ARTIFACTS.md#row-761), [23shades-0765-aaffdgbgi](ARTIFACTS.md#row-765), [23shades-0769-aaefhaief](ARTIFACTS.md#row-769), [23shades-0798-aaidjgdji](ARTIFACTS.md#row-798), [23shades-0799-aahjdgiaa](ARTIFACTS.md#row-799), [23shades-0800-aahfigedf](ARTIFACTS.md#row-800), [23shades-0801-aaigijhgj](ARTIFACTS.md#row-801), [23shades-0807-aahjfbiha](ARTIFACTS.md#row-807), [23shades-0813-aajgefiaf](ARTIFACTS.md#row-813), [23shades-0822-aahjfbdfa](ARTIFACTS.md#row-822), [23shades-0825-aaicfehca](ARTIFACTS.md#row-825), [23shades-0827-aaeiedacj](ARTIFACTS.md#row-827), [23shades-0834-aajgfdhgh](ARTIFACTS.md#row-834), [23shades-0835-aajghfhbf](ARTIFACTS.md#row-835), [23shades-0840-aaeidjejd](ARTIFACTS.md#row-840)

## SATD-G · 性能、内存与执行资源

**定义：** 材料明确涉及执行开销、复杂度、内存、并行或性能测量与比较。

**纳入：** 已有瓶颈、候选优化和待测性能分开记述；并发执行约束也可纳入。

**排除与边界：** 训练 optimizer 名称不自动等于性能优化；未经测量不写已提速。

**例证：**

- [23shades-0037-aajffhihe](ARTIFACTS.md#row-37)：unparse 只支持列举的语法结构；拟转 _ast 因编译约快六倍，两项均有明确依据。
- [23shades-0086-aaicdjedb](ARTIFACTS.md#row-86)：指出此处也可用 n_jobs。
- [23shades-0109-aaibiggcj](ARTIFACTS.md#row-109)：作者认为当前 covars representation 会损害 caching。

**全部成员（逐条证据在链接中）：**

[23shades-0037-aajffhihe](ARTIFACTS.md#row-37), [23shades-0086-aaicdjedb](ARTIFACTS.md#row-86), [23shades-0109-aaibiggcj](ARTIFACTS.md#row-109), [23shades-0112-aafafebib](ARTIFACTS.md#row-112), [23shades-0129-aahfhegdd](ARTIFACTS.md#row-129), [23shades-0151-aafjajfdh](ARTIFACTS.md#row-151), [23shades-0152-aafadbdeg](ARTIFACTS.md#row-152), [23shades-0156-aagiedbjj](ARTIFACTS.md#row-156), [23shades-0178-aaifggehf](ARTIFACTS.md#row-178), [23shades-0204-aadhadibe](ARTIFACTS.md#row-204), [23shades-0221-aagabbida](ARTIFACTS.md#row-221), [23shades-0223-aadbceeib](ARTIFACTS.md#row-223), [23shades-0256-aagcicecj](ARTIFACTS.md#row-256), [23shades-0300-aaejhiaeb](ARTIFACTS.md#row-300), [23shades-0321-aadfdfiba](ARTIFACTS.md#row-321), [23shades-0358-aajajbadj](ARTIFACTS.md#row-358), [23shades-0369-aaehaifef](ARTIFACTS.md#row-369), [23shades-0394-aaghdbejg](ARTIFACTS.md#row-394), [23shades-0401-aaegacgid](ARTIFACTS.md#row-401), [23shades-0406-aahhejjge](ARTIFACTS.md#row-406), [23shades-0425-aadbacfde](ARTIFACTS.md#row-425), [23shades-0457-aaeiecejb](ARTIFACTS.md#row-457), [23shades-0464-aaijbfccj](ARTIFACTS.md#row-464), [23shades-0490-aaaefgdbc](ARTIFACTS.md#row-490), [23shades-0492-aafdfijei](ARTIFACTS.md#row-492), [23shades-0494-aajfbgjhi](ARTIFACTS.md#row-494), [23shades-0518-aaaegjcch](ARTIFACTS.md#row-518), [23shades-0584-aadhccedf](ARTIFACTS.md#row-584), [23shades-0591-aajcgfgji](ARTIFACTS.md#row-591), [23shades-0592-aadageajc](ARTIFACTS.md#row-592), [23shades-0631-aaecaicdb](ARTIFACTS.md#row-631), [23shades-0634-aaebhhdjf](ARTIFACTS.md#row-634), [23shades-0663-aaiedhhfd](ARTIFACTS.md#row-663), [23shades-0722-aaiejccah](ARTIFACTS.md#row-722), [23shades-0733-aajacfjii](ARTIFACTS.md#row-733), [23shades-0735-aaihjgafa](ARTIFACTS.md#row-735), [23shades-0736-aafafebhi](ARTIFACTS.md#row-736), [23shades-0737-aafdiegjf](ARTIFACTS.md#row-737), [23shades-0750-aagbdibbb](ARTIFACTS.md#row-750), [23shades-0751-aahgfjfhj](ARTIFACTS.md#row-751), [23shades-0759-aaibihdci](ARTIFACTS.md#row-759), [23shades-0766-aajacaegf](ARTIFACTS.md#row-766), [23shades-0776-aaieahjdd](ARTIFACTS.md#row-776), [23shades-0792-aagigaiii](ARTIFACTS.md#row-792), [23shades-0796-aagdafeic](ARTIFACTS.md#row-796), [23shades-0803-aaichjjjg](ARTIFACTS.md#row-803), [23shades-0823-aahfibidg](ARTIFACTS.md#row-823), [23shades-0836-aajfhhbig](ARTIFACTS.md#row-836)

## SATD-H · 临时绕行与硬适配

**定义：** 当前依靠临时补丁、占位值、硬编码或脆弱约定实现行为。

**纳入：** 明确 hack/workaround 的语义，以及固定值替代真实数据、依赖未公开约定的补偿。

**排除与边界：** 普通常量或仅描述必要操作不自动构成临时债务。

**例证：**

- [23shades-0005-aaebbecaa](ARTIFACTS.md#row-5)：justify-content 失效导致采用 SVG 居中 hack；问题在显示布局。
- [23shades-0006-aaahbghib](ARTIFACTS.md#row-6)：作者希望用正则或其他方案替代 hack，未提供具体处理内容。
- [23shades-0046-aafchcgjg](ARTIFACTS.md#row-46)：上游未提供 confidence，临时填 1；不能当作真实置信度。

**全部成员（逐条证据在链接中）：**

[23shades-0005-aaebbecaa](ARTIFACTS.md#row-5), [23shades-0006-aaahbghib](ARTIFACTS.md#row-6), [23shades-0046-aafchcgjg](ARTIFACTS.md#row-46), [23shades-0053-aaijeahdh](ARTIFACTS.md#row-53), [23shades-0060-aaebhejej](ARTIFACTS.md#row-60), [23shades-0071-aafiaaaih](ARTIFACTS.md#row-71), [23shades-0073-aadfibefa](ARTIFACTS.md#row-73), [23shades-0083-aadggijai](ARTIFACTS.md#row-83), [23shades-0090-aaacjihab](ARTIFACTS.md#row-90), [23shades-0107-aaeejjfbc](ARTIFACTS.md#row-107), [23shades-0108-aaeieagib](ARTIFACTS.md#row-108), [23shades-0125-aaahbjjic](ARTIFACTS.md#row-125), [23shades-0135-aahfgjaff](ARTIFACTS.md#row-135), [23shades-0136-aahhfejii](ARTIFACTS.md#row-136), [23shades-0137-aahjacacc](ARTIFACTS.md#row-137), [23shades-0141-aadbcebbh](ARTIFACTS.md#row-141), [23shades-0165-aajaicjbh](ARTIFACTS.md#row-165), [23shades-0167-aagiehhgb](ARTIFACTS.md#row-167), [23shades-0170-aaigfaibj](ARTIFACTS.md#row-170), [23shades-0173-aabdgggib](ARTIFACTS.md#row-173), [23shades-0177-aahgdgida](ARTIFACTS.md#row-177), [23shades-0293-aahiihdej](ARTIFACTS.md#row-293), [23shades-0338-aagbbjgij](ARTIFACTS.md#row-338), [23shades-0341-aaecghdag](ARTIFACTS.md#row-341), [23shades-0388-aagaghfcd](ARTIFACTS.md#row-388), [23shades-0452-aajefhbah](ARTIFACTS.md#row-452), [23shades-0458-aaeggadce](ARTIFACTS.md#row-458), [23shades-0556-aadhfidia](ARTIFACTS.md#row-556), [23shades-0557-aajejbfha](ARTIFACTS.md#row-557), [23shades-0648-aadhfgije](ARTIFACTS.md#row-648), [23shades-0657-aajdbjejb](ARTIFACTS.md#row-657), [23shades-0658-aafeaihbg](ARTIFACTS.md#row-658), [23shades-0664-aahidajgj](ARTIFACTS.md#row-664), [23shades-0724-aaidgiiag](ARTIFACTS.md#row-724), [23shades-0727-aaheacagj](ARTIFACTS.md#row-727), [23shades-0769-aaefhaief](ARTIFACTS.md#row-769), [23shades-0798-aaidjgdji](ARTIFACTS.md#row-798), [23shades-0799-aahjdgiaa](ARTIFACTS.md#row-799), [23shades-0800-aahfigedf](ARTIFACTS.md#row-800), [23shades-0801-aaigijhgj](ARTIFACTS.md#row-801), [23shades-0814-aajficacj](ARTIFACTS.md#row-814), [23shades-0842-aajgchffb](ARTIFACTS.md#row-842), [23shades-0849-aaibjdjdc](ARTIFACTS.md#row-849), [23shades-0855-aaeachbce](ARTIFACTS.md#row-855)

## SATD-I · 算法与数据假设适用性

**定义：** 具体数学、数据、形状、初始化或启发式假设需要确认、限制或调整。

**纳入：** 模型选择、占位训练目标、阈值依据、尺度/索引/分布假设及信息损失权衡。

**排除与边界：** 不把疑问当已证错误；仅出现模型代码且无可定位待办用 U。

**例证：**

- [23shades-0046-aafchcgjg](ARTIFACTS.md#row-46)：上游未提供 confidence，临时填 1；不能当作真实置信度。
- [23shades-0050-aabcjdaea](ARTIFACTS.md#row-50)：零和游戏与两个值导致 error 乘二的注释；未明确说这种做法错误，需保留不确定性。
- [23shades-0054-aadaieabb](ARTIFACTS.md#row-54)：当前假定四字节 magic label，拟加 _accept hook。

**全部成员（逐条证据在链接中）：**

[23shades-0046-aafchcgjg](ARTIFACTS.md#row-46), [23shades-0050-aabcjdaea](ARTIFACTS.md#row-50), [23shades-0054-aadaieabb](ARTIFACTS.md#row-54), [23shades-0071-aafiaaaih](ARTIFACTS.md#row-71), [23shades-0083-aadggijai](ARTIFACTS.md#row-83), [23shades-0090-aaacjihab](ARTIFACTS.md#row-90), [23shades-0103-aaeeiehhe](ARTIFACTS.md#row-103), [23shades-0104-aaeeigbeg](ARTIFACTS.md#row-104), [23shades-0118-aajcgbchf](ARTIFACTS.md#row-118), [23shades-0119-aaecffiac](ARTIFACTS.md#row-119), [23shades-0137-aahjacacc](ARTIFACTS.md#row-137), [23shades-0199-aadhaadga](ARTIFACTS.md#row-199), [23shades-0200-aadhaidcc](ARTIFACTS.md#row-200), [23shades-0211-aajeacdfg](ARTIFACTS.md#row-211), [23shades-0232-aaeibhbhc](ARTIFACTS.md#row-232), [23shades-0247-aahiiegaf](ARTIFACTS.md#row-247), [23shades-0266-aaedhfhae](ARTIFACTS.md#row-266), [23shades-0270-aaebjbbad](ARTIFACTS.md#row-270), [23shades-0284-aaecghbgf](ARTIFACTS.md#row-284), [23shades-0296-aahiigecd](ARTIFACTS.md#row-296), [23shades-0318-aaejhfaed](ARTIFACTS.md#row-318), [23shades-0320-aaedbiehj](ARTIFACTS.md#row-320), [23shades-0363-aaebajbaf](ARTIFACTS.md#row-363), [23shades-0370-aafeghegj](ARTIFACTS.md#row-370), [23shades-0385-aaegicgcc](ARTIFACTS.md#row-385), [23shades-0388-aagaghfcd](ARTIFACTS.md#row-388), [23shades-0395-aaggjcebg](ARTIFACTS.md#row-395), [23shades-0405-aahjighda](ARTIFACTS.md#row-405), [23shades-0439-aaeeicdeh](ARTIFACTS.md#row-439), [23shades-0450-aaegfadac](ARTIFACTS.md#row-450), [23shades-0452-aajefhbah](ARTIFACTS.md#row-452), [23shades-0460-aagfecjfe](ARTIFACTS.md#row-460), [23shades-0475-aahjabdbh](ARTIFACTS.md#row-475), [23shades-0484-aabgdhcid](ARTIFACTS.md#row-484), [23shades-0496-aaeedfhcd](ARTIFACTS.md#row-496), [23shades-0497-aaeidiecf](ARTIFACTS.md#row-497), [23shades-0504-aagbbijce](ARTIFACTS.md#row-504), [23shades-0515-aaegihjhc](ARTIFACTS.md#row-515), [23shades-0516-aajegiabc](ARTIFACTS.md#row-516), [23shades-0517-aafafcgbj](ARTIFACTS.md#row-517), [23shades-0526-aagejejha](ARTIFACTS.md#row-526), [23shades-0531-aaffefcib](ARTIFACTS.md#row-531), [23shades-0532-aahddjbah](ARTIFACTS.md#row-532), [23shades-0534-aaeebgfej](ARTIFACTS.md#row-534), [23shades-0537-aaeidjjhd](ARTIFACTS.md#row-537), [23shades-0538-aafibegcj](ARTIFACTS.md#row-538), [23shades-0559-aafdibbge](ARTIFACTS.md#row-559), [23shades-0580-aaffdhejj](ARTIFACTS.md#row-580), [23shades-0583-aaiecfecg](ARTIFACTS.md#row-583), [23shades-0586-aagdaagij](ARTIFACTS.md#row-586), [23shades-0595-aafeaijhi](ARTIFACTS.md#row-595), [23shades-0596-aagbdjhgb](ARTIFACTS.md#row-596), [23shades-0597-aaefagbgc](ARTIFACTS.md#row-597), [23shades-0607-aagafeacd](ARTIFACTS.md#row-607), [23shades-0610-aaegfjdjb](ARTIFACTS.md#row-610), [23shades-0611-aajejahfe](ARTIFACTS.md#row-611), [23shades-0613-aadhcgief](ARTIFACTS.md#row-613), [23shades-0617-aafigfjii](ARTIFACTS.md#row-617), [23shades-0623-aahijjdcb](ARTIFACTS.md#row-623), [23shades-0625-aaefhdgid](ARTIFACTS.md#row-625), [23shades-0626-aadajbgbb](ARTIFACTS.md#row-626), [23shades-0627-aaidgcaed](ARTIFACTS.md#row-627), [23shades-0628-aaifedeec](ARTIFACTS.md#row-628), [23shades-0648-aadhfgije](ARTIFACTS.md#row-648), [23shades-0649-aaeidhcjb](ARTIFACTS.md#row-649), [23shades-0657-aajdbjejb](ARTIFACTS.md#row-657), [23shades-0658-aafeaihbg](ARTIFACTS.md#row-658), [23shades-0663-aaiedhhfd](ARTIFACTS.md#row-663), [23shades-0692-aajcfiaid](ARTIFACTS.md#row-692), [23shades-0693-aajacfjhb](ARTIFACTS.md#row-693), [23shades-0694-aaidhabjj](ARTIFACTS.md#row-694), [23shades-0695-aaeeihicj](ARTIFACTS.md#row-695), [23shades-0696-aaiihdfjc](ARTIFACTS.md#row-696), [23shades-0697-aadhhifdg](ARTIFACTS.md#row-697), [23shades-0701-aaefaahhg](ARTIFACTS.md#row-701), [23shades-0703-aagaahfid](ARTIFACTS.md#row-703), [23shades-0712-aajaighgc](ARTIFACTS.md#row-712), [23shades-0724-aaidgiiag](ARTIFACTS.md#row-724), [23shades-0727-aaheacagj](ARTIFACTS.md#row-727), [23shades-0729-aafafjdeg](ARTIFACTS.md#row-729), [23shades-0732-aahjacheg](ARTIFACTS.md#row-732), [23shades-0733-aajacfjii](ARTIFACTS.md#row-733), [23shades-0740-aagdjibjh](ARTIFACTS.md#row-740), [23shades-0741-aaigbchde](ARTIFACTS.md#row-741), [23shades-0747-aafighdeg](ARTIFACTS.md#row-747), [23shades-0749-aaihgdiif](ARTIFACTS.md#row-749), [23shades-0751-aahgfjfhj](ARTIFACTS.md#row-751), [23shades-0768-aaahbfbgd](ARTIFACTS.md#row-768), [23shades-0769-aaefhaief](ARTIFACTS.md#row-769), [23shades-0770-aadhddfhh](ARTIFACTS.md#row-770), [23shades-0774-aafhiicbj](ARTIFACTS.md#row-774), [23shades-0775-aahjejdja](ARTIFACTS.md#row-775), [23shades-0776-aaieahjdd](ARTIFACTS.md#row-776), [23shades-0803-aaichjjjg](ARTIFACTS.md#row-803), [23shades-0814-aajficacj](ARTIFACTS.md#row-814), [23shades-0815-aajfiebah](ARTIFACTS.md#row-815), [23shades-0819-aageebhag](ARTIFACTS.md#row-819), [23shades-0820-aajggjjdf](ARTIFACTS.md#row-820), [23shades-0823-aahfibidg](ARTIFACTS.md#row-823), [23shades-0826-aaeieahii](ARTIFACTS.md#row-826), [23shades-0827-aaeiedacj](ARTIFACTS.md#row-827), [23shades-0831-aajghfcje](ARTIFACTS.md#row-831), [23shades-0832-aajfibdif](ARTIFACTS.md#row-832), [23shades-0837-aaicicaia](ARTIFACTS.md#row-837), [23shades-0839-aaicgfbda](ARTIFACTS.md#row-839), [23shades-0840-aaeidjejd](ARTIFACTS.md#row-840), [23shades-0844-aaibicege](ARTIFACTS.md#row-844), [23shades-0847-aagbgfjfe](ARTIFACTS.md#row-847), [23shades-0848-aahiefidd](ARTIFACTS.md#row-848), [23shades-0850-aahighbdb](ARTIFACTS.md#row-850), [23shades-0851-aajgdbgid](ARTIFACTS.md#row-851), [23shades-0855-aaeachbce](ARTIFACTS.md#row-855)

## SATD-J · 配置、参数与默认行为

**定义：** 参数可配置性、参数语义、默认值或配置传播存在待改事项。

**纳入：** 硬编码转参数、开关、默认策略、参数缺失/未生效及有对象的配置决策。

**排除与边界：** 仅重命名一般局部变量用 A；测试数据中的参数不必然是产品配置。

**例证：**

- [23shades-0011-aageijaai](ARTIFACTS.md#row-11)：询问 gains/biases 是否应可训练，保留设计疑问。
- [23shades-0012-aafaehach](ARTIFACTS.md#row-12)：name 缺失时拟采用 functionality.__name__。
- [23shades-0022-aahdfibcf](ARTIFACTS.md#row-22)：TODO 指出 nrows 仅用于测试；应关注参数用途，但未说明删除或替代方案，保留待办意图与处置不确定性。

**全部成员（逐条证据在链接中）：**

[23shades-0011-aageijaai](ARTIFACTS.md#row-11), [23shades-0012-aafaehach](ARTIFACTS.md#row-12), [23shades-0022-aahdfibcf](ARTIFACTS.md#row-22), [23shades-0060-aaebhejej](ARTIFACTS.md#row-60), [23shades-0064-aaiicfgag](ARTIFACTS.md#row-64), [23shades-0089-aajdcehac](ARTIFACTS.md#row-89), [23shades-0090-aaacjihab](ARTIFACTS.md#row-90), [23shades-0174-aafbhcbbi](ARTIFACTS.md#row-174), [23shades-0212-aahhiefcg](ARTIFACTS.md#row-212), [23shades-0213-aahhiidji](ARTIFACTS.md#row-213), [23shades-0214-aafhjjgee](ARTIFACTS.md#row-214), [23shades-0224-aadajefje](ARTIFACTS.md#row-224), [23shades-0232-aaeibhbhc](ARTIFACTS.md#row-232), [23shades-0238-aagaggbcc](ARTIFACTS.md#row-238), [23shades-0246-aafehehgb](ARTIFACTS.md#row-246), [23shades-0247-aahiiegaf](ARTIFACTS.md#row-247), [23shades-0250-aafchcgdb](ARTIFACTS.md#row-250), [23shades-0252-aafeifgfi](ARTIFACTS.md#row-252), [23shades-0269-aafehiefj](ARTIFACTS.md#row-269), [23shades-0270-aaebjbbad](ARTIFACTS.md#row-270), [23shades-0280-aafacjcgb](ARTIFACTS.md#row-280), [23shades-0284-aaecghbgf](ARTIFACTS.md#row-284), [23shades-0286-aagcijbch](ARTIFACTS.md#row-286), [23shades-0302-aahiiggad](ARTIFACTS.md#row-302), [23shades-0309-aadfiacgf](ARTIFACTS.md#row-309), [23shades-0318-aaejhfaed](ARTIFACTS.md#row-318), [23shades-0322-aaacgfhgb](ARTIFACTS.md#row-322), [23shades-0327-aadagfcdg](ARTIFACTS.md#row-327), [23shades-0334-aaebajfae](ARTIFACTS.md#row-334), [23shades-0363-aaebajbaf](ARTIFACTS.md#row-363), [23shades-0375-aafeihffh](ARTIFACTS.md#row-375), [23shades-0383-aajdbcadb](ARTIFACTS.md#row-383), [23shades-0384-aahcgeaed](ARTIFACTS.md#row-384), [23shades-0403-aaggciajj](ARTIFACTS.md#row-403), [23shades-0404-aahfghdbg](ARTIFACTS.md#row-404), [23shades-0405-aahjighda](ARTIFACTS.md#row-405), [23shades-0418-aadhgfgeb](ARTIFACTS.md#row-418), [23shades-0449-aajdcigce](ARTIFACTS.md#row-449), [23shades-0450-aaegfadac](ARTIFACTS.md#row-450), [23shades-0452-aajefhbah](ARTIFACTS.md#row-452), [23shades-0475-aahjabdbh](ARTIFACTS.md#row-475), [23shades-0501-aaedhahfd](ARTIFACTS.md#row-501), [23shades-0516-aajegiabc](ARTIFACTS.md#row-516), [23shades-0519-aajfiibhb](ARTIFACTS.md#row-519), [23shades-0526-aagejejha](ARTIFACTS.md#row-526), [23shades-0531-aaffefcib](ARTIFACTS.md#row-531), [23shades-0534-aaeebgfej](ARTIFACTS.md#row-534), [23shades-0556-aadhfidia](ARTIFACTS.md#row-556), [23shades-0557-aajejbfha](ARTIFACTS.md#row-557), [23shades-0569-aahhhfjei](ARTIFACTS.md#row-569), [23shades-0590-aafiggbeh](ARTIFACTS.md#row-590), [23shades-0595-aafeaijhi](ARTIFACTS.md#row-595), [23shades-0597-aaefagbgc](ARTIFACTS.md#row-597), [23shades-0643-aagbdffff](ARTIFACTS.md#row-643), [23shades-0644-aaibjebjh](ARTIFACTS.md#row-644), [23shades-0648-aadhfgije](ARTIFACTS.md#row-648), [23shades-0657-aajdbjejb](ARTIFACTS.md#row-657), [23shades-0658-aafeaihbg](ARTIFACTS.md#row-658), [23shades-0671-aaedghfjd](ARTIFACTS.md#row-671), [23shades-0677-aaefecjfa](ARTIFACTS.md#row-677), [23shades-0693-aajacfjhb](ARTIFACTS.md#row-693), [23shades-0694-aaidhabjj](ARTIFACTS.md#row-694), [23shades-0695-aaeeihicj](ARTIFACTS.md#row-695), [23shades-0699-aaffeacij](ARTIFACTS.md#row-699), [23shades-0708-aahjejchc](ARTIFACTS.md#row-708), [23shades-0724-aaidgiiag](ARTIFACTS.md#row-724), [23shades-0725-aahicjieh](ARTIFACTS.md#row-725), [23shades-0747-aafighdeg](ARTIFACTS.md#row-747), [23shades-0749-aaihgdiif](ARTIFACTS.md#row-749), [23shades-0753-aaeejgbaa](ARTIFACTS.md#row-753), [23shades-0768-aaahbfbgd](ARTIFACTS.md#row-768), [23shades-0791-aahgcaaac](ARTIFACTS.md#row-791), [23shades-0805-aajfiefig](ARTIFACTS.md#row-805), [23shades-0814-aajficacj](ARTIFACTS.md#row-814), [23shades-0844-aaibicege](ARTIFACTS.md#row-844), [23shades-0850-aahighbdb](ARTIFACTS.md#row-850)

## SATD-K · 测试与验证工作

**定义：** 需要新增、启用、更新、扩展或修复测试，以及显式核验行为或性能的工作。

**纳入：** 断言不足、设备无关测试、版本复验及明确测试/比较活动；注明是否只是待核验。

**排除与边界：** 数据集 validation/test 不等于测试代码；判别某类型的 test 仅用 C。

**例证：**

- [23shades-0038-aaeiaheab](ARTIFACTS.md#row-38)：MdC 到 Unicode 转换需要增加测试与清理代码。
- [23shades-0040-aaeiahgad](ARTIFACTS.md#row-40)：Unicode 转换模块拟移除 regex 依赖并增加测试。
- [23shades-0072-aaidadhdg](ARTIFACTS.md#row-72)：希望使用 _skip_test，但 if we could 表示约束未解决。

**全部成员（逐条证据在链接中）：**

[23shades-0038-aaeiaheab](ARTIFACTS.md#row-38), [23shades-0040-aaeiahgad](ARTIFACTS.md#row-40), [23shades-0072-aaidadhdg](ARTIFACTS.md#row-72), [23shades-0080-aaidbchej](ARTIFACTS.md#row-80), [23shades-0164-aajgcjgad](ARTIFACTS.md#row-164), [23shades-0200-aadhaidcc](ARTIFACTS.md#row-200), [23shades-0204-aadhadibe](ARTIFACTS.md#row-204), [23shades-0207-aaggfbief](ARTIFACTS.md#row-207), [23shades-0208-aaeeciehh](ARTIFACTS.md#row-208), [23shades-0242-aafegjcei](ARTIFACTS.md#row-242), [23shades-0243-aafeihbhc](ARTIFACTS.md#row-243), [23shades-0258-aagchjdcj](ARTIFACTS.md#row-258), [23shades-0260-aadfcehfi](ARTIFACTS.md#row-260), [23shades-0261-aaaiefadd](ARTIFACTS.md#row-261), [23shades-0266-aaedhfhae](ARTIFACTS.md#row-266), [23shades-0273-aaebjbbei](ARTIFACTS.md#row-273), [23shades-0300-aaejhiaeb](ARTIFACTS.md#row-300), [23shades-0316-aafbifbhe](ARTIFACTS.md#row-316), [23shades-0317-aaieffgij](ARTIFACTS.md#row-317), [23shades-0348-aajajehgf](ARTIFACTS.md#row-348), [23shades-0359-aajebahia](ARTIFACTS.md#row-359), [23shades-0360-aajecehjc](ARTIFACTS.md#row-360), [23shades-0361-aageaibai](ARTIFACTS.md#row-361), [23shades-0376-aaebjafhg](ARTIFACTS.md#row-376), [23shades-0386-aaiehihbh](ARTIFACTS.md#row-386), [23shades-0395-aaggjcebg](ARTIFACTS.md#row-395), [23shades-0440-aajaijffg](ARTIFACTS.md#row-440), [23shades-0453-aaefagffe](ARTIFACTS.md#row-453), [23shades-0459-aafafahih](ARTIFACTS.md#row-459), [23shades-0477-aafibaccg](ARTIFACTS.md#row-477), [23shades-0479-aahhdgbbd](ARTIFACTS.md#row-479), [23shades-0484-aabgdhcid](ARTIFACTS.md#row-484), [23shades-0490-aaaefgdbc](ARTIFACTS.md#row-490), [23shades-0502-aaidjgfeg](ARTIFACTS.md#row-502), [23shades-0520-aajddbihf](ARTIFACTS.md#row-520), [23shades-0525-aajbigiad](ARTIFACTS.md#row-525), [23shades-0527-aahddidfd](ARTIFACTS.md#row-527), [23shades-0528-aagejdfdj](ARTIFACTS.md#row-528), [23shades-0543-aahggbife](ARTIFACTS.md#row-543), [23shades-0571-aagfabdib](ARTIFACTS.md#row-571), [23shades-0577-aafjgijbb](ARTIFACTS.md#row-577), [23shades-0601-aahfgdcad](ARTIFACTS.md#row-601), [23shades-0606-aahicghci](ARTIFACTS.md#row-606), [23shades-0611-aajejahfe](ARTIFACTS.md#row-611), [23shades-0624-aaeebjfdb](ARTIFACTS.md#row-624), [23shades-0662-aajfceihg](ARTIFACTS.md#row-662), [23shades-0691-aagejcfed](ARTIFACTS.md#row-691), [23shades-0717-aahhgdcgi](ARTIFACTS.md#row-717), [23shades-0718-aadbaabcf](ARTIFACTS.md#row-718), [23shades-0719-aajffiged](ARTIFACTS.md#row-719), [23shades-0720-aagejejie](ARTIFACTS.md#row-720), [23shades-0721-aahdjfjcf](ARTIFACTS.md#row-721), [23shades-0740-aagdjibjh](ARTIFACTS.md#row-740), [23shades-0745-aaidfiegj](ARTIFACTS.md#row-745), [23shades-0751-aahgfjfhj](ARTIFACTS.md#row-751), [23shades-0763-aajdbdjhc](ARTIFACTS.md#row-763), [23shades-0764-aadiicibd](ARTIFACTS.md#row-764), [23shades-0781-aaidjdcbf](ARTIFACTS.md#row-781), [23shades-0784-aahjaaeee](ARTIFACTS.md#row-784), [23shades-0785-aaeiaeifb](ARTIFACTS.md#row-785), [23shades-0787-aafhfhjbf](ARTIFACTS.md#row-787)

## SATD-L · 说明、文档与理解缺口

**定义：** 文档、教程、引用、说明或对实现含义的理解不足。

**纳入：** 缺 docstring、陈旧说明、为何存在的解释、未理解的参数/变量。

**排除与边界：** 日志及运行诊断主要用 O；不能把所有设计疑问都当文档缺失。

**例证：**

- [23shades-0018-aajcabgbe](ARTIFACTS.md#row-18)：认为现有内容可转成生成 phantoms 的教程。
- [23shades-0032-aaejahaed](ARTIFACTS.md#row-32)：doc 占位待写。
- [23shades-0033-aadhcadac](ARTIFACTS.md#row-33)：hyperband synopsis 与长描述为 TODO，占位文档未完成。

**全部成员（逐条证据在链接中）：**

[23shades-0018-aajcabgbe](ARTIFACTS.md#row-18), [23shades-0032-aaejahaed](ARTIFACTS.md#row-32), [23shades-0033-aadhcadac](ARTIFACTS.md#row-33), [23shades-0041-aahdeachi](ARTIFACTS.md#row-41), [23shades-0042-aabgebcce](ARTIFACTS.md#row-42), [23shades-0045-aajdcegja](ARTIFACTS.md#row-45), [23shades-0065-aagfjefaf](ARTIFACTS.md#row-65), [23shades-0066-aahhdbjej](ARTIFACTS.md#row-66), [23shades-0078-aaecffjjg](ARTIFACTS.md#row-78), [23shades-0160-aajbibibf](ARTIFACTS.md#row-160), [23shades-0175-aafecgahb](ARTIFACTS.md#row-175), [23shades-0215-aafjbabdi](ARTIFACTS.md#row-215), [23shades-0216-aaebcicac](ARTIFACTS.md#row-216), [23shades-0228-aaebjjhbc](ARTIFACTS.md#row-228), [23shades-0231-aafchbajj](ARTIFACTS.md#row-231), [23shades-0288-aaedbehai](ARTIFACTS.md#row-288), [23shades-0378-aahiieejb](ARTIFACTS.md#row-378), [23shades-0421-aajfaggeb](ARTIFACTS.md#row-421), [23shades-0486-aahfjcfdg](ARTIFACTS.md#row-486), [23shades-0524-aaifeicfh](ARTIFACTS.md#row-524), [23shades-0538-aafibegcj](ARTIFACTS.md#row-538), [23shades-0585-aadggbdcb](ARTIFACTS.md#row-585), [23shades-0604-aajcjaefh](ARTIFACTS.md#row-604), [23shades-0777-aagaecbjg](ARTIFACTS.md#row-777), [23shades-0802-aafdiabdg](ARTIFACTS.md#row-802), [23shades-0806-aahjgiagj](ARTIFACTS.md#row-806)

## SATD-M · 冗余、弃用与条件性清理

**定义：** 存在待删除的过渡、重复、未用或弃用逻辑，或其必要性尚待判断。

**纳入：** 版本到期清理、替代能力就绪再删、重复参数、疑似无用代码；保留条件。

**排除与边界：** 不能把 probably unnecessary 记为已确认无用或已删除。

**例证：**

- [23shades-0038-aaeiaheab](ARTIFACTS.md#row-38)：MdC 到 Unicode 转换需要增加测试与清理代码。
- [23shades-0058-aaahbfbhe](ARTIFACTS.md#row-58)：作者询问是否 deprecate，认为可能不再需要；尚未裁决。
- [23shades-0080-aaidbchej](ARTIFACTS.md#row-80)：当 0.26 默认 square_distances=True 后删除特定测试；不是普遍测试不足。

**全部成员（逐条证据在链接中）：**

[23shades-0038-aaeiaheab](ARTIFACTS.md#row-38), [23shades-0058-aaahbfbhe](ARTIFACTS.md#row-58), [23shades-0080-aaidbchej](ARTIFACTS.md#row-80), [23shades-0110-aaidajbdi](ARTIFACTS.md#row-110), [23shades-0135-aahfgjaff](ARTIFACTS.md#row-135), [23shades-0150-aahfhedig](ARTIFACTS.md#row-150), [23shades-0153-aajacaegh](ARTIFACTS.md#row-153), [23shades-0155-aafibegdj](ARTIFACTS.md#row-155), [23shades-0161-aagcbdejg](ARTIFACTS.md#row-161), [23shades-0199-aadhaadga](ARTIFACTS.md#row-199), [23shades-0210-aaefhhbid](ARTIFACTS.md#row-210), [23shades-0220-aadcagfcc](ARTIFACTS.md#row-220), [23shades-0246-aafehehgb](ARTIFACTS.md#row-246), [23shades-0331-aafhghged](ARTIFACTS.md#row-331), [23shades-0332-aagejhdij](ARTIFACTS.md#row-332), [23shades-0333-aadfaifgh](ARTIFACTS.md#row-333), [23shades-0334-aaebajfae](ARTIFACTS.md#row-334), [23shades-0335-aagaceabd](ARTIFACTS.md#row-335), [23shades-0338-aagbbjgij](ARTIFACTS.md#row-338), [23shades-0341-aaecghdag](ARTIFACTS.md#row-341), [23shades-0377-aafchfjcg](ARTIFACTS.md#row-377), [23shades-0392-aaghbecie](ARTIFACTS.md#row-392), [23shades-0416-aaiibahhd](ARTIFACTS.md#row-416), [23shades-0422-aajfahfei](ARTIFACTS.md#row-422), [23shades-0458-aaeggadce](ARTIFACTS.md#row-458), [23shades-0509-aaacggdch](ARTIFACTS.md#row-509), [23shades-0513-aajfeejjg](ARTIFACTS.md#row-513), [23shades-0514-aaaggiije](ARTIFACTS.md#row-514), [23shades-0527-aahddidfd](ARTIFACTS.md#row-527), [23shades-0547-aahjacjjf](ARTIFACTS.md#row-547), [23shades-0558-aaibihacc](ARTIFACTS.md#row-558), [23shades-0581-aaeieedge](ARTIFACTS.md#row-581), [23shades-0593-aadbehbcf](ARTIFACTS.md#row-593), [23shades-0637-aaffdijjg](ARTIFACTS.md#row-637), [23shades-0655-aaeffajfh](ARTIFACTS.md#row-655), [23shades-0656-aaefbgdbg](ARTIFACTS.md#row-656), [23shades-0659-aaidbebab](ARTIFACTS.md#row-659), [23shades-0660-aaidbgddf](ARTIFACTS.md#row-660), [23shades-0661-aaidbgfgc](ARTIFACTS.md#row-661), [23shades-0664-aahidajgj](ARTIFACTS.md#row-664), [23shades-0665-aaidbbafi](ARTIFACTS.md#row-665), [23shades-0666-aahicgcid](ARTIFACTS.md#row-666), [23shades-0667-aahjgdcge](ARTIFACTS.md#row-667), [23shades-0668-aaeiebdgb](ARTIFACTS.md#row-668), [23shades-0669-aahibibgj](ARTIFACTS.md#row-669), [23shades-0673-aaiecbahd](ARTIFACTS.md#row-673), [23shades-0676-aaicjgced](ARTIFACTS.md#row-676), [23shades-0677-aaefecjfa](ARTIFACTS.md#row-677), [23shades-0680-aadhbjgee](ARTIFACTS.md#row-680), [23shades-0681-aaibgbejh](ARTIFACTS.md#row-681), [23shades-0683-aaeihdfda](ARTIFACTS.md#row-683), [23shades-0723-aaeacgjbc](ARTIFACTS.md#row-723), [23shades-0726-aadejjjdj](ARTIFACTS.md#row-726), [23shades-0730-aaiheabif](ARTIFACTS.md#row-730), [23shades-0731-aafiggaje](ARTIFACTS.md#row-731), [23shades-0748-aaidaidid](ARTIFACTS.md#row-748), [23shades-0794-aahdadjbj](ARTIFACTS.md#row-794), [23shades-0795-aagibcfja](ARTIFACTS.md#row-795), [23shades-0822-aahjfbdfa](ARTIFACTS.md#row-822), [23shades-0829-aajgdidia](ARTIFACTS.md#row-829), [23shades-0835-aajghfhbf](ARTIFACTS.md#row-835)

## SATD-N · 持久化、序列化与数据表示契约

**定义：** 涉及保存/恢复、格式、输出表示、索引或跨阶段传递的数据结构。

**纳入：** 序列化失败、格式替换、检查点、模型保存、稳定索引、输出元信息。

**排除与边界：** 一般内部抽象变化用 A；未说明格式的泛化待办不必纳入。

**例证：**

- [23shades-0035-aahfiaifg](ARTIFACTS.md#row-35)：CSV corpus 实际仍输出 SVMLight，作者邀请修改。
- [23shades-0045-aajdcegja](ARTIFACTS.md#row-45)：diff 格式需要定义并文档化；版本转换已由 nbformat 处理，不能误码为版本支持缺失。
- [23shades-0054-aadaieabb](ARTIFACTS.md#row-54)：当前假定四字节 magic label，拟加 _accept hook。

**全部成员（逐条证据在链接中）：**

[23shades-0035-aahfiaifg](ARTIFACTS.md#row-35), [23shades-0045-aajdcegja](ARTIFACTS.md#row-45), [23shades-0054-aadaieabb](ARTIFACTS.md#row-54), [23shades-0089-aajdcehac](ARTIFACTS.md#row-89), [23shades-0111-aajdcgacj](ARTIFACTS.md#row-111), [23shades-0115-aaeejbdgh](ARTIFACTS.md#row-115), [23shades-0154-aajdcgijh](ARTIFACTS.md#row-154), [23shades-0230-aahjecdhj](ARTIFACTS.md#row-230), [23shades-0254-aagigfafa](ARTIFACTS.md#row-254), [23shades-0264-aahjaaihb](ARTIFACTS.md#row-264), [23shades-0271-aahddgbeh](ARTIFACTS.md#row-271), [23shades-0274-aaebjhccj](ARTIFACTS.md#row-274), [23shades-0305-aahddgbgb](ARTIFACTS.md#row-305), [23shades-0343-aaadbhidf](ARTIFACTS.md#row-343), [23shades-0344-aafejacii](ARTIFACTS.md#row-344), [23shades-0345-aafagebef](ARTIFACTS.md#row-345), [23shades-0346-aahiiefbj](ARTIFACTS.md#row-346), [23shades-0374-aahiiffci](ARTIFACTS.md#row-374), [23shades-0502-aaidjgfeg](ARTIFACTS.md#row-502), [23shades-0546-aaiejgdgf](ARTIFACTS.md#row-546), [23shades-0594-aafbjgjcd](ARTIFACTS.md#row-594), [23shades-0633-aagcdfdia](ARTIFACTS.md#row-633), [23shades-0638-aaghjajha](ARTIFACTS.md#row-638), [23shades-0680-aadhbjgee](ARTIFACTS.md#row-680), [23shades-0685-aaheajiai](ARTIFACTS.md#row-685), [23shades-0686-aagbiaaje](ARTIFACTS.md#row-686), [23shades-0698-aagdjigjj](ARTIFACTS.md#row-698), [23shades-0701-aaefaahhg](ARTIFACTS.md#row-701), [23shades-0709-aaedaedaa](ARTIFACTS.md#row-709), [23shades-0711-aafbjiedd](ARTIFACTS.md#row-711), [23shades-0712-aajaighgc](ARTIFACTS.md#row-712), [23shades-0727-aaheacagj](ARTIFACTS.md#row-727), [23shades-0780-aaididbfa](ARTIFACTS.md#row-780), [23shades-0790-aahicaeda](ARTIFACTS.md#row-790), [23shades-0793-aahefcehd](ARTIFACTS.md#row-793), [23shades-0796-aagdafeic](ARTIFACTS.md#row-796), [23shades-0804-aajgccaef](ARTIFACTS.md#row-804), [23shades-0810-aajficjje](ARTIFACTS.md#row-810), [23shades-0830-aajfigjji](ARTIFACTS.md#row-830), [23shades-0838-aaeidjach](ARTIFACTS.md#row-838), [23shades-0855-aaeachbce](ARTIFACTS.md#row-855)

## SATD-O · 显示、日志与运行可观察性

**定义：** 展示、图表、告警、日志或运行时间反馈需要改善。

**纳入：** 显示错误、绘图功能、日志等级/范围、警告与测量信息。

**排除与边界：** 日志里有测试输出不代表测试充分；缺断言应并 K。

**例证：**

- [23shades-0059-aacjfgieb](ARTIFACTS.md#row-59)：双换行似乎影响显示；原因不明。
- [23shades-0088-aahedijdj](ARTIFACTS.md#row-88)：don't show 的对象只有转义斜杠，展示意图可见但细节不足。
- [23shades-0202-aafdacejd](ARTIFACTS.md#row-202)：要求 smoother visualization bounds。

**全部成员（逐条证据在链接中）：**

[23shades-0059-aacjfgieb](ARTIFACTS.md#row-59), [23shades-0088-aahedijdj](ARTIFACTS.md#row-88), [23shades-0202-aafdacejd](ARTIFACTS.md#row-202), [23shades-0236-aaejhhjgg](ARTIFACTS.md#row-236), [23shades-0245-aafehehfi](ARTIFACTS.md#row-245), [23shades-0272-aagjifffj](ARTIFACTS.md#row-272), [23shades-0366-aaebagcaf](ARTIFACTS.md#row-366), [23shades-0390-aagdhccjd](ARTIFACTS.md#row-390), [23shades-0405-aahjighda](ARTIFACTS.md#row-405), [23shades-0419-aadheehad](ARTIFACTS.md#row-419), [23shades-0437-aaeacgafj](ARTIFACTS.md#row-437), [23shades-0441-aaefegech](ARTIFACTS.md#row-441), [23shades-0461-aaidhjgaj](ARTIFACTS.md#row-461), [23shades-0585-aadggbdcb](ARTIFACTS.md#row-585), [23shades-0588-aaeiaghhj](ARTIFACTS.md#row-588), [23shades-0589-aaeiafbcg](ARTIFACTS.md#row-589), [23shades-0604-aajcjaefh](ARTIFACTS.md#row-604), [23shades-0620-aafjjehej](ARTIFACTS.md#row-620), [23shades-0662-aajfceihg](ARTIFACTS.md#row-662), [23shades-0772-aahcfeahc](ARTIFACTS.md#row-772), [23shades-0782-aaahbahcg](ARTIFACTS.md#row-782), [23shades-0791-aahgcaaac](ARTIFACTS.md#row-791), [23shades-0797-aafafjdfg](ARTIFACTS.md#row-797), [23shades-0802-aafdiabdg](ARTIFACTS.md#row-802), [23shades-0806-aahjgiagj](ARTIFACTS.md#row-806)

## SATD-Q · 尚未裁决的设计或诊断

**定义：** 作者仍在询问必要性、原因、替代方案、效果或正确性，尚无明确裁决。

**纳入：** 保留问句、maybe、待核实、对象不完整的一般改进，不升级为确认缺陷。

**排除与边界：** 明确待实现且无选择疑问不必加；此为认识状态代码，不替代具体主题。

**例证：**

- [23shades-0010-aaaedagad](ARTIFACTS.md#row-10)：name/index/uuid 可能需要重写；是候选修改而非已确认错误。
- [23shades-0011-aageijaai](ARTIFACTS.md#row-11)：询问 gains/biases 是否应可训练，保留设计疑问。
- [23shades-0022-aahdfibcf](ARTIFACTS.md#row-22)：TODO 指出 nrows 仅用于测试；应关注参数用途，但未说明删除或替代方案，保留待办意图与处置不确定性。

**全部成员（逐条证据在链接中）：**

[23shades-0010-aaaedagad](ARTIFACTS.md#row-10), [23shades-0011-aageijaai](ARTIFACTS.md#row-11), [23shades-0022-aahdfibcf](ARTIFACTS.md#row-22), [23shades-0027-aajfegaca](ARTIFACTS.md#row-27), [23shades-0031-aagbibedf](ARTIFACTS.md#row-31), [23shades-0050-aabcjdaea](ARTIFACTS.md#row-50), [23shades-0051-aagacefbc](ARTIFACTS.md#row-51), [23shades-0058-aaahbfbhe](ARTIFACTS.md#row-58), [23shades-0064-aaiicfgag](ARTIFACTS.md#row-64), [23shades-0066-aahhdbjej](ARTIFACTS.md#row-66), [23shades-0075-aagdagdia](ARTIFACTS.md#row-75), [23shades-0078-aaecffjjg](ARTIFACTS.md#row-78), [23shades-0085-aaebbccje](ARTIFACTS.md#row-85), [23shades-0087-aaiehhaec](ARTIFACTS.md#row-87), [23shades-0089-aajdcehac](ARTIFACTS.md#row-89), [23shades-0091-aagbejage](ARTIFACTS.md#row-91), [23shades-0096-aaeeidbja](ARTIFACTS.md#row-96), [23shades-0098-aaffadbgf](ARTIFACTS.md#row-98), [23shades-0103-aaeeiehhe](ARTIFACTS.md#row-103), [23shades-0104-aaeeigbeg](ARTIFACTS.md#row-104), [23shades-0113-aajdcgebb](ARTIFACTS.md#row-113), [23shades-0114-aafeaaejc](ARTIFACTS.md#row-114), [23shades-0115-aaeejbdgh](ARTIFACTS.md#row-115), [23shades-0116-aafcbidge](ARTIFACTS.md#row-116), [23shades-0119-aaecffiac](ARTIFACTS.md#row-119), [23shades-0133-aaggcfjif](ARTIFACTS.md#row-133), [23shades-0134-aaggcgaie](ARTIFACTS.md#row-134), [23shades-0137-aahjacacc](ARTIFACTS.md#row-137), [23shades-0138-aagdbgcgg](ARTIFACTS.md#row-138), [23shades-0148-aaeigcigi](ARTIFACTS.md#row-148), [23shades-0150-aahfhedig](ARTIFACTS.md#row-150), [23shades-0155-aafibegdj](ARTIFACTS.md#row-155), [23shades-0158-aahgacfhf](ARTIFACTS.md#row-158), [23shades-0160-aajbibibf](ARTIFACTS.md#row-160), [23shades-0161-aagcbdejg](ARTIFACTS.md#row-161), [23shades-0175-aafecgahb](ARTIFACTS.md#row-175), [23shades-0198-aajeiegcd](ARTIFACTS.md#row-198), [23shades-0199-aadhaadga](ARTIFACTS.md#row-199), [23shades-0200-aadhaidcc](ARTIFACTS.md#row-200), [23shades-0201-aaffefhhb](ARTIFACTS.md#row-201), [23shades-0211-aajeacdfg](ARTIFACTS.md#row-211), [23shades-0214-aafhjjgee](ARTIFACTS.md#row-214), [23shades-0222-aahdficjf](ARTIFACTS.md#row-222), [23shades-0232-aaeibhbhc](ARTIFACTS.md#row-232), [23shades-0233-aagaagfeh](ARTIFACTS.md#row-233), [23shades-0237-aafcgegjb](ARTIFACTS.md#row-237), [23shades-0240-aagaagfeg](ARTIFACTS.md#row-240), [23shades-0247-aahiiegaf](ARTIFACTS.md#row-247), [23shades-0258-aagchjdcj](ARTIFACTS.md#row-258), [23shades-0260-aadfcehfi](ARTIFACTS.md#row-260), [23shades-0263-aadbfihhc](ARTIFACTS.md#row-263), [23shades-0266-aaedhfhae](ARTIFACTS.md#row-266), [23shades-0268-aadfdgaei](ARTIFACTS.md#row-268), [23shades-0270-aaebjbbad](ARTIFACTS.md#row-270), [23shades-0271-aahddgbeh](ARTIFACTS.md#row-271), [23shades-0275-aahiigije](ARTIFACTS.md#row-275), [23shades-0284-aaecghbgf](ARTIFACTS.md#row-284), [23shades-0286-aagcijbch](ARTIFACTS.md#row-286), [23shades-0287-aagdffgjh](ARTIFACTS.md#row-287), [23shades-0288-aaedbehai](ARTIFACTS.md#row-288), [23shades-0301-aagacdjjd](ARTIFACTS.md#row-301), [23shades-0305-aahddgbgb](ARTIFACTS.md#row-305), [23shades-0307-aajcfhiga](ARTIFACTS.md#row-307), [23shades-0310-aafadaiij](ARTIFACTS.md#row-310), [23shades-0314-aadfcfhgh](ARTIFACTS.md#row-314), [23shades-0315-aaecghbei](ARTIFACTS.md#row-315), [23shades-0318-aaejhfaed](ARTIFACTS.md#row-318), [23shades-0320-aaedbiehj](ARTIFACTS.md#row-320), [23shades-0324-aajcjfcfc](ARTIFACTS.md#row-324), [23shades-0326-aaeadhaac](ARTIFACTS.md#row-326), [23shades-0328-aadgecacc](ARTIFACTS.md#row-328), [23shades-0336-aafehbbbf](ARTIFACTS.md#row-336), [23shades-0347-aaahgiacg](ARTIFACTS.md#row-347), [23shades-0351-aajbebjea](ARTIFACTS.md#row-351), [23shades-0352-aaifjjgei](ARTIFACTS.md#row-352), [23shades-0367-aadfjffba](ARTIFACTS.md#row-367), [23shades-0373-aagcjhcea](ARTIFACTS.md#row-373), [23shades-0380-aahddgbgf](ARTIFACTS.md#row-380), [23shades-0381-aagcicfdi](ARTIFACTS.md#row-381), [23shades-0389-aagachejb](ARTIFACTS.md#row-389), [23shades-0392-aaghbecie](ARTIFACTS.md#row-392), [23shades-0395-aaggjcebg](ARTIFACTS.md#row-395), [23shades-0401-aaegacgid](ARTIFACTS.md#row-401), [23shades-0405-aahjighda](ARTIFACTS.md#row-405), [23shades-0412-aadbbhbgg](ARTIFACTS.md#row-412), [23shades-0414-aaiiaefbb](ARTIFACTS.md#row-414), [23shades-0419-aadheehad](ARTIFACTS.md#row-419), [23shades-0420-aadhgacdi](ARTIFACTS.md#row-420), [23shades-0434-aaifgcjac](ARTIFACTS.md#row-434), [23shades-0436-aafadcigh](ARTIFACTS.md#row-436), [23shades-0438-aaaifiggc](ARTIFACTS.md#row-438), [23shades-0439-aaeeicdeh](ARTIFACTS.md#row-439), [23shades-0451-aaifgfeag](ARTIFACTS.md#row-451), [23shades-0462-aadehggdg](ARTIFACTS.md#row-462), [23shades-0467-aaididaaj](ARTIFACTS.md#row-467), [23shades-0470-aaedhgdgd](ARTIFACTS.md#row-470), [23shades-0471-aageachcc](ARTIFACTS.md#row-471), [23shades-0473-aagacefai](ARTIFACTS.md#row-473), [23shades-0474-aaeebgdbh](ARTIFACTS.md#row-474), [23shades-0475-aahjabdbh](ARTIFACTS.md#row-475), [23shades-0477-aafibaccg](ARTIFACTS.md#row-477), [23shades-0479-aahhdgbbd](ARTIFACTS.md#row-479), [23shades-0483-aagbdjfdj](ARTIFACTS.md#row-483), [23shades-0484-aabgdhcid](ARTIFACTS.md#row-484), [23shades-0485-aafhihfed](ARTIFACTS.md#row-485), [23shades-0486-aahfjcfdg](ARTIFACTS.md#row-486), [23shades-0496-aaeedfhcd](ARTIFACTS.md#row-496), [23shades-0497-aaeidiecf](ARTIFACTS.md#row-497), [23shades-0500-aaeiedggi](ARTIFACTS.md#row-500), [23shades-0501-aaedhahfd](ARTIFACTS.md#row-501), [23shades-0502-aaidjgfeg](ARTIFACTS.md#row-502), [23shades-0504-aagbbijce](ARTIFACTS.md#row-504), [23shades-0505-aadgfccbh](ARTIFACTS.md#row-505), [23shades-0506-aaeieejja](ARTIFACTS.md#row-506), [23shades-0507-aafbciiij](ARTIFACTS.md#row-507), [23shades-0508-aafhhaijc](ARTIFACTS.md#row-508), [23shades-0509-aaacggdch](ARTIFACTS.md#row-509), [23shades-0514-aaaggiije](ARTIFACTS.md#row-514), [23shades-0515-aaegihjhc](ARTIFACTS.md#row-515), [23shades-0516-aajegiabc](ARTIFACTS.md#row-516), [23shades-0517-aafafcgbj](ARTIFACTS.md#row-517), [23shades-0520-aajddbihf](ARTIFACTS.md#row-520), [23shades-0522-aaadihacg](ARTIFACTS.md#row-522), [23shades-0523-aaiecehba](ARTIFACTS.md#row-523), [23shades-0525-aajbigiad](ARTIFACTS.md#row-525), [23shades-0526-aagejejha](ARTIFACTS.md#row-526), [23shades-0528-aagejdfdj](ARTIFACTS.md#row-528), [23shades-0531-aaffefcib](ARTIFACTS.md#row-531), [23shades-0534-aaeebgfej](ARTIFACTS.md#row-534), [23shades-0538-aafibegcj](ARTIFACTS.md#row-538), [23shades-0539-aaheefgfd](ARTIFACTS.md#row-539), [23shades-0540-aaifgecfh](ARTIFACTS.md#row-540), [23shades-0541-aahafiegd](ARTIFACTS.md#row-541), [23shades-0545-aafbccaac](ARTIFACTS.md#row-545), [23shades-0556-aadhfidia](ARTIFACTS.md#row-556), [23shades-0558-aaibihacc](ARTIFACTS.md#row-558), [23shades-0559-aafdibbge](ARTIFACTS.md#row-559), [23shades-0561-aaegihffd](ARTIFACTS.md#row-561), [23shades-0563-aafihcach](ARTIFACTS.md#row-563), [23shades-0574-aaideghdd](ARTIFACTS.md#row-574), [23shades-0579-aagcdfcie](ARTIFACTS.md#row-579), [23shades-0581-aaeieedge](ARTIFACTS.md#row-581), [23shades-0582-aagbdibae](ARTIFACTS.md#row-582), [23shades-0585-aadggbdcb](ARTIFACTS.md#row-585), [23shades-0595-aafeaijhi](ARTIFACTS.md#row-595), [23shades-0600-aafhihecd](ARTIFACTS.md#row-600), [23shades-0601-aahfgdcad](ARTIFACTS.md#row-601), [23shades-0602-aahidaegb](ARTIFACTS.md#row-602), [23shades-0603-aahgegeef](ARTIFACTS.md#row-603), [23shades-0604-aajcjaefh](ARTIFACTS.md#row-604), [23shades-0607-aagafeacd](ARTIFACTS.md#row-607), [23shades-0608-aaidfjifi](ARTIFACTS.md#row-608), [23shades-0609-aagcdcjae](ARTIFACTS.md#row-609), [23shades-0610-aaegfjdjb](ARTIFACTS.md#row-610), [23shades-0611-aajejahfe](ARTIFACTS.md#row-611), [23shades-0613-aadhcgief](ARTIFACTS.md#row-613), [23shades-0614-aaadihafg](ARTIFACTS.md#row-614), [23shades-0617-aafigfjii](ARTIFACTS.md#row-617), [23shades-0623-aahijjdcb](ARTIFACTS.md#row-623), [23shades-0630-aaeigcjfb](ARTIFACTS.md#row-630), [23shades-0633-aagcdfdia](ARTIFACTS.md#row-633), [23shades-0637-aaffdijjg](ARTIFACTS.md#row-637), [23shades-0638-aaghjajha](ARTIFACTS.md#row-638), [23shades-0639-aaecjeidf](ARTIFACTS.md#row-639), [23shades-0650-aagejhgfd](ARTIFACTS.md#row-650), [23shades-0653-aafajcaia](ARTIFACTS.md#row-653), [23shades-0655-aaeffajfh](ARTIFACTS.md#row-655), [23shades-0679-aaefbfhbj](ARTIFACTS.md#row-679), [23shades-0680-aadhbjgee](ARTIFACTS.md#row-680), [23shades-0684-aaiejaeea](ARTIFACTS.md#row-684), [23shades-0686-aagbiaaje](ARTIFACTS.md#row-686), [23shades-0687-aagbjaigc](ARTIFACTS.md#row-687), [23shades-0688-aafibegea](ARTIFACTS.md#row-688), [23shades-0693-aajacfjhb](ARTIFACTS.md#row-693), [23shades-0694-aaidhabjj](ARTIFACTS.md#row-694), [23shades-0695-aaeeihicj](ARTIFACTS.md#row-695), [23shades-0697-aadhhifdg](ARTIFACTS.md#row-697), [23shades-0699-aaffeacij](ARTIFACTS.md#row-699), [23shades-0700-aaeejihee](ARTIFACTS.md#row-700), [23shades-0701-aaefaahhg](ARTIFACTS.md#row-701), [23shades-0702-aahcjejhi](ARTIFACTS.md#row-702), [23shades-0703-aagaahfid](ARTIFACTS.md#row-703), [23shades-0705-aajdcfhfa](ARTIFACTS.md#row-705), [23shades-0706-aaidjfjdb](ARTIFACTS.md#row-706), [23shades-0707-aaeiefjai](ARTIFACTS.md#row-707), [23shades-0711-aafbjiedd](ARTIFACTS.md#row-711), [23shades-0725-aahicjieh](ARTIFACTS.md#row-725), [23shades-0726-aadejjjdj](ARTIFACTS.md#row-726), [23shades-0729-aafafjdeg](ARTIFACTS.md#row-729), [23shades-0732-aahjacheg](ARTIFACTS.md#row-732), [23shades-0738-aagaeeefj](ARTIFACTS.md#row-738), [23shades-0739-aaibgjddj](ARTIFACTS.md#row-739), [23shades-0740-aagdjibjh](ARTIFACTS.md#row-740), [23shades-0741-aaigbchde](ARTIFACTS.md#row-741), [23shades-0744-aaefediad](ARTIFACTS.md#row-744), [23shades-0747-aafighdeg](ARTIFACTS.md#row-747), [23shades-0748-aaidaidid](ARTIFACTS.md#row-748), [23shades-0749-aaihgdiif](ARTIFACTS.md#row-749), [23shades-0750-aagbdibbb](ARTIFACTS.md#row-750), [23shades-0753-aaeejgbaa](ARTIFACTS.md#row-753), [23shades-0756-aahegjjea](ARTIFACTS.md#row-756), [23shades-0760-aajbhfbhg](ARTIFACTS.md#row-760), [23shades-0762-aaedhjhei](ARTIFACTS.md#row-762), [23shades-0764-aadiicibd](ARTIFACTS.md#row-764), [23shades-0765-aaffdgbgi](ARTIFACTS.md#row-765), [23shades-0766-aajacaegf](ARTIFACTS.md#row-766), [23shades-0768-aaahbfbgd](ARTIFACTS.md#row-768), [23shades-0771-aadgffgjf](ARTIFACTS.md#row-771), [23shades-0775-aahjejdja](ARTIFACTS.md#row-775), [23shades-0776-aaieahjdd](ARTIFACTS.md#row-776), [23shades-0787-aafhfhjbf](ARTIFACTS.md#row-787), [23shades-0788-aahiebjbd](ARTIFACTS.md#row-788), [23shades-0791-aahgcaaac](ARTIFACTS.md#row-791), [23shades-0793-aahefcehd](ARTIFACTS.md#row-793), [23shades-0794-aahdadjbj](ARTIFACTS.md#row-794), [23shades-0795-aagibcfja](ARTIFACTS.md#row-795), [23shades-0805-aajfiefig](ARTIFACTS.md#row-805), [23shades-0806-aahjgiagj](ARTIFACTS.md#row-806), [23shades-0811-aahciiijc](ARTIFACTS.md#row-811), [23shades-0812-aahciiijc](ARTIFACTS.md#row-812), [23shades-0814-aajficacj](ARTIFACTS.md#row-814), [23shades-0816-aajgefjja](ARTIFACTS.md#row-816), [23shades-0817-aajfiegif](ARTIFACTS.md#row-817), [23shades-0819-aageebhag](ARTIFACTS.md#row-819), [23shades-0820-aajggjjdf](ARTIFACTS.md#row-820), [23shades-0821-aajgcfgdg](ARTIFACTS.md#row-821), [23shades-0823-aahfibidg](ARTIFACTS.md#row-823), [23shades-0825-aaicfehca](ARTIFACTS.md#row-825), [23shades-0827-aaeiedacj](ARTIFACTS.md#row-827), [23shades-0830-aajfigjji](ARTIFACTS.md#row-830), [23shades-0833-aajggbgdc](ARTIFACTS.md#row-833), [23shades-0836-aajfhhbig](ARTIFACTS.md#row-836), [23shades-0837-aaicicaia](ARTIFACTS.md#row-837), [23shades-0839-aaicgfbda](ARTIFACTS.md#row-839), [23shades-0840-aaeidjejd](ARTIFACTS.md#row-840), [23shades-0841-aagcbggid](ARTIFACTS.md#row-841), [23shades-0842-aajgchffb](ARTIFACTS.md#row-842), [23shades-0843-aahjgeiic](ARTIFACTS.md#row-843), [23shades-0844-aaibicege](ARTIFACTS.md#row-844), [23shades-0846-aabgahibh](ARTIFACTS.md#row-846), [23shades-0848-aahiefidd](ARTIFACTS.md#row-848), [23shades-0850-aahighbdb](ARTIFACTS.md#row-850), [23shades-0852-aaibijdfi](ARTIFACTS.md#row-852), [23shades-0856-aaicaiffi](ARTIFACTS.md#row-856)

## SATD-U · 材料不足以细化待办

**定义：** 可用注释只有标记、名称、外链或被截断的指代，不能可靠定位待改机制。

**纳入：** 空 TODO/FIXME、没有动作的对象名、未获取外链以及关键句尾缺失。

**排除与边界：** 已明确 implement/refactor 可编码其一般方向；不得据周边名称补造机制。

**例证：**

- [23shades-0002-aaehidhih](ARTIFACTS.md#row-2)：只有 TODO，不能确定工作对象。
- [23shades-0014-aadbjfiab](ARTIFACTS.md#row-14)：空 TODO。
- [23shades-0023-aajffebhi](ARTIFACTS.md#row-23)：空 TODO。

**全部成员（逐条证据在链接中）：**

[23shades-0002-aaehidhih](ARTIFACTS.md#row-2), [23shades-0014-aadbjfiab](ARTIFACTS.md#row-14), [23shades-0023-aajffebhi](ARTIFACTS.md#row-23), [23shades-0031-aagbibedf](ARTIFACTS.md#row-31), [23shades-0047-aajdbecaa](ARTIFACTS.md#row-47), [23shades-0051-aagacefbc](ARTIFACTS.md#row-51), [23shades-0067-aagbghgdd](ARTIFACTS.md#row-67), [23shades-0069-aafdeebba](ARTIFACTS.md#row-69), [23shades-0070-aahfheeac](ARTIFACTS.md#row-70), [23shades-0095-aadgfjhjj](ARTIFACTS.md#row-95), [23shades-0117-aajcgbifg](ARTIFACTS.md#row-117), [23shades-0124-aafacjjjb](ARTIFACTS.md#row-124), [23shades-0127-aafhjffeb](ARTIFACTS.md#row-127), [23shades-0128-aaeccdahj](ARTIFACTS.md#row-128), [23shades-0139-aaiiihajd](ARTIFACTS.md#row-139), [23shades-0148-aaeigcigi](ARTIFACTS.md#row-148), [23shades-0149-aajbfcgda](ARTIFACTS.md#row-149), [23shades-0153-aajacaegh](ARTIFACTS.md#row-153), [23shades-0175-aafecgahb](ARTIFACTS.md#row-175), [23shades-0179-aafehjdhc](ARTIFACTS.md#row-179), [23shades-0180-aahddifgi](ARTIFACTS.md#row-180), [23shades-0181-aaggbcefi](ARTIFACTS.md#row-181), [23shades-0182-aafhddaff](ARTIFACTS.md#row-182), [23shades-0183-aagabbjac](ARTIFACTS.md#row-183), [23shades-0184-aagbcgbed](ARTIFACTS.md#row-184), [23shades-0185-aadbfigaf](ARTIFACTS.md#row-185), [23shades-0186-aafacidaf](ARTIFACTS.md#row-186), [23shades-0187-aadfababd](ARTIFACTS.md#row-187), [23shades-0188-aadgjgddc](ARTIFACTS.md#row-188), [23shades-0189-aaggiaccc](ARTIFACTS.md#row-189), [23shades-0190-aabdibfbd](ARTIFACTS.md#row-190), [23shades-0191-aafijfbah](ARTIFACTS.md#row-191), [23shades-0192-aahdfcffj](ARTIFACTS.md#row-192), [23shades-0193-aajfaiafb](ARTIFACTS.md#row-193), [23shades-0194-aagfeabcg](ARTIFACTS.md#row-194), [23shades-0195-aaibgjfcg](ARTIFACTS.md#row-195), [23shades-0196-aaahgjjag](ARTIFACTS.md#row-196), [23shades-0218-aajbfefjj](ARTIFACTS.md#row-218), [23shades-0257-aagcfdhaj](ARTIFACTS.md#row-257), [23shades-0263-aadbfihhc](ARTIFACTS.md#row-263), [23shades-0279-aafegiaee](ARTIFACTS.md#row-279), [23shades-0281-aafegiafa](ARTIFACTS.md#row-281), [23shades-0282-aafegiafa](ARTIFACTS.md#row-282), [23shades-0289-aafegibaf](ARTIFACTS.md#row-289), [23shades-0304-aahddgcai](ARTIFACTS.md#row-304), [23shades-0315-aaecghbei](ARTIFACTS.md#row-315), [23shades-0357-aaedcebbj](ARTIFACTS.md#row-357), [23shades-0371-aaadajhci](ARTIFACTS.md#row-371), [23shades-0391-aagfeabbh](ARTIFACTS.md#row-391), [23shades-0413-aajdhaicc](ARTIFACTS.md#row-413), [23shades-0414-aaiiaefbb](ARTIFACTS.md#row-414), [23shades-0426-aagdeighd](ARTIFACTS.md#row-426), [23shades-0427-aajdaiegb](ARTIFACTS.md#row-427), [23shades-0428-aaeabafjh](ARTIFACTS.md#row-428), [23shades-0429-aaahcadfb](ARTIFACTS.md#row-429), [23shades-0430-aagaiecgg](ARTIFACTS.md#row-430), [23shades-0431-aahfjddad](ARTIFACTS.md#row-431), [23shades-0432-aadghfgba](ARTIFACTS.md#row-432), [23shades-0435-aagbbijhe](ARTIFACTS.md#row-435), [23shades-0462-aadehggdg](ARTIFACTS.md#row-462), [23shades-0463-aaejdhjid](ARTIFACTS.md#row-463), [23shades-0467-aaididaaj](ARTIFACTS.md#row-467), [23shades-0489-aaiiigjef](ARTIFACTS.md#row-489), [23shades-0503-aadgffbjj](ARTIFACTS.md#row-503), [23shades-0522-aaadihacg](ARTIFACTS.md#row-522), [23shades-0529-aaeieeeje](ARTIFACTS.md#row-529), [23shades-0530-aajacfjji](ARTIFACTS.md#row-530), [23shades-0541-aahafiegd](ARTIFACTS.md#row-541), [23shades-0545-aafbccaac](ARTIFACTS.md#row-545), [23shades-0563-aafihcach](ARTIFACTS.md#row-563), [23shades-0573-aaidjgaag](ARTIFACTS.md#row-573), [23shades-0576-aaeihdcgb](ARTIFACTS.md#row-576), [23shades-0587-aaeiebjie](ARTIFACTS.md#row-587), [23shades-0605-aaeiedgej](ARTIFACTS.md#row-605), [23shades-0608-aaidfjifi](ARTIFACTS.md#row-608), [23shades-0614-aaadihafg](ARTIFACTS.md#row-614), [23shades-0653-aafajcaia](ARTIFACTS.md#row-653), [23shades-0685-aaheajiai](ARTIFACTS.md#row-685), [23shades-0690-aahafiehj](ARTIFACTS.md#row-690), [23shades-0704-aagfjeihb](ARTIFACTS.md#row-704), [23shades-0705-aajdcfhfa](ARTIFACTS.md#row-705), [23shades-0752-aagfegjcg](ARTIFACTS.md#row-752), [23shades-0771-aadgffgjf](ARTIFACTS.md#row-771), [23shades-0818-aajghfhbg](ARTIFACTS.md#row-818), [23shades-0841-aagcbggid](ARTIFACTS.md#row-841), [23shades-0846-aabgahibh](ARTIFACTS.md#row-846)

## SATD-V · 未明确承认待偿还问题

**定义：** 材料主要解释现有操作、必要性、约束或已成立行为，没有明确待办或负面判断。

**纳入：** 说明性注释、正常兼容用途、现有补偿效果；可与其实际主题并存。

**排除与边界：** 明确未完成、错误或质量不足不归本类；不是宣称整个仓库无技术债。

**例证：**

- [23shades-0050-aabcjdaea](ARTIFACTS.md#row-50)：零和游戏与两个值导致 error 乘二的注释；未明确说这种做法错误，需保留不确定性。
- [23shades-0056-aaeeibecj](ARTIFACTS.md#row-56)：circular shift 被描述为正确相位所需；未表述待偿还债务，不强制归为错误。
- [23shades-0057-aajffjdic](ARTIFACTS.md#row-57)：按参数空间需要构造 grids/weights，未明确欠缺或问题。

**全部成员（逐条证据在链接中）：**

[23shades-0050-aabcjdaea](ARTIFACTS.md#row-50), [23shades-0056-aaeeibecj](ARTIFACTS.md#row-56), [23shades-0057-aajffjdic](ARTIFACTS.md#row-57), [23shades-0106-aaefdgjbi](ARTIFACTS.md#row-106), [23shades-0122-aahjceiih](ARTIFACTS.md#row-122), [23shades-0129-aahfhegdd](ARTIFACTS.md#row-129), [23shades-0130-aaijaggcb](ARTIFACTS.md#row-130), [23shades-0142-aaeeiicii](ARTIFACTS.md#row-142), [23shades-0143-aahfjhgbi](ARTIFACTS.md#row-143), [23shades-0144-aajhbagib](ARTIFACTS.md#row-144), [23shades-0145-aahjiddhj](ARTIFACTS.md#row-145), [23shades-0146-aafedbhaj](ARTIFACTS.md#row-146), [23shades-0147-aafedbhaj](ARTIFACTS.md#row-147), [23shades-0150-aahfhedig](ARTIFACTS.md#row-150), [23shades-0168-aafdifcji](ARTIFACTS.md#row-168), [23shades-0169-aafbjfcfe](ARTIFACTS.md#row-169), [23shades-0171-aahfefcag](ARTIFACTS.md#row-171), [23shades-0172-aaahfegjh](ARTIFACTS.md#row-172), [23shades-0176-aadhfdfce](ARTIFACTS.md#row-176), [23shades-0364-aaifjjccj](ARTIFACTS.md#row-364), [23shades-0385-aaegicgcc](ARTIFACTS.md#row-385), [23shades-0697-aadhhifdg](ARTIFACTS.md#row-697), [23shades-0728-aadhcgicg](ARTIFACTS.md#row-728), [23shades-0808-aadbcegej](ARTIFACTS.md#row-808), [23shades-0826-aaeieahii](ARTIFACTS.md#row-826), [23shades-0855-aaeachbce](ARTIFACTS.md#row-855)
