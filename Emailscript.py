import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
import glob

def email():

    # sender and receiver
    fromaddr = "frommail@gmail.com"
    toaddr = "tomail@gmail.com"

    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr

    # create header
    msg['Subject'] = "Your subject"

    # text content of the email
    body = '''Hello,  
        This is an automated script, that sends an email
        everytime a new file appears.
        It also put the new file into the email, so that you can see it

        Thanks
        '''

    msg.attach(MIMEText(body, 'plain'))

    # select the file to be send (in this case the newest .mp4 file)
    filename = "yourfilename.mp4"
    list_of_files = glob.glob('pathtoyourfolder*.mp4')  # you can use the file extension you need
    latest_file = max(list_of_files, key=os.path.getctime)

    attachment = open(latest_file, "rb")

    # name MIMEBase as 'p'
    p = MIMEBase('application', 'octet-stream')

    # put the payload in the encoded form
    p.set_payload((attachment).read())

    # encode to base64
    encoders.encode_base64(p)

    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    # link the 'p' instance to 'msg'
    msg.attach(p)

    # start SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)

    # start TLS for security
    s.starttls()

    # authentification (password)
    s.login(fromaddr, "password from sending mailacc")

    # put th multipart msg into a string
    text = msg.as_string()

    # send mail
    s.sendmail(fromaddr, toaddr, text)

    print("succes!")


if __name__ == "__main__":
    patterns = "*"
    ignore_patterns = ""
    ignore_directories = False
    case_sensitive = True
    my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)

# create function for the email
def on_created(event):
    email()
    print(f"New file!")

my_event_handler.on_created = on_created

# folder observation
path = "pathtoyourfolder"
go_recursively = True
my_observer = Observer()
my_observer.schedule(my_event_handler, path, recursive=go_recursively)

my_observer.start()
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    my_observer.stop()
    my_observer.join()

# this is needed to work fine on windows
input()
