import requests
import csv
import time

GITHUB_TOKEN = 'GITHUB_TOKEN'  
HEADERS = {'Authorization': f'token {GITHUB_TOKEN}'}

API_URL = 'https://api.github.com/search/repositories'

PARAMS = {
    'q': 'language:java',
    'sort': 'stars',
    'order': 'desc',
    'per_page': 100  
}

