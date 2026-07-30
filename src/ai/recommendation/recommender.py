"""
AI Recommendation Engine

Generates actionable recommendations based on employee context
and predicted performance.
"""

from __future__ import annotations

import pandas as pd


class RecommendationEngine:
    """Generate business recommendations."""

    def recommend(
        self,
        context: dict,
        predicted_score: float,
        category: str,
    ) -> list[str]:

        recommendations = []

        if pd.isna(predicted_score):
            return [
                "Validate employee data before generating recommendations."
            ]

        performance = context["performance"]

        attendance = performance["attendance_rate"]
        working_hours = performance["average_working_hours"]

        # Performance-based recommendations
        if category == "High Performer":
            recommendations.extend([
                "Assign leadership responsibilities.",
                "Nominate for advanced learning programs.",
                "Consider succession planning.",
            ])

        elif category == "Consistent Performer":
            recommendations.extend([
                "Assign stretch projects.",
                "Encourage cross-functional collaboration.",
                "Continue skill development.",
            ])

        elif category == "Needs Improvement":
            recommendations.extend([
                "Schedule manager coaching sessions.",
                "Prepare an individual development plan.",
            ])

        elif category == "Critical Attention":
            recommendations.extend([
                "Conduct a performance review meeting.",
                "Identify blockers affecting productivity.",
            ])

        # Attendance
        if attendance < 90:
            recommendations.append(
                "Review attendance trends with the employee."
            )

        # Working hours
        if working_hours < 8:
            recommendations.append(
                "Review workload and productivity patterns."
            )

        return recommendations