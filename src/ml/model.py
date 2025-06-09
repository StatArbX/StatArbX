from sklearn.ensemble import RandomForestClassifier


class PairProfitModel:
    def __init__(self):
        self.model = RandomForestClassifier()

    def train(self, X, y):
        self.model.fit(X, y)

    def predict(self, X):
        return self.model.predict_proba(X)[:, 1]  # probability of class 1 (profitable)
