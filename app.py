import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from dotenv import load_dotenv

# Load environment variables from .env (useful locally)
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev")  # Set to a secure key in production

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        session["user"] = request.form["username"]
        flash("Registered successfully!", "success")
        return redirect(url_for("home"))
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form["username"] == session.get("user"):
            flash("Logged in successfully!", "success")
            return redirect(url_for("home"))
        else:
            flash("Invalid credentials!", "danger")
    return render_template("login.html")

@app.route("/create_event", methods=["GET", "POST"])
def create_event():
    if request.method == "POST":
        title = request.form["event_name"]    # <-- matches form field test
        date = request.form["event_date"]     # <-- matches form field
        desc = request.form.get("event_description", "")
        flash(f"Event '{title}' created for {date}! Description: {desc}", "info")
        return redirect(url_for("home"))
    return render_template("create_event.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("Logged out.", "info")
    return redirect(url_for("login"))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
