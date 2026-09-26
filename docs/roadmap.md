# 计算机科学储备与远期规划

> 本文档严格对齐知识库 **1~7 级核心体系与二级子分组**。  
> 每个分组清晰区分 **[当前已覆盖]** 与 **[储备规划/待学内容]**，便于系统性查漏补缺与演进追踪。

## 1. 理论基础

### 数学原理
- **已覆盖**：微积分、线性代数、概率论与数理统计、离散数学、初等数论
- **储备规划**：
  - 凸优化 (Convex Optimization) 与数值优化算法
  - 数值分析与科学计算 (Numerical Analysis)
  - 随机过程 (Stochastic Processes)
  - 分析与测度论 (Measure Theory)
  - 复变函数与常微分方程 (Complex Analysis & ODE)
  - 抽象代数 (Abstract Algebra)

### 计算理论
- **已覆盖**：编译原理、计算理论 (自动机与形式语言)
- **储备规划**：
  - 计算复杂性：现代方法 (Computational Complexity: A Modern Approach)
  - 形式语言学与语法理论 (Formal Linguistics)
  - 数理逻辑与形式化验证 (Mathematical Logic & Formal Verification)
  - 类型论与函数式范式 (Type Theory & Haskell)

### 科学通识
- **已覆盖**：电子技术与数字逻辑
- **储备规划**：
  - 信息论基础 (Information Theory: 熵、KL散度、信道编码)
  - 信号与系统 (Signals and Systems)
  - 数字信号处理 (DSP: Digital Signal Processing)
  - 控制论与动力系统 (Cybernetics & Dynamical Systems)
  - 复杂系统论 (Complex Systems Theory)

---

## 2. 开发工具与工程实践

### 开发环境与协作
- **已覆盖**：开发环境配置、终端开发环境 (Tmux/Zsh)、Git 协同
- **储备规划**：
  - CI/CD 自动化工程流水线 (GitHub Actions 进阶)
  - 基础设施即代码 (IaC: Terraform / Ansible)

### Linux与Shell
- **已覆盖**：Linux基础、Shell基础、Shell编程、Shell文本处理、Linux系统与网络管理、远程开发与集群
- **储备规划**：
  - Linux eBPF 技术与现代系统可观测性
  - 系统性能剖析与追踪工具实战 (perf / bpftrace / FlameGraph)

### 文档与数据格式
- **已覆盖**：Markdown、TeX、标记语言与序列化 (JSON/YAML/ProtoBuf)
- **储备规划**：
  - 现代学术排版系统 (Typst) 实践

### Web开发与部署
- **已覆盖**：前端开发 (HTML/CSS)、JS&TS、Web开发工具、容器与编排 (Docker/K8s)、Web服务与反向代理 (Nginx)
- **储备规划**：
  - 微服务网关与现代服务网格 (Envoy / Istio)
  - 云原生 Serverless 与边缘计算架构

---

## 3. 程序设计与算法

### 算法与数据结构
- **已覆盖**：大话数据结构、算法第四版、算法设计与分析、算法经典题 (力扣/剑指/编程珠玑)
- **储备规划**：
  - 线性规划与运筹优化 (Linear Programming)
  - 组合优化与图论进阶 (Combinatorial Optimization)
  - 近似算法 (Approximation Algorithms)
  - 随机算法 (Randomized Algorithms)
  - 计算几何 (Computational Geometry)

### 代码风格与软件设计
- **已覆盖**：设计模式、代码规范、软件工程
- **储备规划**：
  - 领域驱动设计 (DDD: Domain-Driven Design)
  - 大型分布式复杂系统架构重构与演进

---

## 4. 计算机系统

### 系统编程语言
- **已覆盖**：C语言核心、LearnCPP、C++最佳实践、C++标准库、C++工具、程序员的自我修养、Rust
- **储备规划**：
  - 并发底层与硬件内存模型 (CPU 内存屏障、原子操作、无锁并发数据结构)
  - Rust 异步底层运行时机制 (Tokio / Future / Pin 深入)

### 硬件与体系结构
- **已覆盖**：汇编语言 (王爽)、计算机组成与设计 (COD)、深入理解计算机系统 (CSAPP)
- **储备规划**：
  - 现代计算机体系结构量化研究 (Hennessy & Patterson: CAQA)
  - 异构计算与专用 AI 加速芯片架构 (TPU / NPU / 存算一体)

### 操作系统与系统软件
- **已覆盖**：操作系统导论 (OSTEP)
- **储备规划**：
  - Linux 内核源码级剖析 (内存管理子系统、CFS/EEVDF 调度器、VFS 虚拟文件系统)
  - 虚拟化技术底层与 Hypervisor 原理 (KVM / QEMU)

