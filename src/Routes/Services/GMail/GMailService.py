##
## EPITECH PROJECT, 2022
## SafeTel-Back
## File description:
## GMailService
##

# mail connexion Import
import smtplib

class GMailService:

    def __init__(self):
        self.emailLogin = ""
        self.emailPassword = ""
        # load the credentials from a DB or file config

    def sendMail(self, userEmail, subject, content):
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()

            smtp.login(self.emailLogin, self.emailPassword) # first is the mail, the second is the password

            msg = f'Subject: {subject}\n\n{body}'

            smtp.sendmail(self.emailLogin, userEmail, msg) # first is the mail
