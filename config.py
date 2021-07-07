from dotenv import load_dotenv

import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASE_DIR, 'config.env'))

TOKEN = os.environ.get('TOKEN')
