"""
Multi-Agent Orchestrator / 多智能体编排器

This module provides orchestrators for coordinating multiple agents.
此模块提供用于协调多个智能体的编排器。

Author: LLM Agent Framework
License: MIT
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

from .agent import Agent


class Orchestrator(ABC):
    """
    Base class for agent orchestrators.
    智能体编排器的基类。

    Orchestrators manage the execution flow of multiple agents working
    together to complete complex tasks.
    编排器管理多个智能体协同工作以完成复杂任务的执行流程。
    """

    def __init__(self, agents: List[Agent]):
        """
        Initialize orchestrator with agents.
        使用智能体初始化编排器。

        Args:
            agents: List of agent instances / 智能体实例列表
        """
        self.agents = agents
        self.execution_history: List[Dict[str, Any]] = []

    @abstractmethod
    def run(self, task: str, context: Optional[Dict[str, Any]] = None) -> Any:
        """
        Execute the orchestration.
        执行编排。

        Args:
            task: Task description / 任务描述
            context: Additional context / 额外上下文

        Returns:
            Orchestration result / 编排结果
        """
        raise NotImplementedError

    def _log_execution(self, agent_name: str, result: Any) -> None:
        """
        Log execution result.
        记录执行结果。

        Args:
            agent_name: Name of agent / 智能体名称
            result: Execution result / 执行结果
        """
        self.execution_history.append({
            "timestamp": datetime.now().isoformat(),
            "agent": agent_name,
            "result": result
        })


class SequentialOrchestrator(Orchestrator):
    """
    Sequential orchestrator - agents work one after another.
    顺序编排器 - 智能体依次工作。

    Each agent receives the previous agent's output as input.
    每个智能体接收前一个智能体的输出作为输入。

    Example:
        Researcher → Analyst → Writer
        研究员 → 分析师 → 写作者
    """

    def run(self, task: str, context: Optional[Dict[str, Any]] = None) -> str:
        """
        Execute agents sequentially.
        顺序执行智能体。

        Args:
            task: Initial task / 初始任务
            context: Additional context / 额外上下文

        Returns:
            Final agent's output / 最终智能体的输出
        """
        current_task = task
        current_context = context or {}

        for agent in self.agents:
            print(f"[SequentialOrchestrator] Running agent: {agent.name}")

            result = agent.run(current_task, current_context)
            self._log_execution(agent.name, result)

            current_context["previous_result"] = result
            current_task = f"Based on the previous result, continue with: {task}"

        return result


class ParallelOrchestrator(Orchestrator):
    """
    Parallel orchestrator - agents work simultaneously.
    并行编排器 - 智能体同时工作。

    All agents receive the same task and work independently.
    所有智能体接收相同的任务并独立工作。

    Example:
        Task → [Agent1, Agent2, Agent3] → Combined results
        任务 → [智能体1, 智能体2, 智能体3] → 合并结果
    """

    def __init__(self, agents: List[Agent], max_workers: int = 3):
        """
        Initialize parallel orchestrator.
        初始化并行编排器。

        Args:
            agents: List of agents / 智能体列表
            max_workers: Maximum parallel workers / 最大并行工作数
        """
        super().__init__(agents)
        self.max_workers = max_workers

    def run(self, task: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, str]:
        """
        Execute agents in parallel.
        并行执行智能体。

        Args:
            task: Task for all agents / 所有智能体的任务
            context: Additional context / 额外上下文

        Returns:
            Dict mapping agent names to their results / 将智能体名称映射到其结果的字典
        """
        results = {}

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_agent = {
                executor.submit(agent.run, task, context): agent
                for agent in self.agents
            }

            for future in as_completed(future_to_agent):
                agent = future_to_agent[future]
                try:
                    result = future.result()
                    results[agent.name] = result
                    self._log_execution(agent.name, result)
                    print(f"[ParallelOrchestrator] {agent.name} completed")
                except Exception as e:
                    error_msg = f"Error: {str(e)}"
                    results[agent.name] = error_msg
                    self._log_execution(agent.name, error_msg)

        return results


class HierarchicalOrchestrator(Orchestrator):
    """
    Hierarchical orchestrator - manager agent delegates to worker agents.
    层级编排器 - 管理者智能体委派任务给工作者智能体。

    A manager agent decides which worker agents to use and coordinates
    their work.
    管理者智能体决定使用哪些工作者智能体并协调它们的工作。

    Structure:
        Manager Agent
          ├── Worker Agent 1
          ├── Worker Agent 2
          └── Worker Agent 3
    """

    def __init__(self, manager: Agent, workers: List[Agent]):
        """
        Initialize hierarchical orchestrator.
        初始化层级编排器。

        Args:
            manager: Manager agent / 管理者智能体
            workers: Worker agents / 工作者智能体
        """
        super().__init__([manager] + workers)
        self.manager = manager
        self.workers = {worker.name: worker for worker in workers}

    def run(self, task: str, context: Optional[Dict[str, Any]] = None) -> str:
        """
        Execute hierarchical orchestration.
        执行层级编排。

        The manager agent plans the work and delegates to workers.
        管理者智能体规划工作并委派给工作者。

        Args:
            task: Main task / 主要任务
            context: Additional context / 额外上下文

        Returns:
            Final response / 最终响应
        """
        context = context or {}
        context["available_workers"] = list(self.workers.keys())

        manager_prompt = f"""Task: {task}

