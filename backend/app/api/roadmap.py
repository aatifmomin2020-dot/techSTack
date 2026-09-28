from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models import Roadmap
from app.services.roadmap_generator import RoadmapGenerator
import json

router = APIRouter(prefix="/api/roadmap", tags=["Learning Roadmap"])

class RoadmapRequest(BaseModel):
    missing_skills: List[str]
    current_skills: Optional[List[str]] = []
    target_role: Optional[str] = "Full Stack Developer"

@router.post("")
def generate_learning_roadmap(request: RoadmapRequest):
    """
    Generates a personalized step-by-step learning roadmap for missing skills.
    """
    generator = RoadmapGenerator()
    missing_items = [{"name": s, "is_required": True} for s in request.missing_skills]
    roadmap_data = generator.generate_roadmap(
        missing_skills=missing_items,
        user_existing_skills=request.current_skills,
        target_role_name=request.target_role
    )
    return roadmap_data

@router.get("/{id}")
def get_roadmap_by_id(id: int, db: Session = Depends(get_db)):
    roadmap = db.query(Roadmap).filter(Roadmap.id == id).first()
    if not roadmap:
        raise HTTPException(status_code=404, detail="Roadmap not found")
    
    return {
        "id": roadmap.id,
        "estimated_weeks": roadmap.estimated_weeks,
        "phases": json.loads(roadmap.steps_json)
    }
