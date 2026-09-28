import os
import pickle
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from app.ml.feature_engineering import FeatureEngineer
from app.ml.predictor import CANDIDATE_STACKS

MODEL_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../ml/models"))

def train_and_save_artifacts():
    """
    Trains the TF-IDF vectorizer over the technology skill corpus and candidate stacks
    and exports vectorizer.pkl and stack_vectors.npy artifacts.
    """
    os.makedirs(MODEL_DIR, exist_ok=True)
    fe = FeatureEngineer()
    
    corpus_list = [fe.create_skill_corpus(stack["technologies"]) for stack in CANDIDATE_STACKS]
    stack_vectors, vectorizer = fe.fit_transform_profiles(corpus_list)

    vectorizer_path = os.path.join(MODEL_DIR, "vectorizer.pkl")
    vectors_path = os.path.join(MODEL_DIR, "stack_vectors.npy")

    with open(vectorizer_path, "wb") as f:
        pickle.dump(vectorizer, f)

    np.save(vectors_path, stack_vectors)
    print(f"ML artifacts saved successfully to {MODEL_DIR}")

if __name__ == "__main__":
    train_and_save_artifacts()
