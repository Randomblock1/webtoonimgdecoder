# Webtoon Image Decoder

![webtoon image decoder logo](logo.jpg)

## Decodes downloaded chapters from the [Webtoon](#webtoon) and [Tapas](#tapas) apps

---

## Webtoon

When you download a chapter from the Webtoon app (on Android), the JPGs are accessible at `/storage/emulated/0/Android/data/com.naver.linewebtoon/files/episode_download`.

But they can't be opened as JPG files! That's because the first 8 bits been XOR'd (bit flipped) to corrupt the magic number and confuse image software. (I know this sounds like nonsense but trust me it's real).

This Python script simply takes a folder as input, searches for JPGs, and decodes them by XOR'ing them again, skipping valid JPGs. GIFs and audio files are likely also encoded like this, but I haven't tested it so this script avoids them entirely.

### Getting the Webtoon JPGs

1. Through the Android Webtoon app, download any chapters you want to save.

2. Install ADB on your computer.

3. Enable ADB debugging on your phone and connect your phone to your computer.

4. Open up a terminal and run this command:

   `adb pull /storage/emulated/0/Android/data/com.naver.linewebtoon/files/episode_download output`

Done. All the data will be stored in the `output` folder. All you need to do is run `python3 decoder.py output` and wait.

### Webtoon Usage

Setup only needs to be done once.

`pip install -r requirements.txt`

Then, point the script at the image download folder.

`python3 decoder.py path/to/images`

It works _fast_! It processes 5409 images in only 9.7 seconds. Plus, it skips over already valid files; it only takes 0.8 seconds to check and skip over 5409 images.

---

## Tapas

Tapas stores normal JPEGs, but they're not named in any order, and they're named weirdly. So, we have to get the internal Tapas database and rename them in order. This is easier said than done, because we need root and the database doesn't always store the needed data.

### Getting the Tapas Data

1. Through the Tapas Android app on a rooted device or emulator, download some chapters.

2. Install ADB on your computer.

3. Enable ADB debugging on your phone and connect your phone to your computer. Run `adb root`.

4. Run `adb pull /data/data/com.tapastic/files/contents_v2` and `adb pull /data/data/com.tapastic/databases/tapas_room.db`.

### Tapas Usage

Setup only needs to be done once.

`pip install -r requirements.txt`

If the contents folder isn't named `contents_v2`, then point the script at the contents_v2 folder. The database must be named `tapas_room.db`.

`python3 tapas.py path/to/contents_v2`

It works instantly. It processes 957 images faster than you can blink.

---

## TODO

Add support for Webtoon music and GIFs. They're probably also encoded like this, but I'm not sure and I haven't checked.
