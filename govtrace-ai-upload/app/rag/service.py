from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from langfuse import (
    get_client,
    propagate_attributes,
)

from langfuse.langchain import CallbackHandler

from app.config import ROOT_DIR

from app.rag.embeddings import (
    get_embeddings,
)

from app.llm import (
    get_llm,
)

from app.evaluation.groundedness import (
    evaluate_groundedness,
)


CHROMA_PATH = (
    ROOT_DIR
    / "data"
    / "chroma"
)


GROUNDEDNESS_THRESHOLD = 0.80


def get_vector_store():

    return Chroma(
        persist_directory=str(
            CHROMA_PATH
        ),
        embedding_function=get_embeddings(),
    )


def format_context(documents):

    context_parts = []

    for index, doc in enumerate(
        documents,
        start=1,
    ):

        source = doc.metadata.get(
            "source",
            "unknown",
        )

        context_parts.append(
            f"""
EVIDENCE CHUNK {index}

SOURCE:
{source}

CONTENT:
{doc.page_content}
"""
        )

    return "\n".join(
        context_parts
    )


def get_unique_sources(documents):

    return sorted(
        {
            doc.metadata.get(
                "source",
                "unknown",
            )
            for doc in documents
        }
    )


def ask_govtrace(
    question: str,
    run_evaluation: bool = True,
):

    # -----------------------------
    # Langfuse
    # -----------------------------

    langfuse = get_client()

    langfuse_handler = (
        CallbackHandler()
    )


    # -----------------------------
    # Root trace
    # -----------------------------

    with langfuse.start_as_current_observation(
        as_type="span",
        name="govtrace-rag-query",
        input={
            "question": question,
        },
    ) as root_span:

        with propagate_attributes(
            user_id="local-developer",
            session_id="govtrace-m1",
            tags=[
                "govtrace",
                "m1",
                "rag",
                "nist-ai-rmf",
            ],
            metadata={
                "system":
                    "GovTrace AI",
                "milestone":
                    "M1.5",
            },
        ):

            # -------------------------
            # Vector store
            # -------------------------

            vector_store = (
                get_vector_store()
            )

            retriever = (
                vector_store.as_retriever(
                    search_kwargs={
                        "k": 3,
                    }
                )
            )


            # -------------------------
            # Evidence retrieval
            # -------------------------

            documents = (
                retriever.invoke(
                    question,
                    config={
                        "callbacks": [
                            langfuse_handler
                        ],
                        "run_name":
                            "chroma-evidence-retrieval",
                    },
                )
            )


            context = format_context(
                documents
            )

            sources = (
                get_unique_sources(
                    documents
                )
            )


            # -------------------------
            # RAG Prompt
            # -------------------------

            prompt = (
                ChatPromptTemplate.from_template(
                    """
You are GovTrace AI.

Your role is to answer AI governance
questions using only the evidence
provided by the GovTrace knowledge base.

Rules:

1. Use only the supplied evidence.

2. Do not invent facts.

3. If the evidence does not contain
   enough information to answer the
   question, say exactly:

   "I do not have enough evidence."

4. Keep the answer factual and concise.

5. Do not claim legal compliance,
   certification, or regulatory approval.

6. When appropriate, identify the
   framework concepts mentioned in
   the evidence.


EVIDENCE:

{context}


USER QUESTION:

{question}


ANSWER:
"""
                )
            )


            # -------------------------
            # Answer chain
            # -------------------------

            chain = (
                prompt
                | get_llm()
                | StrOutputParser()
            )


            response = chain.invoke(
                {
                    "context": context,
                    "question": question,
                },
                config={
                    "callbacks": [
                        langfuse_handler
                    ],
                    "run_name":
                        "govtrace-answer-generation",
                },
            )


            # -------------------------
            # Automated evaluation
            # -------------------------

            evaluation = None

            if run_evaluation:

                evaluation_result = (
                    evaluate_groundedness(
                        question=question,
                        context=context,
                        answer=response,
                        callbacks=[
                            langfuse_handler
                        ],
                    )
                )

                groundedness_score = float(
                    evaluation_result.score
                )

                passed = (
                    groundedness_score
                    >=
                    GROUNDEDNESS_THRESHOLD
                )


                evaluation = {
                    "score":
                        groundedness_score,
                    "passed":
                        passed,
                    "threshold":
                        GROUNDEDNESS_THRESHOLD,
                    "reason":
                        evaluation_result.reason,
                }


                # ---------------------
                # Langfuse Numeric Score
                # ---------------------

                langfuse.score_current_trace(
                    name="groundedness",
                    value=groundedness_score,
                    data_type="NUMERIC",
                    comment=(
                        evaluation_result.reason[
                            :500
                        ]
                    ),
                    metadata={
                        "evaluator":
                            "Gemini",
                        "threshold":
                            GROUNDEDNESS_THRESHOLD,
                    },
                )


                # ---------------------
                # Langfuse PASS Score
                # ---------------------

                langfuse.score_current_trace(
                    name="groundedness_pass",
                    value=(
                        1.0
                        if passed
                        else 0.0
                    ),
                    data_type="BOOLEAN",
                    comment=(
                        "PASS"
                        if passed
                        else "REVIEW"
                    ),
                )


            # -------------------------
            # Root trace output
            # -------------------------

            root_span.update(
                output={
                    "answer":
                        response,
                    "sources":
                        sources,
                    "retrieved_chunks":
                        len(documents),
                    "evaluation":
                        evaluation,
                },
                metadata={
                    "framework":
                        "NIST AI RMF",
                    "vector_store":
                        "Chroma",
                    "embedding_model":
                        (
                            "sentence-transformers/"
                            "all-MiniLM-L6-v2"
                        ),
                    "retrieved_chunks":
                        len(documents),
                    "evaluation_enabled":
                        run_evaluation,
                },
            )


            result = {

                "answer":
                    response,

                "sources":
                    sources,

                "context":
                    context,

                "retrieved_chunks":
                    len(documents),

                "evaluation":
                    evaluation,
            }


    # Important for CLI tests
    langfuse.flush()

    return result