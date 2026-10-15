
from django.shortcuts import render
from ml_model.predict import predict_grade
from ml_model.recommendations import generate_recommendations
from .models import PredictionHistory


def home(request):
    context = {
        "grade": None,
        "recommendations": [],
        "error": None,
    }

    if request.method == "POST":
        try:
            studytime = int(request.POST.get("studytime", ""))
            failures = int(request.POST.get("failures", ""))
            absences = int(request.POST.get("absences", ""))
            G1 = float(request.POST.get("G1", ""))
            G2 = float(request.POST.get("G2", ""))

            if not 1 <= studytime <= 4:
                raise ValueError("Study time must be between 1 and 4.")
            if failures < 0 or absences < 0:
                raise ValueError("Failures and absences cannot be negative.")
            if not 0 <= G1 <= 20 or not 0 <= G2 <= 20:
                raise ValueError("Grades must be between 0 and 20.")

            grade = predict_grade(studytime, failures, absences, G1, G2)
            recommendations = generate_recommendations(
                grade, G1, G2, studytime
            )
            PredictionHistory.objects.create(
    studytime=studytime,
    failures=failures,
    absences=absences,
    G1=G1,
    G2=G2,
    predicted_grade=grade,
)

            context["grade"] = grade
            context["recommendations"] = recommendations

        except (ValueError, KeyError) as e:
            context["error"] = str(e)
        except Exception as e:
            print("Prediction error:", repr(e))
            context["error"] = "Prediction failed. Check the PowerShell error."

        if request.method == "POST":
            return render(request, "performance.html", context)

    return render(request, "home.html", context)
def history(request):
    records = PredictionHistory.objects.order_by("-created_at")

    return render(
        request,
        "history.html",
        {"history": records}
    )

def dashboard(request):
    records = PredictionHistory.objects.order_by("-created_at")

    total_predictions = records.count()

    latest = records.first()

    if total_predictions > 0:
        average_grade = sum(
            item.predicted_grade for item in records
        ) / total_predictions
        average_grade = round(average_grade, 2)
    else:
        average_grade = 0

    previous = records[1] if total_predictions >= 2 else None

    progress = None
    if latest and previous:
        progress = round(
            latest.predicted_grade - previous.predicted_grade, 2
        )

    context = {
        "total_predictions": total_predictions,
        "average_grade": average_grade,
        "latest": latest,
        "progress": progress,
        "recent_records": records[:5],
    }

    return render(request, "dashboard.html", context)
