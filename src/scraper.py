import requests
from bs4 import BeautifulSoup

url = 'https://stackoverflow.com/questions'
headers = {"User-Agent": "Mozilla/5.0"}

response = requests.get(url, headers=headers)
response.raise_for_status()

soup = BeautifulSoup(response.content, 'html.parser')

questions = soup.find_all('div', class_='s-post-summary')

if questions:
    for q in questions:
        tittle_tag = q.find('a', class_='s-link')
        if tittle_tag:
            print(tittle_tag.get_text(strip=True))
else:        
   print("no question content found")
