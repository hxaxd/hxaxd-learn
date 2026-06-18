# openclaw

- 拒绝 MCP
- 文本即一切

## 架构

### Channel

- 管理对话的中央控制平面

### Gateway

- 连接外部系统

### Node

- 执行任务的设备

## 记忆

- SOUL: Agent 的人格, 价值观, 核心身份定义, 创建后不应被修改
- TOOLS: Agent 可用的工具列表, 包括 Skills 和 Plugins
- USER: MEMORY.md (Agent 写的) + RAG (SQLite-vec, 可以向量检索 / 精确检索)
- Session: 当前对话的上下文, 包括历史消息和当前状态

### 交互记录

- 以 append-only 方式写入 `memory/YYYY-MM-DD.md` 文件
- Session 开始时, Agent 会自动读取今天和昨天的日志

### 记忆保存

- 当上下文窗口满时, Agent 会总结记忆并压缩

## 多智能体

- 每个智能体的记忆 / 定时任务 / Skills / 定义 / 会话独立

## 用户

### 权限

- DM 配对: 新渠道接入时, 需要旧渠道的配对码
- 白名单: 提前预设的可访问用户列表

### 群组

- 默认只响应 `@` 机器人的消息
- 无记忆

## 对话

- 主对话仅有任务的总结
- 每次新任务是最对话的分支
