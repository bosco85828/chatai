from dotenv import load_dotenv
import os 
from test2 import test345

load_dotenv()
a=os.getenv('OPENAI_API_KEY')
print(a)
os.environ['OPENAI_API_KEY']= '123'
b=os.getenv('OPENAI_API_KEY')
print(b)

test345()