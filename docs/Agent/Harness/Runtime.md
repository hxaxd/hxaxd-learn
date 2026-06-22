# Runtime

- Runtime 是 Action 与环境状态转变的接口, 也负责将环境状态转换为 Observation
- Runtime 可以承载调用, 调度, 重试和状态持久化等确定性机制, 但这里只关注其中会影响 Agent 智能表现的部分

## 确定性机制

### Hooks

- 通过在 Agent 执行流程的不同阶段插入 Hooks 来实现对 Agent 行为的控制和调整
- 常见的 Hooks 包括:
    - 上下文压缩后: 可以在上下文被压缩后进行检查, 确保没有重要信息被误删
    - Auto模式分类器拒绝操作后: 可以在 Auto 模式下检测到潜在的危险操作时进行干预
    - turn 结束: 可以在每个 turn 结束时进行总结和调整
    - 需要人类授权: 可以在需要人类授权的操作前进行提醒和等待授权
    - 调用工具前后: 可以在调用工具前后进行检查和处理, 确保工具调用的正确性和安全性

## 安全机制

### 输入

- Prompt Injection 扫描读取的所有内容, 如果内容在试图劫持 Agent , 探测器会在内容之前附加一条警告

### 输出

- 对 agent 的操作进行粗细粒度的权限控制, 粗判断可能危险才会细判断
    - YOLO: 一个 ML 驱动的分类器, 把风险分为低中高
- 对工具调用进行核验
    - 是否有权限访问资源
    - 是否是安全行为
- 可以用沙箱以隔离环境并避免对系统造成损害
- 拒绝什么
    - 范围升级: 过度理解用户输入
    - 凭证探索: 自行探索系统中的敏感信息
    - 绕过安全检查: sudo 这一块
    - 数据外泄: 逗死我了这一块

## 可观测性与评估机制

### 轨迹感知

### 在线 Evaluation

- 在线 Evaluation 发生在 Agent 的认知循环中
    - 依据 Objective 判断当前状态, Action 或结果
    - 将评价结果作为 Feedback 返回 Context
    - Feedback 会影响 Agent 后续的 Belief, Plan 和 Action
- Evaluation 与 Observation 不同
    - Observation 描述环境中发生了什么
    - Evaluation 判断发生的事情相对于 Objective 是否正确

### Harness Evaluation

- Harness Evaluation 用于判断 Harness 中的 Knowledge, Cognitive Control 与 Runtime 是否有效
- Evaluation 的结果可以为 Evolution 提供修改 Harness 的依据

### 指标

#### 完成率

#### 幻觉率

- 绝不解释增加
- 未知工具
- 影子工具
- 参数幻觉

#### 工具调用准确率

#### 错误恢复率

#### 成本控制

### 方式

- cicd
- 在线评测
    - 安全全跑 (遥测)
    - 质量少跑一点

#### 评测专用模型

### case 设计

- 去掉目的工具, 看会不会拒绝
- 类似名字的工具, 看会不会搞混
- Prompt 里指定工具, 但可能夸大工具能力 / 工具不存在
