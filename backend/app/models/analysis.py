from datetime import datetime
from sqlalchemy import Column, Integer, Float, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class PortfolioAnalysis(Base):
    __tablename__ = "portfolio_analyses"

    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("developer_profiles.id", ondelete="CASCADE"), nullable=False)
    target_role_id = Column(Integer, ForeignKey("roles.id", ondelete="SET NULL"), nullable=True)
    
    # Portfolio Strength Scores (0 - 100)
    overall_score = Column(Float, nullable=False)
    skill_diversity_score = Column(Float, nullable=False)
    complexity_score = Column(Float, nullable=False)
    activity_score = Column(Float, nullable=False)
    documentation_score = Column(Float, nullable=False)
    relevance_score = Column(Float, nullable=False)
    
    skill_gaps_count = Column(Integer, default=0)
    raw_data_json = Column(Text, nullable=True)  # Stores JSON summary of extraction & analysis
    created_at = Column(DateTime, default=datetime.utcnow)

    profile = relationship("DeveloperProfile", back_populates="analyses")
    target_role = relationship("Role")
    recommendations = relationship("Recommendation", back_populates="analysis", cascade="all, delete-orphan")
    roadmaps = relationship("Roadmap", back_populates="analysis", cascade="all, delete-orphan")

class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, index=True)
    analysis_id = Column(Integer, ForeignKey("portfolio_analyses.id", ondelete="CASCADE"), nullable=False)
    recommended_stack_json = Column(Text, nullable=False)  # JSON array of recommended stacks
    explanation = Column(Text, nullable=True)
    similarity_score = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)

    analysis = relationship("PortfolioAnalysis", back_populates="recommendations")

class Roadmap(Base):
    __tablename__ = "roadmaps"

    id = Column(Integer, primary_key=True, index=True)
    analysis_id = Column(Integer, ForeignKey("portfolio_analyses.id", ondelete="CASCADE"), nullable=False)
    steps_json = Column(Text, nullable=False)  # JSON array of phase steps
    estimated_weeks = Column(Integer, default=8)
    created_at = Column(DateTime, default=datetime.utcnow)

    analysis = relationship("PortfolioAnalysis", back_populates="roadmaps")
