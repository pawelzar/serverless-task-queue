import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# import sentry_sdk
# from sentry_sdk.integrations.aws_lambda import AwsLambdaIntegration

# sentry_sdk.init(
#     dsn="...",
#     integrations=[AwsLambdaIntegration()],
#     traces_sample_rate=1.0,
# )

SMTP_HOST = "smtp.mailtrap.io"
SMTP_PORT = 2525
SMTP_LOGIN = ""
SMTP_PASSWORD = ""


def hello(event, context):
    # wait_for_debug_client()
    body = {
        "message": "Go Serverless v3.0! Your function executed successfully!",
        "input": event,
    }

    title = event['Records'][0]['messageAttributes']['title']['stringValue']
    sender = "from@example.com"
    receiver = "mailtrap@example.com"
    message = MIMEMultipart()
    message["From"] = sender
    message["To"] = receiver
    message["Subject"] = title
    message_body = "This is a test e-mail message."
    message.attach(MIMEText(message_body, "plain"))
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_LOGIN, SMTP_PASSWORD)
        server.sendmail(sender, receiver, message.as_string())

    return {"statusCode": 200, "body": json.dumps(body)}


def wait_for_debug_client(timeout=15):
    """Utility function to enable debugging with Visual Studio Code"""
    import time, threading
    import sys, glob
    sys.path.append(glob.glob(".venv/lib/python*/site-packages")[0])
    import debugpy

    debugpy.listen(("0.0.0.0", 19891))
    class T(threading.Thread):
        daemon = True
        def run(self):
            time.sleep(timeout)
            print("Canceling debug wait task ...")
            debugpy.wait_for_client.cancel()
    T().start()
    print("Waiting for client to attach debugger ...")
    debugpy.wait_for_client()
