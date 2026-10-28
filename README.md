# 机器学习与深度学习：图解速查手册

本次草稿 PR 供验收第一批12张原始速查图的修订成果。

- **先看 [12页验收样章 PDF](review/batch01.pdf)**，再看 [逐图处理说明](review/README.md)。
- 新章为简体中文，覆盖网络结构、前向计算、激活、输出与损失、反向传播及一次完整参数更新。
- 本次公开提交仅包括样章、配套 LaTeX、必要样式与审校记录；原 `main.tex` 和原始图像沿用主分支已有版本。
- 92页整书重构工作稿和完整本地源码包已保留在本轮工作区，未包含在本次缩小范围的PR中。

## 编译与核验

需要 XeLaTeX、latexmk、ctex、TikZ/PGFPlots、tcolorbox、常用数学与表格包，以及 Noto Serif/Sans/Mono CJK SC 字体。

```bash
scripts/build.sh batch01
python scripts/verify_math.py
```

生成 `build/batch01.pdf`。本批PDF共12页，正文10页；全部页面已渲染检查，无溢出、缺字或未定义引用。
梯度用有限差分独立核算。详见 `PROGRESS.md`、`docs/MATH_VERIFICATION.json`。

图片库存 `IMAGE_INVENTORY.csv` 共287条，只有本批12张标记详细视觉核查，其余275张待审。
原作者及历史贡献保留于原稿和 `work record.tex`。原图许可尚未逐图核实，本批正文使用独立编写的矢量图表。

**本轮在12张处暂停，等待用户质量验收；不自动开始第二批。全书未完成。**
