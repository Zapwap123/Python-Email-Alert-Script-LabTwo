import time
#from mailjet_rest import Client
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import os

import psutil

from dotenv import load_dotenv
import os

load_dotenv()

#api_key = os.getenv("MAILJET_API_KEY")
#api_secret = os.getenv("MAILJET_API_SECRET")

EMAIL_ADDRESS = os.getenv("GMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("GMAIL_PASSWORD")
Email_ADDRESS_RECEIVER = os.getenv("GMAIL_ADDRESS_RECEIVER")

# Define system time
current_time = time.localtime()
formatted_time = time.strftime("%Y-%m-%d %H:%M:%S",current_time)

# Define System thresholds ( 10% RAM, 50% free disk space, 10% CPU )
CPU_THRESHOLD = 2
RAM_THRESHOLD = 10
DISK_THRESHOLD = 50 

# Define the function to send email alerts
def send_alert(subject, message):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = Email_ADDRESS_RECEIVER
    msg.set_content(message)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
        print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {str(e)}")

    

# Check system metrics
cpu_usage = psutil.cpu_percent(interval=1)
ram_usage = psutil.virtual_memory().percent
disk_usage = psutil.disk_usage('/').percent

# Create alert message based on threshold breaches
alert_message = ""

if cpu_usage > CPU_THRESHOLD:
 alert_message += f"CPU usage is high: {cpu_usage}% (Threshold: {CPU_THRESHOLD}%)\n"
if ram_usage > RAM_THRESHOLD:
 alert_message += f"RAM usage is high: {ram_usage}% (Threshold: {RAM_THRESHOLD}%)\n"
if disk_usage > DISK_THRESHOLD:
 alert_message += f"Disk space is low: {100 - disk_usage}% free (Threshold: {DISK_THRESHOLD}% free)\n"

 # If any threshold is breached, send an email alert
if alert_message:
 send_alert(f"Python Monitoring Alert Alert-{formatted_time}", alert_message)
else:
 print("All system metrics are within normal limits.")
