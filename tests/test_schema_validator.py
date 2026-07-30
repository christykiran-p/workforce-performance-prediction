from src.validation.schema_validator import validate_required_tables


def test_validate_required_tables():
    result = validate_required_tables()

    assert result["is_valid"] is True
    assert result["missing_tables"] == []
    assert "employee" in result["existing_tables"]
    assert "employee_performance" in result["existing_tables"]