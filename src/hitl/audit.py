from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass
class AuditRecord:
    employee_id: int
    reviewer: str
    decision: str
    timestamp: datetime


class AuditManager:
    """
    Records audit trail for every business decision.
    """

    def log(
        self,
        employee_id: int,
        reviewer: str,
        decision: str
    ) -> AuditRecord:

        return AuditRecord(
            employee_id=employee_id,
            reviewer=reviewer,
            decision=decision,
            timestamp=datetime.now(timezone.utc)
        )