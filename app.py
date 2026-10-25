"""VarsityQ: a queue management system for borrowing sports gear at the school gym.

Run it with:
    flask --app app run --debug
then open http://127.0.0.1:5000
"""
from flask import Flask, render_template, abort

app = Flask(__name__)

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
    return render_template("index.html", tickets=TICKETS, get_service=get_service)


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