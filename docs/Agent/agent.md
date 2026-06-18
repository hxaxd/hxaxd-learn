# Agent 总览

## VLM

- Gemini Agentic Vision: 用代码执行提升视觉模型的多步推理能力
- Visual Prompting: 通过提示词设计来引导视觉模型进行推理
    - 将视觉输出沉淀为结构化的知识, 供后续推理使用

## 能力

- reasoning: 推理能力, 从已有知识中得出新结论的能力
- planing: 补全 LLM 解决复杂问题的能力
    - thinking: 后训练中获取的能力
    - prompt: 通过提示词设计来引导模型进行推理
    - External Planner: 外部规划器 -> 本质报错
    - memory: 记忆能力, 持久化高阶结论
    - 本质是是隐藏层只有精力建模最近的上下文中的复杂状态, 生成部分答案后, 复杂状态被遗忘

## Planner

- 外部的形式化规划器, 可以验证规划的正确性, 并提供错误反馈信息

## WorkFlow

### React

- 思考-行动-思考-结束
- agent 决定下一步是行动还是结束

### Reflection

### Plan&Execute

- 先计划, 后执行, 计划阶段生成一个完整的计划, 执行阶段按照计划执行, 适用于需要多个步骤才能完成的任务
- 在执行中可能会遇到计划中没有考虑到的情况, 需要动态调整计划 (replanning)

### selection: TOT&LOTS

- 拓展 - 打分 - 过滤
- 树形推理

## 工具

### LLM API 中的 tools

- API 直接返回工具调用, 而不是文本
- 帮你校验参数
- 多工具 + 自由要求调用
- 并行调用的返回结果匹配
- 结构化输出: 提示词设计 + 限制选词空间 + 后校验 / 处理

## 多智能体编排

### agent team

### Symphony

## context

### 上下文精简

#### rtk

#### claude-mem

#### lean-ctx

### 记忆

#### beads

#### agentmemory

#### Text2Mem —— 给所有记忆系统定义"操作指令集"，12 个原子操作 + 五元 JSON 契约 + 双层验证

#### Mem0 —— 当下 Star 最多的记忆中间件，5 个工厂 / 双存储 / 三种记忆类型，含真实成本瓶颈分析

#### Letta —— 把 OS 虚拟内存思想搬进 Agent，Git 版本化记忆 + Sleeptime 异步后台学习

#### ReMe —— 阿里 AgentScope 出品，"文件即记忆"，记忆对用户完全透明可直接编辑

#### memU —— 范式最激进：让记忆本身变成一个 24/7 后台主动 Agent

## 代码理解

### 知识图谱

## 优秀框架

### GenericAgent

### openclaw

### hamrs

### manus

### cursor

### ML-intern

### 编排

#### n8n

#### dify

## 技术博客

### claude

### openai

### deepseek

### kimi

### glm

### gork

### gemini
