"""
Custom Tool Template / 自定义工具模板

Template for creating your own custom tools.
创建自己的自定义工具的模板。

Author: LLM Agent Framework
License: MIT
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import Dict, Any, List
from core.tool import Tool
from core.agent import Agent
from core.llm_client import LLMClient
from dotenv import load_dotenv

load_dotenv()


class CustomCalculatorTool(Tool):
    """
    Example: Custom calculator with additional functions.
    示例：带有额外功能的自定义计算器。
    """

    def __init__(self):
        super().__init__(
            name="custom_calculator",
            description="Perform calculations with custom functions like factorial and fibonacci",
            parameters={
                "type": "object",
                "properties": {
                    "operation": {
                        "type": "string",
                        "description": "Operation: 'factorial', 'fibonacci', 'power'"
                    },
                    "number": {
                        "type": "integer",
                        "description": "Input number"
                    },
                    "base": {
                        "type": "integer",
                        "description": "Base for power operation (optional)"
                    }
                },
                "required": ["operation", "number"]
            }
        )

    def execute(self, operation: str, number: int, base: int = 2, **kwargs) -> Dict[str, Any]:
        """
        Execute calculator operation.
        执行计算器操作。
        """
        try:
            if operation == "factorial":
                result = self._factorial(number)
            elif operation == "fibonacci":
                result = self._fibonacci(number)
            elif operation == "power":
                result = number ** base
            else:
                return {
                    "success": False,
                    "error": f"Unknown operation: {operation}"
                }

            return {
                "success": True,
                "operation": operation,
                "input": number,
                "result": result
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def _factorial(self, n: int) -> int:
        """Calculate factorial. / 计算阶乘。"""
        if n < 0:
            raise ValueError("Factorial not defined for negative numbers")
        if n == 0 or n == 1:
            return 1
        return n * self._factorial(n - 1)

    def _fibonacci(self, n: int) -> int:
        """Calculate nth Fibonacci number. / 计算第n个斐波那契数。"""
        if n < 0:
            raise ValueError("Fibonacci not defined for negative numbers")
        if n == 0:
            return 0
        if n == 1:
            return 1
        return self._fibonacci(n - 1) + self._fibonacci(n - 2)


class WeatherTool(Tool):
    """
    Example: Weather information tool (placeholder).
    示例：天气信息工具（占位符）。

    In production, integrate with real weather API like OpenWeatherMap.
    在生产环境中，与真实的天气API（如OpenWeatherMap）集成。
    """

    def __init__(self, api_key: str = None):
        super().__init__(
            name="weather",
            description="Get weather information for a city",
            parameters={
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "City name"
                    },
                    "units": {
                        "type": "string",
                        "description": "Units: 'celsius' or 'fahrenheit'"
                    }
                },
                "required": ["city"]
            }
        )
        self.api_key = api_key

    def execute(self, city: str, units: str = "celsius", **kwargs) -> Dict[str, Any]:
        """
        Get weather information.
        获取天气信息。
        """
        return {
            "success": True,
            "city": city,
            "temperature": 22 if units == "celsius" else 72,
            "units": units,
            "condition": "Sunny",
            "message": "This is mock data. Integrate with a real weather API for production."
        }


class DatabaseQueryTool(Tool):
    """
    Example: Database query tool.
    示例：数据库查询工具。

    Template for creating tools that interact with databases.
    创建与数据库交互的工具的模板。
    """

    def __init__(self, connection_string: str = None):
        super().__init__(
            name="database_query",
            description="Query database and return results",
            parameters={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "SQL query to execute"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of results"
                    }
                },
                "required": ["query"]
            }
        )
        self.connection_string = connection_string

    def execute(self, query: str, limit: int = 10, **kwargs) -> Dict[str, Any]:
        """
        Execute database query.
        执行数据库查询。
        """
        # In production, use actual database connection
        # import sqlite3 or psycopg2, etc.

        return {
            "success": True,
            "query": query,
            "results": [
                {"id": 1, "name": "Example Row 1"},
                {"id": 2, "name": "Example Row 2"}
            ],
            "count": 2,
            "message": "Mock results. Connect to real database for production."
        }


class EmailTool(Tool):
    """
    Example: Email sending tool.
    示例：邮件发送工具。

    Template for creating communication tools.
    创建通信工具的模板。
    """

    def __init__(self, smtp_config: Dict[str, Any] = None):
        super().__init__(
            name="email",
            description="Send emails",
            parameters={
                "type": "object",
                "properties": {
                    "to": {
                        "type": "string",
                        "description": "Recipient email address"
                    },
                    "subject": {
                        "type": "string",
                        "description": "Email subject"
                    },
                    "body": {
                        "type": "string",
                        "description": "Email body"
                    }
                },
                "required": ["to", "subject", "body"]
            }
        )
        self.smtp_config = smtp_config or {}

    def execute(self, to: str, subject: str, body: str, **kwargs) -> Dict[str, Any]:
        """
        Send email.
        发送邮件。
        """
        # In production, use smtplib or email service API
        # import smtplib
        # from email.mime.text import MIMEText

        return {
            "success": True,
            "to": to,
            "subject": subject,
            "message": "Email sent successfully (mock). Configure SMTP for real sending."
        }


def example_using_custom_tools():
    """
    Example of using custom tools with an agent.
    使用自定义工具与智能体的示例。
    """
    print("=" * 70)
    print("Custom Tools Example / 自定义工具示例")
    print("=" * 70)

    client = LLMClient(
        api_url=os.getenv("LLM_API_URL"),
        api_key=os.getenv("LLM_API_KEY"),
        model=os.getenv("LLM_MODEL", "gpt-4")
    )

    custom_tools = [
        CustomCalculatorTool(),
        WeatherTool(),
        DatabaseQueryTool(),
        EmailTool()
    ]

    agent = Agent(
        name="CustomAssistant",
        llm_client=client,
        tools=custom_tools,
        system_prompt="You are an assistant with custom tools."
    )

    tasks = [
        "Calculate the factorial of 5",
        "What's the weather in New York?",
        "Query the database for user records",
    ]

    for i, task in enumerate(tasks, 1):
        print(f"\n{i}. Task: {task}")
        print("-" * 70)

        response = agent.run(task)
        print(f"Response: {response}\n")


if __name__ == "__main__":
    """
    Template Guide / 模板指南

    To create your own custom tool:
    要创建自己的自定义工具：

    1. Inherit from Tool class / 继承Tool类
    2. Define __init__ with name, description, parameters / 定义__init__，包含名称、描述、参数
    3. Implement execute method / 实现execute方法
    4. Return dict with 'success' and result data / 返回包含'success'和结果数据的字典
    5. Handle exceptions gracefully / 优雅地处理异常

    Key Principles / 关键原则:
    - Keep tools focused on single responsibility / 保持工具专注于单一职责
    - Provide clear descriptions for LLM / 为LLM提供清晰的描述
    - Validate inputs in execute method / 在execute方法中验证输入
    - Return structured, consistent results / 返回结构化、一致的结果
    - Include error handling / 包含错误处理
    """

    print("\n" + "="*70)
    print("Custom Tool Template Examples")
    print("自定义工具模板示例")
    print("="*70 + "\n")

    try:
        example_using_custom_tools()

    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure you have configured your .env file.")

    print("\n" + "="*70)
    print("Example completed! / 示例完成！")
    print("="*70 + "\n")
