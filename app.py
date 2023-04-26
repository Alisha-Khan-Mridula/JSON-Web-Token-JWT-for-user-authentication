from flask import Flask, request, jsonify, make_response, render_template, session
import jwt
from datetime import datetime, timedelta
from functools import wraps

app = Flask(__name__)

#Secrect Key
app.config['SECRET_kEY'] = '57de392eaf3c4c1fa6a63ba95eb57f68' 

#JWT store the token in client side
def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.args.get('token') #Build the token
        if not token:
            
           return jsonify({'Alert!' : 'Token is missing!'})
        try:
          payload = jwt.decode(token, app.config['SECRET_KEY'])
          
        except:
            return jsonify({'Alert!': 'Invalid Token'})
        
        return decorated
        


#If user is not logedin , user will be redirect to home page login form
#Home Page
@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('LoginPage.html')
    else:
        return "You are currently logged in"
    
    
    
#For public users    
@app.route('/public')
def public():
    return  'For Public'

#For authenticated users
@app.route('/auth')
@token_required 
def auth():
    return 'JWT is verified. Welcome to Dashboard'  


#Verified user name and password , then login
@app.route('/UserLogin', methods=['POST'])
def userLogin():
    if request.form['username'] and request.form['email'] and request.form['number'] and request.form['password'] == '23234':
        session['logged_in'] = True
        token = jwt.encode({
          'user': request.form['username'],
          'expiration' : str(datetime.utcnow()+ timedelta(seconds=60))
        },
        app.config['SECRET_KEY'])
        return jsonify({'token': token.decode('utf-8')})   
    else: 
        return make_response('Verfication Failed', 403,{'WWW-Authenticate': 'Basic realm:Authentication Failed!!'}) 
    
    

if __name__ == "__main__":
    app.run(debug=True)