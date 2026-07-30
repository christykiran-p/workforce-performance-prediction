"""
AI Report Generator

Coordinates all AI components to generate
a complete employee performance report.
"""

from __future__ import annotations

from src.ai.context.builder import ContextBuilder
from src.ai.explainability.explainer import PredictionExplainer
from src.ai.recommendation.recommender import RecommendationEngine
from src.ai.prompts.prompt_builder import PromptBuilder
from src.ai.llm.factory import LLMFactory
from src.ai.rag.rag_service import RAGService


class AIReportGenerator:
    """
    Generates AI-powered employee reports.
    """

    def __init__(self, employee_df):

        self.context_builder = ContextBuilder(
            employee_df=employee_df,
            performance_df=employee_df,
        )

        self.explainer = PredictionExplainer()

        self.recommender = RecommendationEngine()

        self.prompt_builder = PromptBuilder()

        self.rag = RAGService()

        self.llm = LLMFactory.create()

    def generate(
        self,
        employee_id: int,
        predicted_score: float,
        category: str,
    ) -> dict:

        context = self.context_builder.build(employee_id)

        explanation = self.explainer.explain(
            context=context,
            predicted_score=predicted_score,
            category=category,
        )

        recommendations = self.recommender.recommend(
            context=context,
            predicted_score=predicted_score,
            category=category,
        )

        rag_query = (
            f"{category} "
            f"{context.get('job_title', '')} "
            f"{context.get('department', '')}"
        )

        knowledge = self.rag.retrieve_context(rag_query)

        prompt = self.prompt_builder.build(
            context=context,
            prediction=predicted_score,
            category=category,
            explanation=explanation,
            recommendations=recommendations,
            knowledge=knowledge,
        )

        print(f"Prompt length: {len(prompt)} characters")
        print(prompt[:1000])

        summary = self.llm.generate(prompt)

        return {
            "context": context,
            "explanation": explanation,
            "recommendations": recommendations,
            "summary": summary,
        }