### 计算机网络
- **已覆盖**：计算机网络：自顶向下方法
- **储备规划**：
  - 高性能网络与用户态协议栈 (RDMA / RoCE / DPDK)
  - 数据中心网络架构与现代拥塞控制算法 (DCTCP, BBR)

---

## 5. 数据与分布式系统

### 数据库原理
- **已覆盖**：数据库系统概念、SQL必知必会
- **储备规划**：
  - 现代数据库内核实现 (CMU 15-445: 查询优化器、执行引擎、并发控制与 ARIES 恢复)
  - 现代向量数据库与近似最近邻检索 (Vector DB & ANN: HNSW, DiskANN)

### 存储组件与机制
- **已覆盖**：MySQL技术内幕、Redis设计与实现、PostgreSQL
- **储备规划**：
  - LSM-Tree 存储引擎机制与源码调优 (RocksDB / LevelDB)
  - 分布式存储系统与分布式文件系统 (Ceph / Lustre / MinIO)

### 分布式系统
- **已覆盖**：分布式系统、数据密集型应用系统设计 (DDIA)、系统设计、消息队列、Go
- **储备规划**：
  - 分布式共识协议精进 (Raft / Multi-Paxos 源码级实现与正确性检验)
  - 分布式事务与全球一致性系统 (Spanner / Percolator)

### 数据工程与大数据
- **已覆盖**：数据工程与大数据
- **储备规划**：
  - 现代湖仓一体架构 (Lakehouse: Apache Iceberg / Delta Lake)
  - 实时分布式流计算内核 (Apache Flink 核心机制与状态机)

---

## 6. 机器学习

### Python与数据计算
- **已覆盖**：流畅的Python、Python后端开发基本框架、科学计算与数据分析 (NumPy/Pandas/SciPy)
- **储备规划**：
  - 高性能与可微分计算框架 (JAX / Numba / Polars)

### 基础理论与模型
- **已覆盖**：机器学习 (统计学习方法)、深度学习 (李宏毅)、卷积神经网络
- **储备规划**：
  - 统计学习理论 (Statistical Learning Theory: PAC 框架, VC维, 泛化界)
  - 深度生成模型 (Diffusion Models, Flow Matching)
  - 计算机视觉前沿 (Vision Transformer, 3D点云与神经辐射场 NeRF / 3D Gaussian Splatting)
  - 数字图像处理与现代几何 (Digital Image Processing & Modern Geometry)
  - 计算机图形学：原理与实践 (Computer Graphics: Principles and Practice)

### 机器学习系统
- **已覆盖**：并行计算与AI系统
- **储备规划**：
  - 大规模大规模异构并行计算深入 (PMPP: Programming Massively Parallel Processors)
  - GPU 编程与自研高性能算子 (CUDA 核心编程与 Triton 分块调优)
  - 大规模分布式训练系统 (Megatron-LM 张量/流水/专家并行、DeepSpeed ZeRO-1/2/3)
  - 现代大模型高性能推理系统 (vLLM 架构、PagedAttention、Chunked Prefill、投机采样)
  - 深度学习编译器技术 (PyTorch 2.0 Dynamo/Inductor, TVM)

---

## 7. 人工智能

### 大语言模型
- **已覆盖**：大语言模型 (Transformer 基础、注意力机制、RoPE、预训练与对齐总览)
- **储备规划**：
  - 预训练工程与海量数据合成 (高质量语料清洗、长上下文扩展技术)
  - 现代基础模型架构演进 (DeepSeek MoE 架构、MLA 多头潜在注意力、稀疏激活)
  - 后训练与偏好对齐算法实战 (PPO, DPO, KTO, 过程奖励模型 PRM)
  - 推理时计算与测试时扩展 (Inference-time Scaling, MCTS, CoT 生成)

### Agent
- **已覆盖**：深入理解Agent、Harness总论、Context、Runtime、Evolution、Model、Environment、Human、Retrieval、多智能体、Cloud Agent
- **储备规划**：
  - 智能体模仿学习 (Agent Imitation Learning: DAgger, 轨迹数据飞轮)
  - 复杂交互环境与基准构建 (SWE-bench, WebArena, 真实终端与沙盒仿真)
  - 认知科学与理论神经科学模型 (Cognitive Architectures: ACT-R, SOAR 与 Agent 对照)
  - 多智能体博弈与群体决策 (Multi-Agent Game Theory, 机制设计与协作演化)
