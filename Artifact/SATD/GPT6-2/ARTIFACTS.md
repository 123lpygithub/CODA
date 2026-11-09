# SATD · 全部 artifact 逐条分析

阅读范围和证据限制见 [METHOD.md](METHOD.md)。原文全文在 [artifacts.jsonl](artifacts.jsonl)。

<a id="row-1"></a>
## 1. 23shades-0001-aahiieiig

**主题代码：** SATD-A

**开放代码：** 共享逻辑组织待重构

**逐条判断：** 多个算法共用函数，作者明确承诺后续重构；不是模型算法本身未实现。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `135:222`：

> ''' || Functions used by more than one algorithm || TODO refactor properly later || '''

<a id="row-2"></a>
## 2. 23shades-0002-aaehidhih

**主题代码：** SATD-U

**开放代码：** 证据不足

**逐条判断：** 只有 TODO，不能确定工作对象。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `140:145`：

> !TODO

<a id="row-3"></a>
## 3. 23shades-0003-aaejjbhji

**主题代码：** SATD-A

**开放代码：** 容器选择待简化

**逐条判断：** 作者指出空字典也能满足需求；句子截断，替代方案的完整限制不明。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `128:208`：

> !TODO: An empty dictionary would actually also do here ... despite the fact that

<a id="row-4"></a>
## 4. 23shades-0004-aaejjacgf

**主题代码：** SATD-B

**开放代码：** 数值容器容量不足

**逐条判断：** US 无法容纳某些完整数值；不推断 US 具体类型或位宽。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `145:211`：

> !TODO: In some cases; US is not enough to hold the complete number

<a id="row-5"></a>
## 5. 23shades-0005-aaebbecaa

**主题代码：** SATD-H

**开放代码：** 布局缺陷的临时绕行

**逐条判断：** justify-content 失效导致采用 SVG 居中 hack；问题在显示布局。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `115:165`：

> # Hack to center SVG as justify-content is broken:

<a id="row-6"></a>
## 6. 23shades-0006-aaahbghib

**主题代码：** SATD-A, SATD-H

**开放代码：** 文本处理临时实现待替换

**逐条判断：** 作者希望用正则或其他方案替代 hack，未提供具体处理内容。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `127:169`：

> # hackier; fixme to use regex or something

<a id="row-7"></a>
## 7. 23shades-0007-aaaegfgeb

**主题代码：** SATD-B

**开放代码：** 变换顺序待调整

**逐条判断：** 要求 concat 前 reverse bw；bw 含义缺失，不推断具体网络结构。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `128:160`：

> # reverse bw; before concat TODO

<a id="row-8"></a>
## 8. 23shades-0008-aagcbjjcd

**主题代码：** SATD-D

**开放代码：** 验证与测试数据处理不完整

**逐条判断：** landmarks 只未扩展到 validation/test；明确因当日疲劳推迟，不是单元测试缺失。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `155:259`：

> # TODO : load landmarks in validation and test set also. I'm too sleepy to do it today -_- zzz... zzz...

<a id="row-9"></a>
## 9. 23shades-0009-aagdfgjig

**主题代码：** SATD-A

**开放代码：** 模型调用位置待迁移

**逐条判断：** 将当前模型调用改为远程调用；没有证据说明出于性能或隐私。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `139:173`：

> # TODO Change to call remote model

<a id="row-10"></a>
## 10. 23shades-0010-aaaedagad

**主题代码：** SATD-Q

**开放代码：** 元数据字段改写待定

**逐条判断：** name/index/uuid 可能需要重写；是候选修改而非已确认错误。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `147:197`：

> # TODO May want to rewrite name; index; uuid; etc.

<a id="row-11"></a>
## 11. 23shades-0011-aageijaai

**主题代码：** SATD-J, SATD-Q

**开放代码：** 参数可训练性待决策

**逐条判断：** 询问 gains/biases 是否应可训练，保留设计疑问。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `139:188`：

> # TODO: do we want gains\/biases to be trainable?

<a id="row-12"></a>
## 12. 23shades-0012-aafaehach

**主题代码：** SATD-D, SATD-J

**开放代码：** 缺省命名行为待补充

**逐条判断：** name 缺失时拟采用 functionality.__name__。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `169:236`：

> # TODO: Set name (using \"functionality.__name__\") if name is None

<a id="row-13"></a>
## 13. 23shades-0013-aaebbeedd

**主题代码：** SATD-E

**开放代码：** 分支支持不全

**逐条判断：** 其他 bases 尚未被处理；不推断 bases 是数制还是父类。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `117:162`：

> ## elif (): ## FIXME: handle other bases here

<a id="row-14"></a>
## 14. 23shades-0014-aadbjfiab

**主题代码：** SATD-U

**开放代码：** 证据不足

**逐条判断：** 空 TODO。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `194:202`：

> ## TODO:

<a id="row-15"></a>
## 15. 23shades-0015-aaibjbide

**主题代码：** SATD-E

**开放代码：** 模型行为覆盖不全

**逐条判断：** 需对全部模型加入 intercept；intercept 的具体语义不明。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `131:164`：

> ## TODO: intercept for all models

<a id="row-16"></a>
## 16. 23shades-0016-aadfachjd

**主题代码：** SATD-E

**开放代码：** 优化器支持不全

**逐条判断：** 当前只支持 SGD，希望增加其他训练优化器；不属于执行性能证据。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `145:181`：

> ##TODO add optimizers other than SGD

<a id="row-17"></a>
## 17. 23shades-0017-aaffedgad

**主题代码：** SATD-A

**开放代码：** 参数复制方式待改进

**逐条判断：** 明确改进 copying of parameters，但未说明错误或开销。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `127:167`：

> #TODO: improve the copying of parameters

<a id="row-18"></a>
## 18. 23shades-0018-aajcabgbe

**主题代码：** SATD-L

**开放代码：** 教程材料待补充

**逐条判断：** 认为现有内容可转成生成 phantoms 的教程。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `117:179`：

> #TODO: this can become a nice tutorial for generating phantoms

<a id="row-19"></a>
## 19. 23shades-0019-aaigjhibg

**主题代码：** SATD-F

**开放代码：** 兼容性待修复

**逐条判断：** 只给 fix compatibility，版本和对象缺失。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `155:197`：

> ((); 0); # TODO(sonots): Fix compatibility

<a id="row-20"></a>
## 20. 23shades-0020-aaigjhiah

**主题代码：** SATD-F

**开放代码：** 兼容性待修复

**逐条判断：** 与前条文本一致但保留独立 artifact；兼容对象不明。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `160:202`：

> ((); 0); # TODO(sonots): Fix compatibility

<a id="row-21"></a>
## 21. 23shades-0021-aadbhiccj

**主题代码：** SATD-D

**开放代码：** 工作流组件集成缺失

**逐条判断：** Frontend 和 Model 尚待纳入该 workflow。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `122:173`：

> @todo integrate Frontend and Model to that workflow

<a id="row-22"></a>
## 22. 23shades-0022-aahdfibcf

**主题代码：** SATD-J, SATD-Q

**开放代码：** 测试专用参数残留

**逐条判断：** TODO 指出 nrows 仅用于测试；应关注参数用途，但未说明删除或替代方案，保留待办意图与处置不确定性。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `150:182`：

> @todo nrows is for testing only!

<a id="row-23"></a>
## 23. 23shades-0023-aajffebhi

**主题代码：** SATD-U

**开放代码：** 证据不足

**逐条判断：** 空 TODO。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `134:140`：

> @TODO:

<a id="row-24"></a>
## 24. 23shades-0024-aaeibiccf

**主题代码：** SATD-E

**开放代码：** 字符编码特殊映射缺失

**逐条判断：** arabtex 与 iso8859-6 的某些一对二映射需要独立处理；末句截断。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `133:230`：

> @todo: arabtex and iso8859-6 need individual handling because in some cases using one-two mapping

<a id="row-25"></a>
## 25. 23shades-0025-aajffcjii

**主题代码：** SATD-A

**开放代码：** 代码格式待整理

**逐条判断：** 目标是 20.07 release 的代码格式问题。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `149:195`：

> @TODO: code formatting issue for 20.07 release

<a id="row-26"></a>
## 26. 23shades-0026-aajffcjfa

**主题代码：** SATD-A

**开放代码：** 代码格式待整理

**逐条判断：** 要求处理 20.07 release 的代码格式问题；与第 25 条同文，但来源文件不同，保留独立 artifact。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `143:189`：

> @TODO: code formatting issue for 20.07 release

<a id="row-27"></a>
## 27. 23shades-0027-aajfegaca

**主题代码：** SATD-Q

**开放代码：** 方案不满意但对象不明

**逐条判断：** 只有需要更好方案，无具体机制可归纳。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `125:153`：

> @TODO: need better solutions

<a id="row-28"></a>
## 28. 23shades-0028-aajfejeha

**主题代码：** SATD-A

**开放代码：** 结构重构待办

**逐条判断：** 明确 refactor，无可判断的重构对象。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `130:149`：

> @TODO: Refactor !!!

<a id="row-29"></a>
## 29. 23shades-0029-aajfejjdb

**主题代码：** SATD-A

**开放代码：** 时间依赖接口待封装

**逐条判断：** 拟移除显式 time 使用并转入内部实现；不是简单删除全部功能。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `141:188`：

> @TODO: remove time usage; use it under the hood

<a id="row-30"></a>
## 30. 23shades-0030-aaedcebdc

**主题代码：** SATD-B

**开放代码：** 预测接口行为错误

**逐条判断：** 作者明确称 bug，predict_proba 不应 change；具体改变对象截断。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `130:184`：

> [todo]: this is a bug; predict_proba should not change

<a id="row-31"></a>
## 31. 23shades-0031-aagbibedf

**主题代码：** SATD-Q, SATD-U

**开放代码：** 未定位的模型实现待办

**逐条判断：** 完整阅读注释内 Hopfield/Hooke 模型初始化、条件概率与导数代码；TODO 未指向某段，不能把代码出现的梯度/权重均认定为债务。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `126:3226`：

> \"\"\"   || #TODO: || class HopfieldModel(LatentModel): ||      ||     def __init__(self; nvis; nhid): ||         self.layers = {} ||         self.layers['visible'] = layers.IsingLayer(nvis) ||         self.layers['hidden'] = layers.GaussianLayer(nhid) ||          ||         self.params = {} ||         self.params['weights'] = numpy.random.normal(loc=0.0; scale=1.0; size=(self.layers['visible'].len; self.layers['hidden'].len)).astype(dtype=numpy.float32) ||         self.params['bias'] = numpy.ones_like(self.layers['visible'].loc)   ||  ||  || class HookeMachine(LatentModel): ||      ||     def __init__(self; nvis; nhid; vis_type='gauss'; hid_type='expo'):    ||         assert vis_type.lower() in ['gauss'; 'ising'] ||         assert hid_type.lower() in ['expo'; 'bern'] ||          ||         self.layers = {} ||         self.layers['visible'] = layers.get(vis_type)(nvis) ||         self.layers['hidden'] = layers.get(hid_type)(nhid) ||          ||         self.params = {} ||         self.params['weights'] = numpy.random.normal(loc=0.0; scale=1.0; size=(self.layers['visible'].len; self.layers['hidden'].len)).astype(dtype=numpy.float32) ||         self.params['bias'] = numpy.ones_like(self.layers['hidden'].loc)   ||         self.params['T'] = numpy.ones(1; dtype=numpy.float32) ||                  ||         self.deriv = {} ||         self.deriv['weights'] = numpy.zeros_like(self.params['weights']) ||         self.deriv['bias'] = numpy.zeros_like(self.params['bias']) ||         self.params['T'] = numpy.zeros_like(self.params['T']) ||          ||         self.set_vis(numpy.zeros_like(self.layers['visible'].loc)) ||          ||     def set_vis(self; vis): ||         self.vis = vis ||         self.diff = (self.params['weights'].T - vis).T ||         self.squared_dist = numpy.sum(self.diff ** 2; axis=0) ||         self.layers['hidden'].update_params(self.params['bias'] + self.squared_dist \/ (2 * self.params['T'])) ||         self.energy = -numpy.sum(numpy.log(self.layers['hidden'].partition_function()))         ||          ||     def visible_conditional_params(self; hid): ||         total = numpy.sum(hid) ||         loc = numpy.dot(self.params['weights']; hid) \/ total ||         scale = self.params['T'] \/ total * numpy.ones_like(self.layers['visible'].loc) ||         return (loc; scale) ||          ||     def update_visible_params(self; hid): ||         self.layers['visible'].update_params(*self.visible_conditional_params(hid)) ||          ||     def derivatives(self; vis; key): ||         self.update_hidden_params(vis) ||         hidden_mean = self.layers['hidden'].mean() ||         if key == 'bias': ||             # del H(v; k) \/ del b ||             return hidden_mean ||         elif key == 'weights': ||             # del H(v; k) \/ del W ||             return (self.difference(vis) * hidden_mean.T) \/ self.params['T'] ||         elif key == 'T': ||             # del H(v;k) \/ del T ||             return numpy.dot(hidden_mean.T; self.squared_distance(vis)) ||         else: ||             raise ValueError('unknown key: {}'.format(key)) ||     \"\"\"

<a id="row-32"></a>
## 32. 23shades-0032-aaejahaed

**主题代码：** SATD-L

**开放代码：** 文档缺失

**逐条判断：** doc 占位待写。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `123:163`：

> \"\"\" || .. todo:: ||     doc || \"\"\"

<a id="row-33"></a>
## 33. 23shades-0033-aadhcadac

**主题代码：** SATD-L

**开放代码：** 模块说明缺失

**逐条判断：** hyperband synopsis 与长描述为 TODO，占位文档未完成。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `130:358`：

> \"\"\" || :mod:`orion.algo.hyperband.hyperband -- TODO || ================================================= ||  || .. module:: hyperband ||     :platform: Unix ||     :synopsis: TODO ||  || TODO: Write long description || \"\"\"

<a id="row-34"></a>
## 34. 23shades-0034-aaibjcgbi

**主题代码：** SATD-B

**开放代码：** 示例算法行为错误

**逐条判断：** FastICA 点云示例被明确描述为 still buggy；缺少错误机制。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `133:271`：

> \"\"\" || ========================== || FastICA on 2D point clouds || ========================== ||  || XXX: Still buggy !!! ||  || \"\"\"

<a id="row-35"></a>
## 35. 23shades-0035-aahfiaifg

**主题代码：** SATD-B, SATD-N

**开放代码：** 序列化格式不符

**逐条判断：** CSV corpus 实际仍输出 SVMLight，作者邀请修改。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `132:242`：

> \"\"\" || Corpus in CSV format. TODO: still serializes to SVMLight format; feel free to change this. || \"\"\"

<a id="row-36"></a>
## 36. 23shades-0036-aaibigjdc

**主题代码：** SATD-D

**开放代码：** 示例数据集待替换

**逐条判断：** 高斯混合绘图例子计划采用 faithful dataset；未称当前数据错误。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `126:230`：

> \"\"\" || Simple Gaussian Mixture model plotting example ||  || TODO: use the faithful dataset || \"\"\"

<a id="row-37"></a>
## 37. 23shades-0037-aajffhihe

**主题代码：** SATD-E, SATD-F, SATD-G

**开放代码：** 语法支持不全；编译路径性能改进

**逐条判断：** unparse 只支持列举的语法结构；拟转 _ast 因编译约快六倍，两项均有明确依据。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `148:704`：

> \"\"\" Turn compiler.ast structures back into executable python code. ||  ||     The unparse method takes a compiler.ast tree and transforms it back into ||     valid python code.  It is incomplete and currently only works for ||     import statements; function calls; function definitions; assignments; and ||     basic expressions. ||  ||     Inspired by python-2.5-svn\/Demo\/parser\/unparse.py ||  ||     fixme: We may want to move to using _ast trees because the compiler for ||            them is about 6 times faster than compiler.compile. || \"\"\"

<a id="row-38"></a>
## 38. 23shades-0038-aaeiaheab

**主题代码：** SATD-K, SATD-M

**开放代码：** 测试缺失；实现清理待办

**逐条判断：** MdC 到 Unicode 转换需要增加测试与清理代码。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `116:212`：

> \"\"\"Convert MdC transliterated text to Unicode. ||  || TODO: Add tests and clean up. || \"\"\"

<a id="row-39"></a>
## 39. 23shades-0039-aaehiecae

**主题代码：** SATD-E

**开放代码：** 字符编码特例支持不全

**逐条判断：** 缺 perseus-style iota subscript 和 diaeresis。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `136:268`：

> \"\"\"Converts legacy encodings into Unicode || TODO for replacer.py: ||  - add perseus-style iota subscript and diaeresis || \"\"\"

<a id="row-40"></a>
## 40. 23shades-0040-aaeiahgad

**主题代码：** SATD-F, SATD-K

**开放代码：** 外部依赖移除待办；测试缺失

**逐条判断：** Unicode 转换模块拟移除 regex 依赖并增加测试。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `132:239`：

> \"\"\"Converts legacy encodings into Unicode. ||  || TODO: Rm regex dependency || TODO: Add tests || \"\"\"

<a id="row-41"></a>
## 41. 23shades-0041-aahdeachi

**主题代码：** SATD-L

**开放代码：** 模型概念说明不完整

**逐条判断：** Models 文档中的 more 待补；函数列表本身不证明这些函数未实现。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `130:503`：

> \"\"\"Models. ||  || Models are objects which take Tensor(s) as input; perform some computation on  || those Tensor(s); and output probability distributions. ||  || TODO: more... ||  || * :func:`.Model` || * :func:`.ContinuousModel` || * :func:`.DiscreteModel` || * :func:`.CategoricalModel` || * :func:`.save_model` || * :func:`.load_model` ||  || ---------- ||  || \"\"\"

<a id="row-42"></a>
## 42. 23shades-0042-aabgebcce

**主题代码：** SATD-L

**开放代码：** 特征提取实现缺失；文档不足

**逐条判断：** 模块明确待实现 metafeatures 并改善文档。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `130:283`：

> \"\"\"Module dedicated to extraction of Model Based Metafeatures. ||  || Todo: ||     * Implement metafeatures. ||     * Improve documentation. || \"\"\"

<a id="row-43"></a>
## 43. 23shades-0043-aaehiefac

**主题代码：** SATD-D

**开放代码：** 语料清洗步骤缺失

**逐条判断：** 补 TLG/PHI 清理、非 ASCII 移除、通用 HTML 清理。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `114:428`：

> \"\"\"Process downloaded or local corpora from one format into another. || Some formatting can happen here; or invoke language-specific formatters in || other files. ||  || #TODO: Add TLG & PHI text cleaners from KJ's IPython notebooks || #TODO: Add non-ascii stripper || #TODO: Add generic HTML stripper || \"\"\"

<a id="row-44"></a>
## 44. 23shades-0044-aaeibhiie

**主题代码：** SATD-D

**开放代码：** 字符转换功能缺失

**逐条判断：** Hebrew-to-Aramaic 转换器待添加。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `116:319`：

> \"\"\"The Imperial Aramaic alphabet; plus simple script to transform || a Hebrew transcription of an Imperial Aramaic text to its own Unicode block. ||  || TODO: Add Hebrew-to-Aramaic converter || \"\"\"

<a id="row-45"></a>
## 45. 23shades-0045-aajdcegja

**主题代码：** SATD-L, SATD-N

**开放代码：** 差异格式契约未定义

**逐条判断：** diff 格式需要定义并文档化；版本转换已由 nbformat 处理，不能误码为版本支持缺失。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `132:425`：

> \"\"\"Tools for diffing notebooks. ||  || All diff tools here currently assumes the notebooks have already been || converted to the same format version; currently v4 at time of writing. || Up- and down-conversion is handled by nbformat. ||  || FIXME: Define and document diff format. || \"\"\"

<a id="row-46"></a>
## 46. 23shades-0046-aafchcgjg

**主题代码：** SATD-H, SATD-I

**开放代码：** 缺失置信度以常数代替

**逐条判断：** 上游未提供 confidence，临时填 1；不能当作真实置信度。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `115:219`：

> \"confidence\": 1  # todo discussion confidence from GNormPlus is not provided so just putting in here 1

<a id="row-47"></a>
## 47. 23shades-0047-aajdbecaa

**主题代码：** SATD-U

**开放代码：** 证据不足

**逐条判断：** PickupAbove 的 TODO 占位未说明目标行为。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `124:148`：

> \"PickupAbove\": [TODO];

<a id="row-48"></a>
## 48. 23shades-0048-aagaijehb

**主题代码：** SATD-C

**开放代码：** 参数兼容检查缺失

**逐条判断：** 未来需要验证参数间兼容性。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `122:174`：

> \/\/TODO in future add arguments compatibility check

<a id="row-49"></a>
## 49. 23shades-0049-aagaggihd

**主题代码：** SATD-D, SATD-E

**开放代码：** 多 GPU 执行支持缺失

**逐条判断：** 给出 CUDA_VISIBLE_DEVICES 和 DataParallel 作为未来扩展。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `110:282`：

> A future enhancement TODO for running on multiple GPU: CUDA_VISIBLE_DEVICES=2;3 python main.py   and then also model = torch.nn.DataParallel(model; device_ids=[0;1]).cuda()

<a id="row-50"></a>
## 50. 23shades-0050-aabcjdaea

**主题代码：** SATD-I, SATD-Q, SATD-V

**开放代码：** 训练误差缩放假设

**逐条判断：** 零和游戏与两个值导致 error 乘二的注释；未明确说这种做法错误，需保留不确定性。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `137:217`：

> all games are zero sum that are trained and because 2 values; x2 the error.  XXX

<a id="row-51"></a>
## 51. 23shades-0051-aagacefbc

**主题代码：** SATD-Q, SATD-U

**开放代码：** 生成范围待明确

**逐条判断：** All possibilities will be generated 后有 TODO，但缺少具体待改动作；不能推断穷举算法缺陷，也不能忽略待办标记。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `138:178`：

> All possibilities will be generated TODO

<a id="row-52"></a>
## 52. 23shades-0052-aaahbjdic

**主题代码：** SATD-F

**开放代码：** 特定版本依赖行为异常

**逐条判断：** package_deps 在 3.4 中似乎损坏；保留 apparently 的不确定性。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `112:153`：

> apparently package_deps are broken in 3.4

<a id="row-53"></a>
## 53. 23shades-0053-aaijeahdh

**主题代码：** SATD-H

**开放代码：** 函数调用包装绕行

**逐条判断：** 通过 wrap 并在 __call__ 调用实现 workaround；底层原因未给出。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `158:229`：

> As a workaround; we wrap the function and invoke it in __call__ method.

<a id="row-54"></a>
## 54. 23shades-0054-aadaieabb

**主题代码：** SATD-D, SATD-I, SATD-N

**开放代码：** 固定标签长度假设；接受钩子缺失

**逐条判断：** 当前假定四字节 magic label，拟加 _accept hook。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `164:223`：

> assuming a 4-byte magic label (FIXME: add \"_accept\" hook)

<a id="row-55"></a>
## 55. 23shades-0055-aafeacaha

**主题代码：** SATD-B

**开放代码：** 零长度边界处理调整

**逐条判断：** 拟遍历并将 length=0 提升到 0.125；未说明长度对象。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `122:190`：

> BETTER FIX: iterate through; if length = 0; then bump it up to 0.125

<a id="row-56"></a>
## 56. 23shades-0056-aaeeibecj

**主题代码：** SATD-V

**开放代码：** 信号相位处理说明

**逐条判断：** circular shift 被描述为正确相位所需；未表述待偿还债务，不强制归为错误。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `116:168`：

> circular shift the signal (needed for correct phase)

<a id="row-57"></a>
## 57. 23shades-0057-aajffjdic

**主题代码：** SATD-V

**开放代码：** 按需构造行为说明

**逐条判断：** 按参数空间需要构造 grids/weights，未明确欠缺或问题。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `160:217`：

> Construct grids and weights if needed for parameter space

<a id="row-58"></a>
## 58. 23shades-0058-aaahbfbhe

**主题代码：** SATD-M, SATD-Q

**开放代码：** 疑似废弃逻辑

**逐条判断：** 作者询问是否 deprecate，认为可能不再需要；尚未裁决。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `123:170`：

> DEPRICATE? I don't think this is needed anymore

<a id="row-59"></a>
## 59. 23shades-0059-aacjfgieb

**主题代码：** SATD-B, SATD-O

**开放代码：** 换行渲染异常

**逐条判断：** 双换行似乎影响显示；原因不明。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `122:169`：

> Double newlines seem to mess with the rendering

<a id="row-60"></a>
## 60. 23shades-0060-aaebhejej

**主题代码：** SATD-H, SATD-J

**开放代码：** 测试性临时配置

**逐条判断：** dynamic_pad=True 是 HACK TESTING，未证明正式行为应保持该值。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `159:208`：

> dynamic_pad=True) # HACK TESTING dynamic_pad=True

<a id="row-61"></a>
## 61. 23shades-0061-aagfgggge

**主题代码：** SATD-D

**开放代码：** 早停功能推迟

**逐条判断：** early_stopping 标注下一版加入。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `131:206`：

> early_stopping(index=epoch; avg_valid_loss). (TODO: coming in next release)

<a id="row-62"></a>
## 62. 23shades-0062-aagachfba

**主题代码：** SATD-C

**开放代码：** 重复项检查缺失

**逐条判断：** 应检查 variation 是否已存在。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `138:200`：

> else:  # TODO check that the variation wasn't already in there

<a id="row-63"></a>
## 63. 23shades-0063-aaaedhbbd

**主题代码：** SATD-C

**开放代码：** 输入类型契约待保证

**逐条判断：** 需保证传给 _pool.step 的是 ndarray。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `126:180`：

> Ensure we're really passing an ndarray to _pool.step()

<a id="row-64"></a>
## 64. 23shades-0064-aaiicfgag

**主题代码：** SATD-J, SATD-Q

**开放代码：** 输入预处理使用待定

**逐条判断：** ScaledFloatFrame 是否用于 DQN 尚待决定。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `132:181`：

> env = ScaledFloatFrame(env)  # TODO: use for dqn?

<a id="row-65"></a>
## 65. 23shades-0065-aagfjefaf

**主题代码：** SATD-L

**开放代码：** 张量尺寸操作缺文档

**逐条判断：** 需把层输出尺寸用于 concat 后 resize 的做法写入文档；不是该操作缺失。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `131:224`：

> Extract the output size of the layer to fit resize after the concatenation TODO put it in doc

<a id="row-66"></a>
## 66. 23shades-0066-aahhdbjej

**主题代码：** SATD-L, SATD-Q

**开放代码：** 前缀必要性不明

**逐条判断：** 需要解释 neg_ 前缀的原因。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `136:170`：

> find out why prefix neg_ is needed

<a id="row-67"></a>
## 67. 23shades-0067-aagbghgdd

**主题代码：** SATD-F, SATD-U

**开放代码：** 仅外部问题引用

**逐条判断：** 只有 tensorflow#3388；未读取该外链，不能恢复问题类型。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `128:148`：

> FIX: tensorflow#3388

<a id="row-68"></a>
## 68. 23shades-0068-aaagiadgf

**主题代码：** SATD-E

**开放代码：** 语言词表覆盖不足

**逐条判断：** 需扩展允许的固定复合表达列表。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `126:204`：

> fixed expressions like \"aujourd'hui\". TODO! extend list of allowed compounds

<a id="row-69"></a>
## 69. 23shades-0069-aafdeebba

**主题代码：** SATD-U

**开放代码：** 证据不足

**逐条判断：** 只有 FIXME。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `145:150`：

> FIXME

<a id="row-70"></a>
## 70. 23shades-0070-aahfheeac

**主题代码：** SATD-U

**开放代码：** 证据不足

**逐条判断：** 只有 FIXME。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `136:141`：

> FIXME

<a id="row-71"></a>
## 71. 23shades-0071-aafiaaaih

**主题代码：** SATD-H, SATD-I

**开放代码：** 答案位置启发式脆弱；单问题处理遗漏

**逐条判断：** adhoc 地假设答案在最后一词，同时未忽略 single question；更具体语境不明。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `121:189`：

> FIXME : adhoc (answer being last word); not ignoring single question

<a id="row-72"></a>
## 72. 23shades-0072-aaidadhdg

**主题代码：** SATD-K

**开放代码：** 测试跳过机制使用受限

**逐条判断：** 希望使用 _skip_test，但 if we could 表示约束未解决。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `134:184`：

> FIXME _skip_test should be used here (if we could)

<a id="row-73"></a>
## 73. 23shades-0073-aadfibefa

**主题代码：** SATD-H

**开放代码：** 变长形状批处理绕行

**逐条判断：** 不同 sized shapes 的 batching 依靠 hack。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `128:184`：

> FIXME annoying hack for batching different sized shapes;

<a id="row-74"></a>
## 74. 23shades-0074-aajfadgji

**主题代码：** SATD-B

**开放代码：** 指标归一化适用性问题

**逐条判断：** 警告不能对任意 metric 都 l2_normalize；应按指标选择。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `157:196`：

> FIXME don't l2_normalize for any metric

<a id="row-75"></a>
## 75. 23shades-0075-aagdagdia

**主题代码：** SATD-A, SATD-Q

**开放代码：** 调用泛化待办

**逐条判断：** generic call 信息极少，仅能确定泛化方向。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `133:151`：

> FIXME generic call

<a id="row-76"></a>
## 76. 23shades-0076-aajfajibh

**主题代码：** SATD-A

**开放代码：** 参数语义不一致

**逐条判断：** margin 参数含义需要统一。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `166:215`：

> FIXME homogeneize the meaning of margin parameter

<a id="row-77"></a>
## 77. 23shades-0077-aaicecaej

**主题代码：** SATD-E

**开放代码：** 非均匀样本权重不支持

**逐条判断：** 明确缺少 non-uniform sample weights。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `135:185`：

> FIXME non-uniform sample weights not yet supported

<a id="row-78"></a>
## 78. 23shades-0078-aaecffjjg

**主题代码：** SATD-L, SATD-Q

**开放代码：** 变量语义不明

**逐条判断：** 不清楚 CB1/CB2 的含义，属于理解缺口。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `131:171`：

> FIXME not sure what are those CB1 \/ CB2

<a id="row-79"></a>
## 79. 23shades-0079-aahhbbhjc

**主题代码：** SATD-C

**开放代码：** 并发文件访问缺保护

**逐条判断：** 需 exclusive open，防其他 Celery 线程干扰。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `122:180`：

> FIXME open exclusively; other celery thread might screw up

<a id="row-80"></a>
## 80. 23shades-0080-aaidbchej

**主题代码：** SATD-K, SATD-M

**开放代码：** 版本迁移后的测试清理

**逐条判断：** 当 0.26 默认 square_distances=True 后删除特定测试；不是普遍测试不足。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `142:214`：

> FIXME remove test when square_distances=True becomes the default in 0.26

<a id="row-81"></a>
## 81. 23shades-0081-aaaedbhaj

**主题代码：** SATD-A

**开放代码：** 控制器组织待整合

**逐条判断：** 代码意义依赖所有 controllers 放到同一文件。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `173:251`：

> FIXME This will make sense when all controllers are in one file (like task.py)

<a id="row-82"></a>
## 82. 23shades-0082-aajdcijhj

**主题代码：** SATD-A

**开放代码：** 复制实现待重写

**逐条判断：** 现有函数来自 autoresolve.py 的复制，需要重写实现。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `127:265`：

> FIXME XXX: Implement by rewriting functions above copied from autoresolve.py; search for resolve_strategy_inline_source above in this file

<a id="row-83"></a>
## 83. 23shades-0083-aadggijai

**主题代码：** SATD-H, SATD-I

**开放代码：** 内部命名约定耦合

**逐条判断：** hack 依赖 _0 convention，具脆弱性。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `142:189`：

> FIXME: A hack that depends on the _0 convention

<a id="row-84"></a>
## 84. 23shades-0084-aajdcifej

**主题代码：** SATD-D

**开放代码：** 文本差异支持扩展

**逐条判断：** 希望允许 repr 风格 text/plain 差异。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `129:191`：

> FIXME: Allow some diff; e.g. on repr style text in text\/plain

<a id="row-85"></a>
## 85. 23shades-0085-aaebbccje

**主题代码：** SATD-Q

**开放代码：** 双路径反向传播可行性待查

**逐条判断：** 询问是否能通过 both 反传 error，不能当作已确认梯度 bug。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `116:156`：

