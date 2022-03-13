from re import T
import os
from flask import Flask, render_template, request, url_for
from flask_mail import Mail, Message
from hashlib import sha256

patient_keys = ["GENESIS"]
doctor_keys = [("GENESIS1", "GENESIS2")]
patient_db = {
    "GENESIS": { 
        "records": [""],
        "doctor_keys": [""]
    }, 
}

app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_DEBUG'] = True
app.config['MAIL_USERNAME'] = 'xdhacksvancouverbot@gmail.com'
app.config['MAIL_PASSWORD'] = os.environ['HACK_PASSWORD']
print(os.environ['HACK_PASSWORD'])
mail = Mail(app)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/register", methods=['POST', 'GET'])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        data = request.json
        if data['isPatient']:
            new_key = sha256(patient_keys[-1].encode()).hexdigest()
            patient_keys.append(new_key)
            patient_db[new_key] = {"records": [], "doctor_keys": []}
            msg = Message("Your authentification key for Unirecords", sender="from@example.com", recipients=[data['email']])
            msg.body = f'Authentification key: {new_key}'
            mail.send(msg)
        else:
            new_public_key = sha256(patient_keys[-1][0].encode()).hexdigest()
            new_private_key = sha256(patient_keys[-1][1].encode()).hexdigest()
            doctor_keys.append((new_public_key, new_private_key))
            msg = Message("Your authentification key for Unirecords", sender="from@example.com", recipients=[data['email']])
            msg.body = f'Public key: {new_public_key}\nPrivate key: {new_private_key}'
            mail.send(msg)
        return "success"
@app.route("/login_patient")
def login_patient():
    return render_template("login_patient.html")

@app.route("/login_doctor")
def login_doctor():
    return render_template("login_doctor.html")

@app.route("/patient/<key>")
def patient_view(key):
    return render_template("patient_view.html")

@app.route("/patient/<key>/update")
def patient_update(key):
    return ("YES")