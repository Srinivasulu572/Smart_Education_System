
from django.db import models


class PredictionHistory(models.Model):
    studytime = models.IntegerField()
    failures = models.IntegerField()
    absences = models.IntegerField()
    G1 = models.FloatField()
    G2 = models.FloatField()
    predicted_grade = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prediction: {self.predicted_grade}/20"
