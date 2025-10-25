from flask import Flask, render_template, request, jsonify
import os, json
from advisor import categorize_expenses, recommend_budget, debt_advice, investment_suggestion, summarize

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def index():
    result = None
    error = None
    if request.method == 'POST':
        try:
            monthly_income = float(request.form.get('monthly_income',0) or 0)
            if monthly_income < 0:
                raise ValueError("Monthly income cannot be negative")
            
            # parse expenses from a textarea where each line is "desc,amount"
            raw = request.form.get('expenses','').strip()
            expenses = []
            for line in raw.splitlines():
                if not line.strip():
                    continue
                parts = line.split(',')
                if len(parts) < 2:
                    continue  # Skip malformed lines
                desc = parts[0].strip()
                try:
                    amt = float(parts[1].strip())
                    if amt < 0:
                        continue  # Skip negative amounts
                except ValueError:
                    continue  # Skip lines with invalid amounts
                expenses.append({'desc':desc,'amount':amt})
            debt = None
            if request.form.get('debt_total'):
                try:
                    debt_total = float(request.form.get('debt_total') or 0)
                    debt_monthly = float(request.form.get('debt_monthly') or 0)
                    debt_rate = float(request.form.get('debt_rate') or 0)
                    if debt_total < 0 or debt_monthly < 0 or debt_rate < 0:
                        raise ValueError("Debt values cannot be negative")
                    debt = {'total': debt_total, 'monthly_payment': debt_monthly, 'interest_rate': debt_rate}
                except ValueError as ve:
                    raise ValueError(f"Invalid debt input: {ve}")
            
            savings_goal = None
            if request.form.get('goal_amount'):
                try:
                    goal_amount = float(request.form.get('goal_amount') or 0)
                    goal_months = int(request.form.get('goal_months') or 0)
                    if goal_amount < 0 or goal_months <= 0:
                        raise ValueError("Savings goal amount cannot be negative and months must be positive")
                    savings_goal = {'amount': goal_amount, 'months': goal_months}
                except ValueError as ve:
                    raise ValueError(f"Invalid savings goal input: {ve}")
            risk = request.form.get('risk_profile','moderate')
            categorized = categorize_expenses(expenses)
            rec = recommend_budget(monthly_income, categorized, savings_goal=savings_goal)
            debt_info = debt_advice(debt) if debt else {'status':'no_debt'}
            monthly_savings = rec['baseline']['Savings']
            invest = investment_suggestion(risk, monthly_savings)
            summ = summarize(expenses)
            result = {
                'categorized': categorized,
                'recommendation': rec,
                'debt': debt_info,
                'investment': invest,
                'summary': summ
            }
        except Exception as e:
            error = str(e)
    return render_template('index.html', result=result, error=error)

@app.route('/api/advice', methods=['POST'])
def api_advice():
    payload = request.get_json() or {}
    monthly_income = payload.get('monthly_income',0)
    expenses = payload.get('expenses',[])
    debt = payload.get('debt')
    savings_goal = payload.get('savings_goal')
    risk = payload.get('risk_profile','moderate')
    categorized = categorize_expenses(expenses)
    rec = recommend_budget(monthly_income, categorized, savings_goal=savings_goal)
    debt_info = debt_advice(debt) if debt else {'status':'no_debt'}
    monthly_savings = rec['baseline']['Savings']
    invest = investment_suggestion(risk, monthly_savings)
    summ = summarize(expenses)
    return jsonify({'categorized':categorized,'recommendation':rec,'debt':debt_info,'investment':invest,'summary':summ})
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5500, debug=True)

