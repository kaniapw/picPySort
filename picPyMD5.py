import sys
import os
import hashlib
from collections import defaultdict
from shutil import copyfile


#const
PICTURES_SOURCE_ONE = "c:\\art"
PICTURES_SOURCE_TWO = "c:\\art2"
PRINT_DEBUG = False
COPY_UNIQUE = True

def getMD5ForFiles(directory):
    result = defaultdict()

    for root, subDirs, files in os.walk(directory):
        for fileName in files:
            fileExtension = fileName[-4:].lower()

            if fileExtension in {".jpg", ".mp4", ".avi", ".3gp"}:
                file = root + "\\" + fileName
                md5 = hashlib.md5(open(file, 'rb').read()).hexdigest()

                if PRINT_DEBUG:
                    print(file + ": " +  md5)

                if md5 in result:
                    print("File: " + file + " is a duplicate for: " + result[md5])
                else:
                    result[md5] = file

    print(str(result.__len__()) + " pictures found in: " + PICTURES_SOURCE_ONE + "\n")

    return result

def main(argv):

    dir_one = getMD5ForFiles(PICTURES_SOURCE_ONE)
    dir_two = getMD5ForFiles(PICTURES_SOURCE_TWO)

    print("Unique files:")
    for md5 in dir_one:
        if md5 not in dir_two:
            print(dir_one[md5])

            if COPY_UNIQUE:
                if not os.path.exists(os.path.dirname(PICTURES_SOURCE_ONE + "Unique\\")):
                    os.makedirs(os.path.dirname(PICTURES_SOURCE_ONE + "Unique\\"))
                copyfile(dir_one[md5], PICTURES_SOURCE_ONE + "Unique\\" + str(dir_one[md5]).rsplit('\\', 1)[1])

    print("\n" + str(dir_two.__len__()) + " pictures found in: " + PICTURES_SOURCE_TWO)
    print("Unique files:")
    for md5 in dir_two:
        if md5 not in dir_one:
            print(dir_two[md5])

            if COPY_UNIQUE:
                if not os.path.exists(os.path.dirname(PICTURES_SOURCE_TWO + "Unique\\")):
                    os.makedirs(os.path.dirname(PICTURES_SOURCE_TWO + "Unique\\"))
                copyfile(dir_two[md5], PICTURES_SOURCE_TWO + "Unique\\" + str(dir_two[md5]).rsplit('\\', 1)[1])
    pass

if __name__ == "__main__":
    main(sys.argv)