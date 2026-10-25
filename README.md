# VarsityQ

VarsityQ is a queue management system for borrowing sports gear at Mindanao State University - Iligan Institute of Technology. Students join a queue for a gear category (such as basketball or badminton), leave a collateral, and see their place in line from their phone, while gym staff call the next borrower, mark gear as issued, or record no-shows. To run it: create a virtual environment with `py -m venv .venv`, activate it with `.venv\Scripts\activate`, install the packages with `pip install -r requirements.txt`, then start it with `flask --app app run --debug` and open http://127.0.0.1:5000.

## Project structure

```
```
CCC181/
├── app.py              # routes, validation and the in-memory gear and ticket data
├── requirements.txt    # packages to rebuild the environment
├── .gitignore          # keeps .venv, caches and secrets out of Git
├── .venv/              # your virtual environment (not committed)
├── templates/          # Jinja2 HTML files for render_template()
│   ├── base.html       # shared layout: navbar, flash messages, footer
│   ├── index.html      # home page
│   ├── join.html       # borrow-gear form
│   ├── ticket.html     # My place page for /queue/<ticket_id>
│   └── staff.html      # staff dashboard
└── static/             # served at /static/...
    ├── css/style.css
    └── js/main.js
```

## Routes

| URL | Method | View function | What it does |
|---|---|---|---|
| `/` | GET | `index()` | Home page with the "Join the queue" button |
| `/join` | GET | `join_form()` | Shows the empty borrow-gear form |
| `/join` | POST | `join()` | Checks every field on the server, then creates a ticket |
| `/queue/<int:ticket_id>` | GET | `ticket()` | My place: ticket number, status and people ahead |
| `/queue/<int:ticket_id>/leave` | POST | `leave_queue()` | A waiting borrower leaves the queue |
| `/staff` | GET | `staff_dashboard()` | Staff queue, with a gear category filter |
| `/staff/call-next` | POST | `staff_call_next()` | Calls the next waiting borrower |
| `/staff/tickets/<int:ticket_id>/<action>` | POST | `staff_action()` | Marks a called ticket as issued (`serve`) or `no-show` |

Everything that changes data is a POST, so a refresh or a link preview can't serve someone by accident. A ticket number that doesn't exist, such as `/queue/99` or `/queue/abc`, returns 404.

## 1. Set up the Python environment

```bash
# create (once per project)
python -m venv .venv

# activate (every new terminal)
.venv\Scripts\activate          # Windows
source .venv/bin/activate       # macOS/Linux

# install the packages
pip install -r requirements.txt
```

Your prompt shows `(.venv)` when the environment is active. Some systems use `python3` or `py` instead of `python`.
If PowerShell blocks the activate script, run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` once, or use Command Prompt.

If you add more packages later, record them with:

```bash
pip freeze > requirements.txt
```

## 2. Run the app

```bash
flask --app app run --debug
```

Open http://127.0.0.1:5000. With `--debug`, the server reloads every time you save a file. Never use debug mode in production.

## 3. Put it on GitHub

### Once per computer

```bash
git config --global user.name "Your Name"
git config --global user.email you@g.msuiit.edu.ph   # same email as your GitHub account
git config --list
```

### Create the local repository and first commit

```bash
git init
git branch -M main
git status              # .venv should NOT appear, thanks to .gitignore
git add .
git commit -m "Add Flask starter app"
```

### Connect to GitHub and push

1. On GitHub, create a new **empty** repository (no README, no .gitignore).
2. Copy its URL, then:

```bash
git remote add origin <repo-url>
git push -u origin main
```

GitHub does not accept your account password for Git over HTTPS. Sign in through Git Credential Manager or the GitHub CLI, or use a personal access token or SSH key.

### Everyday loop

```bash
git pull origin main     # before you start working
git status
git add <file>
git commit -m "Add join-queue form"
git push origin main     # when you have commits to share
```

## 4. Lab: ship it through a pull request

1. On GitHub, open an issue: **"Set up Flask starter app"**.
2. Pull the latest `main`, then create a branch:
   ```bash
   git switch main
   git pull origin main
   git switch -c feature/flask-setup
   ```
3. Create `.venv`, install Flask, write `requirements.txt` and `.gitignore`.
4. Build `app.py` with a home route and one dynamic route, rendered with `base.html` and `index.html`.
5. Commit in small steps, then push the branch:
   ```bash
   git push -u origin feature/flask-setup
   ```
6. On GitHub, click **Compare & pull request** and write `Closes #N` in the description (N is your issue number). Merge it, then:
   ```bash
   git switch main
   git pull origin main
   ```

**Early finishers:** add another static CSS rule linked with `url_for`, or a third route based on one Must feature from your project milestone.

## Commit message tips

- Short summary in the imperative: "Add...", "Fix..."
- One logical change per commit
- Commit early and often
- Good: "Add join-queue form". Unhelpful: "update", "asdf", "final na talaga".


   ## Note

   The staff dashboard (`/staff`) is open to anyone for now. Staff login comes in a later week.