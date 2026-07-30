from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class ApprovalDecision:
    employee_id: int
    prediction: str
    reviewer: str
    decision: str
    comments: str = ""
    approved_at: Optional[datetime] = None


class ApprovalManager:
    """
    Handles business approval decisions.
    """

    VALID_DECISIONS = {"Approved", "Rejected"}

    def submit(
        self,
        employee_id: int,
        prediction: str,
        reviewer: str,
        decision: str,
        comments: str = ""
    ) -> ApprovalDecision:

        if decision not in self.VALID_DECISIONS:
            raise ValueError(
                f"Decision must be one of {self.VALID_DECISIONS}"
            )

        return ApprovalDecision(
            employee_id=employee_id,
            prediction=prediction,
            reviewer=reviewer,
            decision=decision,
            comments=comments,
            approved_at=datetime.utcnow(),
        )