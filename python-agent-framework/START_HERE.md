# 🚀 START HERE / 从这里开始

Welcome to the LLM Agent Framework!
欢迎使用LLM智能体框架！

## 📖 What is This? / 这是什么？

A complete Python framework for building LLM-powered agents for scientific research.
一个完整的Python框架，用于构建科研用途的LLM驱动智能体。

**Key Features / 主要特性:**
- 🛠️ Easy-to-use agent and tool system / 易用的智能体和工具系统
- 🤖 Multi-agent collaboration patterns / 多智能体协作模式
- 🎨 Beautiful Streamlit GUI / 漂亮的Streamlit GUI
- 📊 Built-in scientific computing tools / 内置科学计算工具
- 📝 Complete bilingual documentation / 完整的双语文档

## ⚡ Quick Start (5 Minutes) / 快速开始（5分钟）

### Step 1: Install / 安装
```bash
./setup.sh
```

Or manually:
```bash
pip install -r requirements.txt
cp .env.example .env
```

### Step 2: Configure / 配置
Edit `.env` and add your API credentials:
编辑`.env`并添加您的API凭证：

```
LLM_API_URL=https://api.openai.com/v1/chat/completions
LLM_API_KEY=your-api-key-here
LLM_MODEL=gpt-4
```

### Step 3: Run / 运行

**Option A: GUI (Recommended) / 选项A：GUI（推荐）**
```bash
streamlit run gui/app.py
```

**Option B: Examples / 选项B：示例**
```bash
python examples/basic_usage.py
```

## 📚 Documentation / 文档

Read in this order:
按此顺序阅读：

1. **QUICKSTART.md** - Installation and basic usage / 安装和基本使用
2. **README.md** - Complete documentation / 完整文档
3. **PROJECT_STRUCTURE.md** - Architecture details / 架构细节
4. **examples/** - Code examples / 代码示例

## 🎯 What Can I Do? / 我能做什么？

### 1. Chat with AI Agents / 与AI智能体对话
```python
from core.agent import Agent
from core.llm_client import LLMClient
from tools.base_tools import CalculatorTool

client = LLMClient.from_env()
agent = Agent("Assistant", client, tools=[CalculatorTool()])
response = agent.run("What is 123 * 456?")
```

### 2. Create Custom Tools / 创建自定义工具
```python
from core.tool import Tool

class MyTool(Tool):
    def __init__(self):
        super().__init__("my_tool", "Description")

    def execute(self, **kwargs):
        return {"success": True, "result": "..."}
```

### 3. Multi-Agent Collaboration / 多智能体协作
```python
from core.orchestrator import SequentialOrchestrator

orchestrator = SequentialOrchestrator([agent1, agent2])
result = orchestrator.run("Research and analyze topic X")
```

### 4. Data Analysis / 数据分析
```python
from tools.data_tools import DataAnalysisTool

agent = Agent("Analyst", client, tools=[DataAnalysisTool()])
agent.run("Analyze this dataset...")
```

## 🛠️ What's Included? / 包含什么？

### Core Components / 核心组件
- **Agent System** - Smart agents with tool usage / 带工具使用的智能体
- **Tool Framework** - Easy-to-extend tool system / 易于扩展的工具系统
- **LLM Client** - Works with any API / 适用于任何API
- **Orchestrators** - Multi-agent patterns / 多智能体模式

### Built-in Tools (12 Tools) / 内置工具（12个）
- Calculator, File I/O, Python REPL / 计算器、文件I/O、Python执行器
- Scientific Computing, Statistics / 科学计算、统计
- Data Analysis, Visualization / 数据分析、可视化
- And more... / 以及更多...

### Examples (4 Files) / 示例（4个文件）
- Basic usage / 基本使用
- Multi-agent orchestration / 多智能体编排
- Research workflows / 研究工作流
- Custom tool templates / 自定义工具模板

## 🎓 Learning Path / 学习路径

**Beginner / 初学者:**
1. Run `python examples/basic_usage.py`
2. Try the GUI: `streamlit run gui/app.py`
3. Read QUICKSTART.md

**Intermediate / 中级:**
4. Study `examples/orchestration_examples.py`
5. Create a custom tool using the template
6. Read core module code

**Advanced / 高级:**
7. Build a research workflow
8. Create custom orchestration patterns
9. Integrate with your own tools

## 💡 Common Use Cases / 常见用例

### Scientific Research / 科研
- Literature review automation / 文献综述自动化
- Data analysis pipelines / 数据分析流程
- Experiment design assistance / 实验设计辅助

### Data Science / 数据科学
- Multi-step data processing / 多步骤数据处理
- Statistical analysis / 统计分析
- Visualization generation / 可视化生成

### Development / 开发
- Code generation / 代码生成
- Documentation writing / 文档编写
- Testing automation / 测试自动化

## 🆘 Troubleshooting / 故障排除

**Problem: Import errors / 问题：导入错误**
```bash
pip install -r requirements.txt
```

**Problem: API connection fails / 问题：API连接失败**
- Check your `.env` file
- Verify API key is correct
- Test internet connection

**Problem: GUI won't start / 问题：GUI无法启动**
```bash
pip install streamlit
streamlit run gui/app.py
```

## 📊 Project Stats / 项目统计

- **4,278 lines** of documented code / 4278行文档化代码
- **12 built-in tools** ready to use / 12个可用的内置工具
- **5 orchestration patterns** / 5种编排模式
- **4 complete examples** / 4个完整示例
- **3 documentation files** / 3个文档文件

## 🎉 Next Steps / 下一步

1. ✅ Complete the installation above / 完成上述安装
2. 📖 Read QUICKSTART.md / 阅读QUICKSTART.md
3. 🚀 Run an example / 运行一个示例
4. 🎨 Try the GUI / 尝试GUI
5. 🛠️ Create your first custom tool / 创建第一个自定义工具
6. 🤖 Build a multi-agent system / 构建多智能体系统

## 📞 Need Help? / 需要帮助？

- **Documentation**: Read README.md and QUICKSTART.md / 阅读README.md和QUICKSTART.md
- **Examples**: Check `examples/` directory / 查看`examples/`目录
- **Code**: All functions have detailed comments / 所有函数都有详细注释
- **Templates**: Use `examples/custom_tool_template.py` / 使用自定义工具模板

---

## 🌟 You're Ready! / 你准备好了！

Everything you need is in this directory. Start with the Quick Start above and explore!
您需要的一切都在这个目录中。从上面的快速开始开始探索！

**Happy Coding! / 编程愉快！** 🚀

---

For detailed documentation, see:
详细文档请参阅：
- **QUICKSTART.md** - Quick start guide / 快速开始指南
- **README.md** - Full documentation / 完整文档
- **PROJECT_STRUCTURE.md** - Architecture / 架构说明
