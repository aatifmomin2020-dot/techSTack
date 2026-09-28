from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from app.db.database import Base

class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    category = Column(String(50), index=True, nullable=False)  # Programming Language, Frontend, Backend, etc.
    aliases = Column(Text, nullable=True)  # Comma-separated or JSON list of aliases
    description = Column(Text, nullable=True)

    developer_skills = relationship("DeveloperSkill", back_populates="skill")
    role_skills = relationship("RoleSkill", back_populates="skill")
    project_skills = relationship("ProjectSkill", back_populates="skill")
