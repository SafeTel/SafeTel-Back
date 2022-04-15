##
## SAFETEL PROJECT, 2022
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
        self.emaillogin = cred_login
        self.emailpassword = cred_password

    def SendMail(self, useremail, object, content):
        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
                smtp.ehlo()
                smtp.starttls()
                smtp.ehlo()

                mail_data = f'Subject: {object}\n\n{content}'

                smtp.login(self.emaillogin, self.emailpassword)
                smtp.sendmail(self.emaillogin, useremail, mail_data)
        except ValueError:
            import sys
            print("/!\\ WARNING: GMail Service not connected to any Account! /!\\",  file=sys.stderr)
