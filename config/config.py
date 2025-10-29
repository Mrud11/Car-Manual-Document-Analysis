# config/config.py
import os
from dotenv import load_dotenv

load_dotenv()

def get_api_key():
    """
    Get Perplexity API key from environment variable PPLX_API_KEY
    """
    return os.getenv('PPLX_API_KEY', '')