> FIXME: can I backprop error through both

<a id="row-86"></a>
## 86. 23shades-0086-aaicdjedb

**主题代码：** SATD-G

**开放代码：** 并行资源配置未利用

**逐条判断：** 指出此处也可用 n_jobs。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `133:163`：

> FIXME: can use n_jobs here too

<a id="row-87"></a>
## 87. 23shades-0087-aaiehhaec

**主题代码：** SATD-F, SATD-Q

**开放代码：** 框架算子等价性待查

**逐条判断：** 询问 PyTorch 是否有 tf.add_n 等价求和算子。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `112:188`：

> FIXME: does pytorch has something similar to tf.add_n which sum over a list?

<a id="row-88"></a>
## 88. 23shades-0088-aahedijdj

**主题代码：** SATD-O

**开放代码：** 显示内容待隐藏

**逐条判断：** don't show 的对象只有转义斜杠，展示意图可见但细节不足。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `136:156`：

> FIXME: don't show \/

<a id="row-89"></a>
## 89. 23shades-0089-aajdcehac

**主题代码：** SATD-J, SATD-N, SATD-Q

**开放代码：** 执行计数处理策略待定

**逐条判断：** execution_count 是否总设 None 尚无决定。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `132:186`：

> FIXME: Handle execution_count (always change to None?)

<a id="row-90"></a>
## 90. 23shades-0090-aaacjihab

**主题代码：** SATD-H, SATD-I, SATD-J

**开放代码：** 硬编码设计不满意

**逐条判断：** 直接指出 hardcoded 通常不好，但无具体值或影响。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `121:151`：

> FIXME: Hardcoded usually sucks

<a id="row-91"></a>
## 91. 23shades-0091-aagbejage

**主题代码：** SATD-F, SATD-Q

**开放代码：** 图像解码 API 替换待查

**逐条判断：** 希望使用通用 decode_image 替代 decode_jpeg，未说明现有失败。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `133:196`：

> FIXME: how to use tf.image.decode_image instead of decode_jpeg?

<a id="row-92"></a>
## 92. 23shades-0092-aaeeieida

**主题代码：** SATD-A

**开放代码：** 继承与持有方式待调整

**逐条判断：** 提议继承 NetCDFFile 并省略 self.nc；句子未给完整结果。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `122:195`：

> FIXME: if we inherit from scipy.io.netcdf.NetCDFFile and omit the self.nc

<a id="row-93"></a>
## 93. 23shades-0093-aaffafejc

**主题代码：** SATD-D

**开放代码：** 功能尚未实现

**逐条判断：** 明确 implement this functionality，但对象不明。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `133:168`：

> FIXME: Implement this functionality

<a id="row-94"></a>
## 94. 23shades-0094-aadaidhdg

**主题代码：** SATD-D

**开放代码：** 实现不完整

**逐条判断：** 仅 incomplete，保留一般性未完成判断。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `154:171`：

> FIXME: incomplete

<a id="row-95"></a>
## 95. 23shades-0095-aadgfjhjj

**主题代码：** SATD-U

**开放代码：** 截断证据

**逐条判断：** section_type entry is meant to contain 后缺内容，不能判断契约。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `139:192`：

> FIXME: INDRA's section_type entry is meant to contain

<a id="row-96"></a>
## 96. 23shades-0096-aaeeidbja

**主题代码：** SATD-Q

**开放代码：** 返回值行为待确认

**逐条判断：** 怀疑返回空列表，不确认是 bug。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `116:150`：

> FIXME: is returning an empty list?

<a id="row-97"></a>
## 97. 23shades-0097-aajhbhjgb

**主题代码：** SATD-A

**开放代码：** 参数解析职责位置待调整

**逐条判断：** 考虑把定义/解析移入 main。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `123:175`：

> FIXME: move args definition\/parsing inside of main?

<a id="row-98"></a>
## 98. 23shades-0098-aaffadbgf

**主题代码：** SATD-Q

**开放代码：** 数学算子语义待验证

**逐条判断：** 检查 mod 是否等价 NumPy floorMod。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `133:199`：

> FIXME: Need to check if mod is the equivalent of floorMod in NumPy

<a id="row-99"></a>
## 99. 23shades-0099-aaibjjjbc

**主题代码：** SATD-E

**开放代码：** 估计器样本权重支持缺失

**逐条判断：** Ridge 的 sample_weight 待实现。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `141:188`：

> FIXME: need to implement sample_weight in Ridge

<a id="row-100"></a>
## 100. 23shades-0100-aafidfjjc

**主题代码：** SATD-B

**开放代码：** 多标签信息被截取

**逐条判断：** 仅保留首个 label；有信息损失线索但原因未知。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `130:165`：

> FIXME: Only keeping the first label

<a id="row-101"></a>
## 101. 23shades-0101-aagfjecej

**主题代码：** SATD-B, SATD-D

**开放代码：** 目标类别映射未填充

**逐条判断：** pixel_classes 应从 target 类别建立。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `131:212`：

> FIXME: pixel_classes dict needs to be populated with classes obtained from target

<a id="row-102"></a>
## 102. 23shades-0102-aajeddgaa

**主题代码：** SATD-B

**开放代码：** 覆写返回类型违约

**逐条判断：** fit 返回 None，与父类 Model 的 float 契约冲突。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `152:253`：

> FIXME: Return type \"None\" of \"fit\" incompatible with return type \"float\" in supertype \"Model\"

<a id="row-103"></a>
## 103. 23shades-0103-aaeeiehhe

**主题代码：** SATD-I, SATD-Q

**开放代码：** 索引偏移待核实

**逐条判断：** 是否加一与首样本索引为零有关；原句截断。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `110:180`：

> FIXME: should 1 be added? the index 0 is the first sample; thus if the

<a id="row-104"></a>
## 104. 23shades-0104-aaeeigbeg

**主题代码：** SATD-I, SATD-Q

**开放代码：** 直流频段处理待定

**逐条判断：** 询问是否跳过 DC bin 0。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `119:144`：

> FIXME: skip the DC bin 0?

<a id="row-105"></a>
## 105. 23shades-0105-aafahfcgh

**主题代码：** SATD-D, SATD-E

**开放代码：** 评估器扩展缺失

**逐条判断：** 多 evaluator 支持待加，event support 仅候选。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `145:200`：

> FIXME: support for many evaluators; maybe event support

<a id="row-106"></a>
## 106. 23shades-0106-aaefdgjbi

**主题代码：** SATD-V

**开放代码：** 适用对象说明不足以判债务

**逐条判断：** 仅说代码可用于 EpisodicReplayBuffer，未指出其他 buffer 不支持。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `134:181`：

> FIXME: The code works with EpisodicReplayBuffer

<a id="row-107"></a>
## 107. 23shades-0107-aaeejjfbc

**主题代码：** SATD-H

**开放代码：** 临时实现但细节截断

**逐条判断：** 明确 kind of hackish，后续原因不完整。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `117:177`：

> FIXME: this is kind of hackish; but being able to simply set

<a id="row-108"></a>
## 108. 23shades-0108-aaeieagib

**主题代码：** SATD-F, SATD-H

**开放代码：** 动态库定位硬适配待泛化

**逐条判断：** 需在 Python root 找实际 so，以变得更通用。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `110:200`：

> FIXME: this needs to become more generic; we need to find the actual so in the python root

<a id="row-109"></a>
## 109. 23shades-0109-aaibiggcj

**主题代码：** SATD-G

**开放代码：** 协方差表示不利缓存

**逐条判断：** 作者认为当前 covars representation 会损害 caching。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `126:191`：

> FIXME: this representation of covars is going to lose for caching

<a id="row-110"></a>
## 110. 23shades-0110-aaidajbdi

**主题代码：** SATD-M

**开放代码：** 版本性废弃清理

**逐条判断：** 0.25 计划删除。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `139:167`：

> FIXME: to be removed in 0.25

<a id="row-111"></a>
## 111. 23shades-0111-aajdcgacj

**主题代码：** SATD-N

**开放代码：** 输出比较粒度待改进

**逐条判断：** 部分输出拟采用 linebased diff。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `129:180`：

> FIXME: Use linebased diff of some types of outputs:

<a id="row-112"></a>
## 112. 23shades-0112-aafafebib

**主题代码：** SATD-G

**开放代码：** 数组移位实现性能候选

**逐条判断：** numpy.roll 加随机 shift 可能更快，未给测量证据。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `127:186`：

> FIXME: using numpy.roll with a random shift might be faster

<a id="row-113"></a>
## 113. 23shades-0113-aajdcgebb

**主题代码：** SATD-Q

**开放代码：** 差异序列后续条目遗漏疑问

**逐条判断：** 询问 next diff entry 的处理。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `127:165`：

> FIXME: What about the next diff entry?

<a id="row-114"></a>
## 114. 23shades-0114-aafeaaejc

**主题代码：** SATD-C, SATD-Q

**开放代码：** 搜索未命中边界未决

**逐条判断：** 如果永远找不到 fail-high 如何处理。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `116:157`：

> FIXME: What if we never find a fail-high?

<a id="row-115"></a>
## 115. 23shades-0115-aaeejbdgh

**主题代码：** SATD-N, SATD-Q

**开放代码：** 输出格式语义待核实

**逐条判断：** 实际像写 MIDI format 0，未给明确预期差异。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `113:177`：

> FIXME: what we do here s basically writing a MIDI format 0 file;

<a id="row-116"></a>
## 116. 23shades-0116-aafcbidge

**主题代码：** SATD-Q

**开放代码：** 重复调用原因不明

**逐条判断：** 每次 register.tag 会调用两次；未证实性能/正确性后果。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `151:240`：

> fixme: Why is this function called twice for each @register.tag call in template_tags.py?

<a id="row-117"></a>
## 117. 23shades-0117-aajcgbifg

**主题代码：** SATD-U

**开放代码：** 比较分支未处理

**逐条判断：** 仅标记 > case，具体边界上下文不足。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `130:146`：

> FIXME:the > case

<a id="row-118"></a>
## 118. 23shades-0118-aajcgbchf

**主题代码：** SATD-I

**开放代码：** 历史数据预先存在假设

**逐条判断：** 实现假设 history data 一开始就有，缺少不存在时策略。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `117:171`：

> FIXME:we suppose history data should be there at first

<a id="row-119"></a>
## 119. 23shades-0119-aaecffiac

**主题代码：** SATD-I, SATD-Q

**开放代码：** 不兼容数据的筛除策略待定

**逐条判断：** 考虑丢弃不兼容 dataset；不是版本兼容的直接证据。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `129:189`：

> fixme; we might want to drop dataset that are not compatible

<a id="row-120"></a>
## 120. 23shades-0120-aaeihdgig

**主题代码：** SATD-A, SATD-F

**开放代码：** 上游限制下的返回表示迁移

**逐条判断：** Numba#5157 关联去掉 np.asarray 并返回 list；外部原因未展开。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `137:191`：

> FIXME_Numba#5157: remove np.asarray and return as list

<a id="row-121"></a>
## 121. 23shades-0121-aadhbadhi

**主题代码：** SATD-D

**开放代码：** 缓冲区索引循环缺失

**逐条判断：** double/triple buffering 需 wrapping increment。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `159:232`：

> fixme-iui  need to use wrapping increment for double or triple buffering:

<a id="row-122"></a>
## 122. 23shades-0122-aahjceiih

**主题代码：** SATD-V

**开放代码：** 掩码收缩处理说明

**逐条判断：** 只描述必要且可行时 shrink mask，没有明确债务陈述。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `134:186`：

> Force shrinking of the mask if needed (and possible)

<a id="row-123"></a>
## 123. 23shades-0123-aagfeiiaj

**主题代码：** SATD-D

**开放代码：** 权重冻结功能缺失

**逐条判断：** 明确 NOT IMPLEMENTED。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `141:180`：

> Freeze weights - TODO: NOT IMPLEMENTED!

<a id="row-124"></a>
## 124. 23shades-0124-aafacjjjb

**主题代码：** SATD-U

**开放代码：** 未定位的层实现待办

**逐条判断：** dense 配置后只有 #4 TODO，不能推断该层或激活错误。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `137:227`：

> h = tf.layers.dense(h; self.hidden_size * 2; activation=tf.nn.relu; use_bias=True) #4 TODO

<a id="row-125"></a>
## 125. 23shades-0125-aaahbjjic

**主题代码：** SATD-E, SATD-H

**开放代码：** 输入通道裁剪绕行

**逐条判断：** 更多 channels 时采用 hack 拉取部分输入；句子截断，信息丢失范围不明。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `128:188`：

> hack; when inputs have more channels try pulling in only the

<a id="row-126"></a>
## 126. 23shades-0126-aaeiedjia

**主题代码：** SATD-E

**开放代码：** 输入容器支持范围待扩展

**逐条判断：** 已支持 BoxedSeries 与其 list/set，其他类型待办。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `112:174`：

> handle BoxedSeries and list\/set of BoxedSeries; TODO: others?

<a id="row-127"></a>
## 127. 23shades-0127-aafhjffeb

**主题代码：** SATD-U

**开放代码：** 未定位的模块待办

**逐条判断：** HTTP Utilities 标题附 TODO，不能确定缺失功能。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `119:197`：

> HTTP Utilities and MISC (TODO) ###############################################

<a id="row-128"></a>
## 128. 23shades-0128-aaeccdahj

**主题代码：** SATD-U

**开放代码：** 必要性未说明

**逐条判断：** 只有 if this is needed，缺少指代。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `179:197`：

> if this is needed.

<a id="row-129"></a>
## 129. 23shades-0129-aahfhegdd

**主题代码：** SATD-G, SATD-V

**开放代码：** 矩阵布局影响性能

**逐条判断：** 明确布局不合适导致八倍性能下降，是记录的性能约束，不等同尚未实施。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `134:244`：

> IMPORTANT: keep matrices in suitable order for matrix products; failing to do so gives 8x lower performance :(

<a id="row-130"></a>
## 130. 23shades-0130-aaijaggcb

**主题代码：** SATD-F, SATD-V

**开放代码：** 语言版本适配说明

**逐条判断：** Python 3 的 range 需 list 转换；没有明确未完成适配。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `148:243`：

> In Python 3; the `list` call is needed to convert the iterator returned by `range` into a list.

<a id="row-131"></a>
## 131. 23shades-0131-aaffecjha

**主题代码：** SATD-B, SATD-E

**开放代码：** 输入维度泛化缺陷

**逐条判断：** 随机 in_dim 时需要修复，当前 tuple 仅示例。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `135:201`：

> in_dim=(4; 8; 8; 8); # TODO: Needs fix when giving a randon in_dim

<a id="row-132"></a>
## 132. 23shades-0132-aaeiefagi

**主题代码：** SATD-A

**开放代码：** 索引类型表示待替换

**逐条判断：** 当前 Array type，拟转 Index object。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `129:166`：

> index is Array type (TODO: Index obj)

<a id="row-133"></a>
## 133. 23shades-0133-aaggcfjif

**主题代码：** SATD-Q

**开放代码：** 模型初始化必要性待决策

**逐条判断：** 作者询问初始化是否必要。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `137:184`：

> Initialize model (TODO: do i really need this?)

<a id="row-134"></a>
## 134. 23shades-0134-aaggcgaie

**主题代码：** SATD-Q

**开放代码：** 模型初始化必要性待决策

**逐条判断：** 相似注释保留独立记录。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `139:181`：

> Initialize model (TODO: really necessary?)

<a id="row-135"></a>
## 135. 23shades-0135-aahfgjaff

**主题代码：** SATD-H, SATD-M

**开放代码：** 短期用途实现待移除

**逐条判断：** 明确短期用途，将来会去掉。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `138:205`：

> It's only needed for a specific purpose in the short term; will go.

<a id="row-136"></a>
## 136. 23shades-0136-aahhfejii

**主题代码：** SATD-H

**开放代码：** 核传播实现绕行

**逐条判断：** 以带自定义传播矩阵的 subkernel 作 workaround，根因不明。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `124:199`：

> kernel as subkernel with a custom propagation matrix. This is a workaround!

<a id="row-137"></a>
## 137. 23shades-0137-aahjacacc

**主题代码：** SATD-H, SATD-I, SATD-Q

**开放代码：** 临时方案正确性存疑

**逐条判断：** KLUDGE 并询问是否总成立。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `116:142`：

> KLUDGE: Is this always OK?

<a id="row-138"></a>
## 138. 23shades-0138-aagdbgcgg

**主题代码：** SATD-Q

**开放代码：** 返回目标需求待定

**逐条判断：** 考虑不返回 target，未确定接口契约。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `148:175`：

> Maybe return without target

<a id="row-139"></a>
## 139. 23shades-0139-aaiiihajd

**主题代码：** SATD-U

**开放代码：** 未定位的后端映射待办

**逐条判断：** nasnet-a_large 的三个 emitter 后 TODO，无法判断缺哪个后端或是否映射错误。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `129:196`：

> 'nasnet-a_large' : [TensorflowEmit; KerasEmit; PytorchEmit]; # TODO

<a id="row-140"></a>
## 140. 23shades-0140-aaiijdebd

**主题代码：** SATD-D

**开放代码：** 形状信息待补

**逐条判断：** 需要 shape，缺少对象但明确尺寸信息不足。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `136:155`：

> need the shape TODO

<a id="row-141"></a>
## 141. 23shades-0141-aadbcebbh

**主题代码：** SATD-F, SATD-H

**开放代码：** 上游缺陷补偿

**逐条判断：** glob2 疑似 bug 导致 duplicate entries 被移除，额外逻辑因此需要。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `152:215`：

> needed due to apparent bug in glob2 - removes duplicate entries

<a id="row-142"></a>
## 142. 23shades-0142-aaeeiicii

**主题代码：** SATD-V

**开放代码：** 事件处理必要性说明

**逐条判断：** 只说明正确 SysEx 处理需要该逻辑，无明确欠缺。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `113:152`：

> needed for correct SysEx event handling

<a id="row-143"></a>
## 143. 23shades-0143-aahfjhgbi

**主题代码：** SATD-V

**开放代码：** 测试夹具必要性说明

**逐条判断：** TestWikiCorpus 为测试所需，不代表缺测试。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `132:197`：

> Needed for the test_custom_tokenizer is the TestWikiCorpus class.

<a id="row-144"></a>
## 144. 23shades-0144-aajhbagib

**主题代码：** SATD-V

**开放代码：** 命令帮助必要性说明

**逐条判断：** 逻辑用于 completion/help，未提出待完成工作。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `154:202`：

> needed so command completion and help can use it

<a id="row-145"></a>
## 145. 23shades-0145-aahjiddhj

**主题代码：** SATD-V

**开放代码：** 类型检查必要性说明

**逐条判断：** 为通过 ResourceVariable checks 所需，未给未解决缺陷。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `156:195`：

> Needed to pass ResourceVariable checks.

<a id="row-146"></a>
## 146. 23shades-0146-aafedbhaj

**主题代码：** SATD-F, SATD-V

**开放代码：** 兼容约束说明

**逐条判断：** 为 sklearn comparability 所需，未明确需要改动。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `114:145`：

> needed to sklearn comparability

<a id="row-147"></a>
## 147. 23shades-0147-aafedbhaj

**主题代码：** SATD-F, SATD-V

**开放代码：** 兼容约束说明

**逐条判断：** 重复文本独立保留。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `114:145`：

> needed to sklearn comparability

<a id="row-148"></a>
## 148. 23shades-0148-aaeigcigi

**主题代码：** SATD-Q, SATD-U

**开放代码：** 必要性待决策

**逐条判断：** 询问 needed，无具体对象。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `129:136`：

> needed?

<a id="row-149"></a>
## 149. 23shades-0149-aajbfcgda

**主题代码：** SATD-U

**开放代码：** 未定位的损失函数待办

**逐条判断：** normed_cross_entropy 后 TODO，无具体缺陷说明。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `135:162`：

> normed_cross_entropy # TODO

<a id="row-150"></a>
## 150. 23shades-0150-aahfhedig

**主题代码：** SATD-M, SATD-Q, SATD-V

**开放代码：** 冗余逻辑保留态度

**逐条判断：** 作者认为不需要但保留；没有明确删除决定。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `140:166`：

> not needed; but why not...

<a id="row-151"></a>
## 151. 23shades-0151-aafjajfdh

**主题代码：** SATD-G

**开放代码：** 排序与步进顺序性能候选

**逐条判断：** sort 后按 nt_regions stride 可能更高效，未验证。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `161:224`：

> NOTE: probably more efficient to sort then stride by nt_regions

<a id="row-152"></a>
## 152. 23shades-0152-aafadbdeg

**主题代码：** SATD-G

**开放代码：** 稀疏表示性能候选

**逐条判断：** 矩阵乘积考虑改 CSC 提速，保留提议性质。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `126:191`：

> nv by ns dot ns by m -> nv by m  # TODO: Change to CSC for speed?

<a id="row-153"></a>
## 153. 23shades-0153-aajacaegh

**主题代码：** SATD-M, SATD-U

**开放代码：** 截断证据

**逐条判断：** once no longer needed 的从句不足以判断删除对象或条件。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `139:191`：

> once they are no longer needed in the schedule or by

<a id="row-154"></a>
## 154. 23shades-0154-aajdcgijh

**主题代码：** SATD-A, SATD-N

**开放代码：** 差异元数据存储位置待调整

**逐条判断：** 考虑放 global metadata 而非独立 diff dicts。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `129:237`：

> Pass on diff to external difftool (TODO: store in global metadata at end instead of in separate diff dicts?)

<a id="row-155"></a>
## 155. 23shades-0155-aafibegdj

**主题代码：** SATD-M, SATD-Q

**开放代码：** 过渡代码疑似冗余

**逐条判断：** probably not needed，仍未确认。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `146:177`：

> probably not needed; transition

<a id="row-156"></a>
## 156. 23shades-0156-aagiedbjj

**主题代码：** SATD-G

**开放代码：** 批次重复初始化开销

**逐条判断：** 全文描述推理流水线；每 batch 建 inferer 造成开销，建议 MapFlat 改 ParDo 在 start_bundle 初始化；现有十亿次/50分钟的运行速率被作者认为暂够用。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `159:1934`：

> r\"\"\"Run inference on random sequences many times; saving the top results. ||  || This module is designed to run inference on a trained aptamers TF model || to score many sequences and then write out the top scoring sequences to || be used in other analysis. For example; these top predicted sequences || can read in the colab picking sequences in order || to validate the TF model. ||  || This module uses the standard aptamers tensorflow infrastructure to run || the inference. This is the inferer class defined in || learning\/eval_feedforward and described in the Aptamers TensorFlow Doc. ||  || Inference is generally run in batches of sequences; so a MapFlat function || is used to combine the results of interference into a flattened list || of (sequence; score) pairs. (In other words; each map function returns || a list of (sequence; score) pairs and these results are combined into || one list of pairs. Using a standard Map function would result in a || list of lists which is not what we want.) From there; the Top.Of || combiner returns only the top results; sorted by highest score. These || are then written to a text file. ||  || For now; each batch creates its own inferer; causing each map function || to have more overhead. Because of this;batch sizes around the default of || 10000 are performant. Fixing this in the future means converting the || MapFlat to a ParDo and initializing the inferer in start_bundle. || This module runs inference 1 billion times in 50 minutes so it || is sufficient for now ||  || Run locally with: ||  ||   :search_inference -- --flume_exec_mode=UNOPT \\ ||   --target_name='target' \\ ||   --model_dir=xxx \\ ||    --checkpoint_path='model.ckpt-312500' \\ ||    --output_name=xxx\/base30_1B_inference_top2k ||  || \"\"\"

<a id="row-157"></a>
## 157. 23shades-0157-aafejhiea

**主题代码：** SATD-D

**开放代码：** 训练变换输入目标掩码不完整

**逐条判断：** Random Warp 拟同时使用 input mask 与 warped target mask。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `126:203`：

> Random Warp # TODO change masks to have a input mask and a warped target mask

<a id="row-158"></a>
## 158. 23shades-0158-aahgacfhf

**主题代码：** SATD-A, SATD-Q

**开放代码：** 实现位置或质量存疑

**逐条判断：** out of place 与可改进表述存在，未说明对象，不推断具体重构。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `148:221`：

> seem out of place. If you were able to do better; feel free to share your

<a id="row-159"></a>
## 159. 23shades-0159-aajbiahbe

**主题代码：** SATD-D

**开放代码：** 音频组件启用待办

**逐条判断：** AudioComponent 创建处要求 turn on。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `130:185`：

> self._audio = audio.AudioComponent(self) # TODO turn on

<a id="row-160"></a>
## 160. 23shades-0160-aajbibibf

**主题代码：** SATD-L, SATD-Q

**开放代码：** 输入处理职责不清

**逐条判断：** view_controller.update 与键盘输入关系仅作者猜测，保持理解缺口。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `131:242`：

> self._view_controller.update(self.robot) # TODO: <- sounds like this has something to do with keyboard input...

<a id="row-161"></a>
## 161. 23shades-0161-aagcbdejg

**主题代码：** SATD-M, SATD-Q

**开放代码：** 清理调用必要性待定

**逐条判断：** clearChanges 是否需要调用仅是疑问。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `154:188`：

> self.clearChanges() #TODO perhaps?

<a id="row-162"></a>
## 162. 23shades-0162-aaifgcjei

**主题代码：** SATD-B

**开放代码：** 负数边界处理不完整

**逐条判断：** mpc_sum 的负数输入需要更平稳的处理。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `115:192`：

> self.mpc_sum(3; -5) TODO: Future work: how to handle gracefully minus numbers

<a id="row-163"></a>
## 163. 23shades-0163-aafbdjhfg

**主题代码：** SATD-A

**开放代码：** 归一化组件待替换

**逐条判断：** 认为应使用 WeightNorm，无进一步解释。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `120:151`：

> should be WeightNorm here TODO.

<a id="row-164"></a>
## 164. 23shades-0164-aajgcjgad

**主题代码：** SATD-K

**开放代码：** 计算测试缺失

**逐条判断：** covariance calculation 的测试待添加。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `147:187`：

> Test covariance calculation XXX add this

<a id="row-165"></a>
## 165. 23shades-0165-aajaicjbh

**主题代码：** SATD-H

**开放代码：** 类型区分采用临时启发式

**逐条判断：** categorical/binary 区分是 hack；Test 此处是判别，不一定指单元测试。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `141:198`：

> Test for categorical vs. binary in hack-ey way for now...

<a id="row-166"></a>
## 166. 23shades-0166-aahcgjcji

**主题代码：** SATD-F

**开放代码：** 优化器跨框架支持缺口

**逐条判断：** tf.keras.optimizers 似乎不支持 ProximalAdagradOptimizer。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `149:232`：

> tf.train.ProximalAdagradOptimizer todo appears tf.keras.optimizers does not support

<a id="row-167"></a>
## 167. 23shades-0167-aagiehhgb

**主题代码：** SATD-F, SATD-H

**开放代码：** 外部库缺陷绕行

**逐条判断：** dropna 用来绕过 pandas issue，未取得外链详情。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `145:229`：

> The dropna() is a workaround for https:\/\/github.com\/pydata\/pandas\/issues\/13098

<a id="row-168"></a>
## 168. 23shades-0168-aafdifcji

**主题代码：** SATD-V

**开放代码：** 层组织约束说明

**逐条判断：** identity layer 使后续 lambda layers 可选；未声明需要修改。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `129:226`：

> The following identity layer is only needed so that subsequent two lambda layers can be optional.

<a id="row-169"></a>
## 169. 23shades-0169-aafbjfcfe

**主题代码：** SATD-V

**开放代码：** 张量维度转换说明

**逐条判断：** squeeze 用于取得一维张量，不等于未完成债务。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `113:156`：

> the squeeze is needed to obtain a 1D tensor

<a id="row-170"></a>
## 170. 23shades-0170-aaigfaibj

**主题代码：** SATD-B, SATD-E, SATD-H

**开放代码：** 绕行方案限制反向传播

**逐条判断：** 明确 workaround 不支持 backprop，另有 external 需求但句子截断。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `129:197`：

> The workaround does not support backprop; and also requires external

<a id="row-171"></a>
## 171. 23shades-0171-aahfefcag

**主题代码：** SATD-V

**开放代码：** 类型转换保护说明

**逐条判断：** if 为 cast 提供保护；batch norm 原因未完整呈现。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `142:207`：

> This if statement is needed to guard the cast; because batch norm

<a id="row-172"></a>
## 172. 23shades-0172-aaahfegjh

**主题代码：** SATD-F, SATD-V

**开放代码：** 集群执行环境适配说明

**逐条判断：** 导入 matplotlib 是集群运行需要，未声明欠缺。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `129:189`：

> this importing of matplotlib is needed to run on the cluster

<a id="row-173"></a>
## 173. 23shades-0173-aabdgggib

**主题代码：** SATD-H

**开放代码：** 推理过程临时绕行

**逐条判断：** 涉及 go token 的 inference hack；条件截断。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `165:219`：

> This is a hack to allows inference when the <go> token

<a id="row-174"></a>
## 174. 23shades-0174-aafbhcbbi

**主题代码：** SATD-A, SATD-J

**开放代码：** 指标标识魔数待替换

**逐条判断：** 0/4/5 映射 metric 难维护，作者明确计划枚举类。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `130:269`：

> THIS IS A VERY UGLY FUNCTION because it has hardcoded 0\/4\/5 integers for each of the metric. I need to make an enumerated class for this!

<a id="row-175"></a>
## 175. 23shades-0175-aafecgahb

**主题代码：** SATD-L, SATD-Q, SATD-U

**开放代码：** 变体适配说明不完整

**逐条判断：** pre-activation variant 缺 batch 的句子截断，不能确定缺的是 batch normalization。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `146:215`：

> This is needed because the pre-activation variant does not have batch

<a id="row-176"></a>
## 176. 23shades-0176-aadhfdfce

**主题代码：** SATD-V

**开放代码：** 损失历史更新说明

**逐条判断：** 仅说明逻辑用途，无未完成主张。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `118:155`：

> this is needed to update loss history

<a id="row-177"></a>
## 177. 23shades-0177-aahgdgida

**主题代码：** SATD-A, SATD-H

**开放代码：** 最低可用补丁可维护性差

**逐条判断：** 作者明确 messy，但已是 Issue 639 的 minimal working fix。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `113:180`：

> This is very messy; but it's the minimal working fix to Issue #639.

<a id="row-178"></a>
## 178. 23shades-0178-aaifggehf

**主题代码：** SATD-G

**开放代码：** 执行优化待办

**逐条判断：** 明确要求 optimize，但未给瓶颈机制。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `133:181`：

> time to fix. TODO: optimize the crap out of this

<a id="row-179"></a>
## 179. 23shades-0179-aafehjdhc

**主题代码：** SATD-U

**开放代码：** 证据不足

**逐条判断：** 只有 TODO。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `130:134`：

> TODO

<a id="row-180"></a>
## 180. 23shades-0180-aahddifgi

**主题代码：** SATD-U

**开放代码：** 证据不足

**逐条判断：** 只有 TODO。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `128:132`：

> TODO

<a id="row-181"></a>
## 181. 23shades-0181-aaggbcefi

**主题代码：** SATD-U

**开放代码：** 证据不足

**逐条判断：** 只有 TODO。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `121:125`：

> TODO

<a id="row-182"></a>
## 182. 23shades-0182-aafhddaff

**主题代码：** SATD-U

**开放代码：** 证据不足

**逐条判断：** 只有 TODO。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `125:129`：

> TODO

<a id="row-183"></a>
## 183. 23shades-0183-aagabbjac

**主题代码：** SATD-U

**开放代码：** 证据不足

**逐条判断：** 只有 TODO。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `138:142`：

> TODO

<a id="row-184"></a>
## 184. 23shades-0184-aagbcgbed

**主题代码：** SATD-U

**开放代码：** 证据不足

**逐条判断：** 只有 TODO。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `118:122`：

> TODO

<a id="row-185"></a>
## 185. 23shades-0185-aadbfigaf

**主题代码：** SATD-U

**开放代码：** 证据不足

**逐条判断：** 只有 TODO。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `158:162`：

> TODO

<a id="row-186"></a>
## 186. 23shades-0186-aafacidaf

**主题代码：** SATD-U

**开放代码：** 证据不足

**逐条判断：** 只有 TODO。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `117:121`：

> TODO

<a id="row-187"></a>
## 187. 23shades-0187-aadfababd

**主题代码：** SATD-U

**开放代码：** 证据不足

**逐条判断：** 只有 TODO。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `176:180`：

> TODO

<a id="row-188"></a>
## 188. 23shades-0188-aadgjgddc

**主题代码：** SATD-U

**开放代码：** 证据不足

**逐条判断：** 只有 TODO。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `147:151`：

> TODO

<a id="row-189"></a>
## 189. 23shades-0189-aaggiaccc

**主题代码：** SATD-U

**开放代码：** 证据不足

**逐条判断：** 只有 TODO。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `176:180`：

> TODO

<a id="row-190"></a>
## 190. 23shades-0190-aabdibfbd

**主题代码：** SATD-U

**开放代码：** 证据不足

**逐条判断：** 只有 TODO。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `133:137`：

> TODO

<a id="row-191"></a>
## 191. 23shades-0191-aafijfbah

**主题代码：** SATD-U

**开放代码：** 证据不足

**逐条判断：** 只有 TODO。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `160:164`：

> TODO

<a id="row-192"></a>
## 192. 23shades-0192-aahdfcffj

**主题代码：** SATD-U

**开放代码：** 证据不足

**逐条判断：** 只有 todo。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `146:150`：

> todo

<a id="row-193"></a>
## 193. 23shades-0193-aajfaiafb

**主题代码：** SATD-U

**开放代码：** 证据不足

**逐条判断：** 只有 TODO。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `140:144`：

> TODO

<a id="row-194"></a>
## 194. 23shades-0194-aagfeabcg

**主题代码：** SATD-U

**开放代码：** 证据不足

**逐条判断：** 只有 TODO。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `127:131`：

> TODO

<a id="row-195"></a>
## 195. 23shades-0195-aaibgjfcg

**主题代码：** SATD-U

**开放代码：** 证据不足

**逐条判断：** 只有 TODO。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `122:126`：

> TODO

<a id="row-196"></a>
## 196. 23shades-0196-aaahgjjag

**主题代码：** SATD-U

**开放代码：** 证据不足

**逐条判断：** 只有 TODO。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `150:154`：

> TODO

<a id="row-197"></a>
## 197. 23shades-0197-aadbceejg

**主题代码：** SATD-A

**开放代码：** 类集合表示待改进

**逐条判断：** 建议 class list 消除某项需求，但具体被替代对象截断。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `153:226`：

> TODO - a list of classes would be better eliminating the need for the one

<a id="row-198"></a>
## 198. 23shades-0198-aajeiegcd

**主题代码：** SATD-A, SATD-Q

**开放代码：** 展平方案替代待探索

**逐条判断：** 想探索 flattening 的替代方式，方案未完整提供。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `151:220`：

> TODO - as an alternative to the above flattening approach; explore an

<a id="row-199"></a>
## 199. 23shades-0199-aadhaadga

**主题代码：** SATD-I, SATD-M, SATD-Q

**开放代码：** 条件性冗余恢复操作

**逐条判断：** A/B 都 TLU 时可移除一个 m0 restore。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `147:209`：

> TODO - can remove one of these m0 restores if A and B both TLU

<a id="row-200"></a>
## 200. 23shades-0200-aadhaidcc

**主题代码：** SATD-C, SATD-E, SATD-I, SATD-K, SATD-Q

**开放代码：** 高维输入正确性未验证

**逐条判断：** 询问 N-dim tensor 是否正确处理。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `161:209`：

> TODO - does this handle N-dim tensors correctly?

<a id="row-201"></a>
## 201. 23shades-0201-aaffefhhb

**主题代码：** SATD-B, SATD-Q

**开放代码：** 实现与预期不一致待解释

**逐条判断：** 发现 code different，未说明比较基准。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `126:167`：

> TODO - in the code it is different - why?

<a id="row-202"></a>
## 202. 23shades-0202-aafdacejd

**主题代码：** SATD-O

**开放代码：** 可视化边界待平滑

**逐条判断：** 要求 smoother visualization bounds。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `170:225`：

> TODO -- instead; smoother visualization bounds (at MAG)

<a id="row-203"></a>
## 203. 23shades-0203-aahibhdeh

**主题代码：** SATD-A

**开放代码：** 函数参数契约重构

**逐条判断：** 明确引入 model_name/instance/parent 改善函数设计。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `155:246`：

> TODO - refector this function to accept model_name; instance; parent so it makes more sense

<a id="row-204"></a>
## 204. 23shades-0204-aadhadibe

**主题代码：** SATD-G, SATD-K

**开放代码：** 性能测量偏差

**逐条判断：** beta kernels 的 timing 因仅 GSU path 独立 event 偏悲观；是测量问题非已证实运行慢。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `141:251`：

> TODO - timing with beta kernels is somewhat pessimistic since it has this separate event only on the GSU path.

<a id="row-205"></a>
## 205. 23shades-0205-aaiibgbdc

**主题代码：** SATD-C

**开放代码：** 并发竞态

**逐条判断：** 明确 race condition，worker 条件截断。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `123:182`：

> TODO (Alex): There's a race condition here if the worker is

<a id="row-206"></a>
## 206. 23shades-0206-aaegahgbf

**主题代码：** SATD-D, SATD-E

**开放代码：** 分布式优化支持待处理

**逐条判断：** 缺少更具体机制，不混同普通代码性能优化。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `139:193`：

> todo (g-votte): Take care of distributed optimization.

<a id="row-207"></a>
## 207. 23shades-0207-aaggfbief

**主题代码：** SATD-K

**开放代码：** 文件格式测试缺失

**逐条判断：** 需用 binary format file 写测试。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `132:189`：

> TODO (johngiorgi): write tests using a binary format file

<a id="row-208"></a>
## 208. 23shades-0208-aaeeciehh

**主题代码：** SATD-K

**开放代码：** 特征提取行为测试缺失

**逐条判断：** 明确要求测试 feature extraction。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `175:225`：

> TODO (nakago): test feature extraction behavior...

<a id="row-209"></a>
## 209. 23shades-0209-aaihfgcij

**主题代码：** SATD-A

**开放代码：** 索引交集算法待调整

**逐条判断：** 计划排序 indices 再按序交集，返回结果目的截断。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `137:226`：

> TODO (pradeep): Sort the indices and do intersections in order; so that we can return the

<a id="row-210"></a>
## 210. 23shades-0210-aaefhhbid

**主题代码：** SATD-M

**开放代码：** 下一大版本清理

**逐条判断：** 明确随 major version bump 删除。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `118:170`：

> TODO (tdomhan): Remove with next major version bump.

<a id="row-211"></a>
## 211. 23shades-0211-aajeacdfg

**主题代码：** SATD-E, SATD-I, SATD-Q

**开放代码：** 场景覆盖约束待满足

**逐条判断：** 两个场景都至少需 active/inactive，未说明对象，不推断为测试集。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `143:222`：

> TODO (ytz): really; we want at least one active and inactive in both scenarios.

<a id="row-212"></a>
## 212. 23shades-0212-aahhiefcg

**主题代码：** SATD-D, SATD-E, SATD-J

**开放代码：** 分类选项未暴露

**逐条判断：** 五类别需加入 options。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `113:157`：

> TODO : 5 categories. to be added in options.

<a id="row-213"></a>
## 213. 23shades-0213-aahhiidji

**主题代码：** SATD-D, SATD-E, SATD-J

**开放代码：** 无界选项语义待加入

**逐条判断：** None/None 表示 no limit，应放到选项。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `134:191`：

> TODO : add these in the options. (None; None) => no limit

<a id="row-214"></a>
## 214. 23shades-0214-aafhjjgee

**主题代码：** SATD-D, SATD-E, SATD-J, SATD-Q

**开放代码：** 选项范围待扩展

**逐条判断：** 询问 other options，具体选项未列出。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `123:147`：

> TODO : Any other options

<a id="row-215"></a>
## 215. 23shades-0215-aafjbabdi

**主题代码：** SATD-L

**开放代码：** 文档与示例缺失

**逐条判断：** 同时明确 docs 和 example。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `171:194`：

> TODO : docs and example

<a id="row-216"></a>
## 216. 23shades-0216-aaebcicac

**主题代码：** SATD-L

**开放代码：** 文档缺失

**逐条判断：** documentation 待办。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `121:141`：

> TODO : documentation

<a id="row-217"></a>
## 217. 23shades-0217-aaidehfjf

**主题代码：** SATD-A, SATD-B, SATD-D

**开放代码：** 真值变换遗漏；键组织待重构

**逐条判断：** gt maps 当前未变换，拟改 dict keys；这是明确缺失行为。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `125:198`：

> TODO : gt maps are not currently transformed! (need refact w\/ dict keys)

<a id="row-218"></a>
## 218. 23shades-0218-aajbfefjj

**主题代码：** SATD-U

**开放代码：** 证据不足

**逐条判断：** market value 未表达具体操作。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `144:163`：

> TODO : market value

<a id="row-219"></a>
## 219. 23shades-0219-aaeefiahb

**主题代码：** SATD-C

**开放代码：** 不支持属性的异常处理缺失

**逐条判断：** nominal attribute 时应 raise error。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `166:206`：

> Todo : raise error for nominal attribute

<a id="row-220"></a>
## 220. 23shades-0220-aadcagfcc

**主题代码：** SATD-M

**开放代码：** 清理待办

**逐条判断：** 明确 removal，未知对象。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `123:137`：

> TODO : removal

<a id="row-221"></a>
## 221. 23shades-0221-aagabbida

**主题代码：** SATD-G

**开放代码：** 执行速度不足

**逐条判断：** 作者明确认为运行速度差，需修复。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `134:207`：

> TODO : this is quite bad in term of execution speed. We need to fix this.

<a id="row-222"></a>
## 222. 23shades-0222-aahdficjf

**主题代码：** SATD-A, SATD-Q

**开放代码：** 变量来源替换

**逐条判断：** 拟使用 realtime var，动机和对象不明。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `129:152`：

> TODO : use realtime var

<a id="row-223"></a>
## 223. 23shades-0223-aadbceeib

**主题代码：** SATD-G

**开放代码：** 处理过程并行化待办

**逐条判断：** block/line processing 拟线程化或并行。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `153:205`：

> TODO 2- thread or parallelise block\/line processing

<a id="row-224"></a>
## 224. 23shades-0224-aadajefje

**主题代码：** SATD-E, SATD-J

**开放代码：** 稀疏格式接收选项待设

**逐条判断：** 拟设置 accept_sparse=csc，未说明其他格式行为。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `119:145`：

> TODO accept_sparse=\"csc\"

<a id="row-225"></a>
## 225. 23shades-0225-aaidcjdhd

**主题代码：** SATD-D

**开放代码：** 工作流操作缺失

**逐条判断：** new pipeline action 待添加。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `137:169`：

> TODO add \"new pipeline\" action

<a id="row-226"></a>
## 226. 23shades-0226-aafdjfjab

**主题代码：** SATD-D

**开放代码：** 模型偏置项缺失

**逐条判断：** 明确 add bias term。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `125:143`：

> TODO add bias term

<a id="row-227"></a>
## 227. 23shades-0227-aagfchifa

**主题代码：** SATD-C

**开放代码：** 跨文件数据一致性检查缺失

**逐条判断：** h5 key 数必须与 csv 行数一致。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `163:255`：

> TODO add checking to make sure number of keys in h5 file matches number of lines in csv file

<a id="row-228"></a>
## 228. 23shades-0228-aaebjjhbc

**主题代码：** SATD-L

**开放代码：** 文档字符串缺失

**逐条判断：** add docstrings。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `148:167`：

> TODO add docstrings

<a id="row-229"></a>
## 229. 23shades-0229-aadfjchjf

**主题代码：** SATD-D, SATD-E

**开放代码：** 分布抽象功能待扩展

**逐条判断：** 拟加 general Distribution；不推断具体概率分布。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `131:160`：

> TODO add general Distribution

<a id="row-230"></a>
## 230. 23shades-0230-aahjecdhj

**主题代码：** SATD-D, SATD-N

**开放代码：** 输出索引信息缺失

**逐条判断：** xls 文件需添加 index。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `147:173`：

> TODO add index to xls file

<a id="row-231"></a>
## 231. 23shades-0231-aafchbajj

**主题代码：** SATD-L

**开放代码：** 介绍性解释缺失

**逐条判断：** 需 introductory explanation。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `116:149`：

> TODO add introductory explanation

<a id="row-232"></a>
## 232. 23shades-0232-aaeibhbhc

**主题代码：** SATD-C, SATD-I, SATD-J, SATD-Q

**开放代码：** 参数缺省提示策略未决

**逐条判断：** 必须提供 sent_end_chars，或告警后采用默认值，两种方案未选定。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `122:193`：

> TODO add message; must specify sent_end_chars; or warn and use defaults

<a id="row-233"></a>
## 233. 23shades-0233-aagaagfeh

**主题代码：** SATD-D, SATD-Q

**开放代码：** 探测器元信息汇集待定

**逐条判断：** 考虑加入全部 detectors meta info。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `133:171`：

> TODO add meta info from all detectors?

<a id="row-234"></a>
## 234. 23shades-0234-aahiihjjg

**主题代码：** SATD-D

**开放代码：** 工具方法缺失

**逐条判断：** net_util 方法待添加，具体行为不明。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `133:160`：

> TODO add method in net_util

<a id="row-235"></a>
## 235. 23shades-0235-aaebjiiah

**主题代码：** SATD-C

**开放代码：** 输入与目标一致性检查不足

**逐条判断：** X/y 需更多 consistency checks。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `142:195`：

> TODO add more input checks for consistency of X and y

<a id="row-236"></a>
## 236. 23shades-0236-aaejhhjgg

**主题代码：** SATD-O

**开放代码：** 日志支持不足

**逐条判断：** 要求改善日志，但具体内容未定。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `133:154`：

> TODO add nice logging

<a id="row-237"></a>
## 237. 23shades-0237-aafcgegjb

**主题代码：** SATD-D, SATD-E, SATD-Q

**开放代码：** 聚类算法范围待扩展

**逐条判断：** 其他 clustering 是候选。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `132:158`：

> todo add other clustering?

<a id="row-238"></a>
## 238. 23shades-0238-aagaggbcc

**主题代码：** SATD-J

**开放代码：** 路径参数可配置性不足

**逐条判断：** relative path 与 folder names 需要参数区分。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `122:175`：

> TODO add param for relative path vs just folder names

<a id="row-239"></a>
## 239. 23shades-0239-aaggfgbbj

**主题代码：** SATD-B

**开放代码：** 评估调用参数传递不全

**逐条判断：** dictionary 应传给函数内全部 metrics_helper 调用。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `140:220`：

> TODO add passing this dictionary to all calls to metrics_helper in this function

<a id="row-240"></a>
## 240. 23shades-0240-aagaagfeg

**主题代码：** SATD-D, SATD-Q

**开放代码：** 功能扩展待定

**逐条判断：** protocluster 是否添加尚不确定。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `133:155`：

> TODO add protocluster?

<a id="row-241"></a>
## 241. 23shades-0241-aajfahgcg

**主题代码：** SATD-D, SATD-E

**开放代码：** 距离指标支持不全

**逐条判断：** 需支持 euclidean/angular 等其他指标。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `161:220`：

> TODO add support for other metrics (ex. euclidean; angular)

<a id="row-242"></a>
## 242. 23shades-0242-aafegjcei

**主题代码：** SATD-K

**开放代码：** 变换测试需随实现更新

**逐条判断：** Convolve 的 keypoints 改善后增加测试。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `113:185`：

> TODO add test for keypoints once their handling was improved in Convolve

<a id="row-243"></a>
## 243. 23shades-0243-aafeihbhc

**主题代码：** SATD-K

**开放代码：** 测试缺失

**逐条判断：** 明确 add test，未说明对象。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `126:148`：

> TODO add test for this

<a id="row-244"></a>
## 244. 23shades-0244-aafhgihee

**主题代码：** SATD-D, SATD-E

**开放代码：** 加载器行为覆盖不一致

**逐条判断：** 同样行为还需加入 other loaders。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `132:171`：

> TODO Add this to other loaders as well.

<a id="row-245"></a>
## 245. 23shades-0245-aafehehfi

**主题代码：** SATD-D, SATD-O

**开放代码：** 渲染效果控制缺失

**逐条判断：** vertical gradient alpha 用于限制雾在天空/地面高度。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `128:202`：

> TODO add vertical gradient alpha to have fog only at skylevel\/groundlevel

<a id="row-246"></a>
## 246. 23shades-0246-aafehehgb

**主题代码：** SATD-A, SATD-J, SATD-M

**开放代码：** 重复参数待消除

**逐条判断：** alpha_mean 与 density 重叠，应去掉其一。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `128:184`：

> TODO alpha_mean and density overlap - remove one of them

<a id="row-247"></a>
## 247. 23shades-0247-aahiiegaf

**主题代码：** SATD-E, SATD-I, SATD-J, SATD-Q

**开放代码：** 多智能体空间扩展待考虑

**逐条判断：** AEB space 的 multi-agents 场景尚未充分预备。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `117:159`：

> TODO anticipate multi-agents for AEB space

<a id="row-248"></a>
## 248. 23shades-0248-aagjjacbh

**主题代码：** SATD-D

**开放代码：** 算法应用功能缺失

**逐条判断：** AI_trader 待构建以改善 bids/asks；不宣称已取得效果。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `140:212`：

> TODO build AI_trader that uses this algorithm to place better bids\/asks

<a id="row-249"></a>
## 249. 23shades-0249-aafbjfdjh

**主题代码：** SATD-F

**开放代码：** 依赖验证集可用性的变更

**逐条判断：** 待 SVHN 有 val set 再改，明确外部数据条件。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `124:168`：

> TODO change as soon as svhn has a val set :)

