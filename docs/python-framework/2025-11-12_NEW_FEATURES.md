# New Features Guide / 新功能指南

## 🎉 What's New / 新增功能

This guide covers all the new features added to the LLM Agent Framework.
本指南涵盖了LLM智能体框架的所有新功能。

---

## 🛠️ 1. AI-Powered Tool Generation / AI驱动的工具生成

Generate custom tools using AI! Simply describe what you need, and the LLM will create the Python code for you.
使用AI生成自定义工具！只需描述您的需求，LLM就会为您创建Python代码。

### Features / 功能特点

- **Modular Input Forms** / 模块化输入表单 - Guided tool specification
- **LLM Code Generation** / LLM代码生成 - Automatically generate tool code
- **File Storage** / 文件存储 - Save tools as Python files
- **Metadata Tracking** / 元数据跟踪 - Track tool information

### How to Use (Streamlit GUI) / 使用方法（Streamlit界面）

1. **Connect to LLM** / 连接到LLM
   - Go to sidebar → Enter API credentials
   - Click "Test Connection" 
   - ✅ Connection successful!

2. **Navigate to Tool Generator** / 进入工具生成器
   - Select "Generate Tool | 生成工具" from the menu

3. **Specify Your Tool** / 指定工具规格
   ```
   Tool Name: WeatherFetcher
   Description: Fetch weather data for a given city
   
   Input Parameters:
   - city (str): Name of the city
   - units (str): Temperature units (celsius/fahrenheit)
   
   Expected Output: Weather information including temperature, humidity
   
   Implementation Hints (optional): Use requests library to call weather API
   
   Dependencies: requests
   ```

4. **Generate** / 生成
   - Click "🚀 Generate Tool"
   - Wait for LLM to create the code
   - Review the generated code
   - Tool is automatically saved!

### How to Use (CLI) / 使用方法（命令行）

```bash
# Start CLI
python cli.py

# Select option 2: Generate New Tool
# Follow the prompts to specify your tool
```

### Generated Tool Location / 生成的工具位置

- **Code**: `tools/generated/your_tool_name.py`
- **Metadata**: `tools_data/generated_metadata/your_tool_name.json`

---

## 🔍 2. Smart Tool Indexing & Search / 智能工具索引和搜索

Automatically find the right tools for your task! The system indexes all available tools and searches based on relevance.
自动找到适合您任务的工具！系统索引所有可用工具并基于相关性搜索。

### Features / 功能特点

- **Automatic Indexing** / 自动索引 - All tools are indexed
- **Keyword Matching** / 关键词匹配 - Intelligent search
- **Relevance Scoring** / 相关性评分 - Best tools first
- **Cost Reduction** / 成本降低 - Only send relevant tools to LLM

### How It Works / 工作原理

```python
from utils.tool_indexer import ToolIndexer

# Create indexer
indexer = ToolIndexer()

# Search for tools
results = indexer.search_tools(
    "calculate mathematical expressions",
    max_results=5
)

# Results are sorted by relevance score
for tool in results:
    print(f"{tool['name']}: {tool['score']}")
```

### In CLI / 在CLI中

```bash
# Start CLI
python cli.py

# Select option 4: Search Tools
# Enter your task description
# See relevant tools ranked by score
```

### Benefits / 优势

- **💰 Save Tokens** - Only send relevant tools to LLM
- **⚡ Faster Responses** - Less context to process
- **🎯 Better Results** - Agent uses right tools

---

## 💻 3. CLI Mode / 命令行模式

Run the framework without Streamlit! Perfect for terminal users and automation.
无需Streamlit运行框架！适合终端用户和自动化。

### How to Start / 启动方法

```bash
# Navigate to framework directory
cd python-agent-framework

# Run CLI
python cli.py
```

### Features / 功能

```
╔═══════════════════════════════════════════════════════════╗
║          🤖 LLM Agent Framework - CLI Mode 🤖             ║
╚═══════════════════════════════════════════════════════════╝

📋 Main Menu
1. 💬 Chat with Agent
2. 🛠️  Generate New Tool
3. 📚 List Available Tools
4. 🔍 Search Tools
5. ⚙️  Reconfigure LLM
6. 📜 View Chat History
7. 🗑️  Clear Chat History
0. 🚪 Exit
```

