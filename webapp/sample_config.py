import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = ""
API_KEY = ""

SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "..", "webapp.db")
SQLALCHEMY_TRACK_MODIFICATIONS = False

REMEMBER_COOKIE_DURATION = timedelta(days=5)

BP_ATTACHMENT_DIR = os.path.join(basedir, "..", "bp_files")
MAX_CONTENT_LENGTH = 16 * 1024 * 1024

SAMPLE_PASS = "12345"