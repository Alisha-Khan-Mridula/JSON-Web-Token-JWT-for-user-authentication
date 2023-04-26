from flask import Flask, request, jsonify, make_response, render_template, session
import jwt
from datetime import datetime, timedelta
from functools import wraps

app = Flask(__name__)

#Secrect Key
app.config['SECRET_kEY'] = '57de392eaf3c4c1fa6a63ba95eb57f68' 


#If user is not logedin , user will be redirect to home page login form
@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('LoginPage.html')
    else:
        return "You are currently logged in"



if __name__ == "__main__":
    app.run(debug=True)