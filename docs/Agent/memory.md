# 记忆

## 分类

### 作用域

> 以下的记忆文件就指 AutoMem / TeamMem 中的文件

- Managed -> 系统规则
- User -> 用户的 CLAUDE.md
- Project -> 项目的 CLAUDE.md
- Local -> CLAUDE.local.md
- AutoMem -> 由 Agent 自动维护
- TeamMem -> 由 Agent 自动维护, 团队共享的记忆

### 语义 (只有由 Agent 自动维护的才存在语义)

- user
    - 用户是谁, 决定回答的风格, 解释粒度, 协作方式等
- feedback
    - 规则, 决定应该怎么做与不应该怎么做
    - 结构: rule/fact, why, how to apply
    - 是可迁移的, 必须说为什么
- project
    - 代码中无法推断, 但对完成任务很重要的信息
- reference
    - 代码中事实的索引 (去哪找事实)

### 运行期

- Session Memory -> 只在当前会话中有效, 会话结束后丢失
- Agent Memory -> 给专用 Agent 的持久化记忆 (包括 User, Project, Local)

## 结构

- 记忆文件
    - 每个文件对应一个 Topic
    - 每个文件包括元信息 (name, description, type (语义))
- manifest.json
    - 记录所有记忆文件 (除了 MEMORY.md) 的元信息
- MEMORY.md
    - 记录一些重要的事实, 例如用户的偏好, 项目的背景等
    - 由 Agent 维护, 可以被 Agent 修改

## 写入

- 一个 Prompt 触发的一个 turn 完全结束后会 fork 一个子 Agent 来写入记忆
- 先读取 manifest.json 决定新建文件还是修改文件
- `/dream` 是另一种模式, 收集一天的日志, 由 Agent 定期总结并写入记忆

## 召回与注入

- 不要相信记忆中的内容, 只把它当成一个提示, 需要验证后才能使用
