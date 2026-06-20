---
title: MSGG
aliases:
  - RGB-IR Scene Graph Generation
  - 多模态场景图生成
type: project
created: 2026-06-20
status: active
started: 2026-06-20
deadline: ""
tags:
  - scene-graph-generation
  - rgb-ir
  - multimodal
---
[[20-Projects/Projects|返回 Projects]]

> [!info] 研究方向
> 面向 RGB-IR 多模态场景图生成，重点研究 Proposal 如何服务关系推理，以及关系推理阶段的模态偏好建模。

## 项目导航

- 研究想法：[[30-Research/Ideas/MSGG-Relation-aware Fusion|Relation-aware Fusion 候选设计]]
- 代码分析：[[20-Projects/MSGG/Resources/MM Relation Head Forward 结构分析|MM Relation Head Forward 结构分析]]
- 知识领域：[[40-Knowledge/Computer Vision/Computer Vision|Computer Vision]]

## 研究目标

将光红外多模态融合（RGB-Infrared Fusion）引入 Scene Graph Generation（SGG）任务。

与传统 RGB-IR Fusion 不同，本工作不生成像素级融合图像，而是采用：

Feature-level RGB-IR Fusion + Relation-aware Scene Graph Generation

核心目标：

- 提升低光、夜间、遮挡场景下的场景图生成性能
- 利用 RGB 与 IR 的互补信息增强关系推理能力
- 探索跨模态融合从 Object Perception 向 Relation Reasoning 的扩展

---

## 核心问题

现有 RGB-IR 研究主要关注：

- Object Detection
- Semantic Segmentation
- Image Fusion

而 Scene Graph Generation 更关注：

```text
(subject, predicate, object)
```

例如：

```text
(person, riding, bicycle)
```

现有方法存在两个问题：

### 问题1：目标漏检

在低光、夜间等场景下：

```text
RGB
↓
目标检测性能下降
↓
关系无法预测
```

例如：

```text
person 未检测到
↓
person-riding-bike 无法生成
```

---

### 问题2：关系特征退化

即使：

```text
person ✓
bike ✓
```

检测成功，

但由于：

- 光照不足
- 局部遮挡
- 纹理缺失

导致：

```text
riding
holding
looking at
```

等 Predicate 难以预测。

---

## 核心思想

不同阶段承担不同任务，因此采用不同融合策略：

```text
Proposal Generation ≠ Relation Reasoning
```

因此：

```text
Proposal Fusion 与 Relation-aware Fusion 解耦
```

其中，独立的 ROI Fusion 不再作为单独模块。

原因是，在当前 maskrcnn_benchmark 的 SGG 数据流中，Relation Head 本来就同时依赖：

```text
Object ROI Feature
Union Feature
```

因此 ROI Fusion 与 Relation Fusion 很容易发生在同一阶段，二者边界不清。

更合理的设计是：

```text
Proposal Fusion
+
Relation-aware Fusion
```

---

## 整体框架

```text
RGB Image ─ RGB Backbone/FPN ┐
                              ├─ Proposal Fusion ─ RPN ─ Proposals
IR Image  ─ IR Backbone/FPN  ┘


Proposals
   ↓

RGB FPN ─ ROIAlign ─ F_sub_rgb / F_obj_rgb / F_union_rgb
IR FPN  ─ ROIAlign ─ F_sub_ir  / F_obj_ir  / F_union_ir


Relation-aware Fusion
   ↓

Relation Predictor
(Motif / VCTree / Transformer)
   ↓

Scene Graph
```

图示如下：

![[99-Assets/MSGG/rgb-ir-sgg-framework.png]]

---

## 模块一：Proposal Fusion

### 目标

服务于：

```text
RPN
```

提升：

```text
Object Recall
```

而非关系推理。

---

### 输入

```text
P2_rgb
P3_rgb
P4_rgb
P5_rgb

P2_ir
P3_ir
P4_ir
P5_ir
```

---

### 输出

```text
P2_rpn
P3_rpn
P4_rpn
P5_rpn
```

