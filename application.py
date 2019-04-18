import os
import requests

from flask import Flask, session, jsonify, render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helper import login_required, apology

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

@app.route("/")
@login_required
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return "must provide username"

        # Ensure password was submitted
        elif not request.form.get("password"):
            return "must provide username"

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return "Invalid username or password"

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # get username & password from form (POST)
    if request.method == "POST":

        # Check for username
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Check if valid username via DB
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username doesn't exists
        if len(rows) > 0:
            return apology("Sorry, that username is taken already", 403)

        #Check for password correctness
        if not request.form.get("password"):
            return apology("must provide password", 403)

        if not request.form.get("confirmation"):
            return apology("Please confirm your password", 403)

        if not request.form.get("password") == request.form.get("confirmation"):
            return apology("passwords don't match", 403)

        # insert username and password into DB
        username = request.form.get("username")
        hash = generate_password_hash(request.form.get("password"))
        new_user = db.execute("INSERT INTO users (username, hash) VALUES(:username, :hash)",
            username=username, hash = hash)

        # redirect to login page
        return redirect("/")

    else:
        return render_template("register.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")
