import math
from collections import defaultdict

KEYWORD_CATEGORIES = {
    'Housing': ['rent', 'mortgage', 'landlord', 'home'],
    'Groceries': ['grocery', 'groceries', 'supermarket', 'aldi', 'walmart'],
    'Utilities': ['electric', 'water', 'gas', 'internet', 'phone', 'utility'],
    'Transport': ['uber', 'taxi', 'bus', 'train', 'fuel', 'gasoline', 'parking'],
    'Entertainment': ['netflix', 'spotify', 'movie', 'concert', 'game'],
    'Dining': ['restaurant', 'cafe', 'dinner', 'lunch', 'breakfast', 'starbucks'],
    'Insurance': ['insurance', 'premium', 'health insurance', 'car insurance'],
    'Healthcare': ['doctor', 'hospital', 'pharmacy', 'medicine'],
    'Education': ['course', 'tuition', 'school', 'books'],
    'Savings': ['saving', 'deposit'],
    'Other': []
}

def categorize_expenses(expenses):
    """Expenses: list of {'desc':..., 'amount':...}. Returns dict category -> total."""
    cat_totals = defaultdict(float)
    if not expenses:
        return dict(cat_totals)

    for e in expenses:
        # normalize description (allow non-dict items)
        desc = ''
        if isinstance(e, dict):
            desc = (e.get('desc', '') or '')
        else:
            try:
                desc = str(e)
            except Exception:
                desc = ''
        desc = desc.lower()

        # parse amount robustly
        amt = 0.0
        if isinstance(e, dict):
            raw_amt = e.get('amount', 0)
        else:
            raw_amt = 0
        try:
            amt = float(raw_amt or 0)
        except Exception:
            try:
                amt = float(str(raw_amt).replace(',', ''))
            except Exception:
                amt = 0.0

        assigned = False
        for cat, keywords in KEYWORD_CATEGORIES.items():
            for kw in keywords:
                if kw and kw in desc:
                    cat_totals[cat] += amt
                    assigned = True
                    break
            if assigned:
                break
        if not assigned:
            cat_totals['Other'] += amt
    return dict(cat_totals)

def recommend_budget(monthly_income, categorized_expenses, savings_goal=None):
    """Returns recommended allocations and suggestions using a rule-based approach."""
    try:
        income = float(monthly_income or 0)
    except Exception:
        income = 0.0

    essentials = (categorized_expenses.get('Housing', 0) + categorized_expenses.get('Groceries', 0) +
                  categorized_expenses.get('Utilities', 0) + categorized_expenses.get('Transport', 0) +
                  categorized_expenses.get('Insurance', 0) + categorized_expenses.get('Healthcare', 0))
    discretionary = (categorized_expenses.get('Entertainment', 0) + categorized_expenses.get('Dining', 0) +
                     categorized_expenses.get('Other', 0))
    existing_savings = categorized_expenses.get('Savings', 0)

    # baseline using 50/30/20 rule
    baseline = {'Essentials': round(income * 0.5,2), 'Wants': round(income * 0.3,2), 'Savings': round(income * 0.2,2)}

    # compare actual spending to baseline
    actual_essentials = essentials
    actual_wants = discretionary
    actual_savings = existing_savings

    adjustments = []

    if income <= 0:
        adjustments.append("Monthly income is zero or invalid; baseline recommendations are not meaningful.")

    # warn if expenses exceed income (when income provided)
    total_spent = sum(categorized_expenses.values())
    if income and total_spent > income:
        adjustments.append(f"Total tracked expenses ${total_spent:.2f} exceed income ${income:.2f}. Review transactions or adjust budget.")

    if actual_essentials > baseline['Essentials']:
        adjustments.append(f"Essentials spending is high: ${actual_essentials:.2f} vs baseline ${baseline['Essentials']:.2f}. Consider reviewing subscriptions or renegotiating bills.")
    if actual_wants > baseline['Wants']:
        adjustments.append(f"Discretionary spending is high: ${actual_wants:.2f}. Try a 20% cut to meet savings goals.")

    # if user has a specific savings goal, compute required monthly saving
    if savings_goal and isinstance(savings_goal, dict):
        try:
            amt = float(savings_goal.get('amount', 0) or 0)
        except Exception:
            amt = 0.0
        try:
            months = int(savings_goal.get('months', 0) or 0)
        except Exception:
            months = 0

        if months <= 0:
            adjustments.append("Savings goal requires a positive number of months.")
        else:
            required = round(amt / months, 2)
            if required > baseline['Savings']:
                adjustments.append(f"To reach your goal you'd need to save ${required:.2f}/month which is above baseline savings ${baseline['Savings']:.2f}. Consider reducing wants or extending timeline.")
            else:
                adjustments.append(f"Your savings goal requires ${required:.2f}/month — this fits within baseline savings.")
    return {
        'baseline': baseline,
        'actual': {'Essentials': round(actual_essentials,2), 'Wants': round(actual_wants,2), 'Savings': round(actual_savings,2)},
        'adjustments': adjustments
    }

