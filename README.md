最新规则：用户明确批准第二批样章及配套文件公开更新PR #1，取消逐批暂停验收；后续按约两小时会话检查点推进并保存。下文原逐批验收停点不再适用。

# 机器学习与深度学习：图解速查手册

面向初学者的中文图解参考书，按每批10–15张原图推进。

- [第二批13页样章：稳定训练](review/batch02.pdf) · [第二批说明](review/batch02.md)（已完成）
- [第一批12页样章：神经网络基础](review/batch01.pdf) · [第一批说明](review/README.md)（用户已验收）

第二批接续讲解批量、SGD、动量、Adam、梯度消失、初始化、Dropout与提前停止。
最终选用的原始插图全部换为独立图表；原资产与历史署名保留。当前累计详细审查24/287张，全书尚未完成。

本分支公开范围为批次样章、支持LaTeX和审校记录。原main.tex与原始图像仍沿用主分支版本；整书重构和104页工作稿保存在本地，未包含于此PR。

## 构建与核验

需要XeLaTeX、latexmk、ctex、TikZ/PGFPlots、tcolorbox、常用数学与表格包，以及Noto Serif/Sans/Mono CJK SC字体。

```bash
scripts/build.sh batch01
scripts/build.sh batch02
python scripts/verify_math.py
python scripts/verify_training.py
```

输出build/batch01.pdf与build/batch02.pdf。两份独立样章均无Overfull、Underfull、缺字或未定义引用，均已渲染检查。

图片库存见IMAGE_INVENTORY.csv；第二批科学修订与核验见docs/BATCH02_AUDIT.md。原作者及贡献记录保留在原稿和work record.tex。

继续按约两小时会话推进；草稿PR不合并main。
