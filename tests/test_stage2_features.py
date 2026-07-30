import pandas as pd

from src.features.attendance_features import create_attendance_features
from src.features.performance_features import create_performance_features
from src.features.leave_features import create_leave_features
from src.features.hierarchy_features import create_hierarchy_features


def test_create_performance_features():
    df = pd.DataFrame({
        "employee_id": [1, 1, 2],
        "overall_score": [4.0, 5.0, 3.0],
        "bonus_percentage": [10, 20, 5],
    })

    result = create_performance_features(df)

    assert "avg_performance_score" in result.columns
    assert result.loc[result["employee_id"] == 1, "avg_performance_score"].iloc[0] == 4.5


def test_create_attendance_features():
    df = pd.DataFrame({
        "employee_id": [1, 1, 2],
        "attendance_status": ["Present", "Absent", "Present"],
        "total_working_hours": [8, 0, 9],
        "overtime_hours": [1, 0, 2],
        "shortfall_hours": [0, 2, 0],
    })

    result = create_attendance_features(df)

    assert "attendance_rate" in result.columns
    assert result.loc[result["employee_id"] == 1, "attendance_rate"].iloc[0] == 50.0


def test_create_leave_features():
    df = pd.DataFrame({
        "employee_id": [1, 1, 2],
        "privileged_leave_used": [2, 3, 1],
        "sick_leave_used": [1, 1, 0],
        "lop_days": [0, 1, 0],
        "total_leave_balance": [10, 8, 12],
    })

    result = create_leave_features(df)

    assert "total_leave_used" in result.columns
    assert result.loc[result["employee_id"] == 1, "total_leave_used"].iloc[0] == 8


def test_create_hierarchy_features():
    df = pd.DataFrame({
        "employee_id": [2, 3, 4],
        "reporting_manager_id": [1, 1, 2],
    })

    result = create_hierarchy_features(df)

    assert "team_size" in result.columns
    assert result.loc[result["employee_id"] == 1, "team_size"].iloc[0] == 2