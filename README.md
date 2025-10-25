# AI Personal Finance Advisor — Quickstart

Minimal instructions to run the project locally.

Prerequisites
- Python 3.9+ installed

Quickstart (PowerShell)
1) Create & activate a venv:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2) Install dependencies:

```powershell
pip install -r requirements.txt
```

3) Run the app (binds to 127.0.0.1:5500):

```powershell
python app.py
```

4) Open http://127.0.0.1:5500 in your browser.

API (brief)
- POST JSON to `/api/advice` with keys `monthly_income`, `expenses` (array of {desc,amount}), optional `debt`, `savings_goal`, and `risk_profile`.
- Response contains: `categorized`, `recommendation`, `debt`, `investment`, `summary`.

Run tests

```powershell
python -m pytest -q
```

Troubleshooting
- If you see a directory listing in the browser, stop any static server (e.g., Live Server) using port 5500 before starting Flask.
- If Chart.js doesn’t load, the UI will fall back to a simple DOM-based visualization.

Files of interest
- `app.py` — Flask app and API
- `advisor.py` — core logic
- `templates/index.html`, `static/app.js`, `static/styles.css` — frontend

in your browser and use the form.  ## API usage  POST `/api/advice` with JSON body: ```json {   "monthly_income": 4000,   "expenses": [     {"desc":"rent", "amount":1200},     {"desc":"groceries", "amount":300},     {"desc":"netflix", "amount":12}   ],   "debt": {"total":5000, "monthly_payment":150, "interest_rate":10.5},   "savings_goal": {"amount":10000, "months":12},   "risk_profile": "moderate"  // options: conservative, moderate, aggressive } ```  The API returns JSON with budget recommendations, debt advice, and suggested allocations.  ## Files - `app.py` - Flask web app and API endpoints - `advisor.py` - Core finance logic - `templates/` - UI templates - `static/` - static assets (placeholder CSS) - `report.py` - creates a pie chart of expenses - `requirements.txt` - Python dependencies - `tests/` - pytest tests for core logic  Enjoy! 
