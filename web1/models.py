from web1 import app, db
from datetime import datetime


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(50))

    # loans = db.relationship('Loan', backref='customer', lazy='dynamic')
    # payments = db.relationship('Payment', backref='customer', lazy='dynamic')
    # products = db.relationship('Product', secondary='customer_products', backref='customer', lazy='dynamic')
    # loans = db.relationship('Loan', secondary='customer_loans', backref='customer', lazy='dynamic')


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    desc = db.Column(db.String(200))


# Many to Many Relationship
# db.Table("customer_products",
#         db.Column('customer_id', db.Integer, db.ForeignKey('customer.id')),
#         db.Column('product_id', db.Integer, db.ForeignKey('product.id'))
#         )


class Loan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    loan_type = db.Column(db.String(50), nullable=False)
    loan_amount = db.Column(db.Float, nullable=False)
    roi = db.Column(db.Float, nullable=False)
    emi = db.Column(db.Float, nullable=False)
    installments = db.Column(db.Integer, nullable=False)
    total_payable_amount = db.Column(db.Float, nullable=False)
    create_timestamp = db.Column(db.DateTime, default=datetime.now)
    update_timestamp = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    customer_id = db.Column(db.Integer, nullable=False)
    # customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)


class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    loan_type = db.Column(db.String(20), nullable=False)
    loan_number = db.Column(db.Integer, nullable=False)
    installment_number = db.Column(db.Integer)
    installment_amount = db.Column(db.Float)
    customer_id = db.Column(db.Integer, nullable=False)
    # customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))


# Many to Many Relationship
# db.Table("customer_loans",
#         db.Column('customer_id', db.Integer, db.ForeignKey('customer.id')),
#         db.Column('loan_id', db.Integer, db.ForeignKey('loan.id'))
#         )

