from whoosh.qparser import QueryParser, OrGroup
from whoosh import scoring
from whoosh.index import open_dir


def search_for(index_dir, query_str, num_results):
    """

    :param index_dir:
    :param query_str:
    :param num_results:
    :return:
    """
    results = []
    ix = open_dir(index_dir)
    with ix.searcher(weighting=scoring.BM25F) as searcher:
        query = QueryParser("content", ix.schema).parse(query_str)
        result_object = searcher.search(query, limit=num_results)
        if not result_object:
            query = QueryParser("content", ix.schema, group=OrGroup).parse(query_str)
            result_object = searcher.search(query, limit=num_results)
        if not result_object:
            print("No texts were found.\n")

        for i in range(num_results):
            try:
                dict = {}
                dict["title"] = result_object[i]['title']
                dict["score"] = str(result_object[i].score)
                dict["content"] = result_object[i]['content']
                results.append(dict)
            except IndexError:
                continue
    return results


def list_files(index_dir):
    ix = open_dir(index_dir)
    docs = ix.searcher().documents()
    for doc in docs:
        print(doc["title"])


def main():
    num_results = 5
    index_dir = "search_engine/index_dir"

    while True:
        query_str = input("\nPlease state your search query:\n")
        if query_str == "exit":
            exit()
        if query_str == "files":
            list_files(index_dir)
            continue
        results = search_for(index_dir, query_str, num_results)
        for dictionary in results:
            print("Looking through file: ", dictionary["title"], "\n")


if __name__ == "__main__":
    main()


