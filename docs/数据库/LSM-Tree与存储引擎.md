# LSM-Tree 与存储引擎

## 参考资料

- 设计数据密集型应用 (DDIA)
- RocksDB 官方 Wiki

## 核心机制

- 追加写与写放大 (Write Amplification)
- 内存表 (MemTable): 跳表 (SkipList) 与并发写
- 预写日志 (WAL, Write-Ahead Logging): 崩溃恢复保障
- 不可变内存表 (Immutable MemTable)
- 磁盘有序字符串表 (SSTable, Sorted String Table): Data Block, Index Block, Filter Block (布隆过滤器 Bloom Filter)
- 压缩机制 (Compaction): Size-Tiered Compaction 与 Leveled Compaction

## 典型实现与生态

- LevelDB
- RocksDB
- 现代分布式存储单机引擎选型 (TiKV, Kafka Log, Flink StateBackend)
