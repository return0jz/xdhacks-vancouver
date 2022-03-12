from flask import Flask, render_template, request, url_for
from hashlib import sha256

patient_keys = ["GENESIS"]

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/register", methods=['POST', 'GET'])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        new_key = sha256(patient_keys[-1].encode()).hexdigest()
        patient_keys.append(new_key)
        return new_key