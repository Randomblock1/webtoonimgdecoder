# Meant to decode Tapas code-named downloaded images.
# Download the Tapas chapters on a rooted Android and enable ADB then run
# adb root
# adb pull /data/data/com.tapastic/files/contents_v2
# from your computer, when it's attached to your phone with ADB.
# These JPGs are just renamed very strangely.

# You also need the database to match the files to numbers.
# Exit the app completely before doing this.
# adb pull /data/data/com.tapastic/databases/tapas_room.db

# The filenames are in the table download_episode.

from sys import argv
from sqlite3 import connect
from json import loads
from os import rename
from re import sub
from rich.console import Console
from rich.progress import track


if len(argv) > 2:
    exit("Too many arguments.")
elif len(argv) == 2:
    inputFolder = argv[1]
else:
    inputFolder = "contents_v2"

alreadyProcessed = 0
database = connect("tapas_room.db")
c = database.cursor()
c.execute("SELECT contents FROM download_episode")
data = c.fetchall()
Console().print("Processing " + str(len(data)) + " chapters.")
for row in data:
    filedata = loads(row[0])
    counter = 0
    for image in track(range(len(filedata))):
        counter += 1
        image = filedata[image]["fileUrl"]
        image = str(image).replace(
            "/data/user/0/com.tapastic/files/contents_v2", inputFolder
        )
        imageNew = sub("[^\/]+$", str(counter) + ".jpg", image)
        try:
            rename(image, imageNew)
        except FileNotFoundError:
            alreadyProcessed += 1

if alreadyProcessed != 0:
    Console().print(str(alreadyProcessed) + " images already processed.")

Console().print("All webtoons decoded! 🎉", style="bold green")
