from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check_endpoint():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"

def test_get_roles_endpoint():
    response = client.get("/api/roles")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

def test_get_skills_endpoint():
    response = client.get("/api/skills")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

def test_portfolio_analysis_endpoint():
    payload = {
        "github_username": "",
        "target_role_id": 1,
        "current_skills": ["JavaScript", "React", "HTML", "CSS"],
        "years_experience": 2
    }
    response = client.post("/api/analysis", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert "analysis_id" in data
    assert "overall_score" in data
    assert "recommended_stacks" in data
    assert "roadmap" in data
