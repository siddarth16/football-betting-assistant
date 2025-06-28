import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.preprocessing import StandardScaler

INPUT_FILE = "data/merged_dataset.csv"
OUTPUT_FILE = "data/predictions.csv"

def preprocess(df):
    df = df.copy()

    # Drop matches with missing scores
    df = df.dropna(subset=["goals_for", "goals_against"])

    # Encode result
    df["label"] = df["result"].map({"W": 1, "D": 0, "L": -1})

    # Select numeric features
    features = [
        "goals_for", "goals_against", "goal_diff",
        "wins", "losses", "draws",
        "avg_goals_for", "avg_goals_against",
        "avg_corners", "avg_cards", "clean_sheets", "failed_to_score"
    ]

    df = df.dropna(subset=features)
    X = df[features]
    y = df["label"]

    # Normalize features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    return X_scaled, y, df

def main():
    if not os.path.exists(INPUT_FILE):
        print("Missing merged dataset.")
        return

    df = pd.read_csv(INPUT_FILE)
    X, y, full_df = preprocess(df)

    # Train/test split
    X_train, X_test, y_train, y_test, df_train, df_test = train_test_split(
        X, y, full_df, test_size=0.2, random_state=42, stratify=y
    )

    # Model
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)

    # Predict
    y_pred = model.predict(X_test)
    df_test["predicted"] = y_pred
    df_test["actual"] = y_test

    # Save predictions
    df_test.to_csv(OUTPUT_FILE, index=False)
    print("✅ Predictions saved to", OUTPUT_FILE)
    print("\n🧾 Model Performance:\n")
    print(classification_report(y_test, y_pred))

if __name__ == "__main__":
    main()
