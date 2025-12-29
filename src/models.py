"""
数据模型定义
使用 Pydantic 定义结构化的数据模型
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class TopicAnalysis(BaseModel):
    """主题分析结果"""
    topic: str = Field(..., description="用户原始主题")
    topic_type: str = Field(..., description="主题类型：历史、科技、文化、社会等")
    core_elements: List[str] = Field(default_factory=list, description="核心要素列表")
    scope: str = Field(..., description="范围界定和边界说明")
    keywords: List[str] = Field(default_factory=list, description="关键词列表")


class TimelineInfo(BaseModel):
    """时间线信息"""
    key_dates: List[Dict[str, str]] = Field(
        default_factory=list, 
        description="关键时间点，格式：[{'date': '1760', 'event': '工业革命开始'}]"
    )
    time_period: Optional[str] = Field(None, description="时间段描述")
    historical_context: str = Field(default="", description="历史背景")


class LocationInfo(BaseModel):
    """地点信息"""
    places: List[Dict[str, str]] = Field(
        default_factory=list,
        description="相关地点，格式：[{'name': '地点名', 'description': '描述'}]"
    )
    geographic_info: List[str] = Field(default_factory=list, description="地理信息")
    environment: str = Field(default="", description="环境描述")


class PeopleInfo(BaseModel):
    """人物信息"""
    key_persons: List[Dict[str, str]] = Field(
        default_factory=list,
        description="关键人物，格式：[{'name': '姓名', 'role': '角色', 'background': '背景'}]"
    )
    relationships: List[str] = Field(default_factory=list, description="人物关系")


class Enrichment(BaseModel):
    """信息扩展结果"""
    time: TimelineInfo = Field(default_factory=TimelineInfo, description="时间信息")
    location: LocationInfo = Field(default_factory=LocationInfo, description="地点信息")
    people: PeopleInfo = Field(default_factory=PeopleInfo, description="人物信息")


class Reference(BaseModel):
    """引用来源"""
    title: str = Field(..., description="来源标题")
    url: str = Field(..., description="链接地址")
    source: str = Field(..., description="来源名称（网站、出版物等）")
    relevance: str = Field(..., description="相关性说明")
    credibility: str = Field(default="中", description="可信度评估：高、中、低")
    excerpt: Optional[str] = Field(None, description="摘录内容")


class ContentCreationResult(BaseModel):
    """内容创作最终结果"""
    topic: str = Field(..., description="主题")
    analysis: TopicAnalysis = Field(..., description="主题分析")
    enrichment: Enrichment = Field(..., description="信息扩展")
    references: List[Reference] = Field(default_factory=list, description="引用来源列表")
    integrated_output: str = Field(..., description="整合后的结构化输出")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="元数据")


class AgentMessage(BaseModel):
    """Agent 之间传递的消息"""
    sender: str = Field(..., description="发送者名称")
    content: str = Field(..., description="消息内容")
    data: Optional[Dict[str, Any]] = Field(None, description="结构化数据")
    message_type: str = Field(default="text", description="消息类型")
