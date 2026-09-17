import pandas as pd
import joblib

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

print("Loading Dataset...")

df = pd.read_csv("../dataset/bank_dataset.csv")

# Convert text columns into numbers
location_encoder = LabelEncoder()
device_encoder = LabelEncoder()
time_encoder = LabelEncoder()

df["Location"] = location_encoder.fit_transform(df["Location"])
df["Device"] = device_encoder.fit_transform(df["Device"])
df["Time"] = time_encoder.fit_transform(df["Time"])

# Save encoders
joblib.dump(location_encoder, "location_encoder.pkl")
joblib.dump(device_encoder, "device_encoder.pkl")
joblib.dump(time_encoder, "time_encoder.pkl")

X = df.drop("Fraud", axis=1)
y = df["Fraud"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

print("Training Model...")

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

accuracy = model.score(X_test, y_test)

print("Accuracy =", accuracy)

joblib.dump(model, "bank_model.pkl")

print("Model Saved Successfully")