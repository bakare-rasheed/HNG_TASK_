Messaging System with RabbitMQ/Celery and Python Application behind Nginx
Overview
This project involves deploying a Python application behind Nginx that interacts with RabbitMQ/Celery for email sending and logging functionality. The application has two main functionalities:

Sending an email using SMTP.
Logging the current time to a file.
Features
Email Sending: Uses RabbitMQ and Celery to queue and send emails asynchronously.
Logging: Logs the current time to /var/log/messaging_system.log.
Requirements
AWS Ubuntu instance
Python 3.12
RabbitMQ
Celery
FastAPI
Uvicorn
Nginx
Ngrok (for exposing local endpoints)
Local Setup

1. Install RabbitMQ
sudo apt update
sudo apt install rabbitmq-server
sudo systemctl enable rabbitmq-server
sudo systemctl start rabbitmq-server

2. Install Python and Create Virtual Environment
sudo apt update
sudo apt install python3.12 python3.12-venv python3.12-dev
python3.12 -m venv myenv
source myenv/bin/activate

3. Install Required Python Packages
pip install celery fastapi uvicorn

4. Create Project Directory Structure
mkdir messaging_system
cd messaging_system
touch main.py tasks.py

5. main.py
import logging
from fastapi import FastAPI, Request
from datetime import datetime
from tasks import send_email

app = FastAPI()

logging.basicConfig(filename='/var/log/messaging_system.log', level=logging.INFO)

@app.get("/")
async def root(request: Request):
    sendmail = request.query_params.get('sendmail')
    talktome = request.query_params.get('talktome')

    if sendmail:
        send_email.delay(sendmail)
        return {"message": f"Email to {sendmail} has been queued."}

    if talktome:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logging.info(f"Current time logged: {current_time}")
        return {"message": f"Current time logged at {current_time}."}

    return {"message": "Welcome to the Messaging System"}

6. tasks.py
from celery import Celery
import smtplib

app = Celery('tasks', broker='pyamqp://guest@localhost//')

@app.task
def send_email(recipient):
    sender = 'your-email@gmail.com'
    password = 'your-email-password'
    message = f"Subject: Test Email\n\nThis is a test email to {recipient}."

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(sender, password)
        server.sendmail(sender, recipient, message)

7. Configure Nginx
Install Nginx:

sudo apt install nginx
Create an Nginx configuration file:

sudo nano /etc/nginx/sites-available/messaging_system
Add the following content:
server {
    listen 80;

    server_name your-server-ip;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}


Enable the configuration:

bash
Copy code
sudo ln -s /etc/nginx/sites-available/messaging_system /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
8. Expose Local Application using Ngrok

./ngrok http 8000
9. Running the Application

Run the Uvicorn server:
uvicorn main:app --host 0.0.0.0 --port 8000

Start Celery worker:
celery -A tasks worker --loglevel=info