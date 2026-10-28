# 第一批样章续作

- 目标：初学者中文《机器学习与深度学习：图解速查手册》，术语附英文；先科学正确，再追求简洁、连贯和可查。
- 本次公开PR仅包含12图对应的样章、支持LaTeX和审校记录。`main.tex`仍为主分支原稿；完整本地重构另有保存，不能据本分支宣称已改完整书。
- 先读 `PROGRESS.md`、`EDITORIAL_PLAN.md`、`review/README.md` 和 `IMAGE_INVENTORY.csv`。
- 用户要求每批10–15张后暂停。第一批12张已处理，等待质量验收。未验收前只修本批，不开第二批。
- 用户明确批准本批PDF、配套LaTeX和审校记录上传至公开仓库zhang-haifei/ML-Cheat-Sheet的work分支并建草稿PR，不合并main；该范围无需重复询问。
- 必须看实际图片再写语义；detailed_visual才表示详细视觉核查。未审图片不能根据文件名杜撰。保留原图及署名，许可未明不得当作已获出版授权。
- 样章入口 `batch01.tex`，章节 `chapters/neural-foundations.tex`，共享样式 `styles/handbook.sty`，图源在 `figures/`。
- 构建 `scripts/build.sh batch01`；数学复核 `python scripts/verify_math.py`。XeLaTeX与Noto CJK字体。
- 编译后检查错误、缺字、溢出、引用，并渲染看PDF。临时文件放work，构建放build，不入Git。
- 保留原作者与 `work record.tex`，更新新进度不覆盖历史。完成一批须提交可审阅的成果并准确记录未完成项。
