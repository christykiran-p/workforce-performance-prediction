"""
AI Context Builder

Aggregates all context providers into a single AI context.
"""

from __future__ import annotations

import pandas as pd

from src.ai.context.employee import EmployeeContext
from src.ai.context.performance import PerformanceContext


class ContextBuilder:
    """Build complete AI context."""

    def __init__(
        self,
        employee_df: pd.DataFrame,
        performance_df: pd.DataFrame,
    ):
        self.employee_context = EmployeeContext(employee_df)
        self.performance_context = PerformanceContext(performance_df)

    def build(self, employee_id: int) -> dict:
        """Build AI context for one employee."""

        return {
            "employee": self.employee_context.build(employee_id),
            "performance": self.performance_context.build(employee_id),
        }