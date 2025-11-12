"""
Tool Base Class / 工具基类

This module defines the base Tool class that all tools must inherit from.
此模块定义了所有工具必须继承的基础Tool类。

Author: LLM Agent Framework
License: MIT
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import json


class Tool(ABC):
    """
    Base class for all tools in the framework.
    框架中所有工具的基类。

    All custom tools must inherit from this class and implement the execute method.
    所有自定义工具必须继承此类并实现execute方法。

    Attributes:
        name (str): Unique identifier for the tool / 工具的唯一标识符
        description (str): Description of what the tool does / 工具功能描述
        parameters (Dict): Parameter schema for the tool / 工具的参数模式
    """

    def __init__(
        self,
        name: str,
        description: str,
        parameters: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize the Tool.
        初始化工具。

        Args:
            name: Tool name / 工具名称
            description: Tool description / 工具描述
            parameters: Parameter schema (optional) / 参数模式（可选）
        """
        self.name = name
        self.description = description
        self.parameters = parameters or {}

    @abstractmethod
    def execute(self, **kwargs) -> Dict[str, Any]:
        """
        Execute the tool's main functionality.
        执行工具的主要功能。

        This method must be implemented by all subclasses.
        所有子类必须实现此方法。

        Args:
            **kwargs: Tool-specific parameters / 工具特定的参数

        Returns:
            Dict containing the result / 包含结果的字典

        Raises:
            NotImplementedError: If not implemented by subclass / 如果子类未实现
        """
        raise NotImplementedError("Subclasses must implement execute method")

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert tool to dictionary format for LLM function calling.
        将工具转换为LLM函数调用的字典格式。

        Returns:
            Dict representation of the tool / 工具的字典表示
        """
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.parameters
        }

    def validate_parameters(self, **kwargs) -> bool:
        """
        Validate provided parameters against the schema.
        根据模式验证提供的参数。

        Args:
            **kwargs: Parameters to validate / 要验证的参数

        Returns:
            True if valid, False otherwise / 如果有效则为True，否则为False
        """
        if not self.parameters:
            return True

        required = self.parameters.get("required", [])
        properties = self.parameters.get("properties", {})

        for param in required:
            if param not in kwargs:
                return False

        for key, value in kwargs.items():
            if key in properties:
                expected_type = properties[key].get("type")
                if expected_type and not self._check_type(value, expected_type):
                    return False

        return True

    def _check_type(self, value: Any, expected_type: str) -> bool:
        """
        Check if value matches expected type.
        检查值是否匹配预期类型。

        Args:
            value: Value to check / 要检查的值
            expected_type: Expected type string / 预期类型字符串

        Returns:
            True if types match / 如果类型匹配则为True
        """
        type_mapping = {
            "string": str,
            "number": (int, float),
            "integer": int,
            "boolean": bool,
            "array": list,
            "object": dict
        }

        expected = type_mapping.get(expected_type)
        if expected:
            return isinstance(value, expected)
        return True

    def __repr__(self) -> str:
        """String representation of the tool."""
        return f"Tool(name='{self.name}', description='{self.description}')"

    def __str__(self) -> str:
        """User-friendly string representation."""
        return f"{self.name}: {self.description}"


class ToolRegistry:
    """
    Registry for managing available tools.
    用于管理可用工具的注册表。

    This class maintains a collection of tools and provides methods to
    register, retrieve, and list tools.
    此类维护工具集合，并提供注册、检索和列出工具的方法。
    """

    def __init__(self):
        """Initialize the tool registry. / 初始化工具注册表。"""
        self._tools: Dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        """
        Register a tool in the registry.
        在注册表中注册工具。

        Args:
            tool: Tool instance to register / 要注册的工具实例

        Raises:
            ValueError: If tool name already exists / 如果工具名称已存在
        """
        if tool.name in self._tools:
            raise ValueError(f"Tool '{tool.name}' already registered")
        self._tools[tool.name] = tool

    def get(self, name: str) -> Optional[Tool]:
        """
        Get a tool by name.
        按名称获取工具。

        Args:
            name: Tool name / 工具名称

        Returns:
            Tool instance or None / 工具实例或None
        """
        return self._tools.get(name)

    def list_tools(self) -> list[str]:
        """
        List all registered tool names.
        列出所有已注册的工具名称。

        Returns:
            List of tool names / 工具名称列表
        """
        return list(self._tools.keys())

    def get_all(self) -> Dict[str, Tool]:
        """
        Get all registered tools.
        获取所有已注册的工具。

        Returns:
            Dictionary of all tools / 所有工具的字典
        """
        return self._tools.copy()

    def unregister(self, name: str) -> bool:
        """
        Unregister a tool.
        取消注册工具。

        Args:
            name: Tool name / 工具名称

        Returns:
            True if removed, False if not found / 如果已移除则为True，如果未找到则为False
        """
        if name in self._tools:
            del self._tools[name]
            return True
        return False

    def clear(self) -> None:
        """
        Clear all registered tools.
        清除所有已注册的工具。
        """
        self._tools.clear()

    def __len__(self) -> int:
        """Return number of registered tools."""
        return len(self._tools)

    def __contains__(self, name: str) -> bool:
        """Check if tool is registered."""
        return name in self._tools
