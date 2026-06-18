# RAG

- 编译知识大于检索知识

## LightRAG

- KG-based RAG, 以知识图谱为核心构建 RAG 系统

### 构建

- Document -> chunk
- llm-based 提取 chunk 中实体与关系为 K-V 形式 (实体名 - 实体摘要 / 实体暗示的全局主题 - 关系内容)
- 对所有实体 / 关系的 K-V Embedding, 存入 VectorDB, 构建为知识图谱
- 投入新文档不需要重新构建

### 检索

- llm-based 提取 Prompt 中实体与抽象
- 实体向量检索实体, 再根据图谱关系做二跳检索
- 抽象向量检索关系, 获取相关实体
- 查询的原始 chunk 也可以作为补充

### 图合并

- 实体合并
- 关系合并
    - 收集所有关系
    - 去重
    - 拼接 / summarization

### 召回

## Embedding

## VectorDB

## Reranking
