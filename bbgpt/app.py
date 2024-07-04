import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

app = Flask(__name__)
app.secret_key = 'bbgpt4me&u34455656!'

csrf = CSRFProtect(app)

class NameForm(FlaskForm):
    email = StringField('Enter your email', validators=[DataRequired(), Length(10,40)])
    submit = SubmitField('Submit')

@app.route('/', methods=['GET','POST'])
def index():
    form = NameForm()
    message = ''
    if form.validate_on_submit():
        email = form.email.data
        # A finir