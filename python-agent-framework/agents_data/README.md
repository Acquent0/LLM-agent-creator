# Agents Data / 智能体数据

This directory stores agent configurations created through the GUI.
此目录存储通过GUI创建的智能体配置。

## File Structure / 文件结构

- `agents.json` - All agent configurations / 所有智能体配置

## Agent Configuration Format / 智能体配置格式

```json
{
  "agents": [
    {
      "name": "DataAnalyst",
      "tools": ["Calculator", "Data Analysis", "Visualization"],
      "system_prompt": "You are a professional data analyst...",
      "created_at": "2025-11-13T14:30:00",
      "updated_at": "2025-11-13T14:30:00"
    }
  ]
}
```

## Usage / 使用

Agents are automatically saved when created through the GUI and can be loaded on startup.
通过GUI创建的智能体会自动保存，启动时可以加载。
