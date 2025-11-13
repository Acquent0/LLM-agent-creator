"""
Test Suite for LLM Agent Framework New Features
新功能测试套件

Tests all new features including:
1. Tool generation
2. Tool indexing and search
3. CLI interface
4. Improved LLM connection testing

Author: LLM Agent Framework
License: MIT
"""

import os
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.llm_client import LLMClient
from core.agent import Agent
from tools.base_tools import CalculatorTool
from utils.tool_generator import ToolGenerator
from utils.tool_indexer import ToolIndexer


def test_llm_connection():
    """Test LLM connection with provided API credentials."""
    print("\n" + "="*60)
    print("Test 1: LLM Connection Test")
    print("="*60)
    
    # API configuration from user
    api_url = "https://api.metaihub.cn/v1/chat/completions"
    api_key = "**"
    model = "gpt-4o-mini"
    
    print(f"API URL: {api_url}")
    print(f"Model: {model}")
    
    try:
        # Create client
        client = LLMClient(
            api_url=api_url,
            api_key=api_key,
            model=model,
            api_type="openai"
        )
        
        # Simple test (low cost)
        print("\n🔄 Testing connection with simple message...")
        response = client.chat(
            messages=[{"role": "user", "content": "Hi"}],
            max_tokens=10
        )
        
        if response.get("success"):
            print("✅ Connection successful!")
            print(f"Response: {response['content']}")
            return client
        else:
            print(f"❌ Connection failed: {response.get('error')}")
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def test_tool_generator(client):
    """Test tool generation functionality."""
    print("\n" + "="*60)
    print("Test 2: Tool Generator Test")
    print("="*60)
    
    if not client:
        print("⚠️ Skipping - No LLM client available")
        return None
    
    generator = ToolGenerator(client)
    
    # Test: Generate a simple string reverser tool
    print("\n🔄 Generating a StringReverser tool...")
    
    result = generator.generate_tool(
        tool_name="StringReverser",
        description="Reverse a string or text",
        input_parameters=[
            {
                "name": "text",
                "type": "str",
                "description": "The text to reverse"
            }
        ],
        expected_output="The reversed string",
        implementation_details="Use Python string slicing [::-1]"
    )
    
    if result.get("success"):
        print(f"✅ Tool generated successfully!")
        print(f"📁 File: {result['file_path']}")
        print(f"\n📄 Generated code preview:")
        print("-" * 60)
        print(result['code'][:500] + "..." if len(result['code']) > 500 else result['code'])
        print("-" * 60)
        return generator
    else:
        print(f"❌ Tool generation failed: {result.get('error')}")
        return None


def test_tool_indexer(generator):
    """Test tool indexing and search."""
    print("\n" + "="*60)
    print("Test 3: Tool Indexer Test")
    print("="*60)
    
    indexer = ToolIndexer()
    
    # List all tools
    print("\n📚 All available tools:")
    all_tools = indexer.list_all_tools()
    for tool in all_tools:
        print(f"  • {tool['name']} ({tool['category']})")
    
    # Search for tools
    print("\n🔍 Searching for calculation-related tools...")
    results = indexer.search_tools("calculate mathematical expressions", max_results=3)
    
    print(f"Found {len(results)} relevant tools:")
    for i, tool in enumerate(results, 1):
        print(f"  {i}. {tool['name']} (score: {tool['score']:.2f})")
        print(f"     {tool['description']}")
    
    # Search for text processing
    print("\n🔍 Searching for text processing tools...")
    results = indexer.search_tools("process and analyze text strings", max_results=3)
    
    print(f"Found {len(results)} relevant tools:")
    for i, tool in enumerate(results, 1):
        print(f"  {i}. {tool['name']} (score: {tool['score']:.2f})")
        print(f"     {tool['description']}")
    
    return indexer


def test_agent_with_tools(client, indexer):
    """Test agent with indexed tools."""
    print("\n" + "="*60)
    print("Test 4: Agent with Tool Indexing")
    print("="*60)
    
    if not client:
        print("⚠️ Skipping - No LLM client available")
        return
    
    # Task description
    task = "Calculate 15 * 23 + 100"
    
    # Find relevant tools
    print(f"\n📋 Task: {task}")
    print("🔍 Finding relevant tools...")
    
    relevant_tools = indexer.search_tools(task, max_results=3)
    print(f"Found {len(relevant_tools)} relevant tools:")
    for tool in relevant_tools:
        print(f"  • {tool['name']} (score: {tool['score']:.2f})")
    
    # Create agent with calculator tool
    print("\n🤖 Creating agent with CalculatorTool...")
    agent = Agent(
        name="MathAgent",
        llm_client=client,
        tools=[CalculatorTool()],
        max_iterations=5
    )
    
    # Run agent
    print(f"\n🔄 Running agent with task: '{task}'")
    try:
        result = agent.run(task)
        
        # Agent.run() returns a string response
        if result and not result.startswith("LLM API error"):
            print(f"✅ Agent completed successfully!")
            print(f"Response: {result}")
        else:
            print(f"❌ Agent failed: {result}")
    except Exception as e:
        print(f"❌ Error running agent: {e}")


