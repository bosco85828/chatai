import requests
import os
from dotenv import load_dotenv
import os 
load_dotenv()
OPENAI_API_KEY=os.getenv('OPENAI_API_KEY')

headers = {
    'Authorization': 'Bearer {}'.format(OPENAI_API_KEY),
}

response = requests.get('https://api.openai.com/v1/usage/transactions', headers=headers)

if response.status_code == 200:
    usage_data = response.json()
    for transaction in usage_data['data']:
        print('Date:', transaction['usage']['start'])
        print('Tokens used:', transaction['usage']['total_tokens'])
        print('---------')
else:
    print('Error:', response.status_code, response.text)
