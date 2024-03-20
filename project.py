from flask import Flask, render_template, request, session, jsonify, redirect, url_for, make_response
import datetime
import hashlib
from mongodb import MongoDBHelper
import json
from pymongo import MongoClient
from io import BytesIO

web_app = Flask("Baker's Walk")
web_app.secret_key = 'bakerswalk-key-1'
@web_app.route("/")
def login_page():
    return render_template('login.html')

@web_app.route("/register")
def register():
    return render_template('register.html')

@web_app.route("/index")
def index():
    return render_template('index.html')

@web_app.route("/menu")
def menu():
    return render_template('menu.html')

@web_app.route("/about")
def about():
    return render_template('about.html')

@web_app.route("/contact")
def contact():
    return render_template('contact.html')


@web_app.route("/register-user", methods=['POST'])
def register_user():
    if request.method == 'POST':
        admin = {
            'name': request.form['name'],
            'email': request.form['email'],
            'password': hashlib.sha256(request.form['pswd'].encode('utf-8')).hexdigest(),
            'createdOn': datetime.datetime.today()
        }
        db = MongoDBHelper(collection="ID")
        result = db.insert(admin)
        owner_id = result.inserted_id
        session['owner_id'] = str(owner_id)
        session['owner_name'] = admin['name']
        session['owner_email'] = admin['email']
        return render_template('index.html', email=session['owner_email'])



@web_app.route("/login-owner", methods=['POST'])
def login_bin():

    owner_data = {
        'email': request.form['email'],
        'password': hashlib.sha256(request.form['pswd'].encode('utf-8')).hexdigest(),
    }

    print(owner_data)
    db = MongoDBHelper(collection="ID")
    documents = db.fetch(owner_data)
    print(documents, type(documents))
    if len(documents) == 1:
        session['owner_id'] = str(documents[0]['_id'])
        session['owner_email'] = documents[0]['email']
        session['owner_name'] = documents[0]['name']
        print(vars(session))
        return render_template('index.html', email=session['owner_email'], name=session['owner_name'])
    else:
        return render_template('error.html')

@web_app.route("/send-message", methods=['POST'])
def send_message():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        contact_data={
            'name': name,
            'email': email,
            'message': message
        }
        db=MongoDBHelper(collection="feedback")
        result=db.insert(contact_data)

    return render_template('feedback.html')

@web_app.route('/inventory', methods=['POST', 'GET'])
def inventory_data():
    if request.method == 'POST':
        # Handle form submission
        Product_name = request.form.get('product_name')
        belong= session['owner_email']
        price = request.form.get('price')
        quantity = request.form.get('quantity')
        total = int(price) * int(quantity)

        item = {
            'Product_name': Product_name,
            'price': price,
            'quantity': quantity,
            'total': total,
            'belong' :belong
        }

        db = MongoDBHelper(collection="yubi")
        result = db.insert(item)
        owner_id = result.inserted_id
        item=item;
        print(item)

        return render_template('add.html')

    elif request.method == 'GET':
        # Retrieve data from cookies (assuming it was stored as a string)
        inventory_data_str = request.cookies.get('inventory_data', '[]')
        inventory_data = eval(inventory_data_str)
        return render_template('inventory.html', inventory_data=inventory_data)


@web_app.route("/cart")
def cart():
    db = MongoDBHelper(collection="yubi")
    query = {'belong': session['owner_email']}
    documents = db.fetch(query)
    print(documents, type(documents))
    return render_template('inventory.html' , inventory=documents)

@web_app.route("/delete/<belong>")
def delete_work(belong):
    db = MongoDBHelper(collection="yubi")
    query = {'belong': belong}
    customer = db.fetch(query)[0]
    db.delete(query)
    return render_template('delete.html')



def main():
    web_app.run(port=5000)

if __name__ == "__main__":
    main()
