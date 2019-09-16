import json
import os
import shutil


def rename_jsonfiles(json_dir):
    for root, directory, files in os.walk(json_dir):
        for file in files:
            if ".json" in file:
                count = 1
                with open(os.path.join(root, file)) as json_file:
                    json_data = json.load(json_file)
                    path = (os.path.join(root, file))
                    new_name = os.path.join(root, json_data[0]["book_title"].replace(" ", "_"))

                    while os.path.exists(new_name + "_" + str(count) + ".json"):
                        count += 1

                    new_name = new_name + "_" + str(count) + ".json"
                    os.rename(path, new_name)


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
                jsonfile_to_txts(root, file, txt_dir)


def jsonfile_to_txt(root, file, txt_dir):
    """

    :param root:
    :param file:
    :param txt_dir:
    :return:
    """
    with open(os.path.join(root, file)) as json_file:
        json_data = json.load(json_file)
        txt_filename = os.path.join(txt_dir, json_data[0]["book_title"].replace(" ", "_") + ".txt")
        txt_file = open(txt_filename, "w")

        for dict in json_data:
            txt_file.write(dict["content"] + "\n")
            if dict["steps"]:
                for step in dict["steps"]:
                    txt_file.write("step " + str(step["order"]) + ": " + str(step["cmd"]) + "\n")
            txt_file.write("\n")
        txt_file.close()


def jsonfile_to_txts(root, file, txt_dir):
    """

    :param root:
    :param file:
    :param txt_dir:
    :return:
    """
    with open(os.path.join(root, file)) as json_file:
        json_data = json.load(json_file)
        booktitle_dir = os.path.join(txt_dir, file.replace(".json", ""))
        if not os.path.exists(booktitle_dir):
            os.mkdir(booktitle_dir)

        count = 0
        for dict in json_data:
            filename = dict["title"].replace(" ", "_")
            filename = filename.replace("/", "-")
            txt_path = os.path.join(booktitle_dir, filename)
            if len(txt_path) > 250:
                txt_path = txt_path[:250]
            while os.path.exists(txt_path + "-" + str(count) + ".txt"):
                count += 1
            txt_path = txt_path + "-" + str(count) + ".txt"
            print(txt_path)
            txt_file = open(txt_path, "w")
            txt_file.write(dict["content"] + "\n")
            if dict["steps"]:
                for step in dict["steps"]:
                    txt_file.write("step " + str(step["order"]) + ": " + str(step["cmd"]) + "\n")
            txt_file.write("\n")
            txt_file.close()



if __name__ == "__main__":
    json_to_txt("")


