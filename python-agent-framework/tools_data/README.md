# Tools Data Directory | 工具数据目录

This directory stores custom tool configurations created through the GUI.
此目录存储通过GUI创建的自定义工具配置。

## Files | 文件

- `custom_tools.json`: Main storage file for all custom tools | 所有自定义工具的主存储文件
- `*_export.json`: Exported tool configurations | 导出的工具配置

## Structure | 结构

Each tool is stored with the following structure:
每个工具都以以下结构存储：

```json
{
  "tools": [
    {
      "name": "ToolName",
      "description": "Tool description",
      "parameters": {
        "type": "object",
        "properties": {
          "param1": {
            "type": "string",
            "description": "Parameter description"
          }
        },
        "required": ["param1"]
      },
      "code": "Python code implementation (optional)"
    }
  ]
}
```

## Features | 功能

- **Create**: Add new custom tools | 添加新的自定义工具
- **Read**: View all saved tools | 查看所有保存的工具
- **Update**: Edit existing tools | 编辑现有工具
- **Delete**: Remove tools | 删除工具
- **Export/Import**: Share tools between systems | 在系统之间共享工具

## Usage | 使用

1. Navigate to "Tool Management" in the GUI | 在GUI中导航到"工具管理"
2. Create tools using the interface | 使用界面创建工具
3. Tools are automatically saved to `custom_tools.json` | 工具自动保存到 `custom_tools.json`
4. Custom tools will be available in agent creation | 自定义工具将在创建代理时可用

## Note | 注意

- Do not manually edit `custom_tools.json` unless you know what you're doing
- 除非你知道自己在做什么，否则不要手动编辑 `custom_tools.json`
- Always backup your tools before major changes
- 在进行重大更改之前，请始终备份您的工具