<a id="row-250"></a>
## 250. 23shades-0250-aafchcgdb

**主题代码：** SATD-A, SATD-J

**开放代码：** 选项名称待统一

**逐条判断：** normalizazion_database 改为 normalise option。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `118:172`：

> todo change normalizazion_database to normalise option

<a id="row-251"></a>
## 251. 23shades-0251-aagjigcgd

**主题代码：** SATD-A

**开放代码：** 旧实现待替换

**逐条判断：** 计划用下面更好的代码换现有实现，但无质量依据。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `125:176`：

> TODO change out existing code for better code below

<a id="row-252"></a>
## 252. 23shades-0252-aafeifgfi

**主题代码：** SATD-A, SATD-J

**开放代码：** 随机源接口待迁移

**逐条判断：** random_state 改 rng。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `116:147`：

> TODO change random_state to rng

<a id="row-253"></a>
## 253. 23shades-0253-aaebaidgd

**主题代码：** SATD-A

**开放代码：** 字段命名与关联引用迁移

**逐条判断：** self.phonemes 改 self.tgt_labels 并处理 related。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `133:196`：

> TODO Change self.phonemes field to self.tgt_labels; and related

<a id="row-254"></a>
## 254. 23shades-0254-aagigfafa

**主题代码：** SATD-A, SATD-F, SATD-N

**开放代码：** 导出接口返回结构适配

**逐条判断：** ONNX 相关 attns 从 dict 改 list/tuple。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `130:196`：

> TODO change the way attns is returned dict => list or tuple (onnx)

<a id="row-255"></a>
## 255. 23shades-0255-aafegjchi

**主题代码：** SATD-A

**开放代码：** 属性归属待调整

**逐条判断：** 移为 class attributes。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `130:167`：

> TODO change these to class attributes

<a id="row-256"></a>
## 256. 23shades-0256-aagcicecj

**主题代码：** SATD-G

**开放代码：** 数组操作性能改进

**逐条判断：** np.partition 明确为了 PERF。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `135:171`：

> TODO change to np.partition for PERF

<a id="row-257"></a>
## 257. 23shades-0257-aagcfdhaj

**主题代码：** SATD-U

**开放代码：** 证据不足

**逐条判断：** change 疑问未指定对象。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `115:127`：

> TODO change?

<a id="row-258"></a>
## 258. 23shades-0258-aagchjdcj

**主题代码：** SATD-C, SATD-K, SATD-Q

**开放代码：** 正确性待验证

**逐条判断：** 明确 check correctness，无具体失败。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `124:148`：

> TODO CHECK CORRECTNESS!!

<a id="row-259"></a>
## 259. 23shades-0259-aajbgadgf

**主题代码：** SATD-C, SATD-F

**开放代码：** 组件更新与需求检查缺失

**逐条判断：** 每个 tentacle 是否有可用更新及 requirements 待检查。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `137:218`：

> TODO check for each tentacle specified if update is available (with requirements)

<a id="row-260"></a>
## 260. 23shades-0260-aadfcehfi

**主题代码：** SATD-C, SATD-K, SATD-Q

**开放代码：** 函数检查待办不具体

**逐条判断：** getStructureCahinIds 要检查，但无具体预期。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `139:170`：

> TODO check getStructureCahinIds

<a id="row-261"></a>
## 261. 23shades-0261-aaaiefadd

**主题代码：** SATD-C, SATD-K

**开放代码：** 预处理后结果验证待办

**逐条判断：** 标准化 num ft 后待算法就绪再检查结果。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `153:235`：

> TODO check results after standardizing num ft once a ml algorithm is ready to test

<a id="row-262"></a>
## 262. 23shades-0262-aafciifib

**主题代码：** SATD-C

**开放代码：** 同名图像冲突检查缺失

**逐条判断：** 本地缓存与 cloud 可能有同名不同图像，需要核对。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `137:207`：

> TODO check the local cache and cloud for different images of same name

<a id="row-263"></a>
## 263. 23shades-0263-aadbfihhc

**主题代码：** SATD-C, SATD-Q, SATD-U

**开放代码：** 检查对象不明

**逐条判断：** check the start 无上下文。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `153:173`：

> TODO check the start

<a id="row-264"></a>
## 264. 23shades-0264-aahjaaihb

**主题代码：** SATD-D, SATD-N

**开放代码：** 检查点与增量保存缺失

**逐条判断：** 明确 checkpoints/incremental save。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `116:150`：

> TODO checkpoints; incremental save

<a id="row-265"></a>
## 265. 23shades-0265-aaejhfaai

**主题代码：** SATD-D

**开放代码：** 预测结果融合缺失

**逐条判断：** 将多个值组合成最终 prediction。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `134:186`：

> TODO combine these values to get a final prediction!

<a id="row-266"></a>
## 266. 23shades-0266-aaedhfhae

**主题代码：** SATD-C, SATD-I, SATD-K, SATD-Q

**开放代码：** 数学判据待核实

**逐条判断：** 多个 eigenvalue=1 与 rotation 的关系需要确认，原句截断。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `131:193`：

> TODO confirm that multiple eigenvalues of 1 means the rotation

<a id="row-267"></a>
## 267. 23shades-0267-aajgajdca

**主题代码：** SATD-D, SATD-E

**开放代码：** 三维情形支持缺失

**逐条判断：** 拟用 tag->size 处理 3D。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `128:180`：

> ToDo consider 3D case --> do that by using tag->size

<a id="row-268"></a>
## 268. 23shades-0268-aadfdgaei

**主题代码：** SATD-D, SATD-E, SATD-Q

**开放代码：** 多模型支持待考虑

**逐条判断：** 未说明模型组合机制。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `146:175`：

> TODO consider multiple models

<a id="row-269"></a>
## 269. 23shades-0269-aafehiefj

**主题代码：** SATD-A, SATD-J

**开放代码：** 参数表示待重构

**逐条判断：** 考虑转换为 x/y params。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `126:159`：

> TODO convert this to x\/y params?

<a id="row-270"></a>
## 270. 23shades-0270-aaebjbbad

**主题代码：** SATD-I, SATD-J, SATD-Q

**开放代码：** 随机化策略待决定

**逐条判断：** 仅问 could randomise，不推断随机种子缺失。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `147:168`：

> todo could randomise?

<a id="row-271"></a>
## 271. 23shades-0271-aahddgbeh

**主题代码：** SATD-N, SATD-Q

**开放代码：** 序列化方案选择待定

**逐条判断：** cpickle 与 json 的权衡未作出。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `135:155`：

> TODO cpickle vs json

<a id="row-272"></a>
## 272. 23shades-0272-aagjifffj

**主题代码：** SATD-D, SATD-O

**开放代码：** 分析图表缺失

**逐条判断：** 按时期绘制平均收益。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `137:192`：

> TODO create graphs of average earnings per period\uFFFF

<a id="row-273"></a>
## 273. 23shades-0273-aaebjbbei

**主题代码：** SATD-C, SATD-K

**开放代码：** 测试断言范围不足

**逐条判断：** 现有只跑 fit/predict 并比较预测序列长度，未检查数值行为。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `154:235`：

> TODO currently tests only run fit\/predict and compare length of predicted series

<a id="row-274"></a>
## 274. 23shades-0274-aaebjhccj

**主题代码：** SATD-B, SATD-N

**开放代码：** 时间索引在切片中丢失

**逐条判断：** 需给 Xt 恢复 index，明确数据结构信息损失。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `146:233`：

> TODO currently we loose the time index; need to add it back to Xt after slicing in time

<a id="row-275"></a>
## 275. 23shades-0275-aahiigije

**主题代码：** SATD-Q

**开放代码：** 调试待办

**逐条判断：** 未列具体错误，不能恢复根因。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `118:128`：

> TODO debug

<a id="row-276"></a>
## 276. 23shades-0276-aaadbjbdj

**主题代码：** SATD-D

**开放代码：** 图像去雾处理待办

**逐条判断：** 提出用 1/t，缺少算法上下文。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `151:172`：

> TODO Dehaze with 1\/t

<a id="row-277"></a>
## 277. 23shades-0277-aahiiefbi

**主题代码：** SATD-D

**开放代码：** 智能体参数同步待补

**逐条判断：** action_dim 等变量副本也需传给 agent。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `119:180`：

> TODO delegate a copy of variable like action_dim to agent too

<a id="row-278"></a>
## 278. 23shades-0278-aahhdabij

**主题代码：** SATD-A

**开放代码：** 可导入包的高级 API 缺失

**逐条判断：** 要求设计供 advanced access 的接口。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `129:202`：

> TODO design an API interface for advanced access as an importable package

<a id="row-279"></a>
## 279. 23shades-0279-aafegiaee

**主题代码：** SATD-U

**开放代码：** 未定位的图像处理待办

**逐条判断：** DirectedEdgeDetect 名称不足以判断具体欠缺。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `113:136`：

> TODO DirectedEdgeDetect

<a id="row-280"></a>
## 280. 23shades-0280-aafacjcgb

**主题代码：** SATD-J

**开放代码：** 模型过滤器数量调整

**逐条判断：** 计划把 num_filters 加倍，未证明提升。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `127:150`：

> TODO double num_filters

<a id="row-281"></a>
## 281. 23shades-0281-aafegiafa

**主题代码：** SATD-U

**开放代码：** 未定位的变换待办

**逐条判断：** ElasticTransformation 仅名字，无明确行为。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `113:139`：

> TODO ElasticTransformation

<a id="row-282"></a>
## 282. 23shades-0282-aafegiafa

**主题代码：** SATD-U

**开放代码：** 未定位的变换待办

**逐条判断：** 重复文本独立保留。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `113:139`：

> TODO ElasticTransformation

<a id="row-283"></a>
## 283. 23shades-0283-aahiifcef

**主题代码：** SATD-B

**开放代码：** 缺失数值返回约定不一致

**逐条判断：** 子方法应为 loss/explore_var 返回 np.nan 而非 None。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `119:195`：

> TODO ensure submethods return np.nan for loss or explore_var instead of None

<a id="row-284"></a>
## 284. 23shades-0284-aaecghbgf

**主题代码：** SATD-I, SATD-J, SATD-Q

**开放代码：** 参数概念混淆疑问

**逐条判断：** epsilon 与 bias 不等价，但作者尚问是否构成问题。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `175:240`：

> TODO epsilon and bias are not really the same; is this a problem?

<a id="row-285"></a>
## 285. 23shades-0285-aaacggdfb

**主题代码：** SATD-E

**开放代码：** 矩阵输入支持待扩展

**逐条判断：** 当前需扩展到 matrix data。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `140:176`：

> TODO extend to work over matrix data

<a id="row-286"></a>
## 286. 23shades-0286-aagcijbch

**主题代码：** SATD-J, SATD-Q

**开放代码：** 缺省输入处理不足

**逐条判断：** 希望利用 defaults 避免传全部 inputs，目标调用截断。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `120:205`：

> TODO Figure out a way to handle defaults so that all inputs need not be passed to the

<a id="row-287"></a>
## 287. 23shades-0287-aagdffgjh

**主题代码：** SATD-D, SATD-Q

**开放代码：** 领域状态区分策略缺失

**逐条判断：** 如何区分 oxidation states 未解决。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `119:170`：

> TODO Figure out how to distinguish oxidation states

<a id="row-288"></a>
## 288. 23shades-0288-aaedbehai

**主题代码：** SATD-L, SATD-Q

**开放代码：** 参数含义不清

**逐条判断：** size 的作用需要查明。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `128:166`：

> TODO figure out what exactly size does

<a id="row-289"></a>
## 289. 23shades-0289-aafegibaf

**主题代码：** SATD-U

**开放代码：** 证据不足

**逐条判断：** ForceSign 名称未指明待办。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `126:140`：

> TODO ForceSign

<a id="row-290"></a>
## 290. 23shades-0290-aaebieajg

**主题代码：** SATD-E

**开放代码：** 不等长序列支持缺失

**逐条判断：** columns 中 unequal length series 需泛化。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `155:211`：

> TODO generalise to columns with series of unequal length

<a id="row-291"></a>
## 291. 23shades-0291-aaebiddhj

**主题代码：** SATD-E

**开放代码：** 非同索引情形支持缺失

**逐条判断：** non-equal-index 场景待泛化。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `155:195`：

> TODO generalise to non-equal-index cases

<a id="row-292"></a>
## 292. 23shades-0292-aaebieaia

**主题代码：** SATD-E

**开放代码：** 序列函数接口支持不足

**逐条判断：** 扩展 series-to-series functions 及 kwargs。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `156:221`：

> TODO generalise to series-to-series functions and function kwargs

<a id="row-293"></a>
## 293. 23shades-0293-aahiihdej

**主题代码：** SATD-H

**开放代码：** 评估模型位置设置绕行

**逐条判断：** 需在 info_space 内 hack 设置 eval model location。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `104:163`：

> TODO hack and set the eval model location inside info_space

<a id="row-294"></a>
## 294. 23shades-0294-aaebjigjj

**主题代码：** SATD-E

**开放代码：** 一维序列输入不支持

**逐条判断：** 当前限二维 dataframe，需处理一维 series。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `146:191`：

> TODO handle 1d series; not only 2d dataframes

<a id="row-295"></a>
## 295. 23shades-0295-aadghcged

**主题代码：** SATD-E

**开放代码：** 复杂标识符支持不全

**逐条判断：** source/target 为 COMPLEX:ID1_ID2 时需处理。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `144:205`：

> ToDo handle when source and\/or target is COMPLEX:ID1_ID2_...

<a id="row-296"></a>
## 296. 23shades-0296-aahiigecd

**主题代码：** SATD-B, SATD-I

**开放代码：** 无动量时权重更新约束

**逐条判断：** 作者指出无 momentum 时 weights 也不应变化；不假定当前实现确实变化。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `123:178`：

> TODO if without momentum; weights should not change too

<a id="row-297"></a>
## 297. 23shades-0297-aafhgjiha

**主题代码：** SATD-D

**开放代码：** 功能尚未实现

**逐条判断：** Implement 无对象。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `122:136`：

> TODO Implement

<a id="row-298"></a>
## 298. 23shades-0298-aafhhaidh

**主题代码：** SATD-D

**开放代码：** 功能尚未实现

**逐条判断：** Implement 无对象，独立条目。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `122:136`：

> TODO Implement

<a id="row-299"></a>
## 299. 23shades-0299-aahiiegbc

**主题代码：** SATD-D

**开放代码：** 通用方法缺失

**逐条判断：** generic method 待实现。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `119:148`：

> TODO implement generic method

<a id="row-300"></a>
## 300. 23shades-0300-aaejhiaeb

**主题代码：** SATD-D, SATD-E, SATD-G, SATD-K

**开放代码：** 多 GPU 训练缺失；性能比较待执行

**逐条判断：** 需要先实现再比较性能，不能称已提速。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `135:192`：

