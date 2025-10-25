import matplotlib.pyplot as plt
from advisor import categorize_expenses, summarize
import json

def create_expense_pie(expenses, outpath='expense_pie.png'):
    # expenses: list of {'desc','amount'}
    by_cat = categorize_expenses(expenses)
    labels = []
    sizes = []
    for k,v in by_cat.items():
        labels.append(k)
        sizes.append(v)
    if not sizes:
        print('No expenses to plot.')
        return
    plt.figure(figsize=(6,6))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%')
    plt.title('Expenses by Category')
    plt.tight_layout()
    plt.savefig(outpath)
    plt.close()
    print('Saved', outpath)

if __name__ == '__main__':
    # example usage
    sample = [{'desc':'rent','amount':1200},{'desc':'groceries','amount':300},{'desc':'netflix','amount':12},{'desc':'uber','amount':40}]
    create_expense_pie(sample)
