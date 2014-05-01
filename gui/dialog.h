#ifndef DIALOG_H
#define DIALOG_H

#include <QDialog>
#include <QLabel>
#include <QLineEdit>
#include <QPushButton>
#include <QString>

class Dialog : public QDialog
{
    Q_OBJECT

public:
    Dialog(QWidget *parent = 0);
    ~Dialog();

private slots:
    void enableOKButton(const QString &text);
//    void writeChange();

private:
    QLabel      *hostLabel;
    QLabel      *userLabel;
    QLabel      *pwdLabel;
    QLabel      *sshLabel;
    QLabel      *animeLabel;
    QLabel      *epLabel;
    QLabel      *tvLabel;
    QLineEdit   *hostLineEdit;
    QLineEdit   *userLineEdit;
    QLineEdit   *pwdLineEdit;
    QLineEdit   *sshLineEdit;
    QLineEdit   *animeLineEdit;
    QLineEdit   *epLineEdit;
    QLineEdit   *tvLineEdit;
    QPushButton *okButton;
    QPushButton *cancelButton;
};

#endif // DIALOG_H