> TODO implement multi-gpu training and compare performance

<a id="row-301"></a>
## 301. 23shades-0301-aagacdjjd

**主题代码：** SATD-A, SATD-Q

**开放代码：** 正则实现待改进

**逐条判断：** 未说明当前错误匹配或具体优化。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `116:143`：

> TODO improve the regex here

<a id="row-302"></a>
## 302. 23shades-0302-aahiiggad

**主题代码：** SATD-D, SATD-E, SATD-J

**开放代码：** 连续动作空间支持缺失

**逐条判断：** 将 DELTA buttons 用 gym Box space 处理。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `128:224`：

> TODO In future; need to update action to handle (continuous) DELTA buttons using gym's Box space

<a id="row-303"></a>
## 303. 23shades-0303-aahciidhf

**主题代码：** SATD-A

**开放代码：** 初始化职责位置不合理

**逐条判断：** 希望更有原则地在其他位置初始化。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `131:185`：

> TODO init this somewhere else in a more principled way

<a id="row-304"></a>
## 304. 23shades-0304-aahddgcai

**主题代码：** SATD-U

**开放代码：** 未定位的初始化待办

**逐条判断：** init-phase 无具体动作。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `133:148`：

> TODO init-phase

<a id="row-305"></a>
## 305. 23shades-0305-aahddgbgb

**主题代码：** SATD-N, SATD-Q

**开放代码：** 序列化格式选择疑问

**逐条判断：** json 是候选，缺少数据对象。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `135:145`：

> TODO json?

<a id="row-306"></a>
## 306. 23shades-0306-aafchbaid

**主题代码：** SATD-D

**开放代码：** token 边界处理待补

**逐条判断：** last token include 后有表达式，具体语义不足。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `116:164`：

> TODO last token include: \"&& $last_token[...]\"

<a id="row-307"></a>
## 307. 23shades-0307-aajcfhiga

**主题代码：** SATD-A, SATD-Q

**开放代码：** 状态归属待决定

**逐条判断：** paf_scored 是否属于 self 尚未决定。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `146:184`：

> TODO make paf_scored not part of self?

<a id="row-308"></a>
## 308. 23shades-0308-aaaecigij

**主题代码：** SATD-A

**开放代码：** 独立类抽象缺失

**逐条判断：** 明确希望单独 class。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `144:175`：

> TODO Make separate class for it

<a id="row-309"></a>
## 309. 23shades-0309-aadfiacgf

**主题代码：** SATD-J

**开放代码：** 阈值硬编码待参数化

**逐条判断：** threshold 应改变量。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `120:150`：

> TODO make threshold a variable

<a id="row-310"></a>
## 310. 23shades-0310-aafadaiij

**主题代码：** SATD-A, SATD-Q

**开放代码：** 张量操作组织待调整

**逐条判断：** max in one tensor 表述短，不能断言是性能或正确性问题。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `124:146`：

> TODO max in one tensor

<a id="row-311"></a>
## 311. 23shades-0311-aadbcjahd

**主题代码：** SATD-A

**开放代码：** 全局状态耦合待移除

**逐条判断：** 希望不使用 global。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `149:199`：

> TODO maybe improve this so it doesn't use a global

<a id="row-312"></a>
## 312. 23shades-0312-aahddgaji

**主题代码：** SATD-A

**开放代码：** 模块组织待合并

**逐条判断：** 计划与 experiment.py 合并。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `129:158`：

> TODO merge with experiment.py

<a id="row-313"></a>
## 313. 23shades-0313-aadfjejae

**主题代码：** SATD-A

**开放代码：** 后端注册职责待分离

**逐条判断：** 注册移入 backend-specific files。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `119:174`：

> TODO move these registrations to backend-specific files

<a id="row-314"></a>
## 314. 23shades-0314-aadfcfhgh

**主题代码：** SATD-A, SATD-Q

**开放代码：** 结构化表示选择待定

**逐条判断：** named tuple 或 enum 两种候选。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `149:173`：

> TODO named tuple or enum

<a id="row-315"></a>
## 315. 23shades-0315-aaecghbei

**主题代码：** SATD-Q, SATD-U

**开放代码：** 逻辑必要性待定

**逐条判断：** needed，无对象。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `175:187`：

> TODO needed?

<a id="row-316"></a>
## 316. 23shades-0316-aafbifbhe

**主题代码：** SATD-K

**开放代码：** 测试缺失

**逐条判断：** 明确 needs testing。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `129:147`：

> TODO needs testing

<a id="row-317"></a>
## 317. 23shades-0317-aaieffgij

**主题代码：** SATD-K

**开放代码：** 系统变更后测试未更新

**逐条判断：** new system 需要 new tests。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `119:151`：

> TODO new tests due to new system

<a id="row-318"></a>
## 318. 23shades-0318-aaejhfaed

**主题代码：** SATD-I, SATD-J, SATD-Q

**开放代码：** 归一化数学约束待定

**逐条判断：** 是否归一化使总和等于一。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `137:172`：

> TODO normalice to make sum up to 1?

<a id="row-319"></a>
## 319. 23shades-0319-aafdjgjfa

**主题代码：** SATD-E

**开放代码：** 稠密输入不支持

**逐条判断：** 明确 not support dense。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `128:150`：

> todo not support dense

<a id="row-320"></a>
## 320. 23shades-0320-aaedbiehj

**主题代码：** SATD-I, SATD-Q

**开放代码：** 输出通道处理不确定

**逐条判断：** 作者不确定 out-channels 的正确处理。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `140:190`：

> TODO not sure how to handle out-channels properly.

<a id="row-321"></a>
## 321. 23shades-0321-aadfdfiba

**主题代码：** SATD-G

**开放代码：** 执行优化待办

**逐条判断：** optimize method，无具体瓶颈。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `135:160`：

> TODO optimize this method

<a id="row-322"></a>
## 322. 23shades-0322-aaacgfhgb

**主题代码：** SATD-J

**开放代码：** 字符串长度缺少配置

**逐条判断：** 需提供 string length option。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `139:168`：

> TODO Option for string lenght

<a id="row-323"></a>
## 323. 23shades-0323-aaffbcfif

**主题代码：** SATD-C

**开放代码：** 路径输入校验缺失

**逐条判断：** 明确包含 empty path。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `142:174`：

> TODO path validation; empty path

<a id="row-324"></a>
## 324. 23shades-0324-aajcjfcfc

**主题代码：** SATD-E, SATD-F, SATD-Q

**开放代码：** CUDA 移植待评估

**逐条判断：** 问是否 port，不宣称已决定。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `140:158`：

> TODO Port to cuda?

<a id="row-325"></a>
## 325. 23shades-0325-aadfjfbei

**主题代码：** SATD-A

**开放代码：** 类型层次重构

**逐条判断：** 将当前对象提升为 Funsor subclass。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `119:158`：

> TODO Promote this to a Funsor subclass.

<a id="row-326"></a>
## 326. 23shades-0326-aaeadhaac

**主题代码：** SATD-A, SATD-Q

**开放代码：** 随机函数语义待统一

**逐条判断：** random/uniform/randint(discrete) 的关系被列为待办，不能视为已经等价。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `128:172`：

> TODO random == uniform == randint (discrete)

<a id="row-327"></a>
## 327. 23shades-0327-aadagfcdg

**主题代码：** SATD-J

**开放代码：** 随机种子不可配置

**逐条判断：** 要求 random seed option。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `127:156`：

> TODO random seed as an option

<a id="row-328"></a>
## 328. 23shades-0328-aadgecacc

**主题代码：** SATD-A, SATD-Q

**开放代码：** 在线预测引入时需重构

**逐条判断：** live model prediction 实现时调整 if 后半段。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `187:268`：

> TODO refactor second part of if statement when implementing live model prediction

<a id="row-329"></a>
## 329. 23shades-0329-aaaedaiaa

**主题代码：** SATD-A

**开放代码：** 重复方法组织不良

**逐条判断：** 两个 clunky redundant 方法待重构。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `165:214`：

> TODO Refactor these two clunky; redundant methods

<a id="row-330"></a>
## 330. 23shades-0330-aaheeahhj

**主题代码：** SATD-A

**开放代码：** 计数表示复用库抽象

**逐条判断：** self.counts 拟采用 nltk FreqDist。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `135:202`：

> TODO refactor to use nltk_lite.probability.FreqDist for self.counts

<a id="row-331"></a>
## 331. 23shades-0331-aafhghged

**主题代码：** SATD-M

**开放代码：** 清理待办

**逐条判断：** remove 未给对象。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `123:134`：

> TODO remove

<a id="row-332"></a>
## 332. 23shades-0332-aagejhdij

**主题代码：** SATD-M

**开放代码：** 清理待办

**逐条判断：** Remove 未给对象。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `106:117`：

> TODO Remove

<a id="row-333"></a>
## 333. 23shades-0333-aadfaifgh

**主题代码：** SATD-M

**开放代码：** 清理推迟

**逐条判断：** later 删除。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `138:156`：

> TODO remove later.

<a id="row-334"></a>
## 334. 23shades-0334-aaebajfae

**主题代码：** SATD-J, SATD-M

**开放代码：** 参数清理待办

**逐条判断：** 删除 target_type。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `135:158`：

> TODO Remove target_type

<a id="row-335"></a>
## 335. 23shades-0335-aagaceabd

**主题代码：** SATD-M

**开放代码：** 清理待办

**逐条判断：** remove this 无上下文。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `119:135`：

> TODO remove this

<a id="row-336"></a>
## 336. 23shades-0336-aafehbbbf

**主题代码：** SATD-A, SATD-Q

**开放代码：** 命名一致性待改

**逐条判断：** sizes 改 size 尚为疑问。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `116:142`：

> TODO rename sizes to size?

<a id="row-337"></a>
## 337. 23shades-0337-aaebaidjj

**主题代码：** SATD-A

**开放代码：** 命名表达待改

**逐条判断：** 改为 tokens2indices 或类似名字。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `133:193`：

> TODO rename this to \"tokens2indices\" or something similar.

<a id="row-338"></a>
## 338. 23shades-0338-aagbbjgij

**主题代码：** SATD-H, SATD-M

**开放代码：** 可视化修复后替换临时代码

**逐条判断：** 有明确先决条件 viz fixed，再换注释中的实现。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `137:216`：

> TODO replace this code with the following commented out code after viz is fixed

<a id="row-339"></a>
## 339. 23shades-0339-aaifefdce

**主题代码：** SATD-A

**开放代码：** 模型加速实现替换

**逐条判断：** 计划用 nni ModelSpeedup 替代自有 speedup，未测量收益。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `164:244`：

> TODO replace this speedup implementation with nni.compression.torch.ModelSpeedup

<a id="row-340"></a>
## 340. 23shades-0340-aaebjbdgg

**主题代码：** SATD-A

**开放代码：** 参数接口携带过多数据

**逐条判断：** 用单独 metadata container 替代整个 pandas data container 入参。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `141:233`：

> TODO replace whole pandas data container as input argument with separated metadata container

<a id="row-341"></a>
## 341. 23shades-0341-aaecghdag

**主题代码：** SATD-F, SATD-H, SATD-M

**开放代码：** 依赖未实现功能的后续替换

**逐条判断：** pad 实现后替换当前逻辑。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `175:213`：

> TODO replace with pad when implemented

<a id="row-342"></a>
## 342. 23shades-0342-aajceeeid

**主题代码：** SATD-A

**开放代码：** 实现替代待办

**逐条判断：** 拟改 Streamlines，动机不可见。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `120:149`：

> TODO replace with Streamlines

<a id="row-343"></a>
## 343. 23shades-0343-aaadbhidf

**主题代码：** SATD-D, SATD-N

**开放代码：** 训练模型恢复缺失

**逐条判断：** 需从 trained data 恢复 CNN。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `147:185`：

> TODO Restore our CNN from trained data

<a id="row-344"></a>
## 344. 23shades-0344-aafejacii

**主题代码：** SATD-D, SATD-N

**开放代码：** 运行时间信息待补

**逐条判断：** run start date 未说明使用方式。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `126:145`：

> TODO run start date

<a id="row-345"></a>
## 345. 23shades-0345-aafagebef

**主题代码：** SATD-D, SATD-N

**开放代码：** 实验结果持久化缺失

**逐条判断：** 全部 results 保存到实验目录 JSON。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `137:203`：

> TODO save all the results to a json inside the experiment's folder

<a id="row-346"></a>
## 346. 23shades-0346-aahiiefbj

**主题代码：** SATD-D, SATD-N

**开放代码：** 保存功能待定

**逐条判断：** save or smth，意图存在但方案不明确。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `119:136`：

> TODO save or smth

<a id="row-347"></a>
## 347. 23shades-0347-aaahgiacg

**主题代码：** SATD-A, SATD-Q

**开放代码：** 替代算法探索

**逐条判断：** 建议查网络或用 other algorithms，未指定判断标准。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `133:176`：

> TODO Search the web or use other algorithms

<a id="row-348"></a>
## 348. 23shades-0348-aajajehgf

**主题代码：** SATD-F, SATD-K

**开放代码：** 持续集成环境测试失败

**逐条判断：** 测试在 TravisCI 失败，原因在冒号后缺失。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `152:241`：

> TODO see if there is a way to make this test work - it fails on travisCI because of this:

<a id="row-349"></a>
## 349. 23shades-0349-aagciihdj

**主题代码：** SATD-D

**开放代码：** 上下文回传与状态维护缺失

**逐条判断：** context 返回某 list，维护主体截断。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `117:172`：

> TODO Send the context back into some list maintained by

<a id="row-350"></a>
## 350. 23shades-0350-aadfcfcca

**主题代码：** SATD-D

**开放代码：** 领域元信息未设置

**逐条判断：** bioassembly info 待设。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `157:182`：

> TODO Set bioassembly info

<a id="row-351"></a>
## 351. 23shades-0351-aajbebjea

**主题代码：** SATD-A, SATD-Q

**开放代码：** 抽象通用性待决策

**逐条判断：** 是否继续 generic 尚不明确。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `143:181`：

> TODO Should this stay generic? (point)

<a id="row-352"></a>
## 352. 23shades-0352-aaifjjgei

**主题代码：** SATD-Q

**开放代码：** 重建能力需求待决策

**逐条判断：** 是否允许 rebuild 是开放问题。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `119:153`：

> TODO Should we be able to rebuild?

<a id="row-353"></a>
## 353. 23shades-0353-aafehgfdb

**主题代码：** SATD-A

**开放代码：** 重复循环简化

**逐条判断：** heatmaps/keypoints 等循环应类似 Alpha 简化。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `126:204`：

> TODO simplify this loop and the ones for heatmaps; keypoints; similar to Alpha

<a id="row-354"></a>
## 354. 23shades-0354-aagfabaij

**主题代码：** SATD-A

**开放代码：** 职责拆分待办

**逐条判断：** 拆成独立 functions。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `113:147`：

> TODO Split into separate functions

<a id="row-355"></a>
## 355. 23shades-0355-aajgdiheg

**主题代码：** SATD-D

**开放代码：** 刺激通道筛除待办

**逐条判断：** stim channel exclusion，未给标准。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `125:152`：

> TODO stim channel exclusion

<a id="row-356"></a>
## 356. 23shades-0356-aaeidhdde

**主题代码：** SATD-D, SATD-E

**开放代码：** 并行循环支持范围不足

**逐条判断：** recursive parfor/multi-D/multiple body blocks 待支持。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `124:183`：

> TODO support recursive parfor; multi-D; mutiple body blocks

<a id="row-357"></a>
## 357. 23shades-0357-aaedcebbj

**主题代码：** SATD-U

**开放代码：** 证据不足

**逐条判断：** sweep 未说明参数扫描还是其他行为。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `130:140`：

> todo sweep

<a id="row-358"></a>
## 358. 23shades-0358-aajajbadj

**主题代码：** SATD-A, SATD-G

**开放代码：** 不必要复制待改原地操作

**逐条判断：** 明确从复制改 inplace，不额外假定实测内存收益。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `155:222`：

> TODO switch similar statements to work inplace (w\/o making a copy)

<a id="row-359"></a>
## 359. 23shades-0359-aajebahia

**主题代码：** SATD-K

**开放代码：** 格式测试覆盖不足

**逐条判断：** ligand 更多 formats 需测试。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `152:185`：

> TODO test more formats for ligand

<a id="row-360"></a>
## 360. 23shades-0360-aajecehjc

**主题代码：** SATD-K

**开放代码：** 格式测试覆盖不足

**逐条判断：** 重复文本独立保留。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `143:176`：

> TODO test more formats for ligand

<a id="row-361"></a>
## 361. 23shades-0361-aageaibai

**主题代码：** SATD-K

**开放代码：** 结构嵌套测试缺失

**逐条判断：** nestedness 待测试。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `128:148`：

> TODO test nestedness

<a id="row-362"></a>
## 362. 23shades-0362-aahchacde

**主题代码：** SATD-D, SATD-E, SATD-F

**开放代码：** 框架迁移时参数遗漏

**逐条判断：** TF2 需要重新引入 optimizer parameters。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `126:168`：

> todo tf2: reintroduce optimizer parameters

<a id="row-363"></a>
## 363. 23shades-0363-aaebajbaf

**主题代码：** SATD-I, SATD-J

**开放代码：** 固定比率待消除

**逐条判断：** 明确 ratios 不能 hardcoded。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `128:164`：

> TODO These ratios can't be hardcoded

<a id="row-364"></a>
## 364. 23shades-0364-aaifjjccj

**主题代码：** SATD-V

**开放代码：** 异步接口依赖说明

**逐条判断：** 当前代码对 async_fit 必需，没有明确债务陈述。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `117:202`：

> TODO this code is currently necessary for the async_fit method in websocket_client.py

<a id="row-365"></a>
## 365. 23shades-0365-aaebabejj

**主题代码：** SATD-B

**开放代码：** 组合功能失效

**逐条判断：** this combo 不工作，具体对象不明。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `165:193`：

> TODO this combo doens't work

<a id="row-366"></a>
## 366. 23shades-0366-aaebagcaf

**主题代码：** SATD-O

**开放代码：** 错误信息不合适

**逐条判断：** 需要改变 message，不等于异常机制缺失。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `136:175`：

> TODO this error message needs changing.

<a id="row-367"></a>
## 367. 23shades-0367-aadfjffba

**主题代码：** SATD-A, SATD-E, SATD-Q

**开放代码：** 操作注册范围过泛

**逐条判断：** 希望 register all ops，当前 too general；具体注册策略不明。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `120:162`：

> TODO this is too general; register all ops

<a id="row-368"></a>
## 368. 23shades-0368-aafchdiaf

**主题代码：** SATD-B, SATD-E

**开放代码：** 未出现在边中的实体类型处理错误

**逐条判断：** 明确其他 entity types 时 wrong。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `134:203`：

> TODO this is wrong for other entitiey types nor appearing in the edge

<a id="row-369"></a>
## 369. 23shades-0369-aaehaifef

**主题代码：** SATD-G

**开放代码：** 稀疏向量表示浪费内存

**逐条判断：** 作者明确认为可 memory efficient。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `116:185`：

> TODO this vector is very sparse; we can make it more memory efficient

<a id="row-370"></a>
## 370. 23shades-0370-aafeghegj

**主题代码：** SATD-C, SATD-E, SATD-I

**开放代码：** 参数形状能力未检查

**逐条判断：** 若参数不能接受 size=(N,) 会失败。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `120:176`：

> TODO this will fail if a parameter cant handle size=(N;)

<a id="row-371"></a>
## 371. 23shades-0371-aaadajhci

**主题代码：** SATD-U

**开放代码：** 证据不足

**逐条判断：** to be modified，无对象或目的。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `140:159`：

> TODO to be modified

<a id="row-372"></a>
## 372. 23shades-0372-aadfcefca

**主题代码：** SATD-B

**开放代码：** 解码异常与资源警告

**逐条判断：** 原文同时含 unclosed file 和 ASCII decode 失败，无法从混合 traceback 判共同根因。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `134:278`：

> TODO Traceback \"ResourceWarning: unclosed filecodeDecodeError: 'ascii' codec can't decode byte 0xc3 in position 25: ordinal not in range(128)\"

<a id="row-373"></a>
## 373. 23shades-0373-aagcjhcea

**主题代码：** SATD-A, SATD-Q

**开放代码：** 空白规范化方案候选

**逐条判断：** join(split()) 是拟尝试表达式，不推断已发现格式 bug。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `129:162`：

> todo try: \" \".join(foo.split())

<a id="row-374"></a>
## 374. 23shades-0374-aahiiffci

**主题代码：** SATD-D, SATD-N

**开放代码：** 模型保存加载模式未启用

**逐条判断：** 明确 turn on save/load mode。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `104:138`：

> TODO turn on save\/load model mode

<a id="row-375"></a>
## 375. 23shades-0375-aafeihffh

**主题代码：** SATD-A, SATD-J

**开放代码：** 模式参数处理重复待统一

**逐条判断：** 与 global _handle_mode_arg 合并，后句截断。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `130:196`：

> TODO unify this somehow with the global _handle_mode_arg() that is

<a id="row-376"></a>
## 376. 23shades-0376-aaebjafhg

**主题代码：** SATD-K

**开放代码：** 单元测试缺失

**逐条判断：** unit tests 待办。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `147:162`：

> todo unit tests

<a id="row-377"></a>
## 377. 23shades-0377-aafchfjcg

**主题代码：** SATD-A, SATD-M

**开放代码：** 过时位置逻辑待迁移

**逐条判断：** 当前不在这里使用，应 update/move。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `123:168`：

> TODO Update and move now this isn't used here

<a id="row-378"></a>
## 378. 23shades-0378-aahiieejb

**主题代码：** SATD-L

**开放代码：** 文档陈旧

**逐条判断：** 需更新上方 doc。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `125:146`：

> TODO update doc above

<a id="row-379"></a>
## 379. 23shades-0379-aaecjdbfd

**主题代码：** SATD-E, SATD-F

**开放代码：** 框架转换类适配待更新

**逐条判断：** sklearn transformation class 的能力句截断，无法识别确切契约。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `121:188`：

> TODO update these - the sklearn transformation class should be able

<a id="row-380"></a>
## 380. 23shades-0380-aahddgbgf

**主题代码：** SATD-A, SATD-Q

**开放代码：** 容器操作替换

**逐条判断：** 计划用 pop，未给收益或对象。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `135:147`：

> TODO use pop

<a id="row-381"></a>
## 381. 23shades-0381-aagcicfdi

**主题代码：** SATD-A, SATD-Q

**开放代码：** 预计算量使用待调整

**逐条判断：** 计划采用 X_nrom_squared，不推断正确拼写或算法。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `138:161`：

> TODO use X_nrom_squared

<a id="row-382"></a>
## 382. 23shades-0382-aaffbchga

**主题代码：** SATD-C

**开放代码：** 路径校验与规范化缺失

**逐条判断：** 需要 validate/normalize 指定路径形式。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `138:189`：

> TODO validate and normalize to \/path\/to\/variable

<a id="row-383"></a>
## 383. 23shades-0383-aajdbcadb

**主题代码：** SATD-C, SATD-J

**开放代码：** 配置校验与默认设置缺失

**逐条判断：** 两项均明确待办。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `114:158`：

> TODO validate configuration and set defaults

<a id="row-384"></a>
## 384. 23shades-0384-aahcgeaed

**主题代码：** SATD-B, SATD-J

**开放代码：** 配置参数未生效

**逐条判断：** validation_split 没有使用。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `132:165`：

> TODO validation_split is not used

<a id="row-385"></a>
## 385. 23shades-0385-aaegicgcc

**主题代码：** SATD-I, SATD-V

**开放代码：** 处理条件假设

**逐条判断：** 指出 conditioning on positive treatment，未明确是错误。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `131:178`：

> TODO we are conditioning on a postive treatment

<a id="row-386"></a>
## 386. 23shades-0386-aaiehihbh

**主题代码：** SATD-K

**开放代码：** 测试暂未启用

**逐条判断：** 将来 enable test。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `115:153`：

> TODO we need to enable the test later.

<a id="row-387"></a>
## 387. 23shades-0387-aahiiejjd

**主题代码：** SATD-B, SATD-D

**开放代码：** 反向传播变量使用不完整

**逐条判断：** 需使用 relevant r，具体梯度公式未给。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `124:169`：

> TODO when backprop need to use relevant r too

<a id="row-388"></a>
## 388. 23shades-0388-aagaghfcd

**主题代码：** SATD-H, SATD-I

**开放代码：** 损失实现依赖强数据假设

**逐条判断：** WIP temp_coherence_loss 假设所有序列共享 Baxter arm 至少一个三维位置。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `111:223`：

> TODO WIP temp_coherence_loss # assumes all sequences in the dataset share at least one same 3D pos of Baxter arm

<a id="row-389"></a>
## 389. 23shades-0389-aagachejb

**主题代码：** SATD-A, SATD-Q

**开放代码：** 集合表示替代列表待评估

**逐条判断：** set 是否更好尚为疑问。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `145:202`：

> TODO wouldn't it be better with a set rather than a list?

<a id="row-390"></a>
## 390. 23shades-0390-aagdhccjd

**主题代码：** SATD-O

**开放代码：** 告警缺失

**逐条判断：** 需要 write warning，无具体触发条件。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `122:142`：

> TODO write a warning

<a id="row-391"></a>
## 391. 23shades-0391-aagfeabbh

**主题代码：** SATD-U

**开放代码：** 证据不足

**逐条判断：** 只有 TODO。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `128:133`：

> TODO!

<a id="row-392"></a>
## 392. 23shades-0392-aaghbecie

**主题代码：** SATD-F, SATD-M, SATD-Q

**开放代码：** 依赖移除待评估

**逐条判断：** consider removing dependency，尚未决定。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `159:205`：

> TODO(ahundt) consider removing this dependency

<a id="row-393"></a>
## 393. 23shades-0393-aaghajbbe

**主题代码：** SATD-A, SATD-F

**开放代码：** 解析模式差异与字段迁移未解决

**逐条判断：** redundant/regular proto parsing 以及 grasp_success rename 需协调。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `168:298`：

> TODO(ahundt) difference between \"redundant\" and regular proto parsing; figure out how to deal with grasp_success rename properly

<a id="row-394"></a>
## 394. 23shades-0394-aaghdbejg

**主题代码：** SATD-G

**开放代码：** 执行效率改进

**逐条判断：** make more efficient 未给具体机制。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `153:185`：

> TODO(ahundt) make more efficient

<a id="row-395"></a>
## 395. 23shades-0395-aaggjcebg

**主题代码：** SATD-B, SATD-I, SATD-K, SATD-Q

**开放代码：** 旋转分量方向待核实

**逐条判断：** 可能因 sva 实现需要取逆，保留 maybe。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `154:251`：

> TODO(ahundt) maybe the rotation component of this needs to be inverted due to sva implementation?

<a id="row-396"></a>
## 396. 23shades-0396-aaggjhfeh

**主题代码：** SATD-A

**开放代码：** 数据集操作职责迁移

**逐条判断：** 移入 _get_simple_parallel_dataset_ops，不因函数名推断并行实现缺失。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `153:225`：

> TODO(ahundt) MOVE THE CODE ABOVE INTO _get_simple_parallel_dataset_ops()

<a id="row-397"></a>
## 397. 23shades-0397-aahjideha

**主题代码：** SATD-A, SATD-F

**开放代码：** 循环依赖缺陷

**逐条判断：** 明确 fix circular dependencies。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `153:203`：

> TODO(b\/119775953): fix the circular dependencies.

<a id="row-398"></a>
## 398. 23shades-0398-aajabjhjb

**主题代码：** SATD-C, SATD-E, SATD-F

**开放代码：** 类型提升支持前的修复依赖

**逐条判断：** 需等 correct dtype promotion 支持后修复。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `142:201`：

> TODO(beam2d): Fix after supporting correct dtype promotion.

<a id="row-399"></a>
## 399. 23shades-0399-aaijchbde

**主题代码：** SATD-D

**开放代码：** 功能尚未实现

**逐条判断：** Implement it，功能未指明。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `117:143`：

> TODO(beam2d): Implement it

<a id="row-400"></a>
## 400. 23shades-0400-aaigebhce

**主题代码：** SATD-D

**开放代码：** 聚合运算缺失

**逐条判断：** mean 待实现。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `143:171`：

> TODO(beam2d): implement mean

<a id="row-401"></a>
## 401. 23shades-0401-aaegacgid

**主题代码：** SATD-A, SATD-G, SATD-Q

**开放代码：** 资源分配算法待改进

**逐条判断：** 明确 computation/allocation，无具体瓶颈。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `121:187`：

> TODO(crcrpar): Improve resource computation\/allocation algorithm.

<a id="row-402"></a>
## 402. 23shades-0402-aagibhhbe

**主题代码：** SATD-A

**开放代码：** 数据集职责内聚不足

**逐条判断：** 逻辑应移入 dataset definition。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `146:205`：

> TODO(dbieber): Move this logic into the dataset definition.

<a id="row-403"></a>
## 403. 23shades-0403-aaggciajj

**主题代码：** SATD-J

**开放代码：** 配置外置待办

**逐条判断：** 移入 config，具体值缺失。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `132:164`：

> TODO(fstahlberg): Move to config

<a id="row-404"></a>
## 404. 23shades-0404-aahfghdbg

**主题代码：** SATD-A, SATD-J

**开放代码：** 强化学习参数接口迁移

**逐条判断：** 重构为 newer RL-friendly 参数传递。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `142:210`：

> TODO(levskaya): refactor to use newer RL friendly parameter passing.

<a id="row-405"></a>
## 405. 23shades-0405-aahjighda

**主题代码：** SATD-I, SATD-J, SATD-O, SATD-Q

**开放代码：** 缺省图选择缺少可观察性

**逐条判断：** 可能记录 default graph 使用；or set 后方案截断。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `152:220`：

> TODO(mrry): Perhaps log that the default graph is being used; or set

<a id="row-406"></a>
## 406. 23shades-0406-aahhejjge

**主题代码：** SATD-G

**开放代码：** 广播计算性能改进

**逐条判断：** 提出 broadcast 明确为了 performance。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `120:171`：

> TODO(nolivia): improve performance with a broadcast

<a id="row-407"></a>
## 407. 23shades-0407-aaijdefji

**主题代码：** SATD-D

**开放代码：** 分区索引算子缺失

**逐条判断：** argpartition 待实现。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `112:147`：

> TODO(okuta): Implement argpartition

<a id="row-408"></a>
## 408. 23shades-0408-aaijddhbj

**主题代码：** SATD-D

**开放代码：** 分区索引算子缺失

**逐条判断：** 相同文本独立保留。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `116:151`：

> TODO(okuta): Implement argpartition

<a id="row-409"></a>
## 409. 23shades-0409-aaijddeia

**主题代码：** SATD-D

**开放代码：** 矩阵分解算子缺失

**逐条判断：** qr 待实现。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `124:149`：

> TODO(okuta): Implement qr

<a id="row-410"></a>
## 410. 23shades-0410-aaijddddf

**主题代码：** SATD-D

**开放代码：** 排序算子缺失

**逐条判断：** sort 待实现。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `112:139`：

> TODO(okuta): Implement sort

<a id="row-411"></a>
## 411. 23shades-0411-aaiafgfcj

**主题代码：** SATD-B

**开放代码：** 评估回调忽略运行步数

**逐条判断：** eval step hook 应考虑 steps_per_run。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `168:230`：

> TODO(priyag): Fix eval step hook to account for steps_per_run.

<a id="row-412"></a>
## 412. 23shades-0412-aadbbhbgg

**主题代码：** SATD-A, SATD-Q

**开放代码：** 命名生成策略不佳

**逐条判断：** scope names 需更好生成方式。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `165:229`：

> TODO(rathodv): Come up with a better way to generate scope names

<a id="row-413"></a>
## 413. 23shades-0413-aajdhaicc

**主题代码：** SATD-U

**开放代码：** 输入文件假设截断

**逐条判断：** xlsx/csv 所有 columns 被期待满足什么未给出。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `133:203`：

> TODO(rbharath): The script expects that all columns in xlsx\/csv files

<a id="row-414"></a>
## 414. 23shades-0414-aaiiaefbb

**主题代码：** SATD-Q, SATD-U

**开放代码：** 不理想行为说明截断

**逐条判断：** probably undesirable，但行为和临时理由缺失。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `144:209`：

