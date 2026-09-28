from app.services.portfolio_analyzer import PortfolioAnalyzer

def test_portfolio_score_calculation():
    analyzer = PortfolioAnalyzer()
    
    extracted_skills = [
        {"name": "Python", "category": "Programming Language"},
        {"name": "JavaScript", "category": "Programming Language"},
        {"name": "React", "category": "Frontend"},
        {"name": "FastAPI", "category": "Backend"},
        {"name": "PostgreSQL", "category": "Database"},
        {"name": "Docker", "category": "DevOps"}
    ]

    result = analyzer.analyze_portfolio(extracted_skills, github_data=None)

    assert "overall_score" in result
    assert 0.0 <= result["overall_score"] <= 100.0
    assert "components" in result
    assert result["components"]["skill_diversity"] > 0
    assert "explanation" in result
