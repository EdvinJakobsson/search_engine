from whoosh.qparser import QueryParser, OrGroup, MultifieldParser
from whoosh import scoring
from whoosh.index import open_dir
from bert import bert


def search_for(index_dir, query_str, num_results):
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
                dict = {}
                dict["title"] = result_object[i]['title']
                dict["score"] = str(result_object[i].score)
                dict["content"] = result_object[i]['content']
                dict["keywords"] = result_object[i]["keywords"]
                results.append(dict)
            except IndexError:
                continue
    return results


def list_files(index_dir):
    ix = open_dir(index_dir)
    docs = ix.searcher().documents()
    for doc in docs:
        print(doc["title"])
    print("In total: ", ix.searcher().doc_count(), "entries.")


def print_content(file, index_dir):
    ix = open_dir(index_dir)
    docs = ix.searcher().documents()
    for doc in docs:
        if doc["title"] == file:
            print("\n", doc["content"])
            print("\nKeywords:", doc["keywords"])

def ask_questions(model, paragraph):
    while True:
        query = input("What is your question?\n")
        if query == "go back":
            break
        if query == "exit":
            exit()
        answer = bert.bert_answer(model, query, paragraph)
        print("Bert\'s answer: ", answer)

def main():
    model = bert.load_bert()

    num_results = 1
    index_dir = "search_engine/index_dir"
    last_result = None

    while True:
        query_str = input("\n-------------------------------\nPlease state your search query:\n")
        if query_str == "exit":
            exit()
        if query_str == "files":
            list_files(index_dir)
            continue
        if query_str == "read last":
            print("\n" + last_result["title"])
            print("\n" + last_result["content"])
            print("Keywords: ", last_result["keywords"])
            continue
        elif query_str.startswith("read "):
            print_content(query_str[5:], index_dir)
            continue

        results = search_for(index_dir, query_str, num_results)
        if results:
            for dictionary in results:
                print("\nLooking through file: ", dictionary["title"], " length: ", len(dictionary["content"].split()), "words.")
                print("\n", dictionary["content"], "\n")
                print("Keywords:", dictionary["keywords"], "\n")
                ask_questions(model, dictionary["content"])

            last_result = results[0]


if __name__ == "__main__":
    main()

