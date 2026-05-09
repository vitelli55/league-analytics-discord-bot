import requests
import os
import json
from dotenv import load_dotenv
import time
from pathlib import Path

load_dotenv()
RIOT_API = os.getenv("RIOT_API")