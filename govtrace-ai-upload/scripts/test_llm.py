from app.llm import get_llm


def main():
    llm = get_llm()

    response = llm.invoke(
        "Reply with exactly this sentence: "
        "GovTrace Gemini connection successful."
    )

    print(response.content)


if __name__ == "__main__":
    main()