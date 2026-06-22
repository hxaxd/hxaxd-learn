# Context

## Knowledge 与 Belief

- Knowledge 是当前 Context 中提供给模型的信息, 不代表其一定客观为真
    - 可以包括事实, Observation, Feedback, 假设, 预测和相互冲突的信息
    - 应尽可能保留来源, 时间, 可验证性和不确定性, 避免模型把所有信息视为同等可信
- Belief 是模型根据当前 Knowledge 形成的对任务与环境的认知状态
    - 新的 Knowledge 会使 Belief 在交互中自然更新
    - 这种更新属于 Agent 当前的认知过程, 不属于 Harness 的 Evolution
- Reasoning 是模型对 Knowledge 的变换, 以产生判断, 预测, 解释或行动依据
    - 通常用于降低与 Objective 相关的不确定性
    - 探索时也可以先生成多个假设, 再通过 Action 获取 Observation 进行排除

## Objective

- Objective 描述对环境状态, 行动轨迹或最终结果的偏好
    - Goal: 希望达到的状态
    - Constraint: 不可接受的状态或行为
    - Completion Criteria: 判断 Objective 已完成所需的证据
- Planning 根据 Objective, 当前 Belief 与 Action 的可能后果组织未来行动
- 对于开放式 Agent, Objective 还可以包括 Motivation
    - 主动生成下一目标
    - 在探索与利用之间进行选择
    - 根据能力边界形成 Curriculum

## Observation 与 Feedback

- Observation 是 Runtime 从环境中取得并提供给模型的 Knowledge
    - 描述环境中发生了什么
    - Observation 本身不判断结果是否满足 Objective
    - 模型对 Observation 的解释属于 Reasoning
- Evaluation 是依据 Objective 判断状态, Action 或结果好坏的过程
- Feedback 是 Evaluation 产生并提供给模型的 Knowledge
    - 可以来自环境, 测试, 人类, Critic 或模型自身
    - 用于修正 Belief, Plan 和后续 Action
- Observation 与 Feedback 需要分开
    - 命令退出码和文件内容是 Observation
    - 测试是否满足需求和人类是否接受结果是 Feedback

## Workflow

- Workflow 决定使用 Cognitive Control 的流程
- 也包括对 Context 的直接操作

### React

- 思考-行动-思考-结束
- agent 决定下一步是行动还是结束

### Reflection

- 引导模型回顾之前的行动和结果

### Plan&Execute

- 先计划, 后执行, 计划阶段生成一个完整的计划, 执行阶段按照计划执行, 适用于需要多个步骤才能完成的任务
- 在执行中可能会遇到计划中没有考虑到的情况, 需要动态调整计划 (replanning)

### selection: TOT&LOTS

- 拓展 - 打分 - 过滤
- 树形推理

### 压缩

- 过大文件用渐进式披露, 上下文中只有索引, 需要时指定行号读取
- 探索阶段的错误路径会被直接删除压缩
- 文件的旧版本会删除
- 把阶段性流程折叠
- 按固定结构输出压缩 + 最近对话 + 重要信息

#### rtk/Headroom/lean-ctx

- 拦截 Bash 中那些不 AI-Native 的输出, 直接压缩为一个结构化的结果, 从而提高相关信息的覆盖率
    - 智能过滤: 去除噪音
    - 分组: 聚合相似项
    - 截断: 保留相关上下文, 删除冗余
    - 去重: 合并重复日志行并计数
- 拦截 Harness 给 Context 新增的部分中的固定冗余模式, 换个方式表达
    - 用渐进式披露兜底, 如果压缩掉了关键内容, 模型还可以读文件

### Claude Code 的 Workflow

- Think: 理解意图, 制定计划
- Act: 选择工具并执行
- Observe: 检查结果与状态
- Repeat: 决定下一步继续 (以及如何继续) 或结束

## Action

### MCP

### Bash / Cli

### Tool

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
- apply_patch
    - 直接给出补丁, 而不是文本 (受限 DSL)
- exec_command
    - Bash is all you need
- sub_agents
    - 只有用户显示要求调用时才会调用
    - 上下文隔离 + 并发
    - 信号
        - spawn_agent: 创建一个子 Agent
        - send_input: 向子 Agent 继续发送输入
        - wait: 等待子 Agent 结束并获取结果 (不鼓励 Agent 使用)
        - close_agent: 强制关闭子 Agent
        - resume_agent: 恢复一个被 close 的 Agent
- 其它
    - web_search
    - view_image: 由 Agent 决定看什么图片
        - API 里传 Base64 编码
    - write_stdin: 交互式终端
    - request_user_input
- Plan
    - 文件都不落盘
    - Plan mode: 探索仓库写一个 md
        - 非变更探索
        - 提问
        - 产出规格
    - update_plan: TODO list 而不是 Plan Mode
        - 创建
        - 修改 step 状态
        - replan (每次全量)

### LLM API 中的 tools

- API 直接返回工具调用, 而不是文本
- 帮你校验参数
- 多工具 + 自由要求调用
- 并行调用的返回结果匹配
- 结构化输出: 提示词设计 + 限制选词空间 + 后校验 / 处理

### Semble

- 对代码进行 RAG, 提供一个声明式的代码检索工具
- 模型仅需要声明式地描述需要检索什么代码
- 自称相较于 grep+read 节省 98% 的 Token

### CodeGraph

- 把代码建立为知识图谱, 包括符号关系, 调用图和代码结构
- 支持自动同步, 识别部分 WEB 框架的隐式调用关系
- 存在 SOLite, 支持全文搜索
- 支持影响分析, 避免 Agent 漏修改

### graphify

- 不用向量化, 直接 LLM-based 抽取实体和关系, 构建知识图谱