### Interactive Chat / 交互式对话

```bash
# Select option 1: Chat with Agent
# Describe your task
# Agent automatically selects relevant tools
# Chat naturally with the agent
```

### Environment Variables / 环境变量

CLI can read from `.env` file:

```bash
# Create .env file
cp .env.example .env

# Edit .env
nano .env

# Add your credentials
API_URL=https://api.metaihub.cn/v1/chat/completions
API_KEY=sk-your-key-here
MODEL=gpt-4o-mini
```

---

## ✅ 4. Improved Connection Testing / 改进的连接测试

Test LLM connection without spending much! Simple test keeps costs low.
测试LLM连接而不花费太多！简单测试保持低成本。

### How It Works / 工作原理

**Before** / 之前:
```python
# Complex test, high cost
client.chat("Explain quantum physics...")
```

**Now** / 现在:
```python
# Simple test, low cost (max 5 tokens)
client.chat("Hi", max_tokens=5)
```

### In GUI / 在GUI中

- Click "Test Connection | 测试连接"
- Sends: "Hi" (3 characters)
- Receives: ~5 tokens response
- ✅ Connection verified with minimal cost!

### Cost Comparison / 成本对比

| Test Type | Input Tokens | Output Tokens | Approx Cost (GPT-4o-mini) |
|-----------|--------------|---------------|---------------------------|
| Old | ~50 | ~100 | $0.003 |
| **New** | **~3** | **~5** | **$0.0001** |

**Savings: 97% less cost per test!** / 节省：每次测试成本降低97%！

---

## 📦 5. Tool Database System / 工具数据库系统

All generated tools are stored systematically for easy management.
所有生成的工具都系统地存储以便管理。

### Directory Structure / 目录结构

```
python-agent-framework/
├── tools/
│   ├── generated/              # Generated tool code
│   │   ├── weather_fetcher.py
│   │   ├── pdf_parser.py
│   │   └── ...
│   ├── base_tools.py           # Built-in tools
│   └── ...
│
└── tools_data/
    └── generated_metadata/     # Tool metadata
        ├── weather_fetcher.json
        ├── pdf_parser.json
        └── ...
```

### Metadata Format / 元数据格式

```json
{
  "name": "WeatherFetcher",
  "description": "Fetch weather data for a given city",
  "file_path": "/path/to/weather_fetcher.py",
  "created_at": "2024-01-15T10:30:00",
  "input_parameters": [
    {
      "name": "city",
      "type": "str",
      "description": "Name of the city"
    }
  ],
  "expected_output": "Weather information",
  "dependencies": ["requests"]
}
```

### Management / 管理

```python
from utils.tool_generator import ToolGenerator

generator = ToolGenerator(llm_client)

# List all generated tools
tools = generator.list_generated_tools()

# Delete a tool
generator.delete_tool("WeatherFetcher")
```

---

## 🚀 Quick Start Guide / 快速开始指南

### Method 1: Streamlit GUI / Streamlit界面

```bash
# 1. Setup environment
cd python-agent-framework
cp .env.example .env
# Edit .env with your API credentials

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run Streamlit
streamlit run gui/app.py

# 4. In the browser:
#    - Connect to LLM
#    - Generate tools
#    - Create agents
#    - Start chatting!
```

### Method 2: CLI Mode / 命令行模式

```bash
# 1. Setup environment (same as above)
cd python-agent-framework
cp .env.example .env
# Edit .env

# 2. Run CLI
python cli.py

# 3. Follow interactive prompts
#    - Configure LLM
#    - Generate tools
#    - Chat with agent
```

---

## 📊 Testing / 测试

### Run Test Suite / 运行测试套件

```bash
cd python-agent-framework
python test_new_features.py
```

### What It Tests / 测试内容

1. ✅ LLM Connection (with your API)
2. ✅ Tool Generation
3. ✅ Tool Indexing & Search
4. ✅ Agent with Tool Selection
5. ✅ CLI Availability
6. ✅ File Structure

### Expected Output / 预期输出

