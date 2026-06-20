---
title: MSGG Relation-aware Fusion
aliases:
  - 模块2 Relation-aware Fusion 设计
  - Predicate-specific Modality Preference
type: idea
created: 2026-06-20
status: exploring
projects:
  - "[[20-Projects/MSGG/MSGG]]"
tags:
  - scene-graph-generation
  - multimodal-fusion
  - relation-reasoning
---
[[30-Research/Ideas/Ideas|返回 Ideas]] · [[20-Projects/MSGG/MSGG|返回 MSGG 项目]]

## 设计定位

该文件记录模块2的一个候选设计思路：

```text
Relation-aware Fusion
+
Predicate-specific Modality Preference
```

该方案不是把 RGB 和 IR 做通用融合，而是关注一个更具体的关系推理问题：

```text
不同 Predicate 是否存在不同的模态依赖性？

如果存在，模型能否自动学习这种依赖性？
```

因此，模块2的目标不是提升目标检测，而是服务于：

```text
Predicate Prediction
Scene Graph Generation
```

---

## 研究现象

对于同一个目标对：

```text
(subject, object)
```

关系预测通常依赖：

```text
F_sub
F_obj
F_union
```

但是 RGB 与 IR 提供的信息并不相同。

RGB 更擅长提供：

- 纹理
- 颜色
- 外观
- 局部细节

IR 更擅长提供：

- 目标边界
- 热特征
- 低光鲁棒性
- 结构信息

因此，不同关系可能依赖不同模态。

例如：

```text
near
inside
crossing
connected to
```

与：

```text
holding
riding
loading
```

对 RGB/IR 信息的需求并不相同。

---

## 核心假设

传统融合通常可以抽象为：

```text
F_rel = Fusion(F_rgb, F_ir)
```

这种方式隐含假设：

```text
所有 Predicate 共享同一个融合策略
```

但在关系推理中，这一假设并不合理。

更合理的假设是：

```text
Predicate-specific Modality Preference
```

即：

```text
不同 Predicate 具有不同模态偏好
```

模块2希望让模型学习：

```text
当前关系推理应该更多相信 RGB

还是

更多相信 IR
```

---

## 关系特征构建

Proposal 经过 RGB/IR 两路 ROIAlign 后，分别得到 subject、object 与 union 三类特征。

RGB Relation Feature：

```text
F_rgb = [
    F_sub_rgb,
    F_obj_rgb,
    F_union_rgb
]
```

IR Relation Feature：

```text
F_ir = [
    F_sub_ir,
    F_obj_ir,
    F_union_ir
]
```

其中：

- `F_sub` 表示 subject 区域特征
- `F_obj` 表示 object 区域特征
- `F_union` 表示 subject-object 联合区域特征

---

## 设计反思：为什么不直接做 Predicate-aware Gate

一个直观想法是直接为每个 Predicate 学习一个模态权重：

```text
A ∈ R^K
```

即：

```text
A = [α_near, α_inside, α_crossing, ...]
```

然后尝试构造：

```text
F_p = α_p F_rgb + (1 - α_p)F_ir
```

这个想法在理论上可以表达：

```text
不同 Predicate 具有不同模态偏好
```

但放到 SGG 框架中并不自然。

因为 VCTree、Motif 等关系头的基本推理流程是：

```text
输入一个关系特征
↓
输出 K 个 predicate 分数
```

即：

```text
F_rel
↓
VCTree / Motif
↓
[near, inside, crossing, ...]
```

而不是：

```text
K 个关系特征
↓
VCTree / Motif
```

如果为每个 Predicate 都构造一个融合特征，就会变成：

```text
F_near
F_inside
F_crossing
...
↓
关系头
```

这会引入两个问题：

- 结构上不符合现有 SGG 关系头的输入形式
- 逻辑上容易形成 `predicate -> fusion -> predicate` 的循环依赖

