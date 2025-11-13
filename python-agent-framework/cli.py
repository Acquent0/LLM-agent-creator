#!/usr/bin/env python3
"""
CLI Interface for LLM Agent Framework
LLM智能体框架的命令行界面

Interactive command-line interface for running agents without Streamlit.
不使用Streamlit运行智能体的交互式命令行界面。

Features:
- LLM Configuration / LLM配置
- Tool Management / 工具管理  
- Agent Creation & Management / 智能体创建和管理
- Streaming Chat / 流式聊天
- Tool Generation / 工具生成

Author: LLM Agent Framework
License: MIT
"""

import sys
import os
import json
import time
from typing import List, Dict, Any, Optional
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.agent import Agent
from core.llm_client import LLMClient
from core.prompts import ROLE_TEMPLATES
from tools.base_tools import get_base_tools
from utils.tool_generator import ToolGenerator
from utils.tool_storage import ToolStorageManager
from utils.agent_storage import AgentStorageManager
from utils.dynamic_tool import DynamicToolLoader
from dotenv import load_dotenv

load_dotenv()


class Colors:
    """ANSI color codes for terminal output."""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class AgentCLI:
    """Enhanced command-line interface for LLM Agent Framework."""

    def __init__(self):
        """Initialize CLI."""
        self.llm_client = None
        self.agent = None
        self.tool_generator = None
        self.tool_storage = ToolStorageManager()
        self.agent_storage = AgentStorageManager()
        self.dynamic_loader = DynamicToolLoader()
        
        self.base_tools = []
        self.custom_tools = []
        self.generated_tools = []
        self.current_agent = None
        self.chat_history = []

    def run(self):
        """Run the CLI main loop."""
        self.print_banner()
        
        # Setup LLM
        if not self.setup_llm():
            print(f"{Colors.RED}❌ Failed to setup LLM. Exiting...{Colors.ENDC}")
            return

        # Load tools
        self.load_all_tools()

        # Main loop
        while True:
            self.print_main_menu()
            choice = input(f"\n{Colors.CYAN}👉 Select option: {Colors.ENDC}").strip()

            if choice == "1":
                self.llm_configuration_menu()
            elif choice == "2":
                self.tool_management_menu()
            elif choice == "3":
                self.agent_management_menu()
            elif choice == "4":
                self.chat_with_agent()
            elif choice == "5":
                self.view_statistics()
            elif choice == "0":
                print(f"\n{Colors.GREEN}👋 Goodbye!{Colors.ENDC}\n")
                break
            else:
                print(f"{Colors.RED}❌ Invalid option. Please try again.{Colors.ENDC}")

    def print_banner(self):
        """Print welcome banner."""
        banner = f"""
{Colors.CYAN}╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║       {Colors.BOLD}🤖 LLM Agent Framework - Enhanced CLI 🤖{Colors.ENDC}{Colors.CYAN}            ║
║                                                               ║
║          Build and Run Intelligent AI Agents                 ║
║          with Streaming Output & Tool Management             ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝{Colors.ENDC}
        """
        print(banner)

    def print_main_menu(self):
        """Print main menu."""
        print(f"\n{Colors.BOLD}{'='*65}")
        print(f"📋 Main Menu | 主菜单")
        print(f"{'='*65}{Colors.ENDC}")
        print(f"{Colors.GREEN}1. 🔧 LLM Configuration       | LLM配置{Colors.ENDC}")
        print(f"{Colors.BLUE}2. 🛠️  Tool Management         | 工具管理{Colors.ENDC}")
        print(f"{Colors.YELLOW}3. 🤖 Agent Management        | 智能体管理{Colors.ENDC}")
        print(f"{Colors.CYAN}4. 💬 Chat with Agent         | 与智能体对话{Colors.ENDC}")
        print(f"{Colors.HEADER}5. 📊 View Statistics         | 查看统计{Colors.ENDC}")
        print(f"{Colors.RED}0. 🚪 Exit                    | 退出{Colors.ENDC}")
        print(f"{Colors.BOLD}{'='*65}{Colors.ENDC}")

    def setup_llm(self) -> bool:
        """Setup LLM configuration."""
        print(f"\n{Colors.BOLD}🔧 LLM Configuration{Colors.ENDC}")
        print("-" * 65)

        # Check for environment variables first
        api_url = os.getenv("API_URL")
        api_key = os.getenv("API_KEY")
        model = os.getenv("MODEL")

        if api_url and api_key:
            print(f"{Colors.GREEN}✓ Found configuration in environment variables{Colors.ENDC}")
            print(f"  API URL: {api_url}")
            print(f"  Model: {model or 'gpt-4'}")
            use_env = input(f"{Colors.CYAN}Use this configuration? (Y/n): {Colors.ENDC}").strip().lower()
            if use_env != 'n':
                model = model or "gpt-4"
            else:
                api_url = None

        if not api_url:
            api_url = input(f"{Colors.CYAN}API URL: {Colors.ENDC}").strip()
            if not api_url:
                api_url = "https://api.metaihub.cn/v1/chat/completions"
                print(f"{Colors.YELLOW}Using default: {api_url}{Colors.ENDC}")
            
            api_key = input(f"{Colors.CYAN}API Key: {Colors.ENDC}").strip()
            model = input(f"{Colors.CYAN}Model (default: gpt-4o-mini): {Colors.ENDC}").strip() or "gpt-4o-mini"

        # Test connection
        print(f"\n{Colors.YELLOW}🔄 Testing connection...{Colors.ENDC}")
        try:
            self.llm_client = LLMClient(
                api_url=api_url,
                api_key=api_key,
                model=model,
                api_type="openai"
            )

            # Simple test
            test_response = self.llm_client.chat([
                {"role": "user", "content": "Hello, respond with just 'OK'"}
            ], max_tokens=10)

            if test_response.get("success"):
                print(f"{Colors.GREEN}✅ Connection successful!{Colors.ENDC}")
                print(f"   Model: {model}")
                
                # Initialize tool generator
                self.tool_generator = ToolGenerator(self.llm_client)
                
                return True
            else:
                print(f"{Colors.RED}❌ Connection failed: {test_response.get('error')}{Colors.ENDC}")
                return False

        except Exception as e:
            print(f"{Colors.RED}❌ Error: {e}{Colors.ENDC}")
            return False

    def load_all_tools(self):
        """Load all available tools."""
        print(f"\n{Colors.YELLOW}🔄 Loading tools...{Colors.ENDC}")
        
        # Load base tools
        self.base_tools = get_base_tools()
        print(f"{Colors.GREEN}✅ Loaded {len(self.base_tools)} built-in tools{Colors.ENDC}")
        
        # Load custom tools
        try:
            custom_tool_data = self.tool_storage.load_tools()
            for tool_data in custom_tool_data:
                try:
                    tool = self.dynamic_loader.create_tool_from_metadata(tool_data)
                    if tool:
                        self.custom_tools.append(tool)
                except Exception as e:
                    print(f"{Colors.YELLOW}⚠️  Failed to load custom tool: {e}{Colors.ENDC}")
            print(f"{Colors.GREEN}✅ Loaded {len(self.custom_tools)} custom tools{Colors.ENDC}")
        except:
            pass
        
        # Load AI-generated tools
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            gen_dir = os.path.join(current_dir, "tools_data", "generated_metadata")
            if os.path.exists(gen_dir):
                for filename in os.listdir(gen_dir):
                    if filename.endswith('.json'):
                        filepath = os.path.join(gen_dir, filename)
                        try:
                            with open(filepath, 'r', encoding='utf-8') as f:
                                tool_data = json.load(f)
                                tool = self.dynamic_loader.create_tool_from_metadata(tool_data)
                                if tool:
                                    self.generated_tools.append(tool)
                        except Exception as e:
                            print(f"{Colors.YELLOW}⚠️  Failed to load generated tool {filename}: {e}{Colors.ENDC}")
                print(f"{Colors.GREEN}✅ Loaded {len(self.generated_tools)} AI-generated tools{Colors.ENDC}")
        except:
            pass

    def llm_configuration_menu(self):
        """LLM configuration submenu."""
        while True:
            print(f"\n{Colors.BOLD}{'='*65}")
            print(f"🔧 LLM Configuration Menu")
            print(f"{'='*65}{Colors.ENDC}")
            print("1. 🔄 Reconfigure LLM")
            print("2. ℹ️  View Current Config")
            print("3. 🧪 Test Connection")
            print("0. ⬅️  Back to Main Menu")
            print(f"{Colors.BOLD}{'='*65}{Colors.ENDC}")
            
            choice = input(f"\n{Colors.CYAN}👉 Select option: {Colors.ENDC}").strip()
            
            if choice == "1":
                self.setup_llm()
            elif choice == "2":
                self.view_llm_config()
            elif choice == "3":
                self.test_llm_connection()
            elif choice == "0":
                break

    def view_llm_config(self):
        """View current LLM configuration."""
        if not self.llm_client:
            print(f"{Colors.RED}❌ No LLM client configured{Colors.ENDC}")
            return
        
        print(f"\n{Colors.BOLD}ℹ️  Current LLM Configuration:{Colors.ENDC}")
        print(f"  • API URL: {self.llm_client.api_url}")
        print(f"  • Model: {self.llm_client.model}")
        print(f"  • API Type: {self.llm_client.api_type}")
        print(f"  • Timeout: {self.llm_client.timeout}s")
        print(f"  • Requests Made: {self.llm_client.request_count}")
        print(f"  • Total Tokens: {self.llm_client.total_tokens}")

    def test_llm_connection(self):
        """Test LLM connection."""
        if not self.llm_client:
            print(f"{Colors.RED}❌ No LLM client configured{Colors.ENDC}")
            return
        
        print(f"\n{Colors.YELLOW}🧪 Testing connection...{Colors.ENDC}")
        try:
            response = self.llm_client.chat([
                {"role": "user", "content": "Say 'Test successful' in Chinese"}
            ], max_tokens=20)
            
            if response.get("success"):
                print(f"{Colors.GREEN}✅ Test successful!{Colors.ENDC}")
                print(f"   Response: {response['content']}")
            else:
                print(f"{Colors.RED}❌ Test failed: {response.get('error')}{Colors.ENDC}")
        except Exception as e:
            print(f"{Colors.RED}❌ Error: {e}{Colors.ENDC}")

    def tool_management_menu(self):
        """Tool management submenu."""
        while True:
            total_tools = len(self.base_tools) + len(self.custom_tools) + len(self.generated_tools)
            
            print(f"\n{Colors.BOLD}{'='*65}")
            print(f"🛠️  Tool Management Menu")
            print(f"{'='*65}{Colors.ENDC}")
            print(f"{Colors.GREEN}📊 Built-in Tools: {len(self.base_tools)}{Colors.ENDC}")
            print(f"{Colors.BLUE}📝 Custom Tools: {len(self.custom_tools)}{Colors.ENDC}")
            print(f"{Colors.YELLOW}🤖 AI-Generated Tools: {len(self.generated_tools)}{Colors.ENDC}")
            print(f"{Colors.CYAN}📈 Total Tools: {total_tools}{Colors.ENDC}")
            print(f"{Colors.BOLD}{'='*65}{Colors.ENDC}")
            print("1. 📋 List All Tools")
            print("2. 🔍 View Tool Details")
            print("3. 🤖 Generate New Tool (AI)")
            print("4. ➕ Add Custom Tool")
            print("5. 🗑️  Delete Tool")
            print("6. 🔄 Reload Tools")
            print("0. ⬅️  Back to Main Menu")
            print(f"{Colors.BOLD}{'='*65}{Colors.ENDC}")
            
            choice = input(f"\n{Colors.CYAN}👉 Select option: {Colors.ENDC}").strip()
            
            if choice == "1":
                self.list_all_tools()
            elif choice == "2":
                self.view_tool_details()
            elif choice == "3":
                self.generate_tool_interactive()
            elif choice == "4":
                self.add_custom_tool()
            elif choice == "5":
                self.delete_tool()
            elif choice == "6":
                self.load_all_tools()
            elif choice == "0":
                break

    def list_all_tools(self):
        """List all available tools."""
        print(f"\n{Colors.BOLD}📋 All Available Tools{Colors.ENDC}")
        print("=" * 65)
        
        if self.base_tools:
            print(f"\n{Colors.GREEN}🔧 Built-in Tools ({len(self.base_tools)}):{Colors.ENDC}")
            for i, tool in enumerate(self.base_tools, 1):
                print(f"  {i}. {tool.name}")
                print(f"     {tool.description[:60]}...")
        
        if self.custom_tools:
            print(f"\n{Colors.BLUE}📝 Custom Tools ({len(self.custom_tools)}):{Colors.ENDC}")
            for i, tool in enumerate(self.custom_tools, 1):
                print(f"  {i}. {tool.name}")
                print(f"     {tool.description[:60]}...")
        
        if self.generated_tools:
            print(f"\n{Colors.YELLOW}🤖 AI-Generated Tools ({len(self.generated_tools)}):{Colors.ENDC}")
            for i, tool in enumerate(self.generated_tools, 1):
                print(f"  {i}. {tool.name}")
                print(f"     {tool.description[:60]}...")

    def view_tool_details(self):
        """View detailed information about a specific tool."""
        all_tools = self.base_tools + self.custom_tools + self.generated_tools
        if not all_tools:
            print(f"{Colors.RED}❌ No tools available{Colors.ENDC}")
            return
        
        print(f"\n{Colors.BOLD}Available tools:{Colors.ENDC}")
        for i, tool in enumerate(all_tools, 1):
            print(f"{i}. {tool.name}")
        
        try:
            choice = int(input(f"\n{Colors.CYAN}Select tool number: {Colors.ENDC}").strip())
            if 1 <= choice <= len(all_tools):
                tool = all_tools[choice - 1]
                print(f"\n{Colors.BOLD}🛠️  Tool Details:{Colors.ENDC}")
                print(f"  • Name: {tool.name}")
                print(f"  • Description: {tool.description}")
                print(f"  • Parameters:")
                for param_name, param_info in tool.parameters.items():
                    print(f"    - {param_name} ({param_info.get('type', 'any')}): {param_info.get('description', '')}")
            else:
                print(f"{Colors.RED}❌ Invalid choice{Colors.ENDC}")
        except ValueError:
            print(f"{Colors.RED}❌ Invalid input{Colors.ENDC}")

    def generate_tool_interactive(self):
        """Interactive AI tool generation."""
        if not self.tool_generator:
            print(f"{Colors.RED}❌ Tool generator not initialized. Please configure LLM first.{Colors.ENDC}")
            return
        
        print(f"\n{Colors.BOLD}🤖 AI Tool Generation{Colors.ENDC}")
        print("=" * 65)
        
        tool_name = input(f"{Colors.CYAN}Tool name (e.g., WeatherFetcher): {Colors.ENDC}").strip()
        if not tool_name:
            print(f"{Colors.RED}❌ Tool name required{Colors.ENDC}")
            return

        description = input(f"{Colors.CYAN}Description: {Colors.ENDC}").strip()
        if not description:
            print(f"{Colors.RED}❌ Description required{Colors.ENDC}")
            return

        # Input parameters
        print(f"\n{Colors.YELLOW}📥 Input Parameters (press Enter on name to finish):{Colors.ENDC}")
        parameters = []
        i = 1
        while True:
            print(f"\nParameter {i}:")
            param_name = input(f"  Name: ").strip()
            if not param_name:
                break

            param_type = input(f"  Type (str/int/float/list/dict): ").strip() or "str"
            param_desc = input(f"  Description: ").strip()

            parameters.append({
                "name": param_name,
                "type": param_type,
                "description": param_desc
            })
            i += 1

        expected_output = input(f"\n{Colors.CYAN}📤 Expected output: {Colors.ENDC}").strip()
        impl_details = input(f"{Colors.CYAN}💡 Implementation hints (optional): {Colors.ENDC}").strip() or None

        # Generate
        print(f"\n{Colors.YELLOW}🔄 Generating tool with AI...{Colors.ENDC}")
        result = self.tool_generator.generate_tool(
            tool_name=tool_name,
            description=description,
            input_parameters=parameters,
            expected_output=expected_output,
            implementation_details=impl_details
        )

        if result.get("success"):
            print(f"\n{Colors.GREEN}✅ Tool generated successfully!{Colors.ENDC}")
            print(f"   File: {result.get('file_path', 'N/A')}")
            print(f"   Metadata: {result.get('metadata_path', 'N/A')}")
            
            # Reload tools
            self.load_all_tools()
        else:
            print(f"\n{Colors.RED}❌ Failed: {result.get('error')}{Colors.ENDC}")

    def add_custom_tool(self):
        """Add a custom tool manually."""
        print(f"\n{Colors.YELLOW}➕ Add Custom Tool (manual JSON definition){Colors.ENDC}")
        print("This feature allows you to add pre-written tool code.")
        print(f"{Colors.CYAN}Coming soon...{Colors.ENDC}")

    def delete_tool(self):
        """Delete a tool."""
        print(f"\n{Colors.YELLOW}🗑️  Delete Tool{Colors.ENDC}")
        print(f"{Colors.RED}Note: Only custom and AI-generated tools can be deleted.{Colors.ENDC}")
        
        deletable = self.custom_tools + self.generated_tools
        if not deletable:
            print(f"{Colors.RED}❌ No deletable tools available{Colors.ENDC}")
            return
        
        for i, tool in enumerate(deletable, 1):
            print(f"{i}. {tool.name}")
        
        try:
            choice = int(input(f"\n{Colors.CYAN}Select tool number to delete: {Colors.ENDC}").strip())
            if 1 <= choice <= len(deletable):
                tool = deletable[choice - 1]
                confirm = input(f"{Colors.RED}Delete '{tool.name}'? (yes/no): {Colors.ENDC}").strip().lower()
                if confirm == 'yes':
                    # TODO: Implement deletion
                    print(f"{Colors.YELLOW}Deletion functionality coming soon...{Colors.ENDC}")
            else:
                print(f"{Colors.RED}❌ Invalid choice{Colors.ENDC}")
        except ValueError:
            print(f"{Colors.RED}❌ Invalid input{Colors.ENDC}")

    def agent_management_menu(self):
        """Agent management submenu."""
        while True:
            saved_count = self.agent_storage.get_agent_count()
            
            print(f"\n{Colors.BOLD}{'='*65}")
            print(f"🤖 Agent Management Menu")
            print(f"{'='*65}{Colors.ENDC}")
            print(f"{Colors.GREEN}📊 Saved Agents: {saved_count}{Colors.ENDC}")
            print(f"{Colors.BOLD}{'='*65}{Colors.ENDC}")
            print("1. ➕ Create New Agent")
            print("2. 📋 List Saved Agents")
            print("3. 🔍 Load Agent")
            print("4. 🗑️  Delete Agent")
            print("5. ℹ️  View Current Agent")
            print("0. ⬅️  Back to Main Menu")
            print(f"{Colors.BOLD}{'='*65}{Colors.ENDC}")
            
            choice = input(f"\n{Colors.CYAN}👉 Select option: {Colors.ENDC}").strip()
            
            if choice == "1":
                self.create_agent_interactive()
            elif choice == "2":
                self.list_saved_agents()
            elif choice == "3":
                self.load_agent_interactive()
            elif choice == "4":
                self.delete_agent_interactive()
            elif choice == "5":
                self.view_current_agent()
            elif choice == "0":
                break

    def create_agent_interactive(self):
        """Interactive agent creation."""
        print(f"\n{Colors.BOLD}➕ Create New Agent{Colors.ENDC}")
        print("=" * 65)
        
        # Agent name
        agent_name = input(f"{Colors.CYAN}Agent name: {Colors.ENDC}").strip()
        if not agent_name:
            print(f"{Colors.RED}❌ Agent name required{Colors.ENDC}")
            return
        
        # Select role
        print(f"\n{Colors.YELLOW}📋 Available Roles:{Colors.ENDC}")
        roles = list(ROLE_TEMPLATES.keys())
        for i, role in enumerate(roles, 1):
            role_info = ROLE_TEMPLATES[role]
            print(f"{i}. {role} - {role_info.get('description', '')}")
        
        try:
            role_choice = int(input(f"\n{Colors.CYAN}Select role (1-{len(roles)}): {Colors.ENDC}").strip())
            if 1 <= role_choice <= len(roles):
                selected_role = roles[role_choice - 1]
            else:
                print(f"{Colors.RED}❌ Invalid choice{Colors.ENDC}")
                return
        except ValueError:
            print(f"{Colors.RED}❌ Invalid input{Colors.ENDC}")
            return
        
        # Enable ReAct?
        react_input = input(f"{Colors.CYAN}Enable ReAct reasoning? (Y/n): {Colors.ENDC}").strip().lower()
        use_react = react_input != 'n'
        
        # Custom instructions
        custom_inst = input(f"{Colors.CYAN}Custom instructions (optional): {Colors.ENDC}").strip() or None
        
        # Select tools
        all_tools = self.base_tools + self.custom_tools + self.generated_tools
        if not all_tools:
            print(f"{Colors.RED}❌ No tools available{Colors.ENDC}")
            return
        
        print(f"\n{Colors.YELLOW}🛠️  Available Tools:{Colors.ENDC}")
        for i, tool in enumerate(all_tools, 1):
            print(f"{i}. {tool.name} - {tool.description[:40]}...")
        
        tool_indices = input(f"\n{Colors.CYAN}Select tools (comma-separated numbers, or 'all'): {Colors.ENDC}").strip()
        
        if tool_indices.lower() == 'all':
            selected_tools = all_tools
        else:
            try:
                indices = [int(x.strip()) - 1 for x in tool_indices.split(',')]
                selected_tools = [all_tools[i] for i in indices if 0 <= i < len(all_tools)]
            except:
                print(f"{Colors.RED}❌ Invalid tool selection{Colors.ENDC}")
                return
        
        # Create agent
        print(f"\n{Colors.YELLOW}🔄 Creating agent...{Colors.ENDC}")
        try:
            self.current_agent = Agent(
                name=agent_name,
                llm_client=self.llm_client,
                tools=selected_tools,
                role=selected_role,
                use_react=use_react,
                custom_instructions=custom_inst
            )
            
            # Save agent
            self.agent_storage.save_agent(
                name=agent_name,
                tools=[t.name for t in selected_tools],
                role=selected_role,
                custom_instructions=custom_inst,
                use_react=use_react
            )
            
            print(f"{Colors.GREEN}✅ Agent '{agent_name}' created and saved!{Colors.ENDC}")
            print(f"   Role: {selected_role}")
            print(f"   ReAct: {use_react}")
            print(f"   Tools: {len(selected_tools)}")
        except Exception as e:
            print(f"{Colors.RED}❌ Error: {e}{Colors.ENDC}")

    def list_saved_agents(self):
        """List all saved agents."""
        agents = self.agent_storage.load_all_agents()
        if not agents:
            print(f"\n{Colors.YELLOW}No saved agents found.{Colors.ENDC}")
            return
        
        print(f"\n{Colors.BOLD}📋 Saved Agents ({len(agents)}):{Colors.ENDC}")
        print("=" * 65)
        for i, agent in enumerate(agents, 1):
            print(f"\n{i}. {Colors.BOLD}{agent['name']}{Colors.ENDC}")
            print(f"   Role: {agent.get('role', 'N/A')}")
            print(f"   ReAct: {agent.get('use_react', False)}")
            print(f"   Tools: {len(agent.get('tools', []))}")
            print(f"   Created: {agent.get('created_at', 'N/A')}")

    def load_agent_interactive(self):
        """Load a saved agent."""
        agents = self.agent_storage.load_all_agents()
        if not agents:
            print(f"\n{Colors.YELLOW}No saved agents found.{Colors.ENDC}")
            return
        
        print(f"\n{Colors.BOLD}📋 Available Agents:{Colors.ENDC}")
        for i, agent in enumerate(agents, 1):
            print(f"{i}. {agent['name']} ({agent.get('role', 'N/A')})")
        
        try:
            choice = int(input(f"\n{Colors.CYAN}Select agent number: {Colors.ENDC}").strip())
            if 1 <= choice <= len(agents):
                agent_data = agents[choice - 1]
                
                # Load tools
                all_tools = self.base_tools + self.custom_tools + self.generated_tools
                tool_names = agent_data.get('tools', [])
                selected_tools = [t for t in all_tools if t.name in tool_names]
                
                # Create agent
                self.current_agent = Agent(
                    name=agent_data['name'],
                    llm_client=self.llm_client,
                    tools=selected_tools,
                    role=agent_data.get('role', '通用助手'),
                    use_react=agent_data.get('use_react', True),
                    custom_instructions=agent_data.get('custom_instructions')
                )
                
                print(f"{Colors.GREEN}✅ Agent '{agent_data['name']}' loaded successfully!{Colors.ENDC}")
            else:
                print(f"{Colors.RED}❌ Invalid choice{Colors.ENDC}")
        except ValueError:
            print(f"{Colors.RED}❌ Invalid input{Colors.ENDC}")
        except Exception as e:
            print(f"{Colors.RED}❌ Error: {e}{Colors.ENDC}")

    def delete_agent_interactive(self):
        """Delete a saved agent."""
        agents = self.agent_storage.load_all_agents()
        if not agents:
            print(f"\n{Colors.YELLOW}No saved agents found.{Colors.ENDC}")
            return
        
        print(f"\n{Colors.BOLD}📋 Available Agents:{Colors.ENDC}")
        for i, agent in enumerate(agents, 1):
            print(f"{i}. {agent['name']}")
        
        try:
            choice = int(input(f"\n{Colors.CYAN}Select agent to delete: {Colors.ENDC}").strip())
            if 1 <= choice <= len(agents):
                agent_name = agents[choice - 1]['name']
                confirm = input(f"{Colors.RED}Delete '{agent_name}'? (yes/no): {Colors.ENDC}").strip().lower()
                if confirm == 'yes':
                    self.agent_storage.delete_agent(agent_name)
                    print(f"{Colors.GREEN}✅ Agent deleted{Colors.ENDC}")
            else:
                print(f"{Colors.RED}❌ Invalid choice{Colors.ENDC}")
        except ValueError:
            print(f"{Colors.RED}❌ Invalid input{Colors.ENDC}")

    def view_current_agent(self):
        """View current agent details."""
        if not self.current_agent:
            print(f"\n{Colors.YELLOW}No agent currently loaded.{Colors.ENDC}")
            return
        
        print(f"\n{Colors.BOLD}ℹ️  Current Agent:{Colors.ENDC}")
        print(f"  • Name: {self.current_agent.name}")
        print(f"  • Tools: {len(self.current_agent.tools)}")
        for tool in self.current_agent.tools:
            print(f"    - {tool.name}")
        print(f"  • Max Iterations: {self.current_agent.max_iterations}")
        print(f"  • Memory Enabled: {self.current_agent.memory_enabled}")

    def chat_with_agent(self):
        """Chat with the current agent using streaming output."""
        if not self.current_agent:
            print(f"\n{Colors.YELLOW}No agent loaded. Please create or load an agent first.{Colors.ENDC}")
            
            # Quick create option
            create = input(f"{Colors.CYAN}Create a quick agent now? (Y/n): {Colors.ENDC}").strip().lower()
            if create != 'n':
                self.create_quick_agent()
            else:
                return
        
        print(f"\n{Colors.BOLD}{'='*65}")
        print(f"💬 Chat with Agent: {self.current_agent.name}")
        print(f"{'='*65}{Colors.ENDC}")
        print(f"{Colors.YELLOW}Commands: /exit (quit), /clear (clear history), /info (agent info){Colors.ENDC}")
        print("=" * 65)
        
        while True:
            user_input = input(f"\n{Colors.CYAN}👤 You: {Colors.ENDC}").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['/exit', '/quit']:
                break
            elif user_input.lower() == '/clear':
                self.chat_history = []
                self.current_agent.conversation_history = []
                print(f"{Colors.GREEN}✅ Chat history cleared{Colors.ENDC}")
                continue
            elif user_input.lower() == '/info':
                self.view_current_agent()
                continue
            
            print(f"\n{Colors.GREEN}🤖 {self.current_agent.name}:{Colors.ENDC}\n")
            
            # Stream the response
            full_response = ""
            try:
                for event in self.current_agent.run_stream(user_input):
                    event_type = event.get("type")
                    content = event.get("content", "")
                    
                    if event_type == "iteration":
                        print(f"{Colors.BLUE}{content}{Colors.ENDC}")
                    elif event_type == "thought_start":
                        print(f"{Colors.YELLOW}{content}{Colors.ENDC}", end="", flush=True)
                    elif event_type == "thought_chunk":
                        print(content, end="", flush=True)
                        full_response += content
                    elif event_type == "thought_end":
                        print(content)
                    elif event_type == "thought":
                        print(f"{Colors.YELLOW}{content}{Colors.ENDC}")
                        full_response += content
                    elif event_type == "tool_call":
                        print(f"\n{Colors.CYAN}{content}{Colors.ENDC}")
                    elif event_type == "tool_result":
                        print(f"{Colors.GREEN}{content}{Colors.ENDC}")
                    elif event_type == "final_answer":
                        print(f"\n{Colors.BOLD}{Colors.GREEN}{content}{Colors.ENDC}")
                        full_response += content
                    elif event_type == "response":
                        print(content)
                        full_response = content
                    elif event_type == "error":
                        print(f"{Colors.RED}❌ Error: {content}{Colors.ENDC}")
                        full_response = f"Error: {content}"
                    elif event_type == "max_iterations":
                        print(f"{Colors.YELLOW}{content}{Colors.ENDC}")
                
                # Save to history
                self.chat_history.append({
                    "user": user_input,
                    "agent": full_response,
                    "timestamp": datetime.now().isoformat()
                })
            
            except Exception as e:
                print(f"{Colors.RED}❌ Error: {e}{Colors.ENDC}")

    def create_quick_agent(self):
        """Create a quick agent with default settings."""
        print(f"\n{Colors.YELLOW}🚀 Quick Agent Creation{Colors.ENDC}")
        
        agent_name = input(f"{Colors.CYAN}Agent name (default: QuickAgent): {Colors.ENDC}").strip() or "QuickAgent"
        
        # Use default settings
        all_tools = self.base_tools + self.custom_tools + self.generated_tools
        selected_tools = all_tools[:5] if len(all_tools) > 5 else all_tools
        
        self.current_agent = Agent(
            name=agent_name,
            llm_client=self.llm_client,
            tools=selected_tools,
            role="通用助手",
            use_react=True
        )
        
        print(f"{Colors.GREEN}✅ Quick agent created with {len(selected_tools)} tools!{Colors.ENDC}")

    def view_statistics(self):
        """View overall statistics."""
        print(f"\n{Colors.BOLD}{'='*65}")
        print(f"📊 System Statistics")
        print(f"{'='*65}{Colors.ENDC}")
        
        print(f"\n{Colors.GREEN}🛠️  Tools:{Colors.ENDC}")
        print(f"  • Built-in: {len(self.base_tools)}")
        print(f"  • Custom: {len(self.custom_tools)}")
        print(f"  • AI-Generated: {len(self.generated_tools)}")
        print(f"  • Total: {len(self.base_tools) + len(self.custom_tools) + len(self.generated_tools)}")
        
        print(f"\n{Colors.BLUE}🤖 Agents:{Colors.ENDC}")
        print(f"  • Saved: {self.agent_storage.get_agent_count()}")
        print(f"  • Current: {self.current_agent.name if self.current_agent else 'None'}")
        
        if self.llm_client:
            print(f"\n{Colors.YELLOW}🔧 LLM Client:{Colors.ENDC}")
            print(f"  • Model: {self.llm_client.model}")
            print(f"  • Requests: {self.llm_client.request_count}")
            print(f"  • Total Tokens: {self.llm_client.total_tokens}")
        
        print(f"\n{Colors.CYAN}💬 Chat:{Colors.ENDC}")
        print(f"  • Messages: {len(self.chat_history)}")


def main():
    """Main entry point."""
    cli = AgentCLI()
    try:
        cli.run()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}⚠️  Interrupted by user.{Colors.ENDC}")
        print(f"{Colors.GREEN}👋 Goodbye!{Colors.ENDC}\n")
    except Exception as e:
        print(f"\n{Colors.RED}❌ Fatal Error: {e}{Colors.ENDC}\n")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
