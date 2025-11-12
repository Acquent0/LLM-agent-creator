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
    
    # Load custom tools from storage
    tool_storage = st.session_state.get('tool_storage')
    if tool_storage:
        custom_tool_configs = tool_storage.load_all_tools()
        for tool_config in custom_tool_configs:
            tool = load_tool_from_config(tool_config)
            if tool:
                builtin_tools[f"Custom: {tool.name}"] = tool
    
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


def create_agent_interface():
    """Agent creation interface. / 智能体创建界面。"""
    st.header("🛠️ Create Agent | 创建智能体")

    col1, col2 = st.columns(2)

    with col1:
        agent_name = st.text_input(
            "Agent Name | 智能体名称",
            placeholder="e.g., ResearchAssistant"
        )

        system_prompt = st.text_area(
            "System Prompt | 系统提示 (Optional)",
            placeholder="You are a helpful research assistant..."
        )

    with col2:
        available_tools = get_available_tools()
        selected_tools = st.multiselect(
            "Select Tools | 选择工具",
            options=list(available_tools.keys()),
            default=["Calculator"]
        )

    if st.button("Create Agent | 创建智能体"):
        if not st.session_state.llm_client:
            st.error("Please connect to LLM first | 请先连接LLM")
            return

        if not agent_name:
            st.error("Please provide agent name | 请提供智能体名称")
            return

        tools = [available_tools[tool_name] for tool_name in selected_tools]

        agent = Agent(
            name=agent_name,
            llm_client=st.session_state.llm_client,
            tools=tools,
            system_prompt=system_prompt if system_prompt else None
        )

        st.session_state.agents[agent_name] = agent
        st.success(f"✅ Agent '{agent_name}' created | 智能体'{agent_name}'已创建")


def chat_interface():
    """Chat interface for agent interaction. / 智能体交互的聊天界面。"""
    st.header("💬 Chat with Agent | 与智能体对话")

    if not st.session_state.agents:
        st.info("Please create an agent first | 请先创建智能体")
        return

    selected_agent_name = st.selectbox(
        "Select Agent | 选择智能体",
        options=list(st.session_state.agents.keys())
    )

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
            with st.spinner("Thinking | 思考中..."):
                response = agent.run(user_input)
                st.write(response)

        st.session_state.chat_history.append({
            "role": "assistant",
            "content": response
        })


