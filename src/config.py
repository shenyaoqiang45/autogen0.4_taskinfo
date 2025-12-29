"""
配置管理
加载环境变量和应用配置
"""
import os
from typing import Optional
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import logging

# 加载环境变量
load_dotenv()


class Settings(BaseSettings):
    """应用配置"""
    
    # LLM 配置
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    default_model: str = "gpt-5.2-all"
    temperature: float = 0.7
    max_tokens: int = 4096
    
    # WhatAI 中转 API 配置（支持 Claude 和 GPT 系列）
    whatai_api_key: Optional[str] = None
    whatai_base_url: str = "https://api.whatai.cc/v1"
    
    # DeepSeek 官方 API 配置
    deepseek_api_key: Optional[str] = None
    deepseek_base_url: str = "https://api.deepseek.com/v1"
    
    # MCP 工具配置
    tavily_api_key: Optional[str] = None
    amap_api_key: Optional[str] = None
    
    # 日志配置
    log_level: str = "INFO"
    
    # Agent 配置
    max_messages: int = 50  # 最大消息数
    max_rounds: int = 10  # 最大轮次
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# 全局配置实例
settings = Settings()


def get_model_client(model: Optional[str] = None, temperature: Optional[float] = None, max_tokens: Optional[int] = None):
    """获取模型客户端配置（可指定 model / temperature / max_tokens）。

    优先顺序：WhatAI -> DeepSeek -> OpenAI（当对应 API key 存在时）。
    参数会覆盖 `settings` 中的默认值（若提供）。
    """
    logger = logging.getLogger(__name__)

    model = model or settings.default_model
    temperature = temperature if temperature is not None else settings.temperature
    max_tokens = max_tokens if max_tokens is not None else settings.max_tokens

        
    # 其次使用 DeepSeek 官方 Reasoner（若配置了 DEEPSEEK_API_KEY）
    if settings.deepseek_api_key:
        logger.info(f"Using DeepSeek client (model=deepseek-chat, temperature={temperature})")
        return get_deepseek_client(temperature=temperature, max_tokens=max_tokens)


    # 优先使用 WhatAI 中转（若配置了 WHATAI_API_KEY）——按用户请求，强制使用 WhatAI 优先级
    if settings.whatai_api_key:
        logger.info(f"Using WhatAI relay (model={model}, temperature={temperature})")
        return get_whatai_client(model=model, temperature=temperature, max_tokens=max_tokens)

    # 回退到 OpenAI
    from autogen_ext.models.openai import OpenAIChatCompletionClient

    if not settings.openai_api_key:
        raise ValueError(
            "未配置 WHATAI_API_KEY、DEEPSEEK_API_KEY 或 OPENAI_API_KEY。请在 .env 文件中设置 API key。"
        )

    logger.info(f"Using OpenAI client (model={model}, temperature={temperature}, max_tokens={max_tokens})")
    return OpenAIChatCompletionClient(
        model=model,
        api_key=settings.openai_api_key,
        temperature=temperature,
        max_tokens=max_tokens,
    )


def get_tavily_available() -> bool:
    """检查 Tavily API 是否可用"""
    return settings.tavily_api_key is not None and settings.tavily_api_key != ""


def get_amap_available() -> bool:
    """检查高德地图 API 是否可用"""
    return settings.amap_api_key is not None and settings.amap_api_key != ""


def get_deepseek_client(temperature: float = 0.1, max_tokens: Optional[int] = None):
    """
    获取 DeepSeek-Reasoner 客户端
    
    Args:
        temperature: 温度参数
            - 0.0: 用于 Auditor，零温度审计
            - 0.1: 用于 Red Team，严格推理
    """
    from autogen_ext.models.openai import OpenAIChatCompletionClient

    if not settings.deepseek_api_key:
        raise ValueError(
            "未配置 DEEPSEEK_API_KEY。请在 .env 文件中设置 DeepSeek API key。"
        )

    kwargs = {}
    if max_tokens is not None:
        kwargs["max_tokens"] = max_tokens

    return OpenAIChatCompletionClient(
        model="deepseek-reasoner",
        api_key=settings.deepseek_api_key,
        base_url=settings.deepseek_base_url,
        temperature=temperature,
        model_info={
            "vision": False,
            "function_calling": False,
            "json_output": True,
            "family": "r1",
            "structured_output": True,
            "multiple_system_messages": True,
        },
        **kwargs,
    )


def get_whatai_client(model: str = "claude-sonnet-4-5-20250929", temperature: float = 0.3, max_tokens: Optional[int] = None):
    """
    获取 WhatAI 中转 API 客户端
    适用于：Planner (Claude) 和 Executor (GPT)
    
    Args:
        model: 模型名称
            - "claude-sonnet-4-5-20250929": Claude 4.5 for Planner
            - "gpt-5.2": GPT-5.2 for Executor
        temperature: 温度参数
            - 0.3: Planner，保持创造性
            - 0.2: Executor，工程化执行
    """
    from autogen_ext.models.openai import OpenAIChatCompletionClient
    
    if not settings.whatai_api_key:
        raise ValueError(
            "未配置 WHATAI_API_KEY。请在 .env 文件中设置 WhatAI API key。"
        )
    
    kwargs = {}
    if max_tokens is not None:
        kwargs["max_tokens"] = max_tokens

    # Provide minimal model_info for non-OpenAI/backchannel models so the wrapper accepts the model name
    model_info = {
        "vision": False,
        "function_calling": True,
        "json_output": False,
        "family": "gpt-like",
        "structured_output": False,
        "multiple_system_messages": True,
    }

    return OpenAIChatCompletionClient(
        model=model,
        api_key=settings.whatai_api_key,
        base_url=settings.whatai_base_url,
        temperature=temperature,
        model_info=model_info,
        **kwargs,
    )
    
