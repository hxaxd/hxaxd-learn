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

### Context

- Knowledge 是 Context 中关于环境和任务的信息
    - Objective 作为一种特殊的 Knowledge 传递给模型, 模型倾向于进行服从它或对其 Plan 等与其它 Knowledge 不同的行为
    - 对 Knowledge 降低信息熵即为 Reasoning, 当然可能有增加信息熵的情况, 例如探索阶段的假设生成
    - 对 Objective 进行 Reasoning / 拆解规划即为 Planning
    - 上下文压缩通过删除冗余的 Knowledge 来提高有效信号密度
- Objective 指我们希望得到的 Agent 的可能输出的一个子集, 该子集使得 Harness 对环境的更改符合目标的表述
- Cognitive Control 是 Context 中关于如何处理 Knowledge 的模式
    - 直接影响模型的关注点, 抽象层级, 推理方向和行动倾向
    - 本质是在激活稀疏注意力的 index + 引导模型的生成倾向
    - 主要形式是提示词注入
    - Workflow 是一种注入 Cognitive Control 的机制, 决定当前使用哪种 Cognitive Control
- Action 是描述可进行的环境交互与交互后果的 Context
    - 模型倾向于将渴望得到的知识或环境状态转换为 Action, 以满足 Objective 的要求
    - 环境状态对于模型来说是不可直接观察的, 只能通过 Action 转化为 Knowledge 进行间接观察
- Feedback 是一种特殊的 Knowledge, 从 Action 中返回的观测解释得出
    - 模型倾向于将 Feedback 作为坚定可信的知识

### Runtime

- Runtime 是 Action 与环境状态转变的接口
    - 安全机制
    - 可观测性与评估机制
    - Hooks

### Evolution

- Evolution 是 Harness 的自我进化机制
    - 提供 Knowledge, 包括 MEMORY 和 SKILL
    - 调整 Cognitive Control, 包括 WORKFLOW
    - 优化 Runtime, 包括安全机制和可观测性与评估机制

## 其它

### Human

### Multi-Agent

### SPEC&TEST
