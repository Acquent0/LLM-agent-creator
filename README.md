![Banner](https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=12&height=200&section=header&text=LLM%20Agent%20Creator&fontSize=50&fontColor=fff&animation=fadeIn&desc=Build%20Powerful%20AI%20Agents&descAlignY=70) 

<center>
> A complete solution integrating frontend UI and Python agent framework

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![React](https://img.shields.io/badge/React-18-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![TypeScript](https://img.shields.io/badge/TypeScript-5.0-3178C6?style=for-the-badge&logo=typescript&logoColor=white)
![Vite](https://img.shields.io/badge/Vite-5.0-646CFF?style=for-the-badge&logo=vite&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**✨ Multi-Agent Orchestration | 🔌 API-Agnostic | 📊 Research-Oriented | ⚡ High Performance**

[English](#english) | [中文](#chinese)

</center>

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
- 🔍 **类型安全** - 完整的TypeScript支持

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