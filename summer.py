import requests
from bs4 import BeautifulSoup
import sys

def get_webpage_text(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers, verify=False)

    soup = BeautifulSoup(response.text, 'html.parser')

    # ❌ remove scripts & styles
    for script in soup(["script", "style", "nav", "header", "footer"]):
        script.decompose()

    # ✅ try to get only paragraphs
    paragraphs = soup.find_all("p")

    text = ""
    for para in paragraphs:
        text += para.get_text() + " "

    return text


def simple_summary(text):
    sentences = text.split(".")
    important = []

    for sentence in sentences:
        sentence = sentence.strip()

        # ❌ skip useless lines
        if len(sentence) < 60:
            continue
        if any(word in sentence.lower() for word in ["click", "sign up", "login", "subscribe", "advertisement"]):
            continue

        important.append(sentence)

    return important[:5]


# 👇 CLI INPUT
if len(sys.argv) < 2:
    print("Usage: python summer.py <URL>")
    exit()

url = sys.argv[1]

print("🔍 Fetching content...")
text = get_webpage_text(url)

print("🧠 Summarizing...")
summary = simple_summary(text)

print("\n✨ SUMMARY:\n")
for i, line in enumerate(summary, 1):
    print(f"{i}. {line}")