import requests
import time
import sys
import random

# URL SERVIDOR FLASK
base_url = 'http://localhost:5000'  

id = 2
response = requests.delete(f'{base_url}/dados/{id}',)
