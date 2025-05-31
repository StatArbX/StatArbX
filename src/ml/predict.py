# src/ml/predict.py
from .features import extract_features
import numpy as np


def predict_top_pairs(model, price_df, pairs, top_n=5):
    feature_matrix = []
    for a, b in pairs:
        fa = price_df[a].dropna()
        fb = price_df[b].dropna()
        if len(fa) < 30 or len(fb) < 30:
            continue
        try:
            features = extract_features(fa, fb)
            feature_matrix.append((a, b, features))
        except:
            continue

    X = np.vstack([f for _, _, f in feature_matrix])
    scores = model.predict(X)

    pair_scores = [(a, b, s) for (a, b, _), s in zip(feature_matrix, scores)]
    pair_scores.sort(key=lambda x: x[2], reverse=True)
    return pair_scores[:top_n]
