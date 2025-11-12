"""
Storage Utilities / 存储工具

Supabase integration for persistent storage.
用于持久化存储的Supabase集成。

Author: LLM Agent Framework
License: MIT
"""

import os
from typing import Dict, Any, List, Optional
from datetime import datetime
from supabase import create_client, Client


class SupabaseStorage:
    """
    Supabase storage adapter for conversation history and analytics.
    用于对话历史和分析的Supabase存储适配器。

    Stores agent conversations, execution logs, and usage analytics.
    存储智能体对话、执行日志和使用分析。
    """

    def __init__(self, url: str = None, key: str = None):
        """
        Initialize Supabase client.
        初始化Supabase客户端。

        Args:
            url: Supabase URL / Supabase URL
            key: Supabase API key / Supabase API密钥
        """
        self.url = url or os.getenv("SUPABASE_URL")
        self.key = key or os.getenv("SUPABASE_KEY")

        if not self.url or not self.key:
            print("Warning: Supabase credentials not configured. Storage disabled.")
            self.client = None
        else:
            self.client: Client = create_client(self.url, self.key)

    def save_conversation(
        self,
        agent_name: str,
        messages: List[Dict[str, str]],
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Save conversation history.
        保存对话历史。

        Args:
            agent_name: Name of agent / 智能体名称
            messages: Conversation messages / 对话消息
            metadata: Additional metadata / 额外元数据

        Returns:
            Success status / 成功状态
        """
        if not self.client:
            return False

        try:
            data = {
                "agent_name": agent_name,
                "messages": messages,
                "metadata": metadata or {},
                "timestamp": datetime.now().isoformat()
            }

            self.client.table("conversations").insert(data).execute()
            return True

        except Exception as e:
            print(f"Error saving conversation: {e}")
            return False

    def get_conversations(
        self,
        agent_name: Optional[str] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Retrieve conversation history.
        检索对话历史。

        Args:
            agent_name: Filter by agent name / 按智能体名称过滤
            limit: Max number of records / 最大记录数

        Returns:
            List of conversations / 对话列表
        """
        if not self.client:
            return []

        try:
            query = self.client.table("conversations").select("*")

            if agent_name:
                query = query.eq("agent_name", agent_name)

            result = query.order("timestamp", desc=True).limit(limit).execute()
            return result.data

        except Exception as e:
            print(f"Error retrieving conversations: {e}")
            return []

    def save_execution_log(
        self,
        agent_name: str,
        log_entries: List[Dict[str, Any]]
    ) -> bool:
        """
        Save execution log.
        保存执行日志。

        Args:
            agent_name: Agent name / 智能体名称
            log_entries: Log entries / 日志条目

        Returns:
            Success status / 成功状态
        """
        if not self.client:
            return False

        try:
            data = {
                "agent_name": agent_name,
                "log_entries": log_entries,
                "timestamp": datetime.now().isoformat()
            }

            self.client.table("execution_logs").insert(data).execute()
            return True

        except Exception as e:
            print(f"Error saving execution log: {e}")
            return False

    def get_analytics(self) -> Dict[str, Any]:
        """
        Get usage analytics.
        获取使用分析。

        Returns:
            Analytics data / 分析数据
        """
        if not self.client:
            return {"error": "Storage not configured"}

        try:
            conversations = self.client.table("conversations").select("*").execute()
            logs = self.client.table("execution_logs").select("*").execute()

            return {
                "total_conversations": len(conversations.data),
                "total_executions": len(logs.data),
                "agents": list(set(c["agent_name"] for c in conversations.data))
            }

        except Exception as e:
            return {"error": str(e)}

    def clear_history(self, agent_name: Optional[str] = None) -> bool:
        """
        Clear conversation history.
        清除对话历史。

        Args:
            agent_name: Clear specific agent (None for all) / 清除特定智能体（None为全部）

        Returns:
            Success status / 成功状态
        """
        if not self.client:
            return False

        try:
            if agent_name:
                self.client.table("conversations").delete().eq("agent_name", agent_name).execute()
            else:
                self.client.table("conversations").delete().neq("agent_name", "").execute()

            return True

        except Exception as e:
            print(f"Error clearing history: {e}")
            return False
