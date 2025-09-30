# Feedback Analyser

A Python-based web application that analyzes textual feedback from multiple sources (PDFs, Word documents, and text) to generate insightful reports, visualizations, and sentiment analysis. The application leverages natural language processing and visualization tools to help organizations understand user feedback effectively.

---

## Features

- **Multi-format Input**: Supports `.txt`, `.pdf`, and `.docx` files.
- **Text Preprocessing**: Cleans and preprocesses text data for analysis.
- **Sentiment Analysis**: Determines the polarity (positive, neutral, negative) of feedback using TextBlob.
- **Word Cloud Visualization**: Generates word clouds to highlight frequent words.
- **Frequency Analysis**: Shows the most common words in the feedback.
- **Graphical Reports**: Generates bar charts and pie charts for quick insights.
- **AI-powered Summarization**: Optionally uses Google Gemini API for enhanced analysis and summarization.

---

## Technologies Used

- Python 3.x
- Flask (Web Framework)
- Pandas (Data Handling)
- Matplotlib & WordCloud (Visualization)
- TextBlob (Sentiment Analysis)
- PyPDF2 (PDF Processing)
- python-docx (Word Document Processing)
- Google Generative AI (Optional)

---

## Installation

1. **Clone the repository**  
```bash
git clone https://github.com/aju-0812/feedback_analyser.git
cd feedback_analyser
