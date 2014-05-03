#include <QProcess>
#include <QString>
#include <QStringList>

class FTPDownload
{
    public:
        FTPDownload(QString const programName);
        ~FTPDownload();

        // 对程序做标准输入输出
        void Input(QString const context);
        QString const Output(void);
        // 同上，不过会阻塞
        void BlockInput(QString const context);
        QString const BlockOutput(void);
        // 提供参数并运行程序
        bool const Run(QStringList const arguments);

    private:
        QString const programName;
        QStringList const args;
        QProcess* program;
};
