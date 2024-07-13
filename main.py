from fastapi import FastAPI, Request
import logging
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
