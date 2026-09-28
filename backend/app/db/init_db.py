import os
import pandas as pd
from sqlalchemy.orm import Session
from app.db.database import engine, Base, SessionLocal
from app.models import Skill, Role, RoleSkill, Project, ProjectSkill

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../data"))

def init_db(db: Session = None):
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    close_session = False
    if db is None:
        db = SessionLocal()
        close_session = True

    try:
        # Seed Skills
        if db.query(Skill).count() == 0:
            skills_path = os.path.join(DATA_DIR, "skills.csv")
            if os.path.exists(skills_path):
                df_skills = pd.read_csv(skills_path)
                for _, row in df_skills.iterrows():
                    skill = Skill(
                        id=int(row["id"]),
                        name=str(row["name"]).strip(),
                        category=str(row["category"]).strip(),
                        aliases=str(row["aliases"]).strip() if pd.notna(row["aliases"]) else "",
                        description=str(row["description"]).strip() if pd.notna(row["description"]) else ""
                    )
                    db.add(skill)
                db.commit()

        # Seed Roles
        if db.query(Role).count() == 0:
            roles_path = os.path.join(DATA_DIR, "roles.csv")
            if os.path.exists(roles_path):
                df_roles = pd.read_csv(roles_path)
                for _, row in df_roles.iterrows():
                    role = Role(
                        id=int(row["id"]),
                        name=str(row["name"]).strip(),
                        description=str(row["description"]).strip() if pd.notna(row["description"]) else "",
                        category=str(row["category"]).strip() if pd.notna(row["category"]) else "",
                        min_experience_years=int(row["min_experience_years"]) if pd.notna(row["min_experience_years"]) else 1
                    )
                    db.add(role)
                db.commit()

        # Seed Role Skills
        if db.query(RoleSkill).count() == 0:
            role_skills_path = os.path.join(DATA_DIR, "role_skills.csv")
            if os.path.exists(role_skills_path):
                df_rs = pd.read_csv(role_skills_path)
                all_skills = db.query(Skill).all()
                skill_map = {s.name.lower(): s.id for s in all_skills}
                
                for _, row in df_rs.iterrows():
                    role_id = int(row["role_id"])
                    s_name = str(row["skill_name"]).strip().lower()
                    if s_name in skill_map:
                        rs = RoleSkill(
                            role_id=role_id,
                            skill_id=skill_map[s_name],
                            is_required=bool(row["is_required"]),
                            importance_score=float(row["importance_score"])
                        )
                        db.add(rs)
                db.commit()

        # Seed Projects
        if db.query(Project).count() == 0:
            projects_path = os.path.join(DATA_DIR, "projects.csv")
            if os.path.exists(projects_path):
                df_projects = pd.read_csv(projects_path)
                for _, row in df_projects.iterrows():
                    proj = Project(
                        id=int(row["id"]),
                        name=str(row["name"]).strip(),
                        description=str(row["description"]).strip(),
                        difficulty=str(row["difficulty"]).strip(),
                        learning_value=str(row["learning_value"]).strip(),
                        target_role_category=str(row["target_role_category"]).strip() if pd.notna(row["target_role_category"]) else ""
                    )
                    db.add(proj)
                db.commit()

        # Seed Project Skills
        if db.query(ProjectSkill).count() == 0:
            project_skills_path = os.path.join(DATA_DIR, "project_skills.csv")
            if os.path.exists(project_skills_path):
                df_ps = pd.read_csv(project_skills_path)
                all_skills = db.query(Skill).all()
                skill_map = {s.name.lower(): s.id for s in all_skills}
                
                for _, row in df_ps.iterrows():
                    project_id = int(row["project_id"])
                    s_name = str(row["skill_name"]).strip().lower()
                    if s_name in skill_map:
                        ps = ProjectSkill(
                            project_id=project_id,
                            skill_id=skill_map[s_name],
                            role_in_project=str(row["role_in_project"]).strip() if pd.notna(row["role_in_project"]) else ""
                        )
                        db.add(ps)
                db.commit()

    finally:
        if close_session:
            db.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized and seeded successfully!")
