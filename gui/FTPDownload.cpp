#include "FTPDownload.h"

FTPDownload::FTPDownload(QString const programName="../src/FTPDownload.py")
:programName(programName)
{
    program = new QProcess();
}

FTPDownload::~FTPDownload()
{
    delete program;
}

bool const FTPDownload::Run(QStringList const arguments)
{
	args = arguments;
    program->start(programName, args);

    if (!program->waitForStarted())
    	return false;
}

void FTPDownload::Input(QString const context)
{
    if (program->isWritable()) {
        program->write(context, context.length());
    }
}

void FTPDownload::BlockInput(QString const context)
{
    if (program->isWritable() and program->waitForReadyWritten()) {
        program->write(context, context.length());
    }
}

QString const FTPDownload::Output(void)
{
    if (program->isReadable() and program->waitForReadyRead())
        return program->readAll();

    return "";
}
