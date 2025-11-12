# LLM Agent Creator / LLM智能体创建器

> 一个集成了前端界面和Python智能体框架的完整解决方案  
> A complete solution integrating frontend UI and Python agent framework

[English](#english) | [中文](#chinese)

---

## <a id="chinese"></a>中文

### 📋 项目概述

这是一个用于构建和管理LLM智能体的完整平台，包含：

1. **Python Agent Framework** - 灵活的Python智能体框架
2. **Web Frontend** - 基于React + Vite的现代化前端界面

### 🗂️ 项目结构

```
LLM-agent-creator/
├── 📁 python-agent-framework/    # Python智能体框架（后端）
│   ├── core/                      # 核心组件
│   ├── tools/                     # 内置工具
│   ├── gui/                       # Streamlit GUI
│   ├── examples/                  # 使用示例
│   └── utils/                     # 工具函数
│
├── 📁 src/                        # React前端源码
│   ├── App.tsx                    # 主应用组件
│   ├── main.tsx                   # 入口文件
│   └── index.css                  # 样式文件
│
├── 📁 docs/                       # 文档目录
│   ├── README.md                  # 文档索引
│   └── python-framework/          # Python框架文档
│
├── 📁 outputs/                    # 输出文件目录
│
├── 📄 package.json                # 前端依赖配置
├── 📄 vite.config.ts              # Vite配置
├── 📄 tailwind.config.js          # Tailwind CSS配置
└── 📄 README.md                   # 本文件
```

### 🚀 快速开始

#### Python框架

```bash
# 1. 进入Python框架目录
cd python-agent-framework

# 2. 安装依赖
pip install -r requirements.txt

# 3. 配置环境变量
cp .env.example .env
# 编辑 .env 填入你的API密钥

# 4. 运行Streamlit GUI
streamlit run gui/app.py
```

#### 前端界面

```bash
# 1. 在项目根目录安装依赖
npm install

# 2. 启动开发服务器
npm run dev

# 3. 构建生产版本
npm run build
```

### 📚 文档

详细文档请查看 [docs/README.md](./docs/README.md)

**快速链接**：
- 📖 [快速参考](./QUICK_REFERENCE.md) - 常用命令和配置
- 📋 [项目结构](./PROJECT_STRUCTURE.md) - 详细的目录说明
- 📝 [整理总结](./REORGANIZATION_SUMMARY.md) - 项目整理记录

**推荐阅读顺序**：
1. [快速开始](./docs/python-framework/QUICKSTART.md)
2. [项目结构](./docs/python-framework/PROJECT_STRUCTURE.md)
3. [工具快速入门](./docs/python-framework/TOOL_QUICKSTART.md)

### ✨ 主要特性

#### Python Agent Framework

- 🛠️ **灵活的工具系统** - 轻松创建自定义工具
- 🤖 **多智能体协作** - 支持顺序、并行、层次化协作模式
- 🔌 **API无关性** - 支持任意LLM API（OpenAI、Claude等）
- 🎨 **现代化GUI** - 基于Streamlit的交互界面
- 💾 **持久化存储** - Supabase集成，保存对话历史
- 📊 **科研导向** - 内置科学计算、数据分析工具

#### Web Frontend

- ⚡ **快速开发** - Vite + React + TypeScript
- 🎨 **现代设计** - Tailwind CSS样式
- � **类型安全** - 完整的TypeScript支持

### 🛠️ 技术栈

**后端**：
- Python 3.8+
- Streamlit
- Supabase
- NumPy, Pandas, Matplotlib

**前端**：
- React 18
- TypeScript
- Vite
- Tailwind CSS
- Supabase Client

### � 使用示例

查看 [examples/](./python-agent-framework/examples/) 目录了解更多示例。

### 🤝 贡献

欢迎提交Issue和Pull Request！

### 📄 许可证

详见 [LICENSE](./LICENSE) 文件。

---

## <a id="english"></a>English

### 📋 Project Overview

A complete platform for building and managing LLM agents, including:

1. **Python Agent Framework** - Flexible Python agent framework
2. **Web Frontend** - Modern frontend built with React + Vite

### 🗂️ Project Structure

```
LLM-agent-creator/
├── 📁 python-agent-framework/    # Python agent framework (backend)
│   ├── core/                      # Core components
│   ├── tools/                     # Built-in tools
│   ├── gui/                       # Streamlit GUI
│   ├── examples/                  # Usage examples
│   └── utils/                     # Utilities
│
├── 📁 src/                        # React frontend source
│   ├── App.tsx                    # Main app component
│   ├── main.tsx                   # Entry file
│   └── index.css                  # Styles
│
├── 📁 docs/                       # Documentation
│   ├── README.md                  # Documentation index
│   └── python-framework/          # Python framework docs
│
├── 📁 outputs/                    # Output files
│
├── 📄 package.json                # Frontend dependencies
├── 📄 vite.config.ts              # Vite config
├── 📄 tailwind.config.js          # Tailwind CSS config
└── 📄 README.md                   # This file
```

### 🚀 Quick Start

#### Python Framework

```bash
# 1. Navigate to Python framework directory
cd python-agent-framework

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# Edit .env with your API keys

# 4. Run Streamlit GUI
streamlit run gui/app.py
```

#### Frontend

```bash
# 1. Install dependencies at project root
npm install

# 2. Start development server
npm run dev

# 3. Build for production
npm run build
```

### 📚 Documentation

See [docs/README.md](./docs/README.md) for detailed documentation.

**Recommended Reading Order**:
1. [Quick Start](./docs/python-framework/QUICKSTART.md)
2. [Project Structure](./docs/python-framework/PROJECT_STRUCTURE.md)
3. [Tool Quick Start](./docs/python-framework/TOOL_QUICKSTART.md)

### ✨ Key Features

#### Python Agent Framework

- 🛠️ **Flexible Tool System** - Easy custom tool creation
- 🤖 **Multi-Agent Orchestration** - Sequential, parallel, hierarchical patterns
- 🔌 **API-Agnostic** - Works with any LLM API (OpenAI, Claude, etc.)
- 🎨 **Modern GUI** - Streamlit-based interface
- 💾 **Persistent Storage** - Supabase integration for conversation history
- 📊 **Research-Oriented** - Built-in scientific computing and data analysis tools

#### Web Frontend

- ⚡ **Fast Development** - Vite + React + TypeScript
- 🎨 **Modern Design** - Tailwind CSS styling
- 🔍 **Type Safety** - Full TypeScript support

### 🛠️ Tech Stack

**Backend**:
- Python 3.8+
- Streamlit
- Supabase
- NumPy, Pandas, Matplotlib

**Frontend**:
- React 18
- TypeScript
- Vite
- Tailwind CSS
- Supabase Client

### 📖 Examples

Check the [examples/](./python-agent-framework/examples/) directory for more examples.

### 🤝 Contributing

Issues and Pull Requests are welcome!

### 📄 License

See [LICENSE](./LICENSE) file for details.
            name="my_tool",
            description="Description of what this tool does"
        )

    def execute(self, **kwargs) -> Dict[str, Any]:
        """
        Execute the tool logic.
        执行工具逻辑。
        """
        # Your tool logic here
        result = {"status": "success", "data": "result"}
        return result
