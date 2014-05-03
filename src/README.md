Dev_Document
============

   需求总是在变化的。。。

## 需求

   * GUI
   * more ftp client support
   * add N:N support
   * update usage

##### GUI

   不管怎么说还是有个GUI好使啊....

   * 使用C++开发
   * 使用Qt库


         1. 使用QProcess 运行后端程序并进行通信

> 待补充

##### More ftp client support

   添加更多的ftp客户端的支持，希望也能自己写一个

   * 最好使用Python开发


         1. 需要能进行ssl验证，即可以登陆有ssl验证的ftp
         2. 能够获取文件列表，即在FTP使用ls -l命令所获得的信息
         3. 能够从FTP下载文件，并要求有‘新下载’，‘续传’，以及‘已完成’三种方式

##### Add N:N support

   添加N:N 支持，可以同时在多个FTP服务器中监视多个文件
   已实现1:N支持

    现在的设计是:使用listener与getor配合,监视与下载文件.
          * 一个路径名对应一个listener
          * 一个文件名对应一个getor
          * 一个listener对应同一路径名的多个getor

##### Update usage

   使用Downloader与FTP配合，可以实现对一个FTP内任意数量的文件进行(监视)下载

   * 稍微扩展后可以实现对多个FTP的支持(暂时没有这种需求，所以放置play
   * 使用了一个线程锁，预防lftp的使用竞争


> 待补充

------------------
