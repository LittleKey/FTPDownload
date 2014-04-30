首先不得不說寫GUI真的有點累，或許是我剛開始接觸圖形化編程的緣故！

本GUI屬於未完成品，大部份功能尚未實現，剩下的部份正在著手解決，說明部份也正在寫...


Requirement : Python 3.3.5 + Qt 4.8.6

OS : Xubuntu 14.04 x64

如果你需要自己編譯的話：

sudo apt-get install aptitude

sudo aptitude install libqt4-dev libqt4-dbg libqt4-opengl-dev libc6 libc6-dev libqt4-gui libqt4-sql qt4-dev-tools qt4-doc qt4-designer qt4-qtconfig

如果你在使用Qt Creator的IDE的話，只需要打開pro工程檔案，重新配置即可

如果你在使用純Command Line的話，請按照以下步驟：

1.新建一個資料夾例如ftpgui並將標頭(Header)、源碼(cpp)以及資源(Resource)檔案放入該資料夾

2.進入該資料夾，執行qmake -project生成一個無關平臺的項目檔案(ftpgui.pro)

3.執行qmake ftpgui.pro生成一個與平臺相關的Makefile檔案

4.執行make生成對應平臺的二進制檔案(ftpgui)

5.執行./ftpgui

6.執行make clean清理中間產生的目標檔案


未完待續...
