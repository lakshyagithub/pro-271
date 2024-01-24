# Download the helper library from https://www.twilio.com/docs/python/install
import os
from flask import Flask, request, jsonify, render_template, redirect, url_for
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Replace these placeholders with your actual Twilio credentials
account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_API_KEY')
service_sid = os.getenv('TWILIO_SYNC_SERVICE_SID')

client = Client(account_sid, auth_token)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    mobile_number = request.form['number']

    if username == 'verify' and password == '12345':
        verification = client.verify \
            .services(service_sid) \
            .verifications \
            .create(to=mobile_number, channel='sms')

        print(verification.status)

        return render_template('otp_verify.html')
    else:
        return render_template('user_error.html')

@app.route('/otp', methods=['POST'])
def get_otp():
    print("Processing")

    received_otp = request.form['received_otp']
    mobile_number = request.form['number']

    # Replace with your Twilio credentials
    account_sid = os.getenv('TWILIO_ACCOUNT_SID')
    auth_token = os.getenv('TWILIO_API_KEY')
    client = Client(account_sid, auth_token)
    service_sid = os.getenv('TWILIO_SYNC_SERVICE_SID')
    verification_check = client.verify \
        .services(service_sid) \
        .verification_checks \
        .create(to=mobile_number, code=received_otp)

    print(verification_check.status)

    if verification_check.status == "pending":
        return "Entered OTP is wrong"
    else:
        return redirect("https://project-c272.onrender.com/")  # Update with your hosted notepad URL

if __name__ == "__main__":
    app.run()
