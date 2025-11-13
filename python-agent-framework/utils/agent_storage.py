"""
Agent Storage Manager / 智能体存储管理器

Manages saving and loading of agent configurations.
管理智能体配置的保存和加载。

Author: LLM Agent Framework
License: MIT
"""

import json
import os
from typing import List, Dict, Any, Optional
from datetime import datetime


class AgentStorageManager:
    """
    Manages agent configurations stored in JSON files.
    管理存储在JSON文件中的智能体配置。
    """

    def __init__(self, storage_dir: str = None):
        """
        Initialize agent storage manager.
        初始化智能体存储管理器。

        Args:
            storage_dir: Directory to store agent configs. If None, uses default.
        """
        if storage_dir is None:
            # Default to agents_data/ in parent directory
            storage_dir = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                "agents_data"
            )
        
        self.storage_dir = storage_dir
        self.config_file = os.path.join(storage_dir, "agents.json")
        
        # Create directory if it doesn't exist
        os.makedirs(storage_dir, exist_ok=True)
        
        # Initialize file if it doesn't exist
        if not os.path.exists(self.config_file):
            self._save_to_file({"agents": []})

    def _load_from_file(self) -> Dict[str, Any]:
        """Load agents from JSON file."""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading agents: {e}")
            return {"agents": []}

    def _save_to_file(self, data: Dict[str, Any]):
        """Save agents to JSON file."""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving agents: {e}")

    def save_agent(self, agent_config: Dict[str, Any]) -> bool:
        """
        Save an agent configuration.
        保存智能体配置。

        Args:
            agent_config: Dictionary containing agent configuration
                Required keys: name, tools (list of tool names)
                Optional keys: system_prompt, created_at

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            data = self._load_from_file()
            agents = data.get("agents", [])
            
            # Check if agent with same name exists
            existing_index = None
            for i, agent in enumerate(agents):
                if agent.get("name") == agent_config.get("name"):
                    existing_index = i
                    break
            
            # Add metadata
            if "created_at" not in agent_config:
                agent_config["created_at"] = datetime.now().isoformat()
            agent_config["updated_at"] = datetime.now().isoformat()
            
            # Update or add
            if existing_index is not None:
                agents[existing_index] = agent_config
            else:
                agents.append(agent_config)
            
            data["agents"] = agents
            self._save_to_file(data)
            return True
            
        except Exception as e:
            print(f"Error saving agent: {e}")
            return False

    def load_agent(self, agent_name: str) -> Optional[Dict[str, Any]]:
        """
        Load a specific agent configuration.
        加载特定智能体配置。

        Args:
            agent_name: Name of the agent to load

        Returns:
            Dict with agent config or None if not found
        """
        data = self._load_from_file()
        agents = data.get("agents", [])
        
        for agent in agents:
            if agent.get("name") == agent_name:
                return agent
        
        return None

    def load_all_agents(self) -> List[Dict[str, Any]]:
        """
        Load all agent configurations.
        加载所有智能体配置。

        Returns:
            List of agent configuration dictionaries
        """
        data = self._load_from_file()
        return data.get("agents", [])

    def delete_agent(self, agent_name: str) -> bool:
        """
        Delete an agent configuration.
        删除智能体配置。

        Args:
            agent_name: Name of the agent to delete

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            data = self._load_from_file()
            agents = data.get("agents", [])
            
            # Filter out the agent to delete
            original_count = len(agents)
            agents = [a for a in agents if a.get("name") != agent_name]
            
            if len(agents) < original_count:
                data["agents"] = agents
                self._save_to_file(data)
                return True
            
            return False
            
        except Exception as e:
            print(f"Error deleting agent: {e}")
            return False

    def get_agent_count(self) -> int:
        """
        Get the total number of saved agents.
        获取保存的智能体总数。

        Returns:
            int: Number of agents
        """
        data = self._load_from_file()
        return len(data.get("agents", []))

    def agent_exists(self, agent_name: str) -> bool:
        """
        Check if an agent with the given name exists.
        检查是否存在给定名称的智能体。

        Args:
            agent_name: Name to check

        Returns:
            bool: True if exists, False otherwise
        """
        return self.load_agent(agent_name) is not None
