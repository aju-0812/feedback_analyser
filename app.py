from flask import Flask, render_template, request, redirect, url_for, session
from feedback_processor import process_feedback
import os
import sqlite3
import pandas as pd

# ------------------- Flask Config -------------------
app = Flask(__name__)
app.secret_key = "your_secret_key"
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

DB_NAME = "feedback.db"


# ------------------- Database Helper -------------------
def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


# ------------------- Home -------------------
@app.route('/')
def home():
    return redirect(url_for('login'))


# ------------------- Signup -------------------
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        fullname = request.form['fullname']
        email = request.form['email']
        business = request.form.get('business', '')
        industry = request.form.get('industry', '')
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            return "❌ Passwords do not match!"

        conn = get_db_connection()
        existing = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        if existing:
            conn.close()
            return "❌ User already exists!"

        conn.execute(
            "INSERT INTO users (fullname, email, business, industry, password) VALUES (?, ?, ?, ?, ?)",
            (fullname, email, business, industry, password)
        )
        conn.commit()
        conn.close()

        print(f"✅ New signup: {fullname} ({email}) | {business} - {industry}")
        return redirect(url_for('login'))

    return render_template('signup.html')


# ------------------- Login -------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['username']  # form field
        password = request.form['password']

        conn = get_db_connection()
        user = conn.execute(
            "SELECT * FROM users WHERE email = ? AND password = ?",
            (email, password)
        ).fetchone()
        conn.close()

        if user:
            session['user_id'] = user['id']
            session['fullname'] = user['fullname']
            session['email'] = user['email']
            session['business'] = user['business']
            session['industry'] = user['industry']
            return redirect(url_for('upload_file'))
        else:
            return "❌ Invalid credentials!"
    return render_template('login.html')


# ------------------- Upload & Process Feedback -------------------
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        uploaded_files = []

        # Handle multiple categories
        for field in ['image_files', 'pdf_files', 'docx_files', 'excel_files', 'txt_files']:
            if field in request.files:
                files = request.files.getlist(field)
                for f in files:
                    if f.filename != '':
                        file_path = os.path.join(UPLOAD_FOLDER, f.filename)
                        f.save(file_path)
                        uploaded_files.append(file_path)

        # Now process each uploaded file
        all_tables, graphs, wordclouds = [], [], []

        for file_path in uploaded_files:
            try:
                feedback_table, graph, wordcloud_img = process_feedback(file_path)
                all_tables.append(feedback_table)
                graphs.append(graph)
                wordclouds.append(wordcloud_img)
            except Exception as e:
                print(f"⚠️ Error processing {file_path}: {e}")

        # Combine all feedback tables into one big table
        if all_tables:
            combined_table = pd.concat(all_tables, ignore_index=True)
        else:
            combined_table = pd.DataFrame(
                columns=['Feedback', 'Sentiment', 'Response', 'Suggestion']
            )

        return render_template(
            'results.html',
            table=combined_table.to_html(classes='table table-striped', escape=False),
            graphs=graphs,
            wordclouds=wordclouds,
            fullname=session['fullname'],
            business=session['business'],
            industry=session['industry']
        )

    return render_template('upload.html')


# ------------------- Logout -------------------
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


# ------------------- Main -------------------
if __name__ == '__main__':
    app.run(debug=True)
