import os
from pathlib import Path
from dotenv import load_dotenv

dotenv_path = Path(__file__).resolve().parent.parent / '.env'

# Load the .env file
load_dotenv(dotenv_path=dotenv_path)

API_KEY = os.getenv('API_KEY')

URL = "https://api.siliconflow.cn/v1"