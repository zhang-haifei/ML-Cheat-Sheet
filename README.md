# 机器学习与深度学习：图解速查手册

面向初学者的中文图解参考书，将概念、独立矢量图、公式与可复算的小例子放在一起。当前为154页工作稿、17个主章节、78份TikZ/PGFPlots图源，仍在科学与编辑复审。

- [阅读整书PDF](review/handbook-working-draft.pdf)
- [下载可编译源码包](review/handbook-source.zip)
- [当前进度](PROGRESS.md) · [编排与待办](EDITORIAL_PLAN.md)

## 构建与验证

需要XeLaTeX、latexmk、TeX Live中文/扩展/科学组件，以及Noto Serif/Sans/Mono CJK SC和Latin Modern字体。

```bash
scripts/build.sh
python -m pip install numpy pymupdf
python scripts/verify_all.py
python scripts/audit_build.py main
python scripts/package_source.py
```

构建结果在 `build/main.pdf`。`verify_all.py`统一运行各章数值复核；`audit_build.py`检查构建日志、输入依赖、图源和PDF链接；`package_source.py`生成不含PDF、临时文件和Git历史的源码包。正常TeX Live安装无需工作区专用路径，托管环境已有配置则由构建脚本自动加载。

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

已移除不再使用的原图、旧稿、贡献流水和阶段样章。当前构建只依赖上述文件；Git提交历史保留用于追溯。
