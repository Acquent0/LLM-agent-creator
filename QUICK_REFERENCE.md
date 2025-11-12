# 快速参考 / Quick Reference

## 🚀 常用命令

### Python 框架

```bash
# 进入框架目录
cd python-agent-framework

# 安装依赖
pip install -r requirements.txt

# 启动 GUI
streamlit run gui/app.py

# 运行示例
python examples/basic_usage.py
```

### 前端开发

```bash
# 安装依赖
npm install

# 开发模式
npm run dev

# 类型检查
npm run typecheck

# 代码检查
npm run lint

# 构建生产版本
npm run build

# 预览构建结果
npm run preview
```

## 📁 重要目录

| 目录 | 说明 |
|------|------|
| `python-agent-framework/core/` | 核心框架代码 |
| `python-agent-framework/tools/` | 内置工具 |
| `python-agent-framework/examples/` | 使用示例 |
| `src/` | React 前端源码 |
| `docs/` | 项目文档 |
| `outputs/` | 程序输出 |

## 📖 重要文档

| 文档 | 路径 |
|------|------|
| 项目总览 | [README.md](./README.md) |
| 项目结构 | [PROJECT_STRUCTURE.md](./PROJECT_STRUCTURE.md) |
| 文档导航 | [docs/README.md](./docs/README.md) |
| Python框架 | [python-agent-framework/README.md](./python-agent-framework/README.md) |
| 快速开始 | [docs/python-framework/QUICKSTART.md](./docs/python-framework/QUICKSTART.md) |
| 整理总结 | [REORGANIZATION_SUMMARY.md](./REORGANIZATION_SUMMARY.md) |

## 🔧 配置文件

| 文件 | 用途 |
|------|------|
| `.env` | 环境变量（API密钥等）|
| `package.json` | Node.js 依赖和脚本 |
| `requirements.txt` | Python 依赖 |
| `vite.config.ts` | Vite 配置 |
| `tailwind.config.js` | Tailwind CSS 配置 |
| `tsconfig.json` | TypeScript 配置 |

## 💡 快速提示

### 创建新的工具

1. 查看 `python-agent-framework/examples/custom_tool_template.py`
2. 阅读 [TOOL_QUICKSTART.md](./docs/python-framework/TOOL_QUICKSTART.md)

### 查找功能

1. 使用 VS Code 全局搜索 (Cmd/Ctrl + Shift + F)
2. 查看 `examples/` 目录中的示例

### 调试

**Python**:
```python
# 在代码中添加
import pdb; pdb.set_trace()
```

**Frontend**:
```typescript
// 在代码中添加
console.log('Debug:', variable);
```

## 🆘 常见问题

### Python 模块导入错误
```bash
# 确保在正确的目录
cd python-agent-framework

# 或使用绝对导入
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

### 前端端口已被占用
```bash
# 修改端口
npm run dev -- --port 3001
```

### API 密钥配置
```bash
# 复制示例配置
cp .env.example .env

# 编辑 .env 文件
# 添加你的 API 密钥
```

## 🔗 相关链接

- [Streamlit 文档](https://docs.streamlit.io/)
- [Vite 文档](https://vitejs.dev/)
- [React 文档](https://react.dev/)
- [Tailwind CSS 文档](https://tailwindcss.com/)

---

💡 **提示**: 收藏此文件以便快速查找常用信息！
