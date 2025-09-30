import os
import re
from collections import Counter
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from textblob import TextBlob
from PyPDF2 import PdfReader
from docx import Document
import google.generativeai as genai

# ---------- Configure Gemini API ----------
# Set your API key here (from Google Cloud Console)
GENAI_API_KEY = "YOUR_API_KEY"
genai.configure(api_key=GENAI_API_KEY)

# ---------- Extract text from files ----------
def extract_text(file_path):
    text = ""
    if file_path.endswith('.txt'):
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
    elif file_path.endswith(('.xlsx', '.xls')):
        df = pd.read_excel(file_path)
        text = " ".join(df.astype(str).stack())
    elif file_path.endswith('.pdf'):
        reader = PdfReader(file_path)
        text = " ".join([page.extract_text() or "" for page in reader.pages])
    elif file_path.endswith('.docx'):
        doc = Document(file_path)
        text = " ".join([para.text for para in doc.paragraphs])
    return text.strip()

# ---------- Gemini API call ----------
def analyze_with_gemini(text):
    try:
        # Gemini expects a dict prompt for structured output
        response = genai.chat.completions.create(
            model="gemini-2.0",
            messages=[
                {"role": "system", "content": "You are an assistant that analyzes feedback."},
                {"role": "user", "content": f"Analyze this feedback:\n{text}\n\n"
                                            "1. Sentiment (Positive/Negative/Neutral)\n"
                                            "2. Summary response\n"
                                            "3. Improvement suggestion"}
            ],
            temperature=0.2,
        )
        # The latest SDK stores text in response.choices[0].message.content
        content = response.choices[0].message.content
        return {
            "sentiment": None,  # optional parsing
            "response": content,
            "suggestion": None
        }
    except Exception as e:
        print(f"⚠️ Gemini API failed: {e}")
        return None

# ---------- Local sentiment ----------
def get_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity > 0.1:
        return "Positive"
    elif polarity < -0.1:
        return "Negative"
    else:
        return "Neutral"

# ---------- Common terms ----------
def get_common_terms(text, n=5):
    words = re.findall(r'\w+', text.lower())
    stopwords = {'the','is','and','to','i','it','a','but','was','for','on','with','there','are'}
    words = [w for w in words if w not in stopwords]
    most_common = [w for w,_ in Counter(words).most_common(n)]
    return ', '.join(most_common)

# ---------- Graph & WordCloud ----------
def generate_graph_and_wordcloud(text, prefix="feedback"):
    os.makedirs('static/images', exist_ok=True)

    plt.figure(figsize=(3,2))
    plt.bar(['Positive','Neutral','Negative'], [0.3,0.4,0.3],
            color=['#2ecc71','#f1c40f','#e74c3c'])
    plt.title("Feedback Sentiment")
    plt.tight_layout()
    graph_path = f'static/images/{prefix}_graph.png'
    plt.savefig(graph_path)
    plt.close()

    wc = WordCloud(width=300, height=150, background_color='white').generate(text)
    wc_path = f'static/images/{prefix}_wordcloud.png'
    wc.to_file(wc_path)

    return f'images/{prefix}_graph.png', f'images/{prefix}_wordcloud.png'

# ---------- Main processing ----------
def process_feedback(file_path):
    text = extract_text(file_path)

    gemini_result = analyze_with_gemini(text)
    if gemini_result:
        sentiment = gemini_result.get('sentiment', 'Neutral')
        response = gemini_result.get('response', 'Thank you for your feedback!')
        suggestion = gemini_result.get('suggestion', get_common_terms(text))
    else:
        sentiment = get_sentiment(text)
        response = "Thank you for your feedback!"
        suggestion = get_common_terms(text)

    feedback_lines = [line.strip() for line in text.splitlines() if line.strip()]
    feedback_html = "<ul>" + "".join(f"<li>{line}</li>" for line in feedback_lines) + "</ul>"

    df = pd.DataFrame({
        'Feedback': [feedback_html],
        'Sentiment': [sentiment],
        'Response': [response],
        'Suggestion': [suggestion]
    })

    graph_path, wc_path = generate_graph_and_wordcloud(text)

    return df, graph_path, wc_path
