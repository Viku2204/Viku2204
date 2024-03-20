from flask import Flask, render_template, request, session
from datetime import datetime
from mongodb import MongoDBHelper
import hashlib
import pymongo
generate_password_hash

app = Flask("Bus scheduler service")
app.secret_key = 'Busschedulerservice-key-1'

@app.route("/")
def userlogin():
    return render_template('userlogin.html')

@app.route("/usersignup")
def usersignup():
    return render_template('usersignup.html')

@app.route("/homepage")
def homepage():
    return render_template('homepage.html')

@app.route("/safetyrules")
def safety_rules():
    return render_template('safetyrules.html')

@app.route("/timetable")
def timetable():
    return render_template('timetable.html')

@app.route("/contactus")
def contact():
    return render_template('contactus.html')

@app.route("/find")
def find():
    return render_template('find.html')

@app.route("/registeration-form", methods=['POST'])
def register_user():
    user_data = {
        'name': request.form['fullName'],
        'email': request.form['email'],
        'date of birth': request.form['dob'],
        'phone_no': int(request.form['phoneNumber']),
        'password': hashlib.sha256(request.form['password'].encode('utf-8')).hexdigest(),
    }

    db = MongoDBHelper(collection="user-register")

    try:
        result = db.insert(user_data)
        session['user_name'] = user_data['name']
        session['user_email'] = user_data['email']
        return render_template('homepage.html')
    except pymongo.errors.DuplicateKeyError:
        return render_template('duplicate_error.html')

@app.route("/login", methods=['POST'])
def login():
    email = request.form.get('email')
    provided_password = request.form.get('password')

    db = MongoDBHelper(collection="user-register")
    user_data = db.fetch({'email': email})

    if user_data is not None and check_password_hash(user_data.get('password', ''), provided_password):
        session['user_id'] = str(user_data['_id'])
        session['user_email'] = user_data['email']
        session['user_name'] = user_data['name']

        # Redirect to homepage after successful login
        return render_template('homepage.html')

    # Redirect to signup page if login fails
    return render_template('usersignup.html')

@app.route("/submit-contact", methods=['POST'])
def submit_contact():
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    message = request.form['message']

    contact_data = {
        'name': name,
        'email': email,
        'phone': phone,
        'message': message
    }

    db = MongoDBHelper(collection="contact form")
    result = db.insert(contact_data)

    return render_template('contactus1.html')

def main():
    app.run(port=5002, debug=True)

if __name__ == "__main__":
    main()
