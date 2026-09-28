from typing import List, Dict, Any
from sqlalchemy.orm import Session
from app.models import Project, ProjectSkill, Skill
from app.ml.predictor import TechStackPredictor

class RecommendationEngine:
    """
    Main recommendation engine combining ML TF-IDF Tech Stack prediction
    with DB-backed skill-gap project matching.
    """

    def __init__(self, db: Session):
        self.db = db
        self.predictor = TechStackPredictor()

    def recommend_tech_stacks(self, user_skills: List[str], target_role_name: str) -> List[Dict[str, Any]]:
        return self.predictor.predict_stacks(user_skills, target_role_name, top_k=3)

    def recommend_projects(self, missing_skills: List[Dict[str, Any]], target_role_category: str = None) -> List[Dict[str, Any]]:
        missing_names_set = {
            s["name"].strip().lower() for s in missing_skills if isinstance(s, dict) and "name" in s
        }

        all_projects = self.db.query(Project).all()
        scored_projects = []

        for proj in all_projects:
            proj_skills = self.db.query(ProjectSkill).filter(ProjectSkill.project_id == proj.id).all()
            p_skill_names = [ps.skill.name for ps in proj_skills]
            p_skill_set = {s.lower() for s in p_skill_names}

            # Count how many missing skills this project covers
            covered_missing = p_skill_set.intersection(missing_names_set)
            covered_missing_display = [s for s in p_skill_names if s.lower() in covered_missing]

            score = len(covered_missing) * 10

            # Target role category match bonus
            if target_role_category and proj.target_role_category and target_role_category.lower() in proj.target_role_category.lower():
                score += 15

            # Difficulty weight adjustment
            if proj.difficulty == "Intermediate":
                score += 5
            elif proj.difficulty == "Advanced":
                score += 8

            scored_projects.append({
                "id": proj.id,
                "name": proj.name,
                "description": proj.description,
                "difficulty": proj.difficulty,
                "learning_value": proj.learning_value,
                "target_role_category": proj.target_role_category,
                "required_skills": p_skill_names,
                "covered_missing_skills": covered_missing_display,
                "covered_count": len(covered_missing_display),
                "match_score": score,
                "explanation": f"Covers {len(covered_missing_display)} of your identified skill gaps ({', '.join(covered_missing_display[:3])})." if covered_missing_display else f"Builds strong foundational competence in {', '.join(p_skill_names[:3])}."
            })

        # Sort projects by match score descending
        scored_projects.sort(key=lambda x: (x["covered_count"], x["match_score"]), reverse=True)
        return scored_projects[:6]
