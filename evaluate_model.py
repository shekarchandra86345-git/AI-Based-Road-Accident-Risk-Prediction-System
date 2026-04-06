import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.ensemble import RandomForestClassifier

# Load dataset
data = pd.read_csv("accident_data_v2.csv")
X = data.drop("risk", axis=1)
y = data["risk"]

# Split: 80% train, 20% test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train fresh model for evaluation
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)

# ── Results ──────────────────────────────────────────
print("=" * 55)
print("   ROAD ACCIDENT RISK PREDICTION - MODEL EVALUATION")
print("=" * 55)

acc = accuracy_score(y_test, y_pred)
print(f"\n✅ Overall Accuracy     : {acc * 100:.2f}%")
print(f"   Training samples    : {len(X_train)}")
print(f"   Testing samples     : {len(X_test)}")

print("\n── Classification Report ──────────────────────────────")
report = classification_report(
    y_test, y_pred,
    target_names=["Safe (0)", "Less Risky (1)", "Risky (2)"]
)
print(report)

print("── Confusion Matrix ───────────────────────────────────")
cm = confusion_matrix(y_test, y_pred)
labels = ["Safe", "Less Risky", "Risky"]
print(f"{'':>14}", end="")
for l in labels:
    print(f"{l:>12}", end="")
print()
for i, row in enumerate(cm):
    print(f"{labels[i]:>14}", end="")
    for val in row:
        print(f"{val:>12}", end="")
    print()

print("\n── Feature Importances ────────────────────────────────")
importances = pd.Series(model.feature_importances_, index=X.columns)
importances_sorted = importances.sort_values(ascending=False)
for feat, imp in importances_sorted.items():
    bar = "█" * int(imp * 60)
    print(f"  {feat:<22} {imp:.4f}  {bar}")

print("\n" + "=" * 55)
print("  Model is ready to defend in your viva presentation!")
print("=" * 55)
