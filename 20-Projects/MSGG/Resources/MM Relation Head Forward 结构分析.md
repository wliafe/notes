---
title: MM Relation Head Forward 结构分析
aliases:
  - MMROIRelationHead forward
type: reading
created: 2026-06-20
status: done
source: maskrcnn_benchmark/modeling/roi_heads/mm_relation_head/mm_relation_head.py
projects:
  - "[[20-Projects/MSGG/MSGG]]"
tags:
  - scene-graph-generation
  - relation-head
  - maskrcnn-benchmark
---
[[20-Projects/MSGG/MSGG|返回 MSGG 项目]]

本文分析 `maskrcnn_benchmark/modeling/roi_heads/mm_relation_head/mm_relation_head.py` 中 `MMROIRelationHead.forward()` 的结构，包括数据流、经过的模块、训练与推理分支，以及当前双模态实现中存在的问题。

## 调用位置

整体调用链如下：

```text
MMGeneralizedRCNN.forward
  -> visible / infrared 分别经过共享 backbone
  -> ProposalFusion 将两路 FPN 特征逐层相加
  -> RPN 生成 proposals
  -> CombinedROIHeads.forward
       -> MM ROI Box Head
       -> MMROIRelationHead.forward
```

`MMGeneralizedRCNN` 将原始的 `visible_features` 和 `infrared_features` 传给 MM ROI Heads。Relation Head 的接口为：

```python
forward(
    visible_features,
    infrared_features,
    proposals,
    targets=None,
    logger=None,
)
```

各输入的含义：

- `visible_features`：可见光图像经过 backbone 得到的多层 FPN 特征。
- `infrared_features`：红外图像经过 backbone 得到的多层 FPN 特征。
- `proposals`：经过 RPN 和 Box Head 处理后的候选目标框。
- `targets`：训练阶段使用的目标框、类别和关系标注。
- `logger`：传给 relation predictor 的日志对象。

## Forward 总体数据流

按设计，Relation Head 的数据流如下：

```text
visible_features / infrared_features
              + proposals / targets
                        |
                        v
              RelationSampling
        生成关系对、关系标签和二值关系矩阵
                        |
            +-----------+-----------+
            |                       |
            v                       v
  BoxFeatureExtractor      RelationFeatureExtractor
    提取目标 ROI 特征          提取关系 Union 特征
            |                       |
            +-----------+-----------+
                        |
                        v
              RelationPredictor
       目标类别细化 + 关系类别预测
                        |
             +----------+----------+
             |                     |
             v                     v
          训练阶段               推理阶段
       LossEvaluator          PostProcessor
```

## 1. 关系对采样

关系对由 `samp_processor` 生成。训练和推理阶段采用不同逻辑。

### 训练阶段

采样过程位于 `torch.no_grad()` 中，不参与梯度计算：

```python
if self.cfg.MODEL.ROI_RELATION_HEAD.USE_GT_BOX:
    proposals, rel_labels, rel_pair_idxs, rel_binarys = (
        self.samp_processor.gtbox_relsample(proposals, targets)
    )
else:
    proposals, rel_labels, rel_pair_idxs, rel_binarys = (
        self.samp_processor.detect_relsample(proposals, targets)
    )
```

- `gtbox_relsample`：使用 Ground Truth Box 采样关系，适用于 PredCls 和 SGCls。
- `detect_relsample`：在检测框中匹配目标并采样关系，适用于 SGDet。

采样输出：

- `proposals`：采样或匹配后的目标框。
- `rel_labels`：每个关系对对应的谓词类别标签。
- `rel_pair_idxs`：形状为 `[num_rel, 2]`，每行表示 `(subject_idx, object_idx)`。
- `rel_binarys`：目标之间是否存在关系的二值矩阵，主要供 VCTree 等模型使用。

### 推理阶段

推理时没有关系标签，调用 `prepare_test_pairs` 构造候选关系对：

```python
rel_labels, rel_binarys = None, None
rel_pair_idxs = self.samp_processor.prepare_test_pairs(
    features[0].device, proposals
)
```

默认会构造所有非自身的有向目标对，例如目标 0 和目标 1 会形成：

```text
0 -> 1
1 -> 0
```

当处于 SGDet 且配置要求目标框重叠时，还会用 IoU 过滤不重叠的目标对。

## 2. 目标 ROI 特征提取

