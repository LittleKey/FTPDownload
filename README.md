FTPDownload
===========

   [![LittleKey](https://github.com/LittleKey/gallery/blob/master/MyPic.png?raw=true)](https://github.com/LittleKey)

   [I've special develop document.](https://github.com/LittleKey/FTPDownload/blob/master/src/README.md)



### Requirements

    Python 2.6 (or more later include 3.x)
    lftp (need cygwin for windows)

------------------------
### Usage

   > FTPDownload.py AnimeName [moreAnimeName]

   动画名， 使用正则表达式匹配。会下载所有匹配的文件。
   可以输入多个，并附带(FTP上)目录名。目录名默认为'.'

   **p.s: basename尚不能使用 '\', '\w', '\d' 等正则表达式字符. dirname不支持正则表达式.**

  > ftpinfo.json

   用于提供ftp的信息，如果没有提供这个文件则会从标准输入获取
   使用json格式 e.p:

    {
        "host": "ftp://ftp.abc.com:21",
        "user": "account",
        "passwd": "password",
        "ssh": ""
    }

#### New Version(4.x)

   添加 '-n' 参数使用新版本

   支持任意python的正则表达式, dirname也支持正则表达式

   其他的用法相同, 占用的系统资源或许比旧版本多.
   不再使用线程锁, 所以会多lftp并发估计是个异步IO(但是貌似有阻塞啊)

   尚未添加python3支持, 反正我这测试没过....0r2

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

    v3.2: add Download class, support any filenames input.

    v3.3: from settings.py file move lftp command to lftp.json file. update lftp env_set.
    remove LOG_Filename and CONF_Filename settings, remove FTP_FileList_Dir setting. update Processor.

    v3.4: update settings.

    v3.5 update...

    v4.0 suppoer any python's RE, and add dirname support RE, maybe it isn't support Python3.
