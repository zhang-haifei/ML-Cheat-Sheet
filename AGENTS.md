# 项目续作规则

- 目标是面向初学者的简体中文图解参考手册。保持解释深度和图文配合，科学正确优先；版式按最新要求改为连续书籍排版，当前为第一版定稿候选。
- 先读PROGRESS.md、EDITORIAL_PLAN.md、docs/REVIEW_NOTES.md，延续已有正文，不重启全库审计。逐章科学复审和三条读者路线校读已完成；后续按具体反馈维护，不安排机械扩写或重复审计。
- 最新版式要求：普通正文页应尽可能饱满，优先减少页尾大块留白；章末页可自然留白。连续排版已实施；新增内容沿用自然分页，图、图注和读图说明作为一个浮动单元，长表可跨页并重复表头。禁止恢复一节一页；修改后检查非章末留白和孤立标题。
- 唯一整书入口main.tex；正文chapters/，独立TikZ/PGFPlots与CSV在figures/，共享样式styles/。
- 已移除旧图、旧稿、贡献流水、库存与历史批次。按知识缺口推进，不恢复旧资产或为数量机械扩写。
- scripts/build.sh构建；python scripts/verify_all.py核验；构建结束后python scripts/audit_build.py main和python scripts/audit_navigation.py。修订后渲染检查相关PDF页。
- review/只保留当前整书PDF与源码包；docs/只保留当前验证和审校说明。work/、build/不入Git，源码包用scripts/package_source.py生成。
- 不逐批请求验收；按用户当前指定时长保存停止，等用户主动唤醒。会话计时及远程检查点放work/，不写入公开正文。
- 远程与本地历史可能不同；公开更新用远程头为父提交，租约检查后更新。保留Git历史，不强推重写；合并权限以当前用户指示为准。
