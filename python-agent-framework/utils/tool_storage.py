"""
Tool Storage Manager / 工具存储管理器

Manages persistent storage of custom tools.
管理自定义工具的持久化存储。

Author: LLM Agent Framework
License: MIT
"""

import os
import json
from typing import Dict, Any, List, Optional
from pathlib import Path


class ToolStorageManager:
    """
    Manager for saving and loading custom tools.
    用于保存和加载自定义工具的管理器。
    """

    def __init__(self, storage_dir: str = None):
        """
        Initialize tool storage manager.
        初始化工具存储管理器。

        Args:
            storage_dir: Directory to store tool configurations / 存储工具配置的目录
        """
        if storage_dir is None:
            # Default to tools_data folder in project root
            project_root = Path(__file__).parent.parent
            storage_dir = os.path.join(project_root, "tools_data")
        
        self.storage_dir = storage_dir
        self.tools_file = os.path.join(storage_dir, "custom_tools.json")
        
        # Create storage directory if it doesn't exist
        os.makedirs(storage_dir, exist_ok=True)
        
        # Initialize tools file if it doesn't exist
        if not os.path.exists(self.tools_file):
            self._init_tools_file()

    def _init_tools_file(self):
        """Initialize empty tools file. / 初始化空工具文件。"""
        with open(self.tools_file, 'w', encoding='utf-8') as f:
            json.dump({"tools": []}, f, indent=2, ensure_ascii=False)

    def save_tool(self, tool_config: Dict[str, Any]) -> bool:
        """
        Save a tool configuration.
        保存工具配置。

        Args:
            tool_config: Tool configuration dictionary / 工具配置字典
                {
                    "name": str,
                    "description": str,
                    "parameters": dict,
                    "code": str (optional - for custom Python code)
                }

        Returns:
            Success status / 成功状态
        """
        try:
            tools_data = self.load_all_tools()
            
            # Check if tool with same name already exists
            existing_index = None
            for i, tool in enumerate(tools_data):
                if tool.get("name") == tool_config.get("name"):
                    existing_index = i
                    break
            
            # Update existing or add new
            if existing_index is not None:
                tools_data[existing_index] = tool_config
            else:
                tools_data.append(tool_config)
            
            # Save to file
            with open(self.tools_file, 'w', encoding='utf-8') as f:
                json.dump({"tools": tools_data}, f, indent=2, ensure_ascii=False)
            
            return True
        
        except Exception as e:
            print(f"Error saving tool: {e}")
            return False

    def load_all_tools(self) -> List[Dict[str, Any]]:
        """
        Load all saved tools.
        加载所有保存的工具。

        Returns:
            List of tool configurations / 工具配置列表
        """
        try:
            if not os.path.exists(self.tools_file):
                return []
            
            with open(self.tools_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get("tools", [])
        
        except Exception as e:
            print(f"Error loading tools: {e}")
            return []

    def get_tool(self, tool_name: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific tool by name.
        根据名称获取特定工具。

        Args:
            tool_name: Name of the tool / 工具名称

        Returns:
            Tool configuration or None / 工具配置或None
        """
        tools = self.load_all_tools()
        for tool in tools:
            if tool.get("name") == tool_name:
                return tool
        return None

    def delete_tool(self, tool_name: str) -> bool:
        """
        Delete a tool by name.
        根据名称删除工具。

        Args:
            tool_name: Name of the tool to delete / 要删除的工具名称

        Returns:
            Success status / 成功状态
        """
        try:
            tools_data = self.load_all_tools()
            original_length = len(tools_data)
            
            # Filter out the tool to delete
            tools_data = [tool for tool in tools_data if tool.get("name") != tool_name]
            
            if len(tools_data) == original_length:
                # Tool not found
                return False
            
            # Save updated list
            with open(self.tools_file, 'w', encoding='utf-8') as f:
                json.dump({"tools": tools_data}, f, indent=2, ensure_ascii=False)
            
            return True
        
        except Exception as e:
            print(f"Error deleting tool: {e}")
            return False

    def update_tool(self, tool_name: str, updates: Dict[str, Any]) -> bool:
        """
        Update a tool's configuration.
        更新工具配置。

        Args:
            tool_name: Name of the tool to update / 要更新的工具名称
            updates: Dictionary of fields to update / 要更新的字段字典

        Returns:
            Success status / 成功状态
        """
        try:
            tools_data = self.load_all_tools()
            
            # Find and update the tool
            for tool in tools_data:
                if tool.get("name") == tool_name:
                    tool.update(updates)
                    
                    # Save updated list
                    with open(self.tools_file, 'w', encoding='utf-8') as f:
                        json.dump({"tools": tools_data}, f, indent=2, ensure_ascii=False)
                    
                    return True
            
            return False  # Tool not found
        
        except Exception as e:
            print(f"Error updating tool: {e}")
            return False

    def export_tools(self, export_path: str) -> bool:
        """
        Export all tools to a file.
        导出所有工具到文件。

        Args:
            export_path: Path to export file / 导出文件路径

        Returns:
            Success status / 成功状态
        """
        try:
            tools_data = self.load_all_tools()
            
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump({"tools": tools_data}, f, indent=2, ensure_ascii=False)
            
            return True
        
        except Exception as e:
            print(f"Error exporting tools: {e}")
            return False

    def import_tools(self, import_path: str, merge: bool = True) -> bool:
        """
        Import tools from a file.
        从文件导入工具。

        Args:
            import_path: Path to import file / 导入文件路径
            merge: If True, merge with existing tools; if False, replace / 
                   如果为True，与现有工具合并；如果为False，替换

        Returns:
            Success status / 成功状态
        """
        try:
            with open(import_path, 'r', encoding='utf-8') as f:
                import_data = json.load(f)
            
            imported_tools = import_data.get("tools", [])
            
            if merge:
                existing_tools = self.load_all_tools()
                
                # Merge tools (imported tools overwrite existing ones with same name)
                tool_dict = {tool["name"]: tool for tool in existing_tools}
                for tool in imported_tools:
                    tool_dict[tool["name"]] = tool
                
                merged_tools = list(tool_dict.values())
                
                with open(self.tools_file, 'w', encoding='utf-8') as f:
                    json.dump({"tools": merged_tools}, f, indent=2, ensure_ascii=False)
            else:
                # Replace all tools
                with open(self.tools_file, 'w', encoding='utf-8') as f:
                    json.dump({"tools": imported_tools}, f, indent=2, ensure_ascii=False)
            
            return True
        
        except Exception as e:
            print(f"Error importing tools: {e}")
            return False

    def clear_all_tools(self) -> bool:
        """
        Clear all saved tools.
        清除所有保存的工具。

        Returns:
            Success status / 成功状态
        """
        try:
            self._init_tools_file()
            return True
        except Exception as e:
            print(f"Error clearing tools: {e}")
            return False

    def get_tool_count(self) -> int:
        """
        Get the number of saved tools.
        获取保存的工具数量。

        Returns:
            Number of tools / 工具数量
        """
        return len(self.load_all_tools())
