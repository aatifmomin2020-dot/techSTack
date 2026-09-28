from typing import List, Dict, Any

class RoadmapGenerator:
    """
    Generates a personalized, step-by-step multi-phase learning roadmap
    based on missing skills, skill dependency graphs, role importance, and portfolio projects.
    """

    # Skill dependency graph mapping skills to their required prerequisites
    PREREQUISITES_GRAPH = {
        "TypeScript": ["JavaScript"],
        "React": ["JavaScript", "HTML", "CSS"],
        "Next.js": ["React", "JavaScript"],
        "Vue.js": ["JavaScript", "HTML", "CSS"],
        "Angular": ["TypeScript", "JavaScript"],
        "Redux": ["React", "JavaScript"],
        "FastAPI": ["Python", "REST API"],
        "Django": ["Python", "SQL"],
        "Flask": ["Python"],
        "Pandas": ["Python"],
        "NumPy": ["Python"],
        "Scikit-learn": ["Python", "Pandas", "NumPy"],
        "PyTorch": ["Python", "NumPy"],
        "TensorFlow": ["Python", "NumPy"],
        "LangChain": ["Python", "FastAPI"],
        "PostgreSQL": ["SQL"],
        "MySQL": ["SQL"],
        "Redis": ["PostgreSQL"],
        "Docker": ["Linux"],
        "Kubernetes": ["Docker", "Linux"],
        "AWS": ["Linux", "Docker"],
        "Terraform": ["AWS", "Docker"],
        "CI/CD": ["Git", "Docker"]
    }

    # Estimated learning effort (in hours) per technology
    LEARNING_ESTIMATES = {
        "TypeScript": {"hours": 20, "difficulty": "Beginner-Intermediate"},
        "PostgreSQL": {"hours": 25, "difficulty": "Intermediate"},
        "Docker": {"hours": 30, "difficulty": "Intermediate"},
        "Kubernetes": {"hours": 45, "difficulty": "Advanced"},
        "AWS": {"hours": 40, "difficulty": "Intermediate-Advanced"},
        "PyTorch": {"hours": 50, "difficulty": "Advanced"},
        "FastAPI": {"hours": 15, "difficulty": "Intermediate"},
        "React": {"hours": 35, "difficulty": "Intermediate"},
        "LangChain": {"hours": 25, "difficulty": "Intermediate"},
        "Terraform": {"hours": 30, "difficulty": "Intermediate"}
    }

    def generate_roadmap(self, missing_skills: List[Dict[str, Any]], user_existing_skills: List[str], target_role_name: str, recommended_projects: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        existing_set = {s.strip().lower() for s in user_existing_skills if s}

        # Filter out skills developer already possesses
        skills_to_learn = [s for s in missing_skills if s["name"].lower() not in existing_set]

        # Sort skills by prerequisites and importance score
        def dependency_weight(skill_item):
            name = skill_item["name"]
            prereqs = self.PREREQUISITES_GRAPH.get(name, [])
            unmet_prereqs = [p for p in prereqs if p.lower() not in existing_set]
            importance = skill_item.get("importance_score", 0.5)
            # Prioritize items with 0 unmet prereqs and high importance
            return (len(unmet_prereqs), -importance)

        skills_to_learn.sort(key=dependency_weight)

        phases = []
        milestone_project = recommended_projects[0]["name"] if recommended_projects else "Full Stack Portfolio Project"

        for idx, item in enumerate(skills_to_learn[:6]):
            s_name = item["name"]
            prereqs = self.PREREQUISITES_GRAPH.get(s_name, [])
            est = self.LEARNING_ESTIMATES.get(s_name, {"hours": 20, "difficulty": "Intermediate"})
            
            phase_num = idx + 1
            reason = f"Essential technology for {target_role_name}. Mastering {s_name} bridges a critical skill gap."

            phases.append({
                "phase": phase_num,
                "title": f"Phase {phase_num}: {s_name} Mastery",
                "skill": s_name,
                "category": item.get("category", "General"),
                "priority": "High" if item.get("is_required", True) else "Medium",
                "estimated_hours": est["hours"],
                "difficulty_level": est["difficulty"],
                "prerequisites": prereqs,
                "reason": reason,
                "recommended_project": milestone_project if idx == 0 else f"Build a feature incorporating {s_name}"
            })

        total_weeks = max(len(phases) * 2, 4)

        return {
            "total_phases": len(phases),
            "estimated_weeks": total_weeks,
            "target_role": target_role_name,
            "phases": phases
        }
