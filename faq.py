import requests
from bs4 import BeautifulSoup

url = "https://nalsa.gov.in/faqs/"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Find all questions and answers
questions = soup.find_all('h3')
answers = soup.find_all('p')

# Save each Q&A to a separate text file
for i, (q, a) in enumerate(zip(questions, answers)):
    filename = f"data/raw/legal-faqs/faq_{i+1}.txt"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"Q: {q.get_text()}\n")
        f.write(f"A: {a.get_text()}")