因此，核心科学假设应该重新表述为：

```text
不同关系具有不同模态偏好
```

但这不等于：

```text
每个关系类别都显式维护一个 α
```

更合理的做法是先根据当前 subject-object pair 的上下文完成融合，再由关系头预测 Predicate。

---

## 方案1：Relation Context-aware Gate（最推荐）

该方案不预测：

```text
α_near
α_inside
α_crossing
...
```

而是预测当前 subject-object pair 的模态融合权重：

```text
α = Gate(F_sub, F_obj, F_union)
```

其中：

```text
α ∈ [0, 1]
```

表示当前 pair 在关系推理时对 RGB 的依赖程度。

最终融合为：

```text
F_rel = αF_rgb + (1 - α)F_ir
```

然后送入现有关系头：

```text
F_rel
↓
VCTree / Motif / Transformer
↓
Predicate Prediction
```

这样逻辑链条变成：

```text
pair feature
↓
fusion
↓
predicate prediction
```

而不是：

```text
predicate
↓
fusion
↓
predicate
```

例如：

```text
ship + harbor
↓
α = 0.3
```

表示 IR 占主导。

```text
person + bicycle
↓
α = 0.8
```

表示 RGB 占主导。

这里的 `α` 不是由 Predicate 直接决定，而是由当前 pair context 决定。

训练完成后，再按照 Predicate 对样本进行分组统计：

```text
Preference(predicate_k) = mean(α | predicate = k)
```

例如：

```text
near   -> mean(α) = 0.42
inside -> mean(α) = 0.33
riding -> mean(α) = 0.78
```

这样仍然可以得到：

```text
不同 Predicate 具有不同模态偏好
```

但网络结构更加符合 SGG 推理流程，也能直接嵌入 Motif/VCTree 框架。

---

## 方案2：Predicate Prototype（高级版本）

该方案可以作为后续升级方向。

为每个 Predicate 学习一个 prototype：

```text
P_near
P_inside
P_crossing
...
```

融合模块先输出统一的关系特征：

```text
F_rel
```

然后计算 `F_rel` 与各个 Predicate prototype 的相似度：

```text
score_k = sim(F_rel, P_k)
```

即：

```text
F_rel
↓
sim(F_rel, P_near)
sim(F_rel, P_inside)
sim(F_rel, P_crossing)
...
↓
Predicate Scores
```

在这个结构中，Predicate-specific Modality Preference 不再通过显式的 `α_k` 表达，而是隐含在 prototype 表征中。

例如：

```text
P_near
```

可能学习到更偏 IR 的空间结构信息。

```text
P_riding
```

可能学习到更偏 RGB 的外观与交互细节。

该方案表达能力更强，也更接近部分近年关系推理论文中的 prototype / prompt / semantic anchor 思路。

但它的实现难度更高，需要额外考虑：

- prototype 初始化
- prototype 与类别语义的对齐
- 长尾 Predicate 的 prototype 学习稳定性
- 与现有 Motif/VCTree 分类头的兼容方式

因此更适合作为后续扩展，而不是当前阶段的首选实现。

---

## 方案3：Subject/Object/Union 分支 Gate（最符合当前框架）

当前框架中已经显式存在：

```text
F_sub_rgb
F_obj_rgb
F_union_rgb

F_sub_ir
F_obj_ir
F_union_ir
```

因此可以分别为 subject、object、union 三类关系输入学习模态权重：

```text
α_sub
α_obj
α_union
```

对应融合为：

```text
F_sub = α_sub F_sub_rgb + (1 - α_sub)F_sub_ir
```

```text
F_obj = α_obj F_obj_rgb + (1 - α_obj)F_obj_ir
```

```text
F_union = α_union F_union_rgb + (1 - α_union)F_union_ir
```

然后将融合后的三类特征送入关系头：

```text
[F_sub, F_obj, F_union]
↓
VCTree / Motif / Transformer
↓
Predicate Prediction
```

