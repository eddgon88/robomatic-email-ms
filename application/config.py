# config.py
import os
from dotenv import load_dotenv

load_dotenv()

CONFIGURATION_SETUP = os.getenv("CONFIGURATION_SETUP")
MAIL_USERNAME = os.getenv("MAIL_USERNAME")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
MAIL_FROM = os.getenv("MAIL_FROM")
MAIL_PORT = os.getenv("MAIL_PORT")
MAIL_SERVER = os.getenv("MAIL_SERVER")
MAIL_TEMPLATE_FOLDER_DIR = os.getenv("MAIL_TEMPLATE_FOLDER")


