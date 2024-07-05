from web1 import app, db
from flask import render_template, redirect, url_for
from web1.models import Customer, Product, Payment, Loan
from web1.forms import AddCustomer, AddProduct, AssignLoan, AddPayment


@app.route("/")
def homepage():
    """
    home page
    :return:
    show home page
    """
    return render_template('index.html', title="Welcome")


@app.route("/add_customer", methods=["GET", "POST"])
def add_customer():
    form = AddCustomer()
    if form.validate_on_submit():
        customer = Customer(name=form.username.data, phone=form.phone.data)
        db.session.add(customer)
        db.session.commit()
        return redirect(url_for('list_customers'))
    return render_template("customer.html", form=form)


@app.route("/list_customers", methods=["GET", "POST"])
def list_customers():
    customers = Customer.query.all()
    return render_template("customers.html", customers=customers)


@app.route("/add_product", methods=["GET", "POST"])
def add_product():
    form = AddProduct()
    if form.validate_on_submit():
        product = Product(name=form.name.data, desc=form.description.data)
        db.session.add(product)
        db.session.commit()
        return redirect(url_for('list_products'))
    return render_template("product.html", form=form)


@app.route("/list_products", methods=["GET", "POST"])
def list_products():
    products = Product.query.all()
    return render_template("products.html", products=products)


@app.route("/customers/assign/<int:id>", methods=["GET", "POST"])
def assign_loan(id):
    customer = Customer.query.get_or_404(id)
    form = AssignLoan()
    if form.validate_on_submit():
        loan_type = form.products.data.name
        loan_amount = form.loan_amount.data
        roi = form.roi.data
        emi = form.emi.data
        installments = form.installments.data
        total_payable_amount = form.total_payable_amount.data
        loan = Loan(loan_type=loan_type, loan_amount=loan_amount, roi=roi, emi=emi,
                    installments=installments, total_payable_amount=total_payable_amount,
                    customer_id=customer.id)
        db.session.add(loan)
        db.session.commit()
        return redirect(url_for('customer_details',id=id))
    return render_template("assign_loan.html", form=form, customer=customer)


@app.route("/customer/details/<int:id>", methods=["GET", "POST"])
def customer_details(id):
    customer = Customer.query.get_or_404(id)
    loans = Loan.query.filter_by(customer_id=id).all()
    return render_template("customer_details.html", customer=customer, loans=loans)


@app.route("/customer/add_payment/<int:id>/<string:loan_type>", methods=["GET", "POST"])
def add_payment(id, loan_type):
    customer = Customer.query.get_or_404(id)
    loan = Loan.query.filter_by(customer_id=id).filter_by(loan_type=loan_type).first()
    print(loan)
    form = AddPayment()
    form.loan_type.data = loan_type
    form.loan_number.data = loan.id
    form.customer_id.data = id
    if form.validate_on_submit():

        installment_number = form.installment_number.data
        installment_amount = form.installment_amount.data
        payment = Payment(loan_type=loan_type, loan_number= loan.id, installment_number=installment_number,
                          installment_amount=installment_amount,customer_id=id)
        db.session.add(payment)
        db.session.commit()
        return redirect(url_for('payment_details', id=id, loan_type=loan_type))
    return render_template("add_payment.html", form=form, customer=customer, loan_type=loan_type)


@app.route("/customer/payment/<int:id>/<string:loan_type>", methods=["GET", "POST"])
def payment_details(id, loan_type):

    customer = Customer.query.get_or_404(id)
    payments = Payment.query.filter_by(customer_id=id).filter_by(loan_type=loan_type).all()
    loan = Loan.query.filter_by(customer_id=id, loan_type=loan_type).first()

    return render_template("payment_details.html", customer=customer, payments=payments, loan=loan)