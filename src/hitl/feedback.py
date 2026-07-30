from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass
class Feedback:
    employee_id: int
    reviewer: str
    comments: str
    created_at: datetime


class FeedbackManager:
    """
    Handles reviewer feedback.
    """

    def submit(
        self,
        employee_id: int,
        reviewer: str,
        comments: str
    ) -> Feedback:

        if not comments.strip():
            raise ValueError("Feedback comments cannot be empty.")

        return Feedback(
            employee_id=employee_id,
            reviewer=reviewer,
            comments=comments,
            created_at=datetime.now(timezone.utc)
        )