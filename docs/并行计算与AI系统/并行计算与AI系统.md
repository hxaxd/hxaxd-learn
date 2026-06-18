# 并行计算与 AI 系统

## 参考资料

- An Introduction to Parallel Programming
- Programming Massively Parallel Processors
- Machine Learning Systems
- Designing Machine Learning Systems
- Efficient Processing of Deep Neural Networks

## 领域边界

- 并发关注多个任务在时间上的交叠以及同步与通信
- 并行计算关注同时使用多个计算资源缩短时间或扩大可处理规模
- 分布式系统关注不可靠网络上的多节点协作与一致性
- AI 系统关注模型从数据, 训练, 优化到推理和部署的完整计算系统

## 并行模型

- 任务并行与数据并行
- 指令级, 数据级与线程级并行
- 共享内存与消息传递
- SIMD, SIMT 与 MIMD
- 流水线并行
- 数据依赖, 同步, 通信与负载均衡

## CPU 与 GPU

- 缓存, 内存层次与数据局部性
- 多核, NUMA 与向量化
- GPU 线程层次, Warp 与流多处理器
- 内存合并访问, Shared Memory 与 Bank Conflict
- Roofline 模型, 算术强度与带宽限制

## CUDA 与 Triton

- Kernel, Grid, Block 与 Thread
- 内存空间与异步执行
- 并行归约, 扫描, 矩阵乘法与卷积
- Kernel 融合与算子调优
- Triton 的分块编程模型与自动调优

## 张量与算子系统

- 张量布局, 步长与广播
- 自动微分
- 算子注册, 调度与设备后端
- 计算图, 图优化与编译
- PyTorch Extension, Triton 与编译器栈

## 分布式训练

- 数据并行, 张量并行, 流水线并行与专家并行
- 参数, 梯度与优化器状态的切分
- 集合通信与通信计算重叠
- 检查点, 容错与弹性训练
- 数据加载与训练吞吐量

## 推理

- Prefill 与 Decode
- KV Cache
- Continuous Batching
- 量化, 剪枝, 蒸馏与稀疏化
- 并行推理与模型服务
- 延迟, 吞吐量, 显存与成本之间的权衡

## 部署与性能评测

- 模型格式, 运行时与硬件后端
- 在线服务与离线批处理
- 性能剖析与瓶颈定位
- 正确性, 数值稳定性与可复现性
- 训练和推理的基准设计
- 利用率, 能耗, 可靠性与成本

## 待评估书目

- An Introduction to Parallel Programming 2nd Edition
- Programming Massively Parallel Processors 5th Edition
- Structured Parallel Programming
- Efficient Processing of Deep Neural Networks
- Machine Learning Systems Volume 1 and Volume 2
- Designing Machine Learning Systems
- AI Engineering
