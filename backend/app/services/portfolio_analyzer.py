from datetime import datetime, timezone
from typing import Dict, Any, List

class PortfolioAnalyzer:
    """
    Computes a 0-100 Portfolio Strength Score based on 5 empirical components:
    1. Skill Diversity (25%)
    2. Project Complexity (25%)
    3. GitHub Activity (20%)
    4. Documentation Quality (15%)
    5. Technology Relevance (15%)
    """

    WEIGHTS = {
        "skill_diversity": 0.25,
        "complexity": 0.25,
        "activity": 0.20,
        "documentation": 0.15,
        "relevance": 0.15
    }

    # High-demand skills for relevance score calculation
    HIGH_DEMAND_SKILLS = {
        "python", "react", "typescript", "javascript", "fastapi", "node.js",
        "postgresql", "docker", "kubernetes", "aws", "pytorch", "langchain",
        "ci/cd", "redis", "next.js", "graphql", "sql"
    }

    def analyze_portfolio(self, extracted_skills: List[Dict[str, Any]], github_data: Dict[str, Any] = None) -> Dict[str, Any]:
        # 1. Skill Diversity Score (0-100)
        diversity_score = self._calc_skill_diversity(extracted_skills)

        # If no GitHub data is provided, fall back to manual project/experience metrics
        if not github_data:
            complexity_score = min(len(extracted_skills) * 12.0, 80.0)
            activity_score = 65.0  # Default moderate baseline for manual entry
            documentation_score = 60.0
        else:
            complexity_score = self._calc_project_complexity(github_data)
            activity_score = self._calc_github_activity(github_data)
            documentation_score = self._calc_documentation_quality(github_data)

        # 5. Technology Relevance Score (0-100)
        relevance_score = self._calc_technology_relevance(extracted_skills)

        # Calculate total weighted score
        overall_score = (
            diversity_score * self.WEIGHTS["skill_diversity"] +
            complexity_score * self.WEIGHTS["complexity"] +
            activity_score * self.WEIGHTS["activity"] +
            documentation_score * self.WEIGHTS["documentation"] +
            relevance_score * self.WEIGHTS["relevance"]
        )

        overall_score = round(min(max(overall_score, 0.0), 100.0), 1)

        explanations = self._generate_score_explanation(
            overall_score, diversity_score, complexity_score, activity_score, documentation_score, relevance_score
        )

        return {
            "overall_score": overall_score,
            "components": {
                "skill_diversity": round(diversity_score, 1),
                "project_complexity": round(complexity_score, 1),
                "github_activity": round(activity_score, 1),
                "documentation_quality": round(documentation_score, 1),
                "technology_relevance": round(relevance_score, 1)
            },
            "explanation": explanations
        }

    def _calc_skill_diversity(self, skills: List[Dict[str, Any]]) -> float:
        if not skills:
            return 0.0
        
        categories: Set[str] = set(s.get("category", "General") for s in skills)
        num_skills = len(skills)

        # Category coverage bonus (up to 8 categories: Lang, Frontend, Backend, DB, Cloud, AI, Tools, Testing)
        cat_coverage_score = min((len(categories) / 6.0) * 60.0, 60.0)
        # Skill volume score
        volume_score = min((num_skills / 10.0) * 40.0, 40.0)

        return cat_coverage_score + volume_score

    def _calc_project_complexity(self, github_data: Dict[str, Any]) -> float:
        repos = github_data.get("repositories", [])
        if not repos:
            return 20.0

        repo_count = len(repos)
        total_stars = sum(r.get("stars", 0) for r in repos)
        total_forks = sum(r.get("forks", 0) for r in repos)
        multi_lang_repos = sum(1 for r in repos if r.get("topics") or r.get("readme_content"))

        star_score = min(total_stars * 5.0, 35.0)
        fork_score = min(total_forks * 8.0, 25.0)
        volume_score = min(repo_count * 3.0, 20.0)
        richness_score = min(multi_lang_repos * 4.0, 20.0)

        return star_score + fork_score + volume_score + richness_score

    def _calc_github_activity(self, github_data: Dict[str, Any]) -> float:
        public_repos = github_data.get("public_repos", 0)
        followers = github_data.get("followers", 0)
        repos = github_data.get("repositories", [])

        if public_repos == 0:
            return 10.0

        repo_score = min(public_repos * 4.0, 40.0)
        follower_score = min(followers * 5.0, 30.0)

        # Check recent update recency
        recency_score = 30.0
        if repos:
            latest_repo = repos[0]
            updated_at_str = latest_repo.get("updated_at")
            if updated_at_str:
                try:
                    updated_dt = datetime.fromisoformat(updated_at_str.replace("Z", "+00:00"))
                    days_ago = (datetime.now(timezone.utc) - updated_dt).days
                    if days_ago <= 30:
                        recency_score = 30.0
                    elif days_ago <= 90:
                        recency_score = 20.0
                    elif days_ago <= 180:
                        recency_score = 10.0
                    else:
                        recency_score = 5.0
                except Exception:
                    pass

        return repo_score + follower_score + recency_score

    def _calc_documentation_quality(self, github_data: Dict[str, Any]) -> float:
        repos = github_data.get("repositories", [])
        if not repos:
            return 30.0

        repos_with_desc = sum(1 for r in repos if r.get("description"))
        repos_with_topics = sum(1 for r in repos if r.get("topics"))
        repos_with_readme = sum(1 for r in repos if r.get("readme_content"))

        total = len(repos)
        desc_ratio = (repos_with_desc / total) * 35.0
        topic_ratio = (repos_with_topics / total) * 30.0
        readme_ratio = (repos_with_readme / min(total, 5)) * 35.0

        return desc_ratio + topic_ratio + readme_ratio

    def _calc_technology_relevance(self, skills: List[Dict[str, Any]]) -> float:
        if not skills:
            return 0.0

        user_skill_names = {s.get("name", "").lower() for s in skills}
        matches = user_skill_names.intersection(self.HIGH_DEMAND_SKILLS)
        
        # Max out score at 6 high-demand skills
        relevance = min((len(matches) / 6.0) * 100.0, 100.0)
        return relevance

    def _generate_score_explanation(self, overall: float, div: float, comp: float, act: float, doc: float, rel: float) -> str:
        parts = []
        if overall >= 80:
            parts.append("Outstanding portfolio! High technological diversity, strong documentation, and active repository management.")
        elif overall >= 65:
            parts.append("Solid portfolio with strong core capabilities. Expanding project complexity and documentation will elevate your profile.")
        else:
            parts.append("Developing portfolio. Focus on building multi-tier projects, adding detailed READMEs, and expanding your core technical stack.")

        if div < 60:
            parts.append("Consider broadening your skill stack across backend, frontend, and database layers.")
        if doc < 60:
            parts.append("Adding detailed README files and topics to your GitHub repositories will significantly improve recruiter visibility.")

        return " ".join(parts)
