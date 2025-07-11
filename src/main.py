import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

from core.data_loader import DataLoader


def load_and_prepare_data():
    # Load training data
    X_train = pd.read_csv("data/X_train.csv")
    y_train = pd.read_csv("data/y_train.csv")
    train_df = X_train.merge(y_train, on="ID")
    train_df["SIGN_TARGET"] = train_df["RET_TARGET"].apply(lambda x: 1 if x > 0 else -1)

    # Load test data
    X_test = pd.read_csv("data/X_test.csv")

    return train_df, X_test


def train_models(train_df):
    models = {}
    features = [col for col in train_df.columns if col.startswith("RET_") and col != "RET_TARGET"]

    # Train one model per liquid asset (ID_TARGET)
    for i, target_id in enumerate(train_df["ID_TARGET"].unique()):
        subset = train_df[train_df["ID_TARGET"] == target_id]
        X = subset[features]
        y = subset["SIGN_TARGET"]

        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X, y)
        models[target_id] = model

        if i % 10 == 0:
            print(f"Trained {i+1} / 100 models...")

    joblib.dump(models, "models/liquid_models.pkl")
    print(f"[ML] Trained {len(models)} models (1 per liquid asset)")
    return models


def predict(models, X_test):
    features = [col for col in X_test.columns if col.startswith("RET_")]
    predictions = []

    for _, row in X_test.iterrows():
        target_id = row["ID_TARGET"]
        model = models.get(target_id)
        if model:
            x_input = row[features].to_frame().T
            pred = model.predict(x_input)[0]
        else:
            pred = np.random.choice([-1, 1])  # fallback
        predictions.append(pred)

    X_test["RET_TARGET"] = predictions
    X_test[["ID", "RET_TARGET"]].to_csv("submission.csv", index=False)
    print("[✓] Submission file saved as 'submission.csv'")


def main():
    train_df, X_test = load_and_prepare_data()
    models = train_models(train_df)
    predict(models, X_test)


if __name__ == "__main__":
    main()
