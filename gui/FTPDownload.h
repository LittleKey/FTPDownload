#include <QProcess>
#include <QString>

class FTPDownload
{
    public:
        FTPDownload(QString const filename);
        ~FTPDownload();

        void Input(QString const context);
        QString const Output(void);
        bool const Run(void);

    private:
        QString const filename;
        QProcess* program;
};
