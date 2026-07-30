from src.hitl.approval import ApprovalManager
from src.hitl.feedback import FeedbackManager
from src.hitl.audit import AuditManager
from src.hitl.decision_engine import DecisionEngine
from src.hitl.storage import HITLStorage


class HITLWorkflow:
    """
    Complete Human-in-the-Loop workflow.
    """

    def __init__(self):
        self.approval = ApprovalManager()
        self.feedback = FeedbackManager()
        self.audit = AuditManager()
        self.engine = DecisionEngine()
        self.storage = HITLStorage()

    def execute(
        self,
        employee_id: int,
        employee_name: str,
        department: str,
        predicted_score: float,
        prediction_category: str,
        reviewer: str,
        decision: str,
        comments: str,
    ):

        approval = self.approval.submit(
            employee_id=employee_id,
            prediction=prediction_category,
            reviewer=reviewer,
            decision=decision,
            comments=comments,
        )

        feedback = self.feedback.submit(
            employee_id=employee_id,
            reviewer=reviewer,
            comments=comments,
        )

        audit = self.audit.log(
            employee_id=employee_id,
            reviewer=reviewer,
            decision=decision,
        )

        final_decision = self.engine.finalize(
            approval,
            feedback,
            audit,
        )

        self.storage.save(
            employee_id=employee_id,
            employee_name=employee_name,
            department=department,
            predicted_score=predicted_score,
            prediction_category=prediction_category,
            reviewer=reviewer,
            decision=decision,
            comments=comments,
        )

        return final_decision