```
╔═══════════════════════════════════════════════════════════╗
║       🧪 LLM Agent Framework - Test Suite 🧪              ║
╚═══════════════════════════════════════════════════════════╝

Test 1: LLM Connection Test
✅ Connection successful!

Test 2: Tool Generator Test
✅ Tool generated successfully!

Test 3: Tool Indexer Test
✅ Found 10 available tools

Test 4: Agent with Tool Indexing
✅ Agent completed successfully!

Test 5: CLI Availability Test
✅ CLI script found

✅ All tests completed!
```

---

## 💡 Best Practices / 最佳实践

### 1. Tool Generation / 工具生成

- **Be Specific** / 具体明确 - Clear descriptions get better results
- **Test Generated Tools** / 测试生成的工具 - Review and test before using
- **Iterate** / 迭代 - Regenerate if needed
- **Save Prompts** / 保存提示 - Keep track of what works

### 2. Tool Indexing / 工具索引

- **Use Descriptive Names** / 使用描述性名称 - Helps with search
- **Good Descriptions** / 良好的描述 - Improves relevance scoring
- **Refresh Index** / 刷新索引 - After generating new tools

### 3. Cost Management / 成本管理

- **Test Connection Once** / 测试连接一次 - Don't test repeatedly
- **Use Tool Search** / 使用工具搜索 - Reduce token usage
- **Limit Max Tokens** / 限制最大令牌 - Control output length
- **Choose Right Model** / 选择正确模型 - Use mini for simple tasks

### 4. CLI vs GUI / 命令行 vs 图形界面

**Use CLI when** / 使用CLI当：
- ✅ Remote server access
- ✅ Automation scripts
- ✅ Minimal resource usage
- ✅ Terminal preference

**Use GUI when** / 使用GUI当：
- ✅ Visual feedback needed
- ✅ Complex configurations
- ✅ Multiple tabs/views
- ✅ Easier for beginners

---

## 🔧 Troubleshooting / 故障排除

### Connection Issues / 连接问题

```bash
# Test your API manually
curl -X POST https://api.metaihub.cn/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "model": "gpt-4o-mini",
    "messages": [{"role": "user", "content": "Hi"}],
    "max_tokens": 5
  }'
```

### Tool Generation Fails / 工具生成失败

1. **Check LLM Connection** / 检查LLM连接
2. **Verify Prompt** / 验证提示 - Is description clear?
3. **Try Again** / 重试 - LLM outputs can vary
4. **Simplify** / 简化 - Start with simpler tools

### CLI Won't Start / CLI无法启动

```bash
# Make sure you're in the right directory
cd python-agent-framework

# Check Python version (3.8+)
python --version

# Try with python3
python3 cli.py
```

---

## 📚 Examples / 示例

### Example 1: Generate Web Scraper Tool

```
Tool Name: WebScraper
Description: Scrape text content from a webpage
Input Parameters:
  - url (str): URL of the webpage to scrape
  - selector (str): CSS selector to extract (optional)
Expected Output: Extracted text content from the webpage
Dependencies: requests, beautifulsoup4
```

### Example 2: Generate Data Validator Tool

```
Tool Name: DataValidator
Description: Validate data against specified rules
Input Parameters:
  - data (dict): Data to validate
  - rules (dict): Validation rules
Expected Output: Validation result with pass/fail and errors
Implementation Hints: Check for required fields, data types, ranges
```

### Example 3: Use Tool Indexer in Agent

```python
from utils.tool_indexer import ToolIndexer

# Create indexer
indexer = ToolIndexer()

# Get relevant tools for task
task = "I need to download a file and analyze its contents"
tools = indexer.search_tools(task, max_results=3)

# Create agent with only relevant tools
from core.agent import Agent
agent = Agent(
    name="TaskAgent",
    llm_client=client,
    tools=[get_tool_by_name(t['name']) for t in tools]
)

# Run with minimal context
result = agent.run(task)
```

---

## 🎓 Learn More / 了解更多

- [Main Documentation](../docs/README.md)
- [Tool Quick Start](../docs/python-framework/TOOL_QUICKSTART.md)
- [Project Structure](../docs/python-framework/PROJECT_STRUCTURE.md)

---

## 🆘 Support / 支持

If you encounter issues / 如果遇到问题:

1. Check this guide / 查看本指南
2. Run test suite / 运行测试套件
3. Review error messages / 查看错误消息
4. Check GitHub issues / 查看GitHub问题

---

**Happy Building! / 开心构建！** 🚀
