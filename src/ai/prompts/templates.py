"""
Reusable prompt templates.
"""

EMPLOYEE_TEMPLATE = """
Relevant HR Knowledge

{knowledge}

--------------------------------------------------

Employee Context

{context}

--------------------------------------------------

Predicted Performance Score:
{prediction:.2f}

Performance Category:
{category}

--------------------------------------------------

Explanation:
{explanation}

--------------------------------------------------

Recommendations:
{recommendations}
"""