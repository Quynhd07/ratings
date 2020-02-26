"""Movie Ratings."""
from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session

from flask_debugtoolbar import DebugToolbarExtension

from model import User, Rating, Movie, connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""
    return render_template('homepage.html')


@app.route("/register")
def register_form():
    return render_template("registration.html")


@app.route("/register", methods=["POST"])
def register_process():
    user_email = request.form.get("email")
    password = request.form.get("password")
    email = User.query.filter_by(email=user_email).first()

    if not email:
        new_user = User(email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/')
    else:
        return redirect('/login')


@app.route("/login")
def user_login():
    return flash('logging in')


@app.route('/users')
def get_users():
    users = User.query.all()

    return render_template('user_list.html', users=users)


@app.route("/movies")
def get_movies():
    return


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
