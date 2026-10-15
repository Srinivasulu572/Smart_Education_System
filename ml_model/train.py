import pandas as pd 
import joblib
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error,mean_squared_error,r2_score
 
# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "dataset" / "processed" / "cleaned_student_data.csv"
MODEL_PATH = BASE_DIR / "ml_model" / "student_model.pkl"

# Load cleaned dataset
data = pd.read_csv(DATA_PATH)

print("Cleaned dataset loaded:", data.shape)

# Input features
features = ["studytime", "failures", "absences", "G1", "G2"]

X = data[features]
y = data["G3"]

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Create and train the model
model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

# Evaluate predictions
predictions = model.predict(X_test)

mae = mean_absolute_error(y_test, predictions)
rmse = mean_squared_error(y_test, predictions) ** 0.5
r2 = r2_score(y_test, predictions)

print("\nModel Evaluation")
print("----------------")
print(f"Mean Absolute Error (MAE): {mae:.2f}")
print(f"Root Mean Squared Error (RMSE): {rmse:.2f}")
print(f"R² Score: {r2:.2f}")

# Save trained model
joblib.dump(model, MODEL_PATH)

print("\nModel trained and saved successfully!")
print("Model location:", MODEL_PATH)
