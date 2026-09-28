import pytest
from app.services.skill_extractor import SkillExtractor

def test_skill_normalization():
    extractor = SkillExtractor()
    
    assert extractor.normalize_skill("JS") == "JavaScript"
    assert extractor.normalize_skill("ReactJS") == "React"
    assert extractor.normalize_skill("react.js") == "React"
    assert extractor.normalize_skill("Node") == "Node.js"
    assert extractor.normalize_skill("Postgres") == "PostgreSQL"
    assert extractor.normalize_skill("py") == "Python"
    assert extractor.normalize_skill("TS") == "TypeScript"
    assert extractor.normalize_skill("k8s") == "Kubernetes"

def test_skill_extraction_manual():
    extractor = SkillExtractor()
    user_skills = ["JS", "Python", "FastAPI", "Docker"]
    extracted = extractor.extract_from_github_data(github_data=None, user_entered_skills=user_skills)
    
    extracted_names = [s["name"] for s in extracted]
    assert "JavaScript" in extracted_names
    assert "Python" in extracted_names
    assert "FastAPI" in extracted_names
    assert "Docker" in extracted_names
