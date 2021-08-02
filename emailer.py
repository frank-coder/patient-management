import smtplib,ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import sys

class bcolors:
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"

def banner():
    print(bcolors.RED + "[-[-[]Simple Email Sender []]-]-]")
    print(bcolors.YELLOW + " Python is the best \n")

class Emailer:
    count = 0

    def __init__(self,sender,password):
        try:
            self.server = "smtp.gmail.com"
            self.port = 587
            self.frmAddr = sender
            self.password = password
            self.s = smtplib.SMTP(self.server,self.port)
            self.s.ehlo()
            self.s.starttls()
            self.s.ehlo()
            self.s.login(self.frmAddr,self.password)

        except Exception as e:
            print(f"Error: {e}")



    def send(self,receiver,message):
        try:

            self.subject = "Result of Your covid-19 Test"
            self.message = message
            self.target = receiver
            message = MIMEMultipart("alternative")
            message["Subject"] = self.subject
            message["From"] = self.frmAddr
            message["To"] = self.target
            #self.msg = """From: %s\nTo: %s\nSubject: %s\n%s\n
            #"""%(self.frmAddr,self.target,self.subject,self.message)
            part1 = MIMEText(self.message,"html")
            message.attach(part1)
            self.s.sendmail(self.frmAddr,self.target,message.as_string())
            
            self.count += 1
        except Exception as e:
            print(f"Error: {e}")

    def multi_send(self, EmailList,message):
        print(bcolors.RED + "\n[-[-[ Multi send...]-]-]")
        for mail in range(EmailList):
            self.send(mail,message)
        self.s.close()

if __name__ == "__main__":
    banner()
    email = Emailer()