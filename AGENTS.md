# 项目续作规则

- 目标是面向初学者的简体中文图解参考手册。保持解释深度、图文配合和版式，科学正确优先；当前为工作稿。
- 先读PROGRESS.md、EDITORIAL_PLAN.md、docs/REVIEW_NOTES.md，延续已有正文，不重启全库审计。
- 唯一整书入口main.tex；正文chapters/，独立TikZ/PGFPlots与CSV在figures/，共享样式styles/。
- 已移除旧图、旧稿、贡献流水、库存与历史批次。按知识缺口推进，不恢复旧资产或为数量机械扩写。
- scripts/build.sh构建；python scripts/verify_all.py核验；构建结束后python scripts/audit_build.py main。修订后渲染检查相关PDF页。
- review/只保留当前整书PDF与源码包；docs/只保留当前验证和审校说明。work/、build/不入Git，源码包用scripts/package_source.py生成。
- 不逐批请求验收；按用户当前指定时长保存停止，等用户主动唤醒。会话计时及远程检查点放work/，不写入公开正文。
- 远程与本地历史可能不同；公开更新用远程头为父提交，租约检查后更新。保留Git历史，不强推重写；合并权限以当前用户指示为准。
