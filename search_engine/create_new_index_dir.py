import os
import json
import shutil
from whoosh.index import create_in
from whoosh.fields import Schema, TEXT, KEYWORD



def create_searchable_database(root, txt_files=True):
    """
    Loading all files in corpus to the
    :param root (string): Directory of corpus
    """

    index_dir = os.path.join(root, "index_dir")
    if txt_files:
        corpus_dir = os.path.join(root, "txt_dir")
    else:
        corpus_dir = os.path.join(root, "json_dir")
    while True:
        inpt = input(
            'Warning! This will remove the current index_dir. Type "ok" to continue,'
            ' or "exit" to abort: \n'
        )
        if inpt == "ok":
            break
        elif inpt == "exit":
            exit()
    if os.path.exists(index_dir):
        shutil.rmtree(index_dir)
    os.mkdir(index_dir)
    schema = Schema(
        title=TEXT(stored=True),
        keywords=KEYWORD(stored=True, scorable=True, commas=True),
        content=TEXT(stored=True))

    ix = create_in(index_dir, schema)
    writer = ix.writer()
    if txt_files:
        add_txt_documents(writer, corpus_dir)
    else:
        add_json_documents(writer, corpus_dir)
    writer.commit()


def add_json_documents(writer, corpus_dir):
    for root, dirs, files in os.walk(corpus_dir):
        for file in files:
            if ".json" in file:
                with open(os.path.join(root, file)) as json_file:
                    data = json.load(json_file)
                    for dict in data:
                        if dict["content"] == "" and not dict["steps"]:
                            continue
                        content = (dict["content"] + "\n")
                        if dict["steps"]:
                            for step in dict["steps"]:
                                content += "step " + (str(step["order"]) + ": " + str(step["cmd"]) + "\n")
                        content += "\n"
                        writer.add_document(
                            title=dict["book_title"] + " - " + dict["title"],
                            content=content,
                            keywords=dict["keywords"]
                        )


def add_txt_documents(writer, corpus_dir):

    for root, dirs, files in os.walk(corpus_dir):
        for file in files:
            if ".txt" in file:
                with open(os.path.join(root, file), "r") as txt_file:
                    title = file.replace("_", " ")
                    title = title.replace(".txt", "")

                    writer.add_document(
                        title=title,
                        content=txt_file.read()
                    )


if __name__ == "__main__":
    create_searchable_database("", txt_files=False)

