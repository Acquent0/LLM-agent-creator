"""
Agent Base Class / 智能体基类

This module defines the core Agent class that orchestrates LLM interactions
and tool usage.
此模块定义了协调LLM交互和工具使用的核心Agent类。

Author: LLM Agent Framework
License: MIT
"""

import json
import re
from typing import Dict, Any, List, Optional
from datetime import datetime

from .llm_client import LLMClient
from .tool import Tool

# Import prompt templates
try:
    from .prompts import get_system_prompt, format_tools_description, ROLE_TEMPLATES
except ImportError:
    # Fallback if prompts module doesn't exist
    ROLE_TEMPLATES = {}
    def get_system_prompt(*args, **kwargs):
        return ""
    def format_tools_description(tools):
        return ""


class Agent:
    """
    Core agent class that combines LLM and tools to execute tasks.
    结合LLM和工具执行任务的核心智能体类。

    An agent maintains conversation history, manages tools, and implements
    the reasoning loop for tool usage.
    智能体维护对话历史、管理工具，并实现工具使用的推理循环。

    Attributes:
        name (str): Agent name / 智能体名称
        llm_client (LLMClient): LLM client for API calls / 用于API调用的LLM客户端
        tools (List[Tool]): Available tools / 可用工具
        system_prompt (str): System prompt for the agent / 智能体的系统提示
        memory_enabled (bool): Whether to maintain conversation history / 是否维护对话历史
    """

    def __init__(
        self,
        name: str,
        llm_client: LLMClient,
        tools: Optional[List[Tool]] = None,
        system_prompt: Optional[str] = None,
        role: str = "通用助手",
        memory_enabled: bool = True,
        max_memory_tokens: int = 4000,
        max_iterations: int = 10,
        use_react: bool = True
    ):
        """
        Initialize the Agent.
        初始化智能体。

        Args:
            name: Agent name / 智能体名称
            llm_client: LLM client instance / LLM客户端实例
            tools: List of available tools / 可用工具列表
            system_prompt: Custom system prompt (will be added to role template) / 自定义系统提示（将添加到角色模板）
            role: Agent role type (通用助手/数据分析师/数学老师/etc.) / 智能体角色类型
            memory_enabled: Enable conversation memory / 启用对话记忆
            max_memory_tokens: Max tokens for memory / 记忆的最大令牌数
            max_iterations: Max reasoning iterations / 最大推理迭代次数
            use_react: Use ReAct reasoning template / 使用ReAct推理模板
        """
        self.name = name
        self.llm_client = llm_client
        self.tools = {tool.name: tool for tool in (tools or [])}
        self.role = role
        self.use_react = use_react
        self.custom_instructions = system_prompt or ""
        
        # Generate system prompt using template
        tools_list = list(self.tools.values())
        if tools_list and 'get_system_prompt' in globals():
            tools_desc = format_tools_description(tools_list)
            self.system_prompt = get_system_prompt(
                tools_description=tools_desc,
                role=role,
                custom_instructions=self.custom_instructions,
                use_react=use_react
            )
        else:
            self.system_prompt = self._default_system_prompt()
        
        self.memory_enabled = memory_enabled
        self.max_memory_tokens = max_memory_tokens
        self.max_iterations = max_iterations

        self.conversation_history: List[Dict[str, str]] = []
        self.execution_log: List[Dict[str, Any]] = []

    def _default_system_prompt(self) -> str:
        """
        Generate default system prompt with tool descriptions.
        生成包含工具描述的默认系统提示。

        Returns:
            System prompt string / 系统提示字符串
        """
        base_prompt = f"""You are {self.name}, a helpful AI assistant.

You have access to the following tools:
"""

        if self.tools:
            for tool_name, tool in self.tools.items():
                base_prompt += f"\n- {tool_name}: {tool.description}"

            base_prompt += """

To use a tool, respond with a JSON object in this format:
```json
{
    "tool": "tool_name",
    "parameters": {
        "param1": "value1",
        "param2": "value2"
    }
}
```

After receiving tool results, continue the conversation or use another tool if needed.
If you don't need any tools, respond normally to the user.
"""
        else:
            base_prompt += "\nNo tools available. Respond based on your knowledge."

        return base_prompt

    def run_stream(
        self,
        task: str,
        context: Optional[Dict[str, Any]] = None,
        callback=None
    ):
        """
        Execute a task using the agent with streaming output.
        使用智能体执行任务并流式输出。
        
        This method yields updates as they happen, allowing for real-time display.
        此方法在更新发生时产生它们，允许实时显示。
        
        Args:
            task: Task description / 任务描述
            context: Additional context / 额外上下文
            callback: Optional callback function(event_type, content) / 可选的回调函数
            
        Yields:
            Dict with event type and content / 包含事件类型和内容的字典
        """
        messages = self._prepare_messages(task, context)
        
        iteration = 0
        while iteration < self.max_iterations:
            iteration += 1
            
            yield {
                "type": "iteration",
                "iteration": iteration,
                "content": f"🔄 第 {iteration} 轮推理..."
            }
            
            # Stream LLM response
            response = self.llm_client.chat(messages, stream=True)
            
            if not response.get("success"):
                error_msg = f"LLM API error: {response.get('error')}"
                yield {"type": "error", "content": error_msg}
                return
            
            # Collect streaming content
            full_content = ""
            if response.get("stream"):
                yield {"type": "thought_start", "content": "💭 思考中: "}
                for chunk in self.llm_client.parse_stream(response["response"]):
                    full_content += chunk
                    yield {"type": "thought_chunk", "content": chunk}
                yield {"type": "thought_end", "content": "\n"}
            else:
                full_content = response["content"]
                yield {"type": "thought", "content": f"💭 思考: {full_content}\n"}
            
            self._log_execution("llm_response", full_content)
            
            # Try to extract final_answer first
            final_answer = self._extract_final_answer(full_content)
            if final_answer:
                if self.memory_enabled:
                    self.conversation_history.append({
                        "role": "user",
                        "content": task
                    })
                    self.conversation_history.append({
                        "role": "assistant",
                        "content": final_answer
                    })
                
                yield {"type": "final_answer", "content": f"\n✅ 最终答案: {final_answer}"}
                return
            
            # Try to parse tool call
            tool_call = self._parse_tool_call(full_content)
            
            if tool_call:
                # Show tool execution
                tool_name = tool_call.get("tool", "unknown")
                params = tool_call.get("parameters", {})
                
                yield {
                    "type": "tool_call",
                    "content": f"🛠️  调用工具: {tool_name}\n   参数: {json.dumps(params, ensure_ascii=False)}\n"
                }
                
                # Execute the tool
                tool_result = self._execute_tool(tool_call)
                
                yield {
                    "type": "tool_result",
                    "content": f"📊 工具结果: {json.dumps(tool_result, ensure_ascii=False)}\n"
                }
                
                # Add to messages
                messages.append({
                    "role": "assistant",
                    "content": full_content
                })
                
                observation = f"Observation: {json.dumps(tool_result, ensure_ascii=False)}"
                messages.append({
                    "role": "user",
                    "content": observation
                })
                
                if self.memory_enabled:
                    self.conversation_history.extend([
                        {"role": "assistant", "content": full_content},
                        {"role": "user", "content": observation}
                    ])
            else:
                # No tool call and no final_answer
                if self.memory_enabled:
                    self.conversation_history.append({
                        "role": "user",
                        "content": task
                    })
                    self.conversation_history.append({
                        "role": "assistant",
                        "content": full_content
                    })
                
                yield {"type": "response", "content": full_content}
                return
        
        yield {"type": "max_iterations", "content": "⚠️ 达到最大迭代次数"}

    def run(
        self,
        task: str,
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Execute a task using the agent.
        使用智能体执行任务。

        This is the main entry point for agent execution. It handles the
        reasoning loop, tool calling, and response generation.
        这是智能体执行的主要入口点。它处理推理循环、工具调用和响应生成。

        Args:
            task: Task description / 任务描述
            context: Additional context / 额外上下文

        Returns:
            Final response string / 最终响应字符串
        """
        messages = self._prepare_messages(task, context)

        iteration = 0
        while iteration < self.max_iterations:
            iteration += 1

            response = self.llm_client.chat(messages)

            if not response.get("success"):
                error_msg = f"LLM API error: {response.get('error')}"
                self._log_execution("error", error_msg)
                return error_msg

            content = response["content"]
            self._log_execution("llm_response", content)
            
            # Try to extract final_answer first
            final_answer = self._extract_final_answer(content)
            if final_answer:
                # This is the final answer, return it
                if self.memory_enabled:
                    self.conversation_history.append({
                        "role": "user",
                        "content": task
                    })
                    self.conversation_history.append({
                        "role": "assistant",
                        "content": final_answer
                    })
                return final_answer

            # Try to parse tool call
            tool_call = self._parse_tool_call(content)

            if tool_call:
                # Execute the tool
                tool_result = self._execute_tool(tool_call)

                # Add assistant's reasoning and tool call to messages
                messages.append({
                    "role": "assistant",
                    "content": content
                })
                
                # Add tool result as observation
                observation = f"Observation: {json.dumps(tool_result, ensure_ascii=False)}"
                messages.append({
                    "role": "user",
                    "content": observation
                })

                if self.memory_enabled:
                    self.conversation_history.extend([
                        {"role": "assistant", "content": content},
                        {"role": "user", "content": observation}
                    ])
            else:
                # No tool call and no final_answer, treat as direct response
                if self.memory_enabled:
                    self.conversation_history.append({
                        "role": "user",
                        "content": task
                    })
                    self.conversation_history.append({
                        "role": "assistant",
                        "content": content
                    })

                return content

        return "Maximum iterations reached. Task may be incomplete."
    
    def _extract_final_answer(self, content: str) -> Optional[str]:
        """
        Extract final answer from ReAct format response.
        从ReAct格式响应中提取最终答案。
        
        Args:
            content: LLM response content
            
        Returns:
            Final answer string or None
        """
        # Try to extract from JSON
        json_match = re.search(r'```json\s*(\{.*?\})\s*```', content, re.DOTALL)
        
        if json_match:
            try:
                data = json.loads(json_match.group(1))
                if "final_answer" in data:
                    return data["final_answer"]
            except json.JSONDecodeError:
                pass
        
        # Try to parse entire content as JSON
        try:
            data = json.loads(content)
            if "final_answer" in data:
                return data["final_answer"]
        except (json.JSONDecodeError, TypeError):
            pass
        
        return None

    def _prepare_messages(
        self,
        task: str,
        context: Optional[Dict[str, Any]]
    ) -> List[Dict[str, str]]:
        """
        Prepare message list for LLM API call.
        为LLM API调用准备消息列表。

        Args:
            task: Task description / 任务描述
            context: Additional context / 额外上下文

        Returns:
            List of message dicts / 消息字典列表
        """
        messages = [{"role": "system", "content": self.system_prompt}]

        if self.memory_enabled and self.conversation_history:
            messages.extend(self.conversation_history[-10:])

        if context:
            context_str = f"Additional context: {json.dumps(context)}\n\n"
            task = context_str + task

        messages.append({"role": "user", "content": task})

        return messages

    def _parse_tool_call(self, content: str) -> Optional[Dict[str, Any]]:
        """
        Parse tool call from LLM response.
        从LLM响应中解析工具调用。
        
        Supports both old format (tool/parameters) and new ReAct format (action/action_input).
        支持旧格式（tool/parameters）和新ReAct格式（action/action_input）。

        Args:
            content: LLM response content / LLM响应内容

        Returns:
            Tool call dict or None / 工具调用字典或None
        """
        # Try to extract JSON from markdown code block
        json_match = re.search(r'```json\s*(\{.*?\})\s*```', content, re.DOTALL)

        if json_match:
            try:
                data = json.loads(json_match.group(1))
                
                # Check for final_answer (end of reasoning)
                if "final_answer" in data:
                    return None  # No tool call, this is the final answer
                
                # New ReAct format: action/action_input
                if "action" in data and "action_input" in data:
                    return {
                        "tool": data["action"],
                        "parameters": data["action_input"]
                    }
                
                # Old format: tool/parameters
                if "tool" in data:
                    return data
                    
            except json.JSONDecodeError:
                pass

        # Try to parse the entire content as JSON
        try:
            data = json.loads(content)
            
            # Check for final_answer
            if "final_answer" in data:
                return None
            
            # New ReAct format
            if "action" in data and "action_input" in data:
                return {
                    "tool": data["action"],
                    "parameters": data["action_input"]
                }
            
            # Old format
            if "tool" in data:
                return data
                
        except (json.JSONDecodeError, TypeError):
            pass

        return None

    def _execute_tool(self, tool_call: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a tool based on the parsed tool call.
        根据解析的工具调用执行工具。

        Args:
            tool_call: Tool call specification / 工具调用规范

        Returns:
            Tool execution result / 工具执行结果
        """
        tool_name = tool_call.get("tool")
        parameters = tool_call.get("parameters", {})

        self._log_execution("tool_call", {
            "tool": tool_name,
            "parameters": parameters
        })

        if tool_name not in self.tools:
            result = {
                "success": False,
                "error": f"Tool '{tool_name}' not found"
            }
            self._log_execution("tool_error", result)
            return result

        tool = self.tools[tool_name]

        try:
            result = tool.execute(**parameters)
            self._log_execution("tool_result", result)
            return result
        except Exception as e:
            result = {
                "success": False,
                "error": str(e)
            }
            self._log_execution("tool_error", result)
            return result

    def _log_execution(self, event_type: str, data: Any) -> None:
        """
        Log execution events for debugging and analysis.
        记录执行事件以进行调试和分析。

        Args:
            event_type: Type of event / 事件类型
            data: Event data / 事件数据
        """
        self.execution_log.append({
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "data": data
        })

    def add_tool(self, tool: Tool) -> None:
        """
        Add a tool to the agent.
        向智能体添加工具。

        Args:
            tool: Tool instance / 工具实例
        """
        self.tools[tool.name] = tool
        self.system_prompt = self._default_system_prompt()

    def remove_tool(self, tool_name: str) -> bool:
        """
        Remove a tool from the agent.
        从智能体中移除工具。

        Args:
            tool_name: Name of tool to remove / 要移除的工具名称

        Returns:
            True if removed, False if not found / 如果已移除则为True
        """
        if tool_name in self.tools:
            del self.tools[tool_name]
            self.system_prompt = self._default_system_prompt()
            return True
        return False

    def clear_memory(self) -> None:
        """
        Clear conversation history.
        清除对话历史。
        """
        self.conversation_history.clear()

    def get_execution_log(self) -> List[Dict[str, Any]]:
        """
        Get the execution log.
        获取执行日志。

        Returns:
            List of execution events / 执行事件列表
        """
        return self.execution_log.copy()

    def clear_execution_log(self) -> None:
        """
        Clear the execution log.
        清除执行日志。
        """
        self.execution_log.clear()

    def __repr__(self) -> str:
        """String representation of the agent."""
        return f"Agent(name='{self.name}', tools={list(self.tools.keys())})"
