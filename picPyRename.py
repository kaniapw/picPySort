import sys
import os
import exifread
import datetime

#const
PICTURES_SOURCE = "d:\\art\\"
PRINT_DEBUG = True


def main(argv):
    for root, subDirs, files in os.walk(PICTURES_SOURCE):
        for fileName in files:
            fileExtension = fileName[-4:].lower()

            if fileExtension in {".jpg", ".mp4", ".avi", ".3gp"}:

                if PRINT_DEBUG:
                    print(root + "\\" + fileName)

                fileHandle = open(root + "\\" + fileName, 'rb')

                picEXIF = exifread.process_file(fileHandle, details=False)

                if 'Image DateTime' in picEXIF:
                    newFileName = str(picEXIF['Image DateTime'])
                elif 'EXIF DateTimeOriginal' in picEXIF:
                    newFileName = str(picEXIF['EXIF DateTimeOriginal'])
                elif 'EXIF DateTimeDigitized' in picEXIF:
                    newFileName = str(picEXIF['EXIF DateTimeDigitized'])
                else:
                    newFileName = datetime.datetime.fromtimestamp(os.path.getmtime(root + "\\" + fileName)).strftime("%Y %m %d %H %M %S")

                fileHandle.close()

                newFileName = newFileName.replace('/', '')
                newFileName = newFileName.replace(':', '')
                newFileName = newFileName.replace(' ', '')

                if PRINT_DEBUG:
                    print("File: " + root + "\\" + newFileName + fileExtension)
                    print("New file name: " + root + "\\" + newFileName + fileExtension)

                try:
                    os.rename(root + "\\" + fileName, root + "\\" + newFileName + fileExtension)
                except FileExistsError:
                    print("File :" + root + "\\" + newFileName + fileExtension + " already exists!" )

    pass

if __name__ == "__main__":
    main(sys.argv)