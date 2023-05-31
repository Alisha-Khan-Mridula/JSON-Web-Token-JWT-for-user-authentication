from flask import Flask, request, jsonify, make_response, render_template, session
import jwt
from datetime import datetime, timedelta
from functools import wraps
import traceback
app = Flask(__name__)

#Secrect Key
app.config['SECRET_KEY'] = '57de392eaf3c4c1fa6a6333ba95eb57f68' 

#app.secret_key = '57de392eaf3c4c1fa6a6333ba95eb57f68'


#### Token generation ####
#JWT store the token in client side
def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.args.get('token') #Build the token
        if not token:
            
           return jsonify({'Alert!' : 'Token is missing!'})
        try:
          data = jwt.decode(token, app.config['SECRET_KEY'], algorithms="HS256" )
          
        except Exception as e:
            traceback.print_exc()
            return jsonify({'Alert!': 'Invalid Token'})
        return func(*args, **kwargs)
    return decorated


        


#If user is not logedin , user will be redirect to home page login form
###### Home Page/Login Page ######
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
@app.route('/pub', methods = ['GET'])
@token_required 
def auth():
    return 'JWT is verified.'  


#Verified user name and password , then login
@app.route('/UserLogin', methods=['POST'])
def userLogin():
    if request.form['username'] and request.form['email'] and request.form['number'] and request.form['password'] == '23234':
        session['logged_in'] = True
        token = jwt.encode({'user': request.form['username'],'expiration' : str(datetime.utcnow()+ timedelta(seconds=50))},
        app.config['SECRET_KEY'])
        #app.secret_key)
        return jsonify({'token': token})   
        #return "Success"
    else: 
        #return make_response('Verfication Failed', 403,{'WWW-Authenticate': 'Basic realm:Authentication Failed!!'}) 
        return "Not Success"
    
    

if __name__ == "__main__":
    app.run(debug=True)