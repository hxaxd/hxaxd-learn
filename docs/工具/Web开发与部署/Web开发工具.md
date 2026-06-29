# Web 开发工具

## 参考资料

- [GeekHour](https://space.bilibili.com/102438649)
- 官方文档

## 数据库管理工具

### DBeaver

## 接口测试

### postman

- 依赖其图形界面, 你可以方便的进行接口测试, 并将测试结果导出为 html 格式的报告
- 可以编写 js 文件, 构造错误请求, 进行接口测试
- 你可以创建测试集合, 将多个接口测试放在一个集合中, 方便管理
- 可以隔离环境, 并定义环境变量

### bruno

- 离线的轻量的与 postman 哲学一致的接口测试工具

### Hoppscotch

## CI/CD

### CI (持续集成)

- 版本控制 -> 自动构建 -> 自动测试
- 版本控制 Git
- 自动构建形式多样, 自行了解
- 测试框架依托语言

### CD (持续交付)

- 自动部署 -> 监控 -> 改进
- 自动部署形式多样, 如 docker+k8s
- 监控反馈工具多样, 自行了解

## 服务器运维管理工具

### 1panel

- 其可以一键部署各种应用 (Docker)
- 管理界面清晰简单

## 性能测试工具

### JMeter

- 线程组
    - 线程数 -> 模拟的用户数量
    - 循环次数 -> 每个用户模拟的请求次数
    - 启动延迟 -> 加速度, $5$ 秒指在 $5$ 秒内启动所有用户
- 采样器
    - 模拟用户行为, 如 HTTP 请求, 数据库查询
- 逻辑控制器
    - 控制采样器的执行顺序, 如循环, 分支等
- 前置处理器与后置处理器
    - 可以在请求发送前或接收后执行一些操作, 如设置变量, 加密解密等
- 断言
    - 检查响应是否符合预期, 如状态码, 响应体等
- 监听器
    - 查看结果树 -> 查看每个请求的响应结果
    - 聚合报告 -> 查看所有请求的聚合结果
- 定时器
    - 更灵活复杂地控制线程的执行时间, 如随机延迟, 固定延迟等
- 参数化
    - 可以从外部文件读取参数, 如 CSV 文件, 数据库等
- 可以分布式

## 其他工具

### SuperBase

- 一个基于 PostgreSQL 的后端服务

### OpenTelemetry

#### 采集与传输

- OpenTelemetry
    - SDK / 自动埋点 / 手动业务埋点
    - OTLP 作为统一传输协议
    - 通过 trace id 关联 logs, metrics, traces
- Collector: 采集器
    - receivers: 接收数据
    - processors: 采样, 过滤, 批处理, 补充资源属性
    - exporters: 导出到后端
    - connectors: 在不同 pipeline 间转换或派生数据
- Grafana Alloy
    - Grafana 发行的 OpenTelemetry Collector
    - 适合同时接 Prometheus, Loki, Tempo, Pyroscope 等后端

#### 存储

- Metrics: 指标
    - Prometheus: 指标采集与短期存储
    - Mimir: Prometheus 兼容的长期, 高可用, 多租户指标存储
- Traces: 链路追踪
    - Tempo: Grafana 体系下更常用的链路追踪后端
    - Jaeger: 经典 tracing 后端, 适合学习, 调试和已有 Jaeger 生态
- Logs: 日志
    - Loki: 日志存储与查询
- Profiles: 性能剖析
    - Pyroscope: 持续性能剖析, 可选

#### 可视化与告警

- Grafana: 面板 + 告警
