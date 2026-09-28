from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class AnalysisRequest(BaseModel):
    github_username: Optional[str] = None
    target_role_id: int
    current_skills: Optional[List[str]] = []
    years_experience: Optional[int] = 1
    projects_input: Optional[List[str]] = []

class ScoreBreakdown(BaseModel):
    skill_diversity: float
    project_complexity: float
    github_activity: float
    documentation_quality: float
    technology_relevance: float

class AnalysisResponse(BaseModel):
    analysis_id: int
    github_username: Optional[str] = None
    target_role: Dict[str, Any]
    overall_score: float
    score_breakdown: ScoreBreakdown
    score_explanation: str
    existing_skills: List[Dict[str, Any]]
    skill_gaps: Dict[str, Any]
    recommended_stacks: List[Dict[str, Any]]
    recommended_projects: List[Dict[str, Any]]
    roadmap: Dict[str, Any]
    ai_feedback: Dict[str, str]
    github_data: Optional[Dict[str, Any]] = None
