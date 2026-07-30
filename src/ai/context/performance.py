"""
Performance Context Builder

Builds employee performance context from the processed analytics dataset.
"""

from __future__ import annotations

import pandas as pd


class PerformanceContext:
    """Build employee performance context."""

    def __init__(self, performance_df: pd.DataFrame):
        self.performance_df = performance_df

    def build(self, employee_id: int) -> dict:
        employee = self.performance_df.loc[
            self.performance_df["employee_id"] == employee_id
        ]

        if employee.empty:
            raise ValueError(
                f"Employee ID {employee_id} not found."
            )

        employee = employee.iloc[0]

        return {
            "average_performance_score": float(
                employee["avg_performance_score"]
            ),
            "average_bonus_percentage": float(
                employee["avg_bonus_percentage"]
            ),
            "attendance_rate": float(
                employee["attendance_rate"]
            ),
            "average_working_hours": float(
                employee["avg_working_hours"]
            ),
            "team_size": int(
                employee["team_size"]
            ),
        }