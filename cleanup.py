import re
import shutil
import os

DIRECTORY_STRING = "{}/api/static/images/".format(os.getcwd())
OUT_DIRECTORY_STRING = "{}/api/static/cleaned-images/".format(os.getcwd())

directory = os.fsencode(DIRECTORY_STRING)


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if filename.endswith(".png"):
        id = re.split(r'-|\.', filename)[0]

        src_path = os.path.join(DIRECTORY_STRING, filename)
        dest_path = "{}{}.png".format(OUT_DIRECTORY_STRING, id)

        try:
            file = open(dest_path)
            # if pass file exists
        except:
            if is_number(id):
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                shutil.copy(src_path, dest_path)
