# 构建、算例复核与项目维护

本页供希望修改正文、重绘图解或复算例子的读者使用。书籍介绍与阅读入口见[项目首页](../README.md)。下列命令均在项目根目录运行。

## 构建与验证

需要XeLaTeX、latexmk、TeX Live中文/扩展/科学组件，以及Noto Serif/Sans/Mono CJK SC和Latin Modern字体。

```bash
scripts/build.sh
python -m pip install numpy pymupdf
python scripts/verify_all.py
python scripts/audit_build.py main
python scripts/audit_navigation.py
python scripts/audit_layout.py
python scripts/package_source.py
python scripts/check_source_package.py
```

构建结果在 `build/main.pdf`。`verify_all.py`统一运行各章数值复核；`audit_build.py`检查构建日志、输入依赖、图源和PDF链接；`audit_navigation.py`核对主题条目、页码、PDF目的位置与书签；`audit_layout.py`筛查页尾留白供人工复查；`package_source.py`生成不含PDF、临时文件和Git历史的源码包。正常TeX Live安装无需工作区专用路径，托管环境已有配置则由构建脚本自动加载。

从源码包全新解压后也可运行上述命令。打包脚本自动创建 `review/`；完整写出归档后才替换当前ZIP，失败时保留上一份有效文件。
`check_source_package.py`将当前ZIP解压到临时目录，核对重新打包的字节一致性，并验证缺失输入或写入中断时保留原包。

## 找到对应的算例

各脚本输出构造算例的数值检查；图形由LaTeX编译。具体核验范围见脚本断言与[复算结果](MATH_CHECKS.json)。

| 正文主题 | 复核入口 |
|---|---|
| 第1章：拟合、泛化与偏差—方差 | [verify_foundations.py](../scripts/verify_foundations.py) |
| 第2章：填补、缩放与采样 | [verify_data.py](../scripts/verify_data.py) |
| 第3章：缺失机制与特征筛选 | [verify_reliability.py](../scripts/verify_reliability.py) |
| 第4章：分类、ROC与回归指标 | [verify_evaluation.py](../scripts/verify_evaluation.py) |
| 第5章：搜索、概率与区间 | [verify_diagnostics.py](../scripts/verify_diagnostics.py) |
| 第6章及附录A：建模工具、矩阵与梯度 | [verify_tools_math.py](../scripts/verify_tools_math.py) |
| 第7章：线性模型与近邻 | [verify_linear.py](../scripts/verify_linear.py) |
| 第8章：树与集成 | [verify_trees.py](../scripts/verify_trees.py) |
| 第9--10章：核、聚类与PCA | [verify_kernel_unsupervised.py](../scripts/verify_kernel_unsupervised.py) |
| 第11章：神经网络前反向与参数更新 | [verify_math.py](../scripts/verify_math.py) |
| 第12章：优化器、初始化与训练规则 | [verify_training.py](../scripts/verify_training.py) |
| 第13章及第17章任务头：稳定计算与参数数 | [verify_numerics.py](../scripts/verify_numerics.py) |
| 第14章：卷积、形状与归一化 | [verify_cnn.py](../scripts/verify_cnn.py) |
| 第15--16章：TF-IDF、循环与注意力 | [verify_sequence.py](../scripts/verify_sequence.py) |
| 跨章：多标签、感知机、OOB、CDF、SE、VIF与校准 | [verify_review.py](../scripts/verify_review.py) |

15组基础复算仅需NumPy。另提供可选的[PyTorch接口核对](../scripts/check_torch_conventions.py)：在已安装PyTorch的环境运行以下命令，检查BN/LN、卷积与池化、RNN/LSTM/GRU、稳定损失和单步SGD。2026-11-02以PyTorch 2.9.0+cpu、CPU float64实测，结果见[TORCH_CHECKS.json](TORCH_CHECKS.json)。

```bash
python scripts/check_torch_conventions.py
```

## 文件组织

| 路径 | 用途 |
|---|---|
| `main.tex` | 唯一整书入口 |
| `chapters/` | 正文、附录、阅读导航 |
| `figures/` | 独立矢量图源和数值CSV |
| `styles/` | 中文字体、颜色与版式 |
| `scripts/` | 构建、数值复核、审计与打包 |
| `docs/` | 当前验证及审校说明 |
| `review/` | 当前整书PDF与源码包 |

仓库保留当前正文、全部图源、样式、构建与验证脚本、必要审校说明，以及一份PDF和源码包。构建中间文件、预览图、旧稿和会话记录均不纳入交付。
