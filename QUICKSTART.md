# 快速开始指南

本指南帮助你在 5 分钟内启动和运行内容创作 Agent 系统。

## 📦 安装步骤

### 1️⃣ 准备环境

确保你的系统已安装：
- Python 3.10 或更高版本
- pip 包管理器

### 2️⃣ 安装依赖

```bash
# Windows
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3️⃣ 配置 API Keys

**方法 1: 使用环境变量模板（推荐）**
```bash
# Windows
copy .env.example .env

# macOS/Linux
cp .env.example .env
```

然后编辑 `.env` 文件，填入你的 API Keys。

**方法 2: 直接设置环境变量**
```bash
# Windows
set OPENAI_API_KEY=your_key_here

# macOS/Linux
export OPENAI_API_KEY=your_key_here
```

### 4️⃣ 获取 API Keys

#### OpenAI API Key（必需）
1. 访问 https://platform.openai.com/api-keys
2. 登录或注册账号
3. 创建新的 API Key
4. 复制并保存到 `.env` 文件

#### Tavily API Key（推荐）
1. 访问 https://tavily.com/
2. 注册账号
3. 获取免费的 API Key
4. 复制并保存到 `.env` 文件

## 🚀 第一次运行

### 交互模式（最简单）

```bash
python -m src.main
```

然后输入你的主题，例如：
- "第一次工业革命"
- "人工智能在医疗领域的应用"
- "中国春节习俗"

### 命令行模式

```bash
python -m src.main "你的主题"
```

例如：
```bash
python -m src.main "第一次工业革命"
```

### 使用示例脚本

```bash
python examples/simple_example.py
```

## ✅ 验证安装

运行以下命令检查是否一切正常：

```bash
python -c "from src import run_content_creation; print('✓ 安装成功！')"
```

如果看到 "✓ 安装成功！"，说明安装正确。

## 🎯 示例主题

尝试这些主题来测试系统：

### 历史类
- "罗马帝国的兴衰"
- "文艺复兴运动"
- "辛亥革命"

### 科技类
- "量子计算的发展"
- "区块链技术原理"
- "5G 通信技术"

### 文化类
- "中国茶文化"
- "日本武士道精神"
- "西方现代艺术"

### 人物类
- "爱因斯坦的科学贡献"
- "莎士比亚的文学成就"
- "马云的创业历程"

## 🔧 常见问题

### Q: 安装依赖时出错？
A: 尝试升级 pip：
```bash
pip install --upgrade pip
pip install -r requirements.txt --no-cache-dir
```

### Q: 没有 API Key 能试用吗？
A: 抱歉，需要至少一个 OpenAI API Key 才能运行。你可以注册 OpenAI 账号获取免费试用额度。

### Q: Tavily API Key 是必需的吗？
A: 不是必需的。没有 Tavily，SearchAgent 会基于 LLM 的知识提供引用建议，但可能不如搜索结果准确。

### Q: 运行很慢或超时？
A: 这可能是因为：
1. 网络连接问题
2. API 响应慢
3. 主题过于复杂

尝试：
- 使用更简单的主题
- 检查网络连接
- 在 `.env` 中调低 `MAX_TOKENS`

### Q: 输出格式不理想？
A: 你可以：
1. 调整 `src/prompts.py` 中的提示模板
2. 在 `.env` 中调整 `TEMPERATURE` 参数
3. 提供更具体的主题描述

## 📚 下一步

- 阅读 [README.md](README.md) 了解详细功能
- 查看 `examples/` 目录的更多示例
- 探索 `src/` 目录的源代码
- 修改 `src/prompts.py` 自定义 Agent 行为

## 💬 获取帮助

遇到问题？

1. 查看 [README.md](README.md) 的故障排除部分
2. 检查 `memory-bank/` 目录的设计文档
3. 提交 Issue 或联系维护者

---

祝你使用愉快！🎉
