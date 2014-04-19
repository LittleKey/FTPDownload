FTPDownload
===========

   自动从ftp下载(主要用于：尚未更新的)ts

------------------------

### Requirements

    Python 3.3.5 (or more later)
    lftp (need cygwin for windows)

------------------------
### Usage

   FTPDownload.py AnimeName [num] [-t TV]

##### AnimeName
   动画名

##### num [dafault: 0]
    指定要下集数的范围
    下载集数的范围是[num-last]
   
   >p.s: 只会下最新一集

##### -t
    指定要选择的电视台

##### TV [default: '']
    电视台名


------------------------
### ChangeLog

   * 'v0.1' : first release.

   * 'v0.2' : fix code struct.    

   * 'v0.3' : update interactive.

   * 'v0.4' : add ts download dir setting，I've special input passwd technique. update~

   * 'v0.5' : add '-t' argument, add it when you want to select whice TV.

   * 'v1.0' : debug: if TS's filename have TV, but not select TV in args that will don't download anything.