# Agent = 独立上下文的被连续调用的 LLM + 支撑其工作的 Harness 框架 + 工作环境

## 核心

- Agent 领域的工作是发掘模型与环境的更高效的交互方式
- 高效性的来源直接取决于模型的训练数据
- 早期工作本质上是在发掘自然语言数据中蕴含的交互模式, 称之为 Prompt Engineering
- 随着更多后天交互模式反作用于数据的影响 + 模型能力的提升, 交互模式已不是瓶颈
    - 模型是否拥有足够的对环境的对交互方式的知识为主要优化方向, 称之为 Context Engineering
- 直至今天, 长程任务的数据融于模型后训练过程, 模型倾向变成高度可定制的能力, 围绕该能力集的完整设计标准, 称之为 Harness Engineering

## 概念

- Harness 是模型与环境交互的中介, 建立在环境的可解析性与模型的先验能力之上
- Harness 负责维护模型状态 (Context), 也负责与环境的接口 (Runtime), 以及 Harness 自身的进化 (Evolution)
    - Context
    - Runtime
    - Evolution

### Context

- Knowledge 是 Context 中关于环境和任务的信息
    - Object 作为一种特殊的 Knowledge 传递给模型, 模型倾向于进行服从它或对其 Plan 等与其它 Knowledge 不同的行为
    - 对 Knowledge 降低信息熵即为 Reasoning
    - 对 Object 进行 Reasoning / 拆解即为 Planning
    - 上下文压缩通过删除冗余的 Knowledge 来提高 Object 的信号密度
- Object 指我们希望得到的 Agent 的可能输出的一个子集, 该子集使得 Harness 对环境的更改符合目标的表述
- Cognitive Control 是 Context 中关于如何处理 Knowledge 的模式
    - 直接影响模型的关注点, 抽象层级, 推理方向和行动倾向
    - 本质是在激活稀疏注意力的 index + 引导模型的生成倾向
    - 主要形式是提示词注入
    - Workflow 是一种注入 Cognitive Control 的机制, 决定当前使用哪种 Cognitive Control
- Action 是模型输出的一个子集, 通过 Runtime 机制被解释为对环境的交互
    - 模型倾向于将渴望得到的知识或环境状态转换为 Action, 以满足 Object 的要求
    - 环境状态对于模型来说是不可直接观察的, 只能通过 Action 转化为 Knowledge 进行间接观察
- Feedback 是一种特殊的 Knowledge, 从 Action 中返回的观测解释得出
    - 模型倾向于将 Feedback 作为坚定可信的知识

### Runtime

- Runtime 是 Action 与环境状态转变的接口
    - 安全机制
    - 可观测性与评估机制

### Evolution

- Evolution 是 Harness 的自我进化机制
    - 主动提供 Knowledge, 包括 MEMORY 和 SKILL
    - 主动调整 Cognitive Control, 包括 PLAN 和 WORKFLOW

## Context 的实现

## Runtime 的实现

### 安全机制

- 通过限制 Action 的空间来提高安全性, 包括 Action 的类型和范围等

### 可观测性与评估机制

## Evolution 的实现

### Memory

- Memory 是主动提供给模型的 Knowledge, 以弥补模型先验知识的不足
- 广义的 Memory 包括任何主动提供给模型的 Knowledge, 包括 Plan 和 Skill 中的案例等
- 为区分 Skills, 这里将 Memory 定义为环境信息与任务信息的集合, 不包括行动规则和计划等
    - 环境信息简化模型的探索阶段, 但 Memory 应该仅是环境信息的索引, 还需要模型的再加载 / 验证
    - 任务信息简化模型的规划阶段, 但 Memory 应该仅是隐式倾向, 补全任务信息的细节, 而不是直接提供计划

### Skills

- Skill 是主动提供给模型的 Plan, 包括行动规则和案例等, 以弥补模型先验能力的不足
- Skill 压缩了模型的推理与规划过程, 代表相应 Object 的最佳实践

## 未解之谜

### Human

### Multi-Agent

## 可验证预测

- 增加 Context 只有提高相关信息覆盖率时才有益
- Context 优化的重点是选择, 而不只是压缩
- Plan 的主要收益来自更新与重新加载
- Reflection 需要新的 Feedback 才会稳定有效
- Verifier 的独立证据比多一次相同调用更重要
- Memory 应优先保存索引, 决策背景和重新验证要求
- Skill 必须包含适用条件, 失败边界和验证步骤
- Subagent 收益与任务正交性和 Context 污染程度正相关
- Workflow 可以还原为阶段级 Knowledge, Cognitive Control, Action, Feedback 选择
- Harness 自进化的瓶颈通常是 Evaluation
