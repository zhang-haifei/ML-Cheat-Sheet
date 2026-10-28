# 第四批：数据准备

2026-10-28。逐张完整分辨率查看12张原图（9张done、3张to-do），均保留原资产与可见Chris Albon署名。按用户已确认的新要求连续推进，不设本批验收暂停。

## 内容与新图

新增 `chapters/data-preparation.tex`，十个主题页：样本矩阵、无序类别与独热、有序编码、缺失值、近邻填补、缩放、特征选择、不平衡采样、SMOTE、完整流水线。六幅独立TikZ/PGFPlots矢量图，另有策略表和检查表。图为重新设计，未裁剪、描摹或嵌入原插图。旧正文相应9个独特原图引用移除。

## 科学修订

- 有序数字编码不构成真实程度的倍数尺度；线性模型会额外假定相邻编码间距相等。
- 独热编码补充未知类别、列顺序、截距共线性与模型接口。
- 缺失不等于0；填补只在训练中拟合；删除记录的偏差取决于缺失机制。
- 近邻填补按已观测部分距离寻找训练邻居，k不固定为10；例子等权2近邻填补11，全列中位数46。
- Min–Max范围只保证训练极值区间，新值40变为1.5并非错误；标准化使用分母n，不保证正态分布。
- 特征选择区分过滤、包装、嵌入；选择规则每折训练内学习，重要性不直接等于因果。
- 多数/少数与正/负是不同概念；采样不要求1:1，复制不增加独立对象；仅训练采样，验证测试保持目标分布。
- SMOTE明确少数类邻居、插值公式与类别/离散约束，概率解释需注意改变的先验。

## 可复算性

`python scripts/verify_data.py` 独立复算中位数填补、缺失指示、近邻距离与均值、Min–Max、标准化均值与方差、未知新值、独热与截距关系、SMOTE端点与区间。结果见 `BATCH04_MATH_VERIFICATION.json`。

## 依据

访问于2026-10-28：

- https://scikit-learn.org/stable/modules/preprocessing.html
- https://scikit-learn.org/stable/modules/impute.html
- https://scikit-learn.org/stable/modules/feature_selection.html
- https://scikit-learn.org/stable/common_pitfalls.html
- https://imbalanced-learn.org/stable/common_pitfalls.html

逐图语义、原图问题、新内容位置与替代图路径见 `IMAGE_INVENTORY.csv` 的batch04行。出版和核查状态见构建记录。本批先在本地完成；公开上传未包含在已获准的第二批发布负载中。
