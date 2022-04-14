import requests
import json

from django.utils import timezone

URL = 'http://127.0.0.1:8000/post_from_dummy_client'

data = {
    'content': 'Posting to check JSON',
    'date_posted': timezone.now(),
    'author': 40
}

json_data = json.dumps(data, default=str)    # json to python type
r = requests.post(url=URL, data=json_data)
data = r.json()
print(data)