# application/__init__.py
from fastapi import FastAPI
from .routers import apirouter
from . import config

app_configs = {"title": "email-api",
               "CONFIGURATION_SETUP": config.CONFIGURATION_SETUP,
               "MAIL_USERNAME": config.MAIL_USERNAME,
               "MAIL_PASSWORD": config.MAIL_PASSWORD,
               "MAIL_FROM": config.MAIL_FROM,
               "MAIL_PORT": config.MAIL_PORT,
               "MAIL_SERVER": config.MAIL_SERVER,
               "MAIL_TEMPLATE_FOLDER_DIR": config.MAIL_TEMPLATE_FOLDER_DIR,
               "FILE_MANAGER_API_URL": config.FILE_MANAGER_API_URL,
               "EVIDENCE_FILE_DIR": config.EVIDENCE_FILE_DIR,
               "FILE_MANAGER_CONVERT_ENDPOINT": config.FILE_MANAGER_CONVERT_ENDPOINT}

def create_app():
    app = FastAPI(**app_configs)
    app.include_router(apirouter.router)
    return app