每个 proposal 通过 `box_feature_extractor` 提取目标级视觉特征：

```python
roi_features = self.box_feature_extractor(features, proposals)
```

当前配置使用 `FPN2MLPFeatureExtractor`，内部结构为：

```text
多层 FPN 特征
  -> ROI Pooler
  -> 7 x 7 ROI 特征
  -> Flatten
  -> FC6 + ReLU
  -> FC7 + ReLU
  -> roi_features
```

当 `ROI_BOX_HEAD.MLP_HEAD_DIM=4096` 且属性分支关闭时，每个目标最终得到一个 4096 维特征。

## 3. 可选属性特征分支

当 `MODEL.ATTRIBUTE_ON=True` 时，还会调用 `att_feature_extractor`：

```python
att_features = self.att_feature_extractor(features, proposals)
roi_features = torch.cat((roi_features, att_features), dim=-1)
```

初始化时，Box 和 Attribute 两个 extractor 分别输出一半维度，拼接后恢复为 predictor 需要的完整维度。

当前 MARSG relation 配置中 `ATTRIBUTE_ON=False`，因此不会经过该分支。

## 4. 关系 Union 特征提取

当 `ROI_RELATION_HEAD.PREDICT_USE_VISION=True` 时，调用 `union_feature_extractor`：

```python
union_features = self.union_feature_extractor(
    features, proposals, rel_pair_idxs
)
```

当前配置使用 `RelationFeatureExtractor`。对于每一个 `(subject, object)` 关系对，它执行以下操作：

1. 取出 subject box 和 object box。
2. 计算覆盖两个目标的 Union Box。
3. 在 Union Box 上进行 ROI Pooling，提取 Union 区域视觉特征。
4. 构造 subject 和 object 的二通道矩形空间掩码。
5. 使用 `rect_conv` 对空间掩码进行卷积编码。
6. 将 Union 视觉特征和空间特征融合。
7. 经过 `FC6 + FC7` 得到最终的 `union_features`。

当前 `CAUSAL.SEPARATE_SPATIAL=False`，因此采用直接相加：

```python
union_features = union_vis_features + rect_features
union_features = self.feature_extractor.forward_without_pool(union_features)
```

如果关闭 `PREDICT_USE_VISION`，则不提取 Union 特征：

```python
union_features = None
```

## 5. Relation Predictor

目标特征和 Union 特征最终传入关系预测器：

```python
refine_logits, relation_logits, add_losses = self.predictor(
    proposals,
    rel_pair_idxs,
    rel_labels,
    rel_binarys,
    roi_features,
    union_features,
    logger,
)
```

输出含义：

- `refine_logits`：经过上下文建模后重新预测的目标类别 logits。
- `relation_logits`：每个 subject-object 对的关系类别 logits。
- `add_losses`：predictor 内部产生的附加训练损失。

具体 predictor 由配置项 `ROI_RELATION_HEAD.PREDICTOR` 决定。当前配置选择 `CausalAnalysisPredictor`，并使用：

```yaml
PREDICTOR: "CausalAnalysisPredictor"
CAUSAL:
  CONTEXT_LAYER: "motifs"
  FUSION_TYPE: "sum"
  SEPARATE_SPATIAL: False
  SPATIAL_FOR_VISION: True
  EFFECT_TYPE: "none"
```

### 5.1 Motifs 上下文编码

`roi_features` 首先进入 `LSTMContext`：

```text
roi_features
  -> LSTMContext
  -> obj_dists
  -> obj_preds
  -> edge_ctx
```

- `obj_dists`：上下文细化后的目标类别分布。
- `obj_preds`：预测的目标类别。
- `edge_ctx`：用于关系推理的目标上下文表示。

### 5.2 关系对上下文表示

`edge_ctx` 经过线性映射并拆成 head/tail 表示：

```text
edge_ctx
  -> post_emb
  -> head_rep / tail_rep
  -> 按 rel_pair_idxs 选取 subject 和 object
  -> 拼接 subject/object 表示
  -> post_cat
  -> post_ctx_rep
```

`post_ctx_rep` 是每个关系对的上下文特征。

### 5.3 几何空间编码

predictor 根据两个目标框生成 32 维几何信息，然后通过 MLP 编码：

```text
subject/object box
  -> pair_bbox，32维
  -> Linear(32, 512) + ReLU
  -> Linear(512, 4096) + ReLU
  -> 空间关系特征
```

