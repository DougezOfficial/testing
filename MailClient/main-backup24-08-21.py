import sys
from PyQt6 import QtWidgets, uic

import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

class MailGUI(QtWidgets.QMainWindow):

    def __init__(self):
        super(MailGUI, self).__init__()
        uic.loadUi("MailClientgui2.ui", self)
        self.show()

        
        self.loginbtn.clicked.connect(self.login)
        self.sendbtn.clicked.connect(self.send)
        self.attachmentbtn.clicked.connect(self.attach)

    def login(self):
        smtp_servers = [
            "smtp.gmail.com",
            "smtp-mail.outlook.com",
            "smtp.seznam.cz",
            "smtp.mail.yahoo.com"
        ]

        
        smtp_server = smtp_servers[self.serverbtn.currentIndex()]

        try:
            # Connect to the SMTP server
            self.server = smtplib.SMTP(smtp_server, 587)
            self.server.ehlo()
            self.server.starttls()
            self.server.ehlo()
            self.server.login(self.emailfld.text(), self.pwdfld.text())

            
            self.emaillbl.setEnabled(False)
            self.emailfld.setEnabled(False)
            self.pwdlbl.setEnabled(False)
            self.pwdfld.setEnabled(False)
            self.serverlbl.setEnabled(False)
            self.serverbtn.setEnabled(False)
            self.loginbtn.setEnabled(False)

            self.tolbl.setEnabled(True)
            self.tofld.setEnabled(True)
            self.subjectlbl.setEnabled(True)
            self.subjectfld.setEnabled(True)
            self.attachmentlbl.setEnabled(True)
            self.attachmentbtn.setEnabled(True)
            self.textlbl.setEnabled(True)
            self.textfld.setEnabled(True)
            self.sendbtn.setEnabled(True)

            self.msg = MIMEMultipart()

        except smtplib.SMTPAuthenticationError:
            QtWidgets.QMessageBox.warning(self, "Error", "Invalid login credentials!")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"SMTP connection failed: {str(e)}")

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
                self.msg.attach(MIMEText(message_content, "plain"))
                text = self.msg.as_string()
                self.server.sendmail(sender, receiver, text)

                QtWidgets.QMessageBox.information(self, "Success", "Email Sent!")

            except ValueError as e:
                QtWidgets.QMessageBox.warning(self, "Warning", str(e))
            except smtplib.SMTPException as e:
                QtWidgets.QMessageBox.critical(self, "Error", f"Sending failed: {str(e)}")

    def attach(self):
        options = QtWidgets.QFileDialog.options()
        filenames, _ = QtWidgets.QFileDialog.getOpenFileNames(self, "Open File", "", "All Files (*.*)", options=options)
        if filenames:
            for filename in filenames:
                with open(filename, "rb") as attachment:
                    p = MIMEBase("application", "octet-stream")
                    p.set_payload(attachment.read())
                    encoders.encode_base64(p)
                    p.add_header("Content-Disposition", f"attachment; filename={filename.split('/')[-1]}")
                    self.msg.attach(p)
                    current_text = self.attachmentlbl.text()
                    if current_text.endswith(":"):
                        self.attachmentlbl.setText(current_text + " " + filename.split('/')[-1])
                    else:
                        self.attachmentlbl.setText(current_text + ", " + filename.split('/')[-1])

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MailGUI()
    app.exec()
