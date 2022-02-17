##
## EPITECH PROJECT, 2022
## SafeTel-Back
## File description:
## GMailService
##

### INFRA
# mail connexion Import
import smtplib
# Service DB import
from Infrastructure.Services.MongoDB.Casper02.GoogleServiceDB import GoogleServiceDB

# Service class to send emails
class GMail:
    def __init__(self):
        self.db = GoogleServiceDB()
        cred_login, cred_password = self.db.PullGMailCreds()
        self.emailLogin = cred_login
        self.emailPassword = cred_password

    def sendMail(self, userEmail, object, content):
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()

            mail_data = f'Subject: {object}\n\n{content}'

            smtp.login(self.emailLogin, self.emailPassword)
            smtp.sendmail(self.emailLogin, userEmail, mail_data)
