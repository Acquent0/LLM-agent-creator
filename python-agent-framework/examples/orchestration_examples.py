"""
Orchestration Examples / 编排示例

Examples of multi-agent collaboration patterns.
多智能体协作模式示例。

Author: LLM Agent Framework
License: MIT
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.agent import Agent
from core.llm_client import LLMClient
from core.orchestrator import (
    SequentialOrchestrator,
    ParallelOrchestrator,
    HierarchicalOrchestrator
)
from tools.base_tools import CalculatorTool, TextProcessingTool
from tools.research_tools import ScientificComputeTool
from dotenv import load_dotenv

load_dotenv()


def create_client():
    """Create and return LLM client. / 创建并返回LLM客户端。"""
    return LLMClient(
        api_url=os.getenv("LLM_API_URL"),
        api_key=os.getenv("LLM_API_KEY"),
        model=os.getenv("LLM_MODEL", "gpt-4")
    )


def example_1_sequential():
    """
    Example 1: Sequential orchestration.
    示例1：顺序编排。

    Agents work one after another, each building on the previous result.
    智能体依次工作，每个都建立在前一个结果之上。
    """
    print("=" * 60)
    print("Example 1: Sequential Orchestration")
    print("示例1：顺序编排")
    print("=" * 60)

    client = create_client()

    researcher = Agent(
        name="Researcher",
        llm_client=client,
        tools=[TextProcessingTool()],
        system_prompt="You are a research specialist. Analyze topics thoroughly."
    )

    analyst = Agent(
        name="Analyst",
        llm_client=client,
        tools=[CalculatorTool()],
        system_prompt="You are a data analyst. Provide statistical insights."
    )

    writer = Agent(
        name="Writer",
        llm_client=client,
        tools=[],
        system_prompt="You are a technical writer. Summarize findings clearly."
    )

    orchestrator = SequentialOrchestrator([researcher, analyst, writer])

    task = "Analyze the concept of machine learning and its applications"
    print(f"\nTask: {task}\n")

    result = orchestrator.run(task)
    print(f"\nFinal Result:\n{result}\n")


def example_2_parallel():
    """
    Example 2: Parallel orchestration.
    示例2：并行编排。

    Multiple agents work simultaneously on the same task from different angles.
    多个智能体同时从不同角度处理同一任务。
    """
    print("=" * 60)
    print("Example 2: Parallel Orchestration")
    print("示例2：并行编排")
    print("=" * 60)

    client = create_client()

    agent1 = Agent(
        name="Perspective1",
        llm_client=client,
        tools=[],
        system_prompt="You focus on theoretical aspects."
    )

    agent2 = Agent(
        name="Perspective2",
        llm_client=client,
        tools=[],
        system_prompt="You focus on practical applications."
    )

    agent3 = Agent(
        name="Perspective3",
        llm_client=client,
        tools=[],
        system_prompt="You focus on limitations and challenges."
    )

    orchestrator = ParallelOrchestrator([agent1, agent2, agent3], max_workers=3)

    task = "Analyze quantum computing"
    print(f"\nTask: {task}\n")

    results = orchestrator.run(task)

    print("\nResults from different perspectives:")
    for agent_name, result in results.items():
        print(f"\n--- {agent_name} ---")
        print(result[:200] + "..." if len(result) > 200 else result)
    print()


def example_3_hierarchical():
    """
    Example 3: Hierarchical orchestration.
    示例3：层级编排。

    A manager agent delegates tasks to worker agents.
    管理者智能体将任务委派给工作者智能体。
    """
    print("=" * 60)
    print("Example 3: Hierarchical Orchestration")
    print("示例3：层级编排")
    print("=" * 60)

    client = create_client()

    manager = Agent(
        name="ProjectManager",
        llm_client=client,
        tools=[],
        system_prompt="You are a project manager. Plan and coordinate work."
    )

    data_collector = Agent(
        name="DataCollector",
        llm_client=client,
        tools=[TextProcessingTool()],
        system_prompt="You collect and organize data."
    )

    analyst = Agent(
        name="DataAnalyst",
        llm_client=client,
        tools=[CalculatorTool(), ScientificComputeTool()],
        system_prompt="You analyze data and provide insights."
    )

    reporter = Agent(
        name="Reporter",
        llm_client=client,
        tools=[],
        system_prompt="You create comprehensive reports."
    )

    orchestrator = HierarchicalOrchestrator(
        manager=manager,
        workers=[data_collector, analyst, reporter]
    )

    task = "Create a report on data analysis best practices"
    print(f"\nTask: {task}\n")

    result = orchestrator.run(task)
    print(f"\nFinal Report:\n{result}\n")


def example_4_custom_workflow():
    """
    Example 4: Custom workflow combining different patterns.
    示例4：结合不同模式的自定义工作流。
    """
    print("=" * 60)
    print("Example 4: Custom Workflow")
    print("示例4：自定义工作流")
    print("=" * 60)

    client = create_client()

    researchers = [
        Agent(
            name=f"Researcher{i}",
            llm_client=client,
            tools=[TextProcessingTool()],
            system_prompt=f"You are research specialist #{i}."
        )
        for i in range(1, 3)
    ]

    parallel_orchestrator = ParallelOrchestrator(researchers)

    synthesizer = Agent(
        name="Synthesizer",
        llm_client=client,
        tools=[],
        system_prompt="You synthesize multiple research findings."
    )

    task = "Research the benefits of exercise"
    print(f"\nTask: {task}\n")

    print("Phase 1: Parallel research...")
    research_results = parallel_orchestrator.run(task)

    combined_research = "\n\n".join([
        f"{name}: {result}"
        for name, result in research_results.items()
    ])

    print("\nPhase 2: Synthesis...")
    final_result = synthesizer.run(
        f"Synthesize these research findings:\n{combined_research}"
    )

    print(f"\nFinal Synthesis:\n{final_result}\n")


if __name__ == "__main__":
    """
    Run orchestration examples.
    运行编排示例。
    """

    print("\n" + "="*60)
    print("LLM Agent Framework - Orchestration Examples")
    print("LLM智能体框架 - 编排示例")
    print("="*60 + "\n")

    try:
        example_1_sequential()
        print("\n" + "-"*60 + "\n")

        example_2_parallel()
        print("\n" + "-"*60 + "\n")

        example_3_hierarchical()
        print("\n" + "-"*60 + "\n")

        example_4_custom_workflow()

    except Exception as e:
        print(f"\n❌ Error running examples: {e}")
        print("\nMake sure you have:")
        print("1. Set up your .env file with API credentials")
        print("2. Installed all requirements: pip install -r requirements.txt")

    print("\n" + "="*60)
    print("Examples completed!")
    print("示例完成！")
    print("="*60 + "\n")
