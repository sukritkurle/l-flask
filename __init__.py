from flask import Flask, render_template, flash, request, url_for, redirect, session
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from content_management import Content
from dbconnect import connection
from passlib.hash import sha256_crypt
from pymysql import escape_string as thwart
import gc

TOPIC_DICT = Content()
app = Flask(__name__)
app.secret_key = 'kjafslkfjhlmfhd'


@app.route('/')
def homepage():
    return render_template('main.html')


@app.route('/dashboard/')
def dashboard():
    flash("Welcome to my website!")
    return render_template('dashboard.html', TOPIC_DICT=TOPIC_DICT)


@app.errorhandler(404) # Flask built-in error handler.
def page_not_found(e):
    return render_template("404.html")


@app.route('/slashboard/')
def slashboard():
    try:
        return render_template("dashboard.html", TOPIC_DICT = shamwow)
    except Exception as e:
	    return render_template("500.html", error = str(e))


@app.route('/login/', methods=["GET","POST"])
def login_page():
    error = ''
    try:
        c, conn = connection()
        if request.method == "POST":
            data = c.execute("SELECT * FROM users WHERE username = (%s)",
                             thwart(request.form['username']))
            data = c.fetchone()[2] # hashed password from the database.
            # if user does not exist, data is an empty set, which raises an Exception.

            # verify user entered password against encrypted PW from DB.
            if sha256_crypt.verify(request.form['password'], data):
                session['logged_in'] = True
                session['username'] = request.form['username']

                flash("You are now logged in")
                return redirect(url_for("dashboard"))
                # this searches for a method 'dashboard' and returns the associated url.
            else:
                error = "Invalid credentials, try again."
        gc.collect()
        # the below statement will only be reached if the first if fails.
        # if the method is post, it will redirect to dashboard, wont reach here.
        return render_template("login.html", error=error)

    except Exception as e:
        error = "Invalid credentials, try again."
        return render_template("login.html", error = error)


class RegistrationForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=20)])
    email = StringField('<br />Email Address', [validators.Length(min=6, max=50),
        validators.Email()])
    password = PasswordField('<br />New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('<br />Repeat Password')
    accept_tos = BooleanField('<br />I accept the <a href="/tos/"> Terms of Service.</a>',
        [validators.DataRequired()])


@app.route('/register/', methods=["GET","POST"])
def register_page():
    try:
        form = RegistrationForm(request.form)

        if request.method == "POST" and form.validate():
            username  = form.username.data
            email = form.email.data
            password = sha256_crypt.encrypt(str(form.password.data))
            c, conn = connection()

            x = c.execute("SELECT * FROM users WHERE username = (%s)",
                          (thwart(username)))

            if int(x) > 0:
                flash("That username is already taken, please choose another")
                return render_template('register.html', form=form)
            else:
                c.execute("INSERT INTO users (username, password, email, tracking) VALUES (%s, %s, %s, %s)",
                          (thwart(username), thwart(password), thwart(email), thwart("/introduction-to-python-programming/")))

                conn.commit()
                flash("Thanks for registering!")
                c.close()
                conn.close()
                gc.collect()

                session['logged_in'] = True
                session['username'] = username

                return redirect(url_for('dashboard'))

        return render_template("register.html", form=form)

    except Exception as e:
        return(str(e))


if __name__ == "__main__":
    app.run()
