# CodeX

## 上下文

- 一个对话对应一个本地的 session, 存在一个 JSONL 文件中
- 结构
    - system: base_isntructions
    - developer: 权限与沙箱规则
    - user: AGENTS.md
        - 用户的 AGENT.md
        - Skills
        - 环境信息
    - developer: collaboration_mode
    - turn flag 中间夹杂着 user Prompt 和 ReAct, 直到结束

### 上下文压缩

- 官方模型有个压缩 API, 但本质也就是先用 Prompt 压缩
- 压缩 + 压缩后接收的 Prompt

## 工具

### spec

- 一个工具包括
    - name
    - description
    - parameters: JSON Schema 定义参数结构和类型
    - output_schema: JSON Schema 定义输出结构和类型
- 传给 API 时会序列化为 JSON
    - 不包括 output_schema
    - 对于 spawn_agent
        - type
        - name
        - description
        - strict
        - parameters

### apply_patch

- 直接给出补丁, 而不是文本 (受限 DSL)

### exec_command

- Bash is all you need

### sub_agents

- 只有用户显示要求调用时才会调用
- 上下文隔离 + 并发
- 信号
    - spawn_agent: 创建一个子 Agent
    - send_input: 向子 Agent 继续发送输入
    - wait: 等待子 Agent 结束并获取结果 (不鼓励 Agent 使用)
    - close_agent: 强制关闭子 Agent
    - resume_agent: 恢复一个被 close 的 Agent

### 其它

- web_search
- view_image: 由 Agent 决定看什么图片
    - API 里传 Base64 编码
- write_stdin: 交互式终端
- request_user_input

### Plan

- 文件都不落盘
- Plan mode: 探索仓库写一个 md
    - 非变更探索
    - 提问
    - 产出规格
- update_plan: TODO list 而不是 Plan Mode
    - 创建
    - 修改 step 状态
    - replan (每次全量)
