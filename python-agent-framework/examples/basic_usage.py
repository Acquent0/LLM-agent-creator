"""
Basic Usage Examples / 基础使用示例

Simple examples demonstrating core functionality.
演示核心功能的简单示例。

Author: LLM Agent Framework
License: MIT
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.agent import Agent
from core.llm_client import LLMClient
from tools.base_tools import CalculatorTool, TextProcessingTool
from dotenv import load_dotenv

load_dotenv()


def example_1_simple_agent():
    """
    Example 1: Create a simple agent with calculator tool.
    示例1：创建一个带有计算器工具的简单智能体。
    """
    print("=" * 60)
    print("Example 1: Simple Agent with Calculator")
    print("示例1：带计算器的简单智能体")
    print("=" * 60)

    client = LLMClient(
        api_url=os.getenv("LLM_API_URL"),
        api_key=os.getenv("LLM_API_KEY"),
        model=os.getenv("LLM_MODEL", "gpt-4")
    )

    agent = Agent(
        name="MathAssistant",
        llm_client=client,
        tools=[CalculatorTool()],
        system_prompt="You are a helpful math assistant."
    )

    response = agent.run("What is the square root of 144?")
    print(f"\nResponse: {response}\n")


def example_2_multiple_tools():
    """
    Example 2: Agent with multiple tools.
    示例2：具有多个工具的智能体。
    """
    print("=" * 60)
    print("Example 2: Agent with Multiple Tools")
    print("示例2：具有多个工具的智能体")
    print("=" * 60)

    client = LLMClient(
        api_url=os.getenv("LLM_API_URL"),
        api_key=os.getenv("LLM_API_KEY"),
        model=os.getenv("LLM_MODEL", "gpt-4")
    )

    agent = Agent(
        name="TextAnalyzer",
        llm_client=client,
        tools=[
            CalculatorTool(),
            TextProcessingTool()
        ],
        system_prompt="You are a text analysis assistant."
    )

    text = "Hello World! This is a test message."
    response = agent.run(f"Count the words in this text: '{text}'")
    print(f"\nResponse: {response}\n")


def example_3_conversation_memory():
    """
    Example 3: Agent with conversation memory.
    示例3：具有对话记忆的智能体。
    """
    print("=" * 60)
    print("Example 3: Agent with Conversation Memory")
    print("示例3：具有对话记忆的智能体")
    print("=" * 60)

    client = LLMClient(
        api_url=os.getenv("LLM_API_URL"),
        api_key=os.getenv("LLM_API_KEY"),
        model=os.getenv("LLM_MODEL", "gpt-4")
    )

    agent = Agent(
        name="Assistant",
        llm_client=client,
        tools=[CalculatorTool()],
        memory_enabled=True
    )

    response1 = agent.run("Calculate 10 + 5")
    print(f"\nFirst response: {response1}")

    response2 = agent.run("Now multiply that result by 2")
    print(f"\nSecond response: {response2}\n")


def example_4_custom_system_prompt():
    """
    Example 4: Agent with custom system prompt.
    示例4：具有自定义系统提示的智能体。
    """
    print("=" * 60)
    print("Example 4: Custom System Prompt")
    print("示例4：自定义系统提示")
    print("=" * 60)

    client = LLMClient(
        api_url=os.getenv("LLM_API_URL"),
        api_key=os.getenv("LLM_API_KEY"),
        model=os.getenv("LLM_MODEL", "gpt-4")
    )

    custom_prompt = """You are a professional data scientist specializing in
    statistical analysis. Provide detailed, academic-style explanations."""

    agent = Agent(
        name="DataScientist",
        llm_client=client,
        tools=[CalculatorTool()],
        system_prompt=custom_prompt
    )

    response = agent.run("Explain the concept of standard deviation")
    print(f"\nResponse: {response}\n")


def example_5_execution_log():
    """
    Example 5: Viewing agent execution logs.
    示例5：查看智能体执行日志。
    """
    print("=" * 60)
    print("Example 5: Execution Logs")
    print("示例5：执行日志")
    print("=" * 60)

    client = LLMClient(
        api_url=os.getenv("LLM_API_URL"),
        api_key=os.getenv("LLM_API_KEY"),
        model=os.getenv("LLM_MODEL", "gpt-4")
    )

    agent = Agent(
        name="Calculator",
        llm_client=client,
        tools=[CalculatorTool()]
    )

    agent.run("Calculate sqrt(25)")

    log = agent.get_execution_log()
    print(f"\nExecution log entries: {len(log)}")
    for entry in log:
        print(f"- {entry['event_type']}: {entry.get('data', '')[:50]}...")
    print()


if __name__ == "__main__":
    """
    Run all examples.
    运行所有示例。

    Make sure to set your environment variables in .env file:
    确保在.env文件中设置环境变量：
    - LLM_API_URL
    - LLM_API_KEY
    - LLM_MODEL
    """

    print("\n" + "="*60)
    print("LLM Agent Framework - Basic Usage Examples")
    print("LLM智能体框架 - 基础使用示例")
    print("="*60 + "\n")

    try:
        example_1_simple_agent()
        print("\n" + "-"*60 + "\n")

        example_2_multiple_tools()
        print("\n" + "-"*60 + "\n")

        example_3_conversation_memory()
        print("\n" + "-"*60 + "\n")

        example_4_custom_system_prompt()
        print("\n" + "-"*60 + "\n")

        example_5_execution_log()

    except Exception as e:
        print(f"\n❌ Error running examples: {e}")
        print("\nMake sure you have:")
        print("1. Set up your .env file with API credentials")
        print("2. Installed all requirements: pip install -r requirements.txt")

    print("\n" + "="*60)
    print("Examples completed!")
    print("示例完成！")
    print("="*60 + "\n")
