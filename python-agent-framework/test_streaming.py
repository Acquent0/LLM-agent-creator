#!/usr/bin/env python3
"""
Test streaming functionality
测试流式输出功能
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from core.llm_client import LLMClient
from core.agent import Agent
from tools.base_tools import get_base_tools

def test_streaming():
    """Test the streaming agent response"""
    
    print("="*70)
    print("🧪 测试流式输出功能 | Testing Streaming Functionality")
    print("="*70)
    
    # Initialize LLM client
    llm_client = LLMClient(
        api_url="https://api.metaihub.cn/v1/chat/completions",
        api_key="sk-aeASZGvP8mU82z2HBbE9B1Aa5fA14522A2D07a102134978d",
        model="gpt-4o-mini"
    )
    
    # Get base tools
    tools = get_base_tools()
    
    # Create agent with ReAct mode
    agent = Agent(
        name="Test Agent",
        llm_client=llm_client,
        tools=tools[:2],  # Only use first 2 tools for testing
        role="通用助手",
        use_react=True
    )
    
    print("\n🤖 智能体已创建")
    print(f"   - 工具数量: {len(agent.tools)}")
    print(f"   - 角色: 通用助手")
    print(f"   - ReAct模式: 启用")
    
    # Test task
    task = "帮我计算 1234 * 5234 然后对结果开三次方"
    
    print(f"\n💬 用户输入: {task}")
    print("\n" + "="*70)
    print("开始流式输出：")
    print("="*70 + "\n")
    
    # Stream the response
    for event in agent.run_stream(task):
        event_type = event.get("type")
        content = event.get("content", "")
        
        if event_type == "iteration":
            print(f"\n{content}")
        elif event_type == "thought_start":
            print(content, end="", flush=True)
        elif event_type == "thought_chunk":
            print(content, end="", flush=True)
        elif event_type == "thought_end":
            print(content)
        elif event_type == "thought":
            print(content)
        elif event_type == "tool_call":
            print(f"\n{content}")
        elif event_type == "tool_result":
            print(content)
        elif event_type == "final_answer":
            print(content)
        elif event_type == "response":
            print(f"\n📝 响应: {content}")
        elif event_type == "error":
            print(f"\n❌ 错误: {content}")
        elif event_type == "max_iterations":
            print(f"\n{content}")
    
    print("\n" + "="*70)
    print("✅ 测试完成！")
    print("="*70)

if __name__ == "__main__":
    test_streaming()
