#include <QApplication>
#include <QTextCodec>
#include "mainwidget.h"

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);
    QTextCodec::setCodecForTr(QTextCodec::codecForName("UTF8"));
    MainWidget win;
    win.show();

    return app.exec();
}
