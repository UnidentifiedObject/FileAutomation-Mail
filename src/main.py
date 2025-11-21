import os
import shutil
import logging
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from dotenv import load_dotenv

#load credentials from .env
load_dotenv()
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

#Summary Dictionary
summary = {
    "processed_files": [],
    "errors": []
}

#Base Folders
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_DIR = os.path.join(BASE_DIR, "..", "TestFiles")
LOG_DIR = os.path.join(BASE_DIR, "..", "logs")

#Make sure the folders exist
os.makedirs(TEST_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

#Logging Setup
log_file_path = os.path.join(LOG_DIR, "automation.log")

#Timed rotating file handler (Daily, keep for a week)
handler = TimedRotatingFileHandler(
    log_file_path,
    when="midnight",          # Rotate at midnight
    interval= 1,               # Every 1 day
    backupCount = 7           # Keep last 7 logs
)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(handler)

logger.info("===SCRIPT STARTED===")

def process_files():
    logging.info("Starting file processing...")

    #List all files in the TestFiles directory
    for filename in os.listdir(TEST_DIR):
        file_path = os.path.join(TEST_DIR,filename)

        #Skip if it's a folder
        if os.path.isdir(file_path):
            continue

        try:
            #Process one file
            handle_single_file(file_path, filename)
        except Exception as e:
            logging.error(f"Error processing {filename}: {e}")


def get_today_folder():
    today = datetime.now().strftime("%Y-%m-%d")
    today_folder = os.path.join(TEST_DIR, today)
    os.makedirs(today_folder, exist_ok=True)
    return today_folder

def handle_single_file(file_path, filename):
    try:
        # Generate new filename with timestamp
        timestamp = datetime.now().strftime("%H%M%S")
        new_filename = f"{timestamp}_{filename}"

        today_folder = get_today_folder()
        new_path = os.path.join(today_folder, new_filename)

        # Move the file
        shutil.move(file_path, new_path)

        logging.info(f"Moved and renamed: {filename} -> {new_filename}")
        summary["processed_files"].append(new_filename)

    except Exception as e:
        logging.error(f"Error processing {filename}: {e}")
        summary["errors"].append(f"{filename}: {e}")

def send_summary_email(summary):
    try:
        #Email settings
        recipient = EMAIL_USER
        subject = f"Automation Summary for {datetime.now().strftime('%Y-%m-%d')}"
        body = f"Files Processed: {len(summary['processed_files'])}\n"
        if summary['processed_files']:
            body+= "processed files:\n" + "\n".join(summary['processed_files']) + "\n"
        if summary['errors']:
            body += "\n Errors: \n" + "\n".join(summary['errors'])

        #Create email message
        msg = MIMEMultipart()
        msg["FROM"] = EMAIL_USER
        msg["To"] = recipient
        msg["Subject"] = subject
        msg.attach(MIMEText(body,"plain"))

        #Attach log file
        log_file_path = os.path.join(LOG_DIR, "automation.log")
        with open(log_file_path, "rb") as f:
            part = MIMEApplication(f.read(), Name="automation.log")
            part['Content-Disposition'] = 'attachment; filename="automation.log"'
            msg.attach(part)

        #Connect to gmail SMTP server
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(EMAIL_USER, EMAIL_PASS)
            server.send_message(msg)

        logging.info("Summary email sent successfully!")

    except Exception as e:
        logging.error(f"Failed to send summary email: {e}")

if __name__ == "__main__":
    process_files()
    send_summary_email(summary)
    logging.info("===SCRIPT FINISHED===")