```

### Multi-Agent Collaboration

```python
from core.orchestrator import SequentialOrchestrator, ParallelOrchestrator

# Create multiple agents with different specializations
researcher = Agent(
    name="Researcher",
    llm_client=client,
    tools=[...],
    system_prompt="You are a research specialist."
)

analyst = Agent(
    name="Analyst",
    llm_client=client,
    tools=[...],
    system_prompt="You are a data analyst."
)

# Sequential orchestration (agents work one after another)
seq_orchestrator = SequentialOrchestrator([researcher, analyst])
result = seq_orchestrator.run("Research quantum computing and analyze trends")

# Parallel orchestration (agents work simultaneously)
par_orchestrator = ParallelOrchestrator([agent1, agent2, agent3])
results = par_orchestrator.run("Analyze this dataset from different angles")
```

### Built-in Tools

- **CalculatorTool**: Mathematical computations using Python's math library
- **WebSearchTool**: Internet search capabilities (requires API key)
- **FileIOTool**: File reading and writing operations
- **PythonREPLTool**: Execute Python code safely
- **ScientificComputeTool**: NumPy/SciPy integration for scientific computing
- **DataAnalysisTool**: Pandas-based data analysis and statistics
- **VisualizationTool**: Matplotlib/Plotly plotting and visualization
- **LiteratureSearchTool**: Search scientific papers and publications

### Advanced Features

#### Memory and Context Management
```python
agent = Agent(
    name="Assistant",
    llm_client=client,
    tools=[...],
    memory_enabled=True,  # Enable conversation memory
    max_memory_tokens=4000
)
```

#### Custom Orchestration Patterns
```python
from core.orchestrator import CustomOrchestrator

class MyOrchestrator(CustomOrchestrator):
    def orchestrate(self, task: str):
        # Implement your custom orchestration logic
        pass
```

#### Integration with Supabase
```python
from utils.storage import SupabaseStorage

