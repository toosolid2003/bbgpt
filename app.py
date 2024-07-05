from flask import Flask, render_template, redirect, url_for, request
import sqlite3

app = Flask(__name__, template_folder='templates/', static_folder='staticfiles/')

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect('emails.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS emails (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL UNIQUE
        )
    ''')
    conn.commit()
    conn.close()

# Route for the landing page
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle form submission
@app.route('/submit', methods=['POST'])
def submit_email():
    email = request.form['email']

    conn = sqlite3.connect('emails.db')
    c = conn.cursor()
    try:
        c.execute('INSERT INTO emails (email) VALUES (?)', (email,))
        conn.commit()
    except sqlite3.IntegrityError:
        # If the email is already in the database, you can handle it here
        print(f'Email {request.form['email']} already in the database')
    conn.close()
    
    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
