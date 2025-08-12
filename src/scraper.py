import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv
import time
import random

url = 'https://stackoverflow.com/questions?tab=Newest&pagesize=50'
headers = {"User-Agent": "Mozilla/5.0"}

rows = []
seen = set()

max_pages = 5
page = 0

while url and page < max_pages:
    page += 1
    print(f"[page {page}] GET {url}", flush=True)
    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, 'html.parser')
    questions = soup.find_all('div', class_='s-post-summary')

    if not questions:
        print("no question content found")
        break

    added_this_page = 0
    for q in questions:
        tittle_tag = q.find('a', class_='s-link')
        if not tittle_tag:
            continue

        tittle = tittle_tag.get_text(strip=True)
        link = urljoin('https://stackoverflow.com', tittle_tag.get('href', ''))

        if link in seen:
            continue
        seen.add(link)

        stats = q.select('s-post-summary--stats-item-number')

        def to_int(s):
            s = (s or '').strip()
            return int(s) if s.isdigit() else None

        votes = to_int(stats[0].get_text()) if len(stats) > 0 else None
        answers = to_int(stats[1].get_text()) if len(stats) > 1 else None
        tags = [t.get_text(strip=True) for t in q.select('.post-tag')]

        rows.append({
            'title': tittle,
            'link': link,
            'votes': votes,
            'answers': answers,
            'tags': ','.join(tags)
        })
        added_this_page += 1

    print(f"[page {page}] +{added_this_page} novas (total: {len(rows)})", flush=True)

    next_a = soup.select_one("a[rel='next']")
    url = urljoin('https://stackoverflow.com', next_a['href']) if next_a else None

    time.sleep(random.uniform(1.0, 2.0))

with open('so_questions.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['title', 'link', 'votes', 'answers', 'tags'])
    writer.writeheader()
    writer.writerows(rows)

print(f"questions {len(rows)} collected. saved file: so_questions.csv")
