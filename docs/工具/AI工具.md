# 人工智能工具

## 参考资料

- [技术爬爬虾](https://space.bilibili.com/316183842)

## API

- 略

## Trae

- 略

## Cherry Studio

- 略

## Claude code

- 使用 Claude code router

### Claude code 命令

- `/init` 初始化项目, 收集项目信息
- `/compact text` 压缩上下文, text 作为指导
- `/clear` 清除上下文
- `think / think hard / think harder / urtrathink text` 控制思考长度
- `! command` 执行终端命令
- `# text` 作为记忆
- `/ide` 联动 IDE
- `ccr code -p text` 问问题
- `claude mcp add name --scope user --command 参数` 添加 mcp
- `.claude/command` 文件夹中的 md 文件为自定义命令
- `/agent` 创建智能体
- `resume` 历史话题

## 自己写一个吧

### 上下文工程

- 至少使用一些常识性的 prompt 技巧
    - 前提 (充足的上下文)
    - 目标 (明确的目标)
    - 解释 (详细的解释)
    - 限制 (约束条件)
    - 风格 (限定输出风格)
    - 示例 (提供一些短示例)
- 优秀的系统提示词中包含
    - 身份
    - 商业上想传达的信息
    - 禁止事项
    - 风格
    - 知识截止日期 (不要假设或推断超出知识范围的信息)
    - 自我定位与哲学原则 (不要让用户害怕)
    - 不要快速承认错误 (讨好)
- 跨请求的 k-v cache 不会被保留, 部分场景会保留前缀
- 上下文工程的基本原则
    - 选择
        - 内容的选择 (RAG)
        - 工具的选择 (提供针对问题的工具)
        - 记忆的选择 (RAG)
    - 压缩
        - 压缩上下文, 保留重要信息 (让模型做)
    - 多智能体
        - 多个智能体合作, 每个智能体负责一个任务
- 上下文工程的基本方法
    - 压缩
        - 工具内容返回双版本, 一个用于当下, 一个用于记忆 (精简化, 不保留环境信息, 不保留可重建信息)
        - 谨慎的摘要, 因为这是不可恢复的 (最好同时保存原始内容)
        - 找到上下文腐烂的阈值
        - 无论压缩还是摘要, 都要保留一些原始内容, 避免错误示例的误导
    - 工具卸载
        - 对工具进行 RAG 是一种有效的方法
        - 预设一些常用的工具集合可高效利用缓存
    - 多智能体
        - 简单状态下, 使用通信转递信息 (父为子写 Prompt)
        - 复杂状态下, 使用共享全局上下文
- 上下文工程的哲学
    - 简化架构, 相信模型

### Langchain

#### 入门

- [官方文档](https://langchain-doc.cn/v1/python/langchain/quickstart.html)

#### 模型

- 各厂商集成方式不同

```python
# 初始化模型
model = init_chat_model(
    "anthropic:claude-sonnet-4-5", # model
    api_key = "sk-1234567890abcdef1234567890abcdef", # api_key
    temperature=0.7, # 温度
    timeout=30, # 超时时间
    max_tokens=1000, # 最大 token 数
    max_retries=3, # 最大重试次数
)
```

#### 调用与消息

```python
# 普通调用
response = model.invoke("为什么鹦鹉有五颜六色的羽毛？")

# 带角色的调用
# 三种消息对象
conversation = [
    SystemMessage("你是一个将英语翻译成法语的有用助手"),
    HumanMessage("翻译: 我喜欢编程"),
    AIMessage("J'adore la programmation"),
    HumanMessage("翻译: 我喜欢构建应用程序")
]
response = model.invoke(conversation)

# 流式调用
full = None
for chunk in model.stream("天空是什么颜色？"):
    full = chunk if full is None else full + chunk
    print(full.text)
    # 天空
    # 天空是
    # 天空通常
    # 天空通常是蓝色
    # ...

# 批量调用
responses = model.batch([
    "为什么鹦鹉有五颜六色的羽毛？",
    "飞机是如何飞行的？",
    "什么是量子计算？"
])
for response in responses:
    print(response)

# 异步批量调用
for response in model.batch_as_completed([
    "为什么鹦鹉有五颜六色的羽毛？",
    "飞机是如何飞行的？",
    "什么是量子计算？"
]):
    print(response)
```

#### 工具

```python
# 将（可能多个）工具绑定到模型
model_with_tools = model.bind_tools([get_weather])

# 步骤 1: 模型生成工具调用
messages = [{"role": "user", "content": "波士顿的天气怎么样？"}]
ai_msg = model_with_tools.invoke(messages)
messages.append(ai_msg)

# 步骤 2: 执行工具并收集结果
for tool_call in ai_msg.tool_calls:
    # 使用生成的参数执行工具
    tool_result = get_weather.invoke(tool_call)
    messages.append(tool_result)

# 步骤 3: 将结果传递回模型以获取最终响应
final_response = model_with_tools.invoke(messages)
print(final_response.text)


# 流式调用
gathered = None
for chunk in model_with_tools.stream("波士顿的天气怎么样？"):
    gathered = chunk if gathered is None else gathered + chunk
    print(gathered.tool_calls)

# 访问上下文
from langchain.tools import tool, ToolRuntime

@tool
def summarize_conversation(
    runtime: ToolRuntime # ToolRuntime 包含各种上下文信息
) -> str:
    """Summarize the conversation so far."""
    messages = runtime.state["messages"]

    human_msgs = sum(1 for m in messages if m.__class__.__name__ == "HumanMessage")
    ai_msgs = sum(1 for m in messages if m.__class__.__name__ == "AIMessage")
    tool_msgs = sum(1 for m in messages if m.__class__.__name__ == "ToolMessage")

    return f"Conversation has {human_msgs} user messages, {ai_msgs} AI responses, and {tool_msgs} tool results"

# Access custom state fields
@tool
def get_user_preference(
    pref_name: str,
    runtime: ToolRuntime  # ToolRuntime parameter is not visible to the model
) -> str:
    """Get a user preference value."""
    preferences = runtime.state.get("user_preferences", {})
    return preferences.get(pref_name, "Not set")
```

#### 结构化输出

```python
from pydantic import BaseModel, Field

class Movie(BaseModel):
    """一部带有详细信息的电影"""
    title: str = Field(..., description="电影标题")
    year: int = Field(..., description="电影上映年份")
    director: str = Field(..., description="电影导演")
    rating: float = Field(..., description="电影评分, 满分 10 分")

model_with_structure = model.with_structured_output(Movie)
response = model_with_structure.invoke("提供关于电影《盗梦空间》的详细信息")
print(response)  # Movie(title="Inception", year=2010, director="Christopher Nolan", rating=8.8)
```

### 记忆

- 依赖数据库实现

### 中间件

- 字面意思
- 有很多预设

### 智能体

- 动态模型, 依赖 `@wrap_model_call`

```python
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain.agents.middleware import wrap_model_call, ModelRequest, ModelResponse


basic_model = ChatOpenAI(model="gpt-4o-mini")
advanced_model = ChatOpenAI(model="gpt-4o")

@wrap_model_call
def dynamic_model_selection(request: ModelRequest, handler) -> ModelResponse:
    """根据对话复杂性选择模型"""
    message_count = len(request.state["messages"])

    if message_count > 10:
        # 对较长的对话使用高级模型
        model = advanced_model
    else:
        model = basic_model

    request.model = model
    return handler(request)

agent = create_agent(
    model=basic_model,  # 默认模型
    tools=tools,
    middleware=[dynamic_model_selection]
)
```

- 当你需要在结构化输出的部分使用动态模型, 不支持预绑定 `bind_tools` 模型
- 我猜结构化输出通过 `tools` 实现, 静态时预绑定加上就好, 动态时非预绑定同理, 就三者同时出现时冲突
- 定义工具错误处理

```python
from langchain.agents import create_agent
from langchain.agents.middleware import wrap_tool_call
from langchain_core.messages import ToolMessage


@wrap_tool_call
def handle_tool_errors(request, handler):
    """使用自定义消息处理工具执行错误"""
    try:
        return handler(request)
    except Exception as e:
        # 向模型返回自定义错误消息
        return ToolMessage(
            content=f"工具错误: 请检查您的输入并重试({str(e)})",
            tool_call_id=request.tool_call["id"]
        )

agent = create_agent(
    model="openai:gpt-4o",
    tools=[search, get_weather],
    middleware=[handle_tool_errors]
)
```

- 系统提示也可以动态

```python
from typing import TypedDict

from langchain.agents import create_agent
from langchain.agents.middleware import dynamic_prompt, ModelRequest


class Context(TypedDict):
    user_role: str

@dynamic_prompt
def user_role_prompt(request: ModelRequest) -> str:
    """根据用户角色生成系统提示"""
    user_role = request.runtime.context.get("user_role", "user")
    base_prompt = "你是一个有帮助的助手"

    if user_role == "expert":
        return f"{base_prompt} 提供详细的技术响应"
    elif user_role == "beginner":
        return f"{base_prompt} 简单解释概念, 避免使用行话"

    return base_prompt

agent = create_agent(
    model="openai:gpt-4o",
    tools=[web_search],
    middleware=[user_role_prompt],
    context_schema=Context
)

# 系统提示将根据上下文动态设置
result = agent.invoke(
    {"messages": [{"role": "user", "content": "解释机器学习"}]},
    context={"user_role": "expert"}
)
```

### RAG 与向量数据库

- langchain 可以轻松实现 RAG 功能, 封装成工具即可
- 准备一个嵌入模型
- 向量数据库
    - 用于存储和检索文本嵌入向量
    - Chroma/FAISS 本地向量数据库, 简单易用, 适合小规模应用
    - Milvus 高性能向量数据库, 支持大规模应用
