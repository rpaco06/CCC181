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


@app.get("/staff")
def staff_dashboard():
    service_id = request.args.get("service_id", type=int)
    queue = [t for t in TICKETS if t["status"] in ("waiting", "called")]
    if service_id:
        queue = [t for t in queue if t["service_id"] == service_id]
    queue.sort(key=lambda t: t["number"])  # order of arrival
    waiting = sum(1 for t in queue if t["status"] == "waiting")
    by_id = {s["id"]: s for s in SERVICES}
    return render_template("staff.html", queue=queue, services=SERVICES,
                           by_id=by_id, selected=service_id, waiting=waiting)


@app.post("/staff/call-next")
def staff_call_next():
    # Staff actions change data, so they use POST and never a plain link.
    service_id = request.form.get("service_id", type=int)
    waiting = [t for t in TICKETS
               if t["status"] == "waiting"
               and (not service_id or t["service_id"] == service_id)]
    if waiting:
        nxt = min(waiting, key=lambda t: t["number"])
        nxt["status"] = "called"
        flash(f"Ticket #{nxt['number']} ({nxt['name']}) called.", "info")
    else:
        flash("No one is waiting.", "warning")
    return redirect(url_for("staff_dashboard", service_id=service_id))


# action -> (status the ticket must have now, new status, words for the message)
STAFF_ACTIONS = {
    "serve": ("called", "served", "issued"),
    "no-show": ("called", "no-show", "no-show"),
}


@app.post("/staff/tickets/<int:ticket_id>/<action>")
def staff_action(ticket_id, action):
    t = get_ticket(ticket_id)
    rule = STAFF_ACTIONS.get(action)
    if t is None or rule is None:
        abort(404)
    required, new_status, words = rule
    if t["status"] != required:
        flash(f"Ticket #{ticket_id} must be called first.", "warning")
    else:
        t["status"] = new_status
        flash(f"Ticket #{ticket_id} marked {words}.", "info")
    return redirect(url_for("staff_dashboard", service_id=request.form.get("service_id", type=int)))


@app.get("/queue/<int:ticket_id>")
def ticket(ticket_id):
    # <int:ticket_id> only matches numbers, so /queue/abc returns 404.
    t = get_ticket(ticket_id)
    if t is None:
        abort(404)
    # Count only the people still waiting ahead of this ticket for the same gear.
    ahead = [x for x in TICKETS
             if x["service_id"] == t["service_id"]
             and x["status"] == "waiting"
             and x["number"] < t["number"]]
    return render_template("ticket.html", ticket=t, service=get_service(t["service_id"]),
                           ahead=len(ahead))


@app.get("/queue/<int:ticket_id>/status.json")
def ticket_status(ticket_id):
    t = get_ticket(ticket_id)
    if t is None:
        abort(404)
    ahead = sum(1 for x in TICKETS
                if x["service_id"] == t["service_id"]
                and x["status"] == "waiting" and x["number"] < t["number"])
    return {"status": t["status"], "ahead": ahead}


@app.post("/queue/<int:ticket_id>/leave")
def leave_queue(ticket_id):
    t = get_ticket(ticket_id)
    if t is None:
        abort(404)
    if t["status"] != "waiting":
        flash("This ticket can no longer be cancelled.", "warning")
        return redirect(url_for("ticket", ticket_id=ticket_id))
    t["status"] = "no-show"
    flash(f"You left the queue. Ticket #{ticket_id} was cancelled.", "info")
    return redirect(url_for("index"))

if __name__ == "__main__":
    # Lets you also start the app with: python app.py
    app.run(debug=True)