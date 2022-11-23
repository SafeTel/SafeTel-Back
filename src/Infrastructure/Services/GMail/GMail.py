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
        #self.cred_login, cred_password = self.db.PullGMailCreds()
        #self._emaillogin = cred_login
        #self._emailpassword = cred_password
        #self._MailService = smtplib.SMTP('localhost', 8070)


    def SendMail(self, useremail, object, content):
        import sys

        print(useremail, file=sys.stderr)
        print(object, file=sys.stderr)
        print(content, file=sys.stderr)

        import requests
        requests.post(
            "https://api.mailgun.net/v3/sandboxfd26e18457f049e78ab60a93ee8da368.mailgun.org/messages",
            auth = (
                "api",
                "adbd7ba87cc70ae952a7b6ebb4dbb48e-69210cfc-09ba1974"
            ),
            data={
                "from": "Mailgun Sandbox <postmaster@sandboxfd26e18457f049e78ab60a93ee8da368.mailgun.org>",
                "to": useremail,
                "subject": object,
                "text": content
            }
        ) # FIXME: URGEN HOTFIX SEE LATER

        return

        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
                mail_data = f'Subject: {object}\n\n{content}'


                self._MailService.ehlo()
                self._MailService.starttls()
                self._MailService.ehlo()

                self._MailService.sendmail(self._email, useremail, mail_data)
                #smtp.login(self.emaillogin, self.emailpassword)
                #smtp.sendmail(self.emaillogin, useremail, mail_data)
        except ValueError:
            import sys
            print("/!\\ WARNING: GMail Service not connected to any Account! /!\\",  file=sys.stderr)
