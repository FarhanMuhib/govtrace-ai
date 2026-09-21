from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate

from app.llm import get_llm


class GroundednessResult(BaseModel):

    score: float = Field(
        ge=0.0,
        le=1.0,
        description=(
            "How strongly the answer is supported "
            "by the provided evidence."
        ),
    )

    reason: str = Field(
        description=(
            "Short explanation for the score."
        )
    )


def evaluate_groundedness(
    question: str,
    context: str,
    answer: str,
    callbacks=None,
):

    prompt = ChatPromptTemplate.from_template(
        """
You are a strict AI governance evaluator.

Your task is to measure GROUNDEDNESS.

Groundedness means:

"Are the factual claims in the AI answer
supported by the provided evidence?"

You must NOT use outside knowledge.

Evaluate only against the supplied evidence.


SCORING:

1.00
The answer is fully supported by the evidence.

0.80 - 0.99
The answer is strongly supported with only
minor unsupported details.

0.50 - 0.79
The answer is partially supported.

0.20 - 0.49
Most claims are unsupported.

0.00 - 0.19
The answer is unsupported or contradicts
the evidence.


QUESTION:

{question}


EVIDENCE:

{context}


AI ANSWER:

{answer}


Return:

- score from 0.0 to 1.0
- short reason
"""
    )

    structured_llm = (
        get_llm().with_structured_output(
            GroundednessResult
        )
    )

    chain = (
        prompt
        | structured_llm
    )

    result = chain.invoke(
        {
            "question": question,
            "context": context,
            "answer": answer,
        },
        config={
            "callbacks": callbacks or [],
            "run_name":
                "groundedness-evaluator",
        },
    )

    return result