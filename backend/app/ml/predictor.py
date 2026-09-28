import numpy as np
from typing import List, Dict, Any
from app.ml.feature_engineering import FeatureEngineer
from app.ml.similarity import cosine_similarity

# Pre-curated production technology stack templates
CANDIDATE_STACKS = [
    {
        "id": "react-fastapi-pg-docker",
        "name": "Modern Full-Stack Python & React",
        "category": "Full Stack",
        "technologies": ["React", "TypeScript", "FastAPI", "PostgreSQL", "Docker", "Git"],
        "description": "High-performance full-stack architecture coupling a typed React frontend with a asynchronous Python FastAPI backend.",
        "target_roles": ["Full Stack Developer", "Python Developer", "Backend Developer"]
    },
    {
        "id": "react-node-mongo-docker",
        "name": "Full-Stack Node.js Enterprise (MERN+TS)",
        "category": "Full Stack",
        "technologies": ["React", "TypeScript", "Node.js", "Express.js", "MongoDB", "Redis", "Docker"],
        "description": "Scalable JavaScript/TypeScript ecosystem for fast full-stack product iteration.",
        "target_roles": ["Full Stack Developer", "Frontend Developer"]
    },
    {
        "id": "python-pytorch-fastapi-docker",
        "name": "Production AI & Machine Learning Pipeline Stack",
        "category": "AI / ML",
        "technologies": ["Python", "PyTorch", "FastAPI", "Scikit-learn", "Pandas", "NumPy", "Docker"],
        "description": "Robust ML engineering stack for serving deep learning inference models via containerized APIs.",
        "target_roles": ["Machine Learning Engineer", "AI Engineer", "Data Scientist"]
    },
    {
        "id": "langchain-fastapi-react-pg",
        "name": "Generative AI & LLM Agent Application Stack",
        "category": "AI / ML",
        "technologies": ["Python", "LangChain", "FastAPI", "React", "PostgreSQL", "Docker", "TypeScript"],
        "description": "Cutting-edge GenAI stack for RAG vector search applications and intelligent AI agents.",
        "target_roles": ["AI Engineer", "Full Stack Developer"]
    },
    {
        "id": "docker-k8s-aws-terraform",
        "name": "Cloud Native DevOps & Infrastructure Stack",
        "category": "Infrastructure",
        "technologies": ["Docker", "Kubernetes", "AWS", "Terraform", "CI/CD", "Linux", "Python"],
        "description": "Enterprise cloud infrastructure stack for automated IaC provisioning and Kubernetes cluster orchestration.",
        "target_roles": ["DevOps Engineer", "Cloud Engineer"]
    },
    {
        "id": "python-sql-pandas-postgres",
        "name": "Data Analytics & ETL Pipeline Stack",
        "category": "Data & Analytics",
        "technologies": ["Python", "SQL", "Pandas", "NumPy", "PostgreSQL", "Git"],
        "description": "Modern data stack for quantitative analysis, SQL data warehousing, and automated ETL data pipelines.",
        "target_roles": ["Data Analyst", "Data Scientist"]
    }
]

class TechStackPredictor:
    """
    ML Tech Stack Predictor utilizing TF-IDF Vectorization and Cosine Similarity
    to predict and rank optimal technology stacks for developers.
    """

    def __init__(self):
        self.fe = FeatureEngineer()
        self._initialize_stack_vectors()

    def _initialize_stack_vectors(self):
        corpus_list = [self.fe.create_skill_corpus(stack["technologies"]) for stack in CANDIDATE_STACKS]
        self.stack_vectors, self.vectorizer = self.fe.fit_transform_profiles(corpus_list)

    def predict_stacks(self, user_skills: List[str], target_role_name: str = "", top_k: int = 3) -> List[Dict[str, Any]]:
        user_vector = self.fe.transform_profile(user_skills)
        user_skills_set = {s.strip().lower() for s in user_skills if s}

        results = []

        for idx, stack in enumerate(CANDIDATE_STACKS):
            stack_vec = self.stack_vectors[idx]
            cos_sim = cosine_similarity(user_vector, stack_vec)

            stack_techs = stack["technologies"]
            stack_techs_set = {t.lower() for t in stack_techs}

            existing_in_stack = stack_techs_set.intersection(user_skills_set)
            missing_in_stack = stack_techs_set - user_skills_set

            # Role alignment bonus multiplier
            role_bonus = 1.15 if target_role_name in stack.get("target_roles", []) else 1.0

            # Calculate composite match score (0 - 100%)
            raw_score = (cos_sim * 0.6) + (len(existing_in_stack) / float(len(stack_techs)) * 0.4)
            final_score = round(min(raw_score * role_bonus * 100.0, 99.0), 1)

            missing_display = [t for t in stack_techs if t.lower() in missing_in_stack]
            existing_display = [t for t in stack_techs if t.lower() in existing_in_stack]

            results.append({
                "id": stack["id"],
                "name": stack["name"],
                "category": stack["category"],
                "match_score": final_score,
                "cosine_similarity": round(cos_sim, 3),
                "description": stack["description"],
                "technologies": stack["technologies"],
                "existing_skills": existing_display,
                "missing_skills_covered": missing_display,
                "reason": f"Matches {len(existing_display)} of your current skills while introducing key technologies ({', '.join(missing_display[:2])}) essential for {target_role_name or 'your growth'}."
            })

        # Sort by match score descending
        results.sort(key=lambda x: x["match_score"], reverse=True)
        return results[:top_k]