> TODO(rliaw): This behavior is probably undesirable; but right now

<a id="row-415"></a>
## 415. 23shades-0415-aajahjjch

**主题代码：** SATD-A, SATD-F

**开放代码：** 语言实现迁移

**逐条判断：** 拟 C++ 实现；不能无依据归为性能提升。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `126:156`：

> TODO(sonots): Implement in C++

<a id="row-416"></a>
## 416. 23shades-0416-aaiibahhd

**主题代码：** SATD-A, SATD-E, SATD-F, SATD-M

**开放代码：** 版本废弃解除依赖约束

**逐条判断：** 待 ModelV1 弃用且不再 circular 时加功能；后句截断。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `123:197`：

> TODO(sven): Add once ModelV1 is deprecated and we no longer cause circular

<a id="row-417"></a>
## 417. 23shades-0417-aajefdiii

**主题代码：** SATD-A

**开放代码：** 数据结构与批处理功能整合

**逐条判断：** 考虑合并 NamedTuple 和 batchify。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `141:220`：

> TODO(sxjscience) Consider to combine the NamedTuple and batchify functionality.

<a id="row-418"></a>
## 418. 23shades-0418-aadhgfgeb

**主题代码：** SATD-J

**开放代码：** 进程数不可配置

**逐条判断：** 明确应 configurable。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `144:206`：

> TODO(tokunaga): the number of processes should be configurable

<a id="row-419"></a>
## 419. 23shades-0419-aadheehad

**主题代码：** SATD-B, SATD-O, SATD-Q

**开放代码：** 输出未显示原因待查

**逐条判断：** this isn't printed，具体内容不明。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `120:169`：

> TODO(vsatish): Figure out why this isn't printed.

<a id="row-420"></a>
## 420. 23shades-0420-aadhgacdi

**主题代码：** SATD-A, SATD-Q

**开放代码：** 职责位置待迁移

**逐条判断：** move somewhere，目的不明确。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `133:167`：

> TODO(wakisaka): move to somewhere.

<a id="row-421"></a>
## 421. 23shades-0421-aajfaggeb

**主题代码：** SATD-L

**开放代码：** 产物说明文件缺失

**逐条判断：** output_dir 需 README。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `154:194`：

> TODO. create README file in <output_dir>

<a id="row-422"></a>
## 422. 23shades-0422-aajfahfei

**主题代码：** SATD-M

**开放代码：** 旧入口待移除

**逐条判断：** from_model_pt 清理。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `146:176`：

> TODO. get rid of from_model_pt

<a id="row-423"></a>
## 423. 23shades-0423-aagifdbgf

**主题代码：** SATD-A

**开放代码：** 方法可见性过宽

**逐条判断：** 应转 private method。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `137:170`：

> TODO. Make this a private method.

<a id="row-424"></a>
## 424. 23shades-0424-aadbacfge

**主题代码：** SATD-A

**开放代码：** 实体职责待迁移

**逐条判断：** ignored entities 移入 core。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `123:161`：

> TODO. Move ignored entities into core.

<a id="row-425"></a>
## 425. 23shades-0425-aadbacfde

**主题代码：** SATD-G

**开放代码：** 搜索复杂度待改善

**逐条判断：** 当前 O(N)，改善方向未完整给出。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `134:156`：

> TODO. O(N) now; search

<a id="row-426"></a>
## 426. 23shades-0426-aagdeighd

**主题代码：** SATD-U

**开放代码：** 证据不足

**逐条判断：** 空 TODO。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `119:124`：

> TODO:

<a id="row-427"></a>
## 427. 23shades-0427-aajdaiegb

**主题代码：** SATD-U

**开放代码：** 证据不足

**逐条判断：** 空 TODO。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `209:214`：

> TODO:

<a id="row-428"></a>
## 428. 23shades-0428-aaeabafjh

**主题代码：** SATD-U

**开放代码：** 证据不足

**逐条判断：** 空 TODO。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `134:139`：

> TODO:

<a id="row-429"></a>
## 429. 23shades-0429-aaahcadfb

**主题代码：** SATD-U

**开放代码：** 证据不足

**逐条判断：** 空 TODO。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `133:138`：

> TODO:

<a id="row-430"></a>
## 430. 23shades-0430-aagaiecgg

**主题代码：** SATD-U

**开放代码：** 证据不足

**逐条判断：** 空 TODO。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `123:128`：

> TODO:

<a id="row-431"></a>
## 431. 23shades-0431-aahfjddad

**主题代码：** SATD-U

**开放代码：** 证据不足

**逐条判断：** 空 TODO。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `132:137`：

> TODO:

<a id="row-432"></a>
## 432. 23shades-0432-aadghfgba

**主题代码：** SATD-U

**开放代码：** 证据不足

**逐条判断：** 只有 TODO 日期作者信息，无分析内容。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `118:183`：

> TODO:   2014-07-10 16:38:27 by Brian McFee <brm2132@columbia.edu>

<a id="row-433"></a>
## 433. 23shades-0433-aaiiccdhb

**主题代码：** SATD-A

**开放代码：** 跨后端命名一致性

**逐条判断：** 改 stats_fn 对齐 eager/torch。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `129:193`：

> TODO: (sven) rename to simply stats_fn to match eager and torch.

<a id="row-434"></a>
## 434. 23shades-0434-aaifgcjac

**主题代码：** SATD-A, SATD-Q

**开放代码：** 参数获取方案待探索

**逐条判断：** 询问他人更好 ideas，未确认现有错误。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `133:237`：

> TODO: @trask @theo could you take a look at this if you have better ideas on how to get these parameters

<a id="row-435"></a>
## 435. 23shades-0435-aagbbijhe

**主题代码：** SATD-U

**开放代码：** 未定位的指标待办

**逐条判断：** AAM METRIC 未描述欠缺。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `132:148`：

> TODO: AAM METRIC

<a id="row-436"></a>
## 436. 23shades-0436-aafadcigh

**主题代码：** SATD-B, SATD-Q

**开放代码：** 数值准确性改进诉求

**逐条判断：** accurate Value，但对象不明。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `140:160`：

> todo: accurate Value

<a id="row-437"></a>
## 437. 23shades-0437-aaeacgafj

**主题代码：** SATD-D, SATD-E, SATD-O

**开放代码：** 多分类特征重要性展示缺失

**逐条判断：** 明确 visualization 尚需实现。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `117:199`：

> TODO: Actually implement feature importance visualization for multiclass problems.

<a id="row-438"></a>
## 438. 23shades-0438-aaaifiggc

**主题代码：** SATD-Q

**开放代码：** 路径适配待办

**逐条判断：** adapt path 未提供平台或结构。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `132:148`：

> TODO: adapt path

<a id="row-439"></a>
## 439. 23shades-0439-aaeeicdeh

**主题代码：** SATD-C, SATD-E, SATD-I, SATD-Q

**开放代码：** 音频窗口覆盖不足疑问

**逐条判断：** 考虑完整 frame_size 覆盖 whole audio signal。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `110:175`：

> TODO: add a complete frame_size; to cover the whole audio signal?

<a id="row-440"></a>
## 440. 23shades-0440-aajaijffg

**主题代码：** SATD-K

**开放代码：** 特定参数分支测试缺失

**逐条判断：** ignore_sep=False 测试。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `141:178`：

> TODO: Add a test for ignore_sep=False

<a id="row-441"></a>
## 441. 23shades-0441-aaefegech

**主题代码：** SATD-D, SATD-E, SATD-O

**开放代码：** 绘图接口扩展

**逐条判断：** 支持 predefined axes。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `118:177`：

> TODO: Add ability to handle a pre-defined axes for plotting

<a id="row-442"></a>
## 442. 23shades-0442-aabgdbaje

**主题代码：** SATD-D

**开放代码：** 反向图像处理范围待补

**逐条判断：** add backward images，未推断训练用途。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `122:153`：

> TODO: add backward images also.

<a id="row-443"></a>
## 443. 23shades-0443-aaeabdbie

**主题代码：** SATD-D

**开放代码：** 过滤字段引用缺失

**逐条判断：** data table ref 待加。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `157:202`：

> TODO: Add data table ref in fields of filters

<a id="row-444"></a>
## 444. 23shades-0444-aaeabdbjb

**主题代码：** SATD-D

**开放代码：** 过滤字段引用缺失

**逐条判断：** 重复文本独立保留。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `154:199`：

> TODO: Add data table ref in fields of filters

<a id="row-445"></a>
## 445. 23shades-0445-aaeaacdga

**主题代码：** SATD-D

**开放代码：** 日期类型转换缺失

**逐条判断：** 原文 datetype conversion。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `121:150`：

> TODO: add datetype conversion

<a id="row-446"></a>
## 446. 23shades-0446-aaedjcbec

**主题代码：** SATD-A, SATD-F

**开放代码：** 抽象继承依赖上游实现

**逐条判断：** Graph 完成后增加继承。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `116:165`：

> TODO: add inheritance from Graph once implemented

<a id="row-447"></a>
## 447. 23shades-0447-aaecjghji

**主题代码：** SATD-D, SATD-E

**开放代码：** 估计器元标签不全

**逐条判断：** 依 scikit-learn 补 tags。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `139:184`：

> TODO: add more tags based on the scikit-learn

<a id="row-448"></a>
## 448. 23shades-0448-aafhedifh

**主题代码：** SATD-D

**开放代码：** 命令行操作缺失

**逐条判断：** set-name/rename/delete 子命令待加。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `135:185`：

> TODO: add set-name (or rename); delete subcommands

<a id="row-449"></a>
## 449. 23shades-0449-aajdcigce

**主题代码：** SATD-D, SATD-J

**开放代码：** 配置体系集成缺失

**逐条判断：** 当前功能需纳入 configuration framework。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `129:170`：

> TODO: Add this to configuration framework

<a id="row-450"></a>
## 450. 23shades-0450-aaegfadac

**主题代码：** SATD-E, SATD-I, SATD-J

**开放代码：** 初始化策略缺少选择权

**逐条判断：** LSUV 不总更好，需 toggle；保留 empirical seems。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `127:190`：

> TODO: Add toggle for the LSUV init. It seems not always better!

<a id="row-451"></a>
## 451. 23shades-0451-aaifgfeag

**主题代码：** SATD-B, SATD-C, SATD-Q

**开放代码：** 梯度处理遗漏疑问

**逐条判断：** and the grad 问句不能定位公式。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `133:153`：

> TODO: and the grad ?

<a id="row-452"></a>
## 452. 23shades-0452-aajefhbah

**主题代码：** SATD-H, SATD-I, SATD-J

**开放代码：** 任意阈值不可靠

**逐条判断：** 明确 arbitrary threshold problematic。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `120:160`：

> TODO: arbitrary threshold is problematic

<a id="row-453"></a>
## 453. 23shades-0453-aaefagffe

**主题代码：** SATD-E, SATD-F, SATD-K

**开放代码：** 跨版本测试兼容

**逐条判断：** assertWarns 仅 Python3.2+，需各版测试。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `113:179`：

> TODO: assertWarns exist only for Python 3.2+; test in all versions

<a id="row-454"></a>
## 454. 23shades-0454-aaefgiijg

**主题代码：** SATD-E

**开放代码：** 模型族支持局限

**逐条判断：** LHUC 当前 RNN-specific，应扩展其他模型。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `116:197`：

> TODO: At the moment LHUC is RNN specific. We should support other models as well.

<a id="row-455"></a>
## 455. 23shades-0455-aaeiibiib

**主题代码：** SATD-D, SATD-E

**开放代码：** 数据类型推断缺失

**逐条判断：** 自动 detect dtype。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `122:145`：

> TODO: auto detect dtype

<a id="row-456"></a>
## 456. 23shades-0456-aaicfaced

**主题代码：** SATD-E

**开放代码：** 稀疏格式强制转换待避免

**逐条判断：** 为避免 CSR 转换需增加支持，目标格式截断。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `134:204`：

> TODO: avoid conversion of sparse matrices to CSR by adding support for

<a id="row-457"></a>
## 457. 23shades-0457-aaeiecejb

**主题代码：** SATD-G

**开放代码：** 可省略计算未优化

**逐条判断：** no center/large 1D_Block 等明显情况避免 reduce。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `120:190`：

> TODO: avoid reduce for obvious cases like no center and large 1D_Block

<a id="row-458"></a>
## 458. 23shades-0458-aaeggadce

**主题代码：** SATD-F, SATD-H, SATD-M

**开放代码：** 依赖泛型限制的临时绕行

**逐条判断：** pydantic generic types hack 预计下版移除。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `111:187`：

> TODO: Bad hack to work around generic types in pydantic (until next release)

<a id="row-459"></a>
## 459. 23shades-0459-aafafahih

**主题代码：** SATD-A, SATD-K

**开放代码：** 测试实现重复

**逐条判断：** 除 repeated KFold 外与另一测试基本相同。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `198:285`：

> TODO: Basically identical to `test_intra_cv_target_transform` except for repeated KFold

<a id="row-460"></a>
## 460. 23shades-0460-aagfecjfe

**主题代码：** SATD-B, SATD-E, SATD-I

**开放代码：** 批次变长序列假设风险

**逐条判断：** batch 可能不同 sequence lengths，未说明具体处理。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `168:217`：

> TODO: batch might have different sequence lengths

<a id="row-461"></a>
## 461. 23shades-0461-aaidhjgaj

**主题代码：** SATD-D, SATD-O

**开放代码：** 绘图轴共享自动化缺失

**逐条判断：** shareX 自动化待办。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `159:203`：

> TODO: Be able to automatize the shareX thing

<a id="row-462"></a>
## 462. 23shades-0462-aadehggdg

**主题代码：** SATD-Q, SATD-U

**开放代码：** 行为改善诉求不具体

**逐条判断：** unchanged 可 improve，无法定位机制。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `181:228`：

> TODO: behavior is unchanged. Could be improved.

<a id="row-463"></a>
## 463. 23shades-0463-aaejdhjid

**主题代码：** SATD-U

**开放代码：** 未定位的攻击相关待办

**逐条判断：** black box attacks 没有具体实现或防御要求。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `156:179`：

> TODO: black box attacks

<a id="row-464"></a>
## 464. 23shades-0464-aaijbfccj

**主题代码：** SATD-G

**开放代码：** 计算图重复拆分开销

**逐条判断：** graph break 从 nb_iter 降为 nGPU 次。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `170:233`：

> TODO: Break the graph only nGPU times instead of nb_iter times.

<a id="row-465"></a>
## 465. 23shades-0465-aahddhhhe

**主题代码：** SATD-D

**开放代码：** 子模型构建缺失

**逐条判断：** build child models。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `120:144`：

> TODO: build child models

<a id="row-466"></a>
## 466. 23shades-0466-aahddhiba

**主题代码：** SATD-D

**开放代码：** 模型构建缺失

**逐条判断：** build model。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `125:146`：

> TODO: build the model

<a id="row-467"></a>
## 467. 23shades-0467-aaididaaj

**主题代码：** SATD-Q, SATD-U

**开放代码：** 未定位的修复诉求

**逐条判断：** fix it 没有错误信息。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `140:179`：

> TODO: but seriously; we need to fix it!

<a id="row-468"></a>
## 468. 23shades-0468-aagaidebh

**主题代码：** SATD-D

**开放代码：** 几何量计算缺失

**逐条判断：** centroid 待算。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `126:157`：

> TODO: calculate this centroid\"

<a id="row-469"></a>
## 469. 23shades-0469-aaahbfbig

**主题代码：** SATD-D

**开放代码：** 校准数据准备待办

**逐条判断：** calibration dataset，无更多要求。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `123:148`：

> TODO: calibration dataset

<a id="row-470"></a>
## 470. 23shades-0470-aaedhgdgd

**主题代码：** SATD-A, SATD-Q

**开放代码：** 实现位置待调整

**逐条判断：** 询问能否 move up。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `123:150`：

> TODO: Can this be moved up?

<a id="row-471"></a>
## 471. 23shades-0471-aageachcc

**主题代码：** SATD-A, SATD-Q

**开放代码：** 缺失特征处理策略替换

**逐条判断：** feature_na_method 待 change，不推断缺失值具体策略。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `138:173`：

> todo: change the feature_na_method!

<a id="row-472"></a>
## 472. 23shades-0472-aaffdcfdh

**主题代码：** SATD-A

**开放代码：** 优化器抽象选择不当

**逐条判断：** 应改 appropriate Optimizer class。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `111:172`：

> TODO: Change the optimizer to the appropriate Optimizer class

<a id="row-473"></a>
## 473. 23shades-0473-aagacefai

**主题代码：** SATD-A, SATD-Q

**开放代码：** 常量/符号复用

**逐条判断：** 改用 parser_utils 提供变量。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `140:195`：

> TODO: change the symbol to a variable from parser_utils

<a id="row-474"></a>
## 474. 23shades-0474-aaeebgdbh

**主题代码：** SATD-A, SATD-F, SATD-Q

**开放代码：** 外部格式能力成熟后替换逻辑

**逐条判断：** git pretty-format 是变更条件。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `109:166`：

> TODO: change this logic when there is a git pretty-format

<a id="row-475"></a>
## 475. 23shades-0475-aahjabdbh

**主题代码：** SATD-C, SATD-I, SATD-J, SATD-Q

**开放代码：** 有限值约束待启用

**逐条判断：** finite=True 拟调整。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `119:153`：

> TODO: Change this to finite = True

<a id="row-476"></a>
## 476. 23shades-0476-aaeigccaj

**主题代码：** SATD-C, SATD-F

**开放代码：** 循环导入阻碍类型验证

**逐条判断：** SeriesType 循环 import 修复后检查 other 为 Series。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `149:222`：

> TODO: check `other` is Series after a circular import of SeriesType fixed

<a id="row-477"></a>
## 477. 23shades-0477-aafibaccg

**主题代码：** SATD-C, SATD-E, SATD-K, SATD-Q

**开放代码：** 文件输入特殊形式未验证

**逐条判断：** single mrc file 无 @ 时需检查行为。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `150:208`：

> TODO: Check behavior if this is a single mrc file (no '@')

<a id="row-478"></a>
## 478. 23shades-0478-aahdfbbhc

**主题代码：** SATD-C

**开放代码：** 大小写等价检查缺失

**逐条判断：** 保存前按 lowercase 检查大写词。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `125:200`：

> TODO: check CAPTALIZED WORDS as their lower case counterparts before saving

<a id="row-479"></a>
## 479. 23shades-0479-aahhdgbbd

**主题代码：** SATD-C, SATD-K, SATD-Q

**开放代码：** 数学映射参数待验证

**逐条判断：** exp map params 需检查。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `113:139`：

> TODO: Check exp map params

<a id="row-480"></a>
## 480. 23shades-0480-aaeiedgfj

**主题代码：** SATD-C

**开放代码：** 错误检查缺失

**逐条判断：** check for errors 未具体化。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `118:140`：

> TODO: check for errors

<a id="row-481"></a>
## 481. 23shades-0481-aaeifhdjh

**主题代码：** SATD-C, SATD-E

**开放代码：** 输入容器类型检查缺失

**逐条判断：** series/dict/list 检查。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `139:179`：

> TODO: check for series\/dict\/list input

<a id="row-482"></a>
## 482. 23shades-0482-aaebhaafj

**主题代码：** SATD-C

**开放代码：** 生命周期状态检查缺失

**逐条判断：** owner 是否正在 deleting。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `152:185`：

> TODO: Check if owner is deleting.

<a id="row-483"></a>
## 483. 23shades-0483-aagbdjfdj

**主题代码：** SATD-A, SATD-Q

**开放代码：** 已有误差计算方法复用待查

**逐条判断：** 考虑 _mean_squared_error_w_precision，未确认等价。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `145:213`：

> TODO: Check if self._mean_squared_error_w_precision can be used here

<a id="row-484"></a>
## 484. 23shades-0484-aabgdhcid

**主题代码：** SATD-B, SATD-I, SATD-K, SATD-Q

**开放代码：** 步幅导致特征对齐风险

**逐条判断：** stride=2 是否造成 alignment issues 需验证。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `122:190`：

> TODO: check if stride of 2 causes alignment issues if the featuremap

<a id="row-485"></a>
## 485. 23shades-0485-aafhihfed

**主题代码：** SATD-C, SATD-Q

**开放代码：** 模型身份检查缺失

**逐条判断：** 是否 QuartzNet 待检查。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `133:175`：

> TODO: check whether the model is QuartzNet

<a id="row-486"></a>
## 486. 23shades-0486-aahfjcfdg

**主题代码：** SATD-L, SATD-Q

**开放代码：** 条件分支必要性不明

**逐条判断：** 需解释 IF 的原因。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `133:162`：

> TODO: check why there's an IF

<a id="row-487"></a>
## 487. 23shades-0487-aahgfihag

**主题代码：** SATD-A

**开放代码：** 初始化代码清理

**逐条判断：** 明确 clean up。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `113:148`：

> TODO: clean up these initialization

<a id="row-488"></a>
## 488. 23shades-0488-aaahbjgif

**主题代码：** SATD-D

**开放代码：** 几何边界裁剪缺失

**逐条判断：** clip polygons 待办。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `127:146`：

> TODO: clip polygons

<a id="row-489"></a>
## 489. 23shades-0489-aaiiigjef

**主题代码：** SATD-U

**开放代码：** 后端实现待办不具体

**逐条判断：** CntkEmit 名称不足以判断功能。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `129:143`：

> TODO: CntkEmit

<a id="row-490"></a>
## 490. 23shades-0490-aaaefgdbc

**主题代码：** SATD-G, SATD-K

**开放代码：** 性能比较缺失

**逐条判断：** 明确 compare performance，未报测量结果。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `133:163`：

> TODO: compare the performance!

<a id="row-491"></a>
## 491. 23shades-0491-aadggcdfe

**主题代码：** SATD-D, SATD-E

**开放代码：** 枚举项不完整

**逐条判断：** complete list，无具体条目。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `121:149`：

> TODO: complete the list here

<a id="row-492"></a>
## 492. 23shades-0492-aafdfijei

**主题代码：** SATD-G

**开放代码：** 重复几何计算待复用

**逐条判断：** video analysis 的 grids 应只计算一次。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `174:241`：

> TODO: compute all the grids etc. once for the video analysis method

<a id="row-493"></a>
## 493. 23shades-0493-aagbjbdaa

**主题代码：** SATD-D

**开放代码：** 几何距离计算缺失

**逐条判断：** walls 间 signed distance。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `136:179`：

> TODO: compute signed distance between walls

<a id="row-494"></a>
## 494. 23shades-0494-aajfbgjhi

**主题代码：** SATD-A, SATD-G

**开放代码：** 配置重复加载

**逐条判断：** config 在多个文件也应只 load once。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `112:191`：

> TODO: config should only be loaded once (also in database.py and enter_data.py)

<a id="row-495"></a>
## 495. 23shades-0495-aafjhfhii

**主题代码：** SATD-D, SATD-E

**开放代码：** 文本过滤词表扩展

**逐条判断：** blacklist 拟加入 discussion on/of。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `135:205`：

> TODO: Consider adding terms to blacklist: discussion on; discussion of

<a id="row-496"></a>
## 496. 23shades-0496-aaeedfhcd

**主题代码：** SATD-A, SATD-I, SATD-Q

**开放代码：** 决策策略待考虑

**逐条判断：** go/no-go 的 modification 未显示。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `139:191`：

> ToDo: consider go\/no-go with following modification

<a id="row-497"></a>
## 497. 23shades-0497-aaeidiecf

**主题代码：** SATD-C, SATD-I, SATD-Q

**开放代码：** 同名键冲突边界

**逐条判断：** 同名 keys 与带 suffix columns 需考虑。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `117:169`：

> TODO: consider keys with same name; cols with suffix

<a id="row-498"></a>
## 498. 23shades-0498-aagbggddc

**主题代码：** SATD-E

**开放代码：** 平台版本识别粒度不足

**逐条判断：** OS release extraction 需更细。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `117:167`：

> TODO: consider more granular OS release extraction

<a id="row-499"></a>
## 499. 23shades-0499-aadajcbia

**主题代码：** SATD-A, SATD-E, SATD-F

**开放代码：** 框架扩展受实现语言限制

**逐条判断：** MXNet 注册 activation 似需 C++；考虑向上游贡献。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `117:230`：

> TODO: Contribute these to MXNet?  For now it appears that registered activation types must be implemented in C++.

<a id="row-500"></a>
## 500. 23shades-0500-aaeiedggi

**主题代码：** SATD-A, SATD-Q

**开放代码：** 类型转换需求待确认

**逐条判断：** 是否类似 IntegerLiteral conversion。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `109:153`：

> TODO: conversion needed like IntegerLiteral?

<a id="row-501"></a>
## 501. 23shades-0501-aaedhahfd

**主题代码：** SATD-A, SATD-J, SATD-Q

**开放代码：** 优化选项需求待定

**逐条判断：** LK 可否加入 optimization option，未确认必要性。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `122:180`：

> TODO: Could be implemented as optimization option in LK???

<a id="row-502"></a>
## 502. 23shades-0502-aaidjgfeg

**主题代码：** SATD-A, SATD-K, SATD-N, SATD-Q

**开放代码：** 格式类型信息保存待验证

**逐条判断：** QSettings.Format 是否保留 type info。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `126:181`：

> TODO: Could check if QSettings.Format stores type info.

<a id="row-503"></a>
## 503. 23shades-0503-aadgffbjj

**主题代码：** SATD-U

**开放代码：** 截断证据

**逐条判断：** upregulation 的后续转换和问题未给。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `126:185`：

> TODO: Currently this turns any upregulation associated with

<a id="row-504"></a>
## 504. 23shades-0504-aagbbijce

**主题代码：** SATD-I, SATD-Q

**开放代码：** 数据划分使用待调整

**逐条判断：** 目前用 train dataset，未给目标用途；不能据此断言测试泄漏。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `121:157`：

> TO-DO: currently uses train datatset

<a id="row-505"></a>
## 505. 23shades-0505-aadgfccbh

**主题代码：** SATD-D, SATD-Q

**开放代码：** 源文本证据未利用

**逐条判断：** 当前不看 source text，作者考虑加入。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `132:196`：

> TODO: Currently we don't look at source text; but we may want to

<a id="row-506"></a>
## 506. 23shades-0506-aaeieejja

**主题代码：** SATD-A, SATD-Q

**开放代码：** 入参必要性待定

**逐条判断：** dataframe 是否必须传入。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `112:140`：

> TODO: dataframe pass needed?

<a id="row-507"></a>
## 507. 23shades-0507-aafbciiij

**主题代码：** SATD-B, SATD-Q

**开放代码：** 图像格式判断不恰当

**逐条判断：** PNG/JPEG 可能不应按 RAW 处理，作者有不确定性。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `114:184`：

> TODO: deal with png and jpeg files better - they are probably not RAW.

<a id="row-508"></a>
## 508. 23shades-0508-aafhhaijc

**主题代码：** SATD-B, SATD-Q

**开放代码：** 默认值行为待调试

**逐条判断：** defaults 问题未具体列出。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `131:152`：

> TODO: Debug defaults.

<a id="row-509"></a>
## 509. 23shades-0509-aaacggdch

**主题代码：** SATD-A, SATD-M, SATD-Q

**开放代码：** 中间逻辑可省略待决策

**逐条判断：** 可直接传 plot_lr_finders，是否保留未定。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `140:212`：

> TODO: Decide on whether to keep this; could just pass to plot_lr_finders

<a id="row-510"></a>
## 510. 23shades-0510-aadjgaaid

**主题代码：** SATD-D, SATD-E

**开放代码：** 并行机制接口缺失

**逐条判断：** decorator params 需支持 threads/processes/async 等方案。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `133:227`：

> TODO: decorator params: parallelization (e.g. threads; processes; async\/await; greenlets;...)

<a id="row-511"></a>
## 511. 23shades-0511-aahidaefh

**主题代码：** SATD-A, SATD-F

**开放代码：** 分布式组件与调度器耦合

**逐条判断：** DDP 从 SLURM 解耦。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `176:205`：

> TODO: decouple DDP from SLURM

<a id="row-512"></a>
## 512. 23shades-0512-aaicabdbe

**主题代码：** SATD-B, SATD-D

**开放代码：** 训练测试目标变量缺失

**逐条判断：** y_train/y_test 未定义；不是单元测试欠缺。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `151:196`：

> TODO: define variables 'y_train' and 'y_test'

<a id="row-513"></a>
## 513. 23shades-0513-aajfeejjg

**主题代码：** SATD-M

**开放代码：** 过时方法清理

**逐条判断：** 无需求后 delete method。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `130:176`：

> TODO: delete this method when no longer needed

<a id="row-514"></a>
## 514. 23shades-0514-aaaggiije

**主题代码：** SATD-M, SATD-Q

**开放代码：** 废弃决定未作出

**逐条判断：** deprecate 问句。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `147:163`：

> TODO: deprecate?

<a id="row-515"></a>
## 515. 23shades-0515-aaegihjhc

**主题代码：** SATD-I, SATD-Q

**开放代码：** 语义一致约束可能过严

**逐条判断：** same sense 要求是否 too strict 的意思，原文 typo/string 且截断，保留疑问。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `135:194`：

> TODO: determine if requiring same sense is too string; i.e.

<a id="row-516"></a>
## 516. 23shades-0516-aajegiabc

**主题代码：** SATD-D, SATD-I, SATD-J, SATD-Q

**开放代码：** 模型默认值推断不佳

**逐条判断：** 需更好 guess defaults。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `141:198`：

> TODO: Do a better job of guessing defaults from the model

<a id="row-517"></a>
## 517. 23shades-0517-aafafcgbj

**主题代码：** SATD-B, SATD-C, SATD-I, SATD-Q

**开放代码：** 混合数据统计有效性存疑

**逐条判断：** opt.yi 可能含 times，直接 min/max/mean 需核实。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `184:292`：

> TODO: Do below `y_lie` lines directly calculate min\/max\/mean on `opt.yi` when it could also contain times?

<a id="row-518"></a>
## 518. 23shades-0518-aaaegjcch

**主题代码：** SATD-C, SATD-G

**开放代码：** 竞态防护不足

**逐条判断：** 需要更强保护，file lock 是候选。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `195:255`：

> TODO: do more to protect against race conditions. File lock?

<a id="row-519"></a>
## 519. 23shades-0519-aajfiibhb

**主题代码：** SATD-D, SATD-J

**开放代码：** 替换行为过于主动；文本范围选项缺失

**逐条判断：** 未明确许可不替换，同时添加 only hangul。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `116:189`：

> TODO: do not replace unless explicitly noticed + add 'only hangul' option

<a id="row-520"></a>
## 520. 23shades-0520-aajddbihf

**主题代码：** SATD-K, SATD-Q

**开放代码：** 评估工作未完成

**逐条判断：** do some evaluation 无特定指标。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `135:160`：

> TODO: do some evaluation.

<a id="row-521"></a>
## 521. 23shades-0521-aaiiiajei

**主题代码：** SATD-A

**开放代码：** 预处理职责位置待调整

**逐条判断：** transpose 移至 DataLoaderTransformer，不在 host 执行。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `127:195`：

> TODO: do the transpose as a DataLoaderTransformer instead of in host

<a id="row-522"></a>
## 522. 23shades-0522-aaadihacg

**主题代码：** SATD-Q, SATD-U

**开放代码：** 改进诉求不具体

**逐条判断：** do this better 无对象。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `135:155`：

> TODO: do this better

<a id="row-523"></a>
## 523. 23shades-0523-aaiecehba

**主题代码：** SATD-Q

**开放代码：** 必要性待决策

**逐条判断：** 不确定是否需要。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `141:164`：

> TODO: do we need this?!

<a id="row-524"></a>
## 524. 23shades-0524-aaifeicfh

**主题代码：** SATD-L

**开放代码：** 文档字符串缺失

**逐条判断：** 明确 docstring。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `124:139`：

> TODO: docstring

<a id="row-525"></a>
## 525. 23shades-0525-aajbigiad

**主题代码：** SATD-K, SATD-Q

**开放代码：** 计算图生成行为待查

**逐条判断：** 问是否 make graph，未确认缺陷。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `134:159`：

> TODO: does it make graph?

<a id="row-526"></a>
## 526. 23shades-0526-aagejejha

**主题代码：** SATD-A, SATD-I, SATD-J, SATD-Q

**开放代码：** 初始化方式待调整

**逐条判断：** 不应 constant initializer，原因截断。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `126:182`：

