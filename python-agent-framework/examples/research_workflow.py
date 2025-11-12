"""
Research Workflow Example / 科研工作流示例

A complete example of using the framework for scientific research.
使用框架进行科学研究的完整示例。

Author: LLM Agent Framework
License: MIT
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.agent import Agent
from core.llm_client import LLMClient
from core.orchestrator import SequentialOrchestrator
from tools.base_tools import CalculatorTool, PythonREPLTool
from tools.research_tools import ScientificComputeTool, StatisticalTestTool
from tools.data_tools import DataAnalysisTool, VisualizationTool
from dotenv import load_dotenv

load_dotenv()


def research_workflow_example():
    """
    Complete research workflow: data collection → analysis → visualization.
    完整的研究工作流：数据收集 → 分析 → 可视化。
    """
    print("=" * 70)
    print("Scientific Research Workflow Example")
    print("科研工作流示例")
    print("=" * 70)

    client = LLMClient(
        api_url=os.getenv("LLM_API_URL"),
        api_key=os.getenv("LLM_API_KEY"),
        model=os.getenv("LLM_MODEL", "gpt-4")
    )

    print("\n1. Creating specialized research agents...")
    print("1. 创建专门的研究智能体...")

    data_engineer = Agent(
        name="DataEngineer",
        llm_client=client,
        tools=[
            PythonREPLTool(),
            CalculatorTool()
        ],
        system_prompt="""You are a data engineer. You collect, clean, and
        prepare data for analysis. Generate sample datasets when needed."""
    )

    statistician = Agent(
        name="Statistician",
        llm_client=client,
        tools=[
            StatisticalTestTool(),
            ScientificComputeTool(),
            CalculatorTool()
        ],
        system_prompt="""You are a statistician. Perform statistical analysis
        and hypothesis testing on datasets."""
    )

    data_analyst = Agent(
        name="DataAnalyst",
        llm_client=client,
        tools=[
            DataAnalysisTool(),
            CalculatorTool()
        ],
        system_prompt="""You are a data analyst. Analyze datasets and
        extract meaningful insights."""
    )

    visualizer = Agent(
        name="Visualizer",
        llm_client=client,
        tools=[
            VisualizationTool(),
        ],
        system_prompt="""You are a data visualization specialist. Create
        clear and informative visualizations."""
    )

    print("\n2. Creating research orchestrator...")
    print("2. 创建研究编排器...")

    research_team = SequentialOrchestrator([
        data_engineer,
        statistician,
        data_analyst,
        visualizer
    ])

    print("\n3. Defining research task...")
    print("3. 定义研究任务...")

    research_task = """
    Research Task: Analyze the relationship between study hours and exam scores.

    Please:
    1. Generate a sample dataset of 50 students with study hours (0-10) and exam scores (0-100)
    2. Perform statistical analysis (correlation, descriptive statistics)
    3. Test if there's a significant relationship between study hours and scores
    4. Create visualizations to illustrate findings
    5. Provide a summary of the research findings

    研究任务：分析学习时长与考试成绩之间的关系。

    请：
    1. 生成50名学生的样本数据集，包含学习时长（0-10小时）和考试成绩（0-100分）
    2. 进行统计分析（相关性、描述性统计）
    3. 测试学习时长与成绩之间是否存在显著关系
    4. 创建可视化以说明发现
    5. 提供研究发现摘要
    """

    print("\n4. Executing research workflow...")
    print("4. 执行研究工作流...")
    print("-" * 70)

    result = research_team.run(research_task)

    print("\n" + "=" * 70)
    print("RESEARCH FINDINGS | 研究发现")
    print("=" * 70)
    print(result)
    print("=" * 70)

    print("\n5. Viewing execution history...")
    print("5. 查看执行历史...")

    for i, entry in enumerate(research_team.execution_history, 1):
        print(f"\nStep {i}: {entry['agent']}")
        print(f"Timestamp: {entry['timestamp']}")
        print(f"Result: {entry['result'][:100]}..." if len(entry['result']) > 100 else f"Result: {entry['result']}")

    print("\n" + "=" * 70)
    print("Research workflow completed successfully!")
    print("研究工作流成功完成！")
    print("=" * 70)


def custom_analysis_example():
    """
    Custom data analysis example.
    自定义数据分析示例。
    """
    print("\n" + "=" * 70)
    print("Custom Data Analysis Example")
    print("自定义数据分析示例")
    print("=" * 70)

    client = LLMClient(
        api_url=os.getenv("LLM_API_URL"),
        api_key=os.getenv("LLM_API_KEY"),
        model=os.getenv("LLM_MODEL", "gpt-4")
    )

    analyst = Agent(
        name="CustomAnalyst",
        llm_client=client,
        tools=[
            DataAnalysisTool(),
            StatisticalTestTool(),
            CalculatorTool()
        ],
        system_prompt="You are a data analyst specializing in experimental data."
    )

    sample_data = {
        "group_a": [23, 25, 28, 30, 27, 26, 29, 31, 24, 28],
        "group_b": [35, 38, 40, 37, 39, 36, 41, 38, 37, 40]
    }

    task = f"""
    Analyze this experimental data:
    {sample_data}

    Perform:
    1. Descriptive statistics for both groups
    2. T-test to compare the two groups
    3. Determine if there's a significant difference

    分析此实验数据并执行：
    1. 两组的描述性统计
    2. T检验比较两组
    3. 确定是否存在显著差异
    """

    print("\nAnalyzing data...")
    result = analyst.run(task)

    print("\nAnalysis Results | 分析结果:")
    print("-" * 70)
    print(result)
    print("=" * 70)


if __name__ == "__main__":
    """
    Run research workflow examples.
    运行研究工作流示例。
    """

    print("\n" + "="*70)
    print("LLM Agent Framework - Research Workflow Examples")
    print("LLM智能体框架 - 研究工作流示例")
    print("="*70 + "\n")

    try:
        research_workflow_example()

        print("\n\n")

        custom_analysis_example()

    except Exception as e:
        print(f"\n❌ Error running examples: {e}")
        print("\nMake sure you have:")
        print("1. Set up your .env file with API credentials")
        print("2. Installed all requirements: pip install -r requirements.txt")

    print("\n" + "="*70)
    print("All examples completed!")
    print("所有示例完成！")
    print("="*70 + "\n")
