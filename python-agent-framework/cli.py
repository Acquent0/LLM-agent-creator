#!/usr/bin/env python3
"""
CLI Interface for LLM Agent Framework
LLM智能体框架的命令行界面

Interactive command-line interface for running agents without Streamlit.
不使用Streamlit运行智能体的交互式命令行界面。

Author: LLM Agent Framework
License: MIT
"""

import sys
import os
import json
from typing import List, Dict, Any, Optional

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.agent import Agent
from core.llm_client import LLMClient
from tools.base_tools import *
from tools.research_tools import *
from tools.data_tools import *
from utils.tool_generator import ToolGenerator
from utils.tool_indexer import ToolIndexer
from dotenv import load_dotenv

load_dotenv()


class AgentCLI:
    """Command-line interface for LLM Agent Framework."""

    def __init__(self):
        """Initialize CLI."""
        self.llm_client = None
        self.agent = None
        self.tool_generator = None
        self.tool_indexer = None
        self.available_tools = {}
        self.chat_history = []

    def run(self):
        """Run the CLI main loop."""
        self.print_banner()
        
        # Setup LLM
        if not self.setup_llm():
            print("❌ Failed to setup LLM. Exiting...")
            return

        # Setup tools
        self.setup_tools()

        # Main loop
        while True:
            print("\n" + "="*60)
            print("📋 Main Menu")
            print("="*60)
            print("1. 💬 Chat with Agent")
            print("2. 🛠️  Generate New Tool")
            print("3. 📚 List Available Tools")
            print("4. 🔍 Search Tools")
            print("5. ⚙️  Reconfigure LLM")
            print("6. 📜 View Chat History")
            print("7. 🗑️  Clear Chat History")
            print("0. 🚪 Exit")
            print("="*60)

            choice = input("\n👉 Select option: ").strip()

            if choice == "1":
                self.chat_mode()
            elif choice == "2":
                self.generate_tool_interactive()
            elif choice == "3":
                self.list_tools()
            elif choice == "4":
                self.search_tools_interactive()
            elif choice == "5":
                self.setup_llm()
            elif choice == "6":
                self.view_history()
            elif choice == "7":
                self.clear_history()
            elif choice == "0":
                print("\n👋 Goodbye!\n")
                break
            else:
                print("❌ Invalid option. Please try again.")

    def print_banner(self):
        """Print welcome banner."""
        banner = """
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║          🤖 LLM Agent Framework - CLI Mode 🤖             ║
║                                                           ║
║       Build and Run Intelligent AI Agents                ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
        """
        print(banner)

    def setup_llm(self) -> bool:
        """Setup LLM configuration."""
        print("\n🔧 LLM Configuration")
        print("-" * 60)

        # Check for environment variables first
        api_url = os.getenv("API_URL")
        api_key = os.getenv("API_KEY")
        model = os.getenv("MODEL")

        if api_url and api_key:
            print(f"✓ Found configuration in environment variables")
            use_env = input(f"Use API URL: {api_url}? (Y/n): ").strip().lower()
            if use_env != 'n':
                model = model or "gpt-4"
                print(f"✓ Using model: {model}")
            else:
                api_url = None

        if not api_url:
            api_url = input("API URL (e.g., https://api.openai.com/v1/chat/completions): ").strip()
            api_key = input("API Key: ").strip()
            model = input("Model (default: gpt-4): ").strip() or "gpt-4"

        # Test connection
        print("\n🔄 Testing connection...")
        try:
            self.llm_client = LLMClient(
                api_url=api_url,
                api_key=api_key,
                model=model,
                api_type="openai"
            )

            # Simple test
            test_response = self.llm_client.chat([
                {"role": "user", "content": "Hello"}
            ], max_tokens=10)

            if test_response.get("success"):
                print("✅ Connection successful!")
                
                # Initialize tool generator and indexer
                self.tool_generator = ToolGenerator(self.llm_client)
                self.tool_indexer = ToolIndexer(self.llm_client)
                
                return True
            else:
                print(f"❌ Connection failed: {test_response.get('error')}")
                return False

        except Exception as e:
            print(f"❌ Error: {e}")
            return False

    def setup_tools(self):
        """Setup available tools."""
        print("\n🛠️  Setting up tools...")
        
        # Register built-in tools
        self.available_tools = {
            "calculator": CalculatorTool(),
            "file_io": FileIOTool(),
            "python_repl": PythonREPLTool(),
            "text_processing": TextProcessingTool(),
            "scientific_compute": ScientificComputeTool(),
            "statistical_test": StatisticalTestTool(),
            "unit_converter": UnitConverterTool(),
            "data_analysis": DataAnalysisTool(),
            "visualization": VisualizationTool(),
            "data_cleaning": DataCleaningTool()
        }

        print(f"✅ Loaded {len(self.available_tools)} built-in tools")

    def chat_mode(self):
        """Interactive chat mode with the agent."""
        print("\n💬 Chat Mode (type 'exit' to return to main menu)")
        print("-" * 60)

        # Create agent if not exists
        if not self.agent:
            # Get relevant tools based on initial context
            print("\n🤔 What would you like help with?")
            context = input("Task description: ").strip()
            
            if not context:
                print("❌ Task description required")
                return

            # Find relevant tools
            relevant_tools = self.tool_indexer.search_tools(context, max_results=5)
            
            if relevant_tools:
                print(f"\n🔍 Found {len(relevant_tools)} relevant tools:")
                for i, tool in enumerate(relevant_tools, 1):
                    print(f"  {i}. {tool['name']} (score: {tool['score']:.2f})")

            # Select tools to use
            selected_tools = []
            for tool in relevant_tools:
                tool_name_lower = tool['name'].lower().replace("tool", "")
                for key, tool_obj in self.available_tools.items():
                    if key in tool_name_lower or tool_name_lower in key:
                        selected_tools.append(tool_obj)
                        break

            # Create agent with selected tools
            self.agent = Agent(
                name="CLI Agent",
                llm_client=self.llm_client,
                tools=selected_tools or list(self.available_tools.values())[:5],
                max_iterations=10
            )

            print(f"\n✅ Agent created with {len(self.agent.tools)} tools")

        # Chat loop
        while True:
            user_input = input("\n👤 You: ").strip()

            if user_input.lower() in ['exit', 'quit', 'back']:
                break

            if not user_input:
                continue

            print("\n🤖 Agent:", end=" ", flush=True)
            
            try:
                result = self.agent.run(user_input)
                
                if result.get("success"):
                    print(result["response"])
                    
                    # Save to history
                    self.chat_history.append({
                        "user": user_input,
                        "agent": result["response"],
                        "iterations": result.get("iterations", 0)
                    })
                else:
                    print(f"\n❌ Error: {result.get('error')}")

            except Exception as e:
                print(f"\n❌ Error: {e}")

    def generate_tool_interactive(self):
        """Interactive tool generation."""
        print("\n🛠️  Generate New Tool")
        print("-" * 60)

        tool_name = input("Tool name: ").strip()
        if not tool_name:
            print("❌ Tool name required")
            return

        description = input("Description (what does this tool do?): ").strip()
        if not description:
            print("❌ Description required")
            return

        # Input parameters
        print("\n📥 Input Parameters (press Enter when done)")
        parameters = []
        i = 1
        while True:
            print(f"\nParameter {i}:")
            param_name = input("  Name (or Enter to finish): ").strip()
            if not param_name:
                break

            param_type = input("  Type (str/int/float/list/dict): ").strip() or "str"
            param_desc = input("  Description: ").strip()

            parameters.append({
                "name": param_name,
                "type": param_type,
                "description": param_desc
            })
            i += 1

        expected_output = input("\n📤 Expected output description: ").strip()
        
        impl_details = input("💡 Implementation details (optional): ").strip() or None
        
        # Dependencies
        deps_input = input("📦 Dependencies (comma-separated, optional): ").strip()
        dependencies = [d.strip() for d in deps_input.split(",")] if deps_input else None

        # Generate
        print("\n🔄 Generating tool...")
        result = self.tool_generator.generate_tool(
            tool_name=tool_name,
            description=description,
            input_parameters=parameters,
            expected_output=expected_output,
            implementation_details=impl_details,
            dependencies=dependencies
        )

        if result.get("success"):
            print(f"\n✅ Tool generated successfully!")
            print(f"📁 Saved to: {result['file_path']}")
            
            # Refresh index
            self.tool_indexer.refresh_index()
            print("✅ Tool index updated")
        else:
            print(f"\n❌ Failed to generate tool: {result.get('error')}")

    def list_tools(self):
        """List all available tools."""
        print("\n📚 Available Tools")
        print("-" * 60)

        tools = self.tool_indexer.list_all_tools()
        
        # Group by category
        categories = {}
        for tool in tools:
            cat = tool.get("category", "other")
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(tool)

        for category, cat_tools in sorted(categories.items()):
            print(f"\n{category.upper().replace('_', ' ')}:")
            for tool in cat_tools:
                print(f"  • {tool['name']}")
                print(f"    {tool['description']}")

        print(f"\n📊 Total: {len(tools)} tools")

    def search_tools_interactive(self):
        """Interactive tool search."""
        print("\n🔍 Search Tools")
        print("-" * 60)

        query = input("Enter task description: ").strip()
        if not query:
            print("❌ Query required")
            return

        results = self.tool_indexer.search_tools(query, max_results=10)

        if results:
            print(f"\n✅ Found {len(results)} relevant tools:")
            for i, tool in enumerate(results, 1):
                print(f"\n{i}. {tool['name']} (relevance: {tool['score']:.2f})")
                print(f"   {tool['description']}")
                print(f"   Category: {tool['category']}")
        else:
            print("\n❌ No relevant tools found")

    def view_history(self):
        """View chat history."""
        print("\n📜 Chat History")
        print("-" * 60)

        if not self.chat_history:
            print("No chat history yet.")
            return

        for i, entry in enumerate(self.chat_history, 1):
            print(f"\n[{i}] User: {entry['user']}")
            print(f"    Agent: {entry['agent'][:200]}{'...' if len(entry['agent']) > 200 else ''}")

    def clear_history(self):
        """Clear chat history."""
        self.chat_history = []
        print("\n✅ Chat history cleared")


def main():
    """Main entry point."""
    cli = AgentCLI()
    try:
        cli.run()
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted. Goodbye!\n")
    except Exception as e:
        print(f"\n❌ Error: {e}\n")


if __name__ == "__main__":
    main()
