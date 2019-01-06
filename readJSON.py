import json
import os
import sys


def main(argv):
    with open('e:\projects\picPySort\json2.txt', encoding='utf8') as content_file:
        content = content_file.read()

    data = json.loads(content)

    #if len(data["Response"]) > 0:
    if len(data["address"]) > 0:
        try:
            # Here
            #result = data["Response"]["View"][0]["Result"][0]["Location"]["Address"]["City"]
            # openstreetmap
            #result = data["address"]["city"]
            if "fsfd" in data["address"]:
                result = ""
            elif "village" in data["address"]:
                result = data["address"]["village"]
        except IndexError:
            print("Error while attempting to retrive city name")

    print(result)

if __name__ == "__main__":
    main(sys.argv)