> TODO: don't make these a constant initializer because we

<a id="row-527"></a>
## 527. 23shades-0527-aahddidfd

**主题代码：** SATD-K, SATD-M

**开放代码：** 测试框架迁移后冗余

**逐条判断：** py.test 下不需要此逻辑。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `133:166`：

> TODO: don't need this w\/ py.test

<a id="row-528"></a>
## 528. 23shades-0528-aagejdfdj

**主题代码：** SATD-F, SATD-K, SATD-Q

**开放代码：** 版本条件假设需复验

**逐条判断：** 核实在1.9.0仍成立，不臆测库。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `121:170`：

> TODO: double check if this is still true in 1.9.0

<a id="row-529"></a>
## 529. 23shades-0529-aaeieeeje

**主题代码：** SATD-U

**开放代码：** 类型相关待办不具体

**逐条判断：** dtype 单词未给修改。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `119:130`：

> TODO: dtype

<a id="row-530"></a>
## 530. 23shades-0530-aajacfjji

**主题代码：** SATD-U

**开放代码：** 条件性切换证据截断

**逐条判断：** 待 once 条件满足启用下一行，但条件缺失。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `139:187`：

> todo: enable the following line instead once the

<a id="row-531"></a>
## 531. 23shades-0531-aaffefcib

**主题代码：** SATD-C, SATD-I, SATD-J, SATD-Q

**开放代码：** 缺失值编码配置待确认

**逐条判断：** dummy_na=False 是否符合预期。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `140:185`：

> TODO: ensure dummy_na =False is what you want

<a id="row-532"></a>
## 532. 23shades-0532-aahddjbah

**主题代码：** SATD-C, SATD-I

**开放代码：** 模型拟合输入形状契约

**逐条判断：** fit 时 x 必须匹配 model placeholder shape。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `134:202`：

> TODO: ensure x data shape matches model._ph['x'] shape (only if fit)

<a id="row-533"></a>
## 533. 23shades-0533-aahdfajdh

**主题代码：** SATD-D

**开放代码：** 语言词表/上下文扩展

**逐条判断：** 对周边常用词扩展 proper nouns，策略不完整。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `125:179`：

> TODO: EXPAND PROPER NOUNS FOR COMMON WORDS AROUND WORD

<a id="row-534"></a>
## 534. 23shades-0534-aaeebgfej

**主题代码：** SATD-D, SATD-I, SATD-J, SATD-Q

**开放代码：** 模型深度实验待开展

**逐条判断：** 尝试更多 layers，非已确认结构缺失。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `134:167`：

> TODO: experiment with more layers

<a id="row-535"></a>
## 535. 23shades-0535-aaebchhbi

**主题代码：** SATD-D, SATD-E

**开放代码：** 多保真问题支持扩展

**逐条判断：** 通过 training_points approx 扩展。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `137:218`：

> TODO: Extend to multifidelity problems by adding training_points = {'approx': {}}

<a id="row-536"></a>
## 536. 23shades-0536-aaeidieej

**主题代码：** SATD-D, SATD-E

**开放代码：** 键类型覆盖不全

**逐条判断：** other key types 待支持。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `117:148`：

> TODO: extend to other key types

<a id="row-537"></a>
## 537. 23shades-0537-aaeidjjhd

**主题代码：** SATD-C, SATD-I

**开放代码：** 评估函数提取脆弱

**逐条判断：** 要求更 robust 的 extraction。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `122:162`：

> TODO: extract an eval func more robustly

<a id="row-538"></a>
## 538. 23shades-0538-aafibegcj

**主题代码：** SATD-I, SATD-L, SATD-Q

**开放代码：** 张量运算形状语义不明

**逐条判断：** einsum 结果为何需 reshape。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `146:208`：

> TODO: figure out how why the result of einsum requires reshape

<a id="row-539"></a>
## 539. 23shades-0539-aaheefgfd

**主题代码：** SATD-B, SATD-Q

**开放代码：** 空文档返回原因待查

**逐条判断：** 实际异常行为明确但根因未知。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `116:173`：

> TODO: figure out while empty documents are being returned

<a id="row-540"></a>
## 540. 23shades-0540-aaifgecfh

**主题代码：** SATD-Q

**开放代码：** 机器差异行为待解释

**逐条判断：** 不同 machines 偏好不同 options，未给平台原因。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `115:177`：

> TODO: figure out why some machines prefer one of these options

<a id="row-541"></a>
## 541. 23shades-0541-aahafiegd

**主题代码：** SATD-Q, SATD-U

**开放代码：** 原因待查但事件缺失

**逐条判断：** this happens 没有指代。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `126:160`：

> TODO: figure out why this happens.

<a id="row-542"></a>
## 542. 23shades-0542-aagbabhfa

**主题代码：** SATD-D

**开放代码：** 实现未完成

**逐条判断：** finish this，无对象。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `115:132`：

> TODO: finish this

<a id="row-543"></a>
## 543. 23shades-0543-aahggbife

**主题代码：** SATD-B, SATD-F, SATD-K

**开放代码：** 估计器契约检查失败

**逐条判断：** AutoEncoder estimator check 待修。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `119:160`：

> TODO: fix estimator check for AutoEncoder

<a id="row-544"></a>
## 544. 23shades-0544-aaedabagi

**主题代码：** SATD-B

**开放代码：** 文本读取行为缺陷

**逐条判断：** read whole wiki 需要 fix，失败细节不明。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `114:139`：

> TODO: fix read whole wiki

<a id="row-545"></a>
## 545. 23shades-0545-aafbccaac

**主题代码：** SATD-Q, SATD-U

**开放代码：** 未定位的修复诉求

**逐条判断：** fix later，无具体错误。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `142:162`：

> TODO: fix this later

<a id="row-546"></a>
## 546. 23shades-0546-aaiejgdgf

**主题代码：** SATD-D, SATD-N

**开放代码：** 持久化格式策略待调整

**逐条判断：** 应保存全部 materialized formats，而非指定格式。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `114:193`：

> TODO: Formats should not be specified; just saving all the materialized formats

<a id="row-547"></a>
## 547. 23shades-0547-aahjacjjf

**主题代码：** SATD-M

**开放代码：** 清理待办

**逐条判断：** get rid of this。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `134:155`：

> TODO: Get rid of this

<a id="row-548"></a>
## 548. 23shades-0548-aajgceiba

**主题代码：** SATD-D, SATD-E

**开放代码：** 参数元组支持缺失

**逐条判断：** arg tuples 待处理。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `146:169`：

> TODO: handle arg tuples

<a id="row-549"></a>
## 549. 23shades-0549-aaeieddbj

**主题代码：** SATD-B, SATD-C

**开放代码：** 布尔标量处理不正确

**逐条判断：** properly 表示现有不充分。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `109:146`：

> TODO: handle boolean scalars properly

<a id="row-550"></a>
## 550. 23shades-0550-aaahcdafe

**主题代码：** SATD-D, SATD-E

**开放代码：** 通道模态处理推迟

**逐条判断：** channel modalities later。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `138:175`：

> TODO: handle channel modalities later

<a id="row-551"></a>
## 551. 23shades-0551-aajdbhhhh

**主题代码：** SATD-D, SATD-E

**开放代码：** 多说话者支持缺失

**逐条判断：** multi-speaker。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `133:159`：

> TODO: handle multi-speaker

<a id="row-552"></a>
## 552. 23shades-0552-aabfjgehb

**主题代码：** SATD-C

**开放代码：** 空值边界处理缺失

**逐条判断：** Nones。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `125:143`：

> TODO: handle Nones

<a id="row-553"></a>
## 553. 23shades-0553-aadgfdibb

**主题代码：** SATD-D, SATD-E

**开放代码：** 参与者类型覆盖不全

**逐条判断：** other participant types。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `137:173`：

> TODO: handle other participant types

<a id="row-554"></a>
## 554. 23shades-0554-aahjdcjgg

**主题代码：** SATD-B, SATD-C, SATD-E

**开放代码：** 列表记录值缺乏处理与拒绝

**逐条判断：** 至少应报错，而非无定义行为。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `145:202`：

> TODO: handle record value which are lists; at least error

<a id="row-555"></a>
## 555. 23shades-0555-aaeidjhhg

**主题代码：** SATD-D, SATD-E

**开放代码：** 字符串输入处理缺失

**逐条判断：** handle string。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `122:141`：

> TODO: handle string

<a id="row-556"></a>
## 556. 23shades-0556-aadhfidia

**主题代码：** SATD-A, SATD-H, SATD-J, SATD-Q

**开放代码：** 硬编码提取方案待替代

**逐条判断：** 当前 hard coded，寻找更好 extraction。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `132:195`：

> TODO: hard coded for now; looking for better extraction methods

<a id="row-557"></a>
## 557. 23shades-0557-aajejbfha

**主题代码：** SATD-A, SATD-H, SATD-J

**开放代码：** 重复魔数待清理

**逐条判断：** 各处999需更清晰方案。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `125:202`：

> TODO: here; and every time we use this 999 number; find a cleaner\/better way

<a id="row-558"></a>
## 558. 23shades-0558-aaibihacc

**主题代码：** SATD-M, SATD-Q

**开放代码：** 低使用率逻辑必要性存疑

**逐条判断：** believe not much used，不等于已确定可删。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `126:170`：

> TODO: I believe this is not really much used

<a id="row-559"></a>
## 559. 23shades-0559-aafdibbge

**主题代码：** SATD-B, SATD-I, SATD-Q

**开放代码：** 结果质量不足

**逐条判断：** 尚未得到 good results，未指定测量或原因。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `119:164`：

> TODO: I cannot get good results with this yet

<a id="row-560"></a>
## 560. 23shades-0560-aaifhghej

**主题代码：** SATD-F

**开放代码：** 导入问题未解决

**逐条判断：** 作者无法处理 import issue。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `151:198`：

> TODO: I can't manage the import issue; can you?

<a id="row-561"></a>
## 561. 23shades-0561-aaegihffd

**主题代码：** SATD-A, SATD-Q

**开放代码：** 语言检测器选择待比较

**逐条判断：** 寻找 OSS Python 最优 detector，未给标准。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `124:194`：

> TODO: identify the \"best\" language detector available for OSS python

<a id="row-562"></a>
## 562. 23shades-0562-aaeiefhcb

**主题代码：** SATD-C, SATD-E

**开放代码：** 非数值输入过滤缺失

**逐条判断：** ignore non-numerics。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `129:154`：

> TODO: ignore non-numerics

<a id="row-563"></a>
## 563. 23shades-0563-aafihcach

**主题代码：** SATD-Q, SATD-U

**开放代码：** 局部实现理解不确定

**逐条判断：** not sure，缺少对象。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `132:166`：

> TODO: I'm not sure about this part

<a id="row-564"></a>
## 564. 23shades-0564-aafjicajb

**主题代码：** SATD-D

**开放代码：** 卷积转置算子缺失

**逐条判断：** Conv Transpose 待实现。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `140:170`：

> TODO: Implement Conv Transpose

<a id="row-565"></a>
## 565. 23shades-0565-aajfdefij

**主题代码：** SATD-D

**开放代码：** 分析方法集成缺失

**逐条判断：** diffxpy method 待实现。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `118:148`：

> TODO: implement diffxpy method

<a id="row-566"></a>
## 566. 23shades-0566-aaiffabhh

**主题代码：** SATD-A, SATD-D

**开放代码：** 方法实现缺失；可维护性重构

**逐条判断：** get_owners 待实现并重构漂亮些。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `116:175`：

> TODO: Implement get_owners and refactor to make it prettier

<a id="row-567"></a>
## 567. 23shades-0567-aadbcjbcc

**主题代码：** SATD-C

**开放代码：** 批量下载限流处理缺失

**逐条判断：** 429 时需要 cool-off。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `139:211`：

> TODO: Implement mass downloading with a cool-off in case of 429 response

<a id="row-568"></a>
## 568. 23shades-0568-aafbihhej

**主题代码：** SATD-D

**开放代码：** 范围功能缺失

**逐条判断：** ranges 待实现，具体类型不明。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `150:172`：

> TODO: Implement ranges

<a id="row-569"></a>
## 569. 23shades-0569-aahhhfjei

**主题代码：** SATD-D, SATD-J

**开放代码：** 必需参数支持缺失

**逐条判断：** required params 待实现。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `130:161`：

> TODO: implement required params

<a id="row-570"></a>
## 570. 23shades-0570-aagaghfef

**主题代码：** SATD-D

**开放代码：** 模型残差连接缺失

**逐条判断：** 明确 residual connection。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `119:154`：

> TODO: implement residual connection

<a id="row-571"></a>
## 571. 23shades-0571-aagfabdib

**主题代码：** SATD-K

**开放代码：** 测试实现缺失

**逐条判断：** test_to_set_fw_dic 测试代码待实现。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `142:188`：

> TODO: implement test_to_set_fw_dic() test code

<a id="row-572"></a>
## 572. 23shades-0572-aaachjhaj

**主题代码：** SATD-D

**开放代码：** 功能尚未实现

**逐条判断：** this 未说明对象。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `135:155`：

> TODO: implement this

<a id="row-573"></a>
## 573. 23shades-0573-aaidjgaag

**主题代码：** SATD-U

**开放代码：** 截断证据

**逐条判断：** child 的相关行为未完整给出。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `133:183`：

> TODO: Important because of this any time the child

<a id="row-574"></a>
## 574. 23shades-0574-aaideghdd

**主题代码：** SATD-A, SATD-B, SATD-Q

**开放代码：** 数字解析不完善

**逐条判断：** improve number parsing。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `117:145`：

> TODO: improve number parsing

<a id="row-575"></a>
## 575. 23shades-0575-aaejcccgj

**主题代码：** SATD-A

**开放代码：** 函数式接口不应初始化模块

**逐条判断：** nn.Module 初始化与 functional API 边界冲突。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `116:205`：

> TODO: In terms of functional API; there should not be any initialization of an nn.Module.

<a id="row-576"></a>
## 576. 23shades-0576-aaeihdcgb

**主题代码：** SATD-U

**开放代码：** 未定位的元数据待办

**逐条判断：** index and name 没有具体动作。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `126:146`：

> TODO: index and name

<a id="row-577"></a>
## 577. 23shades-0577-aafjgijbb

**主题代码：** SATD-K

**开放代码：** 索引测试不充分

**逐条判断：** not thoroughly tested。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `129:165`：

> TODO: Indexing not thoroughly tested

<a id="row-578"></a>
## 578. 23shades-0578-aaeiefhaa

**主题代码：** SATD-A

**开放代码：** 变量组织待简化

**逐条判断：** inline freevar，未说明性能作用。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `124:144`：

> TODO: inline freevar

<a id="row-579"></a>
## 579. 23shades-0579-aagcdfcie

**主题代码：** SATD-A, SATD-Q

**开放代码：** 原地操作选择待定

**逐条判断：** inplace 问句。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `135:149`：

> todo: inplace?

<a id="row-580"></a>
## 580. 23shades-0580-aaffdhejj

**主题代码：** SATD-A, SATD-F, SATD-I

**开放代码：** 设备探测路径待改

**逐条判断：** 使用 is_cuda 判断 GPU 可用而非 self.cpu。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `132:199`：

> TODO: Instead of self.cpu(); use is_cuda to know if you can use gpu

<a id="row-581"></a>
## 581. 23shades-0581-aaeieedge

**主题代码：** SATD-A, SATD-M, SATD-Q

**开放代码：** 引用计数必要性待定

**逐条判断：** incref 是否 required。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `119:144`：

> TODO: is incref required?

<a id="row-582"></a>
## 582. 23shades-0582-aagbdibae

**主题代码：** SATD-A, SATD-Q

**开放代码：** 处理方案待评估

**逐条判断：** best way 问句，无对象。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `135:167`：

> TODO: is that best way to handle

<a id="row-583"></a>
## 583. 23shades-0583-aaiecfecg

**主题代码：** SATD-D, SATD-E, SATD-I

**开放代码：** 数据处理范围不足

**逐条判断：** 希望 method 跑 entire data，现有限定对象截断。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `141:211`：

> TODO: It could be nice if this method was run on entire data; not just

<a id="row-584"></a>
## 584. 23shades-0584-aadhccedf

**主题代码：** SATD-G

**开放代码：** 阻塞调用限制

**逐条判断：** 当前 blocking call，未展开并发后果。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `134:161`：

> TODO: it is a blocking call

<a id="row-585"></a>
## 585. 23shades-0585-aadggbdcb

**主题代码：** SATD-L, SATD-O, SATD-Q

**开放代码：** 读取耗时缺少观测

**逐条判断：** 希望知道读取时间，非已经发现慢。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `149:210`：

> TODO: it might be interesting to get the time it took to read

<a id="row-586"></a>
## 586. 23shades-0586-aagdaagij

**主题代码：** SATD-B, SATD-F, SATD-I

**开放代码：** 重训练后恢复正确预处理

**逐条判断：** InceptionResNetV2 重训后切回 correct preprocess_input；有明确前置条件。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `155:261`：

> TODO: it's worth to switch back to the correct preprocess_input when InceptionResNetV2 model is re-trained

<a id="row-587"></a>
## 587. 23shades-0587-aaeiebjie

**主题代码：** SATD-U

**开放代码：** 证据不足

**逐条判断：** list 无动作。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `117:127`：

> TODO: list

<a id="row-588"></a>
## 588. 23shades-0588-aaeiaghhj

**主题代码：** SATD-O

**开放代码：** 日志消息缺失

**逐条判断：** Log message 待办。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `125:142`：

> TODO: Log message

<a id="row-589"></a>
## 589. 23shades-0589-aaeiafbcg

**主题代码：** SATD-O

**开放代码：** 日志等级待调整

**逐条判断：** 拟使用 INFO。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `123:144`：

> TODO: Logg INFO level

<a id="row-590"></a>
## 590. 23shades-0590-aafiggbeh

**主题代码：** SATD-J

**开放代码：** 可配置性不足

**逐条判断：** make configurable，无对象。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `123:146`：

> TODO: make configurable

<a id="row-591"></a>
## 591. 23shades-0591-aajcgfgji

**主题代码：** SATD-G

**开放代码：** 执行效率待改进

**逐条判断：** make efficient，未指出方法。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `166:186`：

> TODO: make efficient

<a id="row-592"></a>
## 592. 23shades-0592-aadageajc

**主题代码：** SATD-G

**开放代码：** 执行效率待改进

**逐条判断：** 重复文本独立保留。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `151:171`：

> TODO: make efficient

<a id="row-593"></a>
## 593. 23shades-0593-aadbehbcf

**主题代码：** SATD-A, SATD-M

**开放代码：** 旧模型路径待去耦/清理

**逐条判断：** make fast_rcnn irrelevant 的方向明确，具体替代未给。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `179:210`：

> TODO: make fast_rcnn irrelevant

<a id="row-594"></a>
## 594. 23shades-0594-aafbjgjcd

**主题代码：** SATD-A, SATD-N

**开放代码：** 压缩输出格式待替换

**逐条判断：** tarfile 改 zipfile。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `115:165`：

> TODO: make it save a zipfile instead of a tarfile.

<a id="row-595"></a>
## 595. 23shades-0595-aafeaijhi

**主题代码：** SATD-I, SATD-J, SATD-Q

**开放代码：** 形状转换缺少选择权

**逐条判断：** clip_to_window 的 reshape 应 option。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `192:246`：

> TODO: make reshape an option for the clip_to_window op

<a id="row-596"></a>
## 596. 23shades-0596-aagbdjhgb

**主题代码：** SATD-C, SATD-I

**开放代码：** 除零边界保护缺失

**逐条判断：** 明确 safe to div by zero。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `151:191`：

> TODO: Make the below safe to div by zero

<a id="row-597"></a>
## 597. 23shades-0597-aaefagbgc

**主题代码：** SATD-I, SATD-J

**开放代码：** 数据类型不可配置

**逐条判断：** dtype 配置见 __init__。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `115:164`：

> TODO: make the dtype configurable; see __init__()

<a id="row-598"></a>
## 598. 23shades-0598-aahiijgjf

**主题代码：** SATD-C

**开放代码：** 异常分类不具体

**逐条判断：** 需 more specific exception。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `133:172`：

> TODO: make this exception more specific

<a id="row-599"></a>
## 599. 23shades-0599-aajajcaie

**主题代码：** SATD-E

**开放代码：** 短列名边界支持缺失

**逐条判断：** 少于三个字符列名需 work。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `148:210`：

> TODO: make this work with col names shorter than three letters

<a id="row-600"></a>
## 600. 23shades-0600-aafhihecd

**主题代码：** SATD-A, SATD-Q

**开放代码：** 池化方案待定

**逐条判断：** maxpool 问句，无上下文。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `140:154`：

> TODO: maxpool?

<a id="row-601"></a>
## 601. 23shades-0601-aahfgdcad

**主题代码：** SATD-K, SATD-Q

**开放代码：** 外部测试复用待评估

**逐条判断：** 考虑 dopamine testStepTrain 等测试。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `145:220`：

> TODO: maybe add testStepTrain (and possibly some other tests) from dopamine

<a id="row-602"></a>
## 602. 23shades-0602-aahidaegb

**主题代码：** SATD-A, SATD-Q

**开放代码：** 缺省环境抽象待考虑

**逐条判断：** DefaultEnvironment 尚为 maybe。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `176:219`：

> TODO: maybe introduce a DefaultEnvironment?

<a id="row-603"></a>
## 603. 23shades-0603-aahgegeef

**主题代码：** SATD-A, SATD-Q

**开放代码：** 结构重构候选

**逐条判断：** maybe refactor，无明确范围。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `138:163`：

> TODO: maybe refactor this

<a id="row-604"></a>
## 604. 23shades-0604-aajcjaefh

**主题代码：** SATD-L, SATD-O, SATD-Q

**开放代码：** 向量长度诊断提示待定

**逐条判断：** message about lengths 问句。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `131:166`：

> TODO: message about vector lengths?

<a id="row-605"></a>
## 605. 23shades-0605-aaeiedgej

**主题代码：** SATD-U

**开放代码：** 证据不足

**逐条判断：** min 无上下文。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `118:127`：

> TODO: min

<a id="row-606"></a>
## 606. 23shades-0606-aahicghci

**主题代码：** SATD-E, SATD-K

**开放代码：** 设备无关测试缺失

**逐条判断：** mock GPU 数以便任意设备运行全部测试。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `144:203`：

> Todo: mock nb Gpus so all these tests can run on any device

<a id="row-607"></a>
## 607. 23shades-0607-aagafeacd

**主题代码：** SATD-I, SATD-Q

**开放代码：** 模型精度待办不具体

**逐条判断：** Model Precision 无测量或改进说明。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `130:151`：

> TODO: Model Precision

<a id="row-608"></a>
## 608. 23shades-0608-aaidfjifi

**主题代码：** SATD-Q, SATD-U

**开放代码：** 证据不足

**逐条判断：** modify later 未给原因。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `209:232`：

> TODO: modify this later

<a id="row-609"></a>
## 609. 23shades-0609-aagcdcjae

**主题代码：** SATD-A, SATD-D, SATD-Q

**开放代码：** 接口签名灵活性不足

**逐条判断：** more flexible signature 是提议。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `127:157`：

> todo: more flexible signature?

<a id="row-610"></a>
## 610. 23shades-0610-aaegfjdjb

**主题代码：** SATD-A, SATD-C, SATD-E, SATD-I, SATD-Q

**开放代码：** 类型约束过宽疑问

**逐条判断：** 是否应 more specific types。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `125:151`：

> TODO: more specific types?

<a id="row-611"></a>
## 611. 23shades-0611-aajejahfe

**主题代码：** SATD-C, SATD-I, SATD-K, SATD-Q

**开放代码：** 验证不足但类型不明

**逐条判断：** more validation 不能推断是数据校验还是模型验证。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `123:144`：

> TODO: more validation

<a id="row-612"></a>
## 612. 23shades-0612-aagfbfdbb

**主题代码：** SATD-A

**开放代码：** 模块职责内聚

**逐条判断：** 移入 corpus module。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `118:150`：

> TODO: move this to corpus module

<a id="row-613"></a>
## 613. 23shades-0613-aadhcgief

**主题代码：** SATD-B, SATD-I, SATD-Q

**开放代码：** 算法实现结果不一致

**逐条判断：** 自有 idf 与对方不完全匹配，未确认哪方正确。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `115:183`：

> TODO: My implementation of idf isn't matching *exactly* with theirs;

<a id="row-614"></a>
## 614. 23shades-0614-aaadihafg

**主题代码：** SATD-Q, SATD-U

**开放代码：** 方案不满意但对象不明

**逐条判断：** need better way。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `139:162`：

> TODO: need a better way

<a id="row-615"></a>
## 615. 23shades-0615-aabgddhjh

**主题代码：** SATD-D, SATD-E

**开放代码：** 绘图能力未支持

**逐条判断：** 函数需改动才能 plotting。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `145:198`：

> TODO: need to change this function to allow plotting.

<a id="row-616"></a>
## 616. 23shades-0616-aafcachjb

**主题代码：** SATD-D

**开放代码：** 动态流水线缺失

**逐条判断：** dynamic pipeline 待定义。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `134:173`：

> TODO: Need to defing a dynamic pipeline

<a id="row-617"></a>
## 617. 23shades-0617-aafigfjii

**主题代码：** SATD-A, SATD-I, SATD-Q

**开放代码：** 设计合法性与适宜性待讨论

**逐条判断：** allowed/smart 尚不明确，不等同法律问题。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `133:189`：

> TODO: need to discuss whether this is 'allowed' or smart

<a id="row-618"></a>
## 618. 23shades-0618-aaebbbhhb

**主题代码：** SATD-B

**开放代码：** 坐标变换方向错误

**逐条判断：** 需 CameraToWorld 取逆为 WorldToCamera。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `130:199`：

> TODO: Need to invert the CameraToWorld matrix => WorldToCamera matrix

<a id="row-619"></a>
## 619. 23shades-0619-aaffecghg

**主题代码：** SATD-A, SATD-F

**开放代码：** 数据接口版本契约迁移

**逐条判断：** 重写以匹配新 stitch datasets signature。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `137:205`：

> TODO: needs to be re-written to match new stitch datasets signature.

<a id="row-620"></a>
## 620. 23shades-0620-aafjjehej

**主题代码：** SATD-O

**开放代码：** 混淆矩阵视觉表达待调整

**逐条判断：** 大小点的新样式。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `127:189`：

> TODO: new style for confusion matrix (using small and big dot)

<a id="row-621"></a>
## 621. 23shades-0621-aaeiefhcd

**主题代码：** SATD-C, SATD-E

**开放代码：** 非数值列自动过滤缺失

**逐条判断：** 应自动 ignore。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `124:181`：

> TODO: non-numeric columns should be ignored automatically

<a id="row-622"></a>
## 622. 23shades-0622-aagagihei

**主题代码：** SATD-B, SATD-D

**开放代码：** 状态归一化待补

**逐条判断：** true states 需 normalize。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `126:153`：

> TODO: normalize true states

<a id="row-623"></a>
## 623. 23shades-0623-aahijjdcb

**主题代码：** SATD-B, SATD-I, SATD-Q

**开放代码：** 未定位的失败

**逐条判断：** NOT PASSED，无测试或计算对象。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `137:153`：

> TODO: NOT PASSED

<a id="row-624"></a>
## 624. 23shades-0624-aaeebjfdb

**主题代码：** SATD-K

**开放代码：** 行为尚未测试

**逐条判断：** 明确 Not test yet/check behavior。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `131:165`：

> TODO: Not test yet; check behavior

<a id="row-625"></a>
## 625. 23shades-0625-aaefhdgid

**主题代码：** SATD-B, SATD-D, SATD-I

**开放代码：** 填充批次计数遗漏

**逐条判断：** fillup policy padding 时 num pad examples 未设置。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `114:186`：

> TODO: num pad examples is not set here if fillup policy would be padding

<a id="row-626"></a>
## 626. 23shades-0626-aadajbgbb

**主题代码：** SATD-B, SATD-D, SATD-I

**开放代码：** 填充批次计数遗漏

**逐条判断：** 与前条近似，用 strategy 表述，独立保留。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `118:192`：

> TODO: num pad examples is not set here if fillup strategy would be padding

<a id="row-627"></a>
## 627. 23shades-0627-aaidgcaed

**主题代码：** SATD-B, SATD-I

**开放代码：** 索引差一错误

**逐条判断：** 明确 off by one。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `123:174`：

> TODO: off by one ... you fool george; sort this out

<a id="row-628"></a>
## 628. 23shades-0628-aaifedeec

**主题代码：** SATD-D, SATD-E, SATD-I

**开放代码：** 共享输入拓扑需支持

**逐条判断：** 同一 input 可供多个 nodes，当前处理欠缺未细述。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `151:203`：

> TODO: one input could be the input of multiple nodes

<a id="row-629"></a>
## 629. 23shades-0629-aaeajfcic

**主题代码：** SATD-D, SATD-E

**开放代码：** 调度适用范围不足

**逐条判断：** optimize scheduling 的目的明确为 support more cases，未必速度。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `133:181`：

> TODO: optimize scheduling to support more cases.

<a id="row-630"></a>
## 630. 23shades-0630-aaeigcjfb

**主题代码：** SATD-D, SATD-E, SATD-Q

**开放代码：** 类型覆盖待扩展

**逐条判断：** other types 问句。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `126:144`：

> TODO: other types?

<a id="row-631"></a>
## 631. 23shades-0631-aaecaicdb

**主题代码：** SATD-D, SATD-E, SATD-G

**开放代码：** 并行执行待实现

**逐条判断：** parallelize。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `174:191`：

> TODO: parallelize

<a id="row-632"></a>
## 632. 23shades-0632-aaiffchcj

**主题代码：** SATD-A

**开放代码：** 入参耦合与负载过大

**逐条判断：** 仅传 id 而非整个 obj_msg。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `122:178`：

> TODO: pass in just the id instead of the entire obj_msg.

<a id="row-633"></a>
## 633. 23shades-0633-aagcdfdia

**主题代码：** SATD-A, SATD-N, SATD-Q

**开放代码：** 序列化格式替换待评估

**逐条判断：** pickle 可能更好，无最终决定。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `135:189`：

> todo: perhaps it's better to use pickle in the future?

<a id="row-634"></a>
## 634. 23shades-0634-aaebhhdjf

**主题代码：** SATD-A, SATD-G

**开放代码：** 设备内存放置改造

**逐条判断：** tensors 放 GPU memory 需要重写。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `162:226`：

> TODO: Place tensors into GPU memory. This will require rewriting

<a id="row-635"></a>
## 635. 23shades-0635-aaedbcjji

**主题代码：** SATD-D

**开放代码：** 数据集获取待办

**逐条判断：** download 来源截断，不能假定已可用。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `132:170`：

> TODO: please download the dataset from

<a id="row-636"></a>
## 636. 23shades-0636-aaibjdfgf

**主题代码：** SATD-D

**开放代码：** 预计算功能未实现

**逐条判断：** 当前 empty。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `131:163`：

> TODO: precompute : empty for now

<a id="row-637"></a>
## 637. 23shades-0637-aaffdijjg

**主题代码：** SATD-M, SATD-Q

**开放代码：** 疑似冗余逻辑

**逐条判断：** pretty sure not necessary，仍非已核实。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `132:170`：

> TODO: pretty sure this isn't necessary

<a id="row-638"></a>
## 638. 23shades-0638-aaghjajha

**主题代码：** SATD-A, SATD-D, SATD-N, SATD-Q

**开放代码：** 深复制协议实现候选

**逐条判断：** 建议实现 __deepcopy__。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `170:219`：

> TODO: Probably should just implement __deepcopy__

<a id="row-639"></a>
## 639. 23shades-0639-aaecjeidf

**主题代码：** SATD-C, SATD-E, SATD-Q

**开放代码：** 能力识别检查缺失

**逐条判断：** 程序检查 predict/correct 是否为 features，词义不足以精确归为 ML 特征。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `138:218`：

> TODO: programmatically check wether these are indeed features (predict; correct)

<a id="row-640"></a>
## 640. 23shades-0640-aaghjahhi

**主题代码：** SATD-A, SATD-F

**开放代码：** 循环依赖待解除

**逐条判断：** 明确 break properly。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `154:196`：

> TODO: Properly break circular dependencies

<a id="row-641"></a>
## 641. 23shades-0641-aaefghgda

