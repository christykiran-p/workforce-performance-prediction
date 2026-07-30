from dataclasses import dataclass

from src.hitl.approval import ApprovalDecision
from src.hitl.feedback import Feedback
from src.hitl.audit import AuditRecord


@dataclass
class FinalDecision:
    employee_id: int
    prediction: str
    reviewer: str
    decision: str
    comments: str
    status: str


class DecisionEngine:
    """
    Generates the final business decision.
    """

    def finalize(
        self,
        approval: ApprovalDecision,
        feedback: Feedback,
        audit: AuditRecord
    ) -> FinalDecision:

        status = (
            "Completed"
            if approval.decision == "Approved"
            else "Rejected"
        )

        return FinalDecision(
            employee_id=approval.employee_id,
            prediction=approval.prediction,
            reviewer=approval.reviewer,
            decision=approval.decision,
            comments=feedback.comments,
            status=status
        )