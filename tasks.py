import smtplib
from celery import Celery
import os

celery = Celery('tasks', broker='pyamqp://guest@localhost//')

@celery.task
def send_email(recipient):
    sender = "bakarerasheed.a38@gmail.com"
    password = os.getenv('SMTP_PASSWORD')  # Ensure you get the app password from environment variables

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)
        server.sendmail(sender, recipient, "Subject: Test Email\n\nThis is a test email from Celery, developed by Bakare Rasheed a Devops Engineer @ HNG-Internship Stage 3 Project.")

    print(f"Email sent to {recipient}")
