"""
Tool Generator / 工具生成器

Uses LLM to automatically generate custom tools based on user requirements.
使用LLM根据用户需求自动生成自定义工具。

Author: LLM Agent Framework
License: MIT
"""

import json
import os
from typing import Dict, Any, Optional, List
from datetime import datetime


class ToolGenerator:
    """
    Generates custom tools using LLM based on user specifications.
    根据用户规格使用LLM生成自定义工具。
    """

    def __init__(self, llm_client, tools_dir: str = None):
        """
        Initialize tool generator.
        初始化工具生成器。

        Args:
            llm_client: LLM client instance / LLM客户端实例
            tools_dir: Directory to save generated tools / 保存生成工具的目录
        """
        self.llm_client = llm_client
        self.tools_dir = tools_dir or os.path.join(
            os.path.dirname(os.path.dirname(__file__)), 
            "tools", 
            "generated"
        )
        os.makedirs(self.tools_dir, exist_ok=True)

    def generate_tool(
        self,
        tool_name: str,
        description: str,
        input_parameters: List[Dict[str, str]],
        expected_output: str,
        implementation_details: Optional[str] = None,
        dependencies: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Generate a custom tool based on specifications.
        根据规格生成自定义工具。

        Args:
            tool_name: Name of the tool / 工具名称
            description: What the tool does / 工具功能描述
            input_parameters: List of input parameters with name, type, description
            expected_output: Description of expected output / 期望输出描述
            implementation_details: Additional implementation hints / 额外实现提示
            dependencies: Required Python packages / 所需Python包

        Returns:
            Dictionary with generated tool info / 生成的工具信息字典
        """
        # Create the prompt for LLM
        prompt = self._create_generation_prompt(
            tool_name,
            description,
            input_parameters,
            expected_output,
            implementation_details,
            dependencies
        )

        # Generate tool code using LLM
        messages = [
            {
                "role": "system",
                "content": "You are an expert Python developer. Generate clean, well-documented, and functional Python code for tools. Always follow the Tool base class structure."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]

        try:
            response = self.llm_client.chat(messages, temperature=0.3, max_tokens=2000)
            
            if not response.get("success"):
                return {
                    "success": False,
                    "error": "Failed to generate tool code"
                }

            # Extract code from response
            code = self._extract_code_from_response(response["content"])
            
            # Save the tool
            file_path = self._save_tool(tool_name, code, description)
            
            # Create metadata
            metadata = {
                "name": tool_name,
                "description": description,
                "file_path": file_path,
                "created_at": datetime.now().isoformat(),
                "input_parameters": input_parameters,
                "expected_output": expected_output,
                "dependencies": dependencies or []
            }

            # Save metadata
            self._save_metadata(tool_name, metadata)

            return {
                "success": True,
                "tool_name": tool_name,
                "file_path": file_path,
                "metadata": metadata,
                "code": code
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def _create_generation_prompt(
        self,
        tool_name: str,
        description: str,
        input_parameters: List[Dict[str, str]],
        expected_output: str,
        implementation_details: Optional[str],
        dependencies: Optional[List[str]]
    ) -> str:
        """Create the prompt for tool generation."""
        params_str = "\n".join([
            f"  - {p['name']} ({p['type']}): {p['description']}"
            for p in input_parameters
        ])

        deps_str = ""
        if dependencies:
            deps_str = f"\nRequired dependencies: {', '.join(dependencies)}"

        impl_str = ""
        if implementation_details:
            impl_str = f"\nImplementation details:\n{implementation_details}"

        prompt = f"""Generate a Python tool class with the following specifications:

Tool Name: {tool_name}
Description: {description}

Input Parameters:
{params_str}

Expected Output: {expected_output}{deps_str}{impl_str}

Requirements:
1. Inherit from the Tool base class
2. Implement the execute() method
3. Include comprehensive docstrings
4. Add error handling
5. Return results in a dictionary format
6. Use type hints

Base Tool class structure:
```python
class Tool:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
    
    def execute(self, **kwargs) -> Dict[str, Any]:
        raise NotImplementedError
```

Generate ONLY the Python code for the tool class, wrapped in ```python ``` code blocks. Do not include any explanation or additional text outside the code block."""

        return prompt

    def _extract_code_from_response(self, response: str) -> str:
        """Extract Python code from LLM response."""
        # Find code block
        if "```python" in response:
            start = response.find("```python") + 9
            end = response.find("```", start)
            code = response[start:end].strip()
        elif "```" in response:
            start = response.find("```") + 3
            end = response.find("```", start)
            code = response[start:end].strip()
        else:
            code = response.strip()

        return code

    def _save_tool(self, tool_name: str, code: str, description: str) -> str:
        """Save the generated tool to a file."""
        # Convert tool name to valid Python filename
        filename = tool_name.lower().replace(" ", "_").replace("-", "_")
        if not filename.endswith(".py"):
            filename += ".py"

        file_path = os.path.join(self.tools_dir, filename)

        # Add header comment
        header = f'''"""
{tool_name}

{description}

Auto-generated by LLM Agent Framework
Generated at: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""

import sys
import os
from typing import Dict, Any

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.tool import Tool

'''

        full_code = header + code

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(full_code)

        return file_path

    def _save_metadata(self, tool_name: str, metadata: Dict[str, Any]) -> None:
        """Save tool metadata to JSON file."""
        metadata_dir = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "tools_data",
            "generated_metadata"
        )
        os.makedirs(metadata_dir, exist_ok=True)

        filename = tool_name.lower().replace(" ", "_").replace("-", "_") + ".json"
        file_path = os.path.join(metadata_dir, filename)

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)

    def list_generated_tools(self) -> List[Dict[str, Any]]:
        """List all generated tools with their metadata."""
        metadata_dir = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "tools_data",
            "generated_metadata"
        )

        if not os.path.exists(metadata_dir):
            return []

        tools = []
        for filename in os.listdir(metadata_dir):
            if filename.endswith(".json"):
                file_path = os.path.join(metadata_dir, filename)
                with open(file_path, "r", encoding="utf-8") as f:
                    metadata = json.load(f)
                    tools.append(metadata)

        return tools

    def delete_tool(self, tool_name: str) -> bool:
        """Delete a generated tool and its metadata."""
        filename = tool_name.lower().replace(" ", "_").replace("-", "_")
        
        # Delete Python file
        py_file = os.path.join(self.tools_dir, filename + ".py")
        if os.path.exists(py_file):
            os.remove(py_file)

        # Delete metadata
        metadata_dir = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "tools_data",
            "generated_metadata"
        )
        json_file = os.path.join(metadata_dir, filename + ".json")
        if os.path.exists(json_file):
            os.remove(json_file)

        return True
