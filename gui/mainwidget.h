#ifndef MAINWIDGET_H
#define MAINWIDGET_H

#include <QWidget>
#include <QProcess>
#include <QLabel>
#include <QLineEdit>
#include <QPushButton>
#include <QTextEdit>
#include <QString>
#include <QTextCodec>

class MainWidget : public QWidget
{
    Q_OBJECT

public:
    MainWidget(QWidget *parent = 0);
    ~MainWidget();

private slots:
    void Clicked();
    void Output();
    void configDialog();

private:
    QProcess    *python;
    QString      output;
    QLabel      *outputLabel;
    QLineEdit   *outputLineEdit;
    QLabel      *inputLabel;
    QLineEdit   *inputLineEdit;
    QPushButton *downloadButton;
    QPushButton *configButton;
    QTextEdit   *detail;

};

#endif // MAINWIDGET_H
