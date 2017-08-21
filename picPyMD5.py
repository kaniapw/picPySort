import sys
import os
import hashlib
from collections import defaultdict
from shutil import copyfile

import picPyConst

#const
PICTURES_SOURCE_ONE = "w:\\"
PICTURES_SOURCE_TWO = "d:\\zdjecia"

UNIQUE_FOLDER_NAME = "\\Unique\\"

PRINT_DEBUG = False
COPY_UNIQUE = True

def getMD5ForFiles(directory):
    result = defaultdict()

    print("Processing folder: " + directory)

    for root, subDirs, files in os.walk(directory):
        for fileName in files:
            fileExtension = fileName[-4:].lower()

            searchFor = picPyConst.PICTURES
            #searchFor += picPyConst.VIDEOS

            if fileExtension in searchFor:
                file = root + "\\" + fileName
                fileHandle = open(file, 'rb')

                try:
                    md5 = hashlib.md5(fileHandle.read()).hexdigest()
                except MemoryError:
                    md5 = ""
                    print("File :" + file + " is probably to big, skipping it.")
                    #Todo: read file in chunks

                fileHandle.close()

                if md5 != "":
                    if PRINT_DEBUG:
                        print(file + ": " +  md5)

                    if md5 in result:
                        print("File: " + file + " is a duplicate for: " + result[md5])
                    else:
                        result[md5] = file

    print(str(result.__len__()) + " pictures found in: " + directory + "\n")

    return result

def main(argv):

    dir_one = getMD5ForFiles(PICTURES_SOURCE_ONE)
    dir_two = getMD5ForFiles(PICTURES_SOURCE_TWO)

    print("Unique files:")
    for md5 in dir_one:
        if md5 not in dir_two:
            print(dir_one[md5])

            if COPY_UNIQUE:
                if not os.path.exists(os.path.dirname(PICTURES_SOURCE_ONE + UNIQUE_FOLDER_NAME)):
                    os.makedirs(os.path.dirname(PICTURES_SOURCE_ONE + UNIQUE_FOLDER_NAME))
                copyfile(dir_one[md5], PICTURES_SOURCE_ONE + UNIQUE_FOLDER_NAME + str(dir_one[md5]).rsplit('\\', 1)[1])

    print("\n" + str(dir_two.__len__()) + " pictures found in: " + PICTURES_SOURCE_TWO)
    print("Unique files:")
    for md5 in dir_two:
        if md5 not in dir_one:
            print(dir_two[md5])

            if COPY_UNIQUE:
                if not os.path.exists(os.path.dirname(PICTURES_SOURCE_TWO + UNIQUE_FOLDER_NAME)):
                    os.makedirs(os.path.dirname(PICTURES_SOURCE_TWO + UNIQUE_FOLDER_NAME))
                copyfile(dir_two[md5], PICTURES_SOURCE_TWO + UNIQUE_FOLDER_NAME + str(dir_two[md5]).rsplit('\\', 1)[1])
    pass

if __name__ == "__main__":
    main(sys.argv)