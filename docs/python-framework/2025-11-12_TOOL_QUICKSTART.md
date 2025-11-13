# Quick Start: Tool Management | 工具管理快速开始

## 启动应用 | Start Application

```bash
# 1. 激活环境
conda activate py310

# 2. 进入项目目录
cd /Users/acquent/Desktop/Project\ Process/Demos/project_agents/python-agent-framework

# 3. 启动 Streamlit 应用
streamlit run gui/app.py
```

## 创建第一个工具 | Create Your First Tool

### 方法 1: 使用 GUI (推荐)

1. 打开浏览器访问 http://localhost:8501
2. 在侧边栏选择 "Tool Management | 工具管理"
3. 点击 "Create Tool | 创建工具" 标签
4. 填写表单:
   - **工具名称**: 例如 "WeatherChecker"
   - **工具描述**: "检查指定城市的天气"
   - **参数名称**: "city"
   - **参数类型**: "string"
   - ✓ 勾选 "Required"
   - **Python代码**:
     ```python
     # 示例代码
     result = f"{city}的天气: 晴天, 25°C"
     ```
5. 点击 "Save Tool | 保存工具"

### 方法 2: 直接编辑 JSON

编辑文件: `tools_data/custom_tools.json`

```json
{
  "tools": [
    {
      "name": "WeatherChecker",
      "description": "检查指定城市的天气",
      "parameters": {
        "type": "object",
        "properties": {
          "city": {
            "type": "string",
            "description": "城市名称"
          }
        },
        "required": ["city"]
      },
      "code": "result = f'{city}的天气: 晴天, 25°C'"
    }
  ]
}
```

## 使用自定义工具 | Use Custom Tools

1. 在侧边栏选择 "Create Agent | 创建智能体"
2. 在 "Select Tools" 下拉菜单中，你会看到你的工具显示为 "Custom: WeatherChecker"
3. 选择你需要的工具
4. 创建智能体
5. 在 "Chat | 对话" 页面与智能体交互

## 管理工具 | Manage Tools

### 查看所有工具 | View All Tools
- 导航到 "Tool Management" → "View Tools" 标签
- 查看所有保存的工具及其详细信息

### 编辑工具 | Edit Tools
- 导航到 "Tool Management" → "Edit Tool" 标签
- 选择要编辑的工具
- 修改并保存

### 删除工具 | Delete Tools
- 导航到 "Tool Management" → "Delete Tool" 标签
- 选择要删除的工具
- 确认删除

### 导出/导入 | Export/Import
- 在 "View Tools" 标签中
- 点击 "Export All Tools" 导出所有工具
- 使用文件上传器导入工具

## 工具代码编写指南 | Tool Code Writing Guide

### 基本规则

1. **使用 `result` 变量存储输出**
   ```python
   result = "你的结果"
   ```

2. **访问参数**
   参数名称会自动成为变量，直接使用即可
   ```python
   # 如果参数名是 'location'
   result = f"位置: {location}"
   ```

3. **处理多个参数**
   ```python
   # 参数: city (string), days (integer)
   result = f"{city}未来{days}天的天气预报"
   ```

### 示例工具

#### 示例 1: 简单计算器
```python
# 参数: num1 (number), num2 (number), operation (string)
if operation == "add":
    result = num1 + num2
elif operation == "subtract":
    result = num1 - num2
elif operation == "multiply":
    result = num1 * num2
elif operation == "divide":
    result = num1 / num2 if num2 != 0 else "Error: Division by zero"
```

#### 示例 2: 文本处理
```python
# 参数: text (string), action (string)
if action == "uppercase":
    result = text.upper()
elif action == "lowercase":
    result = text.lower()
elif action == "reverse":
    result = text[::-1]
elif action == "length":
    result = len(text)
```

#### 示例 3: 数据分析
```python
# 参数: numbers (array)
import statistics

result = {
    "mean": statistics.mean(numbers),
    "median": statistics.median(numbers),
    "min": min(numbers),
    "max": max(numbers)
}
```

## 故障排除 | Troubleshooting

### 工具不显示?
```bash
# 1. 检查文件是否存在
ls tools_data/custom_tools.json

# 2. 验证 JSON 格式
python -m json.tool tools_data/custom_tools.json

# 3. 重启应用
# Ctrl+C 停止，然后重新运行
streamlit run gui/app.py
```

### 代码执行错误?
- 确保使用了 `result` 变量
- 检查参数名称是否匹配
- 添加错误处理:
  ```python
  try:
      result = your_code_here
  except Exception as e:
      result = f"Error: {str(e)}"
  ```

### 清除所有数据重新开始
```bash
# 删除自定义工具文件
rm tools_data/custom_tools.json

# 重启应用会自动创建新文件
streamlit run gui/app.py
```

## 最佳实践 | Best Practices

1. **工具命名**: 使用清晰的、描述性的名称
2. **参数设计**: 只包含必要的参数
3. **错误处理**: 在代码中添加 try-except
4. **文档**: 写清楚的描述
5. **测试**: 创建后立即测试工具
6. **备份**: 定期导出工具作为备份

## 下一步 | Next Steps

1. ✅ 创建你的第一个工具
2. ✅ 在智能体中使用它
3. ✅ 探索更复杂的工具实现
4. ✅ 与团队分享你的工具 (export/import)
5. ✅ 查看 TOOL_MANAGEMENT_GUIDE.md 了解更多详情

---

**需要帮助?** 查看完整文档: `TOOL_MANAGEMENT_GUIDE.md`
