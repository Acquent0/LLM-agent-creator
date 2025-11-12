# LLM Agent Framework for Scientific Research / 科研LLM智能体框架

[English](#english) | [中文](#chinese)

---

## <a id="english"></a>English

### Overview

A lightweight, flexible framework for building custom LLM agents for scientific research. This framework provides an intuitive API for creating agents with custom tools, organizing multi-agent collaboration, and integrating with any LLM API endpoint.

### Key Features

- 🛠️ **Flexible Tool System**: Easy-to-create custom tools with built-in utilities
- 🤖 **Multi-Agent Orchestration**: Advanced collaboration patterns (Sequential, Parallel, Hierarchical)
- 🔌 **API-Agnostic**: Works with any LLM API (OpenAI, Claude, custom endpoints)
- 🎨 **Modern GUI**: Streamlit-based interactive interface
- 💾 **Persistent Storage**: Supabase integration for conversation history and analytics
- 📊 **Research-Oriented**: Built-in tools for scientific computing, data analysis, and literature search
- 📝 **Extensive Documentation**: Detailed annotations and examples

### Architecture

```
python-agent-framework/
├── core/                  # Core framework components
│   ├── agent.py          # Base agent class
│   ├── tool.py           # Tool system
│   ├── llm_client.py     # LLM API integration
│   └── orchestrator.py   # Multi-agent collaboration
├── tools/                 # Built-in tools
│   ├── base_tools.py     # Calculator, web search, etc.
│   ├── research_tools.py # Scientific computing tools
│   └── data_tools.py     # Data analysis tools
├── gui/                   # Streamlit GUI
│   └── app.py            # Main interface
├── examples/              # Usage examples
├── utils/                 # Utilities
└── config/                # Configuration
```

### Quick Start

1. **Installation**
```bash
cd python-agent-framework
pip install -r requirements.txt
```

2. **Configure Environment**
```bash
cp .env.example .env
# Edit .env with your API keys
```

3. **Run GUI**
```bash
streamlit run gui/app.py
```

4. **Basic Usage**
```python
from core.agent import Agent
from core.llm_client import LLMClient
from tools.base_tools import CalculatorTool

# Initialize LLM client
client = LLMClient(
    api_url="https://api.openai.com/v1/chat/completions",
    api_key="your-key",
    model="gpt-4"
)

# Create agent with tools
agent = Agent(
    name="ResearchAssistant",
    llm_client=client,
    tools=[CalculatorTool()],
    system_prompt="You are a helpful research assistant."
)

# Run task
response = agent.run("Calculate the square root of 144")
print(response)
```

### Creating Custom Tools

```python
from core.tool import Tool
from typing import Dict, Any

class MyCustomTool(Tool):
    """
    Custom tool example.
    自定义工具示例。
    """
    def __init__(self):
        super().__init__(
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
