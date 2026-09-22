# Context

## Objective

- 多个来源的指令可能冲突, 必须先定义谁能覆盖谁
- 同一条指令不应在所有任务中永久生效, 必须明确其作用边界
    - workflow / skill / rules 都是在调控指令注入时间

## Observation 与 Feedback

- 观察描述发生了什么, 反馈判断这件事是否符合目标, 两者会以不同方式更新后续行为
- 模型应该以此判断 object 是否解决

## Cognitive Control

- 相同知识和目标仍可能产生不同策略

### Reasoning

- 推理负责从已有信息产生判断, 是认知控制中处理当前不确定性的部分
- Reasoning 是模型对 Knowledge 的变换, 用于降低与 Objective 相关的不确定性
- 亦称推理时计算

### Planning

- 规划负责把目标展开为未来动作, 解决的是跨步骤组织
- Planning 根据 Objective, 当前 Belief 与 Action 的可能后果组织未来行动

### Workflow

- 工作流把推理和规划放入可重复的阶段结构, 使控制模式能够被稳定调用
- Workflow 决定使用 Cognitive Control 的流程
- 也包括对 Context 的直接操作

#### ReAct

- 思考-行动-思考-结束
- agent 决定下一步是行动还是结束

#### Reflection

- 引导模型回顾之前的行动和结果

#### Plan and Execute

- 长任务需要把全局组织与局部执行分开, 否则计划容易被即时观察淹没
- 先计划, 后执行, 计划阶段生成一个完整的计划, 执行阶段按照计划执行, 适用于需要多个步骤才能完成的任务
- 在执行中可能会遇到计划中没有考虑到的情况, 需要动态调整计划 (replanning)

#### Search

- 拓展 - 打分 - 过滤
- 树形推理

#### Claude Code

- Think: 理解意图, 制定计划
- Act: 选择工具并执行
- Observe: 检查结果与状态
- Repeat: 决定下一步继续 (以及如何继续) 或结束

## Context Management

### 选择

- 进入上下文之前先决定信息价值, 才能避免低价值内容占用注意力

### 压缩

- 探索阶段的错误路径会被直接删除压缩
- 文件的旧版本会删除
- 把阶段性流程折叠
- 按固定结构输出压缩 + 最近对话 + 重要信息

### 卸载

- 有些信息不能删除但也不必常驻, 外置并保留取回路径形成独立机制
- 拦截 Bash 中那些不 AI-Native 的输出, 直接压缩为一个结构化的结果, 从而提高相关信息的覆盖率
    - 智能过滤: 去除噪音
    - 分组: 聚合相似项
    - 截断: 保留相关上下文, 删除冗余
    - 去重: 合并重复日志行并计数

### Branch

- 互斥假设若共享一份上下文会相互污染, 分支用于隔离探索路径

## Action

### Schema

- 一个工具包括
    - name
    - description
    - parameters: JSON Schema 定义参数结构和类型
    - output_schema: JSON Schema 定义输出结构和类型

### 发现

- 可用动作会随环境和权限变化, 模型不能假设工具集合恒定
- 例如 search_tools
