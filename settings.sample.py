import os
from pathlib import Path

DATABASE = {
    'NAME': '',
    'USER': '',
    'PASSWORD': '',
    'HOST': 'localhost',
    'PORT': '5432',
}

CELERY_BROKER = ''

BASE_DIR = Path(__file__).resolve().parent
MEDIA_ROOT = os.path.join(BASE_DIR, "uploads")

MAGAZINE_URL = "https://techcrunch.com/wp-json/tc/v1/magazine?page{PAGE_NUMBER}&es=true&cachePrevention=0"
SEARCH_URL = "https://search.techcrunch.com/search;?p={KEYWORD}&fr2=sb-top&fr=techcrunch&b={PAGE_NUMBER}"

# Number to check duplicate posts. Exit after that
DUPLICATED_POST_NUMBER = 50

RANDOM_TILL_WAIT_TIME_BETWEEN_REQUESTS = 15
