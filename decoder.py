# Meant to decode Webtoon encoded downloaded images.
# Download the Webtoon chapters on an Android and enable ADB then run
# adb pull /storage/emulated/0/Android/data/com.naver.linewebtoon/files/episode_download outputfolder
# from your computer, when it's attached to your phone with ADB.
# These JPGs are just XOR'd for the first 8 bytes.

# Decompile the Webtoon APK with JADX if you want to see
# the Java source function used to reverse engineer this.
# Original function is at
# src/main/java/com/naver/linewebtoon/common/util/CryptoInputStream.java/read().

from pathlib import Path, PosixPath
from sys import argv

from rich.console import Console
from rich.progress import track


def readBytes(byte_array: bytearray, offset: int, length: int) -> bytearray:
    """Returns part of a byte array, specifying offset and length."""
    fetchedBytes = bytearray(length)
    for bytecount in range(length):
        fetchedBytes[bytecount] = byte_array[bytecount + offset]
    return fetchedBytes


def xorBytes(byte_array: bytearray, magicbyte: bytes) -> bytearray:
    """Reads a byte array and xors every byte with the input byte."""
    inputLength = len(byte_array)
    xorArray = bytearray(inputLength)
    for i in range(inputLength):
        xorArray[i] = byte_array[i] ^ magicbyte
    return xorArray


def xorJpg(filename: PosixPath):
    """Xor-decodes a JPG."""
    # Load file.
    file = open(filename, "rb")
    filedata = file.read()
    file.close()

    # If file is empty, the program goofed up.
    if filedata == b"":
        exit("Error! File " + filename + " is empty!")

    # Convert binary file to byte array.
    fileBytes = bytearray(filedata)
    # Read the first 8 bytes.
    gotBytes = readBytes(fileBytes, 0, 8)

    # If the bytes aren't already decoded, decode it.
    if gotBytes != bytearray(b"\xff\xd8\xff\xe0\x00\x10\x4a\x46"):
        output = xorBytes(gotBytes, 0xFF)
        outFile = open(filename, "wb")
        # Combine xor'd bytes and original bytes, and rewrite original file.
        # Obviously we need to skip the first 8 original bytes.
        outFile.write(output + readBytes(fileBytes, 8, (len(filedata) - 8)))
        outFile.close()
    else:  # Otherwise, skip it.
        global alreadyDecoded
        alreadyDecoded += 1


if len(argv) < 2:
    Console().print(
        "Please specify a folder to scan. Example: python3 decoder.py imagefolder",
        style="bold red",
    )
    exit(1)
if len(argv) > 2:
    Console().print(
        "Too many arguments! Please specify one folder to scan. It will be scanned recursively.",
        style="bold red",
    )
    exit(1)

# Set first argument as input path
inputPath = Path(argv[1])

# Initialize some variables
pathArray = []
alreadyDecoded = 0

# We need to get a list of all file paths for Rich progress to work.
# For now, this only processes JPGs.
# I don't know if GIFs are the same, or how music is stored, etc.
for path in inputPath.glob("**/*[0-9].jpg"):
    pathArray.append(str(path))

# Now, track the progress.
Console().print("Need to process " + str(len(pathArray)) + " images.")
for jpg in track(pathArray):
    xorJpg(jpg)

# If some images were already decoded, say so.
if alreadyDecoded != 0:
    Console().print(
        str(alreadyDecoded)
        + " out of "
        + str(len(pathArray))
        + " images were already decoded."
    )

Console().print("All webtoons decoded! 🎉", style="bold green")
