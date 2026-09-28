from typing import List, Dict, Any, Set
from sqlalchemy.orm import Session
from app.models import Role, RoleSkill, Skill

class SkillGapAnalyzer:
    """
    Deterministic skill gap analysis comparing developer existing skills
    against required & optional technologies for a target career role.
    """

    def __init__(self, db: Session):
        self.db = db

    def analyze_gaps(self, user_skills: List[Dict[str, Any]], target_role_id: int) -> Dict[str, Any]:
        role = self.db.query(Role).filter(Role.id == target_role_id).first()
        if not role:
            # Fallback to default Full Stack Developer (id=3) if role not found
            role = self.db.query(Role).filter(Role.name == "Full Stack Developer").first()
            if not role:
                role = self.db.query(Role).first()

        role_skills = self.db.query(RoleSkill).filter(RoleSkill.role_id == role.id).all()

        user_skill_names: Set[str] = {
            s["name"].strip().lower() for s in user_skills if isinstance(s, dict) and "name" in s
        }

        matched_skills = []
        missing_required = []
        missing_optional = []

        total_required_count = 0

        for rs in role_skills:
            s_name = rs.skill.name
            s_category = rs.skill.category
            s_name_lower = s_name.lower()

            if rs.is_required:
                total_required_count += 1

            if s_name_lower in user_skill_names:
                matched_skills.append({
                    "name": s_name,
                    "category": s_category,
                    "is_required": rs.is_required,
                    "importance_score": rs.importance_score
                })
            else:
                gap_item = {
                    "name": s_name,
                    "category": s_category,
                    "is_required": rs.is_required,
                    "importance_score": rs.importance_score
                }
                if rs.is_required:
                    missing_required.append(gap_item)
                else:
                    missing_optional.append(gap_item)

        gap_percentage = 0.0
        if total_required_count > 0:
            missing_req_count = len(missing_required)
            gap_percentage = round((missing_req_count / float(total_required_count)) * 100.0, 1)

        match_percentage = round(100.0 - gap_percentage, 1)

        return {
            "target_role": {
                "id": role.id,
                "name": role.name,
                "category": role.category,
                "description": role.description
            },
            "match_percentage": match_percentage,
            "gap_percentage": gap_percentage,
            "matched_skills": matched_skills,
            "missing_required_skills": missing_required,
            "missing_optional_skills": missing_optional,
            "total_role_skills": len(role_skills)
        }
