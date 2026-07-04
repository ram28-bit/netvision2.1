from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import os
app = Flask(__name__)
app.secret_key = "netvision123"


def get_db():
    return sqlite3.connect("users.db")


@app.route("/")
def home():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login():

    username = request.form["username"]
    password = request.form["password"]

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, password)
    )

    user = cursor.fetchone()

    conn.close()

    if user:
        session["user"] = username
        return redirect(url_for("dashboard"))

    return render_template("login.html", error="Invalid Username or Password")


@app.route("/dashboard")
def dashboard():

    if "user" not in session:
        return redirect(url_for("home"))

    alerts = []

    return render_template(
        "dashboard.html",
        google="UP",
        cloudflare="UP",
        alerts=alerts
    )


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)