该方案非常符合关系推理中的特征分工：

```text
F_sub / F_obj
↓
主要编码实体信息
```

```text
F_union
↓
主要编码交互区域与关系信息
```

模型可能学习到：

```text
α_sub   = 0.8
α_obj   = 0.8
α_union = 0.3
```

这可以解释为：

```text
实体识别更依赖 RGB
关系区域更依赖 IR
```

相比“每个 Predicate 一个 α”，该解释更自然，也更贴合当前已有的 `sub / obj / union` 输入结构。

---

## 推荐主线

当前阶段建议将模块2从：

```text
Predicate-aware Gate
```

调整为：

```text
Relation Context-aware Modality Gate
```

核心流程为：

```text
(F_sub, F_obj, F_union)
↓
Gate Network
↓
α 或 [α_sub, α_obj, α_union]
↓
RGB/IR Fusion
↓
VCTree / Motif
↓
Predicate Prediction
```

推荐优先实现两个版本：

### 版本 A：Pair-level Gate

学习一个当前 pair 共享的模态权重：

```text
α = Gate(F_sub, F_obj, F_union)
```

优点是结构简单，适合作为主实验或强 baseline。

### 版本 B：Sub/Obj/Union Gate

学习三个分支级模态权重：

```text
[α_sub, α_obj, α_union] = Gate(F_sub, F_obj, F_union)
```

优点是更贴合现有 SGG relation feature 结构，解释性也更强。

---

## 可解释性分析

训练完成后，不直接解释 `α_k`，而是统计不同 Predicate 样本上的平均 gate 值。

对于 Pair-level Gate：

```text
Preference(predicate_k) = mean(α_i | y_i = predicate_k)
```

对于 Sub/Obj/Union Gate：

```text
Preference_sub(predicate_k)   = mean(α_sub_i | y_i = predicate_k)
Preference_obj(predicate_k)   = mean(α_obj_i | y_i = predicate_k)
Preference_union(predicate_k) = mean(α_union_i | y_i = predicate_k)
```

然后分析：

- 哪些 Predicate 更依赖 RGB
- 哪些 Predicate 更依赖 IR
- 哪些 Predicate 需要双模态共同作用
- `sub / obj / union` 三个分支的模态偏好是否存在差异
- 这种偏好是否符合关系语义和场景条件

该分析可以作为论文中的额外证据，用来证明模型不是盲目融合 RGB/IR，而是学习到了：

```text
关系语义与模态依赖之间的对应关系
```

---

## 实验验证

建议至少包含以下对比：

### 1. Fixed Fusion

固定融合 RGB/IR，不学习动态权重。

用于验证简单多模态融合是否有效。

---

### 2. Pair-level Relation Context-aware Gate

所有 pair 学习一个由关系上下文决定的 `α`：

```text
α = Gate(F_sub, F_obj, F_union)
```

用于验证 relation-aware adaptive fusion 是否有效。

---

### 3. Sub/Obj/Union Gate

分别学习：

```text
α_sub
α_obj
α_union
```

用于验证实体区域与关系区域是否具有不同模态偏好。

---

### 4. Predicate Prototype

作为高级扩展实验，验证 Predicate prototype 是否能进一步增强关系语义建模。

---

### 5. Modality Preference Analysis

按照 Predicate 对 gate 值进行分组统计或可视化。

目标是证明：

```text
不同关系确实表现出不同模态依赖性
```

但这个结论来自模型在 pair context 上学习到的融合行为，而不是来自先验指定的 `α_k`。

---

## 一句话概括

Relation-aware Fusion 不应该强行设计成“每个 Predicate 一个融合权重”，而应该让模型根据当前 subject-object pair 的关系上下文自适应融合 RGB/IR，再通过统计不同 Predicate 样本上的 gate 分布证明：

```text
关系语义与模态依赖之间存在可学习的对应关系
```
