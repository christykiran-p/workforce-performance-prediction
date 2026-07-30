"""
Employee Context Builder

Builds employee profile information required by the AI layer.
"""

from __future__ import annotations

import pandas as pd


class EmployeeContext:
    """Build employee profile context."""

    def __init__(self, employee_df: pd.DataFrame):
        self.employee_df = employee_df

    def build(self, employee_id: int) -> dict:
        employee = self.employee_df.loc[
            self.employee_df["employee_id"] == employee_id
        ]

        if employee.empty:
            raise ValueError(f"Employee ID {employee_id} not found.")

        employee = employee.iloc[0]

        # Temporary: print available columns
        print("\nEmployee Columns:")
        print(employee.index.tolist())

        return {
            "employee_id": int(employee["employee_id"]),
        }