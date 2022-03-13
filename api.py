from crypt import methods
import enum
from re import T
import os
from flask import Flask, render_template, request, url_for
from flask_mail import Mail, Message
from hashlib import sha256
import json

patient_keys = ["GENESIS"]
doctor_keys = {"GENESISPRIVATE": "GENESISPUBLIC"}
patient_db = {
    "GENESIS": { 
        "records": [],
        "doctor_keys": []
    }, 
    "TEST": { 
        "records": ["drive.google.com/profile.pdf"],
        "doctor_keys": ["aksdjfldsa92edk0", "GENESISPUBLIC"]
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
            doctor_keys[new_private_key] = new_public_key
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
    try:
        patient_data = patient_db[key]
    except:
        return "No user exists."
    else:
        return render_template("patient_view.html", data=patient_db[key],
                                url1=f'/patient/{key}/perm', 
                                url2=f'/patient/{key}/records', 
                                url3=f'/patient/{key}/profile')

@app.route("/patient/<key>/perm")
def patient_perm(key):
    return render_template("patient_perm.html", key=key, inp_keys=patient_db[key]['doctor_keys'])

@app.route("/patient/<key>/records")
def patient_records(key):
    return render_template("patient_records.html", key=key, inp_records=patient_db[key]['records'])

@app.route("/doctor/<key>")
def doctor_view(key):
    pubkey = doctor_keys[key]
    patients_of_doctor = []
    for i in patient_db:
        if pubkey in patient_db[i]["doctor_keys"]:
            patients_of_doctor.append(patient_db[i])
    return render_template("doctor_view.html", patients=patients_of_doctor, enumerate=enumerate)

@app.route("/api/updateRecords", methods=["POST"])
def update_records():
    data = request.json
    try:
        patient_db[data['patient_key']]
    except:
        return "fail"
    else:
        patient_db[data['patient_key']]['records'] = data['records']
        print(patient_db)
        return "success"

@app.route("/api/updatePerm", methods=["POST"])
def update_perm():
    data = request.json
    try:
        patient_db[data['patient_key']]
    except:
        return "fail"
    else:
        patient_db[data['patient_key']]['doctor_keys'] = data['doctor_keys']
        print(patient_db)
        return "success"
