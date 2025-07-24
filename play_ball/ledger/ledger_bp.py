from flask import Blueprint, render_template, request, redirect, url_for, session

from play_ball.models import db, Customer, Account, Journal, Transaction, Entry, AuditLog, Users

ledger_bp = Blueprint('ledger', __name__, template_folder='templates')
# -- Accounting
@ledger_bp.route('/chart_of_accounts', methods=['GET', 'POST'])
def chart_of_accounts():
    accounts = Account.query.all()
    return render_template('chart_of_accounts.html', accounts=accounts)

@ledger_bp.route('/sales', methods=['GET', 'POST'])
def make_sale():
    customers = Customer.query.all()
    if request.method == 'POST':
        customer_id = request.form['customer_id']
        amount = float(request.form['amount'])
        desc = request.form['description']
        date_str = request.form['date']
        date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()

        txn = Transaction(customer_id=customer_id, description=desc, transaction_date=date_obj, journal_id=2)
        db.session.add(txn)
        db.session.flush()

        db.session.add(Entry(transaction_id=txn.id, account_id=2, amount=amount, entry_type='debit', memo='Invoice'))  # A/R
        db.session.add(Entry(transaction_id=txn.id, account_id=3, amount=amount, entry_type='credit', memo='Service Revenue'))
        db.session.commit()
        return redirect(url_for('make_sale'))
    return render_template('make_sale.html', customers=customers)

@ledger_bp.route('/receive-payment', methods=['GET', 'POST'])
def receive_payment():
    customers = Customer.query.all()
    if request.method == 'POST':
        customer_id = request.form['customer_id']
        amount = float(request.form['amount'])
        date_str = request.form['date']
        date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()

        txn = Transaction( description='Payment Received', transaction_date=date_obj, journal_id=3)
        db.session.add(txn)
        db.session.flush()

        db.session.add(Entry(transaction_id=txn.id, account_id=1, amount=amount, entry_type='debit', memo='Cash Received'))
        db.session.add(Entry(transaction_id=txn.id, account_id=2, amount=amount, entry_type='credit', memo='Reduce A/R'))
        db.session.commit()
        return redirect(url_for('receive_payment'))
    return render_template('receive_payment.html', customers=customers)

@ledger_bp.route('/open-invoices')
def open_invoices():
    ar_entries = db.session.query(
        Transaction.user_id,
        Users.last_name,
        db.func.sum(db.case((Entry.entry_type == 'debit', Entry.amount), else_=0)).label('invoiced'),
        db.func.sum(db.case((Entry.entry_type == 'credit', Entry.amount), else_=0)).label('paid')
    ).join(Entry).join(Users).filter(Entry.account_id == 2).group_by(Transaction.user_id).all()
    return render_template('open_invoices.html', rows=ar_entries)

@ledger_bp.route('/trial-balance')
def trial_balance():
    balances = db.session.query(
        Account.name,
        Account.code,
        db.func.sum(db.case((Entry.entry_type == 'debit', Entry.amount), else_=0)).label('debits'),
        db.func.sum(db.case((Entry.entry_type == 'credit', Entry.amount), else_=0)).label('credits')
    ).join(Entry).group_by(Account.id).all()
    return render_template('trial_balance.html', balances=balances)


