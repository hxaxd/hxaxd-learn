# NoSQL 与专用数据库

## 存储模型对比

- 键值数据库 (Key-Value): 极速单键点查, 内存为主 (Redis)
- 文档数据库 (Document): 半结构化 JSON/BSON, 灵活模式 (MongoDB)
- 列族与宽列存储 (Wide-Column): 稀疏多维映射, 高吞吐大容量 (Cassandra, HBase)
- 时序数据库 (TSDB): 时间戳为核心, 高写入吞吐, 数据自动衰减与降采样 (InfluxDB, Prometheus)
- 图数据库 (Graph): 节点与边, 原生图遍历与深度关系查询 (Neo4j)

## 核心设计权衡

- 灵活模式 (Schema-Free) vs 强模式 (Schema-on-Write)
- 水平分片机制 (Consistent Hashing 与 Range Partitioning)
- 索引结构: 倒排索引 (Inverted Index), LSM-Tree, 图指针
- 适用场景与技术选型
