from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models import Skill, Role, RoleSkill
from app.config import settings

router = APIRouter(tags=["System & Metadata"])

@router.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "app_name": settings.APP_NAME,
        "database": settings.DATABASE_URL.split("://")[0]
    }

@router.get("/api/skills")
def get_all_skills(db: Session = Depends(get_db)):
    skills = db.query(Skill).all()
    return [{
        "id": s.id,
        "name": s.name,
        "category": s.category,
        "aliases": s.aliases.split(",") if s.aliases else [],
        "description": s.description
    } for s in skills]

@router.get("/api/roles")
def get_all_roles(db: Session = Depends(get_db)):
    roles = db.query(Role).all()
    res = []
    for r in roles:
        r_skills = db.query(RoleSkill).filter(RoleSkill.role_id == r.id).all()
        required_techs = [rs.skill.name for rs in r_skills if rs.is_required]
        res.append({
            "id": r.id,
            "name": r.name,
            "description": r.description,
            "category": r.category,
            "min_experience_years": r.min_experience_years,
            "required_technologies": required_techs
        })
    return res

@router.get("/api/roles/{role_identifier}")
def get_role_by_id_or_name(role_identifier: str, db: Session = Depends(get_db)):
    if role_identifier.isdigit():
        role = db.query(Role).filter(Role.id == int(role_identifier)).first()
    else:
        role = db.query(Role).filter(Role.name.ilike(role_identifier.strip())).first()

    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    r_skills = db.query(RoleSkill).filter(RoleSkill.role_id == role.id).all()
    skills_detail = [{
        "name": rs.skill.name,
        "category": rs.skill.category,
        "is_required": rs.is_required,
        "importance_score": rs.importance_score
    } for rs in r_skills]

    return {
        "id": role.id,
        "name": role.name,
        "description": role.description,
        "category": role.category,
        "min_experience_years": role.min_experience_years,
        "skills": skills_detail
    }
