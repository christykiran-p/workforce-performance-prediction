"""
Prediction Explainability
"""

from __future__ import annotations

import pandas as pd


class PredictionExplainer:

    def explain(
        self,
        context: dict,
        predicted_score: float,
        category: str,
    ) -> dict:

        performance = context["performance"]

        summary = []

        if pd.isna(predicted_score):
            summary.append(
                "Prediction could not be generated because sufficient information was unavailable."
            )

            return {
                "predicted_score": None,
                "category": "Prediction Unavailable",
                "summary": summary,
            }

        attendance = performance["attendance_rate"]

        if attendance >= 95:
            summary.append(
                "Excellent attendance."
            )
        elif attendance >= 85:
            summary.append(
                "Good attendance consistency."
            )
        else:
            summary.append(
                "Attendance needs improvement."
            )

        working_hours = performance["average_working_hours"]

        if working_hours >= 8:
            summary.append(
                "Working hours are within the expected range."
            )
        else:
            summary.append(
                "Average working hours are below the expected range."
            )

        return {
            "predicted_score": round(float(predicted_score), 2),
            "category": category,
            "summary": summary,
        }