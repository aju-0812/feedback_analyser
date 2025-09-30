# feedback_analyzer_with_responses.py

import pandas as pd
from textblob import TextBlob
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords
import nltk

# Download stopwords once
nltk.download('stopwords')

# ------------------------
# 1. Load Data
# ------------------------
df = pd.read_csv("feedback.csv")

# ------------------------
# 2. Sentiment Analysis
# ------------------------
def get_sentiment(text):
    analysis = TextBlob(str(text))
    if analysis.sentiment.polarity > 0:
        return "Positive"
    elif analysis.sentiment.polarity < 0:
        return "Negative"
    else:
        return "Neutral"

df["Sentiment"] = df["feedback"].apply(get_sentiment)

# ------------------------
# 3. Auto Response Generator
# ------------------------
def generate_response(sentiment):
    if sentiment == "Positive":
        return "Thank you for your valuable feedback! We're glad you enjoyed the experience."
    elif sentiment == "Negative":
        return "We’re sorry for the inconvenience. Your feedback helps us improve, and we’ll address this issue immediately."
    else:
        return "Thank you for your feedback. We’ll take it into consideration."

df["Auto_Response"] = df["Sentiment"].apply(generate_response)

# ------------------------
# 4. Keyword Extraction
# ------------------------
vectorizer = CountVectorizer(stop_words=stopwords.words('english'))
X = vectorizer.fit_transform(df["feedback"])
keywords = vectorizer.get_feature_names_out()

# ------------------------
# 5. Insights
# ------------------------
print("=== Feedback Analysis with Responses ===")
print(df)

print("\nMost common words in feedback:")
word_counts = X.toarray().sum(axis=0)
common_words = sorted(list(zip(keywords, word_counts)), key=lambda x: x[1], reverse=True)[:10]
for word, count in common_words:
    print(f"{word}: {count}")

# ------------------------
# 6. Save Results
# ------------------------
df.to_csv("feedback_analysis_with_responses.csv", index=False)
print("\nResults saved to feedback_analysis_with_responses.csv")
