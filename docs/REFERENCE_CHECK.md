# 参考入口核对

2026-10-29。PDF有37个外部URI注释、35个不同地址；跨行链接可产生多个注释。本次用网页检索工具逐一打开入口并检查标题/来源类型；重定向另跟进目标页。32个地址已解析（包括新增4个主题入口及原有5个重定向目标），1个只确认重定向，2个受访问限制或超时影响。此处记录工具观察，不作未来可达性保证，也不把“能打开”当作全文科学审定。

DBSCAN论文改用可读取的AAAI官方CDN。LSTM的正式DOI返回403，Stanford教材入口超时，均保留原引文。PyTorch stable是浮动别名；工具本次返回的版本信息不等于本项目安装或测试了该框架版本。

| PDF入口 | 工具观察 | 解析目标或说明 |
|---|---|---|
| [cdn.aaai.org / KDD96-037.pdf](https://cdn.aaai.org/KDD/1996/KDD96-037.pdf) | 已解析 | 旧地址工具不可读取；已替换为AAAI官方CDN，论文6页可读取 |
| [arxiv.org / 1301.3781](https://arxiv.org/abs/1301.3781) | 已解析 |  |
| [arxiv.org / 1406.1078](https://arxiv.org/abs/1406.1078) | 已解析 |  |
| [arxiv.org / 1412.6980](https://arxiv.org/abs/1412.6980) | 已解析 |  |
| [arxiv.org / 1502.01852](https://arxiv.org/abs/1502.01852) | 已解析 |  |
| [arxiv.org / 1512.03385](https://arxiv.org/abs/1512.03385) | 已解析 |  |
| [arxiv.org / 1706.03762](https://arxiv.org/abs/1706.03762) | 已解析 |  |
| [arxiv.org / 1711.05101](https://arxiv.org/abs/1711.05101) | 已解析 |  |
| [d2l.ai / 主页](https://d2l.ai/) | 已解析 |  |
| [d2l.ai / backprop.html](https://d2l.ai/chapter_multilayer-perceptrons/backprop.html) | 已解析 |  |
| [docs.pytorch.org / 主页](https://docs.pytorch.org/docs/stable/) | 重定向后已解析 | [目标](https://docs.pytorch.org/docs/2.15/)；stable为浮动入口；本次工具返回2.15文档 |
| [docs.pytorch.org / torch.nn.BCEWithLogitsLoss.html](https://docs.pytorch.org/docs/stable/generated/torch.nn.BCEWithLogitsLoss.html) | 重定向后已解析 | [目标](https://docs.pytorch.org/docs/2.15/generated/torch.nn.BCEWithLogitsLoss.html)；stable为浮动入口；本次工具返回2.15文档 |
| [docs.pytorch.org / torch.nn.CrossEntropyLoss.html](https://docs.pytorch.org/docs/stable/generated/torch.nn.CrossEntropyLoss.html) | 重定向后已解析 | [目标](https://docs.pytorch.org/docs/2.15/generated/torch.nn.CrossEntropyLoss.html)；stable为浮动入口；本次工具返回2.15文档 |
| [docs.pytorch.org / torch.nn.Dropout.html](https://docs.pytorch.org/docs/stable/generated/torch.nn.Dropout.html) | 重定向后已解析 | [目标](https://docs.pytorch.org/docs/2.15/generated/torch.nn.Dropout.html)；stable为浮动入口；本次工具返回2.15文档 |
| [docs.pytorch.org / torch.optim.Adam.html](https://docs.pytorch.org/docs/stable/generated/torch.optim.Adam.html) | 重定向后已解析 | [目标](https://docs.pytorch.org/docs/2.15/generated/torch.optim.Adam.html)；stable为浮动入口；本次工具返回2.15文档 |
| [docs.pytorch.org / nn.init.html](https://docs.pytorch.org/docs/stable/nn.init.html) | 仅确认重定向 | [目标](https://docs.pytorch.org/docs/2.15/nn.init.html)；stable入口可读取；目标页未能由工具解析 |
| [docs.pytorch.org / transfer_learning_tutorial.html](https://docs.pytorch.org/tutorials/beginner/transfer_learning_tutorial.html) | 已解析 |  |
| [doi.org / neco.1997.9.8.1735](https://doi.org/10.1162/neco.1997.9.8.1735) | 访问受限 | 工具收到403；保留正式DOI，不据此认定链接失效 |
| [imbalanced-learn.org / 主页](https://imbalanced-learn.org/stable/) | 已解析 |  |
| [jmlr.org / bergstra12a.html](https://jmlr.org/papers/v13/bergstra12a.html) | 已解析 |  |
| [jmlr.org / srivastava14a.html](https://jmlr.org/papers/v15/srivastava14a.html) | 已解析 |  |
| [keras.io / 主页](https://keras.io/api/callbacks/early_stopping/) | 已解析 |  |
| [mml-book.github.io / 主页](https://mml-book.github.io/) | 已解析 |  |
| [nlp.stanford.edu / 主页](https://nlp.stanford.edu/IR-book/) | 待复查 | 工具两次超时；保留教材作者网站 |
| [scikit-learn.org / common_pitfalls.html](https://scikit-learn.org/stable/common_pitfalls.html) | 已解析 |  |
| [scikit-learn.org / sklearn.metrics.r2_score.html](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.r2_score.html) | 已解析 |  |
| [scikit-learn.org / sklearn.metrics.roc_auc_score.html](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.roc_auc_score.html) | 已解析 |  |
| [scikit-learn.org / user_guide.html](https://scikit-learn.org/stable/user_guide.html) | 已解析 |  |
| [www.deeplearningbook.org / 主页](https://www.deeplearningbook.org/) | 已解析 |  |
| [www.statlearning.com / 主页](https://www.statlearning.com/) | 已解析 |  |
| [zh.d2l.ai / 主页](https://zh.d2l.ai/) | 已解析 |  |
| [docs.pytorch.org / BatchNorm2d](https://docs.pytorch.org/docs/stable/generated/torch.nn.BatchNorm2d.html) | 重定向后已解析 | 工具返回2.15文档；核对统计轴、方差分母、运行统计与评估模式 |
| [docs.pytorch.org / LayerNorm](https://docs.pytorch.org/docs/stable/generated/torch.nn.LayerNorm.html) | 重定向后已解析 | 工具返回2.15文档；核对normalized_shape末尾轴与训练/评估统计 |
| [docs.pytorch.org / GRU](https://docs.pytorch.org/docs/stable/generated/torch.nn.GRU.html) | 重定向后已解析 | 工具返回2.15文档；明确对照原始写法与PyTorch重置门位置及偏置位置 |
| [scikit-learn.org / TF-IDF](https://scikit-learn.org/stable/modules/feature_extraction.html#tfidf-term-weighting) | 已解析 | 核对原始计数、平滑IDF、L2归一化与分词器边界 |

补充核对：[Cambridge第9章Linear Predictors](https://www.cambridge.org/core/books/abs/understanding-machine-learning/linear-predictors/FF366AA369F369BA571D934AF66EC412)对应2014年Shalev-Shwartz与Ben-David教材的线性预测器章节；本书的感知机继续阅读入口据此核对。AdamW、残差网络、注意力与Word2Vec等论文的arXiv入口标题/作者/年代与引文相符。

[Keras EarlyStopping文档](https://keras.io/api/callbacks/early_stopping/)明确区分停止与恢复最佳权重，当前默认restore_best_weights为False；本书要求检查恢复规则的说明与之相符。

本次复查原有3个未完整解析入口：Stanford教材主页及官方HTML/PDF入口仍超时，LSTM正式DOI仍403，nn.init仍只确认stable重定向而未解析目标。另核对Cho等2014年论文的官方arXiv HTML，确认重置门与候选状态的定义。保留正式入口，不以未核验镜像替换。
