# Import libraries
from flask import Flask, render_template, request, url_for, redirect

# Instantiate Flask functionality
app = Flask(__name__)

# Sample data
transactions = [
    {'id': 1, 'date': '2023-06-01', 'amount': 100},
    {'id': 2, 'date': '2023-06-02', 'amount': -200},
    {'id': 3, 'date': '2023-06-03', 'amount': 300}
]

# Read operation
@app.route('/')
def get_transactions():
    return render_template('transactions.html', transactions=transactions)

# Create operation
@app.route("/add", methods=['GET', 'POST'])
def add_transaction():
    if request.method == 'GET':
        return render_template('form.html')
    elif request.method == 'POST':
        transation = {
            'id': len(transactions) + 1,
            'date': request.form['date'],
            'amount': float(request.form['amount']),
        }
        transactions.append(transation)

        return redirect(url_for('get_transactions'))
    return "Please use GET/POST", 404

# Update operation
@app.route('/edit/<int:transaction_id>', methods=['GET', 'POST'])
def edit_transaction(transaction_id):
    if request.method == 'POST':
        date = request.form['date']
        amount = request.form['amount']

        for transaction in transactions:
            if transaction['id'] == transaction_id:
                transaction['date'] = date
                transaction['amount'] = amount
                break
        return redirect(url_for('get_transactions', transactions=transactions))

    for transaction in transactions:
        if transaction['id'] == transaction_id:
            return render_template('edit.html', transaction=transaction)

    return {"msg": "Transaction not found"}, 404

# Delete operation
@app.route("/delete/<int:transaction_id>")
def delete_transaction(transaction_id):
    for transaction in transactions:
        if transaction['id'] == transaction_id:
            transactions.remove(transaction)
            break
    return redirect(url_for('get_transactions'))

# Search Transactions
@app.route("/search", methods=['GET', 'POST'])
def search_transactions():
    if request.method == 'POST':
        max = float(request.form['max_amount'])
        min = float(request.form['min_amount'])
        filtered_transactions = []
        for transaction in transactions:
            if transaction['amount'] >= min and transaction['amount'] <= max:
                filtered_transactions.append(transaction)
        return render_template('transactions.html', transactions=filtered_transactions)
    return render_template('search.html')

# Total Balance
@app.route("/balance")
def total_balance():
    total = 0
    for transaction in transactions:
        total = total + transaction['amount']

    return render_template('transactions.html', transactions=transactions, total=total)

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
    