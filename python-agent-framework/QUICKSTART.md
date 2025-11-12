# Quick Start Guide / 快速开始指南

[English](#english) | [中文](#chinese)

---

## <a id="english"></a>English

### Installation

1. **Install Dependencies**
```bash
cd python-agent-framework
pip install -r requirements.txt
```

2. **Configure Environment**
```bash
cp .env.example .env
```

Edit `.env` and add your API credentials:
```
LLM_API_URL=https://api.openai.com/v1/chat/completions
LLM_API_KEY=your-api-key-here
LLM_MODEL=gpt-4
```

### Usage Methods

#### Method 1: Run the GUI (Recommended)

```bash
streamlit run gui/app.py
```

This launches an interactive web interface where you can:
- Create and manage agents
- Chat with agents
- Set up multi-agent orchestration
- View analytics and logs

#### Method 2: Run Examples

**Basic Usage:**
```bash
python examples/basic_usage.py
```

**Orchestration Examples:**
```bash
python examples/orchestration_examples.py
```

**Research Workflow:**
```bash
python examples/research_workflow.py
```

#### Method 3: Use in Your Code

```python
from core.agent import Agent
from core.llm_client import LLMClient
from tools.base_tools import CalculatorTool

# Create LLM client
client = LLMClient(
    api_url="https://api.openai.com/v1/chat/completions",
    api_key="your-key",
    model="gpt-4"
)

# Create agent
agent = Agent(
    name="Assistant",
    llm_client=client,
    tools=[CalculatorTool()]
)

# Run task
response = agent.run("Calculate the square root of 144")
print(response)
```

### Creating Custom Tools

```python
from core.tool import Tool

class MyTool(Tool):
    def __init__(self):
        super().__init__(
            name="my_tool",
            description="What this tool does"
        )

    def execute(self, **kwargs):
        # Your logic here
        return {"success": True, "result": "..."}

# Use in agent
agent.add_tool(MyTool())
```

### Multi-Agent Collaboration

```python
from core.orchestrator import SequentialOrchestrator

agent1 = Agent(name="Researcher", llm_client=client, tools=[...])
agent2 = Agent(name="Analyst", llm_client=client, tools=[...])

orchestrator = SequentialOrchestrator([agent1, agent2])
result = orchestrator.run("Research and analyze topic X")
```

### Troubleshooting

**Problem:** API connection errors
- Check your API URL and key in `.env`
- Verify your internet connection
- Ensure API credits are available

**Problem:** Import errors
- Run `pip install -r requirements.txt`
- Check Python version (3.8+ required)

**Problem:** GUI won't start
- Ensure Streamlit is installed: `pip install streamlit`
- Try: `python -m streamlit run gui/app.py`

---

## <a id="chinese"></a>中文

### 安装

1. **安装依赖**
```bash
cd python-agent-framework
pip install -r requirements.txt
```

2. **配置环境**
```bash
cp .env.example .env
```

编辑`.env`文件并添加您的API凭证：
```
LLM_API_URL=https://api.openai.com/v1/chat/completions
LLM_API_KEY=your-api-key-here
LLM_MODEL=gpt-4
```

### 使用方法

#### 方法1：运行GUI（推荐）

```bash
streamlit run gui/app.py
```

这将启动一个交互式Web界面，您可以：
- 创建和管理智能体
- 与智能体对话
- 设置多智能体编排
- 查看分析和日志

#### 方法2：运行示例

**基础用法：**
```bash
python examples/basic_usage.py
```

**编排示例：**
```bash
python examples/orchestration_examples.py
```

**研究工作流：**
```bash
python examples/research_workflow.py
```

#### 方法3：在您的代码中使用

```python
from core.agent import Agent
from core.llm_client import LLMClient
from tools.base_tools import CalculatorTool

# 创建LLM客户端
client = LLMClient(
    api_url="https://api.openai.com/v1/chat/completions",
    api_key="your-key",
    model="gpt-4"
)

# 创建智能体
agent = Agent(
    name="助手",
    llm_client=client,
    tools=[CalculatorTool()]
)

# 运行任务
response = agent.run("计算144的平方根")
print(response)
```

### 创建自定义工具

```python
from core.tool import Tool

class MyTool(Tool):
    def __init__(self):
        super().__init__(
            name="my_tool",
            description="此工具的功能描述"
        )

    def execute(self, **kwargs):
        # 您的逻辑
        return {"success": True, "result": "..."}

# 在智能体中使用
agent.add_tool(MyTool())
```

### 多智能体协作

```python
from core.orchestrator import SequentialOrchestrator

agent1 = Agent(name="研究员", llm_client=client, tools=[...])
agent2 = Agent(name="分析师", llm_client=client, tools=[...])

orchestrator = SequentialOrchestrator([agent1, agent2])
result = orchestrator.run("研究并分析主题X")
```

### 故障排除

**问题：** API连接错误
- 检查`.env`中的API URL和密钥
- 验证您的互联网连接
- 确保API额度可用

**问题：** 导入错误
- 运行`pip install -r requirements.txt`
- 检查Python版本（需要3.8+）

**问题：** GUI无法启动
- 确保已安装Streamlit：`pip install streamlit`
- 尝试：`python -m streamlit run gui/app.py`

### 下一步

- 查看`examples/`目录中的详细示例
- 阅读`README.md`了解完整文档
- 创建您自己的自定义工具和智能体
- 探索多智能体编排模式

### 支持

如有问题，请参阅：
- README.md中的完整文档
- examples/目录中的示例代码
- 工具和核心模块中的代码注释
