from fastapi import APIRouter, Depends, Query
from typing import List, Optional
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models import Project, ProjectSkill
from app.services.recommendation_engine import RecommendationEngine

router = APIRouter(prefix="/api/projects", tags=["Projects"])

@router.get("/recommended")
def get_recommended_projects(
    missing_skills: Optional[str] = Query(None, description="Comma-separated missing skills"),
    target_role: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """
    Returns curated portfolio projects tailored to cover specific missing skills.
    """
    engine = RecommendationEngine(db=db)
    missing_list = []
    if missing_skills:
        missing_list = [{"name": s.strip()} for s in missing_skills.split(",") if s.strip()]
    
    projects = engine.recommend_projects(missing_list, target_role)
    return {"projects": projects}
