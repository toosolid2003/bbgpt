from flask import Flask, render_template, redirect, url_for, request, flash
from flask_wtf.csrf import CSRFProtect
import sqlite3
from forms import EmailForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tX4y00j'
csrf = CSRFProtect(app)


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
@app.route('/', methods=['GET', 'POST'])
def index():
    form = EmailForm()

    if form.validate_on_submit():
        email = form.email.data
        conn = sqlite3.connect('emails.db')
        c = conn.cursor()
        try:
            c.execute('INSERT INTO emails (email) VALUES (?)', (email,))
            conn.commit()
            flash('Thanks, you have registered successfully! We\'ll be in touch!')
        except sqlite3.IntegrityError:
            # If the email is already in the database, you can handle it here
            flash('This email is already subscribed','danger')
        conn.close()
        return redirect(url_for('index'))

    return render_template('index.html', form=form)


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
