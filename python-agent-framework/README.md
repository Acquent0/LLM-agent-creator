# Python Agent Framework / Python智能体框架

灵活的Python智能体框架，用于构建自定义LLM智能体。

## 📁 目录结构

```
python-agent-framework/
├── core/                  # 核心组件
│   ├── agent.py          # 智能体基类
│   ├── tool.py           # 工具系统
│   ├── llm_client.py     # LLM API集成
│   └── orchestrator.py   # 多智能体协作
│
├── tools/                 # 内置工具
│   ├── base_tools.py     # 基础工具（计算器、网络搜索等）
│   ├── research_tools.py # 科研工具
│   └── data_tools.py     # 数据分析工具
│
├── gui/                   # Streamlit GUI
│   └── app.py            # 主界面
│
├── examples/              # 使用示例
│   ├── basic_usage.py
│   ├── custom_tool_template.py
│   ├── orchestration_examples.py
│   └── research_workflow.py
│
├── utils/                 # 工具函数
│   ├── dynamic_tool.py
│   ├── storage.py
│   └── tool_storage.py
│
└── tools_data/            # 工具数据存储
    ├── custom_tools.json
    ├── example_tools.json
    └── README.md
```

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境

创建 `.env` 文件并配置你的API密钥：

```bash
# LLM API配置
OPENAI_API_KEY=your-api-key-here
API_URL=https://api.openai.com/v1/chat/completions
MODEL_NAME=gpt-4

# Supabase配置（可选）
SUPABASE_URL=your-supabase-url
SUPABASE_KEY=your-supabase-key
```

### 3. 运行GUI

```bash
streamlit run gui/app.py
```

## 💡 基本使用

### 创建简单智能体

```python
from core.agent import Agent
from core.llm_client import LLMClient
from tools.base_tools import CalculatorTool

# 初始化LLM客户端
client = LLMClient(
    api_url="https://api.openai.com/v1/chat/completions",
    api_key="your-api-key",
    model="gpt-4"
)

# 创建带工具的智能体
agent = Agent(
    name="助手",
    llm_client=client,
    tools=[CalculatorTool()],
    system_prompt="你是一个有帮助的助手。"
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
    """自定义工具示例"""
    
    def __init__(self):
        super().__init__(
            name="my_custom_tool",
            description="描述你的工具功能",
            parameters={
                "param1": {"type": "string", "description": "参数1描述"}
            }
        )
    
    def execute(self, **kwargs) -> Dict[str, Any]:
        """执行工具逻辑"""
        param1 = kwargs.get("param1")
        
        # 你的逻辑代码
        result = f"处理了：{param1}"
        
        return {
            "success": True,
            "result": result
        }
```

## 📚 更多文档

详细文档请查看项目根目录的 `docs/` 文件夹：

- [快速开始](../docs/python-framework/QUICKSTART.md)
- [工具快速入门](../docs/python-framework/TOOL_QUICKSTART.md)
- [工具管理指南](../docs/python-framework/TOOL_MANAGEMENT_GUIDE.md)
- [演示指南](../docs/python-framework/DEMO_GUIDE.md)
- [项目结构](../docs/python-framework/PROJECT_STRUCTURE.md)

## 🛠️ 内置工具

- **CalculatorTool** - 基础计算器
- **WebSearchTool** - 网络搜索
- **ScientificCalculatorTool** - 科学计算
- **DataVisualizationTool** - 数据可视化
- **StatisticalAnalysisTool** - 统计分析

## 🤝 多智能体协作

框架支持多种协作模式：

```python
from core.orchestrator import Orchestrator

# 顺序执行
orchestrator = Orchestrator(mode="sequential")
result = orchestrator.run([agent1, agent2], task)

# 并行执行
orchestrator = Orchestrator(mode="parallel")
result = orchestrator.run([agent1, agent2], task)

# 层次化执行
orchestrator = Orchestrator(mode="hierarchical")
result = orchestrator.run([coordinator, worker1, worker2], task)
```

## 📖 示例

查看 `examples/` 目录获取更多使用示例：

- `basic_usage.py` - 基础使用示例
- `custom_tool_template.py` - 自定义工具模板
- `orchestration_examples.py` - 多智能体协作示例
- `research_workflow.py` - 科研工作流示例

## 🔧 依赖

主要依赖包括：

- requests - HTTP请求
- python-dotenv - 环境变量管理
- streamlit - GUI界面
- numpy, pandas - 数据处理
- matplotlib, plotly - 数据可视化
- scipy - 科学计算
- supabase - 数据库集成

## 📝 许可证

详见项目根目录的 LICENSE 文件。
