from dataclasses import dataclass


@dataclass
class Reviewer:
    reviewer_id: str
    reviewer_name: str
    designation: str
    department: str


class ReviewerManager:
    """
    Handles reviewer validation and lookup.
    """

    def validate(self, reviewer: Reviewer) -> bool:

        if not reviewer.reviewer_id.strip():
            raise ValueError("Reviewer ID cannot be empty.")

        if not reviewer.reviewer_name.strip():
            raise ValueError("Reviewer name cannot be empty.")

        return True