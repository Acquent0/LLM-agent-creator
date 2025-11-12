"""
Dynamic Tool Loader / 动态工具加载器

Dynamically creates Tool instances from saved configurations.
从保存的配置动态创建Tool实例。

Author: LLM Agent Framework
License: MIT
"""

from typing import Dict, Any, Optional
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.tool import Tool


class DynamicTool(Tool):
    """
    A tool created dynamically from configuration.
    从配置动态创建的工具。
    """

    def __init__(
        self,
        name: str,
        description: str,
        parameters: Optional[Dict[str, Any]] = None,
        code: Optional[str] = None
    ):
        """
        Initialize dynamic tool.
        初始化动态工具。

        Args:
            name: Tool name / 工具名称
            description: Tool description / 工具描述
            parameters: Parameter schema / 参数模式
            code: Python code to execute (optional) / 要执行的Python代码（可选）
        """
        super().__init__(name, description, parameters)
        self.code = code

    def execute(self, **kwargs) -> Dict[str, Any]:
        """
        Execute the tool with provided parameters.
        使用提供的参数执行工具。

        Args:
            **kwargs: Tool parameters / 工具参数

        Returns:
            Execution result / 执行结果
        """
        try:
            # Validate parameters
            if not self.validate_parameters(**kwargs):
                return {
                    "success": False,
                    "error": "Invalid parameters",
                    "result": None
                }

            # If custom code is provided, execute it
            if self.code:
                # Create a safe execution environment
                local_vars = kwargs.copy()
                exec(self.code, {"__builtins__": __builtins__}, local_vars)
                
                # Return the 'result' variable if it exists
                if 'result' in local_vars:
                    return {
                        "success": True,
                        "result": local_vars['result'],
                        "error": None
                    }
                else:
                    return {
                        "success": True,
                        "result": "Code executed successfully",
                        "error": None
                    }
            else:
                # Default behavior: just return the parameters
                return {
                    "success": True,
                    "result": kwargs,
                    "error": None
                }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "result": None
            }


def load_tool_from_config(tool_config: Dict[str, Any]) -> Optional[DynamicTool]:
    """
    Load a tool from configuration dictionary.
    从配置字典加载工具。

    Args:
        tool_config: Tool configuration / 工具配置

    Returns:
        DynamicTool instance or None / DynamicTool实例或None
    """
    try:
        return DynamicTool(
            name=tool_config.get("name"),
            description=tool_config.get("description"),
            parameters=tool_config.get("parameters", {}),
            code=tool_config.get("code")
        )
    except Exception as e:
        print(f"Error loading tool: {e}")
        return None
