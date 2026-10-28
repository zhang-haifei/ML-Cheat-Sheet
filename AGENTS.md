最新规则：用户明确批准第二批样章及配套文件公开更新PR #1，取消逐批暂停验收；后续按约两小时会话检查点推进并保存。下文原逐批验收停点不再适用。

# 批次样章续作

- 目标：初学者中文《机器学习与深度学习：图解速查手册》，术语附英文；科学正确、解释清楚、图文连贯、方便速查。
- 最终采用的原始插图全部替换为独立绘图；原资产和署名保留审计。冗余或淘汰图无需全部收录。
- 第一批12图已获用户验收；第二批12图完成待验收。每批10–15张，未获第二批验收前不开始第三批。
- 先读PROGRESS.md、EDITORIAL_PLAN.md、review/batch02.md与IMAGE_INVENTORY.csv。必须实际查看图片再判断语义，detailed_visual才代表详细视觉核查。
- 本PR只含批次样章、配套LaTeX和记录；main.tex仍是主分支原稿，整书重构另有本地检查点，不可把本分支视为完成书稿。
- 用户已授权将批次样章与记录上传公开仓库的work分支并建草稿PR，后续明确允许按既定计划继续；相同流程不重复询问，不合并main。更广整书源码曾被审批拒绝，未另获授权不扩大公开范围。
- 入口batch01.tex、batch02.tex；章节chapters/neural-foundations.tex、chapters/training-stability.tex；共享styles/handbook.sty，图源figures/。
- scripts/build.sh batch01或batch02；python scripts/verify_math.py与python scripts/verify_training.py。XeLaTeX、Noto CJK字体。
- 编译后检查警告并渲染查看PDF。临时文件work，构建build，不入Git。保留work record.tex和原作者。
- 每批更新库存、进度与编辑路线，准确记录未完成事项；下一批优先旧稿数据/评估图，以减少尚在正文使用的原图。