def debt_advice(debt):
    """Debt: {'total':..., 'monthly_payment':..., 'interest_rate':...} Returns simple payoff estimate and strategy."""
    if not debt or float(debt.get('total', 0) or 0) <= 0:
        return {'status': 'no_debt'}
    total = float(debt.get('total', 0) or 0)
    pmt = float(debt.get('monthly_payment', 0) or 0)
    apr = float(debt.get('interest_rate', 0) or 0)
    monthly_rate = apr / 100.0 / 12.0  # monthly rate

    if pmt <= 0:
        return {'status': 'missing_payment', 'message': 'Monthly payment must be > 0 to estimate payoff.'}

    # If there's interest, use amortization formula when possible:
    months = None
    if monthly_rate > 0:
        # If payment is less than or equal to monthly interest, balance won't decrease
        if pmt <= total * monthly_rate:
            return {'status': 'insufficient_payment', 'message': 'Monthly payment does not cover interest; balance will not be paid down.'}
        try:
            months_f = math.log(pmt / (pmt - total * monthly_rate)) / math.log(1 + monthly_rate)
            months = math.ceil(months_f)
        except Exception:
            months = math.ceil(total / pmt)
    else:
        months = math.ceil(total / pmt)

    strategy = 'avalanche' if monthly_rate > 0.015 else 'snowball'  # heuristic
    return {'status': 'ok', 'months_to_payoff': months, 'strategy': strategy, 'interest_rate': apr}

def investment_suggestion(risk_profile, monthly_savings):
    """Return suggested allocation based on risk profile."""
    try:
        s = float(monthly_savings or 0)
    except Exception:
        s = 0.0

    rp = (risk_profile or '').strip().lower()
    if rp == 'conservative':
        alloc = {'HighYieldSavings': 0.6, 'Bonds': 0.3, 'LowRiskETFs': 0.1}
    elif rp == 'aggressive':
        alloc = {'US_Stocks': 0.5, 'International_Stocks': 0.2, 'Growth_ETFs': 0.2, 'Crypto': 0.1}
    else:  # moderate or unknown
        alloc = {'US_Stocks': 0.4, 'Bonds': 0.3, 'Intl_Stocks': 0.2, 'Cash': 0.1}
    # convert to dollar suggestions
    return {k: round(v * s,2) for k,v in alloc.items()}

def summarize(expenses):
    total = sum(float(e.get('amount', 0) or 0) if isinstance(e, dict) else 0 for e in expenses or [])
    by_cat = categorize_expenses(expenses or [])
    top = sorted(by_cat.items(), key=lambda x: x[1], reverse=True)[:5]
    return {'total': round(total,2), 'by_category': by_cat, 'top_categories': top}
