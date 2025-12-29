"""
内容创作 Agent 系统
基于 AutoGen 0.4+
"""
from .agents_clean import (
    create_topic_analyzer,
    create_info_enricher,
    create_search_agent,
    create_integrator,
    create_orchestrator,
    create_content_creation_team,
    create_selector_team,
)
from .main import run_content_creation, interactive_mode
from .models import (
    TopicAnalysis,
    TimelineInfo,
    LocationInfo,
    PeopleInfo,
    Enrichment,
    Reference,
    ContentCreationResult,
)
from .config import settings

__version__ = "0.1.0"
__all__ = [
    "create_topic_analyzer",
    "create_info_enricher",
    "create_search_agent",
    "create_integrator",
    "create_orchestrator",
    "create_content_creation_team",
    "create_selector_team",
    "run_content_creation",
    "interactive_mode",
    "settings",
]
