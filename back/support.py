from os import walk

def import_folder(path):
    for _, __, img_file in walk(path):
         print(path + img_file)