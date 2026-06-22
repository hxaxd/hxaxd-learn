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
- Harness 负责维护若干个模型状态 (Context), 也负责与环境的接口 (Runtime), 以及 Harness 自身的进化 (Evolution)

### Context

- Knowledge 是 Context 中关于环境和任务的信息
    - Knowledge 表示提供给模型的信息, 不代表其一定客观为真, 其中可以包括事实, 观察, 假设, 预测和相互冲突的信息
    - Reasoning 是模型对 Knowledge 的变换, 以产生判断, 预测, 解释或行动依据
        - Reasoning 通常降低与 Objective 相关的不确定性
        - 探索阶段也可能通过生成假设主动增加候选解释
    - 上下文压缩通过删除冗余的 Knowledge 来提高有效信号密度
- Objective 是一种特殊的 Knowledge, 描述对环境状态, 行动轨迹或最终结果的偏好
    - 包括希望达到的 Goal, 不可违反的 Constraint 和判断完成的 Completion Criteria
    - 模型倾向于服从 Objective, 并围绕 Objective 进行推理与规划
    - Planning 是根据 Objective, 当前 Belief 与 Action 的可能后果组织未来行动
- Cognitive Control 是 Context 中关于如何处理 Knowledge 的模式
    - 直接影响模型的关注点, 抽象层级, 推理方向和行动倾向
    - 可以理解为激活模型已有行为模式的 index + 引导模型的注意分配与生成倾向
    - 主要形式是提示词注入
    - Workflow 是一种注入 Cognitive Control 的机制, 决定当前使用哪种 Cognitive Control
- Action 是模型输出中可被 Runtime 解释为环境交互的部分
    - Action 的类型, 参数及可能后果会作为 Knowledge 提供给模型
    - 模型倾向于将渴望得到的知识或环境状态转换为 Action, 以满足 Objective 的要求
    - 环境状态对于模型来说不可直接观察, 只能由 Runtime 转换为 Observation 后进入 Context
- Observation 是 Runtime 从环境中取得并提供给模型的 Knowledge
    - Observation 描述环境中发生了什么, 但不直接表示结果相对于 Objective 是否正确
    - 模型对 Observation 的解释属于 Reasoning, 不等于 Observation 本身
- Feedback 是 Evaluation 产生并提供给模型的 Knowledge, 用于修正后续推理与行动
    - Feedback 可以来自环境, 测试, 人类, Critic 或模型自身, 不一定由 Action 直接返回
    - 模型倾向于高估 Observation 与 Feedback 的可信度, 因此需要保留其来源与可验证性

### Runtime

- Runtime 是 Action 与环境状态转变的接口, 也负责将环境状态转换为 Observation
    - 安全机制
    - 可观测性与评估机制
    - Hooks

### Evolution

- Evolution 专指 Harness 根据交互经验对自身进行持久化修改的机制
    - 不包括 Agent 在当前 Context 中自然发生的认知更新
    - 不包括 Model 权重的训练与更新
    - 提供 Knowledge, 包括 MEMORY 和 SKILL
    - 调整 Cognitive Control, 包括 WORKFLOW
    - 优化 Runtime, 包括安全机制和可观测性与评估机制

## 其它

### Human

### Multi-Agent

### SPEC&TEST
