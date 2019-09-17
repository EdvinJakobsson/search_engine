from whoosh.qparser import QueryParser, OrGroup, MultifieldParser
from whoosh import scoring
from whoosh.index import open_dir
from bert import bert


def search(index_dir, query_str, num_results):
    """

    Args:
        index_dir:
        query_str:
        num_results:

    Returns:

    """
    results = []
    ix = open_dir(index_dir)
    with ix.searcher(weighting=scoring.BM25F) as searcher:
        query = QueryParser("title", ix.schema).parse(query_str)
        result_object = searcher.search(query, limit=num_results)
        if not result_object:
            query = QueryParser("title", ix.schema, group=OrGroup).parse(query_str)
            result_object = searcher.search(query, limit=num_results)
        print("Query:", query)
        if not result_object:
            print("No texts were found.\n")

        for i in range(num_results):
            try:
                dictionary = {}
                dictionary["title"] = result_object[i]['title']
                dictionary["score"] = str(result_object[i].score)
                dictionary["content"] = result_object[i]['content']
                dictionary["keywords"] = result_object[i]["keywords"]
                results.append(dictionary)
            except IndexError:
                continue
    return results


def list_files(index_dir):
    ix = open_dir(index_dir)
    docs = ix.searcher().documents()
    for doc in docs:
        print(doc["title"])
    print("In total: ", ix.searcher().doc_count(), "entries.")


def read_file(file):
    try:
        print("\n" + file["title"])
        print("\n" + file["content"])
        print("Keywords: ", file["keywords"])
    except:
        print("No file found.")


def ask_questions(model, paragraph):
    while True:
        query = input("What is your question?\n")
        if query == "go back":
            break
        if query == "exit":
            exit()
        answer = bert.bert_answer(model, query, paragraph)
        print("Bert\'s answer: ", answer)


def ask_bert(model, results):
    for result in results:
        print("\nLooking through file: ", result["title"], " length: ", len(result["content"].split()),
              "words.")
        print("\n", result["content"], "\n")
        print("Keywords:", result["keywords"], "\n")
        ask_questions(model, result["content"])


def main():
    model = bert.load_bert()

    num_results = 1
    index_dir = "search_engine/index_dir"
    last_result = None

    while True:
        query_str = input("\n-------------------------------\n"
                          "Please state your search query:\n")
        if query_str == "exit":
            exit()
        if query_str == "files":
            list_files(index_dir)
            continue
        if query_str == "read last":
            read_file(last_result)
            continue

        results = search(index_dir, query_str, num_results)
        if results:
            ask_bert(model, results)
            last_result = results[0]


if __name__ == "__main__":
    main()
