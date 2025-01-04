import os

from dotenv import load_dotenv

load_dotenv()

# API keys
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OUTSCRAPER_API_KEY = os.getenv('OUTSCRAPER_API_KEY') 
GOOGLE_MAP_API_KEY = os.getenv('GOOGLE_MAP_API_KEY')
PERPLEXITY_API_KEY = os.getenv('PERPLEXITY_API_KEY')