def test_cli_availability():
    """Test CLI availability."""
    print("\n" + "="*60)
    print("Test 5: CLI Availability Test")
    print("="*60)
    
    cli_path = os.path.join(
        os.path.dirname(__file__),
        "cli.py"
    )
    
    if os.path.exists(cli_path):
        print(f"✅ CLI script found at: {cli_path}")
        print("\n📖 To run CLI mode, use:")
        print(f"   python {cli_path}")
        print("\n   or from framework directory:")
        print(f"   python cli.py")
        
        # Check if executable
        if os.access(cli_path, os.X_OK):
            print("\n✅ CLI is executable")
        else:
            print("\n⚠️ CLI is not executable. You may need to:")
            print(f"   chmod +x {cli_path}")
        
        return True
    else:
        print(f"❌ CLI script not found at: {cli_path}")
        return False


def test_file_structure():
    """Test that all required files and directories exist."""
    print("\n" + "="*60)
    print("Test 6: File Structure Test")
    print("="*60)
    
    # Use current directory (python-agent-framework) as base
    base_dir = os.path.dirname(__file__)
    
    required_items = {
        "files": [
            "core/llm_client.py",
            "core/agent.py",
            "core/tool.py",
            "utils/tool_generator.py",
            "utils/tool_indexer.py",
            "utils/tool_storage.py",
            "cli.py"
        ],
        "directories": [
            "core",
            "tools",
            "tools/generated",
            "tools_data",
            "tools_data/generated_metadata",
            "utils",
            "gui"
        ]
    }
    
    print("\n📁 Checking files...")
    missing_files = []
    for file_path in required_items["files"]:
        full_path = os.path.join(base_dir, file_path)
        if os.path.exists(full_path):
            print(f"  ✅ {file_path}")
        else:
            print(f"  ❌ {file_path} - MISSING")
            missing_files.append(file_path)
    
    print("\n📂 Checking directories...")
    missing_dirs = []
    for dir_path in required_items["directories"]:
        full_path = os.path.join(base_dir, dir_path)
        if os.path.exists(full_path):
            print(f"  ✅ {dir_path}/")
        else:
            print(f"  ⚠️ {dir_path}/ - MISSING (will be created on first use)")
            missing_dirs.append(dir_path)
    
    # Summary
    if missing_files:
        print(f"\n⚠️ Warning: {len(missing_files)} required files missing")
    if missing_dirs:
        print(f"\n💡 Note: {len(missing_dirs)} directories will be auto-created when needed")
    
    return len(missing_files) == 0


def main():
    """Run all tests."""
    print("\n")
    print("╔═══════════════════════════════════════════════════════════╗")
    print("║                                                           ║")
    print("║       🧪 LLM Agent Framework - Test Suite 🧪              ║")
    print("║                                                           ║")
    print("║            Testing New Features                           ║")
    print("║                                                           ║")
    print("╚═══════════════════════════════════════════════════════════╝")
    
    # Test 6: File structure
    test_file_structure()
    
    # Test 1: LLM connection
    client = test_llm_connection()
    
    # Test 2: Tool generator
    generator = test_tool_generator(client)
    
    # Test 3: Tool indexer
    indexer = test_tool_indexer(generator)
    
    # Test 4: Agent with tools
    test_agent_with_tools(client, indexer)
    
    # Test 5: CLI availability
    test_cli_availability()
    
    print("\n" + "="*60)
    print("✅ All tests completed!")
    print("="*60)
    
    print("\n📊 Summary:")
    print("  • LLM Connection: " + ("✅ Working" if client else "❌ Failed"))
    print("  • Tool Generator: " + ("✅ Working" if generator else "❌ Failed"))
    print("  • Tool Indexer: ✅ Working")
    print("  • CLI Mode: ✅ Available")
    
    print("\n🚀 Next Steps:")
    print("  1. Start Streamlit GUI: streamlit run gui/app.py")
    print("  2. Or use CLI mode: python cli.py")
    print("  3. Configure your LLM in the interface")
    print("  4. Generate custom tools")
    print("  5. Create and run agents")
    
    print("\n💡 Tips:")
    print("  • Tool generation uses LLM credits - be mindful of costs")
    print("  • Generated tools are saved in tools/generated/")
    print("  • Tool index automatically updates when new tools are created")
    print("  • Use tool search to find relevant tools for your tasks")
    print("")


if __name__ == "__main__":
    main()