**主题代码：** SATD-A, SATD-F

**开放代码：** 上游优化器访问接口缺失

**逐条判断：** MXNet Module 应提供 get_optimizer。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `115:209`：

> TODO: Push update to MXNet to expose the optimizer (Module should have a get_optimizer method)

<a id="row-642"></a>
## 642. 23shades-0642-aahcigdjj

**主题代码：** SATD-D

**开放代码：** 轨迹构造与折叠基础设施缺失

**逐条判断：** 边建 trace 边 fold。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `121:182`：

> TODO: put in infrastructure to fold over trace as it's built.

<a id="row-643"></a>
## 643. 23shades-0643-aagbdffff

**主题代码：** SATD-J

**开放代码：** 替换行为配置缺失

**逐条判断：** 添加 substitution option，适用场景截断。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `115:185`：

> TODO: put in the option to do substitution here (most likely scenario;

<a id="row-644"></a>
## 644. 23shades-0644-aaibjebjh

**主题代码：** SATD-A, SATD-J

**开放代码：** 复制行为缺少按需控制

**逐条判断：** 添加 copy keyword 来 copy on demand。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `131:171`：

> TODO: put keyword copy to copy on demand

<a id="row-645"></a>
## 645. 23shades-0645-aadbbbcgh

**主题代码：** SATD-F

**开放代码：** 依赖声明缺失

**逐条判断：** package requirements 待填。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `125:160`：

> TODO: put package requirements here

<a id="row-646"></a>
## 646. 23shades-0646-aagaijdhc

**主题代码：** SATD-D, SATD-E

**开放代码：** 分布族支持待办

**逐条判断：** quasi/quasibinomial/quasipoisson 列表，未给具体实现缺陷。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `119:159`：

> TODO: quasi; quasibinomial; quasipoisson

<a id="row-647"></a>
## 647. 23shades-0647-aaidbfgae

**主题代码：** SATD-C

**开放代码：** 版本性异常策略迁移

**逐条判断：** 1.1 改 raise error，当前行为未知。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `141:173`：

> TODO: raise error in 1.1 instead

<a id="row-648"></a>
## 648. 23shades-0648-aadhfgije

**主题代码：** SATD-H, SATD-I, SATD-J

**开放代码：** 数据规模硬编码

**逐条判断：** 10000 应从 datasets 读取。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `137:176`：

> TODO: Read this 10000 from the datasets

<a id="row-649"></a>
## 649. 23shades-0649-aaeidhcjb

**主题代码：** SATD-B, SATD-E, SATD-I

**开放代码：** 输出分布维度差异处理

**逐条判断：** 1D 而非1D_Var 时 rebalance。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `116:180`：

> TODO: rebalance if output distributions are 1D instead of 1D_Var

<a id="row-650"></a>
## 650. 23shades-0650-aagejhgfd

**主题代码：** SATD-A, SATD-Q

**开放代码：** 统计量维度待降低

**逐条判断：** mean 降 dim，目的不明。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `113:139`：

> TODO: Reduce dim. of mean.

<a id="row-651"></a>
## 651. 23shades-0651-aagfjdjeg

**主题代码：** SATD-A

**开放代码：** 职责提取

**逐条判断：** 重构为 independent function。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `131:169`：

> TODO: refactor as independent function

<a id="row-652"></a>
## 652. 23shades-0652-aadbaaejd

**主题代码：** SATD-A, SATD-E

**开放代码：** 配置类复用性不足

**逐条判断：** 简化 Configuration 以支持更多 cases，场景截断。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `133:204`：

> TODO: Refactor\/simplify Configuration class so it can be used in cases

<a id="row-653"></a>
## 653. 23shades-0653-aafajcaia

**主题代码：** SATD-Q, SATD-U

**开放代码：** 改进诉求不具体

**逐条判断：** refine 无对象。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `180:192`：

> TODO: refine

<a id="row-654"></a>
## 654. 23shades-0654-aagbifedh

**主题代码：** SATD-D

**开放代码：** 约束求解功能待重实现

**逐条判断：** constraint satisfaction method 按需恢复支持。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `124:195`：

> TODO: re-implement support for constraint satisfaction method as needed

<a id="row-655"></a>
## 655. 23shades-0655-aaeffajfh

**主题代码：** SATD-M, SATD-Q

**开放代码：** 实体清理待办

**逐条判断：** Remove corruption entities，不能确定是代码还是污染样本。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `137:169`：

> TODO: Remove corruption entities

<a id="row-656"></a>
## 656. 23shades-0656-aaefbgdbg

**主题代码：** SATD-M

**开放代码：** 调试任务残留

**逐条判断：** 删除 dummy/debug tasks。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `112:145`：

> TODO: remove dummy \/ debug tasks

<a id="row-657"></a>
## 657. 23shades-0657-aajdbjejb

**主题代码：** SATD-A, SATD-H, SATD-I, SATD-J

**开放代码：** 尺寸硬编码

**逐条判断：** 考虑改成 parent-relative sizes。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `133:191`：

> TODO: remove hard-coded sizes and make relative to parent?

<a id="row-658"></a>
## 658. 23shades-0658-aafeaihbg

**主题代码：** SATD-A, SATD-H, SATD-I, SATD-J

**开放代码：** 缩放计算硬编码

**逐条判断：** 移除 downscaling hardcoding。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `149:201`：

> TODO: Remove hardcoding of downscaling calculations.

<a id="row-659"></a>
## 659. 23shades-0659-aaidbebab

**主题代码：** SATD-F, SATD-M

**开放代码：** 版本性兼容清理

**逐条判断：** _pairwise 在0.26移除后清理。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `154:214`：

> TODO: Remove in 0.26 when the _pairwise attribute is removed

<a id="row-660"></a>
## 660. 23shades-0660-aaidbgddf

**主题代码：** SATD-M

**开放代码：** 版本性清理

**逐条判断：** 1.2删除，未知对象。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `129:148`：

> TODO: Remove in 1.2

<a id="row-661"></a>
## 661. 23shades-0661-aaidbgfgc

**主题代码：** SATD-M

**开放代码：** 版本性清理

**逐条判断：** v1.2删除，独立记录。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `143:163`：

> TODO: Remove in v1.2

<a id="row-662"></a>
## 662. 23shades-0662-aajfceihg

**主题代码：** SATD-K, SATD-O

**开放代码：** 测试依赖人工看日志

**逐条判断：** 应去 logging 并真正断言 values，不只日志功能问题。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `127:172`：

> TODO: remove logging and actually test values

<a id="row-663"></a>
## 663. 23shades-0663-aaiedhhfd

**主题代码：** SATD-G, SATD-I

**开放代码：** 批次引用可能阻碍内存回收

**逐条判断：** 去 refs 是否降低内存需验证，不能称已确诊泄漏。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `118:197`：

> TODO: remove refs on batch to avoid high mem consumption ? -> need verification

<a id="row-664"></a>
## 664. 23shades-0664-aahidajgj

**主题代码：** SATD-E, SATD-F, SATD-H, SATD-M

**开放代码：** 设备批传输支持前的限制

**逐条判断：** Lightning DP mode 完成集成后移除 blocker。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `169:264`：

> TODO: Remove this blocker once batch transfer to device is integrated in Lightning for DP mode.

<a id="row-665"></a>
## 665. 23shades-0665-aaidbbafi

**主题代码：** SATD-M

**开放代码：** 实验性估计器检查待清理

**逐条判断：** 退出 experimental 后 remove check。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `134:203`：

> TODO: remove this check once the estimator is no longer experimental.

<a id="row-666"></a>
## 666. 23shades-0666-aahicgcid

**主题代码：** SATD-M

**开放代码：** 版本性方法清理

**逐条判断：** v1.3.0移除 method。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `150:185`：

> TODO: remove this method in v1.3.0.

<a id="row-667"></a>
## 667. 23shades-0667-aahjgdcge

**主题代码：** SATD-F, SATD-M

**开放代码：** 旧语言版本兼容负担

**逐条判断：** 停止 Python2 后移除 functools.wraps 相关逻辑。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `141:205`：

> TODO: remove this when we drop Python 2 support (functools.wraps

<a id="row-668"></a>
## 668. 23shades-0668-aaeiebdgb

**主题代码：** SATD-M

**开放代码：** 旧类型清理

**逐条判断：** timestamp_series_type 待移除。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `112:146`：

> TODO: remove timestamp_series_type

<a id="row-669"></a>
## 669. 23shades-0669-aahibibgj

**主题代码：** SATD-M

**开放代码：** 旧结果格式废弃后清理

**逐条判断：** dict results deprecated 为先决条件。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `162:207`：

> TODO: remove when dict results are deprecated

<a id="row-670"></a>
## 670. 23shades-0670-aaeeijdhi

**主题代码：** SATD-A

**开放代码：** 函数名称表达待改

**逐条判断：** assemble_filterbank 是候选。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `119:166`：

> TODO: rename function to assemble_filterbank()?

<a id="row-671"></a>
## 671. 23shades-0671-aaedghfjd

**主题代码：** SATD-A, SATD-J

**开放代码：** 参数名称精确化

**逐条判断：** forward 改 forward_additive。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `123:177`：

> TODO: rename kwarg \"forward\" to \"forward_additive\"

<a id="row-672"></a>
## 672. 23shades-0672-aagahbjib

**主题代码：** SATD-A

**开放代码：** 跨仓库字段命名迁移

**逐条判断：** split_index 改复数并同步 RL repo。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `120:181`：

> TODO: rename split_index -> split_indices + change in RL repo

<a id="row-673"></a>
## 673. 23shades-0673-aaiecbahd

**主题代码：** SATD-A, SATD-F, SATD-M

**开放代码：** 模块名冲突

**逐条判断：** 需避免与 stdlib 同名。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `129:200`：

> TODO: Rename the module to something that does not conflict with stdlib

<a id="row-674"></a>
## 674. 23shades-0674-aagiejcbj

**主题代码：** SATD-A

**开放代码：** 呈现职责转模板

**逐条判断：** render in template。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `159:183`：

> TODO: render in template

<a id="row-675"></a>
## 675. 23shades-0675-aadagdejg

**主题代码：** SATD-B, SATD-D, SATD-E, SATD-F

**开放代码：** 动态分割受算子限制

**逐条判断：** Repeat_elements/tf.split 不支持 dynamic splits。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `133:199`：

> TODO: Repeat_elements and tf.split doesn't support dynamic splits.

<a id="row-676"></a>
## 676. 23shades-0676-aaicjgced

**主题代码：** SATD-A, SATD-F, SATD-M

**开放代码：** 版本性表示迁移

**逐条判断：** 0.21替换为 dict。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `140:171`：

> TODO: replace by a dict in 0.21

<a id="row-677"></a>
## 677. 23shades-0677-aaefecjfa

**主题代码：** SATD-A, SATD-J, SATD-M

**开放代码：** 默认初始化与告警迁移

**逐条判断：** v0.6.0 init=None 改 auto 并移除 warning。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `133:204`：

> TODO: replace init=None by init='auto' in v0.6.0 and remove the warning

<a id="row-678"></a>
## 678. 23shades-0678-aafeaiffi

**主题代码：** SATD-A

**开放代码：** 损失层抽象待替换

**逐条判断：** Lambda 改 custom Keras layer。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `138:192`：

> TODO: Replace Lambda with custom Keras layer for loss.

<a id="row-679"></a>
## 679. 23shades-0679-aaefbfhbj

**主题代码：** SATD-A, SATD-Q

**开放代码：** 组件替代待办

**逐条判断：** MTTask 替代，理由未给。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `111:141`：

> TODO: replace this with MTTask

<a id="row-680"></a>
## 680. 23shades-0680-aadhbjgee

**主题代码：** SATD-M, SATD-N, SATD-Q

**开放代码：** 数据库容量制约变更

**逐条判断：** space in db 后替换，未说明内容。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `153:183`：

> TODO: Replace when space in db

<a id="row-681"></a>
## 681. 23shades-0681-aaibgbejh

**主题代码：** SATD-A, SATD-F, SATD-M

**开放代码：** 稳定依赖可用性制约

**逐条判断：** 若可用则替换 Draft6Validator。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `109:166`：

> TODO: replace with (stable) Draft6Validator; if available

<a id="row-682"></a>
## 682. 23shades-0682-aaejbieif

**主题代码：** SATD-D, SATD-E, SATD-F

**开放代码：** 三维输入受上游能力限制

**逐条判断：** grid_sample 支持后采用3d input。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `132:202`：

> ToDo: replace with 3d input; when grid_sample will start to support it

<a id="row-683"></a>
## 683. 23shades-0683-aaeihdfda

**主题代码：** SATD-A, SATD-F, SATD-M

**开放代码：** 编译模式算子受限

**逐条判断：** Numba nopython 支持 np.isin 后简化。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `141:215`：

> TODO: replace with below line when Numba supports np.isin in nopython mode

<a id="row-684"></a>
## 684. 23shades-0684-aaiejaeea

**主题代码：** SATD-A, SATD-Q

**开放代码：** 批次聚合操作待替换

**逐条判断：** 改 unbatch/readout，选择未定。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `126:163`：

> TODO: replace with unbatch or readout

<a id="row-685"></a>
## 685. 23shades-0685-aaheajiai

**主题代码：** SATD-N, SATD-U

**开放代码：** 结果结构证据截断

**逐条判断：** result_dict 含 images batches，但 while 后对比缺失。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `152:203`：

> TODO: result_dict contains batches of images; while

<a id="row-686"></a>
## 686. 23shades-0686-aagbiaaje

**主题代码：** SATD-A, SATD-N, SATD-Q

**开放代码：** 返回标识形式待改

**逐条判断：** return id's key，具体对象不足。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `120:141`：

> TODO: return id's key

<a id="row-687"></a>
## 687. 23shades-0687-aagbjaigc

**主题代码：** SATD-D, SATD-Q

**开放代码：** 奖励计算待办

**逐条判断：** reward computation 无更具体缺陷。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `136:160`：

> TODO: reward computation

<a id="row-688"></a>
## 688. 23shades-0688-aafibegea

**主题代码：** SATD-A, SATD-B, SATD-F, SATD-Q

**开放代码：** 上游输出形状契约待改善

**逐条判断：** rotated_grids 应直接给 correctly shaped array。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `146:229`：

> TODO: rotated_grids might as well give us correctly shaped array in the first place

<a id="row-689"></a>
## 689. 23shades-0689-aaacjhcjh

**主题代码：** SATD-A

**开放代码：** 模块拆分待办

**逐条判断：** run-on/split module，不推断算法错误。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `125:154`：

> TODO: run-on and split module

<a id="row-690"></a>
## 690. 23shades-0690-aahafiehj

**主题代码：** SATD-U

**开放代码：** 仅外部教程引用

**逐条判断：** 链接指 face alignment，但未读取网页，不从链接恢复待实现内容。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `126:222`：

> TODO: See https:\/\/www.pyimagesearch.com\/2017\/05\/22\/face-alignment-with-opencv-and-python\/

<a id="row-691"></a>
## 691. 23shades-0691-aagejcfed

**主题代码：** SATD-K

**开放代码：** 测试输入分离

**逐条判断：** 拆成两个不同 inputs 以测试，后续行为截断。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `134:192`：

> TODO: separate this into two different inputs to test that

<a id="row-692"></a>
## 692. 23shades-0692-aajcfiaid

**主题代码：** SATD-C, SATD-I

**开放代码：** 最终模型完整性检查未启用

**逐条判断：** check_hash 应 True。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `137:180`：

> TODO: set check_hash to True on final model

<a id="row-693"></a>
## 693. 23shades-0693-aajacfjhb

**主题代码：** SATD-A, SATD-I, SATD-J, SATD-Q

**开放代码：** 初始化接口参数化待定

**逐条判断：** 考虑 keyword arg。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `139:179`：

> todo: set in initializer as keyword arg?

<a id="row-694"></a>
## 694. 23shades-0694-aaidhabjj

**主题代码：** SATD-A, SATD-I, SATD-J, SATD-Q

**开放代码：** 日期间隔选择待定

**逐条判断：** original date interval 未定。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `136:178`：

> TODO: Set interval for the original date ?

<a id="row-695"></a>
## 695. 23shades-0695-aaeeihicj

**主题代码：** SATD-A, SATD-I, SATD-J, SATD-Q

**开放代码：** 音频特征默认值适用性待查

**逐条判断：** MFCC 是否用不同于 filterbank 的 defaults。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `120:189`：

> TODO: set other defaults than those in cp.audio.filterbank for MFCCs?

<a id="row-696"></a>
## 696. 23shades-0696-aaiihdfjc

**主题代码：** SATD-B, SATD-D, SATD-I

**开放代码：** 条件性批量状态初始化

**逐条判断：** self.bsum 时设置 batch_sum。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `120:160`：

> TODO: Set up self.batch_sum if self.bsum

<a id="row-697"></a>
## 697. 23shades-0697-aadhhifdg

**主题代码：** SATD-I, SATD-Q, SATD-V

**开放代码：** 标识属性排除

**逐条判断：** 作者自问 port/IP/MAC 是否忽略并答 yes；不能推断隐私动机。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `148:198`：

> TODO: should port\/ip\/mac address be ignored? yes

<a id="row-698"></a>
## 698. 23shades-0698-aagdjigjj

**主题代码：** SATD-D, SATD-N

**开放代码：** 模型持久化缺失

**逐条判断：** 此处应保存 TPOT model。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `137:170`：

> todo: should save tpot model here

<a id="row-699"></a>
## 699. 23shades-0699-aaffeacij

**主题代码：** SATD-A, SATD-J, SATD-Q

**开放代码：** 命名连续性

**逐条判断：** self.network 以保持 continuity，尚为疑问。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `129:185`：

> TODO: Should this be called self.network for continuity?

<a id="row-700"></a>
## 700. 23shades-0700-aaeejihee

**主题代码：** SATD-A, SATD-Q

**开放代码：** 差异处理职责范围待定

**逐条判断：** class 是否始终只处理 differences/filtering。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `120:189`：

> TODO: should this class always act on just the differences? filtering

<a id="row-701"></a>
## 701. 23shades-0701-aaefaahhg

**主题代码：** SATD-A, SATD-I, SATD-N, SATD-Q

**开放代码：** 返回表示选择待定

**逐条判断：** LogarithmicFilteredSpectrogram 作为候选返回类型。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `130:186`：

> TODO: should we return a LogarithmicFilteredSpectrogram?

<a id="row-702"></a>
## 702. 23shades-0702-aahcjejhi

**主题代码：** SATD-A, SATD-Q

**开放代码：** 抽象升级后实现可简化

**逐条判断：** 多变量 flow 使用 multivariate base distributions 后简化。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `129:224`：

> TODO: Simplify following line once using multivariate base distributions for multivariate flows

<a id="row-703"></a>
## 703. 23shades-0703-aagaahfid

**主题代码：** SATD-C, SATD-I, SATD-Q

**开放代码：** 异常恢复策略待定

**逐条判断：** 是否 skip on error。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `131:153`：

> TODO: skip on error???

<a id="row-704"></a>
## 704. 23shades-0704-aagfjeihb

**主题代码：** SATD-U

**开放代码：** 证据不足

**逐条判断：** something if deep9 无可判读目标。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `133:158`：

> TODO: something if deep 9

<a id="row-705"></a>
## 705. 23shades-0705-aajdcfhfa

**主题代码：** SATD-Q, SATD-U

**开放代码：** 方案不满意但对象不明

**逐条判断：** Something smarter。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `129:153`：

> TODO: Something smarter?

<a id="row-706"></a>
## 706. 23shades-0706-aaidjfjdb

**主题代码：** SATD-A, SATD-Q

**开放代码：** 几何坐标参照缺明确配置

**逐条判断：** relative to 后对象截断。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `134:194`：

> TODO: specifiy if the geometry should be set relative to the

<a id="row-707"></a>
## 707. 23shades-0707-aaeiefjai

**主题代码：** SATD-A, SATD-Q

**开放代码：** 视图拆分待办

**逐条判断：** split view 无细节。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `126:142`：

> TODO: split view

<a id="row-708"></a>
## 708. 23shades-0708-aahjejchc

**主题代码：** SATD-A, SATD-J

**开放代码：** 命名约定不一致

**逐条判断：** _offset 与 offset 统一。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `143:200`：

> TODO: standardize `_offset` vs `offset` naming convention

<a id="row-709"></a>
## 709. 23shades-0709-aaedaedaa

**主题代码：** SATD-B, SATD-N

**开放代码：** 张量结果序列化失败

**逐条判断：** start/end logits Tensor 不能 JSON serialize，明确 TypeError。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `132:220`：

> TODO: start and end logits (TypeError: Object of type 'Tensor' is not JSON serializable)

<a id="row-710"></a>
## 710. 23shades-0710-aaeiiihac

**主题代码：** SATD-D

**开放代码：** 实现未完成

**逐条判断：** still in progress。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `131:154`：

> TODO: still in progress

<a id="row-711"></a>
## 711. 23shades-0711-aafbjiedd

**主题代码：** SATD-A, SATD-N, SATD-Q

**开放代码：** 存储表示待简化

**逐条判断：** store something cleaner，未说明介质或性能。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `146:175`：

> TODO: store something cleaner

<a id="row-712"></a>
## 712. 23shades-0712-aajaighgc

**主题代码：** SATD-A, SATD-B, SATD-I, SATD-N

**开放代码：** 行号不稳定需持久索引

**逐条判断：** table 应存 actual index，避免 row number 不稳定。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `142:210`：

> TODO: store the actual index in table in case row number is unstable

<a id="row-713"></a>
## 713. 23shades-0713-aaahbbdbf

**主题代码：** SATD-A, SATD-F

**开放代码：** 上游参数注册贡献待提交

**逐条判断：** imgaug PR 待提交，非已合并功能。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `126:179`：

> TODO: submit a PR to imgaug that registers parameters

<a id="row-714"></a>
## 714. 23shades-0714-aaadhcgbc

**主题代码：** SATD-D, SATD-E

**开放代码：** 批量输入支持缺失

**逐条判断：** batch tf example inputs。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `148:186`：

> TODO: Support batch tf example inputs.

<a id="row-715"></a>
## 715. 23shades-0715-aaeiedfaj

**主题代码：** SATD-D, SATD-E

**开放代码：** 容器索引接口缺失

**逐条判断：** getitem 待支持。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `124:158`：

> TODO: support getitem of container

<a id="row-716"></a>
## 716. 23shades-0716-aacjgagdb

**主题代码：** SATD-D, SATD-E

**开放代码：** 骨干模型覆盖不足

**逐条判断：** more backbone。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `145:172`：

> TODO: support more backbone

<a id="row-717"></a>
## 717. 23shades-0717-aahhgdcgi

**主题代码：** SATD-K

**开放代码：** 测试缺失

**逐条判断：** Test，无对象。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `140:150`：

> TODO: Test

<a id="row-718"></a>
## 718. 23shades-0718-aadbaabcf

**主题代码：** SATD-K

**开放代码：** 交易行为测试缺失

**逐条判断：** buy-to-close option trades。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `130:167`：

> TODO: Test buy to close option trades

<a id="row-719"></a>
## 719. 23shades-0719-aajffiged

**主题代码：** SATD-K

**开放代码：** 执行顺序测试缺失

**逐条判断：** no-plot 后 examples 是否执行并产出，产出细节截断。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `156:221`：

> TODO: test that examples are executed after a no-plot and produce

<a id="row-720"></a>
## 720. 23shades-0720-aagejejie

**主题代码：** SATD-K

**开放代码：** 重复构建测试缺失

**逐条判断：** rebuilding multiple times。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `126:182`：

> TODO: test that rebuilding multiple times works properly

<a id="row-721"></a>
## 721. 23shades-0721-aahdjfjcf

**主题代码：** SATD-K

**开放代码：** 测试缺失

**逐条判断：** test this。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `140:155`：

> TODO: test this

<a id="row-722"></a>
## 722. 23shades-0722-aaiejccah

**主题代码：** SATD-G

**开放代码：** 现有算子可改善批图性能

**逐条判断：** TF unsorted_segment_max 可加速 _max_on，未提供实测。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `128:208`：

> TODO: TF has unsorted_segment_max; which can accelerate _max_on on batched graph

<a id="row-723"></a>
## 723. 23shades-0723-aaeacgjbc

**主题代码：** SATD-F, SATD-M

**开放代码：** 调用方迁移后的兼容选项清理

**逐条判断：** 所有用户传正确 phabricator_deployment 后可去空字符串选择。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `130:241`：

> TODO: The \"\" choice can be removed when all users have been updated to pass a correct phabricator_deployment.

<a id="row-724"></a>
## 724. 23shades-0724-aaidgiiag

**主题代码：** SATD-A, SATD-H, SATD-I, SATD-J

**开放代码：** 硬编码偏移依赖坐标共享

**逐条判断：** -2 仅末元素 shared axes 时成立，应自动检测。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `134:213`：

> TODO: the -2 is only if the last element has shared axes; we should detect that

<a id="row-725"></a>
## 725. 23shades-0725-aahicjieh

**主题代码：** SATD-A, SATD-J, SATD-Q

**开放代码：** 生命周期钩子迁移位置未决

**逐条判断：** setup 改名 pre_training，hook 何时调用待定。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `151:240`：

> TODO: the old setup is now called \"pre_training\"; where should this hook be called now?

<a id="row-726"></a>
## 726. 23shades-0726-aadejjjdj

**主题代码：** SATD-B, SATD-M, SATD-Q

**开放代码：** 规则项未使用

**逐条判断：** 第二元素被忽略，未判断是冗余还是遗漏。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `128:182`：

> TODO: the second element of the rule is not being used

<a id="row-727"></a>
## 727. 23shades-0727-aaheacagj

**主题代码：** SATD-H, SATD-I, SATD-N

**开放代码：** 真实训练目标被随机占位替代

**逐条判断：** y_train 应外部提供，目前随机生成，明确数据来源债务。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `125:210`：

> TODO: the y_train should be given us externally; so far we create it as random values

<a id="row-728"></a>
## 728. 23shades-0728-aadhcgicg

**主题代码：** SATD-V

**开放代码：** 单内容词边界说明

**逐条判断：** 描述触发 branch 的条件，未明确错误或待改行为。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `115:175`：

> TODO: This branch happens when there's only one content word

<a id="row-729"></a>
## 729. 23shades-0729-aafafjdeg

**主题代码：** SATD-B, SATD-I, SATD-Q

**开放代码：** 层共享被破坏但影响未定

**逐条判断：** 作者明确 breaks layer sharing，并问该类是否受影响。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `135:198`：

> TODO: This breaks layer sharing. Does it matter for this class?

<a id="row-730"></a>
## 730. 23shades-0730-aaiheabif

**主题代码：** SATD-F, SATD-M

**开放代码：** 上游批维模式支持前的兼容逻辑

**逐条判断：** word/locked_dropout 有 batch_first 后才可删除。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `139:253`：

> TODO: this can only be removed once the implementations of word_dropout and locked_dropout have a batch_first mode

<a id="row-731"></a>
## 731. 23shades-0731-aafiggaje

**主题代码：** SATD-A, SATD-M

**开放代码：** 冗余标记待整合

**逐条判断：** 与前 flag 重复，后句截断。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `123:187`：

> TODO: this flag is somewhat redundant given the flag above; need

<a id="row-732"></a>
## 732. 23shades-0732-aahjacheg

**主题代码：** SATD-B, SATD-I, SATD-Q

**开放代码：** 相位信息丢失的适用性疑问

**逐条判断：** discarding phase 是否可接受未定。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `127:170`：

> TODO: This is discarding phase. Is that ok?

<a id="row-733"></a>
## 733. 23shades-0733-aajacfjii

**主题代码：** SATD-G, SATD-I

**开放代码：** 二次复杂度扩展风险

**逐条判断：** O(N²) 可能对大图过慢，未断言已测得。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `139:196`：

> todo: this is O(N^2) and maybe too slow for large graphs.

<a id="row-734"></a>
## 734. 23shades-0734-aaifdieif

**主题代码：** SATD-A

**开放代码：** 初始化职责集中导致可维护性差

**逐条判断：** 作者称 ugly，全部工作塞一方法的依赖原因截断。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `136:236`：

> TODO: this is ugly; we put all the initialization work in this method; because initialization relies

<a id="row-735"></a>
## 735. 23shades-0735-aaihjgafa

**主题代码：** SATD-G

**开放代码：** 执行效率低

**逐条判断：** 明确 very inefficient needs fix。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `129:173`：

> TODO: This is very inefficient and needs fix

<a id="row-736"></a>
## 736. 23shades-0736-aafafebhi

**主题代码：** SATD-G

**开放代码：** 循环并行机会

**逐条判断：** parallelizable 表示可改进，不等于已实现。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `127:160`：

> TODO: this loop is parallelizable

<a id="row-737"></a>
## 737. 23shades-0737-aafdiegjf

**主题代码：** SATD-G

**开放代码：** 匹配过程缓慢

**逐条判断：** 建议避免 loops 提速。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `144:224`：

> TODO: This matching process is slow. Make it faster; avoid loops where possible.

<a id="row-738"></a>
## 738. 23shades-0738-aagaeeefj

**主题代码：** SATD-A, SATD-F, SATD-Q

**开放代码：** 依赖聚合过重

**逐条判断：** method 拉入全部 implementation dependencies，后续影响缺失。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `162:229`：

> TODO: This method pulls in all the implementation dependencies into

<a id="row-739"></a>
## 739. 23shades-0739-aaibgjddj

**主题代码：** SATD-A, SATD-Q

**开放代码：** 命名语义待改

**逐条判断：** 可能不应叫 corpora。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `114:152`：

> TODO: This might not be called corpora

<a id="row-740"></a>
## 740. 23shades-0740-aagdjibjh

**主题代码：** SATD-B, SATD-E, SATD-F, SATD-I, SATD-K, SATD-Q

**开放代码：** 数值类型兼容未验证

**逐条判断：** NumPy types 可能不工作，作者明确 haven't checked。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `139:203`：

> TODO: This might not work with numpy types; haven't checked - AD

<a id="row-741"></a>
## 741. 23shades-0741-aaigbchde

**主题代码：** SATD-C, SATD-I, SATD-Q

**开放代码：** 约束过宽

**逐条判断：** 应 enforce more specific，但对象未列。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `172:230`：

> TODO: This needs to be enforced to something more specific

<a id="row-742"></a>
## 742. 23shades-0742-aahedhicb

**主题代码：** SATD-A

**开放代码：** 代码难理解

**逐条判断：** dense/confusing，需要清理。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `118:186`：

> TODO: This next code is dense and confusing. Clean up at some point.

<a id="row-743"></a>
## 743. 23shades-0743-aahgffjcf

**主题代码：** SATD-D, SATD-E

**开放代码：** 模块递归搜索缺失

**逐条判断：** 应递归查有 flatten_parameters 的 module。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `120:196`：

> TODO: This should be recusive looking for any module with flatten_parameters

<a id="row-744"></a>
## 744. 23shades-0744-aaefediad

**主题代码：** SATD-A, SATD-Q

**开放代码：** 编程风格重构

**逐条判断：** 可改 functional style，未说明性能或正确性收益。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `154:205`：

> TODO: This we can change easily to functional style

<a id="row-745"></a>
## 745. 23shades-0745-aaidfiegj

**主题代码：** SATD-K

**开放代码：** 测试缺失

**逐条判断：** to be tested。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `207:225`：

> TODO: to be tested

<a id="row-746"></a>
## 746. 23shades-0746-aajgdgaed

**主题代码：** SATD-D, SATD-E

**开放代码：** 功能扩展待办截断

**逐条判断：** raw object 要 expand，但新增内容缺失。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `129:194`：

> TODO: To further functionality; eventually expand raw object with

<a id="row-747"></a>
## 747. 23shades-0747-aafighdeg

**主题代码：** SATD-A, SATD-I, SATD-J, SATD-Q

**开放代码：** 训练样本挖掘策略待决策

**逐条判断：** 是否 hard example mining。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `149:224`：

> TODO: To hard example mine or not to hard example mine; that's the question

<a id="row-748"></a>
## 748. 23shades-0748-aaidaidid

**主题代码：** SATD-A, SATD-M, SATD-Q

**开放代码：** 树操作冗余疑问

**逐条判断：** 此情形 tree 不应需要该逻辑。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `126:168`：

> TODO: tree should't need this in this case

<a id="row-749"></a>
## 749. 23shades-0749-aaihgdiif

**主题代码：** SATD-A, SATD-I, SATD-J, SATD-Q

**开放代码：** 参数值探索

**逐条判断：** 尝试更小 numbers，未指明参数。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `156:182`：

> TODO: Try smaller numbers?

<a id="row-750"></a>
## 750. 23shades-0750-aagbdibbb

**主题代码：** SATD-G, SATD-Q

**开放代码：** 复制开销优化候选

**逐条判断：** 不复制可能 faster，尚未验证。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `134:176`：

> TODO: try without copying? could be faster

<a id="row-751"></a>
## 751. 23shades-0751-aahgfjfhj

**主题代码：** SATD-G, SATD-I, SATD-K

**开放代码：** 性能检查受数据生成质量限制

**逐条判断：** 更好 data generation 前先关 performance check。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `115:179`：

> TODO: turn off performance check before a better data generation

<a id="row-752"></a>
## 752. 23shades-0752-aagfegjcg

**主题代码：** SATD-U

**开放代码：** 证据不足

**逐条判断：** 只有 U。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `132:139`：

> TODO: U

<a id="row-753"></a>
## 753. 23shades-0753-aaeejgbaa

**主题代码：** SATD-A, SATD-J, SATD-Q

**开放代码：** 参数/概念语义统一

**逐条判断：** look_aside 与 interval_sigma 统一。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `117:178`：

> TODO: unify look_aside with CRFBeatDetection's interval_sigma

<a id="row-754"></a>
## 754. 23shades-0754-aafibabbi

**主题代码：** SATD-A

**开放代码：** 成对操作缺生命周期抽象

**逐条判断：** unroll/roll 总共同用，适合 context manager。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `147:250`：

> TODO: unroll\/roll are great candidates for a context manager since they're always used in conjunction.

<a id="row-755"></a>
## 755. 23shades-0755-aahdfaija

**主题代码：** SATD-A, SATD-D

**开放代码：** 词表内容约束

**逐条判断：** nouns list 只保留 named entities。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `125:173`：

> TODO: update nouns list with only named enitites

<a id="row-756"></a>
## 756. 23shades-0756-aahegjjea

**主题代码：** SATD-A, SATD-D, SATD-Q

**开放代码：** 词表外部来源更新候选

**逐条判断：** 考虑用 Wikipedia emoticons list，未访问链接。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `113:183`：

> ToDo: Update with http:\/\/en.wikipedia.org\/wiki\/List_of_emoticons ?

<a id="row-757"></a>
## 757. 23shades-0757-aajdcfhjb

**主题代码：** SATD-A

**开放代码：** 差异算法库复用

**逐条判断：** 改用 google-diff-patch-match。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `129:170`：

> TODO: Use google-diff-patch-match library

<a id="row-758"></a>
## 758. 23shades-0758-aagfbieab

**主题代码：** SATD-A

**开放代码：** 输入输出职责抽象

**逐条判断：** 用 Input/Output 类处理。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `128:191`：

> todo: use Input and Output classes to handle inputs and outputs

<a id="row-759"></a>
## 759. 23shades-0759-aaibihdci

**主题代码：** SATD-G

**开放代码：** 并行执行待实现

**逐条判断：** joblib 或 multiprocessing 两个候选。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `138:211`：

> TODO: use joblib.Parallel or multiprocessing to parallelize the following

<a id="row-760"></a>
## 760. 23shades-0760-aajbhfbhg

**主题代码：** SATD-A, SATD-Q

**开放代码：** 算法库实现替代待评估

**逐条判断：** TruncatedSVD 是否使用尚为疑问。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `142:195`：

> TODO: Use sklearn.decomposition.TruncatedSVD instead?

<a id="row-761"></a>
## 761. 23shades-0761-aaffdjjaa

**主题代码：** SATD-A, SATD-F

**开放代码：** 框架新模块迁移待办

**逐条判断：** tablemodules NEW，未展开链接内容。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `132:220`：

> TODO: Use tablemodules NEW: https:\/\/github.com\/torch\/nn\/blob\/master\/doc\/table.md

<a id="row-762"></a>
## 762. 23shades-0762-aaedhjhei

**主题代码：** SATD-A, SATD-Q

**开放代码：** 既有复制函数复用

**逐条判断：** Use copy function，无具体语义保证。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `114:141`：

> TODO: Use the copy function

<a id="row-763"></a>
## 763. 23shades-0763-aajdbdjhc

**主题代码：** SATD-K

**开放代码：** 验证器测试缺失

**逐条判断：** verifier tests。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `116:136`：

> TODO: verifier tests

<a id="row-764"></a>
## 764. 23shades-0764-aadiicibd

**主题代码：** SATD-C, SATD-K, SATD-Q

**开放代码：** 行为有效性待验证

**逐条判断：** verify working，无明确已失败。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `202:231`：

> TODO: verify if it is working

<a id="row-765"></a>
## 765. 23shades-0765-aaffdgbgi

**主题代码：** SATD-A, SATD-F, SATD-Q

**开放代码：** 命名空间冲突下命名待决策

**逐条判断：** 想叫 activation 但 namespace 有约束。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `136:203`：

> TODO: want to call it activation but namespace; so what to do best?

<a id="row-766"></a>
## 766. 23shades-0766-aajacaegf

**主题代码：** SATD-G, SATD-Q

**开放代码：** 内存释放优化机会

**逐条判断：** 释放 memory 可能减少 usage，不确认泄漏。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `139:201`：

> todo: We can potentially reduce memory usage by freeing memory

<a id="row-767"></a>
## 767. 23shades-0767-aaiefdgde

**主题代码：** SATD-D, SATD-E

**开放代码：** 过滤能力受限

**逐条判断：** tracker filter 此处不能使用，过滤对象截断。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `136:188`：

> TODO: we can't use tracker filter here to filter for

<a id="row-768"></a>
## 768. 23shades-0768-aaahbfbgd

**主题代码：** SATD-A, SATD-I, SATD-J, SATD-Q

**开放代码：** 监测默认值不合理

**逐条判断：** 可以选 reasonable monitor default，未定值。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `123:190`：

> TODO: we could probably default the monitor to something reasonable

<a id="row-769"></a>
## 769. 23shades-0769-aaefhaief

**主题代码：** SATD-F, SATD-H, SATD-I

**开放代码：** 依赖已知 bug 的脆弱实现

**逐条判断：** 利用 unravel_index bug 避免知道 first shape，明确缺陷耦合。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `116:226`：

> TODO: we currently exploit a bug in the implementation of unravel_index to not require knowing the first shape

<a id="row-770"></a>
## 770. 23shades-0770-aadhddfhh

**主题代码：** SATD-D, SATD-E, SATD-I

**开放代码：** 特殊尺寸支持待扩展

**逐条判断：** 未来可支持 size=-1。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `121:165`：

> TODO: we may support size = -1 in the future

<a id="row-771"></a>
## 771. 23shades-0771-aadgffgjf

**主题代码：** SATD-Q, SATD-U

**开放代码：** 方案不满意但对象不明

**逐条判断：** more intelligent。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `142:195`：

> TODO: we really should be more intelligent about this

<a id="row-772"></a>
## 772. 23shades-0772-aahcfeahc

**主题代码：** SATD-O

**开放代码：** 日志范围过宽

**逐条判断：** 不应记录 nested estimator parameters，原因截断，不能推断敏感泄露。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `127:182`：

> TODO: We should not log nested estimator parameters for

<a id="row-773"></a>
## 773. 23shades-0773-aahgddjfi

**主题代码：** SATD-B, SATD-C

**开放代码：** 畸形输入不应出现

**逐条判断：** 作者要求修复 malformed inputs 的产生，未确认根因。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `119:182`：

> TODO: We shouldn't be getting these malformed inputs. Fix this.

<a id="row-774"></a>
## 774. 23shades-0774-aafhiicbj

**主题代码：** SATD-A, SATD-B, SATD-I

**开放代码：** 权重计算方式待改

**逐条判断：** 此处应按 length 加权。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `114:141`：

> TODO: weight by length here

<a id="row-775"></a>
## 775. 23shades-0775-aahjejdja

**主题代码：** SATD-B, SATD-I, SATD-Q

**开放代码：** 零值分支不一致

**逐条判断：** 处理0与其他地方相反，需解释。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `143:204`：

> TODO: Why does this handle the 0 case the opposite of others?

<a id="row-776"></a>
## 776. 23shades-0776-aaieahjdd

**主题代码：** SATD-G, SATD-I, SATD-Q

**开放代码：** 超出所需的分布计算

**逐条判断：** 只需 min/max 却计算 whole distribution，明确冗余计算疑问。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `127:196`：

> TODO: why is the whole distribution computed instead of just min\/max

<a id="row-777"></a>
## 777. 23shades-0777-aagaecbjg

**主题代码：** SATD-L

**开放代码：** 来源引用缺失

**逐条判断：** add ref from source。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `120:162`：

> TODO: would be good to add ref from source

<a id="row-778"></a>
## 778. 23shades-0778-aajfbhgdi

**主题代码：** SATD-A

**开放代码：** 会话生命周期管理不当

**逐条判断：** 需要 with session_context 正确包装。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `116:169`：

> TODO: wrap this properly in a with session_context():

<a id="row-779"></a>
## 779. 23shades-0779-aajffiiac

**主题代码：** SATD-A

**开放代码：** 函数抽象缺失

**逐条判断：** 提取函数执行当前逻辑。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `135:170`：

> TODO: write a function to do this..

<a id="row-780"></a>
## 780. 23shades-0780-aaididbfa

**主题代码：** SATD-D, SATD-N

**开放代码：** 索引输出缺失

**逐条判断：** write index，无格式信息。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `115:132`：

> TODO: write index

<a id="row-781"></a>
## 781. 23shades-0781-aaidjdcbf

**主题代码：** SATD-K

**开放代码：** 测试覆盖不足

**逐条判断：** more tests。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `116:139`：

> TODO: Write more tests!

<a id="row-782"></a>
## 782. 23shades-0782-aaahbahcg

**主题代码：** SATD-D, SATD-O

**开放代码：** 可视化输出缺失

**逐条判断：** write out visualizations。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `139:175`：

> TODO: write out a few visualizations

<a id="row-783"></a>
## 783. 23shades-0783-aagbcgbif

**主题代码：** SATD-D

**开放代码：** 方法实现缺失

**逐条判断：** CopyMetaField.resolve 待写。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `118:162`：

> TODO: Write resolve method for CopyMetaField

<a id="row-784"></a>
## 784. 23shades-0784-aahjaaeee

**主题代码：** SATD-K

**开放代码：** 测试缺失

**逐条判断：** write tests。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `106:123`：

> TODO: Write tests

<a id="row-785"></a>
## 785. 23shades-0785-aaeiaeifb

**主题代码：** SATD-K

**开放代码：** 跨语料测试覆盖不足

**逐条判断：** all treebanks 需测试。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `121:156`：

> TODO: Write tests for all treebanks

<a id="row-786"></a>
## 786. 23shades-0786-aahddigdj

**主题代码：** SATD-D, SATD-E

**开放代码：** 输入表示支持不全

**逐条判断：** x/y 应支持 numpy、pandas 或 TF dataset iterator。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `128:214`：

> TODO: x;y input should be able to be np arrays; pandas arrays; or tf dataset iterators

<a id="row-787"></a>
## 787. 23shades-0787-aafhfhjbf

**主题代码：** SATD-D, SATD-K, SATD-Q

**开放代码：** 自动推理功能完成度不明

**逐条判断：** implement automatic inference 但 maybe done，需确认状态。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `123:170`：

> TODO; implement automatic inference; maybe done

<a id="row-788"></a>
## 788. 23shades-0788-aahiebjbd

**主题代码：** SATD-A, SATD-Q

**开放代码：** 可维护性改善诉求

**逐条判断：** make nicer，无具体机制。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `116:132`：

> TODO; make nicer

<a id="row-789"></a>
## 789. 23shades-0789-aahicagej

**主题代码：** SATD-D

**开放代码：** 结果传递不完整

**逐条判断：** 还应传 best score。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `170:196`：

> todo; pass also best score

<a id="row-790"></a>
## 790. 23shades-0790-aahicaeda

**主题代码：** SATD-D, SATD-N

**开放代码：** 检查点状态传递不完整

**逐条判断：** 需传 complete checkpoint as state dictionary。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `166:216`：

> todo; pass complete checkpoint as state dictionary

<a id="row-791"></a>
## 791. 23shades-0791-aahgcaaac

**主题代码：** SATD-C, SATD-J, SATD-O, SATD-Q

**开放代码：** 额外参数冲突提示待定

**逐条判断：** extras 与已有不匹配时是否 warning。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `134:184`：

> TODO? warn if not matching extras already present?

<a id="row-792"></a>
## 792. 23shades-0792-aagigaiii

**主题代码：** SATD-G

**开放代码：** 内存占用过大

**逐条判断：** lazy load 更好但推迟；明确现有负担。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `114:169`：

> too much memory. A lazy load would be better; but later

<a id="row-793"></a>
## 793. 23shades-0793-aahefcehd

**主题代码：** SATD-D, SATD-N, SATD-Q

**开放代码：** HTML 获取未完成

**逐条判断：** trying to fetch，无具体失败。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `113:146`：

> Trying to fetch a HTML file TODO:

<a id="row-794"></a>
## 794. 23shades-0794-aahdadjbj

**主题代码：** SATD-M, SATD-Q

**开放代码：** 未使用逻辑

**逐条判断：** unused，未给对象。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `128:134`：

> unused

<a id="row-795"></a>
## 795. 23shades-0795-aagibcfja

**主题代码：** SATD-M, SATD-Q

**开放代码：** 未使用逻辑

**逐条判断：** 独立条目保留。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `160:166`：

> Unused

<a id="row-796"></a>
## 796. 23shades-0796-aagdafeic

**主题代码：** SATD-G, SATD-N

**开放代码：** 实时路径磁盘写入不合适

**逐条判断：** 建议先 memory buffer，退出前写盘；明确实时约束。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `143:239`：

> WARNING: bad realtime practice (writing file) TODO: add to a memory buffer and write before exit

<a id="row-797"></a>
## 797. 23shades-0797-aafafjdfg

**主题代码：** SATD-C, SATD-O

**开放代码：** 形状变换边界诊断缺失

**逐条判断：** channels axis split 时 Reshape 需要 warning/error checking。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `135:200`：

> Warning\/error checking needed for Reshape if channels axis split

<a id="row-798"></a>
## 798. 23shades-0798-aaidjgdji

**主题代码：** SATD-F, SATD-H

**开放代码：** 外部解释器 bug 绕行

**逐条判断：** Python issue11159 未读取，不恢复根因。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `127:169`：

> workaround for bugs.python.org\/issue11159

<a id="row-799"></a>
## 799. 23shades-0799-aahjdgiaa

**主题代码：** SATD-F, SATD-H

**开放代码：** 不必要数值强转的外部绕行

**逐条判断：** GH17886 casts to float，为明确 workaround。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `152:208`：

> Workaround for GH #17886 (unnecessarily casts to float):

<a id="row-800"></a>
## 800. 23shades-0800-aahfigedf

**主题代码：** SATD-F, SATD-H

**开放代码：** 旧 Python 兼容绕行

**逐条判断：** Python2.6。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `133:158`：

> workaround for python 2.6

<a id="row-801"></a>
## 801. 23shades-0801-aaigijhgj

**主题代码：** SATD-F, SATD-H

**开放代码：** 特定 NumPy 版本缺陷绕行

**逐条判断：** NumPy1.9 issue。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `158:185`：

> Workaround NumPy 1.9 issue.

<a id="row-802"></a>
## 802. 23shades-0802-aafdiabdg

**主题代码：** SATD-L, SATD-O

**开放代码：** 日志设施复用不足

**逐条判断：** 希望改 python logger。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `163:199`：

> would be better to use python logger

<a id="row-803"></a>
## 803. 23shades-0803-aaichjjjg

**主题代码：** SATD-B, SATD-G, SATD-I

**开放代码：** 数值溢出风险

**逐条判断：** 改善 precision overflows，未给数值范围。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `138:186`：

> XXX : can do better to avoid precision overflows

<a id="row-804"></a>
## 804. 23shades-0804-aajgccaef

**主题代码：** SATD-D, SATD-N

**开放代码：** 可视化资源打包缺失

**逐条判断：** mpld3 JS libraries 需放 html folder。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `121:168`：

> XXX : include mpld3 js libraries in html folder

<a id="row-805"></a>
## 805. 23shades-0805-aajfiefig

**主题代码：** SATD-D, SATD-E, SATD-J, SATD-Q

**开放代码：** 参数接收范围不足

**逐条判断：** 至少接受 population name。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `116:162`：

> XXX Accept at least the name of the population

<a id="row-806"></a>
## 806. 23shades-0806-aahjgiagj

**主题代码：** SATD-L, SATD-O, SATD-Q

**开放代码：** 说明信息不足

**逐条判断：** add more info，但无法确定是文档还是输出。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `143:160`：

> XXX add more info

<a id="row-807"></a>
## 807. 23shades-0807-aahjfbiha

**主题代码：** SATD-E, SATD-F

**开放代码：** 后向兼容待办

**逐条判断：** 无具体版本或接口。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `145:171`：

> XXX backward compatibility

<a id="row-808"></a>
## 808. 23shades-0808-aadbcegej

**主题代码：** SATD-V

**开放代码：** 方案等效说明

**逐条判断：** both work，无债务方向。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `154:167`：

> XXX both work

<a id="row-809"></a>
## 809. 23shades-0809-aajfhgecg

**主题代码：** SATD-C

**开放代码：** 多线程同时执行不安全

**逐条判断：** 明确不能 simultaneously，保护方案截断。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `116:175`：

> XXX Can't do this simultaneously in multiple threads.  Need

<a id="row-810"></a>
## 810. 23shades-0810-aajficjje

**主题代码：** SATD-A, SATD-N

**开放代码：** 表示模型迁移

**逐条判断：** baseline 改 Foreign clause，领域语义未展开。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `138:183`：

> XXX Convert the baseline to a Foreign clause.

<a id="row-811"></a>
## 811. 23shades-0811-aahciiijc

**主题代码：** SATD-A, SATD-Q

**开放代码：** 复制操作选择待定

**逐条判断：** copy_() 问句。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `131:144`：

> XXX copy_() ?

<a id="row-812"></a>
## 812. 23shades-0812-aahciiijc

**主题代码：** SATD-A, SATD-Q

**开放代码：** 复制操作选择待定

**逐条判断：** 独立记录保留。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `131:144`：

> XXX copy_() ?

<a id="row-813"></a>
## 813. 23shades-0813-aajgefiaf

**主题代码：** SATD-A, SATD-F

**开放代码：** 跨项目复制实现待去重

**逐条判断：** 考虑与 Montage 代码 de-duplicate。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `127:182`：

> XXX de-duplicate this with code from Montage somewhere?

<a id="row-814"></a>
## 814. 23shades-0814-aajficacj

**主题代码：** SATD-H, SATD-I, SATD-J, SATD-Q

**开放代码：** 缺省样本数缺依据

**逐条判断：** 作者直称随意选择，不能视作经验验证值。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `138:187`：

> XXX Default number of samples drawn from my arse.

<a id="row-815"></a>
## 815. 23shades-0815-aajfiebah

**主题代码：** SATD-B, SATD-C, SATD-I

**开放代码：** 操作依赖未约束

**逐条判断：** 没有 CreateTab 时应 disable SimulateModels。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `121:165`：

> XXX Disable SimulateModels without CreateTab

<a id="row-816"></a>
## 816. 23shades-0816-aajgefjja

**主题代码：** SATD-D, SATD-Q

**开放代码：** 条件性投影处理待办

**逐条判断：** 必要时 do projections，未说明判据。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `122:158`：

> XXX do projections here if necessary

<a id="row-817"></a>
## 817. 23shades-0817-aajfiegif

**主题代码：** SATD-A, SATD-D, SATD-Q

**开放代码：** API 暴露不足

**逐条判断：** bqlfn 需更好暴露接口。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `120:158`：

> XXX Expose this API better from bqlfn.

<a id="row-818"></a>
## 818. 23shades-0818-aajghfhbg

**主题代码：** SATD-U

**开放代码：** 未定位的绘图待办

**逐条判断：** add_gridspec(15,1) 只有 XXX，不能认定布局错误。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `126:158`：

> XXX gs = fig.add_gridspec(15; 1)

<a id="row-819"></a>
## 819. 23shades-0819-aageebhag

**主题代码：** SATD-B, SATD-I, SATD-Q

**开放代码：** 输入属性被忽略

**逐条判断：** weight/type 当前忽略，缺少预期解释。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `110:135`：

> XXX ignores weight & type

<a id="row-820"></a>
## 820. 23shades-0820-aajggjjdf

**主题代码：** SATD-B, SATD-I, SATD-Q

**开放代码：** 协方差状态设置不充分

**逐条判断：** inv.source_cov 理论上应正确设置。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `136:191`：

> XXX in theory we should set inv['source_cov'] properly.

<a id="row-821"></a>
## 821. 23shades-0821-aajgcfgdg

**主题代码：** SATD-A, SATD-C, SATD-Q

**开放代码：** 类型检查策略待定

**逐条判断：** test_times 是否 DecodingTime 待判；此处 test 是检查而非单元测试。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `132:194`：

> XXX JRK: Should this test whether test_times if a DecodingTime

<a id="row-822"></a>
## 822. 23shades-0822-aahjfbdfa

**主题代码：** SATD-A, SATD-F, SATD-M

**开放代码：** 语言能力可用后容器替换

**逐条判断：** set 作为 builtin 可依赖后改 set。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `136:201`：

> XXX may convert to set here when we can rely on set being builtin

<a id="row-823"></a>
## 823. 23shades-0823-aahfibidg

**主题代码：** SATD-G, SATD-I, SATD-Q

**开放代码：** 每轮模型重置的性能取舍

**逐条判断：** 每 worker/iteration 重置 LDA 是需求，方案可能慢，不仅一般初始化缺失。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `130:227`：

> XXX might possibly be slow solution; but every worker needs reseted LDA model for every iteration

<a id="row-824"></a>
## 824. 23shades-0824-aajghfgdd

**主题代码：** SATD-A

**开放代码：** 绘图函数结构待改善

**逐条判断：** plot_sensors 需重构才能 cleanly work。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `126:194`：

> XXX MPL. Probably needs a refactor of plot_sensors() to work cleanly

<a id="row-825"></a>
## 825. 23shades-0825-aaicfehca

**主题代码：** SATD-A, SATD-F, SATD-Q

**开放代码：** 新版本库功能可替代实现

**逐条判断：** 新 SciPy sparse.rand，未指明最低版本。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `155:215`：

> XXX newer versions of SciPy have scipy.sparse.rand for this.

<a id="row-826"></a>
## 826. 23shades-0826-aaeieahii

**主题代码：** SATD-I, SATD-V

**开放代码：** 整数类型约束说明

**逐条判断：** offset uint32，未明确溢出或错误。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `119:144`：

> XXX offset type is uint32

<a id="row-827"></a>
## 827. 23shades-0827-aaeiedacj

**主题代码：** SATD-E, SATD-F, SATD-I, SATD-Q

**开放代码：** 库输入窗口支持限制

**逐条判断：** pandas 只接受 variable window cov/corr，具体替代未给。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `112:161`：

> XXX pandas only accepts variable window cov\/corr

<a id="row-828"></a>
## 828. 23shades-0828-aajcadhbi

**主题代码：** SATD-A

**开放代码：** 信噪比计算结构重构

**逐条判断：** 为计算 Rician SNR 重构。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `115:156`：

> XXX Refactor to calculate the Rician SNR:

<a id="row-829"></a>
## 829. 23shades-0829-aajgdidia

**主题代码：** SATD-M

**开放代码：** 清理待办

**逐条判断：** Remove，无对象。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `136:146`：

> XXX Remove

<a id="row-830"></a>
## 830. 23shades-0830-aajfigjji

**主题代码：** SATD-A, SATD-N, SATD-Q

**开放代码：** 返回容器契约待调整

**逐条判断：** singleton list，理由句截断。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `132:192`：

> XXX Return a singleton list; since self._crosscat.similarity

<a id="row-831"></a>
## 831. 23shades-0831-aajghfcje

**主题代码：** SATD-B, SATD-I

**开放代码：** 特定参数分支失败

**逐条判断：** n_pca_components==8 明确失败，根因未知。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `143:184`：

> XXX this fails: or n_pca_components == 8:

<a id="row-832"></a>
## 832. 23shades-0832-aajfibdif

**主题代码：** SATD-B, SATD-I

**开放代码：** 返回数学表示不适当

**逐条判断：** 作者要求 log densities 而非 densities。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `118:184`：

> XXX This is silly.  We should return log densities; not densities.

<a id="row-833"></a>
## 833. 23shades-0833-aajggbgdc

**主题代码：** SATD-D, SATD-E, SATD-Q

**开放代码：** 功能支持推迟

**逐条判断：** 将来应 supported，未知对象。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `130:166`：

> XXX this should be supported someday

<a id="row-834"></a>
## 834. 23shades-0834-aajgfdhgh

**主题代码：** SATD-A, SATD-F

**开放代码：** 重构传播到依赖调用者

**逐条判断：** 重构后 Report._render_raw 同步更新。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `122:190`：

> XXX when it's refactored; Report._render_raw will need to be updated

<a id="row-835"></a>
## 835. 23shades-0835-aajghfhbf

**主题代码：** SATD-A, SATD-F, SATD-M

**开放代码：** 最低版本升级后清理兼容实现

**逐条判断：** matplotlib3.3 成最低版本后替换。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `126:183`：

> XXX when matplotlib 3.3 is min version; replace this with

<a id="row-836"></a>
## 836. 23shades-0836-aajfhhbig

**主题代码：** SATD-A, SATD-G, SATD-Q

**开放代码：** 语句准备时机优化候选

**逐条判断：** 希望提前 prepare statement，未给收益。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `121:180`：

> XXX Would be nice if we could prepare this statement before

<a id="row-837"></a>
## 837. 23shades-0837-aaicicaia

**主题代码：** SATD-B, SATD-I, SATD-Q

**开放代码：** 数值显示/精度原因待查

**逐条判断：** 为何仅2 digits，未明确截断位置。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `148:176`：

> XXX: Check why only 2 digits

<a id="row-838"></a>
## 838. 23shades-0838-aaeidjach

**主题代码：** SATD-D, SATD-E, SATD-N

**开放代码：** JIT 下时间序列索引实现

**逐条判断：** regular Numba 的 timestamp series getitem 待办。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `120:175`：

> XXX: code for timestamp series getitem in regular Numba

<a id="row-839"></a>
## 839. 23shades-0839-aaicgfbda

**主题代码：** SATD-A, SATD-B, SATD-I, SATD-Q

**开放代码：** 缩放约定待审视

**逐条判断：** 目前 variance=n_samples，无明确目标值，不能直接判错。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `134:177`：

> XXX: currently scaled to variance=n_samples

<a id="row-840"></a>
## 840. 23shades-0840-aaeidjejd

**主题代码：** SATD-A, SATD-F, SATD-I, SATD-Q

**开放代码：** 控制流与类型推断关系待查

**逐条判断：** Numba 是否受影响尚为问题。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `112:166`：

> XXX: does control flow affect type inference in Numba?

<a id="row-841"></a>
## 841. 23shades-0841-aagcbggid

**主题代码：** SATD-Q, SATD-U

**开放代码：** 方案选择不确定

**逐条判断：** 不知道哪种最好，无候选内容。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `128:171`：

> XXX: don't know which way would be the best

<a id="row-842"></a>
## 842. 23shades-0842-aajgchffb

**主题代码：** SATD-H, SATD-Q

**开放代码：** 不透明临时实现

**逐条判断：** hack 且不解释原因，缺少可维护依据。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `143:167`：

> XXX: hack; don't ask why

<a id="row-843"></a>
## 843. 23shades-0843-aahjgeiic

**主题代码：** SATD-A, SATD-C, SATD-Q

**开放代码：** 依赖环检测策略未解决

**逐条判断：** 如何正确 catch dependence cycles。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `144:190`：

> XXX: How to catch dependence cycles correctly?

<a id="row-844"></a>
## 844. 23shades-0844-aaibicege

**主题代码：** SATD-A, SATD-I, SATD-J, SATD-Q

**开放代码：** 参数取值依据缺失

**逐条判断：** level 的 good values 如何找未定。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `137:181`：

> XXX: how to find \"good\" values for level ?

<a id="row-845"></a>
## 845. 23shades-0845-aaibjdjdj

**主题代码：** SATD-D, SATD-E

**开放代码：** 字典输入不支持

**逐条判断：** 明确 not handling dictionaries。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `127:158`：

> XXX: not handling dictionnaries

<a id="row-846"></a>
## 846. 23shades-0846-aabgahibh

**主题代码：** SATD-Q, SATD-U

**开放代码：** 方案不满意但对象不明

**逐条判断：** could be smarter。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `145:175`：

> XXX: one could be smarter here

<a id="row-847"></a>
## 847. 23shades-0847-aagbgfjfe

**主题代码：** SATD-A, SATD-C, SATD-I

**开放代码：** 防外部修改的复制需求

**逐条判断：** 返回 copy 保护内部状态，不是代码重复。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `123:179`：

> XXX: return a copy to prevent modification by the caller

<a id="row-848"></a>
## 848. 23shades-0848-aahiefidd

**主题代码：** SATD-A, SATD-C, SATD-I, SATD-Q

**开放代码：** 类型/能力识别策略待定

**逐条判断：** 是否检查 estimator instance，不是明确测试缺失。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `104:156`：

> XXX: should we rather test if instance of estimator?

<a id="row-849"></a>
## 849. 23shades-0849-aaibjdjdc

**主题代码：** SATD-A, SATD-H

**开放代码：** 估计器类别识别临时方案

**逐条判断：** classifier 判定 temporary solution。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `127:196`：

> XXX: Temporary solution to figure out if an estimator is a classifier

<a id="row-850"></a>
## 850. 23shades-0850-aahighbdb

**主题代码：** SATD-A, SATD-B, SATD-I, SATD-J, SATD-Q

**开放代码：** 继承层级配置冲突

**逐条判断：** 与 children class 的 debug flag 冲突。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `129:191`：

> XXX: This conflicts with the debug flag used in children class

<a id="row-851"></a>
## 851. 23shades-0851-aajgdbgid

**主题代码：** SATD-B, SATD-E, SATD-I

**开放代码：** 初始化方法类型边界失败

**逐条判断：** init 为 staticmethod 时失败，后续条件截断。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `128:189`：

> XXX: This is going to fail if the init is a staticmethod; but

<a id="row-852"></a>
## 852. 23shades-0852-aaibijdfi

**主题代码：** SATD-A, SATD-Q

**开放代码：** 可维护性负面评价

**逐条判断：** Ugly 未给具体重构方向。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `146:155`：

> XXX: Ugly

<a id="row-853"></a>
## 853. 23shades-0853-aaeigcjdd

**主题代码：** SATD-A

**开放代码：** 容器类型统一

**逐条判断：** Series/Array 统一为 Array。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `126:159`：

> XXX: unify Series\/Array as Array

<a id="row-854"></a>
## 854. 23shades-0854-aaeieedfd

**主题代码：** SATD-A, SATD-C

**开放代码：** 日期类型检查适配

**逐条判断：** 采用 .values 检查 date type，DatetimeIndex 原因截断。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `119:184`：

> XXX: using .values to check date type since DatetimeIndex returns

<a id="row-855"></a>
## 855. 23shades-0855-aaeachbce

**主题代码：** SATD-H, SATD-I, SATD-N, SATD-V

**开放代码：** 缓存完整性补偿

**逐条判断：** 为保证每项都有 mozci version 重新 cache；未明确计划替代。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `146:215`：

> XXX: We re-cache now just to make sure all items get a mozci version.

<a id="row-856"></a>
## 856. 23shades-0856-aaicaiffi

**主题代码：** SATD-A, SATD-Q

**开放代码：** 职责位置待决策

**逐条判断：** where should this be，无对象。

**材料可用性：** released_comment_only。发布的完整注释及来源字段；未取得注释外源代码。

**结果与限度：** 仅依据注释判断当时待办；未读取仓库后续实现，不判断偿还完成

**原文证据：**

位置 `147:173`：

> XXX: where should this be?

