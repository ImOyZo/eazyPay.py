from flask import Blueprint, redirect, render_template, request, jsonify, session as flask_session
from .utils import login, make_payment, create_invoice 
from .models import db, User, Payment, desc

bp = Blueprint('main', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login_user_route():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        with db.session() as session:
            result = login(session, username, password)

        if result:
            flask_session['username'] = result.username  
            flask_session['account'] = result.account
            return jsonify({"message": f"Welcome Back {result.name}" }), 200 
        else:
            return jsonify({"message": result}), 401  
        
    return render_template('login.html')

@bp.route('/dashboard')
def dashboard_route():
    username = flask_session.get('username')

    user = db.session.query(User).filter_by(username=username).first()

    if user:
        print(f"User found: {user}")
        return render_template('Dashboard.html', 
                               user_name=user.name, 
                               user_account=user.account, 
                               user_balance=user.balance)
    else:
        print("User not found!") 
        return "User not found!"
    
@bp.route('/invoice')
def invoice():
    return render_template('Create_Invoice-1.html')
    
@bp.route('/create-invoice', methods=['GET','POST'])
def create_invoice_route():
    
    if request.method == 'POST':
        data = request.json
        print(data)
        sender_account = data['account']
        receiver_account = flask_session.get('account')
        amount = data['amount']

        with db.session() as session:
            result = create_invoice(session, sender_account, receiver_account, amount)
        return jsonify({"message": result})

    return render_template('Create_Invoice-2.html')

@bp.route('/invoice-result')
def invoice_information_route():
    account = flask_session.get('account')
    print(f"Account from session: {account}")

    payment = db.session.query(Payment.amount, Payment.receiver, Payment.sender).filter_by(receiver=account, status='pending').first()
    print(f"Query result: {payment}")

    if payment:
        amount, receiver, sender = payment
        print(f"User found: {payment}")
        return render_template('Invoice_Information.html', 
                               user_account_sender=sender, 
                               user_account_receiver=receiver, 
                               user_amount=amount)
    else:
        print("Payment not found!") 
        return "Payment not found!"
    
@bp.route('/payment-success')
def payment_success_route():
    account = flask_session.get('account')
    print(f"Account from session: {account}")

    payment = db.session.query(Payment.amount, Payment.receiver, Payment.sender).filter_by(sender=account, status='Successful').order_by(desc(Payment.payment_number)).first()
    amount, receiver, sender = payment
    return render_template('Payment_Success.html', 
                           sender_account = sender,
                           receiver_account = receiver,
                           payment_amount = amount)


@bp.route('/perform-payment', methods=['GET', 'POST'])
def make_payment_route():
    if request.method == 'POST':
        data = request.json
        receiver_account = data['account']
        receiver_username = data['username']

        sender_account = flask_session.get('account')

        # Query the payment amount
        payment = db.session.query(Payment.amount).filter_by(receiver=receiver_account, status='pending').first()
        
        # Extract the amount from the query result
        if payment:
            amount = payment.amount  # Extract the float value
        else:
            return jsonify({"message": "No pending payment found for this receiver."})

        with db.session() as session:
            result = make_payment(session, sender_account, receiver_account, receiver_username, amount)
        
        return jsonify({"message": result})

    # Render the payment page for GET requests
    return render_template('Perform_Payment.html')



