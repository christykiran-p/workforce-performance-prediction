"""
Prompt Builder
"""

from __future__ import annotations

from src.ai.prompts.summary_prompt import SUMMARY_INSTRUCTIONS
from src.ai.prompts.templates import EMPLOYEE_TEMPLATE


class PromptBuilder:

    def build(
        self,
        context,
        prediction,
        category,
        explanation,
        recommendations,
        knowledge,
    ) -> str:

        prompt = EMPLOYEE_TEMPLATE.format(
            context=context,
            prediction=prediction,
            category=category,
            explanation=explanation,
            recommendations="\n".join(recommendations),
            knowledge=knowledge,
        )

        return f"{SUMMARY_INSTRUCTIONS}\n\n{prompt}"