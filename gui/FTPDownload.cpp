#include "FTPDownload.h"

FTPDownload::FTPDownload(QString const filename="FTPDownload.cmd")
:filename(filename)
{
    program = new QProcess();
}

FTPDownload::~FTPDownload()
{
    delete program;
}

bool const FTPDownload::Run(void)
{
    program->start(filename);
}

void FTPDownload::Input(QString const context)
{
    if(program->isWritable()) {
        program->write(context, context.length());
    }
}

QString const FTPDownload::Output(void)
{
    if(program->isReadable())
        return program->readAll();

    return "";
}
