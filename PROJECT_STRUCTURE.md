# 项目结构说明 / Project Structure Guide

## 📂 整体结构

```
LLM-agent-creator/
│
├── 📁 python-agent-framework/     # Python智能体框架（后端核心）
│   ├── 📁 core/                   # 核心组件
│   ├── 📁 tools/                  # 内置工具集
│   ├── 📁 gui/                    # Streamlit用户界面
│   ├── 📁 examples/               # 使用示例代码
│   ├── 📁 utils/                  # 辅助工具函数
│   ├── 📁 tools_data/             # 工具配置数据
│   ├── 📄 requirements.txt        # Python依赖
│   ├── 📄 setup.sh               # 安装脚本
│   └── 📄 README.md              # 框架说明文档
│
├── 📁 src/                        # React前端源代码
│   ├── 📄 App.tsx                # 主应用组件
│   ├── 📄 main.tsx               # 应用入口
│   ├── 📄 index.css              # 全局样式
│   └── 📄 vite-env.d.ts          # Vite类型定义
│
├── 📁 docs/                       # 项目文档
│   ├── 📄 README.md              # 文档导航索引
│   └── 📁 python-framework/       # Python框架详细文档
│       ├── 📄 START_HERE.md      # 从这里开始
│       ├── 📄 QUICKSTART.md      # 快速入门
│       ├── 📄 TOOL_QUICKSTART.md # 工具快速入门
│       ├── 📄 TOOL_MANAGEMENT_GUIDE.md
│       ├── 📄 DEMO_GUIDE.md
│       ├── 📄 PROJECT_STRUCTURE.md
│       ├── 📄 PYTHON_FRAMEWORK_SUMMARY.md
│       ├── 📄 IMPLEMENTATION_COMPLETE.md
│       └── 📄 UPDATE_SUMMARY.md
│
├── 📁 outputs/                    # 程序输出文件目录
│
├── 📁 dist/                       # 前端构建输出（自动生成）
│
├── 📄 package.json                # Node.js项目配置
├── 📄 package-lock.json           # 依赖锁定文件
│
├── 📄 vite.config.ts              # Vite构建配置
├── 📄 tsconfig.json               # TypeScript配置
├── 📄 tsconfig.app.json           # 应用TypeScript配置
├── 📄 tsconfig.node.json          # Node环境TypeScript配置
│
├── 📄 tailwind.config.js          # Tailwind CSS配置
├── 📄 postcss.config.js           # PostCSS配置
├── 📄 eslint.config.js            # ESLint配置
│
├── 📄 index.html                  # HTML入口文件
├── 📄 .gitignore                  # Git忽略文件
├── 📄 LICENSE                     # 许可证
└── 📄 README.md                   # 项目主说明文档
```

## 🎯 各目录说明

### 后端部分 (Python)

#### `python-agent-framework/core/`
核心框架组件，包含：
- `agent.py` - 智能体基类实现
- `tool.py` - 工具系统基类
- `llm_client.py` - LLM API客户端
- `orchestrator.py` - 多智能体协作编排器

#### `python-agent-framework/tools/`
预定义的工具集：
- `base_tools.py` - 基础工具（计算器、搜索等）
- `research_tools.py` - 科研专用工具
- `data_tools.py` - 数据分析工具

#### `python-agent-framework/gui/`
Streamlit图形界面：
- `app.py` - 主应用界面

#### `python-agent-framework/examples/`
使用示例：
- `basic_usage.py` - 基础用法
- `custom_tool_template.py` - 自定义工具模板
- `orchestration_examples.py` - 多智能体协作示例
- `research_workflow.py` - 科研工作流

#### `python-agent-framework/utils/`
辅助工具：
- `dynamic_tool.py` - 动态工具加载
- `storage.py` - 数据存储
- `tool_storage.py` - 工具配置存储

#### `python-agent-framework/tools_data/`
工具配置数据：
- `custom_tools.json` - 自定义工具定义
- `example_tools.json` - 示例工具

### 前端部分 (React + Vite)

#### `src/`
React应用源代码：
- `App.tsx` - 主应用组件
- `main.tsx` - 应用入口点
- `index.css` - 全局样式定义

#### 配置文件
- `vite.config.ts` - Vite开发和构建配置
- `tsconfig.*.json` - TypeScript编译配置
- `tailwind.config.js` - Tailwind CSS样式框架配置
- `eslint.config.js` - 代码质量检查配置

### 文档部分

#### `docs/`
集中的文档目录：
- `README.md` - 文档导航
- `python-framework/` - Python框架的详细文档

### 输出和构建

#### `outputs/`
程序运行时的输出文件存储位置

#### `dist/`
前端构建后的生产文件（通过 `npm run build` 生成）

## 🔄 工作流程

### 开发Python智能体
1. 在 `python-agent-framework/` 中开发
2. 查看 `docs/python-framework/` 中的文档
3. 参考 `examples/` 中的示例
4. 通过 `gui/app.py` 测试

### 开发前端界面
1. 在 `src/` 中编写React组件
2. 使用 `npm run dev` 启动开发服务器
3. 使用 `npm run build` 构建生产版本

## 📝 命名规范

- **Python文件**: 小写+下划线 (snake_case)
  - 例：`my_tool.py`, `data_processor.py`

- **TypeScript/React文件**: 大驼峰 (PascalCase) for 组件
  - 例：`MyComponent.tsx`, `UserProfile.tsx`

- **配置文件**: 小写+点号分隔
  - 例：`vite.config.ts`, `tailwind.config.js`

## 🚫 应忽略的文件/目录

以下目录在 `.gitignore` 中已配置忽略：
- `__pycache__/` - Python缓存
- `node_modules/` - Node.js依赖
- `dist/` - 构建输出
- `outputs/` - 程序输出
- `.env` - 环境变量（包含密钥）
- `*.pyc` - Python编译文件

## 💡 最佳实践

1. **模块化**: 保持每个文件职责单一
2. **文档**: 为重要功能编写文档
3. **示例**: 在 `examples/` 中提供使用示例
4. **测试**: 添加必要的测试文件
5. **版本控制**: 不提交敏感信息和构建产物

## 🔗 相关文档

- [主README](../README.md)
- [Python框架文档](../docs/python-framework/)
- [快速开始指南](../docs/python-framework/QUICKSTART.md)