当前 `SPATIAL_FOR_VISION=True`，空间特征通过逐元素乘法作用到上下文关系特征：

```python
post_ctx_rep = post_ctx_rep * self.spt_emb(pair_bbox)
```

### 5.4 三分支关系分类

`CausalAnalysisPredictor` 包含三个关系分类来源：

- 视觉分支：`union_features -> vis_compress`。
- 上下文分支：`post_ctx_rep -> ctx_compress`。
- 频率分支：subject/object 类别对通过 `FrequencyBias` 查询关系先验。

当前 `FUSION_TYPE="sum"`，最终关系 logits 为：

```text
relation_logits
  = visual_logits
  + context_logits
  + frequency_logits
```

训练时 predictor 还会返回以下辅助损失：

- `auxiliary_ctx`：约束上下文分支独立预测关系。
- `auxiliary_vis`：约束视觉分支独立预测关系。
- `auxiliary_frq`：约束频率分支独立预测关系。
- `binary_loss`：仅在 context layer 返回二值关系预测时产生。

## 6. 训练阶段输出

训练时，`loss_evaluator` 计算主要损失：

```python
loss_relation, loss_refine = self.loss_evaluator(
    proposals,
    rel_labels,
    relation_logits,
    refine_logits,
)
```

主要包括：

- `loss_rel`：关系谓词分类损失。
- `loss_refine_obj`：上下文目标类别细化损失。
- `loss_refine_att`：属性分支开启时的属性分类损失。

随后合并 predictor 返回的附加损失：

```python
output_losses.update(add_losses)
```

最终返回：

```python
return roi_features, proposals, output_losses
```

在当前配置下，`output_losses` 通常包含：

```text
loss_rel
loss_refine_obj
auxiliary_ctx
auxiliary_vis
auxiliary_frq
```

## 7. 推理阶段输出

推理时，预测结果进入 `post_processor`：

```python
result = self.post_processor(
    (relation_logits, refine_logits),
    rel_pair_idxs,
    proposals,
)
```

后处理主要完成：

1. 对目标 logits 做 softmax，生成目标类别和置信度。
2. 对关系 logits 做 softmax，生成关系类别和置信度。
3. 计算三元组分数：

```text
triple_score
  = subject_score
  * relation_score
  * object_score
```

4. 根据三元组分数对关系预测排序。
5. 将预测结果写入 `BoxList`。

主要输出字段为：

```text
pred_labels
pred_scores
rel_pair_idxs
pred_rel_scores
pred_rel_labels
```

最终返回：

```python
return roi_features, result, {}
```

## 当前实现存在的问题

当前 `MMROIRelationHead.forward()` 只修改了函数签名，函数体仍然直接复制自单模态 `ROIRelationHead.forward()`。

函数接收的是：

```python
visible_features
infrared_features
```

但函数体使用的是未定义变量 `features`：

```python
features[0].device
self.box_feature_extractor(features, proposals)
self.att_feature_extractor(features, proposals)
self.union_feature_extractor(features, proposals, rel_pair_idxs)
```

因此当前状态下：

- `visible_features` 没有被使用。
- `infrared_features` 没有被使用。
- `features` 没有定义。
- 运行到相关代码时会触发 `NameError`。
- Relation Head 内部尚未实现 RGB/IR 特征融合。

需要注意的是，RPN 前已经存在 `ProposalFusion`：

```python
proposal_features = tuple(
    visible_feature + infrared_feature
    for visible_feature, infrared_feature
    in zip(visible_features, infrared_features)
)
```

但是这个 `proposal_features` 只传给了 RPN。ROI Box Head 和 Relation Head 接收到的仍然是原始两路特征，因此 RPN 的相加融合结果没有直接进入 Relation Head。

## 结论

从设计上看，`MMROIRelationHead.forward()` 包含以下模块：

```text
RelationSampling
  -> BoxFeatureExtractor
  -> 可选 AttributeFeatureExtractor
  -> RelationFeatureExtractor（Union视觉与空间特征）
  -> RelationPredictor（上下文、视觉、频率分支）
  -> LossEvaluator 或 PostProcessor
```

但从当前代码状态看，它仍是单模态 Relation Head 的未完成迁移版本。双模态输入已经传到函数接口，却尚未定义两路特征在目标 ROI 特征和关系 Union 特征阶段应如何融合，因此当前代码不能形成可运行的双模态 Relation Head。
