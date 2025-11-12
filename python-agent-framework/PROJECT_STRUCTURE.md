# Project Structure / 项目结构

## Directory Overview / 目录概览

```
python-agent-framework/
│
├── README.md                      # Complete documentation / 完整文档
├── QUICKSTART.md                  # Quick start guide / 快速开始指南
├── PROJECT_STRUCTURE.md           # This file / 本文件
├── requirements.txt               # Python dependencies / Python依赖
├── .env.example                   # Environment variables template / 环境变量模板
├── .gitignore                     # Git ignore rules / Git忽略规则
│
├── core/                          # Core framework components / 核心框架组件
│   ├── __init__.py               # Module exports / 模块导出
│   ├── agent.py                  # Agent class (250+ lines) / 智能体类
│   ├── tool.py                   # Tool base class and registry / 工具基类和注册表
│   ├── llm_client.py             # LLM API client / LLM API客户端
│   └── orchestrator.py           # Multi-agent orchestrators / 多智能体编排器
│
├── tools/                         # Built-in tools / 内置工具
│   ├── __init__.py               # Tool exports / 工具导出
│   ├── base_tools.py             # Basic tools (Calculator, File I/O, etc.) / 基础工具
│   ├── research_tools.py         # Scientific computing tools / 科学计算工具
│   └── data_tools.py             # Data analysis and visualization / 数据分析和可视化
│
├── gui/                           # Streamlit GUI / Streamlit图形界面
│   └── app.py                    # Main GUI application / 主GUI应用
│
├── utils/                         # Utility modules / 实用工具模块
│   ├── __init__.py               # Utility exports / 工具导出
│   └── storage.py                # Supabase storage integration / Supabase存储集成
│
└── examples/                      # Usage examples / 使用示例
    ├── basic_usage.py            # Basic agent examples / 基础智能体示例
    ├── orchestration_examples.py # Multi-agent orchestration / 多智能体编排
    ├── research_workflow.py      # Complete research workflow / 完整研究工作流
    └── custom_tool_template.py   # Template for custom tools / 自定义工具模板
```

## Core Components / 核心组件

### 1. Agent (`core/agent.py`)
**Purpose:** Core agent that combines LLM and tools to execute tasks
**用途:** 结合LLM和工具执行任务的核心智能体

**Key Features:**
- Tool calling and execution
- Conversation memory management
- Reasoning loop implementation
- Execution logging

**主要特性:**
- 工具调用和执行
- 对话记忆管理
- 推理循环实现
- 执行日志记录

### 2. Tool (`core/tool.py`)
**Purpose:** Base class for all tools with parameter validation
**用途:** 所有工具的基类，带参数验证

**Key Features:**
- Abstract base class pattern
- Parameter schema definition
- Tool registry for management
- Type validation

### 3. LLMClient (`core/llm_client.py`)
**Purpose:** Unified client for various LLM APIs
**用途:** 各种LLM API的统一客户端

**Supported APIs:**
- OpenAI-compatible endpoints
- Claude (Anthropic)
- Custom endpoints

**支持的API:**
- OpenAI兼容端点
- Claude (Anthropic)
- 自定义端点

### 4. Orchestrator (`core/orchestrator.py`)
**Purpose:** Coordinate multiple agents working together
**用途:** 协调多个智能体协同工作

**Patterns:**
- Sequential: Agents work one after another / 顺序：智能体依次工作
- Parallel: Agents work simultaneously / 并行：智能体同时工作
- Hierarchical: Manager delegates to workers / 层级：管理者委派给工作者
- Conditional: Route based on conditions / 条件：基于条件路由
- Custom: Implement your own pattern / 自定义：实现自己的模式

## Built-in Tools / 内置工具

### Base Tools (`tools/base_tools.py`)
1. **CalculatorTool** - Mathematical calculations / 数学计算
2. **FileIOTool** - File reading and writing / 文件读写
3. **PythonREPLTool** - Execute Python code / 执行Python代码
4. **WebSearchTool** - Internet search / 互联网搜索
5. **TextProcessingTool** - Text manipulation / 文本处理

### Research Tools (`tools/research_tools.py`)
1. **ScientificComputeTool** - NumPy/SciPy operations / NumPy/SciPy运算
2. **StatisticalTestTool** - Hypothesis testing / 假设检验
3. **LiteratureSearchTool** - Paper search (placeholder) / 论文搜索（占位符）
4. **UnitConverterTool** - Scientific unit conversion / 科学单位转换

### Data Tools (`tools/data_tools.py`)
1. **DataAnalysisTool** - Pandas data analysis / Pandas数据分析
2. **VisualizationTool** - Create charts with Plotly / 使用Plotly创建图表
3. **DataCleaningTool** - Data preprocessing / 数据预处理

