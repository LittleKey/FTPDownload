Dev_Document
============

   需求总是在变化的。。。

## 需求

   * GUI
   * more ftp client support
   * code refactoring
   * add N:N support

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

##### Code refactoring

    重构后端， 'CK', 'Listen'的类之间的关系设计得不怎么好....重新弄一下才行

##### Add N:N support

    添加N:N 支持，可以同时在多个FTP服务器中监视多个文件

> 待补充

------------------