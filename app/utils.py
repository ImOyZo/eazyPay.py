from datetime import datetime
from sqlalchemy.orm import Session
from .models import User, Payment

def login(session: Session, username: str, password: str):
    user = session.query(User).filter_by(username=username, password=password).first()
    if user:
        return user
    else:
        return "Invalid credentials!"

def make_payment(session: Session, sender_account: int, receiver_account: int, receiver_username: str, amount: float, status="Successful"):
    sender = session.query(User).filter_by(account=sender_account).first()
    receiver = session.query(User).filter_by(account=receiver_account, username=receiver_username).first()

    if not sender or not receiver:
        return "Sender or Receiver not found!"

    if sender.balance < amount:
        return "Insufficient balance in sender's account!"

    sender.balance -= amount
    receiver.balance += amount

    payment = session.query(Payment).filter_by(sender=sender_account, receiver=receiver_account, status='pending').order_by(Payment.payment_number).first()

    if not payment:
        return "No pending payment record found to update!"

    rows_updated = session.query(Payment).filter_by(
        sender=sender_account, receiver=receiver_account, status='pending', payment_number=payment.payment_number
    ).update({
        Payment.amount: amount,
        Payment.date: datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        Payment.status: status
    })

    if rows_updated == 0:
        return "No pending payment record found to update!"

    session.commit()
    return f"Payment from {sender_account} to {receiver_account} updated successfully!"

def create_invoice(session: Session, sender_account: int, receiver_account: int, amount: float, status: str = "pending"):
    receiver = session.query(User).filter_by(account=sender_account).first()
    if not receiver:
        return "Receiver not found!"

    invoice = Payment(
        payment_number=int(datetime.now().timestamp()),
        date=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        status=status,
        sender=sender_account,
        receiver=receiver_account,
        amount=amount
    )
    session.add(invoice)
    session.commit()

    return f"Invoice of {amount} to {receiver.name} created successfully!"
