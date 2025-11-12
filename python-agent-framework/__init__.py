"""
LLM Agent Framework
科研LLM智能体框架

A lightweight, flexible framework for building custom LLM agents for scientific research.
一个轻量级、灵活的框架，用于构建科研用途的自定义LLM智能体。

Author: LLM Agent Framework
License: MIT
Version: 1.0.0
"""

__version__ = "1.0.0"

from .core import (
    Agent,
    Tool,
    ToolRegistry,
    LLMClient,
    SequentialOrchestrator,
    ParallelOrchestrator,
    HierarchicalOrchestrator
)

from .tools import (
    CalculatorTool,
    FileIOTool,
    PythonREPLTool,
    ScientificComputeTool,
    DataAnalysisTool,
    VisualizationTool
)

__all__ = [
    'Agent',
    'Tool',
    'ToolRegistry',
    'LLMClient',
    'SequentialOrchestrator',
    'ParallelOrchestrator',
    'HierarchicalOrchestrator',
    'CalculatorTool',
    'FileIOTool',
    'PythonREPLTool',
    'ScientificComputeTool',
    'DataAnalysisTool',
    'VisualizationTool'
]