def tool_generator_interface():
    """Tool generation interface using LLM. / 使用LLM生成工具的界面。"""
    st.header("🛠️ Generate Custom Tool | 生成自定义工具")
    
    if not st.session_state.llm_client or not st.session_state.tool_generator:
        st.warning("⚠️ Please connect to LLM first | 请先连接LLM")
        return
    
    st.markdown("""
    Generate custom tools by describing what you need. The LLM will create Python code for your tool.
    通过描述需求来生成自定义工具。LLM将为您的工具创建Python代码。
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
    
    tool_storage = st.session_state.tool_storage
    
    # Display tool count
    tool_count = tool_storage.get_tool_count()
    st.metric("Custom Tools | 自定义工具数量", tool_count)
    
    st.markdown("---")
    
    # Tabs for different operations
    tab1, tab2, tab3, tab4 = st.tabs([
        "📝 Create Tool | 创建工具",
        "📋 View Tools | 查看工具",
        "✏️ Edit Tool | 编辑工具",
        "🗑️ Delete Tool | 删除工具"
    ])
    
    # Tab 1: Create Tool
    with tab1:
        st.subheader("Create New Tool | 创建新工具")
        
        col1, col2 = st.columns(2)
        
        with col1:
            new_tool_name = st.text_input(
                "Tool Name | 工具名称*",
                placeholder="e.g., WeatherAPI",
                key="new_tool_name"
            )
            
            new_tool_desc = st.text_area(
                "Tool Description | 工具描述*",
                placeholder="Describe what this tool does...",
                key="new_tool_desc",
                height=100
            )
        
        with col2:
            st.markdown("**Parameter Schema | 参数模式**")
            
            param_name = st.text_input(
                "Parameter Name | 参数名称",
                placeholder="e.g., location",
                key="param_name"
            )
            
            param_type = st.selectbox(
                "Parameter Type | 参数类型",
                ["string", "number", "integer", "boolean", "array", "object"],
                key="param_type"
            )
            
            param_required = st.checkbox("Required | 必需", key="param_required")
        
        st.markdown("**Tool Implementation | 工具实现 (Optional)**")
        st.markdown("Define custom Python code. Use `result` variable for the output.")
        st.markdown("定义自定义Python代码。使用 `result` 变量作为输出。")
        
        tool_code = st.text_area(
            "Python Code | Python代码",
            placeholder="""# Example:
# Access parameters as variables
# e.g., if parameter is 'location', use: location

result = f"Weather for {location}: Sunny, 25°C"
""",
            height=200,
            key="tool_code"
        )
        
        col_save, col_clear = st.columns([1, 1])
        
        with col_save:
            if st.button("💾 Save Tool | 保存工具", use_container_width=True):
                if not new_tool_name or not new_tool_desc:
                    st.error("Please provide tool name and description | 请提供工具名称和描述")
                else:
                    # Build parameter schema
                    parameters = {
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                    
                    if param_name:
                        parameters["properties"][param_name] = {
                            "type": param_type,
                            "description": f"Parameter {param_name}"
                        }
                        if param_required:
                            parameters["required"].append(param_name)
                    
                    # Create tool config
                    tool_config = {
                        "name": new_tool_name,
                        "description": new_tool_desc,
                        "parameters": parameters,
                        "code": tool_code if tool_code.strip() else None
                    }
                    
                    # Save tool
                    if tool_storage.save_tool(tool_config):
                        st.success(f"✅ Tool '{new_tool_name}' saved successfully!")
                        st.balloons()
                        # Force refresh
                        st.rerun()
                    else:
                        st.error("Failed to save tool | 保存工具失败")
        
        with col_clear:
            if st.button("🗑️ Clear Form | 清空表单", use_container_width=True):
                st.rerun()
    
    # Tab 2: View Tools
    with tab2:
        st.subheader("View All Tools | 查看所有工具")
        
        tools = tool_storage.load_all_tools()
        
        if not tools:
            st.info("No custom tools created yet | 还未创建自定义工具")
        else:
            for i, tool in enumerate(tools):
                with st.expander(f"🔧 {tool.get('name', 'Unnamed Tool')}"):
                    st.markdown(f"**Description | 描述:** {tool.get('description', 'No description')}")
                    
                    st.markdown("**Parameters | 参数:**")
                    params = tool.get('parameters', {}).get('properties', {})
                    required = tool.get('parameters', {}).get('required', [])
                    
                    if params:
                        for param_name, param_info in params.items():
                            req_mark = "✓" if param_name in required else ""
                            st.write(f"- `{param_name}` ({param_info.get('type', 'unknown')}) {req_mark}")
                    else:
                        st.write("No parameters")
                    
                    if tool.get('code'):
                        st.markdown("**Code | 代码:**")
                        st.code(tool.get('code'), language='python')
                    
                    # Export single tool
                    if st.button(f"📥 Export | 导出", key=f"export_{i}"):
                        export_path = os.path.join(tool_storage.storage_dir, f"{tool.get('name')}.json")
                        import json
                        with open(export_path, 'w', encoding='utf-8') as f:
                            json.dump(tool, f, indent=2, ensure_ascii=False)
                        st.success(f"Exported to {export_path}")
        
        # Export/Import all tools
        st.markdown("---")
        col_exp, col_imp = st.columns(2)
        
        with col_exp:
            if st.button("📦 Export All Tools | 导出所有工具"):
                export_path = os.path.join(tool_storage.storage_dir, "all_tools_export.json")
                if tool_storage.export_tools(export_path):
                    st.success(f"✅ Exported to {export_path}")
                else:
                    st.error("Export failed | 导出失败")
        
        with col_imp:
            uploaded_file = st.file_uploader(
                "Import Tools | 导入工具",
                type=['json'],
                key="import_tools"
            )
            if uploaded_file:
                import tempfile
                with tempfile.NamedTemporaryFile(delete=False, suffix='.json') as tmp:
                    tmp.write(uploaded_file.getvalue())
                    tmp_path = tmp.name
                
                if tool_storage.import_tools(tmp_path, merge=True):
                    st.success("✅ Tools imported successfully!")
                    os.unlink(tmp_path)
                    st.rerun()
                else:
                    st.error("Import failed | 导入失败")
                    os.unlink(tmp_path)
    
    # Tab 3: Edit Tool
    with tab3:
        st.subheader("Edit Tool | 编辑工具")
        
        tools = tool_storage.load_all_tools()
        
        if not tools:
            st.info("No tools to edit | 没有可编辑的工具")
        else:
            tool_names = [tool.get('name') for tool in tools]
            selected_tool_name = st.selectbox(
                "Select Tool to Edit | 选择要编辑的工具",
                tool_names,
                key="edit_tool_select"
            )
            
            if selected_tool_name:
                tool_config = tool_storage.get_tool(selected_tool_name)
                
                if tool_config:
                    st.markdown("---")
                    
                    edit_name = st.text_input(
                        "Tool Name | 工具名称",
                        value=tool_config.get('name', ''),
                        key="edit_name"
                    )
                    
                    edit_desc = st.text_area(
                        "Description | 描述",
                        value=tool_config.get('description', ''),
                        key="edit_desc",
                        height=100
                    )
                    
                    edit_code = st.text_area(
                        "Code | 代码",
                        value=tool_config.get('code', ''),
                        key="edit_code",
                        height=200
                    )
                    
                    if st.button("💾 Update Tool | 更新工具"):
                        # Delete old tool if name changed
                        if edit_name != selected_tool_name:
                            tool_storage.delete_tool(selected_tool_name)
                        
                        # Save updated tool
                        updated_config = {
                            "name": edit_name,
                            "description": edit_desc,
                            "parameters": tool_config.get('parameters', {}),
                            "code": edit_code if edit_code.strip() else None
                        }
                        
                        if tool_storage.save_tool(updated_config):
                            st.success("✅ Tool updated successfully!")
                            st.rerun()
                        else:
                            st.error("Failed to update tool | 更新工具失败")
    
    # Tab 4: Delete Tool
    with tab4:
        st.subheader("Delete Tool | 删除工具")
        
        tools = tool_storage.load_all_tools()
        
        if not tools:
            st.info("No tools to delete | 没有可删除的工具")
        else:
            tool_names = [tool.get('name') for tool in tools]
            selected_delete_tool = st.selectbox(
                "Select Tool to Delete | 选择要删除的工具",
                tool_names,
                key="delete_tool_select"
            )
            
            if selected_delete_tool:
                tool_config = tool_storage.get_tool(selected_delete_tool)
                
                if tool_config:
                    st.warning(f"⚠️ You are about to delete tool: **{selected_delete_tool}**")
                    st.json(tool_config)
                    
                    col_del, col_cancel = st.columns([1, 1])
                    
                    with col_del:
                        if st.button("🗑️ Confirm Delete | 确认删除", use_container_width=True):
                            if tool_storage.delete_tool(selected_delete_tool):
                                st.success(f"✅ Tool '{selected_delete_tool}' deleted!")
                                st.rerun()
                            else:
                                st.error("Failed to delete tool | 删除工具失败")
                    
                    with col_cancel:
                        if st.button("❌ Cancel | 取消", use_container_width=True):
                            st.rerun()
            
            st.markdown("---")
            st.markdown("### Danger Zone | 危险区域")
            
            if st.button("🗑️ Delete All Tools | 删除所有工具", type="secondary"):
                if st.checkbox("I understand this will delete all custom tools | 我了解这将删除所有自定义工具"):
                    if tool_storage.clear_all_tools():
                        st.success("✅ All tools deleted!")
                        st.rerun()
                    else:
                        st.error("Failed to delete tools | 删除工具失败")


def main():
    """Main application. / 主应用。"""
    init_session_state()

    setup_llm_client()

    st.sidebar.markdown("---")
    st.sidebar.header("📋 Navigation | 导航")

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

    [Documentation](https://github.com/yourusername/llm-agent-framework)
    """)


if __name__ == "__main__":
    main()
