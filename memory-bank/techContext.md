# Tech Context: 内容创作 Agent 系统

## 技术栈

### 核心框架
- **AutoGen 0.4+**: 微软开源的多 agent 框架
  - 版本: 0.4.x (最新稳定版)
  - 关键模块: autogen_agentchat, autogen_ext
  - 文档: https://microsoft.github.io/autogen/

### Python 环境
- **Python 版本**: 3.10+
- **包管理**: pip / poetry
- **虚拟环境**: venv / conda

### 依赖库
```python
# 核心依赖
autogen-agentchat>=0.4.0
autogen-ext>=0.4.0

# LLM 提供商
openai>=1.0.0
anthropic>=0.8.0  # 可选

# 工具和实用库
pydantic>=2.0.0  # 数据验证
python-dotenv>=1.0.0  # 环境变量
aiohttp>=3.9.0  # 异步 HTTP
```

## MCP 工具集成

### Tavily Search (搜索工具)
- **用途**: 网络搜索、信息检索
- **配置**: 需要 Tavily API Key
- **功能**:
  - tavily-search: 综合搜索
  - tavily-extract: 内容提取
- **限制**: API 调用配额

### 高德地图 (地理工具)
- **用途**: 地点信息查询
- **配置**: 需要高德地图 API Key
- **功能**:
  - 地理编码: 地址 → 坐标
  - 逆地理编码: 坐标 → 地址
  - POI 搜索: 地点详细信息
- **限制**: API 调用配额

## AutoGen 0.4 关键概念

### Agent 类型
```python
# 1. AssistantAgent - 基础助手
from autogen_agentchat.agents import AssistantAgent

# 2. UserProxyAgent - 用户代理
from autogen_agentchat.agents import UserProxyAgent

# 3. ToolAgent - 工具代理 (新增)
from autogen_ext.agents import ToolAgent
```

### GroupChat 模式
```python
# RoundRobinGroupChat - 轮询模式
from autogen_agentchat.teams import RoundRobinGroupChat

# SelectorGroupChat - 选择器模式
from autogen_agentchat.teams import SelectorGroupChat
```

### 终止条件
```python
from autogen_agentchat.conditions import (
    MaxMessageTermination,
    TextMentionTermination,
    StopMessageTermination
)
```

### 消息类型
```python
from autogen_agentchat.messages import (
    TextMessage,
    ToolCallMessage,
    ToolCallResultMessage
)
```

## 开发环境设置

### 1. 项目结构
```
autogen0.4_taskinfo/
├── memory-bank/           # Memory Bank 文档
├── src/                   # 源代码
│   ├── agents/           # Agent 定义
│   ├── tools/            # 工具集成
│   ├── prompts/          # 提示模板
│   └── utils/            # 工具函数
├── examples/             # 示例代码
├── tests/                # 测试
├── .env.example          # 环境变量示例
├── requirements.txt      # 依赖列表
└── README.md            # 项目说明
```

### 2. 环境变量配置
```env
# LLM API Keys
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key  # 可选

# MCP 工具 API Keys
TAVILY_API_KEY=your_tavily_key
AMAP_API_KEY=your_amap_key

# 模型配置
DEFAULT_MODEL=gpt-4-turbo-preview
TEMPERATURE=0.7
MAX_TOKENS=4096
```

### 3. 安装步骤
```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 填入 API keys
```

## 技术约束

### 1. API 限制
- OpenAI API: 请求速率限制
- Tavily API: 免费层有配额限制
- 高德地图: 每日调用次数限制

### 2. 性能考虑
- LLM 响应时间: 通常 2-10 秒
- 搜索 API 延迟: 1-3 秒
- 总处理时间: 预计 30-60 秒/请求

### 3. 数据隐私
- 不存储用户敏感信息
- API 调用遵循各服务提供商隐私政策
- 可选择本地模型降低隐私风险

## 工具使用模式

### MCP 工具注册
```python
# 通过 autogen_ext 集成 MCP 工具
from autogen_ext.tools.mcp import MCPClient

# 创建 MCP 客户端
mcp_client = MCPClient(server_name="tavily")

# 获取工具
tools = mcp_client.get_tools()

# 注册到 agent
agent = AssistantAgent(
    name="search_agent",
    model_client=model_client,
    tools=tools
)
```

### 异步处理
```python
import asyncio
from autogen_agentchat.teams import RoundRobinGroupChat

# 异步运行团队
async def run_content_creation(topic: str):
    team = RoundRobinGroupChat(agents, termination_condition)
    result = await team.run(task=topic)
    return result

# 执行
result = asyncio.run(run_content_creation("主题"))
```

## 调试和监控

### 日志配置
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

### 追踪工具
- 使用 AutoGen 内置日志
- 记录 agent 对话历史
- 监控 API 调用次数和延迟
