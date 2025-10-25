from advisor import categorize_expenses, recommend_budget, debt_advice, investment_suggestion

def test_categorize_basic():
    exp = [{'desc':'rent','amount':1000},{'desc':'grocery store','amount':200},{'desc':'netflix','amount':15},{'desc':'unknown','amount':50}]
    cats = categorize_expenses(exp)
    assert cats['Housing'] == 1000
    assert cats['Groceries'] == 200
    assert cats['Entertainment'] == 15
    assert cats['Other'] == 50

def test_recommend_budget():
    cats = {'Housing':1000,'Groceries':200,'Utilities':100,'Transport':50,'Entertainment':100,'Dining':50,'Other':0}
    rec = recommend_budget(3000, cats, savings_goal={'amount':6000,'months':12})
    assert 'baseline' in rec
    assert rec['baseline']['Savings'] == 600.0  # 20% of 3000

def test_debt_advice():
    d = {'total':5000,'monthly_payment':200,'interest_rate':12}
    res = debt_advice(d)
    assert res['status'] == 'ok'
    assert res['months_to_payoff'] >= 25

def test_investment_suggestion():
    alloc = investment_suggestion('moderate', 600)
    assert isinstance(alloc, dict)
    assert sum(alloc.values()) <= 600 + 1  # rounding tolerance
