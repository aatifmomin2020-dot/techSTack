from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class DeveloperProfile(Base):
    __tablename__ = "developer_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    github_username = Column(String(100), index=True, nullable=True)
    bio = Column(Text, nullable=True)
    location = Column(String(100), nullable=True)
    years_experience = Column(Integer, default=1)
    target_role_id = Column(Integer, ForeignKey("roles.id", ondelete="SET NULL"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="profiles")
    target_role = relationship("Role")
    developer_skills = relationship("DeveloperSkill", back_populates="profile", cascade="all, delete-orphan")
    repositories = relationship("GithubRepository", back_populates="profile", cascade="all, delete-orphan")
    analyses = relationship("PortfolioAnalysis", back_populates="profile", cascade="all, delete-orphan")

class DeveloperSkill(Base):
    __tablename__ = "developer_skills"

    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("developer_profiles.id", ondelete="CASCADE"), nullable=False)
    skill_id = Column(Integer, ForeignKey("skills.id", ondelete="CASCADE"), nullable=False)
    proficiency_level = Column(String(50), default="Intermediate")  # Beginner, Intermediate, Advanced
    source = Column(String(50), default="manual")  # github, manual

    profile = relationship("DeveloperProfile", back_populates="developer_skills")
    skill = relationship("Skill", back_populates="developer_skills")

class GithubRepository(Base):
    __tablename__ = "github_repositories"

    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("developer_profiles.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(150), nullable=False)
    description = Column(Text, nullable=True)
    primary_language = Column(String(50), nullable=True)
    stars = Column(Integer, default=0)
    forks = Column(Integer, default=0)
    topics = Column(Text, nullable=True)  # JSON or comma-separated
    readme_content = Column(Text, nullable=True)
    repo_url = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    profile = relationship("DeveloperProfile", back_populates="repositories")
