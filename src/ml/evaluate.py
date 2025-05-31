# src/ml/evaluate.py
def precision_at_k(preds, truths, k=5):
    top_preds = preds[:k]
    hits = sum(1 for (a, b) in top_preds if (a, b) in truths)
    return hits / k
