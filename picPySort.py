import sys
import os
import exifread
import requests
import json
import datetime
import calendar
from geopy.distance import vincenty
from collections import defaultdict
from shutil import copyfile

#const
PICTURES_SOURCE = "d:\\art\\"
PICTURES_DESTINATION = "d:\\Destination\\"
HOME = (53.514546, 14.613439)
HOME_AREA = 35
OTHER_AREA = 15
REMOVE_FROM_ADDRESS = [", Poland", "Gmina", "/", "\\", "-"]
REMOVE_FROM_MODEL = ["/", "<", ">"]

GEOCODE_URL = 'http://maps.googleapis.com/maps/api/geocode/json?latlng='
HTTP_OK = 200
PRINT_DEBUG = False

#variable
POSITIONS = {}

class Picture(object):
    def __init__(self):
        self.fileName = ""
        self.fileNameWithPath = ""
        self.make = ""
        self.model = ""
        self.address = ""

def fromGPSToAddress(latitude, longitude):
    result = ""

    newPosition = (latitude, longitude)

    for knownPosition in POSITIONS:
        if vincenty(newPosition, knownPosition).kilometers < OTHER_AREA:
            result = POSITIONS[knownPosition]

    if result == "":
        response = requests.get(GEOCODE_URL + latitude + "," + longitude + "&sensor=true")

        if HTTP_OK == response.status_code:
            data = json.loads(response.text)
            if len(data["results"]) > 0:
                try:
                    result = data["results"][1]["formatted_address"]
                except IndexError:
                    print("No data for: " + response.text)
                    POSITIONS[(latitude, longitude)] = result

                for remove in REMOVE_FROM_ADDRESS:
                    result = result.replace(remove, '')

                #some times there is a postal code therefore attempt to remove it
                result = ''.join(i for i in result if not i.isdigit())
                result = result.lstrip(' ')

                if result != "":
                    filePath = PICTURES_DESTINATION + "pos\\" + result
                    if not os.path.exists(os.path.dirname(filePath)):
                        os.makedirs(os.path.dirname(filePath))

                    file = open(filePath, 'w', encoding='utf8')
                    file.write(latitude + "\n")
                    file.write(longitude + "\n")
                    file.write(response.text)
                    file.close()

                    POSITIONS[(latitude, longitude)] = result

                print(result)
        else:
            print(response.status_code)

    return result

def fromGPSDataToKey(gpsData):
    result = (str(gpsData)[0:4], str(str(gpsData)[5] + str(gpsData)[6]))
    return result

def convertToDegress(coordinate, direction):
    d = float(coordinate.values[0].num) / float(coordinate.values[0].den)
    m = float(coordinate.values[1].num) / float(coordinate.values[1].den)
    s = float(coordinate.values[2].num) / float(coordinate.values[2].den)

    result = d + (m / 60.0) + (s / 3600.0)

    if direction == 'S' or direction == 'W':
        result = 0 - result

    return str(result)

def loadPositions():
    posFile = PICTURES_DESTINATION + "pos\\"
    if os.path.exists(os.path.dirname(posFile)):
        for file in os.listdir(posFile):
            with open(posFile + file, encoding='utf8') as fileHandle:
                lines = fileHandle.readlines()
            latitude = lines[0]
            longitude = lines[1]
            POSITIONS[(latitude, longitude)] = file
            fileHandle.close()

    if (POSITIONS.__len__() > 0):
        print("Known positions:")
        for key in POSITIONS:
            print(POSITIONS[key])

def main(argv):
    pictures = defaultdict(list)
    picCount = 0
    picCountCheck = 0

    loadPositions()

    for root, subdirs, files in os.walk(PICTURES_SOURCE):
        for filename in files:
            if filename[-3:].lower() in {"jpg", "mp4", "avi", "3gp"}:

                picCount = picCount + 1

                pic = Picture()
                pic.fileName = filename
                pic.fileNameWithPath = root + "\\" + filename

                if PRINT_DEBUG:
                    print(pic.fileNameWithPath)

                picFileHandle = open(pic.fileNameWithPath, 'rb')

                picEXIF = exifread.process_file(picFileHandle, details=False)

                #objectKey is a tupple (year, month)
                if 'Image DateTime' in picEXIF:
                    objectKey = fromGPSDataToKey(picEXIF['Image DateTime'])
                elif 'EXIF DateTimeOriginal' in picEXIF:
                    objectKey = fromGPSDataToKey(picEXIF['EXIF DateTimeOriginal'])
                elif 'EXIF DateTimeDigitized' in picEXIF:
                    objectKey = fromGPSDataToKey(picEXIF['EXIF DateTimeDigitized'])
                else:
                    picCreationTime = datetime.datetime.fromtimestamp(os.path.getmtime(pic.fileNameWithPath))
                    if picCreationTime.month < 10:
                        objectKey = (str(picCreationTime.year), str("0" + str(picCreationTime.month)))
                    else:
                        objectKey = (str(picCreationTime.year), str(picCreationTime.month))

                if 'Image Make' in picEXIF and 'Image Model' in picEXIF:
                    pic.make = str(picEXIF['Image Make']).rstrip(' ')
                    pic.model = str(picEXIF['Image Model'])
                    pic.model = pic.model[0:15]
                    for remove in REMOVE_FROM_MODEL:
                        pic.model = pic.model.replace(remove, '')
                    pic.model = pic.model.rstrip(' ')

                if 'GPS GPSLatitude' in picEXIF and 'GPS GPSLatitudeRef' in picEXIF and 'GPS GPSLongitude' in picEXIF and 'GPS GPSLongitudeRef' in picEXIF:
                    latitude = convertToDegress(picEXIF['GPS GPSLatitude'], picEXIF['GPS GPSLatitudeRef'])
                    longitude = convertToDegress(picEXIF['GPS GPSLongitude'], picEXIF['GPS GPSLongitudeRef'])
                    picPoint = (latitude, longitude)
                    if vincenty(HOME, picPoint).kilometers > HOME_AREA:
                        pic.address = fromGPSToAddress(latitude, longitude)

                pictures[objectKey].append(pic)

                picFileHandle.close()

    for objectKey, picList in pictures.items():
        pic = picList[0]

        newPath = PICTURES_DESTINATION
        newPath = newPath + objectKey[0] + "\\" + objectKey[1]
        combainedAddresses = ""

        #iterate for the first time to get all addresses in one string
        for i, pic in enumerate(picList):
            if pic.address != "" and pic.address not in combainedAddresses:
                combainedAddresses = combainedAddresses + " " + pic.address

        if combainedAddresses != "":
            newPath = newPath + " -" + combainedAddresses

        for i, pic in enumerate(picList):
            picCountCheck = picCountCheck + 1

            wholePath = newPath

            if pic.make != "" or pic.model != "":
                wholePath = wholePath + "\\" + str(pic.make) + " " + str(pic.model)

            wholePath = wholePath + "\\" + pic.fileName

            if not os.path.exists(os.path.dirname(wholePath)):
                os.makedirs(os.path.dirname(wholePath))

            if PRINT_DEBUG:
                print(pic.fileNameWithPath)
                print(wholePath)

            try:
                #copyfile(pic.fileNameWithPath, wholePath) #copy
                os.rename(pic.fileNameWithPath, wholePath)  # move
            except FileExistsError:
                print("File :" + wholePath + " already exists!" )

    if picCount == picCountCheck:
        print("All pictures (" + str(picCount) + ") found were copied or moved :D")
    else:
        print("We've lost some picture on the way !!!")

    pass

if __name__ == "__main__":
    main(sys.argv)