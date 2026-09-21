from app.rag.service import ask_govtrace


def main():

    result = ask_govtrace(
        "What are the four NIST AI RMF functions?"
    )


    print("\nANSWER")
    print("----------------")
    print(
        result["answer"]
    )


    print("\nSOURCES")
    print("----------------")

    for source in result["sources"]:
        print(source)



if __name__ == "__main__":
    main()