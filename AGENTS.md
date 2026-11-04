# 项目维护规则

- 本项目为简体中文机器学习与深度学习图解手册：17个主章节、两份附录、87幅独立矢量图。main保留当前全文润色版，后续依据具体反馈修订。
- 先读README.md；编辑口径见docs/EDITORIAL_REPORT.md。先讲对象、机制与条件，用具体解释替代泛泛否定和重复提醒。
- 唯一整书入口main.tex；正文在chapters/，TikZ/PGFPlots和CSV图源在figures/，共享样式在styles/。
- 连续书籍排版：正文11pt、1.12倍行距；普通页尽可能饱满，章末自然换页。图、图注及读图说明整体排放，长表可跨页并重复表头。
- 修改后按范围运行scripts/build.sh、python scripts/verify_all.py、python scripts/audit_build.py main和python scripts/audit_navigation.py；检查受影响的渲染页、孤立标题及页尾留白。
- scripts/check_torch_conventions.py为可选PyTorch接口核验；15组基础复算只依赖NumPy。已有框架实测记录见docs/TORCH_CHECKS.json。
- review/只保留当前PDF及源码包；源码包用scripts/package_source.py生成，并用scripts/check_source_package.py核对独立解压、重新打包和失败保护。
- build/、work/、预览图及会话记录为临时文件，交付后删除；保持README链接和docs/当前验证记录有效，不恢复旧图、阶段样章或重复进度文档。
- 合并及公开发布遵循用户当前授权；保留Git历史，不强推重写。
