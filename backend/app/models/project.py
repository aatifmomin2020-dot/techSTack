from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), unique=True, nullable=False)
    description = Column(Text, nullable=False)
    difficulty = Column(String(50), default="Intermediate")  # Beginner, Intermediate, Advanced
    learning_value = Column(String(50), default="High")  # Medium, High, Very High
    target_role_category = Column(String(50), nullable=True)

    project_skills = relationship("ProjectSkill", back_populates="project", cascade="all, delete-orphan")

class ProjectSkill(Base):
    __tablename__ = "project_skills"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    skill_id = Column(Integer, ForeignKey("skills.id", ondelete="CASCADE"), nullable=False)
    role_in_project = Column(String(100), nullable=True)  # e.g. Frontend UI, Database Storage, etc.

    project = relationship("Project", back_populates="project_skills")
    skill = relationship("Skill", back_populates="project_skills")