storage = SupabaseStorage()
# Store conversation history
storage.save_conversation(agent_name, messages)
# Retrieve analytics
analytics = storage.get_analytics()
```

---

## <a id="chinese"></a>中文

### 概述

一个轻量级、灵活的科研LLM智能体框架。本框架提供直观的API用于创建带有自定义工具的智能体、组织多智能体协作，并集成任何LLM API端点。

### 核心特性

- 🛠️ **灵活的工具系统**：易于创建自定义工具，包含内置实用工具
- 🤖 **多智能体编排**：高级协作模式（顺序、并行、层级）
- 🔌 **API无关**：支持任何LLM API（OpenAI、Claude、自定义端点）
- 🎨 **现代化GUI**：基于Streamlit的交互界面
- 💾 **持久化存储**：Supabase集成，用于对话历史和分析
- 📊 **面向科研**：内置科学计算、数据分析和文献检索工具
- 📝 **详尽文档**：详细注释和示例

### 系统架构

本框架采用模块化设计，核心组件包括：
- **Agent（智能体）**：执行任务的基本单元
- **Tool（工具）**：智能体可调用的功能模块
- **LLMClient（LLM客户端）**：与各种LLM API通信
- **Orchestrator（编排器）**：管理多智能体协作

### 快速开始

1. **安装依赖**
```bash
cd python-agent-framework
pip install -r requirements.txt
```

2. **配置环境**
```bash
cp .env.example .env
# 编辑.env文件，填入您的API密钥
```

3. **运行GUI界面**
```bash
streamlit run gui/app.py
```

4. **基础用法**
```python
from core.agent import Agent
from core.llm_client import LLMClient
from tools.base_tools import CalculatorTool

# 初始化LLM客户端
client = LLMClient(
    api_url="https://api.openai.com/v1/chat/completions",
    api_key="your-key",
    model="gpt-4"
)

# 创建带工具的智能体
agent = Agent(
    name="研究助手",
    llm_client=client,
    tools=[CalculatorTool()],
    system_prompt="你是一个有帮助的研究助手。"
)

# 执行任务
response = agent.run("计算144的平方根")
print(response)
```

### 创建自定义工具

```python
from core.tool import Tool
from typing import Dict, Any

class MyCustomTool(Tool):
    """
    自定义工具示例。
    Custom tool example.
    """
    def __init__(self):
        super().__init__(
            name="my_tool",
            description="描述此工具的功能"
        )

    def execute(self, **kwargs) -> Dict[str, Any]:
        """
        执行工具逻辑。
        Execute the tool logic.
        """
        # 在这里实现您的工具逻辑
        result = {"status": "success", "data": "结果"}
        return result
```

### 多智能体协作

```python
from core.orchestrator import SequentialOrchestrator, ParallelOrchestrator

# 创建具有不同专长的多个智能体
researcher = Agent(
    name="研究员",
    llm_client=client,
    tools=[...],
    system_prompt="你是一名研究专家。"
)

analyst = Agent(
    name="分析师",
    llm_client=client,
    tools=[...],
    system_prompt="你是一名数据分析师。"
)

# 顺序编排（智能体依次工作）
seq_orchestrator = SequentialOrchestrator([researcher, analyst])
result = seq_orchestrator.run("研究量子计算并分析趋势")

# 并行编排（智能体同时工作）
par_orchestrator = ParallelOrchestrator([agent1, agent2, agent3])
results = par_orchestrator.run("从不同角度分析此数据集")
```

### 内置工具

- **计算器工具**：使用Python math库进行数学计算
- **网络搜索工具**：互联网搜索能力（需要API密钥）
- **文件操作工具**：文件读写操作
- **Python执行器**：安全执行Python代码
- **科学计算工具**：NumPy/SciPy集成的科学计算
- **数据分析工具**：基于Pandas的数据分析和统计
- **可视化工具**：Matplotlib/Plotly绘图和可视化
- **文献检索工具**：搜索科学论文和出版物

### 高级功能

#### 记忆与上下文管理
```python
agent = Agent(
    name="助手",
    llm_client=client,
    tools=[...],
    memory_enabled=True,  # 启用对话记忆
    max_memory_tokens=4000
)
```

#### 自定义编排模式
```python
from core.orchestrator import CustomOrchestrator

class MyOrchestrator(CustomOrchestrator):
    def orchestrate(self, task: str):
        # 实现您的自定义编排逻辑
        pass
```

#### 与Supabase集成
```python
from utils.storage import SupabaseStorage

storage = SupabaseStorage()
# 存储对话历史
storage.save_conversation(agent_name, messages)
# 检索分析数据
analytics = storage.get_analytics()
```

### 使用场景

1. **科学文献综述**：自动搜索、分析和总结科研论文
2. **数据分析工作流**：多步骤数据处理和可视化
3. **实验设计助手**：协助设计和优化实验方案
4. **代码生成与调试**：生成科研代码并进行测试
5. **知识图谱构建**：从文献中提取和组织知识

### 许可证 / License

MIT License

### 贡献 / Contributing

欢迎贡献代码、报告问题或提出新功能建议！
Contributions, issues, and feature requests are welcome!

### 支持 / Support

如有问题，请创建Issue或查看文档。
For questions, please create an issue or check the documentation.
