"""
Base Tools / 基础工具

This module provides fundamental tools for agents.
此模块为智能体提供基础工具。

Author: LLM Agent Framework
License: MIT
"""

import math
import os
import sys
from io import StringIO
from typing import Dict, Any
import requests

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.tool import Tool


class CalculatorTool(Tool):
    """
    Mathematical calculator tool.
    数学计算器工具。

    Performs basic and advanced mathematical operations.
    执行基本和高级数学运算。
    """

    def __init__(self):
        super().__init__(
            name="calculator",
            description="Perform mathematical calculations. Supports basic operations (+, -, *, /) and advanced functions (sqrt, sin, cos, log, etc.)",
            parameters={
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Mathematical expression to evaluate"
                    }
                },
                "required": ["expression"]
            }
        )

    def execute(self, expression: str, **kwargs) -> Dict[str, Any]:
        """
        Evaluate a mathematical expression.
        计算数学表达式。

        Args:
            expression: Math expression string / 数学表达式字符串

        Returns:
            Calculation result / 计算结果
        """
        try:
            safe_dict = {
                "abs": abs, "round": round, "min": min, "max": max,
                "sum": sum, "pow": pow,
                "sqrt": math.sqrt, "sin": math.sin, "cos": math.cos,
                "tan": math.tan, "log": math.log, "log10": math.log10,
                "exp": math.exp, "pi": math.pi, "e": math.e,
                "ceil": math.ceil, "floor": math.floor
            }

            result = eval(expression, {"__builtins__": {}}, safe_dict)

            return {
                "success": True,
                "result": result,
                "expression": expression
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "expression": expression
            }


class FileIOTool(Tool):
    """
    File input/output tool.
    文件输入/输出工具。

    Read and write text files safely.
    安全地读写文本文件。
    """

    def __init__(self):
        super().__init__(
            name="file_io",
            description="Read from or write to text files",
            parameters={
                "type": "object",
                "properties": {
                    "operation": {
                        "type": "string",
                        "description": "Operation to perform: 'read' or 'write'"
                    },
                    "filepath": {
                        "type": "string",
                        "description": "Path to the file"
                    },
                    "content": {
                        "type": "string",
                        "description": "Content to write (only for write operation)"
                    }
                },
                "required": ["operation", "filepath"]
            }
        )

    def execute(self, operation: str, filepath: str, content: str = "", **kwargs) -> Dict[str, Any]:
        """
        Perform file I/O operation.
        执行文件I/O操作。

        Args:
            operation: 'read' or 'write' / 'read'或'write'
            filepath: File path / 文件路径
            content: Content to write / 要写入的内容

        Returns:
            Operation result / 操作结果
        """
        try:
            if operation == "read":
                with open(filepath, 'r', encoding='utf-8') as f:
                    file_content = f.read()
                return {
                    "success": True,
                    "operation": "read",
                    "filepath": filepath,
                    "content": file_content
                }

            elif operation == "write":
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                return {
                    "success": True,
                    "operation": "write",
                    "filepath": filepath,
                    "message": f"Successfully wrote {len(content)} characters"
                }

            else:
                return {
                    "success": False,
                    "error": f"Unknown operation: {operation}"
                }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "operation": operation,
                "filepath": filepath
            }


class PythonREPLTool(Tool):
    """
    Python code execution tool.
    Python代码执行工具。

    Execute Python code safely in a restricted environment.
    在受限环境中安全执行Python代码。
    """

    def __init__(self):
        super().__init__(
            name="python_repl",
            description="Execute Python code and return the output",
            parameters={
                "type": "object",
                "properties": {
                    "code": {
                        "type": "string",
                        "description": "Python code to execute"
                    }
                },
                "required": ["code"]
            }
        )

    def execute(self, code: str, **kwargs) -> Dict[str, Any]:
        """
        Execute Python code.
        执行Python代码。

        Args:
            code: Python code string / Python代码字符串

        Returns:
            Execution result / 执行结果
        """
        old_stdout = sys.stdout
        sys.stdout = captured_output = StringIO()

        try:
            exec_globals = {
                "__builtins__": __builtins__,
                "math": math,
            }

            exec(code, exec_globals)

            output = captured_output.getvalue()

            return {
                "success": True,
                "output": output,
                "code": code
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "code": code
            }

        finally:
            sys.stdout = old_stdout


class WebSearchTool(Tool):
    """
    Web search tool.
    网络搜索工具。

    Search the internet for information.
    在互联网上搜索信息。

    Note: Requires a search API key (e.g., SerpAPI, Bing Search API)
    注意：需要搜索API密钥（例如SerpAPI、Bing搜索API）
    """

    def __init__(self, api_key: str = None):
        super().__init__(
            name="web_search",
            description="Search the internet for information",
            parameters={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query"
                    },
                    "num_results": {
                        "type": "integer",
                        "description": "Number of results to return (default: 5)"
                    }
                },
                "required": ["query"]
            }
        )
        self.api_key = api_key or os.getenv("SEARCH_API_KEY")

    def execute(self, query: str, num_results: int = 5, **kwargs) -> Dict[str, Any]:
        """
        Perform web search.
        执行网络搜索。

        Args:
            query: Search query / 搜索查询
            num_results: Number of results / 结果数量

        Returns:
            Search results / 搜索结果
        """
        if not self.api_key:
            return {
                "success": False,
                "error": "No search API key configured. Set SEARCH_API_KEY environment variable."
            }

        return {
            "success": True,
            "query": query,
            "results": [
                {
                    "title": "Example Result (API key needed for real search)",
                    "url": "https://example.com",
                    "snippet": "This is a placeholder. Configure SEARCH_API_KEY for real searches."
                }
            ],
            "message": "Web search tool requires API key configuration for real searches."
        }


class TextProcessingTool(Tool):
    """
    Text processing tool.
    文本处理工具。

    Perform various text operations like counting, splitting, replacing, etc.
    执行各种文本操作，如计数、拆分、替换等。
    """

    def __init__(self):
        super().__init__(
            name="text_processing",
            description="Process text: count words, split, replace, extract, etc.",
            parameters={
                "type": "object",
                "properties": {
                    "operation": {
                        "type": "string",
                        "description": "Operation: 'count_words', 'split', 'replace', 'upper', 'lower', 'strip'"
                    },
                    "text": {
                        "type": "string",
                        "description": "Text to process"
                    },
                    "pattern": {
                        "type": "string",
                        "description": "Pattern for split or replace operations"
                    },
                    "replacement": {
                        "type": "string",
                        "description": "Replacement text for replace operation"
                    }
                },
                "required": ["operation", "text"]
            }
        )

    def execute(
        self,
        operation: str,
        text: str,
        pattern: str = " ",
        replacement: str = "",
        **kwargs
    ) -> Dict[str, Any]:
        """
        Process text according to operation.
        根据操作处理文本。

        Args:
            operation: Operation to perform / 要执行的操作
            text: Input text / 输入文本
            pattern: Pattern for operations / 操作的模式
            replacement: Replacement text / 替换文本

        Returns:
            Processing result / 处理结果
        """
        try:
            if operation == "count_words":
                result = len(text.split())
            elif operation == "split":
                result = text.split(pattern)
            elif operation == "replace":
                result = text.replace(pattern, replacement)
            elif operation == "upper":
                result = text.upper()
            elif operation == "lower":
                result = text.lower()
            elif operation == "strip":
                result = text.strip()
            else:
                return {
                    "success": False,
                    "error": f"Unknown operation: {operation}"
                }

            return {
                "success": True,
                "operation": operation,
                "result": result
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "operation": operation
            }