用于：

```text
RPN
```

---

### 作用

解决：

```text
目标漏检
```

尤其：

- 夜间
- 逆光
- 小目标
- 遮挡

场景。

---

### 初始实现

简单门控融合：

```text
F_rpn = Gate(P_rgb, P_ir)
```

或：

```text
F_rpn = Conv(Concat(P_rgb, P_ir))
```

---

## 模块二：Relation-aware Fusion

### 当前候选设计

这是整个工作的核心创新。

该模块发生在：

```text
union_features 生成之后
Relation Predictor 之前
```

对应 maskrcnn_benchmark 中：

```text
maskrcnn_benchmark/modeling/roi_heads/relation_head/
```

目前模块2先作为一个候选设计保留，核心思路是：

```text
Predicate-specific Modality Preference
```

即不再把模块2理解为普通的 RGB-IR 融合，而是研究：

```text
不同 Predicate 是否存在不同模态依赖性，
模型能否自动学习这种依赖性。
```

详细设计单独记录在：

[[30-Research/Ideas/MSGG-Relation-aware Fusion|模块2：Relation-aware Fusion 候选设计]]

该候选方案的基本形式是先构建：

```text
F_rgb = [F_sub_rgb, F_obj_rgb, F_union_rgb]
F_ir  = [F_sub_ir,  F_obj_ir,  F_union_ir]
```

再学习关系推理过程中的模态偏好，例如：

```text
α = Gate(F_rgb, F_ir)
F_rel = αF_rgb + (1 - α)F_ir
```

进一步版本学习：

```text
A = [α1, α2, ..., αK]
```

其中 `K` 为 Predicate 类别数，用于建模每类关系对应的 RGB/IR 模态偏好。

---

## 损失函数

基础版本：

```text
L = L_rpn + L_box + L_obj + L_rel
```

---

后续可扩展：

### 跨模态一致性

```text
L_align
```

约束：

```text
RGB Relation Feature ≈ IR Relation Feature
```

---

### Predicate-aware Consistency

约束：

```text
Fusion Feature

保持关系语义一致
```

---

## 实验设计

### Baseline 1

RGB-only SGG

---

### Baseline 2

IR-only SGG

---

### Baseline 3

RGB-IR FPN Fusion

统一融合后送入 SGG。

---

### Baseline 4

Proposal Fusion Only

验证：

```text
目标召回提升
```

是否能够提升 SGG。

---

### Baseline 5

Relation-aware Fusion Candidate Only

验证：

```text
候选模块2是否能够增强关系推理
```

效果。

---

### Baseline 6

Shared Gate vs Predicate-specific Gate

验证：

```text
所有关系共享一个 α
```

与：

```text
每个 Predicate 学习独立模态偏好
```

之间的差异。

---

### Analysis

Modality Preference Analysis

观察：

```text
不同 Predicate 的 RGB/IR 偏好是否形成差异
```

用于证明模型是否真的学到了关系语义与模态依赖之间的对应关系。

---

### Ours

- Proposal Fusion

- Relation-aware Fusion Candidate

---

## 预期贡献

### Contribution 1

提出：

```text
RGB-IR Scene Graph Generation
```

任务框架。

---

### Contribution 2

提出：

```text
Task-Decoupled Fusion
```

即：

```text
Proposal Fusion
Relation-aware Fusion
```

解耦设计。

---

### Contribution 3

提出：

```text
Predicate-specific Relation-aware Fusion
```

基于：

```text
F_sub
F_obj
F_union
```

建模关系语义与模态依赖之间的对应关系，使模型能够根据 Predicate 语义学习 RGB/IR 模态偏好。

---

### Contribution 4

验证：

RGB-IR 融合不仅提升目标检测能力，

还能够提升：

```text
Predicate Recognition
Scene Graph Generation
```

性能。

这个版本已经比较接近后续开题报告或论文 Method 部分的雏形，后面还可以进一步细化成网络结构图、模块公式和消融实验设计。
