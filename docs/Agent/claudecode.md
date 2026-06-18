# claude code

## Context

- 过大文件用渐进式披露, 上下文中只有索引, 需要时指定行号读取
- 探索阶段的错误路径会被直接删除压缩
- 文件的旧版本会删除
- 把阶段性流程折叠
- 总结: 九段式 + 必要信息 + 最近内容

## TAOR

- Think: 理解意图, 制定计划
- Act: 选择工具并执行
- Observe: 检查结果与状态
- Repeat: 决定下一步继续 (以及如何继续) 或结束

## auto 模式

- 一个Prompt Injection探测器会扫描Claude读取的所有内容（文件、网页、命令输出）。如果内容看起来像在试图劫持Claude的行为（比如某个文件里写着「忽略之前的指令」），探测器会在内容传给Claude之前附加一条警告。
- 对 agent 的操作进行粗细粒度的权限控制, 粗判断可能危险才会细判断
- 拒绝什么
    - 范围升级: 过度理解用户输入
    - 凭证探索: 自行探索系统中的敏感信息
    - 绕过安全检查: sudo 这一块
    - 数据外泄: 逗死我了这一块

## /permissions

- 细粒度权限控制, 定制可执行的命令列表
- 存在 `.claude/settings.json`

## YOLO

- 一个 ML 驱动的分类器, 把风险分为低中高

## Worktrees

- 通过 git worktree 的能力, 同时多目录开发多分支

## 人类干预

- 新会话
- 压缩
- 停止
- 回滚
- 侧链提问

## CLAUDE.md

- 写规则而不是知识
- 写代码中没法推断的信息
- 更多内容渐进式披露
- 给出不能做的事情的替代方案
- 层级结构的 CLAUDE.md

## 最佳实践

- 具体
- 参照
- 不要自己猜 bug
- 渐进式披露
- 让 Claude 采访你
- 越早纠正成本越低
- 只纠正两次
- subagent 去调研
- 换任务清理上下文

## Hooks

- 上下文压缩后
- Auto模式分类器拒绝操作后
- turn 结束
- 需要人类授权
- 调用工具前后

## agent teams

- 感觉没用

## 小工具

- `claude -p`: 直接在命令行输入 Prompt, 适合嵌入脚本
- `/batch`: agent 帮你调用一批 agent
- `/loop`: agent 帮你循环执行一个任务, 直到满足条件

## 新功能

### KAIROS

- 一个始终在线的后台助手, 监听GitHub webhook, 在有新 PR, 新 Issue, CI 失败时主动介入
- 日志
- 每次主动操作最多占用15秒计算资源

### ULTRAPLAN

- 把复杂 Plan 卸载到云端

### Coordinator Mode

- Research -> Synthesis -> Implementation -> Verification
    - 每个阶段可以启动不同数量的子 Agent 并行工作

### 未来

- 交错思维
- 可休眠 agent
- 情绪感知
