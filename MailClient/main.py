import sys
from PyQt6 import QtWidgets, uic

import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

while True:

    class MailGUI(QtWidgets.QMainWindow):

        def __init__(self):
            super(MailGUI, self).__init__()
            uic.loadUi("MailClientgui2.ui", self)
            self.show()

            self.loginbtn.clicked.connect(self.login)
            self.sendbtn.clicked.connect(self.send)
            self.attachmentbtn.clicked.connect(self.attach)

        def login(self):
            smtp_server = self.serverbtn.currentIndex()

            if self.serverbtn.currentIndex() == 0:
                smtp_server = "smtp.gmail.com"
            elif self.serverbtn.currentIndex() == 1:
                smtp_server = "smtp-mail.outlook.com"
            elif self.serverbtn.currentIndex() == 2:
                smtp_server = "smtp.seznam.cz"
            elif self.serverbtn.currentIndex() == 3:
                smtp_server = "smtp.mail.yahoo.com"

            try:
                
                self.server = smtplib.SMTP(smtp_server, 587)
                self.server.ehlo()
                self.server.starttls()
                self.server.ehlo()
                self.server.login(self.emailfld.text(), self.pwdfld.text())

                self.emailfld.setEnabled(False)
                self.pwdfld.setEnabled(False)
                self.smtpfld.setEnabled(False)
                self.portfld.setEnabled(False)
                self.loginbtn.setEnabled(False)

                self.tofld.setEnabled(True)
                self.tolbl.setEnabled(True)
                self.subjectlbl.setEnabled(True)
                self.subjectfld.setEnabled(True)
                self.attachmentlbl.setEnabled(True)
                self.attachmentbtn.setEnabled(True)
                self.textfld.setEnabled(True)
                self.textlbl.setEnabled(True)
                self.sendbtn.setEnabled(True)

                self.msg = MIMEMultipart()

            except smtplib.SMTPAuthenticationError:
                message_box = QtWidgets.QMessageBox()
                message_box.setText("Invalid login!")
                message_box.exec()
            except:
                message_box = QtWidgets.QMessageBox()
                message_box.setText("SMTP connection failed!")
                message_box.exec()

        def send(self):
            dialog = QtWidgets.QMessageBox()
            dialog.setText("Do you want to send this Email?")
            dialog.addButton(QtWidgets.QPushButton("Proceed"), QtWidgets.QMessageBox.ButtonRole.YesRole) 
            dialog.addButton(QtWidgets.QPushButton("Cancel"), QtWidgets.QMessageBox.ButtonRole.NoRole)

            if dialog.exec() == 0:
                try:
                    sender = self.emailfld.text()
                    receiver = self.tofld.text()
                    subject = self.subjectfld.text()
                    message_content = self.textfld.toPlainText()

                    if not sender or not receiver or not subject or not message_content:
                        raise ValueError("Missing required fields")

                    if not self.server:
                        raise ValueError("SMTP server not connected")

                    self.msg["From"] = sender
                    self.msg["To"] = receiver
                    self.msg["Subject"] = subject
                    self.msg.attach(MIMEMultipart(message_content, "plain"))
                    self.msg["From"] = self.emailfld.text()
                    self.msg["To"] = self.tofld.text()
                    self.msg["Subject"] = self.subjectfld.text()
                    self.msg.attach(MIMEText(self.textfld.toPlainText(), "plain"))
                    text = self.msg.as_string()
                    self.server.sendmail(sender, receiver, text)
                    #self.server.send(self.emailfld.text, self.tofld.text, text)

                    message_box = QtWidgets.QMessageBox()
                    message_box.setText("Email Sent!")
                    message_box.exec()

                except ValueError as e:
                    message_box = QtWidgets.QMessageBox()
                    message_box.setText(str(e))
                    message_box.exec()

                except smtplib.SMTPException as e:
                    message_box = QtWidgets.QMessageBox()
                    message_box.setText(f"Sending failed: {str(e)}")
                    message_box.exec()


        def attach(self):
            pass

    app = QtWidgets.QApplication(sys.argv)
    window = MailGUI()
    app.exec()
    