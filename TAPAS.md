# Tapas

Tapas is similar to Webtoon in that they try not to just store ordered JPEGs. While Webtoon stores everything in a nice order, only xor'ing the files slightly, Tapas renames the files in a seemingly random order and stores the order as a list in tapas_room.db.

Additionally, while Webtoon episodes can be got without root, Tapas stores its stuff in /data/data/com.tapastic. However, it's trivial to create an emulator with ADB root access.

The JPEGs are stored at `/data/data/com.tapastic/files/contents_v2/seriesId/chapterId/`. They are named weirdly, like `[Ljava.lang.Object;@9596b32`, but they are not encoded. You just have to change the extension to `.jpg`, and it will work. However, that's not much use if they're all out of order (which they are).

Luckily, the SQLITE database at `/data/data/com.tapastic/databases/tapas_room.db` has every file ordered in a table called `download_episode`. In order to rename these to their correct filename (1.jpg, 2.jpg etc...) we simply need to read a `fileUrl` field, and match the files. For every match we get in one chapter, we rename the file to a counter that goes up.

The chapters are separated by rows, but the Sqlite database needs to be saved completely first (or else it will be in memory and not saved.) You might need to close the app, redownload chapters, or open them before getting the database. Sometimes it gets saved, sometimes it doesn't.
