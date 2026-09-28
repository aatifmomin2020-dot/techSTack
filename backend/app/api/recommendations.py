from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.services.recommendation_engine import RecommendationEngine

router = APIRouter(prefix="/api/recommendations", tags=["Recommendations"])

class TechStackRequest(BaseModel):
    user_skills: List[str]
    target_role: Optional[str] = "Full Stack Developer"

@router.post("")
def get_tech_stack_recommendations(request: TechStackRequest, db: Session = Depends(get_db)):
    """
    Returns top ML TF-IDF technology stack recommendations based on current user skills and target role.
    """
    engine = RecommendationEngine(db=db)
    stacks = engine.recommend_tech_stacks(request.user_skills, request.target_role)
    return {"recommended_stacks": stacks}
