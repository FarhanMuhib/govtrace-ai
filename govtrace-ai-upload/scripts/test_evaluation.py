from app.rag.service import (
    ask_govtrace,
)


def main():

    question = (
        "What are ISO 42001 Annex A controls?"
    )

    result = ask_govtrace(
        question,
        run_evaluation=True,
    )


    print(
        "\nANSWER"
    )

    print(
        "----------------"
    )

    print(
        result["answer"]
    )


    print(
        "\nSOURCES"
    )

    print(
        "----------------"
    )

    for source in result["sources"]:

        print(source)


    print(
        "\nEVALUATION"
    )

    print(
        "----------------"
    )

    evaluation = (
        result["evaluation"]
    )


    print(
        "Groundedness:",
        evaluation["score"],
    )

    print(
        "Threshold:",
        evaluation["threshold"],
    )

    print(
        "Result:",
        (
            "PASS"
            if evaluation["passed"]
            else "REVIEW"
        ),
    )

    print(
        "Reason:",
        evaluation["reason"],
    )


if __name__ == "__main__":

    main()