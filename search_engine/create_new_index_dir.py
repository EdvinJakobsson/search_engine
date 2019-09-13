import os
import json
from whoosh.index import create_in
from whoosh.fields import Schema, TEXT, ID
import shutil


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
        # path=ID(),
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
                    for item in range(len(data)):
                        print(data[item]["content"])
                        if data[item]["steps"]:
                            for step in data[item]["steps"]:
                                print(step["order"], ": ", step["cmd"])
                        print("\n")
                        writer.add_document(
                            title=data[item]["book_title"],
                            content=data[item]["content"],
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


def json_to_txt(root):
    """

    :param root:
    :return:
    """
    json_dir = os.path.join(root, "json_dir")
    txt_dir = os.path.join(root, "txt_dir")
    if os.path.exists(txt_dir):
        shutil.rmtree(txt_dir)
    os.mkdir(txt_dir)

    for root, dirs, files in os.walk(json_dir):
        for file in files:
            if ".json" in file:
                jsonfile_to_txt(root, file, txt_dir)


def jsonfile_to_txt(root, file, txt_dir):
    """

    :param root:
    :param file:
    :param txt_dir:
    :return:
    """
    with open(os.path.join(root, file)) as json_file:
        json_data = json.load(json_file)
        txt_file = open(
            os.path.join(
                txt_dir, json_data[0]["book_title"].replace(" ", "_") + ".txt"
            ),
            "w",
        )
        for dict in json_data:
            txt_file.write(dict["content"] + "\n")
            if dict["steps"]:
                for step in dict["steps"]:
                    txt_file.write(str(step["order"]) + ": " + str(step["cmd"]) + "\n")
            txt_file.write("\n")
        txt_file.close()


if __name__ == "__main__":
    create_searchable_database("")
    # json_to_txt("")
