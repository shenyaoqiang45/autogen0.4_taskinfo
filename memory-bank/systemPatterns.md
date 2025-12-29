# System Patterns: 内容创作 Agent 系统

## 系统架构

### 多 Agent 协作架构
```
User Input (主题)
    ↓
Orchestrator Agent (协调器)
    ↓
┌───────────────┬────────────────┬──────────────────┐
↓               ↓                ↓                  ↓
Topic Analyzer  Info Enricher   Search Agent    Integrator
(主题分析)      (信息扩展)       (搜索引用)       (内容整合)
```

### Agent 角色设计

#### 1. Orchestrator Agent (协调器)
- **职责**: 任务分解、流程控制、结果汇总
- **输入**: 用户主题
- **输出**: 任务分配和最终结果
- **关键能力**: 理解用户意图、协调其他 agent、质量控制

#### 2. Topic Analyzer Agent (主题分析器)
- **职责**: 分析主题、提取关键要素、确定主题类型
- **输入**: 原始主题文本
- **输出**: 结构化的主题分析结果
- **关键能力**: 主题分类、要素提取、范围界定

#### 3. Info Enricher Agent (信息扩展器)
- **职责**: 补充时间、地点、人物信息
- **输入**: 主题分析结果
- **输出**: 完善的时间、地点、人物信息
- **关键能力**: 历史知识、地理知识、人物关系分析
- **工具**: 高德地图 API（地点信息）

#### 4. Search Agent (搜索代理)
- **职责**: 搜索引用来源、验证信息可靠性
- **输入**: 需要引用的关键信息点
- **输出**: 可靠的引用来源列表
- **关键能力**: 信息检索、来源验证、相关性判断
- **工具**: Tavily Search API

#### 5. Integrator Agent (整合器)
- **职责**: 整合所有信息、生成结构化输出
- **输入**: 各 agent 的处理结果
- **输出**: 完整的创作素材文档
- **关键能力**: 信息组织、格式化、结构优化

## 核心设计模式

### 1. 团队协作模式 (Team Pattern)
使用 AutoGen 0.4 的 RoundRobinGroupChat 或 SelectorGroupChat 实现多 agent 协作：
- Orchestrator 作为协调者
- 其他 agent 作为专业工作者
- 通过消息传递实现信息共享

### 2. 工具使用模式 (Tool Use Pattern)
每个 agent 配置特定工具：
- Search Agent → Tavily MCP 工具
- Info Enricher → 高德地图 MCP 工具
- 其他 agent 使用 LLM 推理能力

### 3. 状态管理模式
使用 TerminationCondition 控制对话流程：
- MaxMessageTermination: 防止无限循环
- TextMentionTermination: 检测任务完成标志
- StopMessageTermination: 支持显式停止

### 4. 提示工程模式
每个 agent 使用专门的系统提示：
- 明确角色定位
- 清晰的输入输出格式
- 具体的工作流程指引

## 数据流设计

### 信息传递结构
```python
{
    "topic": "用户原始主题",
    "analysis": {
        "type": "主题类型",
        "core_elements": ["核心要素"],
        "scope": "范围界定"
    },
    "enrichment": {
        "time": {
            "timeline": [],
            "key_dates": [],
            "historical_context": ""
        },
        "location": {
            "places": [],
            "geographic_info": [],
            "environment": ""
        },
        "people": {
            "key_persons": [],
            "relationships": [],
            "backgrounds": []
        }
    },
    "references": [
        {
            "source": "来源名称",
            "url": "链接",
            "relevance": "相关性说明",
            "credibility": "可信度评估"
        }
    ],
    "integrated_output": "结构化的完整输出"
}
```

## 关键技术决策

### 1. 使用 AutoGen 0.4 新特性
- AssistantAgent: 基础 agent 类型
- GroupChat: 多 agent 协作
- ToolAgent: 集成 MCP 工具
- TerminationCondition: 流程控制

### 2. 异步处理
部分信息收集可以并行处理：
- 时间信息收集
- 地点信息收集
- 人物信息收集
（搜索引用依赖前面结果，需串行）

### 3. 错误处理
- 网络请求失败：重试机制
- API 配额限制：降级处理
- 信息不足：提示用户补充
- 格式错误：自动修正或请求重新生成

### 4. 可扩展性
- Agent 插件化：易于添加新的专业 agent
- 工具可配置：支持更换或添加新工具
- 模型可选：支持不同 LLM 提供商
