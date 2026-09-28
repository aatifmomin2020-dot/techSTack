import numpy as np
from typing import List, Dict, Any, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer

class FeatureEngineer:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(token_pattern=r"(?u)\b[\w\+\#\.\-]+\b")

    def create_skill_corpus(self, skill_list: List[str]) -> str:
        """Converts a list of skill names into a space-separated corpus string for TF-IDF."""
        return " ".join([s.strip().lower().replace(" ", "_") for s in skill_list if s])

    def fit_transform_profiles(self, corpus_list: List[str]) -> Tuple[np.ndarray, TfidfVectorizer]:
        """Fits TF-IDF vectorizer over candidate corpus and returns feature vectors matrix."""
        matrix = self.vectorizer.fit_transform(corpus_list)
        return matrix.toarray(), self.vectorizer

    def transform_profile(self, skill_list: List[str]) -> np.ndarray:
        """Transforms a user skill profile into a fitted TF-IDF feature vector."""
        corpus = self.create_skill_corpus(skill_list)
        return self.vectorizer.transform([corpus]).toarray()[0]
