# 📁 Project Structure / 项目结构

**最后更新**: 2024-11-12  
**版本**: v1.2.0

---

## 🗂️ 目录结构总览

```
LLM-agent-creator/
├── 📄 核心文档 (Root Documentation)
│   ├── README.md                    # 项目介绍和快速开始
│   ├── GETTING_STARTED.md          # 详细入门指南
│   ├── PROJECT_STRUCTURE.md        # 本文件 - 项目结构说明
│   └── LICENSE                      # 开源许可证
│
├── 📚 文档 (Documentation)
│   ├── docs/
│   │   ├── README.md               # 文档目录索引
│   │   ├── changelog/              # 📝 版本日志文件夹 (NEW!)
│   │   │   ├── README.md           # 变更日志索引
│   │   │   ├── REORGANIZATION_COMPLETE.md    # v1.2.0 - 重组报告
│   │   │   ├── UPDATE_LOG.md                 # v1.1.0 - 更新日志
│   │   │   ├── IMPLEMENTATION_SUMMARY.md     # v1.0.0 - 实现总结
│   │   │   ├── FILES_CHANGED.md              # v1.1.0 - 文件变更
│   │   │   └── CLEANUP_SUMMARY.md            # v1.1.1 - 清理总结
│   │   │
│   │   └── python-framework/       # Python 框架专属文档
│   │       ├── NEW_FEATURES.md     # 新功能详细说明
│   │       ├── PROJECT_STRUCTURE.md # 框架内部结构
│   │       ├── QUICKSTART.md       # 快速开始指南
│   │       └── TOOL_QUICKSTART.md  # 工具快速指南
│
├── 🐍 Python Agent Framework (核心框架)
│   └── python-agent-framework/
│       ├── 🧠 核心模块 (Core)
│       │   ├── core/
│       │   │   ├── agent.py        # Agent 主逻辑
│       │   │   ├── llm_client.py   # LLM API 客户端
│       │   │   ├── orchestrator.py # 任务编排器
│       │   │   └── tool.py         # 工具基类
│       │
│       ├── 🛠️ 工具系统 (Tools)
│       │   ├── tools/
│       │   │   ├── base_tools.py   # 基础工具集
│       │   │   ├── data_tools.py   # 数据处理工具
│       │   │   ├── research_tools.py # 研究类工具
│       │   │   └── generated/      # AI生成的自定义工具
│       │   │
│       │   └── tools_data/         # 工具数据存储
│       │       ├── custom_tools.json    # 自定义工具元数据
│       │       ├── example_tools.json   # 示例工具
│       │       └── README.md
│       │
│       ├── 🔧 工具集 (Utils)
│       │   └── utils/
│       │       ├── tool_generator.py   # 🆕 AI工具生成器
│       │       ├── tool_indexer.py     # 🆕 智能工具索引
│       │       ├── tool_storage.py     # 工具存储管理
│       │       ├── dynamic_tool.py     # 动态工具加载
│       │       └── storage.py          # 通用存储
│       │
│       ├── 🎨 用户界面 (GUI)
│       │   └── gui/
│       │       └── app.py          # Streamlit GUI (含工具生成页面)
│       │
│       ├── 💻 命令行界面 (CLI)
│       │   └── cli.py              # 🆕 完整的CLI交互界面
│       │
│       ├── 📝 示例代码 (Examples)
│       │   └── examples/
│       │       ├── basic_usage.py
│       │       ├── custom_tool_template.py
│       │       ├── orchestration_examples.py
│       │       └── research_workflow.py
│       │
│       ├── ✅ 测试文件 (Tests)
│       │   └── test_new_features.py    # 新功能测试套件
│       │
│       └── 📦 配置文件
│           ├── requirements.txt    # Python依赖
│           ├── setup.sh           # 安装脚本
│           └── README.md          # 框架说明
│
├── 🌐 Web Frontend (可选的Web界面)
│   ├── src/                       # React/TypeScript 源码
│   ├── index.html
│   ├── package.json
│   ├── vite.config.ts
│   └── tsconfig.json
│
├── 📤 输出文件夹
│   ├── outputs/                   # 运行时生成的输出
│   └── assets/                    # 静态资源
│
└── ⚙️ 配置文件
    ├── .gitignore
    ├── eslint.config.js
    ├── postcss.config.js
    └── tailwind.config.js
```

---

## 📋 文档导航指南

### 🚀 快速开始
1. **首次使用**: 阅读 [`README.md`](README.md)
2. **详细设置**: 阅读 [`GETTING_STARTED.md`](GETTING_STARTED.md)
3. **Python框架**: 进入 [`python-agent-framework/README.md`](python-agent-framework/README.md)

### 📖 深入学习
- **新功能说明**: [`docs/python-framework/NEW_FEATURES.md`](docs/python-framework/NEW_FEATURES.md)
- **工具快速指南**: [`docs/python-framework/TOOL_QUICKSTART.md`](docs/python-framework/TOOL_QUICKSTART.md)
- **框架快速开始**: [`docs/python-framework/QUICKSTART.md`](docs/python-framework/QUICKSTART.md)

### 📝 版本历史
查看 [`docs/changelog/`](docs/changelog/) 文件夹:
- **v1.2.0**: 项目结构重组 (最新)
- **v1.1.0**: 新功能实现
- **v1.0.0**: 初始版本

---

## 🎯 核心功能模块说明

### 1️⃣ Agent System (智能体系统)
- **位置**: `python-agent-framework/core/`
- **功能**: 任务规划、工具调用、响应生成

### 2️⃣ Tool System (工具系统)
- **位置**: `python-agent-framework/tools/`
- **功能**: 
  - 内置工具: 计算器、网页搜索、文件操作等
  - AI生成工具: 使用LLM自动生成自定义工具
  - 工具索引: 智能工具搜索和推荐

### 3️⃣ Utility System (工具集)
- **位置**: `python-agent-framework/utils/`
- **功能**:
  - 🆕 `tool_generator.py`: AI驱动的工具生成
  - 🆕 `tool_indexer.py`: 智能工具索引和检索
  - `tool_storage.py`: 工具持久化存储

### 4️⃣ Interface (用户界面)
- **GUI**: `python-agent-framework/gui/app.py` (Streamlit)
- **CLI**: `python-agent-framework/cli.py` (命令行)

---

## 🔧 开发指南

### 添加新功能
1. 在相应模块下创建文件
2. 更新 `requirements.txt` (如需新依赖)
3. 在 `examples/` 下添加示例
4. 更新相关文档

### 文档更新规范
- **核心文档**: 直接更新根目录文件
- **版本日志**: 在 `docs/changelog/` 创建新版本文件
- **功能文档**: 更新 `docs/python-framework/` 下对应文件

---

## 📊 项目统计

- **总文档数**: 约20个Markdown文件
- **Python模块**: 15+ 个核心模块
- **内置工具**: 10+ 个预定义工具
- **代码行数**: 2000+ 行Python代码

---

## 🔍 快速查找

| 我想... | 查看这个文件 |
|--------|------------|
| 快速开始使用 | `GETTING_STARTED.md` |
| 了解新功能 | `docs/python-framework/NEW_FEATURES.md` |
| 查看版本历史 | `docs/changelog/README.md` |
| 生成自定义工具 | `docs/python-framework/TOOL_QUICKSTART.md` |
| 了解CLI使用 | `python-agent-framework/cli.py` (内含帮助) |
| 查看代码示例 | `python-agent-framework/examples/` |

---

**💡 提示**: 所有文档都包含中英双语说明，方便不同用户使用。
