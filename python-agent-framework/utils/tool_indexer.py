"""
Tool Indexer / 工具索引器

Creates semantic index of tools to efficiently retrieve relevant tools for tasks.
创建工具的语义索引，以高效检索任务相关工具。

Author: LLM Agent Framework
License: MIT
"""

import json
import os
from typing import List, Dict, Any, Optional
import re


class ToolIndexer:
    """
    Indexes tools and retrieves relevant ones based on task description.
    索引工具并根据任务描述检索相关工具。
    
    Uses simple keyword matching and can be extended with embeddings.
    使用简单的关键词匹配，可以扩展为嵌入向量匹配。
    """

    def __init__(self, llm_client=None):
        """
        Initialize tool indexer.
        初始化工具索引器。

        Args:
            llm_client: Optional LLM client for semantic matching
        """
        self.llm_client = llm_client
        self.tool_index = {}
        self._build_index()

    def _build_index(self):
        """Build index from all available tools."""
        # Index built-in tools
        self._index_builtin_tools()
        
        # Index generated tools
        self._index_generated_tools()

    def _index_builtin_tools(self):
        """Index built-in tools from tools/ directory."""
        builtin_tools = {
            "CalculatorTool": {
                "description": "Perform mathematical calculations and evaluations",
                "keywords": ["calculate", "math", "compute", "arithmetic", "evaluate", "expression"],
                "category": "computation"
            },
            "FileIOTool": {
                "description": "Read and write files",
                "keywords": ["file", "read", "write", "save", "load", "text", "data"],
                "category": "file_operations"
            },
            "PythonREPLTool": {
                "description": "Execute Python code",
                "keywords": ["python", "code", "execute", "run", "script", "programming"],
                "category": "code_execution"
            },
            "TextProcessingTool": {
                "description": "Process and analyze text",
                "keywords": ["text", "string", "process", "analyze", "word", "character", "count"],
                "category": "text_processing"
            },
            "ScientificComputeTool": {
                "description": "Scientific computing operations",
                "keywords": ["scientific", "compute", "matrix", "linear algebra", "numpy"],
                "category": "scientific"
            },
            "StatisticalTestTool": {
                "description": "Statistical tests and analysis",
                "keywords": ["statistics", "test", "hypothesis", "mean", "variance", "distribution"],
                "category": "scientific"
            },
            "UnitConverterTool": {
                "description": "Convert between different units",
                "keywords": ["convert", "unit", "measurement", "length", "weight", "temperature"],
                "category": "conversion"
            },
            "DataAnalysisTool": {
                "description": "Analyze data and compute statistics",
                "keywords": ["data", "analyze", "statistics", "mean", "median", "correlation"],
                "category": "data_analysis"
            },
            "VisualizationTool": {
                "description": "Create data visualizations and plots",
                "keywords": ["plot", "chart", "graph", "visualize", "visualization", "matplotlib"],
                "category": "visualization"
            },
            "DataCleaningTool": {
                "description": "Clean and preprocess data",
                "keywords": ["clean", "preprocess", "missing", "outlier", "normalize", "standardize"],
                "category": "data_processing"
            }
        }

        self.tool_index.update(builtin_tools)

    def _index_generated_tools(self):
        """Index dynamically generated tools."""
        metadata_dir = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "tools_data",
            "generated_metadata"
        )

        if not os.path.exists(metadata_dir):
            return

        for filename in os.listdir(metadata_dir):
            if filename.endswith(".json"):
                file_path = os.path.join(metadata_dir, filename)
                with open(file_path, "r", encoding="utf-8") as f:
                    metadata = json.load(f)
                    
                    # Extract keywords from description and parameters
                    keywords = self._extract_keywords(metadata)
                    
                    self.tool_index[metadata["name"]] = {
                        "description": metadata["description"],
                        "keywords": keywords,
                        "category": "custom",
                        "metadata": metadata
                    }

    def _extract_keywords(self, metadata: Dict[str, Any]) -> List[str]:
        """Extract keywords from tool metadata."""
        keywords = []
        
        # From description
        desc = metadata.get("description", "").lower()
        keywords.extend(re.findall(r'\w+', desc))
        
        # From parameters
        for param in metadata.get("input_parameters", []):
            keywords.extend(re.findall(r'\w+', param.get("description", "").lower()))
        
        # Remove common words
        stop_words = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "by"}
        keywords = [k for k in keywords if k not in stop_words and len(k) > 2]
        
        return list(set(keywords))

    def search_tools(
        self,
        task_description: str,
        max_results: int = 5,
        min_score: float = 0.0
    ) -> List[Dict[str, Any]]:
        """
        Search for relevant tools based on task description.
        根据任务描述搜索相关工具。

        Args:
            task_description: Description of the task / 任务描述
            max_results: Maximum number of tools to return / 返回的最大工具数
            min_score: Minimum relevance score / 最小相关性分数

        Returns:
            List of relevant tools with scores / 带分数的相关工具列表
        """
        # Extract keywords from task
        task_keywords = set(re.findall(r'\w+', task_description.lower()))
        task_keywords = {k for k in task_keywords if len(k) > 2}

        # Score each tool
        scored_tools = []
        for tool_name, tool_info in self.tool_index.items():
            score = self._calculate_relevance_score(task_keywords, tool_info)
            
            if score >= min_score:
                scored_tools.append({
                    "name": tool_name,
                    "description": tool_info["description"],
                    "score": score,
                    "category": tool_info["category"],
                    "info": tool_info
                })

        # Sort by score and return top results
        scored_tools.sort(key=lambda x: x["score"], reverse=True)
        return scored_tools[:max_results]

    def _calculate_relevance_score(
        self,
        task_keywords: set,
        tool_info: Dict[str, Any]
    ) -> float:
        """Calculate relevance score between task and tool."""
        tool_keywords = set(tool_info.get("keywords", []))
        
        # Calculate keyword overlap
        overlap = len(task_keywords & tool_keywords)
        if len(tool_keywords) == 0:
            return 0.0
        
        # Jaccard similarity
        union = len(task_keywords | tool_keywords)
        jaccard = overlap / union if union > 0 else 0.0
        
        # Boost score if description contains task keywords
        desc_lower = tool_info.get("description", "").lower()
        desc_boost = sum(1 for kw in task_keywords if kw in desc_lower) * 0.1
        
        return jaccard + desc_boost

    def get_tool_by_name(self, tool_name: str) -> Optional[Dict[str, Any]]:
        """Get tool information by name."""
        return self.tool_index.get(tool_name)

    def list_all_tools(self, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        List all available tools, optionally filtered by category.
        列出所有可用工具，可选按类别过滤。
        """
        tools = []
        for tool_name, tool_info in self.tool_index.items():
            if category is None or tool_info.get("category") == category:
                tools.append({
                    "name": tool_name,
                    "description": tool_info["description"],
                    "category": tool_info["category"]
                })
        return tools

    def refresh_index(self):
        """Refresh the tool index to include newly generated tools."""
        self.tool_index = {}
        self._build_index()

    def get_tool_summary(self, tool_names: List[str]) -> str:
        """
        Get a concise summary of multiple tools for LLM context.
        获取多个工具的简洁摘要，用于LLM上下文。
        """
        summaries = []
        for name in tool_names:
            if name in self.tool_index:
                info = self.tool_index[name]
                summaries.append(f"- {name}: {info['description']}")
        
        return "\n".join(summaries)
