
def generate_recommendations(predicted_grade, G1, G2, studytime):
    recommendations = []

    # Recommendation based on predicted performance
    if predicted_grade < 10:
        recommendations.append(
            "Revise fundamental concepts and seek teacher support."
        )
    elif predicted_grade < 14:
        recommendations.append(
            "Practise more problems and revise difficult concepts."
        )
    else:
        recommendations.append(
            "Maintain your study routine and practise advanced problems."
        )

    # Recommendation based on previous grades
    if G2 < G1:
        recommendations.append(
            "Your recent grade decreased. Review topics you found difficult."
        )
    elif G2 > G1:
        recommendations.append(
            "Your grade improved. Continue the study methods that are helping."
        )

    # Recommendation based on study time
    if studytime <= 2:
        recommendations.append(
            "Consider setting aside more regular time for studying."
        )

    return recommendations


if __name__ == "__main__":
    results = generate_recommendations(
        predicted_grade=14.33,
        G1=12,
        G2=14,
        studytime=3
    )

    print("Personalized Learning Recommendations:")
    for recommendation in results:
        print("-", recommendation)
