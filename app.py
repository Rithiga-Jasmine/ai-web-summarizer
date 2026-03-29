from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# 🔹 Get clean text from webpage
def get_webpage_text(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        # Remove unwanted tags
        for tag in soup(["script", "style", "nav", "header", "footer"]):
            tag.decompose()

        paragraphs = soup.find_all("p")

        text = ""
        for para in paragraphs:
            text += para.get_text() + " "

        return text

    except:
        return ""


# 🔹 Simple summary logic
def simple_summary(text):
    sentences = text.split(".")
    important = []

    for sentence in sentences:
        sentence = sentence.strip()

        if len(sentence) > 60:
            important.append(sentence)

    return important[:5]


# 🔹 HOME PAGE (input)
@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


# 🔹 SUMMARY PAGE (result)
@app.route("/summary", methods=["POST"])
def summary():
    url = request.form.get("url")

    if url:
        text = get_webpage_text(url)
        result = simple_summary(text)
    else:
        result = []

    return render_template("summary.html", summary=result)


# 🔹 RUN APP
if __name__ == "__main__":
    app.run(debug=True)