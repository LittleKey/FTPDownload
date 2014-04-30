#include <QtGui>
#include <QIcon>
#include "dialog.h"

Dialog::Dialog(QWidget *parent)
    :QDialog(parent)
{
    hostLabel       = new QLabel(tr("Host"));
    hostLineEdit    = new QLineEdit();
    hostLabel->setBuddy(hostLineEdit);

    userLabel       = new QLabel(tr("User"));
    userLineEdit    = new QLineEdit();
    userLabel->setBuddy(userLineEdit);

    pwdLabel        = new QLabel(tr("Password"));
    pwdLineEdit     = new QLineEdit();
    pwdLabel->setBuddy(pwdLineEdit);

    sshLabel        = new QLabel(tr("SSH"));
    sshLineEdit     = new QLineEdit();
    sshLabel->setBuddy(sshLineEdit);

    animeLabel      = new QLabel(tr("Anime"));
    animeLineEdit   = new QLineEdit();
    animeLabel->setBuddy(animeLineEdit);

    epLabel         = new QLabel(tr("EP"));
    epLineEdit      = new QLineEdit();
    epLabel->setBuddy(epLineEdit);

    tvLabel         = new QLabel(tr("TV"));
    tvLineEdit      = new QLineEdit();
    tvLabel->setBuddy(tvLineEdit);

    okButton        = new QPushButton(tr("OK"));
    cancelButton    = new QPushButton(tr("Cancel"));
    cancelButton->setDefault(true);
    okButton->setEnabled(false);

    connect(hostLineEdit, SIGNAL(textChanged(QString)), this, SLOT(enableOKButton(QString)));
    connect(cancelButton, SIGNAL(clicked()),            this, SLOT(close()));
//    connect(okButton, SIGNAL(clicked()), this, SLOT(writeChange());

    QVBoxLayout *leftLayout     = new QVBoxLayout();
    leftLayout->addWidget(hostLabel);
    leftLayout->addWidget(userLabel);
    leftLayout->addWidget(pwdLabel);
    leftLayout->addWidget(sshLabel);
    leftLayout->addWidget(animeLabel);
    leftLayout->addWidget(epLabel);
    leftLayout->addWidget(tvLabel);

    QVBoxLayout *rightLayout    = new QVBoxLayout();
    rightLayout->addWidget(hostLineEdit);
    rightLayout->addWidget(userLineEdit);
    rightLayout->addWidget(pwdLineEdit);
    rightLayout->addWidget(sshLineEdit);
    rightLayout->addWidget(animeLineEdit);
    rightLayout->addWidget(epLineEdit);
    rightLayout->addWidget(tvLineEdit);

    QHBoxLayout *buttomLayout   = new QHBoxLayout();
    buttomLayout->addWidget(okButton);
    buttomLayout->addWidget(cancelButton);

    QHBoxLayout *topLayout      = new QHBoxLayout();
    topLayout->addLayout(leftLayout);
    topLayout->addLayout(rightLayout);

    QVBoxLayout *mainLayout     = new QVBoxLayout();
    mainLayout->addLayout(topLayout);
    mainLayout->addLayout(buttomLayout);
    setLayout(mainLayout);

    setWindowTitle(tr("Configure"));
    setWindowIcon(QIcon(":/new/png/logo.png"));
}

void Dialog::enableOKButton(const QString &text)
{
    okButton->setEnabled(!text.isEmpty());
}

Dialog::~Dialog()
{

}
