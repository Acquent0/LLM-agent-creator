# Tool Management Update | 工具管理更新

## New Features Added | 新增功能

### 1. Persistent Tool Storage | 持久化工具存储

All custom tools are now automatically saved to the `tools_data/` directory and will be available after restarting the application.

所有自定义工具现在会自动保存到 `tools_data/` 目录，应用重启后仍然可用。

**Storage Location | 存储位置:**
- `python-agent-framework/tools_data/custom_tools.json`

### 2. Tool Management Interface | 工具管理界面

A complete CRUD interface for custom tools has been added to the GUI:

GUI中添加了完整的自定义工具增删改查界面:

#### Features | 功能:

✅ **Create Tool | 创建工具**
- Define tool name and description | 定义工具名称和描述
- Configure parameters and types | 配置参数和类型
- Write custom Python code implementation | 编写自定义Python代码实现
- Automatic validation | 自动验证

✅ **View Tools | 查看工具**
- List all custom tools | 列出所有自定义工具
- View tool details and parameters | 查看工具详情和参数
- Export individual or all tools | 导出单个或所有工具

✅ **Edit Tool | 编辑工具**
- Modify existing tool configurations | 修改现有工具配置
- Update name, description, or code | 更新名称、描述或代码
- Automatic saving | 自动保存

✅ **Delete Tool | 删除工具**
- Remove individual tools | 删除单个工具
- Bulk delete all tools | 批量删除所有工具
- Safety confirmations | 安全确认

### 3. Import/Export Functionality | 导入/导出功能

Share tools between systems or create backups:

在系统之间共享工具或创建备份:

- Export all tools to JSON file | 导出所有工具到JSON文件
- Import tools from JSON file | 从JSON文件导入工具
- Merge or replace existing tools | 合并或替换现有工具

### 4. Dynamic Tool Loading | 动态工具加载

Custom tools are automatically loaded when:

自定义工具会在以下情况自动加载:

- Application starts | 应用启动时
- Creating new agents | 创建新代理时
- Tool list is refreshed | 工具列表刷新时

### How to Use | 使用方法

#### 1. Access Tool Management | 访问工具管理

```
1. Start the Streamlit app: streamlit run gui/app.py
2. In the sidebar, select "Tool Management | 工具管理"
```

#### 2. Create a Custom Tool | 创建自定义工具

**Example: Weather Tool**

```
Name: WeatherAPI
Description: Get current weather for a location
Parameter: location (string, required)
Code:
# This is example code - in production, call a real API
result = f"Weather for {location}: Sunny, 25°C"
```

#### 3. Use Custom Tools in Agents | 在代理中使用自定义工具

When creating an agent, your custom tools will appear with "Custom:" prefix in the tool selection dropdown.

创建代理时，自定义工具会在工具选择下拉菜单中以"Custom:"前缀显示。

### File Structure | 文件结构

```
python-agent-framework/
├── tools_data/                    # NEW: Tool storage directory
│   ├── custom_tools.json         # Main storage file
│   ├── example_tools.json        # Example tools
│   └── README.md                 # Documentation
├── utils/
│   ├── tool_storage.py           # NEW: Storage manager
│   └── dynamic_tool.py           # NEW: Dynamic tool loader
└── gui/
    └── app.py                    # UPDATED: Added tool management UI
```

### API Reference | API参考

#### ToolStorageManager

```python
from utils.tool_storage import ToolStorageManager

# Initialize
storage = ToolStorageManager()

# Save a tool
tool_config = {
    "name": "MyTool",
    "description": "My custom tool",
    "parameters": {...},
    "code": "result = 'Hello'"
}
storage.save_tool(tool_config)

# Load all tools
tools = storage.load_all_tools()

# Get specific tool
tool = storage.get_tool("MyTool")

# Update tool
storage.update_tool("MyTool", {"description": "Updated description"})

# Delete tool
storage.delete_tool("MyTool")

# Export/Import
storage.export_tools("backup.json")
storage.import_tools("backup.json", merge=True)
```

#### DynamicTool

```python
from utils.dynamic_tool import DynamicTool, load_tool_from_config

# Create from config
tool_config = {...}
tool = load_tool_from_config(tool_config)

# Use in agent
agent = Agent(
    name="MyAgent",
    llm_client=llm_client,
    tools=[tool]
)
```

### Benefits | 优势

1. **Persistence | 持久性**: Tools survive application restarts
2. **Reusability | 可重用性**: Share tools across projects
3. **Version Control | 版本控制**: JSON format works with Git
4. **Safety | 安全性**: Built-in validation and error handling
5. **Flexibility | 灵活性**: Easy to extend with custom code

### Migration Guide | 迁移指南

If you have existing tools in code, you can migrate them to the storage system:

如果你在代码中有现有工具，可以将它们迁移到存储系统:

```python
# Old way (temporary)
class MyCustomTool(Tool):
    def execute(self, **kwargs):
        ...

# New way (persistent)
# Use the GUI to create the tool, or:
from utils.tool_storage import ToolStorageManager

storage = ToolStorageManager()
storage.save_tool({
    "name": "MyCustomTool",
    "description": "...",
    "parameters": {...},
    "code": "..."  # Your execute logic
})
```

### Troubleshooting | 故障排除

**Tools not appearing?**
- Check `tools_data/custom_tools.json` exists
- Verify JSON syntax is valid
- Restart the Streamlit app

**Code execution errors?**
- Ensure your code uses the `result` variable
- Check parameter names match your code
- Add error handling in custom code

### Future Enhancements | 未来增强

- [ ] Tool templates library
- [ ] Code syntax highlighting in GUI
- [ ] Tool testing interface
- [ ] Tool versioning
- [ ] Collaborative tool sharing platform

---

**Version**: 1.1.0  
**Last Updated**: 2025-11-12
