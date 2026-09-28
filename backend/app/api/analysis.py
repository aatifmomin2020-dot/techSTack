import json
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models import DeveloperProfile, DeveloperSkill, Skill, Role, PortfolioAnalysis, Recommendation, Roadmap
from app.schemas.analysis import AnalysisRequest, AnalysisResponse
from app.services.github_service import GithubService, GithubServiceError
from app.services.skill_extractor import SkillExtractor
from app.services.portfolio_analyzer import PortfolioAnalyzer
from app.services.skill_gap_analyzer import SkillGapAnalyzer
from app.services.recommendation_engine import RecommendationEngine
from app.services.roadmap_generator import RoadmapGenerator
from app.services.gemini_service import GeminiService

router = APIRouter(prefix="/api/analysis", tags=["Portfolio Analysis"])

@router.post("", response_model=AnalysisResponse, status_code=status.HTTP_201_CREATED)
async def create_portfolio_analysis(request: AnalysisRequest, db: Session = Depends(get_db)):
    """
    Executes complete end-to-end Developer Portfolio Analysis pipeline:
    GitHub Fetch -> Skill Extraction & Normalization -> Portfolio Strength Scoring ->
    Skill Gap Analysis -> ML Tech Stack Recommendation -> Project Recommendation ->
    Learning Roadmap Generation -> Gemini AI Career Feedback -> Database Persistence.
    """
    github_data = None
    if request.github_username and request.github_username.strip():
        gh_service = GithubService()
        try:
            github_data = await gh_service.fetch_user_data(request.github_username.strip())
        except GithubServiceError as e:
            # If GitHub API fails or username doesn't exist, log and proceed with manual skills
            pass
        except Exception:
            pass

    # 1. Skill Extraction & Normalization
    extractor = SkillExtractor(db=db)
    extracted_skills = extractor.extract_from_github_data(
        github_data=github_data,
        user_entered_skills=request.current_skills or []
    )

    # 2. Portfolio Strength Scoring
    analyzer = PortfolioAnalyzer()
    score_res = analyzer.analyze_portfolio(extracted_skills, github_data)

    # 3. Skill Gap Detection
    gap_analyzer = SkillGapAnalyzer(db=db)
    gap_res = gap_analyzer.analyze_gaps(extracted_skills, request.target_role_id)

    target_role_info = gap_res["target_role"]

    # 4. ML Recommendation Engine
    rec_engine = RecommendationEngine(db=db)
    user_skill_names = [s["name"] for s in extracted_skills]
    recommended_stacks = rec_engine.recommend_tech_stacks(user_skill_names, target_role_info["name"])

    # 5. Project Recommendation Engine
    missing_required = gap_res["missing_required_skills"] + gap_res["missing_optional_skills"]
    recommended_projects = rec_engine.recommend_projects(missing_required, target_role_info.get("category"))

    # 6. Personalized Learning Roadmap Generation
    roadmap_gen = RoadmapGenerator()
    roadmap_res = roadmap_gen.generate_roadmap(
        missing_skills=missing_required,
        user_existing_skills=user_skill_names,
        target_role_name=target_role_info["name"],
        recommended_projects=recommended_projects
    )

    # 7. Gemini AI Service Feedback
    gemini_svc = GeminiService()
    ai_feedback = await gemini_svc.generate_portfolio_feedback(
        username=request.github_username or "Developer",
        target_role=target_role_info["name"],
        portfolio_score=score_res["overall_score"],
        existing_skills=user_skill_names,
        missing_skills=missing_required
    )

    # 8. Database Persistence
    profile = DeveloperProfile(
        github_username=request.github_username,
        target_role_id=request.target_role_id,
        years_experience=request.years_experience or 1
    )
    db.add(profile)
    db.commit()
    db.refresh(profile)

    # Persist Developer Skills
    for sk in extracted_skills:
        s_obj = db.query(Skill).filter(Skill.name == sk["name"]).first()
        if s_obj:
            ds = DeveloperSkill(
                profile_id=profile.id,
                skill_id=s_obj.id,
                proficiency_level="Intermediate",
                source=sk.get("source", "manual")
            )
            db.add(ds)

    analysis_record = PortfolioAnalysis(
        profile_id=profile.id,
        target_role_id=request.target_role_id,
        overall_score=score_res["overall_score"],
        skill_diversity_score=score_res["components"]["skill_diversity"],
        complexity_score=score_res["components"]["project_complexity"],
        activity_score=score_res["components"]["github_activity"],
        documentation_score=score_res["components"]["documentation_quality"],
        relevance_score=score_res["components"]["technology_relevance"],
        skill_gaps_count=len(missing_required),
        raw_data_json=json.dumps({
            "existing_skills": extracted_skills,
            "skill_gaps": gap_res,
            "score_explanation": score_res["explanation"],
            "ai_feedback": ai_feedback
        })
    )
    db.add(analysis_record)
    db.commit()
    db.refresh(analysis_record)

    # Persist Recommendations & Roadmap
    rec_record = Recommendation(
        analysis_id=analysis_record.id,
        recommended_stack_json=json.dumps(recommended_stacks),
        explanation=score_res["explanation"],
        similarity_score=recommended_stacks[0]["cosine_similarity"] if recommended_stacks else 0.0
    )
    db.add(rec_record)

    roadmap_record = Roadmap(
        analysis_id=analysis_record.id,
        steps_json=json.dumps(roadmap_res["phases"]),
        estimated_weeks=roadmap_res["estimated_weeks"]
    )
    db.add(roadmap_record)
    db.commit()

    return {
        "analysis_id": analysis_record.id,
        "github_username": request.github_username,
        "target_role": target_role_info,
        "overall_score": score_res["overall_score"],
        "score_breakdown": score_res["components"],
        "score_explanation": score_res["explanation"],
        "existing_skills": extracted_skills,
        "skill_gaps": gap_res,
        "recommended_stacks": recommended_stacks,
        "recommended_projects": recommended_projects,
        "roadmap": roadmap_res,
        "ai_feedback": ai_feedback,
        "github_data": github_data
    }

@router.get("/{analysis_id}")
def get_analysis_by_id(analysis_id: int, db: Session = Depends(get_db)):
    record = db.query(PortfolioAnalysis).filter(PortfolioAnalysis.id == analysis_id).first()
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Analysis record not found.")

    raw_data = json.loads(record.raw_data_json or "{}")
    rec_obj = db.query(Recommendation).filter(Recommendation.analysis_id == record.id).first()
    roadmap_obj = db.query(Roadmap).filter(Roadmap.analysis_id == record.id).first()

    role = db.query(Role).filter(Role.id == record.target_role_id).first()

    return {
        "analysis_id": record.id,
        "github_username": record.profile.github_username if record.profile else None,
        "target_role": {"id": role.id, "name": role.name, "category": role.category, "description": role.description} if role else {},
        "overall_score": record.overall_score,
        "score_breakdown": {
            "skill_diversity": record.skill_diversity_score,
            "project_complexity": record.complexity_score,
            "github_activity": record.activity_score,
            "documentation_quality": record.documentation_score,
            "technology_relevance": record.relevance_score
        },
        "score_explanation": raw_data.get("score_explanation", ""),
        "existing_skills": raw_data.get("existing_skills", []),
        "skill_gaps": raw_data.get("skill_gaps", {}),
        "recommended_stacks": json.loads(rec_obj.recommended_stack_json) if rec_obj else [],
        "roadmap": {"phases": json.loads(roadmap_obj.steps_json), "estimated_weeks": roadmap_obj.estimated_weeks} if roadmap_obj else {},
        "ai_feedback": raw_data.get("ai_feedback", {})
    }
