import mlflow
import mlflow.sklearn
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import os

# 1. Load data
DATA_PATH = os.path.join("data", "processed", "listings_clean.csv")
df = pd.read_csv(DATA_PATH)
print("Data loaded: " + str(len(df)) + " rows")

# 2. Compute quality_score from README rules
def compute_score(row):
    score = 100
    if row["photo_count"] < 3:
        score -= 20
    if row["description_length"] < 100:
        score -= 15
    if row["surface"] > 0 and (row["price"] / row["surface"]) > 15000:
        score -= 10
    if row["rooms"] == 0:
        score -= 10
    if row["location_precision"] == "city":
        score -= 10
    return score

df["quality_score"] = df.apply(compute_score, axis=1)
print("Score range: " + str(df["quality_score"].min()) + " to " + str(df["quality_score"].max()))

# 3. Features and target
FEATURES = ["price", "surface", "photo_count", "description_length", "rooms"]
TARGET = "quality_score"
X = df[FEATURES]
y = df[TARGET]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. Hyperparameters
N_ESTIMATORS = 100
MAX_DEPTH = 6

# 5. MLflow experiment tracking
mlflow.set_experiment("scorimo-quality-scoring")

with mlflow.start_run():
    model = RandomForestRegressor(
        n_estimators=N_ESTIMATORS,
        max_depth=MAX_DEPTH,
        random_state=42
    )
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    mae = mean_absolute_error(y_test, preds)
    print("MAE: " + str(round(mae, 2)))

    mlflow.log_param("n_estimators", N_ESTIMATORS)
    mlflow.log_param("max_depth", MAX_DEPTH)
    mlflow.log_metric("mae", mae)

    mlflow.sklearn.log_model(
        sk_model=model,
        artifact_path="model",
        registered_model_name="scorimo-model"
    )

    print("Model logged and registered to MLflow Registry")
    print("Open http://localhost:5000 to view results")
    print("Promote the model to Production in the Registry tab")