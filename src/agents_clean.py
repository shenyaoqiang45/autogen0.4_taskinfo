"""Clean agents implementation (replacement for corrupted `agents.py`)."""

from typing import List, Optional, Dict, Any
import logging

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat, SelectorGroupChat
from autogen_agentchat.conditions import MaxMessageTermination, TextMentionTermination
from autogen_agentchat.messages import TextMessage

from .config import get_model_client, settings, get_tavily_available
from .prompts import (
    TOPIC_ANALYZER_PROMPT,
    INFO_ENRICHER_PROMPT,
    SEARCH_AGENT_PROMPT,
    INTEGRATOR_PROMPT,
    ORCHESTRATOR_PROMPT,
)

logger = logging.getLogger(__name__)


def _make_agent(name: str, requested_model: str, temp: float, max_t: Optional[int], system_message: str, description: str) -> AssistantAgent:
    # If max_t is None, let get_model_client fall back to global settings.max_tokens
    mc = get_model_client(requested_model, temp, max_t)
    agent = AssistantAgent(
        name=name,
        model_client=mc,
        system_message=system_message,
        description=description,
    )
    max_disp = max_t if max_t is not None else 'default'
    logger.info(f"Agent {name} role='{description}' model={requested_model} (temp={temp}, max_tokens={max_disp})")
    return agent


def create_topic_analyzer() -> AssistantAgent:
    return _make_agent(
        name="TopicAnalyzer",
        requested_model="gpt-5-mini",
        temp=0.1,
        max_t=None,
        system_message=TOPIC_ANALYZER_PROMPT,
        description="分析用户主题，提取核心要素和关键词",
    )


def create_info_enricher() -> AssistantAgent:
    return _make_agent(
        name="InfoEnricher",
        requested_model="gpt-5",
        temp=0.2,
        max_t=None,
        system_message=INFO_ENRICHER_PROMPT,
        description="补充时间、地点、人物等详细信息",
    )


def create_search_agent() -> AssistantAgent:
    agent = _make_agent(
        name="SearchAgent",
        requested_model="gpt-5-mini",
        temp=0.1,
        max_t=None,
        system_message=SEARCH_AGENT_PROMPT,
        description="搜索和收集可靠的引用来源",
    )
    if get_tavily_available():
        logger.info("Tavily 可用：请在部署时为 SearchAgent 注入检索工具")
    return agent


def create_integrator() -> AssistantAgent:
    return _make_agent(
        name="Integrator",
        requested_model="gpt-5",
        temp=0.7,
        max_t=None,
        system_message=INTEGRATOR_PROMPT,
        description="整合所有信息，生成结构化的创作素材并输出完整叙事",
    )


def create_orchestrator() -> AssistantAgent:
    return _make_agent(
        name="Orchestrator",
        requested_model="gpt-5-mini",
        temp=0.1,
        max_t=None,
        system_message=ORCHESTRATOR_PROMPT,
        description="协调整个内容创作流程",
    )


def create_content_creation_team(model_overrides: Optional[Dict[str, Any]] = None) -> RoundRobinGroupChat:
    model_overrides = model_overrides or {}
    topic_analyzer = create_topic_analyzer()
    info_enricher = create_info_enricher()
    search_agent = create_search_agent()
    integrator = create_integrator()
    agents = [topic_analyzer, info_enricher, search_agent, integrator]
    logger.info("[Team] content creation team 模型摘要：")
    for a in agents:
        desc = getattr(a, "description", "")
        logger.info(f"  - {a.name}: role='{desc}'")
    termination = MaxMessageTermination(max_messages=min(settings.max_messages, len(agents) + 1)) | TextMentionTermination("TERMINATE")
    team = RoundRobinGroupChat(participants=agents, termination_condition=termination)
    return team


def create_selector_team() -> SelectorGroupChat:
    orchestrator = create_orchestrator()
    topic_analyzer = create_topic_analyzer()
    info_enricher = create_info_enricher()
    search_agent = create_search_agent()
    integrator = create_integrator()
    agents = [orchestrator, topic_analyzer, info_enricher, search_agent, integrator]
    logger.info("[Team] selector team 模型摘要：")
    for a in agents:
        desc = getattr(a, "description", "")
        logger.info(f"  - {a.name}: role='{desc}'")
    termination = MaxMessageTermination(max_messages=settings.max_messages) | TextMentionTermination("TERMINATE")
    model_client = get_model_client()
    team = SelectorGroupChat(participants=agents, model_client=model_client, termination_condition=termination)
    return team
