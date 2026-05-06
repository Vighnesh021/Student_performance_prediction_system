from flask import Flask, render_template, request, redirect, send_file
import csv
import os
import pandas as pd

app = Flask(__name__)

FILE = "history.csv"

# Create file if not exists
if not os.path.exists(FILE):
    with open(FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Study", "Attendance", "Marks", "Assignments", "Internal", "Result"])


# LOGIN
@app.route("/", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        return redirect("/dashboard")
    return render_template("login.html")


# REGISTER
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        return redirect("/login")
    return render_template("register.html")


# LOGOUT
@app.route("/logout")
def logout():
    return redirect("/login")


# DASHBOARD
@app.route("/dashboard")
def dashboard():
    data = []
    passed = 0
    failed = 0

    with open(FILE) as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)
            if row["Result"] == "PASS":
                passed += 1
            else:
                failed += 1

    total = len(data)

    return render_template("dashboard.html", total=total, passed=passed, failed=failed)


# PREDICT
@app.route("/predict", methods=["GET", "POST"])
def predict():
    result = None

    if request.method == "POST":
        study = float(request.form["study"])
        attendance = float(request.form["attendance"])
        marks = float(request.form["marks"])
        assignments = float(request.form["assignments"])
        internal = float(request.form["internal"])

        avg = (marks + assignments + internal) / 3

        if avg >= 50 and attendance >= 50:
            result = "PASS"
        else:
            result = "FAIL"

        with open(FILE, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([study, attendance, marks, assignments, internal, result])

    return render_template("predict.html", result=result)


# HISTORY
@app.route("/history")
def history():
    data = []
    with open(FILE) as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)

    return render_template("history.html", data=data)


# DOWNLOAD EXCEL
@app.route("/download")
def download():
    df = pd.read_csv(FILE)
    df.to_excel("history.xlsx", index=False)
    return send_file("history.xlsx", as_attachment=True)


# CLEAR HISTORY
@app.route("/clear")
def clear():
    with open(FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Study", "Attendance", "Marks", "Assignments", "Internal", "Result"])
    return redirect("/history")


if __name__ == "__main__":
    app.run(debug=True)