import os
import json
from whoosh.index import create_in
from whoosh.fields import Schema, TEXT, ID
import shutil



def create_searchable_database(root):
    """
    Loading all files in corpus to the
    :param root (string): Directory of corpus
    """

    index_dir = os.path.join(root, "index_dir")
    corpus_dir = os.path.join(root, "json_data2")
    shutil.rmtree(index_dir)
    exit()
    if not os.path.exists(index_dir):
        os.mkdir(index_dir)
    schema = Schema(title=TEXT(stored=True))
                    # path=ID(),
                    # content=TEXT(stored=True))

    ix = create_in(index_dir, schema)
    writer = ix.writer()
    add_documents(writer, corpus_dir)
    writer.commit()


def add_documents(writer, corpus_dir):

    # filepaths = [os.path.join(corpus_dir, i) for i in os.listdir(corpus_dir)]
    for root, dirs, files in os.walk(corpus_dir):
        for file in files:
            if ".json" in file:
                with open(os.path.join(root, file)) as json_file:
                    data = json.load(json_file)
                    for item in range(len(data)):
                        print( data[item]["book_title"] )
                        writer.add_document(title=data[item]["book_title"])
                        break



        """
        fp = open(path, "r")
        text = fp.read()
        writer.add_document(title=path.split("/")[-1], path=path, content=text)
        fp.close()
        """

if __name__ == "__main__":
    create_searchable_database("")