## Usage Examples / 使用示例

### 1. Basic Usage (`examples/basic_usage.py`)
- Simple agent creation / 简单智能体创建
- Tool usage / 工具使用
- Conversation memory / 对话记忆
- Custom prompts / 自定义提示
- Execution logs / 执行日志

### 2. Orchestration (`examples/orchestration_examples.py`)
- Sequential workflow / 顺序工作流
- Parallel execution / 并行执行
- Hierarchical coordination / 层级协调
- Custom workflows / 自定义工作流

### 3. Research Workflow (`examples/research_workflow.py`)
- Complete research pipeline / 完整研究流程
- Data collection and analysis / 数据收集和分析
- Statistical testing / 统计检验
- Visualization / 可视化

### 4. Custom Tools (`examples/custom_tool_template.py`)
- Tool creation template / 工具创建模板
- Best practices / 最佳实践
- Example implementations / 示例实现

## GUI Application / GUI应用

The Streamlit GUI (`gui/app.py`) provides:
Streamlit GUI提供：

1. **LLM Configuration** - Set up API credentials / 设置API凭证
2. **Agent Creation** - Create agents with tools / 创建带工具的智能体
3. **Chat Interface** - Interactive chat / 交互式聊天
4. **Orchestration** - Multi-agent workflows / 多智能体工作流
5. **Analytics** - Usage statistics and logs / 使用统计和日志

## Key Design Principles / 关键设计原则

1. **Modularity** - Clear separation of concerns / 清晰的关注点分离
2. **Extensibility** - Easy to add new tools and patterns / 易于添加新工具和模式
3. **API-Agnostic** - Works with any LLM API / 适用于任何LLM API
4. **Research-Focused** - Built-in scientific tools / 内置科学工具
5. **Bilingual** - English and Chinese documentation / 中英文文档

## Code Statistics / 代码统计

- **Core Framework:** ~1500 lines / 核心框架：约1500行
- **Built-in Tools:** ~1200 lines / 内置工具：约1200行
- **GUI Application:** ~400 lines / GUI应用：约400行
- **Examples:** ~800 lines / 示例：约800行
- **Documentation:** Extensive inline comments / 文档：广泛的内联注释

## Dependencies / 依赖

**Core:**
- requests - HTTP client / HTTP客户端
- python-dotenv - Environment variables / 环境变量
- pydantic - Data validation / 数据验证

**Scientific:**
- numpy - Numerical computing / 数值计算
- scipy - Scientific computing / 科学计算
- pandas - Data analysis / 数据分析

**Visualization:**
- matplotlib - Static plots / 静态图表
- plotly - Interactive plots / 交互式图表

**GUI:**
- streamlit - Web interface / Web界面

**Storage:**
- supabase - Database integration / 数据库集成

## Extending the Framework / 扩展框架

### Add a New Tool / 添加新工具

1. Create a new class inheriting from `Tool`
2. Implement `__init__` and `execute` methods
3. Add to appropriate tools module
4. Import in `tools/__init__.py`

### Add a New Orchestrator / 添加新编排器

1. Inherit from `Orchestrator` or `CustomOrchestrator`
2. Implement the `run` or `orchestrate` method
3. Add to `core/orchestrator.py`
4. Export in `core/__init__.py`

### Integrate a New LLM API / 集成新LLM API

1. Add new method in `LLMClient` (e.g., `_custom_api_chat`)
2. Update the `chat` method to route to your new method
3. Add configuration in `.env.example`

## Best Practices / 最佳实践

1. **Tool Design**
   - Single responsibility principle / 单一职责原则
   - Clear, descriptive names / 清晰、描述性的名称
   - Comprehensive error handling / 全面的错误处理
   - Return structured dicts / 返回结构化字典

2. **Agent Configuration**
   - Use specific system prompts / 使用特定的系统提示
   - Enable memory for conversational tasks / 为对话任务启用记忆
   - Limit tools to what's needed / 限制工具为所需
   - Monitor execution logs / 监控执行日志

3. **Orchestration**
   - Choose appropriate pattern / 选择适当的模式
   - Handle errors gracefully / 优雅地处理错误
   - Log intermediate results / 记录中间结果
   - Test with simple tasks first / 先用简单任务测试

## License / 许可证

MIT License - Free for research and commercial use
MIT许可证 - 可免费用于研究和商业用途

## Support / 支持

- Read the README.md for detailed documentation / 阅读README.md获取详细文档
- Check examples/ for code samples / 查看examples/获取代码示例
- Review inline code comments / 查看内联代码注释
- Create issues for bugs or feature requests / 为错误或功能请求创建问题
