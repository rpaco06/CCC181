"""VarsityQ: a queue management system for borrowing sports gear at MSU-IIT.
Run it with:
    flask --app app run --debug
then open http://127.0.0.1:5000
"""
import re

from flask import Flask, abort, flash, redirect, render_template, request, url_for

app = Flask(__name__)
app.secret_key = "dev-only-change-me"  # Week 11 moves this into an environment variable

# Gear categories and where each one is stored (FR-03: storage rack locations).
SERVICES = [
    {"id": 1, "name": "Basketball", "rack": "Rack A"},
    {"id": 2, "name": "Volleyball", "rack": "Rack B"},
    {"id": 3, "name": "Badminton", "rack": "Rack C"},
    {"id": 4, "name": "Table tennis", "rack": "Rack D"},
]

# What the student leaves with the gym staff (FR-01, FR-05).
COLLATERALS = ["Student ID Card", "Other ID", "Cash deposit"]

# Each ticket: number, name, student_id, service_id, collateral, pe_class, status
# status is one of: waiting, called, served, no-show
TICKETS = [
    {"number": 1, "name": "Ana Reyes", "student_id": "2024-0123", "service_id": 1,
     "collateral": "Student ID Card", "pe_class": True, "status": "waiting"},
    {"number": 2, "name": "Ben Cruz", "student_id": "2024-0456", "service_id": 2,
     "collateral": "Other ID", "pe_class": False, "status": "waiting"},
]


def get_service(service_id):
    """Return the gear category with this id, or None."""
    for service in SERVICES:
        if service["id"] == service_id:
            return service
    return None


def get_ticket(number):
    """Return the ticket with this number, or None."""
    for t in TICKETS:
        if t["number"] == number:
            return t
    return None


@app.route("/")
def index():
    return render_template("index.html")


# Student ID format: 4 digits, a hyphen, 4 digits (for example 2024-1423).
STUDENT_ID_PATTERN = re.compile(r"^\d{4}-\d{4}$")


@app.get("/join")
def join_form():
    return render_template("join.html", services=SERVICES, collaterals=COLLATERALS, form={})


@app.post("/join")
def join():
    form = request.form
    name = form.get("name", "").strip()
    student_id = form.get("student_id", "").strip()
    service_id = form.get("service_id", type=int)
    collateral = form.get("collateral", "")
    pe_class = form.get("pe_class") == "on"

    # Never trust form input: the server checks every field.
    errors = {}
    if not name:
        errors["name"] = "Enter your full name."
    if not STUDENT_ID_PATTERN.match(student_id):
        errors["student_id"] = "Enter your student ID as 4 digits, a hyphen, then 4 digits (for example 2024-1423)."
    if service_id not in [s["id"] for s in SERVICES]:
        errors["service_id"] = "Choose the gear you want to borrow."
    if collateral not in COLLATERALS:
        errors["collateral"] = "Choose the collateral you will leave."

    if errors:
        flash("Please fix the highlighted fields.", "danger")
        return render_template("join.html", services=SERVICES, collaterals=COLLATERALS,
                               form=form, errors=errors), 400

    number = max((t["number"] for t in TICKETS), default=0) + 1
    TICKETS.append({"number": number, "name": name, "student_id": student_id,
                    "service_id": service_id, "collateral": collateral,
                    "pe_class": pe_class, "status": "waiting"})
    flash(f"You joined the queue. Your ticket is #{number}.", "success")
    return redirect(url_for("ticket", ticket_id=number))


@app.route("/staff")
def staff_dashboard():
    return "Staff dashboard coming soon"


@app.route("/queue/<int:ticket_id>")
def ticket(ticket_id):
    # <int:ticket_id> only matches numbers, so /queue/abc returns 404.
    t = get_ticket(ticket_id)
    if t is None:
        abort(404)
    return render_template("ticket.html", ticket=t, service=get_service(t["service_id"]))


if __name__ == "__main__":
    # Lets you also start the app with: python app.py
    app.run(debug=True)