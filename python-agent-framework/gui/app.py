"""
Streamlit GUI Application / Streamlit GUI应用

Interactive interface for the LLM Agent Framework.
LLM智能体框架的交互界面。

Author: LLM Agent Framework
License: MIT
"""

import streamlit as st
import sys
import os
from typing import List, Dict, Any

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.agent import Agent
from core.llm_client import LLMClient
from core.orchestrator import SequentialOrchestrator, ParallelOrchestrator
from tools.base_tools import CalculatorTool, FileIOTool, PythonREPLTool, TextProcessingTool
from tools.research_tools import ScientificComputeTool, StatisticalTestTool, UnitConverterTool
from tools.data_tools import DataAnalysisTool, VisualizationTool, DataCleaningTool
from utils.tool_storage import ToolStorageManager
from utils.agent_storage import AgentStorageManager
from utils.dynamic_tool import DynamicTool, load_tool_from_config
from utils.tool_generator import ToolGenerator
from utils.tool_indexer import ToolIndexer

from dotenv import load_dotenv
load_dotenv()


st.set_page_config(
    page_title="LLM Agent Framework",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 LLM Agent Framework")
st.markdown("### 科研LLM智能体框架 | Scientific Research LLM Agent Framework")


def init_session_state():
    """Initialize session state variables. / 初始化会话状态变量。"""
    if 'agents' not in st.session_state:
        st.session_state.agents = {}
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'llm_client' not in st.session_state:
        st.session_state.llm_client = None
    if 'tool_storage' not in st.session_state:
        st.session_state.tool_storage = ToolStorageManager()
    if 'agent_storage' not in st.session_state:
        st.session_state.agent_storage = AgentStorageManager()
    if 'tool_generator' not in st.session_state:
        st.session_state.tool_generator = None
    if 'tool_indexer' not in st.session_state:
        st.session_state.tool_indexer = ToolIndexer()
    if 'custom_tools' not in st.session_state:
        # Load custom tools from storage
        st.session_state.custom_tools = {}


def get_available_tools() -> Dict[str, Any]:
    """Get dictionary of available tools. / 获取可用工具字典。"""
    # Built-in tools
    builtin_tools = {
        "Calculator": CalculatorTool(),
        "File I/O": FileIOTool(),
        "Python REPL": PythonREPLTool(),
        "Text Processing": TextProcessingTool(),
        "Scientific Compute": ScientificComputeTool(),
        "Statistical Test": StatisticalTestTool(),
        "Unit Converter": UnitConverterTool(),
        "Data Analysis": DataAnalysisTool(),
        "Visualization": VisualizationTool(),
        "Data Cleaning": DataCleaningTool(),
    }
    
    # Load manually created custom tools from storage
    tool_storage = st.session_state.get('tool_storage')
    if tool_storage:
        custom_tool_configs = tool_storage.load_all_tools()
        for tool_config in custom_tool_configs:
            tool = load_tool_from_config(tool_config)
            if tool:
                builtin_tools[f"Custom: {tool.name}"] = tool
    
    # Load AI-generated tools from generated_metadata
    import json
    import os
    import sys
    from importlib import import_module
    
    # Get absolute path to parent directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    
    # Ensure the parent directory is in sys.path for imports
    if parent_dir not in sys.path:
        sys.path.insert(0, parent_dir)
    
    metadata_dir = os.path.join(parent_dir, "tools_data", "generated_metadata")
    
    if os.path.exists(metadata_dir):
        for filename in os.listdir(metadata_dir):
            if filename.endswith(".json"):
                file_path = os.path.join(metadata_dir, filename)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        metadata = json.load(f)
                    
                    tool_name = metadata.get("name")
                    tool_file = metadata.get("file_path")
                    
                    if tool_file and os.path.exists(tool_file):
                        # Import the generated tool dynamically
                        # Convert file path to module path
                        # e.g., tools/generated/mathcalculator.py -> tools.generated.mathcalculator
                        rel_path = os.path.relpath(tool_file, parent_dir)
                        module_path = rel_path.replace(os.sep, '.').replace('.py', '')
                        
                        try:
                            module = import_module(module_path)
                            # Find the tool class (usually <ToolName>)
                            tool_class = getattr(module, tool_name, None)
                            if tool_class:
                                builtin_tools[f"Generated: {tool_name}"] = tool_class()
                        except Exception as e:
                            # If import fails, create a dynamic tool from metadata
                            tool_config = {
                                "name": tool_name,
                                "description": metadata.get("description", ""),
                                "parameters": {
                                    "type": "object",
                                    "properties": {},
                                    "required": []
                                }
                            }
                            # Build parameters from metadata
                            for param in metadata.get("input_parameters", []):
                                param_name = param.get("name")
                                param_type = param.get("type", "string")
                                # Convert Python types to JSON schema types
                                if param_type in ["str", "string"]:
                                    json_type = "string"
                                elif param_type in ["int", "integer"]:
                                    json_type = "integer"
                                elif param_type in ["float", "number"]:
                                    json_type = "number"
                                elif param_type in ["bool", "boolean"]:
                                    json_type = "boolean"
                                else:
                                    json_type = "string"
                                
                                tool_config["parameters"]["properties"][param_name] = {
                                    "type": json_type,
                                    "description": param.get("description", "")
                                }
                                tool_config["parameters"]["required"].append(param_name)
                            
                            # Try to read the code from file
                            if tool_file and os.path.exists(tool_file):
                                with open(tool_file, "r", encoding="utf-8") as f:
                                    tool_config["code"] = f.read()
                            
                            tool = load_tool_from_config(tool_config)
                            if tool:
                                builtin_tools[f"Generated: {tool_name}"] = tool
                except Exception as e:
                    print(f"Error loading generated tool {filename}: {e}")
                    continue
    
    return builtin_tools


def setup_llm_client():
    """Setup LLM client configuration. / 设置LLM客户端配置。"""
    st.sidebar.header("⚙️ LLM Configuration | LLM配置")

    api_url = st.sidebar.text_input(
        "API URL",
        value=os.getenv("LLM_API_URL", "https://api.openai.com/v1/chat/completions")
    )

    api_key = st.sidebar.text_input(
        "API Key",
        type="password",
        value=os.getenv("LLM_API_KEY", "")
    )

    model = st.sidebar.text_input(
        "Model",
        value=os.getenv("LLM_MODEL", "gpt-4")
    )

    api_type = st.sidebar.selectbox(
        "API Type",
        ["openai", "claude", "custom"]
    )

    if st.sidebar.button("Test Connection | 测试连接"):
        if api_url and api_key:
            with st.spinner("Testing connection... | 测试连接中..."):
                try:
                    # Create client
                    test_client = LLMClient(
                        api_url=api_url,
                        api_key=api_key,
                        model=model,
                        api_type=api_type
                    )
                    
                    # Simple test with minimal cost
                    test_response = test_client.chat(
                        messages=[{"role": "user", "content": "Hi"}],
                        max_tokens=5
                    )
                    
                    if test_response.get("success"):
                        st.session_state.llm_client = test_client
                        st.session_state.tool_generator = ToolGenerator(test_client)
                        st.sidebar.success("✅ Connected successfully! | 连接成功！")
                    else:
                        st.sidebar.error(f"❌ Connection failed: {test_response.get('error')}")
                        
                except Exception as e:
                    st.sidebar.error(f"❌ Error: {str(e)}")
        else:
            st.sidebar.error("Please provide API URL and Key | 请提供API URL和密钥")


def load_saved_agents():
    """Load all saved agents from storage into session."""
    if not st.session_state.llm_client:
        st.error("❌ 请先连接LLM才能加载智能体")
        return
    
    saved_agents = st.session_state.agent_storage.load_all_agents()
    available_tools = get_available_tools()
    loaded_count = 0
    
    for agent_config in saved_agents:
        agent_name = agent_config.get("name")
        tool_names = agent_config.get("tools", [])
        role = agent_config.get("role", "通用助手")
        custom_instructions = agent_config.get("custom_instructions") or agent_config.get("system_prompt")
        use_react = agent_config.get("use_react", True)
        
        # Get tool objects
        tools = []
        for tool_name in tool_names:
            if tool_name in available_tools:
                tools.append(available_tools[tool_name])
        
        # Create agent with new parameters
        agent = Agent(
            name=agent_name,
            llm_client=st.session_state.llm_client,
            tools=tools,
            role=role,
            system_prompt=custom_instructions,
            use_react=use_react
        )
        
        st.session_state.agents[agent_name] = agent
        loaded_count += 1
    
    if loaded_count > 0:
        st.success(f"✅ 成功加载 {loaded_count} 个智能体")
        st.rerun()
    else:
        st.info("📭 没有找到已保存的智能体")


def create_agent_interface():
    """Agent creation interface. / 智能体创建界面。"""
    st.header("🛠️ Create Agent | 创建智能体")
    
    # Add load saved agents button
    col_header1, col_header2 = st.columns([3, 1])
    with col_header2:
        if st.button("📂 加载已保存智能体", use_container_width=True):
            load_saved_agents()
    
    # Show saved agents count
    saved_count = st.session_state.agent_storage.get_agent_count()
    if saved_count > 0:
        st.info(f"💾 已保存 {saved_count} 个智能体配置")
    
    # Add helpful instructions
    with st.expander("ℹ️ 如何创建智能体？ | How to Create an Agent?", expanded=False):
        st.markdown("""
        ### 📖 创建步骤 | Steps:
        
        1. **命名智能体** - 给你的智能体起一个描述性的名字
           - 例如：`DataAnalyst`, `ResearchHelper`, `CodeReviewer`
        
        2. **选择工具** - 选择智能体可以使用的工具
           - 🧮 **Calculator** - 数学计算
           - 📁 **FileIO** - 文件读写
           - 🐍 **PythonREPL** - 执行Python代码
           - 📊 **DataAnalysis** - 数据分析
           - 🔬 **Scientific** - 科学计算
           - 更多工具可在"生成工具"页面创建！
        
        3. **系统提示（可选）** - 定义智能体的角色和行为
           - 例如：`你是一个专业的数据分析师，擅长统计分析和可视化`
        
        ### 💡 示例配置:
        - **名称**: `MathTeacher`
        - **工具**: `Calculator`, `PythonREPL`
        - **提示**: `你是一位耐心的数学老师，帮助学生理解数学概念`
        """)

    col1, col2 = st.columns(2)

    with col1:
        agent_name = st.text_input(
            "🏷️ 智能体名称 | Agent Name *",
            placeholder="例如: DataAnalyst, MathTeacher"
        )
        
        # Import role templates
        from core.prompts import ROLE_TEMPLATES
        
        role = st.selectbox(
            "🎭 角色类型 | Role Type *",
            options=list(ROLE_TEMPLATES.keys()),
            help="选择预设角色模板，自动配置专业的系统提示词"
        )
        
        # Show role description
        if role in ROLE_TEMPLATES:
            st.caption(f"💡 {ROLE_TEMPLATES[role]['description']}")
        
        # Advanced options
        with st.expander("⚙️ 高级选项 | Advanced Options"):
            use_react = st.checkbox(
                "使用ReAct推理模式",
                value=True,
                help="ReAct模式让智能体更有条理地思考和行动"
            )
            
            custom_instructions = st.text_area(
                "额外指令 (可选) | Custom Instructions",
                placeholder="在角色模板基础上添加额外要求...",
                height=100,
                help="这会补充到角色模板中，不需要重复基础要求"
            )

    with col2:
        available_tools = get_available_tools()
        selected_tools = st.multiselect(
            "🔧 选择工具 | Select Tools *",
            options=list(available_tools.keys()),
            default=["Calculator"],
            help="选择智能体可以使用的工具"
        )
        
        # Show tool count
        if selected_tools:
            st.info(f"已选择 {len(selected_tools)} 个工具")

    if st.button("✨ 创建智能体 | Create Agent", type="primary", use_container_width=True):
        if not st.session_state.llm_client:
            st.error("❌ 请先连接LLM | Please connect to LLM first")
            return

        if not agent_name:
            st.error("❌ 请提供智能体名称 | Please provide agent name")
            return
        
        if not selected_tools:
            st.error("❌ 请至少选择一个工具 | Please select at least one tool")
            return

        # Get tool objects
        tools = [available_tools[tool_name] for tool_name in selected_tools]

        # Create agent with role and custom instructions
        agent = Agent(
            name=agent_name,
            llm_client=st.session_state.llm_client,
            tools=tools,
            role=role,
            system_prompt=custom_instructions if custom_instructions else None,
            use_react=use_react
        )

        # Save to session
        st.session_state.agents[agent_name] = agent
        
        # Save configuration to file
        agent_config = {
            "name": agent_name,
            "tools": selected_tools,  # Save tool names, not objects
            "role": role,
            "custom_instructions": custom_instructions if custom_instructions else None,
            "use_react": use_react
        }
        st.session_state.agent_storage.save_agent(agent_config)
        
        st.success(f"✅ 智能体 '{agent_name}' 创建成功！| Agent '{agent_name}' created successfully!")
        st.info(f"🎭 角色: {ROLE_TEMPLATES[role]['name']}\n🔧 工具: {len(selected_tools)} 个\n🧠 推理模式: {'ReAct' if use_react else 'Simple'}")
        st.balloons()


def chat_interface():
    """Chat interface for agent interaction. / 智能体交互的聊天界面。"""
    st.header("💬 Chat with Agent | 与智能体对话")

    if not st.session_state.agents:
        st.warning("⚠️ 还没有智能体！| No agents created yet!")
        st.markdown("""
        ### 📝 如何开始：
        
        1. 点击左侧导航的 **"创建智能体 | Create Agent"**
        2. 配置智能体的名称、工具和系统提示
        3. 创建后返回这里开始对话
        
        ### 💡 提示：
        - 智能体会根据您选择的工具来完成任务
        - 例如：选择了Calculator工具，就可以让它做数学计算
        - 选择了FileIO工具，就可以让它读写文件
        """)
        return

    selected_agent_name = st.selectbox(
        "Select Agent | 选择智能体",
        options=list(st.session_state.agents.keys())
    )
    
    # Show agent info
    selected_agent = st.session_state.agents[selected_agent_name]
    with st.expander("ℹ️ 智能体信息 | Agent Info"):
        # Get tool names safely
        tool_names = []
        for tool in selected_agent.tools:
            if hasattr(tool, 'name'):
                tool_names.append(tool.name)
            elif isinstance(tool, str):
                tool_names.append(tool)
            else:
                tool_names.append(str(type(tool).__name__))
        
        st.markdown(f"""
        - **名称**: {selected_agent.name}
        - **工具**: {', '.join(tool_names)}
        - **系统提示**: {selected_agent.system_prompt or '(未设置)'}
        
        ### 💬 对话示例：
        - "帮我计算 123 * 456"
        - "分析这段数据的统计特征"
        - "执行这段Python代码：print('Hello')"
        """)

    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    user_input = st.chat_input("Enter your message | 输入消息...")

    if user_input:
        st.session_state.chat_history.append({
            "role": "user",
            "content": user_input
        })

        with st.chat_message("user"):
            st.write(user_input)

        agent = st.session_state.agents[selected_agent_name]

        with st.chat_message("assistant"):
            # Create containers for different parts
            iteration_container = st.container()
            thought_container = st.container()
            tool_container = st.container()
            final_container = st.container()
            
            full_response = ""
            current_thought = ""
            thought_placeholder = None
            
            # Stream the response
            for event in agent.run_stream(user_input):
                event_type = event.get("type")
                content = event.get("content", "")
                
                if event_type == "iteration":
                    with iteration_container:
                        st.markdown(f"**{content}**")
                    full_response += f"\n{content}\n"
                    
                elif event_type == "thought_start":
                    current_thought = content
                    with thought_container:
                        thought_placeholder = st.empty()
                        thought_placeholder.markdown(current_thought + "▌")
                    full_response += content
                    
                elif event_type == "thought_chunk":
                    current_thought += content
                    if thought_placeholder:
                        thought_placeholder.markdown(current_thought + "▌")
                    full_response += content
                    
                elif event_type == "thought_end":
                    current_thought += content
                    if thought_placeholder:
                        thought_placeholder.markdown(current_thought)
                    full_response += content
                    thought_placeholder = None
                    
                elif event_type == "thought":
                    with thought_container:
                        st.markdown(content)
                    full_response += content
                    
                elif event_type == "tool_call":
                    with tool_container:
                        st.markdown(content)
                    full_response += f"\n{content}"
                    
                elif event_type == "tool_result":
                    with tool_container:
                        st.markdown(content)
                    full_response += f"{content}\n"
                    
                elif event_type == "final_answer":
                    with final_container:
                        st.markdown(content)
                    full_response += content
                    
                elif event_type == "response":
                    st.markdown(content)
                    full_response = content
                    
                elif event_type == "error":
                    st.error(f"❌ 错误: {content}")
                    full_response = f"❌ 错误: {content}"
                    
                elif event_type == "max_iterations":
                    st.warning(content)
                    full_response += f"\n{content}"

        st.session_state.chat_history.append({
            "role": "assistant",
            "content": full_response
        })


def tool_generator_interface():
    """Tool generation interface using LLM. / 使用LLM生成工具的界面。"""
    st.header("🛠️ Generate Custom Tool | 生成自定义工具")
    
    if not st.session_state.llm_client or not st.session_state.tool_generator:
        st.warning("⚠️ Please connect to LLM first | 请先连接LLM")
        return
    
    # Add detailed instructions
    with st.expander("ℹ️ 什么是AI工具生成？| What is AI Tool Generation?", expanded=True):
        st.markdown("""
        ### 🤖 AI驱动的工具生成 | AI-Powered Tool Generation
        
        **这个功能会使用大模型（LLM）自动为您生成Python工具代码！**
        
        #### 📝 如何使用：
        
        1. **工具名称** - 给工具起个名字，如 `WeatherFetcher`, `EmailSender`
        
        2. **描述功能** - 详细说明工具要做什么
           - ✅ 好的描述: "获取指定城市的天气信息，包括温度、湿度和风速"
           - ❌ 差的描述: "天气工具"
        
        3. **定义参数** - 工具需要哪些输入？
           - 例如: `city` (城市名), `date` (日期), `api_key` (API密钥)
        
        4. **期望输出** - 工具应该返回什么？
           - 例如: "包含温度、湿度、天气状况的字典"
        
        5. **实现提示（可选）** - 给LLM一些实现建议
           - 例如: "使用requests库调用OpenWeather API"
        
        #### 💡 示例：生成一个文本翻译工具
        
        - **名称**: `TextTranslator`
        - **描述**: `将输入的文本从一种语言翻译成另一种语言`
        - **参数1**: 
          - 名称: `text` (类型: str)
          - 描述: `要翻译的文本内容`
        - **参数2**: 
          - 名称: `target_language` (类型: str)
          - 描述: `目标语言，如 'zh', 'en', 'ja'`
        - **期望输出**: `翻译后的文本字符串`
        - **实现提示**: `可以使用googletrans库或其他翻译API`
        
        #### ⚠️ 注意事项：
        - 🔴 **生成工具会消耗LLM tokens** - 通常每个工具消耗500-2000 tokens
        - ✅ 生成的代码会自动保存到 `tools/generated/` 文件夹
        - ✅ 工具会自动添加到可用工具列表，智能体可以直接使用
        - ✅ 您可以在生成后查看和修改代码
        """)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📝 Tool Specification | 工具规格")
        
        tool_name = st.text_input(
            "Tool Name | 工具名称 *",
            placeholder="e.g., WeatherFetcher, PDFParser",
            help="A descriptive name for your tool"
        )
        
        description = st.text_area(
            "Description | 描述 *",
            placeholder="What does this tool do? Be specific...",
            help="Describe what the tool does and its purpose",
            height=100
        )
        
        st.markdown("#### Input Parameters | 输入参数")
        st.caption("Define what inputs your tool needs")
        
        # Dynamic parameter input
        if 'param_count' not in st.session_state:
            st.session_state.param_count = 1
        
        parameters = []
        for i in range(st.session_state.param_count):
            with st.expander(f"Parameter {i+1}", expanded=True):
                pcol1, pcol2 = st.columns(2)
                with pcol1:
                    param_name = st.text_input(
                        "Name",
                        key=f"param_name_{i}",
                        placeholder="e.g., url, text, data"
                    )
                    param_type = st.selectbox(
                        "Type",
                        ["str", "int", "float", "list", "dict", "bool"],
                        key=f"param_type_{i}"
                    )
                with pcol2:
                    param_desc = st.text_area(
                        "Description",
                        key=f"param_desc_{i}",
                        placeholder="What is this parameter for?",
                        height=100
                    )
                
                if param_name and param_desc:
                    parameters.append({
                        "name": param_name,
                        "type": param_type,
                        "description": param_desc
                    })
        
        pcol1, pcol2 = st.columns(2)
        with pcol1:
            if st.button("➕ Add Parameter"):
                st.session_state.param_count += 1
                st.rerun()
        with pcol2:
            if st.session_state.param_count > 1:
                if st.button("➖ Remove Last"):
                    st.session_state.param_count -= 1
                    st.rerun()
        
        expected_output = st.text_area(
            "Expected Output | 期望输出 *",
            placeholder="Describe what the tool should return...",
            help="What kind of result should this tool produce?",
            height=80
        )
        
    with col2:
        st.subheader("⚙️ Advanced Options | 高级选项")
        
        implementation_details = st.text_area(
            "Implementation Hints | 实现提示",
            placeholder="Optional: Specific algorithms, methods to use...",
            help="Provide specific implementation guidance if needed",
            height=120
        )
        
        dependencies = st.text_input(
            "Dependencies | 依赖包",
            placeholder="e.g., requests, beautifulsoup4",
            help="Comma-separated list of required Python packages"
        )
        
        st.markdown("---")
        
        # Show existing generated tools
        st.markdown("### 📚 Generated Tools")
        if st.session_state.tool_generator:
            generated_tools = st.session_state.tool_generator.list_generated_tools()
            if generated_tools:
                for tool in generated_tools:
                    with st.expander(f"🔧 {tool['name']}"):
                        st.caption(tool['description'])
                        st.text(f"Created: {tool['created_at'][:19]}")
            else:
                st.info("No tools generated yet")
    
    st.markdown("---")
    
    # Generate button
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        if st.button("🚀 Generate Tool | 生成工具", type="primary", use_container_width=True):
            # Validation
            if not tool_name:
                st.error("❌ Please provide a tool name | 请提供工具名称")
                return
            
            if not description:
                st.error("❌ Please provide a description | 请提供描述")
                return
            
            if not parameters:
                st.error("❌ Please define at least one parameter | 请定义至少一个参数")
                return
            
            if not expected_output:
                st.error("❌ Please describe expected output | 请描述期望输出")
                return
            
            # Parse dependencies
            deps = None
            if dependencies:
                deps = [d.strip() for d in dependencies.split(",")]
            
            # Generate tool
            with st.spinner("🔄 Generating tool... This may take a moment | 生成工具中..."):
                result = st.session_state.tool_generator.generate_tool(
                    tool_name=tool_name,
                    description=description,
                    input_parameters=parameters,
                    expected_output=expected_output,
                    implementation_details=implementation_details if implementation_details else None,
                    dependencies=deps
                )
            
            if result.get("success"):
                st.success(f"✅ Tool '{tool_name}' generated successfully! | 工具'{tool_name}'生成成功！")
                
                st.markdown("### 📄 Generated Code | 生成的代码")
                st.code(result['code'], language='python')
                
                st.info(f"📁 Saved to: {result['file_path']}")
                
                # Refresh tool indexer
                st.session_state.tool_indexer.refresh_index()
                
                # Reset parameter count
                st.session_state.param_count = 1
                
            else:
                st.error(f"❌ Failed to generate tool: {result.get('error')}")
    
    with col2:
        if st.button("🔄 Reset Form | 重置表单", use_container_width=True):
            st.session_state.param_count = 1
            st.rerun()
    
    with col3:
        st.button("📚 View Tools | 查看工具", use_container_width=True)


def orchestrator_interface():
    """Multi-agent orchestration interface. / 多智能体编排界面。"""
    st.header("🎭 Multi-Agent Orchestration | 多智能体编排")

    if len(st.session_state.agents) < 2:
        st.info("Please create at least 2 agents | 请创建至少2个智能体")
        return

    orchestration_type = st.selectbox(
        "Orchestration Type | 编排类型",
        ["Sequential | 顺序", "Parallel | 并行"]
    )

    selected_agents = st.multiselect(
        "Select Agents | 选择智能体",
        options=list(st.session_state.agents.keys())
    )

    task = st.text_area(
        "Task Description | 任务描述",
        placeholder="Describe the task for the agents..."
    )

    if st.button("Run Orchestration | 运行编排"):
        if len(selected_agents) < 2:
            st.error("Please select at least 2 agents | 请选择至少2个智能体")
            return

        if not task:
            st.error("Please provide a task | 请提供任务")
            return

        agents = [st.session_state.agents[name] for name in selected_agents]

        with st.spinner("Running orchestration | 运行编排中..."):
            if "Sequential" in orchestration_type:
                orchestrator = SequentialOrchestrator(agents)
                result = orchestrator.run(task)
                st.success("Orchestration Complete | 编排完成")
                st.write("**Final Result | 最终结果:**")
                st.write(result)
            else:
                orchestrator = ParallelOrchestrator(agents)
                results = orchestrator.run(task)
                st.success("Orchestration Complete | 编排完成")
                st.write("**Results | 结果:**")
                for agent_name, result in results.items():
                    with st.expander(f"Agent: {agent_name}"):
                        st.write(result)


def analytics_interface():
    """Analytics and monitoring interface. / 分析和监控界面。"""
    st.header("📊 Analytics | 分析")

    if not st.session_state.agents:
        st.info("No agents created yet | 还未创建智能体")
        return

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Agents | 总智能体数", len(st.session_state.agents))

    with col2:
        st.metric("Total Messages | 总消息数", len(st.session_state.chat_history))

    with col3:
        if st.session_state.llm_client:
            stats = st.session_state.llm_client.get_stats()
            st.metric("API Requests | API请求数", stats.get("request_count", 0))

    st.subheader("Agent Details | 智能体详情")

    for agent_name, agent in st.session_state.agents.items():
        with st.expander(f"🤖 {agent_name}"):
            st.write(f"**Tools | 工具:** {', '.join(agent.tools.keys())}")
            st.write(f"**Memory Enabled | 记忆启用:** {agent.memory_enabled}")

            if st.button(f"Clear Memory | 清除记忆 ({agent_name})", key=f"clear_{agent_name}"):
                agent.clear_memory()
                st.success(f"Memory cleared for {agent_name}")

            if st.button(f"View Execution Log | 查看执行日志 ({agent_name})", key=f"log_{agent_name}"):
                log = agent.get_execution_log()
                if log:
                    st.json(log)
                else:
                    st.info("No execution log available")


def tool_management_interface():
    """Tool management interface for CRUD operations. / 工具管理界面，用于增删改查操作。"""
    st.header("🔧 Tool Management | 工具管理")
    
    # Add explanation at the top
    with st.expander("ℹ️ 什么是工具？| What are Tools?", expanded=False):
        st.markdown("""
        ### 工具说明 | Tool Overview
        
        **工具是智能体可以调用的功能模块**
        
        #### 📦 两种类型的工具：
        
        1. **内置工具 (Built-in Tools)** - 系统预装，无需创建
           - ✅ Calculator - 数学计算
           - ✅ FileIO - 文件读写
           - ✅ PythonREPL - 执行Python代码
           - ✅ DataAnalysis - 数据分析
           - 等等...共10个内置工具
        
        2. **自定义工具 (Custom Tools)** - 你创建的工具
           - 在"生成工具"页面用AI生成
           - 或在这里手动创建
        
        #### 💡 提示：
        - 创建智能体时可以选择任意工具组合
        - 内置工具开箱即用，无需配置
        - 自定义工具保存在 `tools_data/` 文件夹
        """)
    
    tool_storage = st.session_state.tool_storage
    
    # Count generated tools
    import json
    import os
    
    # Get the absolute path to the parent directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    metadata_dir = os.path.join(parent_dir, "tools_data", "generated_metadata")
    generated_count = 0
    
    if os.path.exists(metadata_dir):
        json_files = [f for f in os.listdir(metadata_dir) if f.endswith('.json')]
        generated_count = len(json_files)
    else:
        # Fallback: try current directory
        metadata_dir = os.path.join(current_dir, "..", "tools_data", "generated_metadata")
        metadata_dir = os.path.abspath(metadata_dir)
        if os.path.exists(metadata_dir):
            json_files = [f for f in os.listdir(metadata_dir) if f.endswith('.json')]
            generated_count = len(json_files)
    
    # Display tool statistics with better explanation
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🔧 内置工具 | Built-in", "10")
    with col2:
        custom_count = tool_storage.get_tool_count()
        st.metric("✍️ 手动创建 | Manual", custom_count)
    with col3:
        st.metric("🤖 AI生成 | Generated", generated_count)
    with col4:
        st.metric("📊 总计 | Total", 10 + custom_count + generated_count)
    
    st.markdown("---")
    
    # Tabs for different operations
    tab1, tab2, tab3, tab4 = st.tabs([
        "� 查看所有工具 | View All Tools",
        "� 创建工具 | Create Tool",
        "✏️ 编辑工具 | Edit Tool",
        "🗑️ 删除工具 | Delete Tool"
    ])
    
    # Tab 1: View All Tools (changed order - most useful first)
    with tab1:
        col_header, col_refresh = st.columns([4, 1])
        with col_header:
            st.subheader("📋 查看所有可用工具 | View All Available Tools")
        with col_refresh:
            if st.button("🔄 刷新", help="重新加载所有工具", use_container_width=True):
                st.cache_data.clear()
                st.rerun()
        
        # Section 1: Built-in Tools
        st.markdown("### 🔧 内置工具 (10个)")
        st.caption("系统预装，创建智能体时可直接选择使用 | Pre-installed, ready to use when creating agents")
        
        builtin_tools_list = [
            ("Calculator", "计算器", "执行数学计算和表达式求值"),
            ("File I/O", "文件读写", "读取和写入文件"),
            ("Python REPL", "Python执行器", "执行Python代码"),
            ("Text Processing", "文本处理", "处理和分析文本"),
            ("Scientific Compute", "科学计算", "科学和工程计算"),
            ("Statistical Test", "统计检验", "统计测试和分析"),
            ("Unit Converter", "单位转换", "转换各种单位"),
            ("Data Analysis", "数据分析", "分析和计算数据统计"),
            ("Visualization", "可视化", "创建图表和可视化"),
            ("Data Cleaning", "数据清洗", "清理和预处理数据"),
        ]
        
        for i, (name_en, name_cn, desc) in enumerate(builtin_tools_list):
            with st.expander(f"✅ {name_en} | {name_cn}"):
                st.markdown(f"**功能:** {desc}")
                st.markdown("**状态:** ✅ 可用")
                st.markdown("**使用:** 创建智能体时从工具列表选择")
        
        st.markdown("---")
        
        # Section 2: AI-Generated Tools
        st.markdown("### 🤖 AI生成的工具")
        st.caption("通过'生成工具'页面由AI自动创建的工具 | Tools automatically created by AI via 'Generate Tool' page")
        
        # Load generated tools metadata
        import json
        import os
        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(current_dir)
        metadata_dir = os.path.join(parent_dir, "tools_data", "generated_metadata")
        
        generated_tools = []
        if os.path.exists(metadata_dir):
            for filename in os.listdir(metadata_dir):
                if filename.endswith('.json'):
                    file_path = os.path.join(metadata_dir, filename)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            metadata = json.load(f)
                            generated_tools.append(metadata)
                    except Exception as e:
                        continue
        
        if not generated_tools:
            st.info("""
            💡 **还没有AI生成的工具**
            
            **如何创建:**
            1. 点击左侧导航的 **"生成工具 | Generate Tool"**
            2. 描述你需要的工具功能
            3. AI会自动生成完整的Python代码
            4. 生成后可在"创建智能体"时使用
            
            **优势:**
            - 自动编写代码，功能强大
            - 支持复杂逻辑
            - 包含错误处理
            """)
        else:
            for i, metadata in enumerate(generated_tools):
                tool_name = metadata.get('name', 'Unnamed')
                with st.expander(f"🤖 {tool_name}"):
                    st.markdown(f"**描述:** {metadata.get('description', '无描述')}")
                    st.markdown(f"**创建时间:** {metadata.get('created_at', 'Unknown')[:19]}")
                    
                    # Parameters
                    params = metadata.get('input_parameters', [])
                    if params:
                        st.markdown("**参数:**")
                        for param in params:
                            param_name = param.get('name')
                            param_type = param.get('type', 'unknown')
                            param_desc = param.get('description', '无描述')
                            st.write(f"- `{param_name}` ({param_type}): {param_desc}")
                    
                    # Expected output
                    if metadata.get('expected_output'):
                        st.markdown(f"**返回值:** {metadata['expected_output']}")
                    
                    # Dependencies
                    if metadata.get('dependencies'):
                        deps = ', '.join(metadata['dependencies'])
                        st.markdown(f"**依赖:** `{deps}`")
                    
                    # Code file
                    tool_file = metadata.get('file_path')
                    if tool_file and os.path.exists(tool_file):
                        with st.expander("查看代码"):
                            with open(tool_file, 'r', encoding='utf-8') as f:
                                code = f.read()
                            st.code(code, language='python')
        
        st.markdown("---")
        
        # Section 3: Manually Created Custom Tools
        st.markdown("### ✍️ 手动创建的工具")
        st.caption("通过工具管理手动添加的简单工具 | Simple tools manually added via tool management")
        
        custom_tools = tool_storage.load_all_tools()
        
        if not custom_tools:
            st.info("""
            💡 **还没有手动创建的工具**
            
            **创建方法:**
            - 在上方的"创建工具"标签页手动创建
            
            **区别:**
            - 手动创建：简单快速，适合基础工具，不消耗tokens
            - AI生成：功能强大，自动编写代码，但消耗tokens
            """)
        else:
            for i, tool in enumerate(custom_tools):
                with st.expander(f"⭐ {tool.get('name', 'Unnamed Tool')}"):
                    st.markdown(f"**描述:** {tool.get('description', '无描述')}")
                    
                    # Parameters
                    params = tool.get('parameters', {}).get('properties', {})
                    required = tool.get('parameters', {}).get('required', [])
                    
                    if params:
                        st.markdown("**参数:**")
                        for param_name, param_info in params.items():
                            req_mark = "✅ 必需" if param_name in required else "⭕ 可选"
                            st.write(f"- `{param_name}` ({param_info.get('type', 'unknown')}) - {req_mark}")
                    
                    # Code
                    if tool.get('code'):
                        with st.expander("查看代码"):
                            st.code(tool.get('code'), language='python')
    
    # Tab 2: Create Tool (manual creation)
    with tab2:
        st.subheader("✍️ 手动创建工具 | Manually Create Tool")
        
        st.warning("""
        ⚠️ **注意 | Note:** 
        
        - **这里是手动创建**简单工具（如简单的文本处理）
        - **如果需要AI自动生成代码**，请使用左侧导航的"生成工具 | Generate Tool"页面
        
        **区别:**
        - 🤖 AI生成：功能强大，自动编写代码，但消耗tokens
        - ✍️ 手动创建：简单快速，不消耗tokens，适合基础工具
        """)
        
        st.markdown("---")
        
        # Basic info
        tool_name = st.text_input(
            "🏷️ 工具名称 *",
            placeholder="例如: TextReverser",
            help="工具的唯一标识名称"
        )
        
        tool_desc = st.text_area(
            "📝 工具描述 *",
            placeholder="例如: 反转输入的文本字符串",
            help="说明这个工具的功能",
            height=80
        )
        
        st.markdown("---")
        st.markdown("### 📋 参数配置 | Parameters")
        st.caption("可以添加多个参数，每个参数需要指定名称、类型和是否必需")
        
        # Initialize session state for parameters
        if 'tool_params' not in st.session_state:
            st.session_state.tool_params = []
        
        # Display existing parameters
        if st.session_state.tool_params:
            st.markdown("**当前参数列表:**")
            for idx, param in enumerate(st.session_state.tool_params):
                col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
                with col1:
                    st.text(f"📌 {param['name']}")
                with col2:
                    st.text(f"类型: {param['type']}")
                with col3:
                    req_text = "✅ 必需" if param['required'] else "⭕ 可选"
                    st.text(req_text)
                with col4:
                    if st.button("🗑️", key=f"del_param_{idx}", help="删除此参数"):
                        st.session_state.tool_params.pop(idx)
                        st.rerun()
            st.markdown("---")
        
        # Add new parameter
        st.markdown("**添加新参数:**")
        col1, col2, col3 = st.columns([3, 2, 2])
        
        with col1:
            new_param_name = st.text_input(
                "参数名称",
                placeholder="例如: text",
                help="参数的变量名",
                key="new_param_name"
            )
        
        with col2:
            new_param_type = st.selectbox(
                "参数类型",
                ["string", "number", "integer", "boolean", "array"],
                key="new_param_type"
            )
        
        with col3:
            new_param_required = st.checkbox(
                "必需参数", 
                value=True,
                key="new_param_required"
            )
        
        if st.button("➕ 添加参数", use_container_width=True):
            if new_param_name:
                # Check for duplicate
                if any(p['name'] == new_param_name for p in st.session_state.tool_params):
                    st.error(f"❌ 参数 '{new_param_name}' 已存在")
                else:
                    st.session_state.tool_params.append({
                        'name': new_param_name,
                        'type': new_param_type,
                        'required': new_param_required
                    })
                    st.success(f"✅ 已添加参数: {new_param_name}")
                    st.rerun()
            else:
                st.error("❌ 请输入参数名称")
        
        st.markdown("---")
        st.markdown("**💻 Python代码实现 (可选)**")
        st.caption("可以直接使用参数名作为变量，使用 result 变量存储返回值")
        
        # Show example based on parameters
        if st.session_state.tool_params:
            param_names = ", ".join([p['name'] for p in st.session_state.tool_params])
            example_text = f"""# 示例: 可使用的参数变量: {param_names}
# 使用 result 变量存储返回值
result = {st.session_state.tool_params[0]['name']}[::-1]  # 示例"""
        else:
            example_text = """# 示例: 反转字符串
result = text[::-1]"""
        
        code_example = st.text_area(
            "代码",
            placeholder=example_text,
            height=150,
            help="编写Python代码实现工具功能"
        )
        
        st.markdown("---")
        
        # Save and reset buttons
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("💾 保存工具", type="primary", use_container_width=True):
                if not tool_name or not tool_desc:
                    st.error("❌ 请填写工具名称和描述")
                elif not st.session_state.tool_params:
                    st.error("❌ 请至少添加一个参数")
                else:
                    # Build parameters schema
                    params = {
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                    
                    for param in st.session_state.tool_params:
                        params["properties"][param['name']] = {
                            "type": param['type']
                        }
                        if param['required']:
                            params["required"].append(param['name'])
                    
                    config = {
                        "name": tool_name,
                        "description": tool_desc,
                        "parameters": params,
                        "code": code_example.strip() if code_example.strip() else None
                    }
                    
                    if tool_storage.save_tool(config):
                        st.success(f"✅ 工具 '{tool_name}' 保存成功！")
                        st.balloons()
                        # Clear parameters
                        st.session_state.tool_params = []
                        st.rerun()
                    else:
                        st.error("❌ 保存失败，工具名称可能已存在")
        
        with col_btn2:
            if st.button("🗑️ 清空重置", use_container_width=True):
                st.session_state.tool_params = []
                st.rerun()
    
    # Tab 3: Edit Tool
    with tab3:
        st.subheader("✏️ 编辑工具 | Edit Tool")
        
        st.caption("只能编辑自定义工具，内置工具无法修改 | Only custom tools can be edited")
        
        tools = tool_storage.load_all_tools()
        
        if not tools:
            st.info("📭 还没有自定义工具可以编辑\n\n请先创建或生成工具")
        else:
            tool_names = [tool.get('name') for tool in tools]
            selected = st.selectbox(
                "选择要编辑的工具",
                tool_names,
                key="edit_select"
            )
            
            if selected:
                tool = tool_storage.get_tool(selected)
                
                if tool:
                    st.markdown("---")
                    
                    new_name = st.text_input("工具名称", value=tool.get('name', ''))
                    new_desc = st.text_area("描述", value=tool.get('description', ''), height=80)
                    new_code = st.text_area("代码", value=tool.get('code', ''), height=200)
                    
                    if st.button("💾 保存修改", type="primary"):
                        if new_name != selected:
                            tool_storage.delete_tool(selected)
                        
                        updated = {
                            "name": new_name,
                            "description": new_desc,
                            "parameters": tool.get('parameters', {}),
                            "code": new_code.strip() or None
                        }
                        
                        if tool_storage.save_tool(updated):
                            st.success("✅ 更新成功！")
                            st.rerun()
                        else:
                            st.error("❌ 更新失败")
    
    # Tab 4: Delete Tool
    with tab4:
        st.subheader("🗑️ 删除工具 | Delete Tool")
        
        st.caption("只能删除自定义工具，内置工具无法删除 | Only custom tools can be deleted")
        
        tools = tool_storage.load_all_tools()
        
        if not tools:
            st.info("📭 没有可删除的工具")
        else:
            st.warning("⚠️ 删除操作不可恢复，请谨慎操作")
            
            tool_names = [tool.get('name') for tool in tools]
            selected = st.selectbox("选择要删除的工具", tool_names)
            
            if selected:
                tool = tool_storage.get_tool(selected)
                
                if tool:
                    with st.expander("📄 工具信息", expanded=True):
                        st.markdown(f"**名称:** {tool.get('name')}")
                        st.markdown(f"**描述:** {tool.get('description')}")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("🗑️ 确认删除", type="primary", use_container_width=True):
                            if tool_storage.delete_tool(selected):
                                st.success(f"✅ 已删除 '{selected}'")
                                st.rerun()
                            else:
                                st.error("❌ 删除失败")
                    
                    with col2:
                        if st.button("❌ 取消", use_container_width=True):
                            st.rerun()
            
            st.markdown("---")
            st.markdown("### ⚠️ 危险操作")
            
            with st.expander("删除所有自定义工具"):
                st.error("这将删除所有自定义工具，此操作不可恢复！")
                confirm = st.checkbox("我明白此操作的后果")
                if confirm and st.button("🗑️ 删除全部"):
                    if tool_storage.clear_all_tools():
                        st.success("✅ 已删除所有工具")
                        st.rerun()
                    else:
                        st.error("❌ 操作失败")


def main():
    """Main application. / 主应用。"""
    init_session_state()

    setup_llm_client()

    st.sidebar.markdown("---")
    st.sidebar.header("📋 Navigation | 导航")
    
    # Add quick start guide in sidebar
    with st.sidebar.expander("🚀 快速开始 | Quick Start"):
        st.markdown("""
        ### 使用步骤：
        
        **1️⃣ 配置LLM**
        - 在左侧输入API信息
        - 点击"测试连接"
        
        **2️⃣ 创建智能体**
        - 进入"创建智能体"页面
        - 选择工具，命名智能体
        
        **3️⃣ 开始对话**
        - 进入"对话"页面
        - 与智能体交互
        
        **💡 高级功能：**
        - 生成工具：用AI创建自定义工具
        - 编排：多智能体协作
        """)

    page = st.sidebar.radio(
        "Select Page | 选择页面",
        ["Create Agent | 创建智能体",
         "Chat | 对话",
         "Generate Tool | 生成工具",
         "Orchestration | 编排",
         "Analytics | 分析",
         "Tool Management | 工具管理"]
    )

    st.sidebar.markdown("---")

    if st.sidebar.button("Clear All | 清除所有"):
        st.session_state.agents = {}
        st.session_state.chat_history = []
        st.success("All data cleared | 所有数据已清除")

    if "Create" in page:
        create_agent_interface()
    elif "Chat" in page:
        chat_interface()
    elif "Generate Tool" in page:
        tool_generator_interface()
    elif "Orchestration" in page:
        orchestrator_interface()
    elif "Analytics" in page:
        analytics_interface()
    elif "Tool Management" in page:
        tool_management_interface()

    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    **LLM Agent Framework**

    Version: 1.0.0

    [Documentation](https://github.com/Acquent0/llm-agent-framework)
    """)


if __name__ == "__main__":
    main()
