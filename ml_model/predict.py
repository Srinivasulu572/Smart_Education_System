
import joblib
import pandas as pd
from pathlib import Path

# Locate the trained model
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "ml_model" / "student_model.pkl"

# Load the trained model
model = joblib.load(MODEL_PATH)


def predict_grade(studytime, failures, absences, G1, G2):
    student = pd.DataFrame([{
        "studytime": studytime,
        "failures": failures,
        "absences": absences,
        "G1": G1,
        "G2": G2
    }])

    prediction = model.predict(student)[0]

    # Keep prediction within the dataset's grade range
    prediction = max(0, min(20, prediction))

    return round(float(prediction), 2)


if __name__ == "__main__":
    grade = predict_grade(
        studytime=3,
        failures=0,
        absences=2,
        G1=12,
        G2=14
    )

    print("Predicted final grade:", grade, "/ 20")
