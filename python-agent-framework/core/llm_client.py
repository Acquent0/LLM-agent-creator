"""
LLM Client / LLM客户端

This module provides a flexible client for interacting with various LLM APIs.
此模块提供了一个灵活的客户端，用于与各种LLM API交互。

Supports OpenAI-compatible APIs, Claude, and custom endpoints.
支持OpenAI兼容的API、Claude和自定义端点。

Author: LLM Agent Framework
License: MIT
"""

import requests
import json
import time
from typing import Dict, Any, List, Optional, Union
from datetime import datetime
import os


class LLMClient:
    """
    Client for interacting with LLM APIs.
    用于与LLM API交互的客户端。

    Supports multiple API formats and provides retry logic, error handling,
    and response parsing.
    支持多种API格式，并提供重试逻辑、错误处理和响应解析。

    Attributes:
        api_url (str): API endpoint URL / API端点URL
        api_key (str): API authentication key / API认证密钥
        model (str): Model name / 模型名称
        timeout (int): Request timeout in seconds / 请求超时时间（秒）
        max_retries (int): Maximum retry attempts / 最大重试次数
    """

    def __init__(
        self,
        api_url: str,
        api_key: str,
        model: str = "gpt-4",
        timeout: int = 60,
        max_retries: int = 3,
        api_type: str = "openai"
    ):
        """
        Initialize the LLM client.
        初始化LLM客户端。

        Args:
            api_url: API endpoint URL / API端点URL
            api_key: API key / API密钥
            model: Model name / 模型名称
            timeout: Request timeout / 请求超时时间
            max_retries: Maximum retries / 最大重试次数
            api_type: API type ("openai", "claude", "custom") / API类型
        """
        self.api_url = api_url
        self.api_key = api_key
        self.model = model
        self.timeout = timeout
        self.max_retries = max_retries
        self.api_type = api_type

        self.request_count = 0
        self.total_tokens = 0

    def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        stream: bool = False,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Send a chat completion request to the LLM.
        向LLM发送聊天补全请求。

        Args:
            messages: List of message dicts with 'role' and 'content' / 消息字典列表
            temperature: Sampling temperature (0-2) / 采样温度
            max_tokens: Maximum tokens to generate / 生成的最大令牌数
            stream: Whether to stream the response / 是否流式响应
            **kwargs: Additional API-specific parameters / 额外的API特定参数

        Returns:
            Response dictionary containing the completion / 包含补全的响应字典

        Raises:
            Exception: If request fails after retries / 如果重试后请求失败
        """
        if self.api_type == "openai":
            return self._openai_chat(messages, temperature, max_tokens, stream, **kwargs)
        elif self.api_type == "claude":
            return self._claude_chat(messages, temperature, max_tokens, stream, **kwargs)
        else:
            return self._custom_chat(messages, temperature, max_tokens, stream, **kwargs)

    def _openai_chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float,
        max_tokens: Optional[int],
        stream: bool,
        **kwargs
    ) -> Dict[str, Any]:
        """
        OpenAI-compatible chat completion.
        OpenAI兼容的聊天补全。
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "stream": stream,
            **kwargs
        }

        if max_tokens:
            payload["max_tokens"] = max_tokens

        for attempt in range(self.max_retries):
            try:
                response = requests.post(
                    self.api_url,
                    headers=headers,
                    json=payload,
                    timeout=self.timeout,
                    stream=stream
                )

                response.raise_for_status()
                
                # If streaming, return the response object for iteration
                if stream:
                    return {
                        "success": True,
                        "stream": True,
                        "response": response,
                        "model": self.model,
                        "timestamp": datetime.now().isoformat()
                    }
                
                # Non-streaming response
                result = response.json()

                self.request_count += 1
                if "usage" in result:
                    self.total_tokens += result["usage"].get("total_tokens", 0)

                return {
                    "success": True,
                    "content": result["choices"][0]["message"]["content"],
                    "raw_response": result,
                    "model": self.model,
                    "timestamp": datetime.now().isoformat()
                }

            except requests.exceptions.RequestException as e:
                if attempt == self.max_retries - 1:
                    return {
                        "success": False,
                        "error": str(e),
                        "timestamp": datetime.now().isoformat()
                    }
                time.sleep(2 ** attempt)

        return {
            "success": False,
            "error": "Max retries exceeded",
            "timestamp": datetime.now().isoformat()
        }
    
    def parse_stream(self, response):
        """
        Parse streaming response from OpenAI-compatible API.
        解析OpenAI兼容API的流式响应。
        
        Yields:
            str: Content chunks as they arrive
        """
        for line in response.iter_lines():
            if line:
                line = line.decode('utf-8')
                if line.startswith('data: '):
                    data = line[6:]  # Remove 'data: ' prefix
                    if data == '[DONE]':
                        break
                    try:
                        chunk = json.loads(data)
                        if 'choices' in chunk and len(chunk['choices']) > 0:
                            delta = chunk['choices'][0].get('delta', {})
                            if 'content' in delta:
                                yield delta['content']
                    except json.JSONDecodeError:
                        continue

    def _claude_chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float,
        max_tokens: Optional[int],
        stream: bool,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Claude API chat completion.
        Claude API聊天补全。
        """
        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json"
        }

        system_message = ""
        user_messages = []

        for msg in messages:
            if msg["role"] == "system":
                system_message = msg["content"]
            else:
                user_messages.append(msg)

        payload = {
            "model": self.model,
            "messages": user_messages,
            "temperature": temperature,
            "max_tokens": max_tokens or 4096,
            **kwargs
        }

        if system_message:
            payload["system"] = system_message

        for attempt in range(self.max_retries):
            try:
                response = requests.post(
                    self.api_url,
                    headers=headers,
                    json=payload,
                    timeout=self.timeout
                )

                response.raise_for_status()
                result = response.json()

                self.request_count += 1
                if "usage" in result:
                    self.total_tokens += result["usage"].get("input_tokens", 0)
                    self.total_tokens += result["usage"].get("output_tokens", 0)

                return {
                    "success": True,
                    "content": result["content"][0]["text"],
                    "raw_response": result,
                    "model": self.model,
                    "timestamp": datetime.now().isoformat()
                }

            except requests.exceptions.RequestException as e:
                if attempt == self.max_retries - 1:
                    return {
                        "success": False,
                        "error": str(e),
                        "timestamp": datetime.now().isoformat()
                    }
                time.sleep(2 ** attempt)

        return {
            "success": False,
            "error": "Max retries exceeded",
            "timestamp": datetime.now().isoformat()
        }

    def _custom_chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float,
        max_tokens: Optional[int],
        stream: bool,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Custom API chat completion.
        自定义API聊天补全。

        Attempts OpenAI format first, with fallback handling.
        首先尝试OpenAI格式，并提供回退处理。
        """
        return self._openai_chat(messages, temperature, max_tokens, stream, **kwargs)

    def get_stats(self) -> Dict[str, Any]:
        """
        Get usage statistics for this client.
        获取此客户端的使用统计信息。

        Returns:
            Dict containing usage stats / 包含使用统计信息的字典
        """
        return {
            "request_count": self.request_count,
            "total_tokens": self.total_tokens,
            "model": self.model,
            "api_type": self.api_type
        }

    def reset_stats(self) -> None:
        """
        Reset usage statistics.
        重置使用统计信息。
        """
        self.request_count = 0
        self.total_tokens = 0

    @classmethod
    def from_env(cls, api_type: str = "openai") -> "LLMClient":
        """
        Create LLMClient from environment variables.
        从环境变量创建LLMClient。

        Args:
            api_type: Type of API / API类型

        Returns:
            Configured LLMClient instance / 已配置的LLMClient实例

        Raises:
            ValueError: If required env vars are missing / 如果缺少必需的环境变量
        """
        api_url = os.getenv("LLM_API_URL")
        api_key = os.getenv("LLM_API_KEY")
        model = os.getenv("LLM_MODEL", "gpt-4")

        if not api_url or not api_key:
            raise ValueError(
                "Missing required environment variables: LLM_API_URL and LLM_API_KEY"
            )

        timeout = int(os.getenv("REQUEST_TIMEOUT", "60"))
        max_retries = int(os.getenv("MAX_RETRIES", "3"))

        return cls(
            api_url=api_url,
            api_key=api_key,
            model=model,
            timeout=timeout,
            max_retries=max_retries,
            api_type=api_type
        )

    def __repr__(self) -> str:
        """String representation of the client."""
        return f"LLMClient(model='{self.model}', api_type='{self.api_type}')"
