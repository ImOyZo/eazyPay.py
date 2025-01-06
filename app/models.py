from dotenv import load_dotenv
import os
from sqlalchemy import create_engine, Column, Integer, Float, String, ForeignKey, desc
from sqlalchemy.orm import relationship
from app.init import db

class User(db.Model):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)  
    balance = Column(Float, nullable=False, default=0.0)
    account = Column(Integer, unique=True, nullable=False)
    username = Column(String(50), unique=True, nullable=False)  
    password = Column(String(100), nullable=False)  

    sent_payments = relationship('Payment', foreign_keys='Payment.sender', back_populates='sender_user')
    received_payments = relationship('Payment', foreign_keys='Payment.receiver', back_populates='receiver_user')

    def __repr__(self):
        return f"<User(id={self.id}, name={self.name}, balance={self.balance})>"

class Payment(db.Model):
    __tablename__ = 'payment'

    id = Column(Integer, primary_key=True, autoincrement=True)
    payment_number = Column(Integer, unique=True, nullable=False)
    date = Column(String(50), nullable=False)  
    status = Column(String(20), nullable=False)  
    sender = Column(Integer, ForeignKey('users.account'), nullable=False)
    receiver = Column(Integer, ForeignKey('users.account'), nullable=False)
    amount = Column(Float, nullable=False, default=0.0)

    sender_user = relationship('User', foreign_keys=[sender], back_populates='sent_payments')
    receiver_user = relationship('User', foreign_keys=[receiver], back_populates='received_payments')

    def __repr__(self):
        return f"<Payment(id={self.id}, payment_no={self.payment_number}, status={self.status})>"