Available workers: {', '.join(self.workers.keys())}

As the manager, plan how to break down this task and delegate to workers.
Respond with your plan and the subtask for each worker.
"""

        plan = self.manager.run(manager_prompt, context)
        self._log_execution(self.manager.name, plan)

        worker_results = {}
        for worker_name, worker in self.workers.items():
            subtask = f"Based on the manager's plan:\n{plan}\n\nComplete your part of the task: {task}"
            result = worker.run(subtask, context)
            worker_results[worker_name] = result
            self._log_execution(worker_name, result)

        final_prompt = f"""Original task: {task}

Your plan: {plan}

Worker results:
{self._format_results(worker_results)}

Synthesize the final response based on all worker outputs.
"""

        final_result = self.manager.run(final_prompt, context)
        self._log_execution(f"{self.manager.name} (final)", final_result)

        return final_result

    def _format_results(self, results: Dict[str, str]) -> str:
        """
        Format worker results for display.
        格式化工作者结果以供显示。

        Args:
            results: Worker results / 工作者结果

        Returns:
            Formatted string / 格式化字符串
        """
        formatted = []
        for worker_name, result in results.items():
            formatted.append(f"{worker_name}:\n{result}\n")
        return "\n".join(formatted)


class ConditionalOrchestrator(Orchestrator):
    """
    Conditional orchestrator - route based on conditions.
    条件编排器 - 基于条件进行路由。

    Routes tasks to different agents based on conditions or LLM decisions.
    根据条件或LLM决策将任务路由到不同的智能体。
    """

    def __init__(
        self,
        router: Agent,
        agents: Dict[str, Agent],
        default_agent: Optional[str] = None
    ):
        """
        Initialize conditional orchestrator.
        初始化条件编排器。

        Args:
            router: Agent that decides routing / 决定路由的智能体
            agents: Dict mapping agent names to instances / 将智能体名称映射到实例的字典
            default_agent: Default agent name / 默认智能体名称
        """
        super().__init__(list(agents.values()) + [router])
        self.router = router
        self.agents = agents
        self.default_agent = default_agent

    def run(self, task: str, context: Optional[Dict[str, Any]] = None) -> str:
        """
        Execute conditional routing.
        执行条件路由。

        Args:
            task: Task to route / 要路由的任务
            context: Additional context / 额外上下文

        Returns:
            Response from selected agent / 所选智能体的响应
        """
        routing_prompt = f"""Task: {task}

Available agents: {', '.join(self.agents.keys())}

Which agent should handle this task? Respond with just the agent name.
"""

        selected_name = self.router.run(routing_prompt, context).strip()
        self._log_execution(self.router.name, f"Selected: {selected_name}")

        if selected_name not in self.agents:
            if self.default_agent:
                selected_name = self.default_agent
            else:
                selected_name = list(self.agents.keys())[0]

        selected_agent = self.agents[selected_name]
        result = selected_agent.run(task, context)
        self._log_execution(selected_name, result)

        return result


class CustomOrchestrator(Orchestrator):
    """
    Base class for implementing custom orchestration patterns.
    实现自定义编排模式的基类。

    Inherit from this class to create your own orchestration logic.
    继承此类以创建自己的编排逻辑。
    """

    def run(self, task: str, context: Optional[Dict[str, Any]] = None) -> Any:
        """
        Implement your custom orchestration logic.
        实现您的自定义编排逻辑。

        Args:
            task: Task description / 任务描述
            context: Additional context / 额外上下文

        Returns:
            Orchestration result / 编排结果
        """
        return self.orchestrate(task, context)

    @abstractmethod
    def orchestrate(self, task: str, context: Optional[Dict[str, Any]]) -> Any:
        """
        Custom orchestration method to implement.
        要实现的自定义编排方法。

        Args:
            task: Task description / 任务描述
            context: Additional context / 额外上下文

        Returns:
            Result / 结果
        """
        raise NotImplementedError("Implement your orchestration logic here")
