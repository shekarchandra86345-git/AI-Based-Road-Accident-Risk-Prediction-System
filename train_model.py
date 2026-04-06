import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import pickle

# Load dataset
data = pd.read_csv("accident_data_v2.csv")

X = data.drop("risk", axis=1)
y = data["risk"]

# Train model with tuned hyperparameters
model = RandomForestClassifier(
    n_estimators=200,          # more trees = more stable
    max_depth=20,              # prevent shallow trees
    min_samples_leaf=2,        # reduce overfitting
    class_weight='balanced',   # fix class imbalance automatically
    random_state=42,
    n_jobs=-1                  # use all CPU cores for speed
)
model.fit(X, y)

# Save model
pickle.dump(model, open("model.pkl", "wb"))
print("Model trained successfully with 13 features.")
