from flask import Flask, render_template, flash, request, url_for, redirect
from content_management import Content

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
        if request.method == "POST":
            attempted_username = request.form['username']
            attempted_password = request.form['password']

            if attempted_username == "admin" and attempted_password == "password":
                return redirect(url_for('dashboard'))
                # this searches for a method 'dashboard' and returns the associated url.
            else:
                error = "Invalid credentials. Try Again."
        # the below statement will only be reached if the first if fails.
        # if the method is post, it will redirect to dashboard, wont reach here.
        return render_template("login.html", error = error)

    except Exception as e:
        return render_template("login.html", error = error)

if __name__ == "__main__":
    app.run()
