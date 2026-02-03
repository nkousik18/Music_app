import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from xgboost import XGBClassifier
from sklearn.metrics import classification_report
import joblib
import mlflow
import mlflow.sklearn
from sklearn.preprocessing import LabelEncoder


FEATURES = [
  "danceability","energy","loudness","speechiness",
  "acousticness","instrumentalness","liveness",
  "valence","tempo","duration_ms","track_popularity"
]

df = pd.read_csv("../data/songs.csv")

X = df[FEATURES]
le = LabelEncoder()
y = le.fit_transform(df["playlist_genre"])


X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("model", XGBClassifier(
        objective="multi:softprob",
        eval_metric="mlogloss",
        n_estimators=200,
        max_depth=6,
        learning_rate=0.1,
        n_jobs=1,
        tree_method="hist",
        random_state=42
    ))
])

mlflow.set_experiment("genre_classification")

with mlflow.start_run():
    pipeline.fit(X_train, y_train)

    preds = pipeline.predict(X_test)
    report = classification_report(y_test, preds, output_dict=True)

    mlflow.log_params({
        "model": "XGBoost",
        "features": len(FEATURES),
        "n_estimators": 200
    })

    mlflow.log_metrics({
        "accuracy": report["accuracy"]
    })

    mlflow.sklearn.log_model(pipeline, "genre_model")

    joblib.dump(le, "../artifacts/genre_label_encoder.pkl")

