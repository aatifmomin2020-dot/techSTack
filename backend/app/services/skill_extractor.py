import re
from typing import List, Dict, Any, Set, Optional
from sqlalchemy.orm import Session
from app.models import Skill

class SkillExtractor:
    # Centralized alias mapping dictionary for fallback & fast lookup
    STATIC_ALIASES: Dict[str, str] = {
        "js": "JavaScript",
        "ecmascript": "JavaScript",
        "ts": "TypeScript",
        "py": "Python",
        "python3": "Python",
        "cpp": "C++",
        "cplusplus": "C++",
        "csharp": "C#",
        ".net": "C#",
        "golang": "Go",
        "rustlang": "Rust",
        "reactjs": "React",
        "react.js": "React",
        "vue": "Vue.js",
        "vuejs": "Vue.js",
        "angularjs": "Angular",
        "ng": "Angular",
        "next": "Next.js",
        "nextjs": "Next.js",
        "sveltejs": "Svelte",
        "tailwind": "Tailwind CSS",
        "tailwindcss": "Tailwind CSS",
        "node": "Node.js",
        "nodejs": "Node.js",
        "express": "Express.js",
        "expressjs": "Express.js",
        "fastapi": "FastAPI",
        "drf": "Django",
        "django-rest-framework": "Django",
        "springboot": "Spring Boot",
        "spring": "Spring Boot",
        "nestjs": "NestJS",
        "restful": "REST API",
        "rest": "REST API",
        "postgres": "PostgreSQL",
        "pg": "PostgreSQL",
        "postgresql": "PostgreSQL",
        "mariadb": "MySQL",
        "mongo": "MongoDB",
        "valkey": "Redis",
        "sqlite3": "SQLite",
        "firestore": "Firebase",
        "container": "Docker",
        "containers": "Docker",
        "k8s": "Kubernetes",
        "kube": "Kubernetes",
        "aws cloud": "AWS",
        "amazon web services": "AWS",
        "gcp": "Google Cloud",
        "google cloud platform": "Google Cloud",
        "microsoft azure": "Azure",
        "github actions": "CI/CD",
        "gitlab ci": "CI/CD",
        "jenkins": "CI/CD",
        "torch": "PyTorch",
        "tf": "TensorFlow",
        "keras": "TensorFlow",
        "sklearn": "Scikit-learn",
        "scikit": "Scikit-learn",
        "llm": "LangChain",
        "rag": "LangChain",
        "testing library": "Jest"
    }

    def __init__(self, db: Session = None):
        self.db = db
        self.skill_catalog: Dict[str, Dict[str, Any]] = {}
        self.alias_lookup: Dict[str, str] = dict(self.STATIC_ALIASES)
        self._load_catalog()

    def _load_catalog(self):
        """Loads canonical skills and aliases from database or static default."""
        if self.db:
            skills = self.db.query(Skill).all()
            for s in skills:
                canonical_name = s.name
                self.skill_catalog[canonical_name.lower()] = {
                    "id": s.id,
                    "name": canonical_name,
                    "category": s.category,
                    "description": s.description
                }
                # Register canonical name as its own lookup key
                self.alias_lookup[canonical_name.lower()] = canonical_name

                # Register aliases
                if s.aliases:
                    for alias in s.aliases.split(","):
                        cleaned_alias = alias.strip().lower()
                        if cleaned_alias:
                            self.alias_lookup[cleaned_alias] = canonical_name

    def normalize_skill(self, input_text: str) -> Optional[str]:
        """Maps any skill name or alias to its canonical representation."""
        if not input_text:
            return None
        clean = input_text.strip().lower()
        if clean in self.alias_lookup:
            return self.alias_lookup[clean]
        
        # Word boundary search if exact match fails
        for alias_key, canonical_name in self.alias_lookup.items():
            if len(alias_key) >= 3 and alias_key in clean:
                return canonical_name
        return None

    def extract_from_github_data(self, github_data: Dict[str, Any], user_entered_skills: List[str] = None) -> List[Dict[str, Any]]:
        """
        Extracts and normalizes skills from GitHub repos, topics, READMEs, and manual user inputs.
        """
        extracted_skills: Dict[str, Dict[str, Any]] = {}

        # 1. Process manual user skills (High confidence)
        if user_entered_skills:
            for raw_skill in user_entered_skills:
                canonical = self.normalize_skill(raw_skill) or raw_skill.strip()
                if canonical:
                    cat = self.skill_catalog.get(canonical.lower(), {}).get("category", "General")
                    extracted_skills[canonical] = {
                        "name": canonical,
                        "category": cat,
                        "source": "manual",
                        "confidence": 1.0,
                        "occurrences": 1
                    }

        if not github_data:
            return list(extracted_skills.values())

        # 2. Process primary languages from repositories
        languages_summary = github_data.get("languages_summary", {})
        for lang, count in languages_summary.items():
            canonical = self.normalize_skill(lang) or lang.strip()
            cat = self.skill_catalog.get(canonical.lower(), {}).get("category", "Programming Language")
            if canonical in extracted_skills:
                extracted_skills[canonical]["confidence"] = max(extracted_skills[canonical]["confidence"], 0.9)
                extracted_skills[canonical]["occurrences"] += count
            else:
                extracted_skills[canonical] = {
                    "name": canonical,
                    "category": cat,
                    "source": "github_language",
                    "confidence": 0.9,
                    "occurrences": count
                }

        # 3. Process repository topics
        topics_summary = github_data.get("topics_summary", [])
        for topic in topics_summary:
            canonical = self.normalize_skill(topic)
            if canonical:
                cat = self.skill_catalog.get(canonical.lower(), {}).get("category", "Tools & Frameworks")
                if canonical in extracted_skills:
                    extracted_skills[canonical]["occurrences"] += 1
                else:
                    extracted_skills[canonical] = {
                        "name": canonical,
                        "category": cat,
                        "source": "github_topic",
                        "confidence": 0.85,
                        "occurrences": 1
                    }

        # 4. Process repository descriptions and READMEs text
        repositories = github_data.get("repositories", [])
        for repo in repositories:
            text_corpus = f"{repo.get('description', '')} {repo.get('readme_content', '')}".lower()
            if not text_corpus.strip():
                continue

            # Tokenize & search catalog skills in corpus
            for canonical_key, meta in self.skill_catalog.items():
                canonical_name = meta["name"]
                if canonical_name in extracted_skills:
                    continue

                # Search pattern using word boundaries
                pattern = r'\b' + re.escape(canonical_key) + r'\b'
                if re.search(pattern, text_corpus):
                    extracted_skills[canonical_name] = {
                        "name": canonical_name,
                        "category": meta["category"],
                        "source": "github_readme",
                        "confidence": 0.75,
                        "occurrences": 1
                    }

        return list(extracted_skills.values())
