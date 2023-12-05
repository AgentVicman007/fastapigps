from geopy.distance import geodesic
from models import RawData, Address
from database import SessionLocal
from celery import Celery, schedules
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os

# Start Redis and workes
# redis-server /usr/local/etc/redis.conf
# celery -A tasks beat --loglevel=info
# celery -A tasks worker --loglevel=info



# Celery configuration
app = Celery('tasks', broker='redis://127.0.0.1:6379/0')
app.conf.beat_schedule = {
    'check-gps-every-minute': {
        'task': 'tasks.check_gps_and_send_email',
        'schedule': schedules.crontab(minute='*'),
    },
}

# Email configuration
EMAIL_HOST = 'email-smtp.us-east-1.amazonaws.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'AKIARZQ3RWQZ2CVBZMDB'  # Replace with your AWS Access Key ID
EMAIL_HOST_PASSWORD = 'BIqDT0ivViENmX/OhrIe39m9NzHcH0ytuJadHxSdfYtm'  # Replace with your AWS Secret Access Key
DEFAULT_FROM_EMAIL = 'victor@swiftpigeon.io'

@app.task
def check_gps_and_send_email():
    db = SessionLocal()
    try:
        today = datetime.utcnow().date()
        raw_data_entries = db.query(RawData).filter(RawData.created_at >= today).all()

        emails_sent_count = 0
        emails_sent_to = []

        for entry in raw_data_entries:
            for address in db.query(Address).all():
                if address.notification_sent:
                    continue

                if address.radius is not None and isinstance(address.radius, (float, int)):
                    distance = geodesic(
                        (entry.latitude, entry.longitude),
                        (address.latitude, address.longitude)
                    ).miles
                    if address.alert and distance <= address.radius:
                        send_email_function(address.email, "GPS Proximity Alert", "Your message here")
                        address.notification_sent = True
                        address.notified_on = datetime.utcnow()
                        db.commit()
                        emails_sent_count += 1
                        emails_sent_to.append(address.email)
                else:
                    print(f"Invalid or missing radius for address with email {address.email}")

        summary_subject = "Task Execution Summary"
        summary_body = f"Total Emails Sent: {emails_sent_count}\nEmails Sent To: {', '.join(emails_sent_to)}"
        send_email_function('victor@swiftpigeon.io', summary_subject, summary_body)
    finally:
        db.close()

def send_email_function(recipient, subject, body):
    if recipient is None or subject is None or body is None:
        print("Error: Email recipient, subject, or body is None.")
        return

    message = MIMEMultipart()
    message['Subject'] = subject
    message['From'] = DEFAULT_FROM_EMAIL
    message['To'] = recipient
    message.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        if EMAIL_USE_TLS:
            server.starttls()
        server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
        server.sendmail(DEFAULT_FROM_EMAIL, recipient, message.as_string())
        server.quit()
    except Exception as e:
        print(f"Error sending email: {e}")

# Other configurations...
