# 机器学习与深度学习：图解速查手册

面向初学者的中文图解参考书。原项目作者：张海飞、郭金珊、任露芹、李慧、朱靖、朱弘毅。项目始于2020年，现持续编校、独立补图与重排。

**当前为154页工作稿，17个主章节；尚未定稿。** 正文使用78份独立TikZ/PGFPlots图源和正文表格，当前入口不直接嵌入原插图。287张原资产均已至少初筛，其中159张详细核查、128张仅初筛。

## 阅读与进度

- [154页整书工作稿](review/handbook-working-draft.pdf)，从 `main.tex` 构建为 `build/main.pdf`；本地副本位于 `/workspace/output/`。
- 14份阶段PDF快照在 `review/`；当前公开交付状态见 `PROGRESS.md`。
- 阶段PDF是当时快照；共享章节继续修订后，重新编译旧批入口可能增加内容或改变页数。
- 阅读路线、符号说明、方法比较和可点击主题页码均在整书中。
- 进度：[PROGRESS.md](PROGRESS.md)；编排：[EDITORIAL_PLAN.md](EDITORIAL_PLAN.md)；逐图库存：[IMAGE_INVENTORY.csv](IMAGE_INVENTORY.csv)；审校证据：`docs/BATCHNN_*`。

## 构建

需要XeLaTeX、latexmk、TeX Live中文/扩展/科学组件，以及开源Noto Serif/Sans/Mono CJK SC字体，西文字体为Latin Modern。

```bash
scripts/build.sh main
scripts/build.sh batch14
```

`batch01`至`batch14`均为独立入口。脚本在仓库根目录运行XeLaTeX并将产物写入 `build/`。托管环境若存在 `/workspace/setup/latex-env.sh` 会自动加载；正常TeX Live安装不需要这个专用路径。

数学复核需要Python 3、NumPy；库存维护需要Pillow，PDF审计需要PyMuPDF。可按需要安装：

```bash
python -m pip install numpy pillow pymupdf
python scripts/verify_math.py
python scripts/verify_numerics.py
python scripts/verify_reliability.py
python scripts/audit_build.py main
```

其余 `scripts/verify_*.py` 分别核对各章小算例。审计只在构建结束后运行，会拒绝比源码/日志旧或不完整的PDF。库存刷新用 `python scripts/refresh_inventory.py`，保留人工笔记，不自动推断图片语义。

## 文件组织

```text
main.tex / batchNN.tex     整书与阶段入口
chapters/                 正文、附录与阅读导航
styles/handbook.sty        共享中文字体、颜色和版式
figures/                  独立矢量图与数值CSV
scripts/                  构建、库存与数值/构建审计
docs/                     批次审校、验证结果与筛查记录
review/                   阶段PDF快照
build/ / work/            构建及临时校样，不入Git
done/ to-do/ illustration/ 原始图像，保持原样
work record.tex           历史贡献记录，保留不改
```

原始主稿在Git历史与本地 `archive/main-2021.tex` 快照中保留。当前源码包只需新正文、图源和构建支持即可编译，不依赖原插图或旧稿快照。

原资产及可见署名未删除；原图授权与中文改写贡献者尚未逐图核实，详情记在库存。当前工作稿不声称已完成全库存科学审校或最终出版许可审查。
