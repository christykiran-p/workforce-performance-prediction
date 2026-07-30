from pathlib import Path
from datetime import datetime
import pandas as pd


class HITLStorage:
    """
    Handles persistence of Human-in-the-Loop review decisions.
    """

    def __init__(self):
        self.output_dir = Path("output")
        self.output_dir.mkdir(exist_ok=True)

        self.file_path = self.output_dir / "hitl_decisions.csv"

    def save(
        self,
        employee_id: int,
        employee_name: str,
        department: str,
        predicted_score: float,
        prediction_category: str,
        reviewer: str,
        decision: str,
        comments: str,
    ) -> None:

        review = pd.DataFrame(
            [
                {
                    "review_id": datetime.now().strftime("%Y%m%d%H%M%S%f"),
                    "employee_id": employee_id,
                    "employee_name": employee_name,
                    "department": department,
                    "predicted_score": predicted_score,
                    "prediction_category": prediction_category,
                    "reviewer": reviewer,
                    "decision": decision,
                    "comments": comments,
                    "review_time": datetime.now(),
                }
            ]
        )

        if self.file_path.exists():
            existing = pd.read_csv(self.file_path)
            review = pd.concat([existing, review], ignore_index=True)

        review.to_csv(self.file_path, index=False)