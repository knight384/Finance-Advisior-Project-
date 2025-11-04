1) Project Report — Finance Advisor

Project Title: AI Personal Finance Advisor — Budgeting & Investment Recommendations

Submitted by:
Name: Anish Choudhary
Internship Role: Virtual Intern
Organization: Hack Culprit
GitHub Profile: @knight384 (replace if you want a different display)
Project Duration: [Start Date] – [End Date]
Project Repository: (your repo)

1. Executive Summary

This project implements an AI-backed personal finance advisor that accepts user finances (income, expenses, debts, savings goals, risk profile) and returns actionable budget, debt repayment, and investment recommendations. The system is implemented as a Flask web app with a simple frontend, programmatic API, plotting/reporting utilities, and unit tests — making it ideal for demonstration and further extension into production. 
GitHub

2. Problem Statement

Many users struggle to translate monthly income and expenses into a sound budget and realistic savings/investment plan. The project provides an automated advisor that categorizes expenses, suggests allocations (essentials, savings, discretionary), recommends debt repayment strategies, and proposes investment mixes aligned with a user’s risk profile.

3. Project Objectives

Implement a reproducible API and frontend to collect basic financial information.

Provide clear budget breakdowns, debt advice and investment suggestions.

Visualize spending using simple charts and exportable reports.

Ship unit tests for core logic and create clear documentation for users/developers.

4. Development Approach

Requirement & Design — defined input JSON schema and expected outputs (budget, recommendation, summary).

Implementation — built core logic in advisor.py, Flask endpoints in app.py, report generation in report.py, and the UI in templates/ & static/. 
GitHub

Testing — added pytest tests for core finance logic. 
GitHub

Documentation — prepared README.md, local_README.md and remote_README.md for quickstarts and troubleshooting. 
GitHub

5. Tools & Technologies

Language: Python 3.9+

Framework: Flask (web API + simple UI)

Visualization: Chart.js + Python plotting for reports

Testing: pytest

Other: Git / GitHub, sample CSV data for demonstration. 
GitHub

6. Installation & Setup

(Sample steps; paste exact commands in final submission)

# Create & activate virtual environment
python -m venv .venv
# Windows PowerShell
.\.venv\Scripts\Activate.ps1

# Install requirements
pip install -r requirements.txt

# Run the web app (binds to 127.0.0.1:5500 by default)
python app.py


Open the local server in a browser to use the UI or POST to /api/advice. 
GitHub

7. Key Features

REST API: POST /api/advice accepts monthly income, expenses (list), debt, savings goal and risk profile; returns categorized expenses and recommendations. 
GitHub

Frontend: Form-based UI that visualizes budget and recommendations. 
GitHub

Report generation: simple pie charts for expense breakdown (report.py). 
GitHub

Tests: pytest tests for core advisor logic. 
GitHub

8. Demonstration

Include screenshots showing:

The web form and results page.

The /api/advice sample request + JSON response.

The pie-chart report output created by report.py.

(Use sample_expenses.csv for demo inputs.) 
GitHub

9. Challenges Encountered

Designing rules that generalize across different user profiles while remaining interpretable.

Balancing simple heuristics vs. more advanced ML-based recommendations (kept the first iteration deterministic).

Making the UI lightweight and resilient if Chart.js fails (fallback to DOM visualizations).

10. Future Enhancements

Add user authentication and per-user persistent storage.

Expand to dynamic investment suggestions using market-data connectors (careful with credentials & rate limits).

Add CI/CD and Dockerfile for easy deployment.

Improve the advisor by adding a data-driven model (trained recommendations) and more robust uncertainty estimates.

11. Conclusion

The Finance Advisor project produced a working, test-covered prototype that demonstrates core budgeting and personal finance advisory features. It is documented and packaged for local run and further extension.

12. Acknowledgements

Thanks to Hack Culprit mentors and open-source libraries for making this project possible.

13. License

MIT License.
