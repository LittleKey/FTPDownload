FTPDownload
===========

   ![LittleKey](https://github.com/LittleKey/gallery/blob/master/MyPic.png?raw=true)

   [I've special develop document.](https://github.com/LittleKey/FTPDownload/blob/master/src/README.md)



### Requirements

    Python 2.6 (or more later include 3.x)
    lftp (need cygwin for windows)

------------------------
### Usage

   > FTPDownload.py AnimeName

##### AnimeName
    动画名， 使用正则表达式匹配。会下载所有匹配的文件。


------------------------
### ChangeLog

    v0.1: first release.

    v0.2: fix code struct.

    v0.3: update interactive.

    v0.4: add ts download dir setting，I've special input passwd technique. update~

    v0.5: add '-t' argument, add it when you want to select whice TV.

    v1.0: debug: if TS's filename have TV, but not select TV in args that will don't download anything.

    v1.1: code refactoring.

    v1.2: fix some bug.

    v2.0: code refactoring.

    v2.1: i'm forgot it...

    v2.2: add lftp check...if you use this software in windows, you'll must set lftp's dir in settings.py file.

    v3.0: 3rd code refactoring....

    v3.1: 4th code refactoring...
