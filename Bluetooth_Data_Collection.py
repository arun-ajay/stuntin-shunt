'''
PLEASE NOTE
 I've omitted the following:
 In def_text alert():
    account_side -> key
    auth_token -> key
    to -> phone number
    from -> phone number
    
 In email_alert():
    email_user -> email of sender
    email_password -> email password
    email_send -> email of receiver
'''

import serial
from datetime import datetime
import csv
from itertools import zip_longest
from twilio.rest import Client
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

'''Twilio Text Messaging System Function for Patient'''
def text_alert():
    account_sid = "OMITTED"
    auth_token = "OMITTED"

    client = Client(account_sid, auth_token)

    client.messages.create(
          to = "OMITTED",
          from_="OMITTED",
          body = "Shunt Obstruction Detected. Please contact your physician immediately."
    )

'''Email Alert Messaging System Function for Physician'''
def email_alert():
    email_user = 'OMITTED'
    email_password = 'OMITTED'
    email_send = 'OMITTED'

    subject = 'Alert: Shunt Obstruction Detection for Patient John Doe'

    msg = MIMEMultipart()
    msg['From'] = email_user
    msg['To'] = email_send
    msg['Subject'] = subject

    body = 'Patient John Doe is experiencing a Shunt Obstruction. Attached is the data collected.'
    msg.attach(MIMEText(body,'plain'))

    filename='shunt.csv'
    attachment =open(filename,'rb')

    part = MIMEBase('application','octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition',"attachment; filename= "+filename)

    msg.attach(part)
    text = msg.as_string()
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    server.login(email_user,email_password)


    server.sendmail(email_user,email_send,text)
    server.quit()


'''Data Collection of States and Times'''
FSR_Log_Binary = [] # 0 = Closed, 1 = open
FSR_Times = []

Prox_Log_Binary = [] # 0 = No flow, 1 = flow, INITIALIZE FIRST VALUE USING 0 AND DATETIME
Prox_Times = []

'''Flag to break out of while loop'''
obstruction = False




'''Initialize Bluetooth Pathway'''
print("Initiating connection to Shunt...")
bluetooth = serial.Serial(port = "COM7", baudrate= 9600, timeout= 5 ) ## Use OUTGOING connection
print("Connected.")

time_previous = datetime.now()
'''Data Collection'''
while obstruction == False:
    line = (bluetooth.readline().decode())
    print(line)
    timenow = datetime.now()
    seconds = (timenow-time_previous).total_seconds()
    print(seconds, "seconds")
    if seconds > 15:
        break
    if line.find("Open") != -1:
        FSR_Log_Binary.append("Open")
        FSR_Times.append(datetime.now().strftime('%m/%d/%y %H:%M:%S'))
        time_previous = datetime.now()

    elif line.find("Closed") != -1:
        FSR_Log_Binary.append("Closed")
        FSR_Times.append(datetime.now().strftime('%m/%d/%y %H:%M:%S'))
        time_previous = datetime.now()
    elif line.find("No Flow") != -1:
        Prox_Log_Binary.append("No Flow")
        Prox_Times.append(datetime.now().strftime('%m/%d/%y %H:%M:%S'))
        time_previous = datetime.now()
    elif line.find("Flow detec") != -1:
        Prox_Log_Binary.append("Flow")
        Prox_Times.append(datetime.now().strftime('%m/%d/%y %H:%M:%S'))
        time_previous = datetime.now()

'''Data file creation'''
Total_Data = [FSR_Log_Binary,FSR_Times,Prox_Log_Binary,Prox_Times]
export_data = zip_longest(*Total_Data, fillvalue = '')
with open('shunt.csv', 'w', encoding="ISO-8859-1", newline='') as myfile:
    wr = csv.writer(myfile)
    wr.writerow(("FSR State", "FSR TIME", "PROX BINARY", "PROX TIME"))
    wr.writerows(export_data)
myfile.close()
text_alert()
email_alert()
