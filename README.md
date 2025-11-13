![Banner](https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=12&height=200&section=header&text=LLM%20Agent%20Creator&fontSize=50&fontColor=fff&animation=fadeIn&desc=Build%20Powerful%20AI%20Agents&descAlignY=70) 

<div align="center">

> A complete solution integrating frontend UI and Python agent framework  

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![React](https://img.shields.io/badge/React-18-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![TypeScript](https://img.shields.io/badge/TypeScript-5.0-3178C6?style=for-the-badge&logo=typescript&logoColor=white)
![Vite](https://img.shields.io/badge/Vite-5.0-646CFF?style=for-the-badge&logo=vite&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**✨ Multi-Agent Orchestration | 🔌 API-Agnostic | 📊 Research-Oriented | ⚡ High Performance**

</div>

---

## 🎉 What's New! / 新功能！

### Latest Updates (2025-11-13) - Version 1.0

🚀 **Major Release - Production Ready!** Complete agent framework with advanced features:

#### 🌟 Core Features
1. **🤖 AI-Powered Tool Generation** - Generate custom tools using LLM! No coding required.
2. **🧠 ReAct Reasoning Mode** - Advanced reasoning with thought-action-observation loops.
3. **👥 Multiple Agent Roles** - Pre-configured roles: 通用助手, 数据分析师, 数学老师, 代码助手, 研究助手.
4. **💾 Agent Persistence** - Save and load agent configurations.
5. **🌊 Streaming Output** - Real-time streaming for better user experience.

#### 🎨 Dual Interface
- **🌐 Streamlit GUI** - Beautiful web interface with real-time streaming
- **� Enhanced CLI** - Full-featured command-line interface for developers

#### 🛠️ Tool Management
- 10 built-in tools (Math, Python REPL, Data Analysis, etc.)
- AI tool generation with natural language
- Custom tool support
- Organized tool storage and management

📖 **[See Documentation →](./docs/python-framework/)** | **[Quick Start →](./docs/python-framework/2025-11-12_QUICKSTART.md)** | **[Release Notes →](./docs/changelog/2025-11-13_RELEASE_v1.0.md)**

---

[English](#english) | [中文](#chinese)

---

## <a id="english"></a>English

### 📋 Project Overview

A complete platform for building and managing LLM agents, including:

1. **Python Agent Framework** - Flexible Python agent framework
2. **Web Frontend** - Modern frontend built with React + Vite

### 🗂️ Project Structure

📖 **[See Detailed Structure →](./docs/python-framework/2025-11-12_PROJECT_STRUCTURE.md)**

```
LLM-agent-creator/
├── 📁 python-agent-framework/    # ⭐ Main Python Framework (v1.0)
│   ├── core/                      # Core: Agent, LLM Client, Tools, Prompts
│   │   ├── agent.py               # Agent with ReAct reasoning
│   │   ├── llm_client.py          # LLM client with streaming
│   │   ├── prompts.py             # ReAct templates & role configs
│   │   └── tool.py                # Base tool class
│   ├── utils/                     # Tool Generator, Storage, Dynamic Loader
│   ├── tools/                     # 10 built-in tools + generated tools
│   ├── gui/                       # 🌐 Streamlit GUI (streaming support)
│   │   └── app.py                 # Full-featured web interface
│   ├── cli.py                     # 📟 Enhanced CLI interface
│   ├── agents_data/               # Saved agent configurations
│   ├── tools_data/                # Tool metadata & generated tools
│   └── examples/                  # Usage examples
│
├── 📁 src/                        # React frontend (optional)
├── 📁 docs/                       # 📚 Documentation
│   ├── python-framework/          # Framework guides
│   │   ├── 2025-11-12_QUICKSTART.md
│   │   ├── 2025-11-12_PROJECT_STRUCTURE.md
│   │   ├── 2025-11-12_TOOL_QUICKSTART.md
│   │   ├── 2025-11-13_CLI_GUIDE.md           # ⭐ CLI usage guide
│   │   └── 2025-11-13_STREAMING_FEATURE.md   # ⭐ Streaming docs
│   └── changelog/                 # Version history
│
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

# 4. Choose your interface:

# Option A: Streamlit GUI (Recommended for visual interaction)
streamlit run gui/app.py

# Option B: CLI Mode (Recommended for developers)
python cli.py
```

**First Time Setup:**
1. Configure LLM (API URL, Key, Model)
2. Create an agent with desired role and tools
3. Start chatting with streaming output!

📖 **Detailed Guides:**
- [Quick Start Guide](./docs/python-framework/2025-11-12_QUICKSTART.md)
- [CLI Guide](./docs/python-framework/2025-11-13_CLI_GUIDE.md)
- [Streaming Feature](./docs/python-framework/2025-11-13_STREAMING_FEATURE.md)

#### Frontend (Optional)

```bash
# 1. Install dependencies at project root
npm install

# 2. Start development server
npm run dev

# 3. Build for production
npm run build
```

### 📚 Documentation

See [docs/README.md](./docs/README.md) for complete documentation index.

**Recommended Reading Order**:
1. [Quick Start](./docs/python-framework/2025-11-12_QUICKSTART.md) - Get started in 5 minutes
2. [Project Structure](./docs/python-framework/2025-11-12_PROJECT_STRUCTURE.md) - Understand the codebase
3. [Tool Quick Start](./docs/python-framework/2025-11-12_TOOL_QUICKSTART.md) - Create custom tools
4. [CLI Guide](./docs/python-framework/2025-11-13_CLI_GUIDE.md) - Command-line interface
5. [Streaming Feature](./docs/python-framework/2025-11-13_STREAMING_FEATURE.md) - Real-time output

**Version 1.0 Highlights:**
- 🧠 ReAct reasoning with role templates
- 🌊 Streaming output in both GUI and CLI
- 💾 Agent persistence system
- 🤖 AI-powered tool generation
- 📟 Full-featured CLI interface

### ✨ Key Features

#### Python Agent Framework (v1.0)

**🧠 Advanced Reasoning**
- 🎯 **ReAct Mode** - Thought-Action-Observation reasoning loop
- � **Role Templates** - 5 pre-configured roles (通用助手, 数据分析师, 数学老师, 代码助手, 研究助手)
- 🔄 **Iterative Execution** - Multi-step task solving with tool calls

**🌊 Streaming & Real-time**
- 💬 **Streaming Chat** - Real-time output in both GUI and CLI
- 👀 **Visible Reasoning** - See every thought, tool call, and result
- ⚡ **Immediate Feedback** - No waiting for complete responses

**🛠️ Tool Ecosystem**
- 📦 **10 Built-in Tools** - Math, Python REPL, Data Analysis, File I/O, etc.
- 🤖 **AI Tool Generation** - Create tools using natural language
- 💾 **Tool Persistence** - Organized storage and management
- 🔌 **Easy Extension** - Simple tool creation framework

**💾 Agent Management**
- 📋 **Save/Load Agents** - Persistent agent configurations
- 🎨 **Custom Instructions** - Personalize agent behavior
- 🔧 **Flexible Configuration** - Choose tools, roles, and settings

**🎨 Dual Interface**
- 🌐 **Streamlit GUI** - Beautiful web interface with drag-and-drop
- � **Enhanced CLI** - Full-featured terminal interface with colors
- 🔄 **Feature Parity** - Both interfaces have identical capabilities

**🔌 Integration**
- 🌍 **API-Agnostic** - Works with any LLM API (OpenAI, Claude, etc.)
- 📊 **Research-Oriented** - Built-in scientific computing tools
- 🐍 **Pure Python** - No complex dependencies

#### Web Frontend

- ⚡ **Fast Development** - Vite + React + TypeScript
- 🎨 **Modern Design** - Tailwind CSS styling
- 🔍 **Type Safety** - Full TypeScript support

### 🛠️ Tech Stack

**Python Framework (v1.0)**:
- Python 3.8+
- Streamlit (Web GUI)
- Rich terminal formatting (CLI)
- OpenAI-compatible APIs
- JSON-based storage

**Frontend (Optional)**:
- React 18
- TypeScript
- Vite
- Tailwind CSS

**Core Dependencies**:
```
openai
streamlit
python-dotenv
requests
```

### 📖 Examples

Check the [examples/](./python-agent-framework/examples/) directory for more examples.

### 🤝 Contributing

Issues and Pull Requests are welcome!

### 📄 License

See [LICENSE](./LICENSE) file for details.

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

# 4. 选择界面启动：

# 方式A: Streamlit图形界面（推荐用于可视化交互）
streamlit run gui/app.py

# 方式B: CLI命令行模式（推荐用于开发者）
python cli.py
```

**首次使用步骤：**
1. 配置LLM（API地址、密钥、模型）
2. 创建智能体（选择角色和工具）
3. 开始对话（支持流式输出）！

📖 **详细指南：**
- [快速开始](./docs/python-framework/2025-11-12_QUICKSTART.md)
- [CLI使用指南](./docs/python-framework/2025-11-13_CLI_GUIDE.md)
- [流式输出功能](./docs/python-framework/2025-11-13_STREAMING_FEATURE.md)

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

**推荐阅读顺序**：
1. [快速开始](./docs/python-framework/2025-11-12_QUICKSTART.md) - 5分钟上手
2. [项目结构](./docs/python-framework/2025-11-12_PROJECT_STRUCTURE.md) - 理解代码结构
3. [工具快速入门](./docs/python-framework/2025-11-12_TOOL_QUICKSTART.md) - 创建自定义工具
4. [CLI使用指南](./docs/python-framework/2025-11-13_CLI_GUIDE.md) - 命令行界面
5. [流式输出功能](./docs/python-framework/2025-11-13_STREAMING_FEATURE.md) - 实时输出

**v1.0 版本亮点：**
- 🧠 ReAct推理模式与角色模板
- 🌊 GUI和CLI双界面流式输出
- 💾 智能体持久化系统
- 🤖 AI驱动的工具生成
- 📟 功能完整的CLI界面

### ✨ 主要特性

#### Python Agent Framework (v1.0)

**🧠 高级推理**
- 🎯 **ReAct模式** - 思考-行动-观察推理循环
- � **角色模板** - 5个预配置角色（通用助手、数据分析师、数学老师、代码助手、研究助手）
- 🔄 **迭代执行** - 多步骤任务求解与工具调用

**🌊 流式与实时**
- 💬 **流式聊天** - GUI和CLI双界面实时输出
- 👀 **可见推理** - 看到每一步思考、工具调用和结果
- ⚡ **即时反馈** - 无需等待完整响应

**🛠️ 工具生态**
- 📦 **10个内置工具** - 数学计算、Python执行、数据分析、文件操作等
- 🤖 **AI工具生成** - 使用自然语言创建工具
- 💾 **工具持久化** - 有组织的存储和管理
- 🔌 **易于扩展** - 简单的工具创建框架

**💾 智能体管理**
- 📋 **保存/加载智能体** - 持久化智能体配置
- 🎨 **自定义指令** - 个性化智能体行为
- 🔧 **灵活配置** - 选择工具、角色和设置

**🎨 双界面**
- 🌐 **Streamlit GUI** - 美观的Web界面
- 📟 **增强CLI** - 全功能终端界面（彩色输出）
- 🔄 **功能对等** - 两个界面功能完全一致

**� 集成能力**
- 🌍 **API无关** - 支持任何LLM API（OpenAI、Claude等）
- 📊 **科研导向** - 内置科学计算工具
- 🐍 **纯Python** - 无复杂依赖

#### Web Frontend

- ⚡ **快速开发** - Vite + React + TypeScript
- 🎨 **现代设计** - Tailwind CSS样式
- 🔍 **类型安全** - 完整的TypeScript支持

### 🛠️ 技术栈

**Python框架 (v1.0)**：
- Python 3.8+
- Streamlit（Web界面）
- Rich终端格式化（CLI）
- OpenAI兼容API
- JSON数据存储

**前端（可选）**：
- React 18
- TypeScript
- Vite
- Tailwind CSS

**核心依赖**：
```
openai
streamlit
python-dotenv
requests
```

### � 使用示例

查看 [examples/](./python-agent-framework/examples/) 目录了解更多示例。

### 🤝 贡献

欢迎提交Issue和Pull Request！

### 📄 许可证

详见 [LICENSE](./LICENSE) 文件。

---