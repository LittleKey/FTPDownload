#include <QtGui>
#include "mainwidget.h"
#include "dialog.h"

MainWidget::MainWidget(QWidget *parent)
    : QWidget(parent)
{
    inputLabel              = new QLabel(tr("Your Python Script:"));
    inputLineEdit           = new QLineEdit(tr(""));
    configButton            = new QPushButton(tr("Configure"));
    downloadButton          = new QPushButton(tr("Download"));

    outputLabel             = new QLabel(tr("Detail:"));
    detail                  = new QTextEdit();
    detail->setReadOnly(true);

    python                  = new QProcess();

    connect(configButton,   SIGNAL(clicked()),          this, SLOT(configDialog()));
    connect(inputLineEdit,  SIGNAL(returnPressed()),    this, SLOT(Clicked()));
    connect(downloadButton, SIGNAL(clicked()),          this, SLOT(Clicked()));
    connect(python,         SIGNAL(readyRead()),        this, SLOT(Output()));

    QVBoxLayout *lefttop    = new QVBoxLayout();
    lefttop->addWidget(inputLabel);
    lefttop->addWidget(inputLineEdit);

    QVBoxLayout *righttop   = new QVBoxLayout();
    righttop->addWidget(configButton);
    righttop->addWidget(downloadButton);

    QHBoxLayout *top        = new QHBoxLayout();
    top->addLayout(lefttop);
    top->addLayout(righttop);

    QVBoxLayout *centLayout = new QVBoxLayout();
    centLayout->addWidget(outputLabel);
    centLayout->addWidget(detail);

    QVBoxLayout *mainLayout = new QVBoxLayout();
    mainLayout->addLayout(top);
    mainLayout->addLayout(centLayout);
    setLayout(mainLayout);
    setWindowTitle(tr("FTP Downloader"));
    setWindowIcon(QIcon(":/new/png/logo.png"));

    resize(640, 480);
}

MainWidget::~MainWidget()
{

}

void MainWidget::configDialog()
{
    Dialog *dialog = new Dialog();
    dialog->show();
}

void MainWidget::Clicked()
{
    QString input  = inputLineEdit->text();
    python->start(input);
    output = tr("");
    detail->setText(output);
}

void MainWidget::Output()
{
    output += python->readAll();
    detail->setText(output);
}
