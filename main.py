import pyrebase
from firebase import *
from firebaseConfig import *
from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
from flask_login import LoginManager, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'FlaskAuth'#Initialze flask constructor

db = Database.initializedatabase()
collection = db.collection('users')

#initialize firebase
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return auth.get_user(user_id)

#Initialze person as dictionary

person = {"is_logged_in": False, "name": "", "email": "", "uid": "", "age": "", "phone": ""}

#Login
@app.route("/")
def login():
    return render_template("login.html")

#Sign up/ Register
@app.route("/signup")
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('welcome'))
    else:
        return render_template("signup.html")

#Welcome page
@app.route("/welcome")
def welcome():
        return render_template("welcome.html", email = person["email"], name = person["name"])

#If someone clicks on login, they are redirected to /result
@app.route("/result", methods = ["POST", "GET"])
def result():
    if request.method == "POST":        #Only if data has been posted
        result = request.form.to_dict()           #Get the data
        print(result)
        email = result["email"]
        password = result["pass"]
        try:
            #Try signing in the user with the given information
            user = auth.sign_in_with_email_and_password(email, password)
            # Insert the user data in the global person
            global person
            person["is_logged_in"] = True
            person["email"] = user["email"]
            person["uid"] = user["localId"]
            #Get the name of the user
            data = collection.document(email).get().to_dict()
            person["name"] = data["Name"]
            #Redirect to welcome page
            return redirect(url_for('welcome'))
        except:
            #If there is any error, redirect back to login
            print("redirecting user to login page")
            return redirect(url_for('login'))
    else:
        print("else part reached")
        if person["is_logged_in"] == True:
            return redirect(url_for('welcome'))
        else:
            return redirect(url_for('login'))

#If someone clicks on register, they are redirected to /register
@app.route("/register", methods = ["POST", "GET"])
def register():
    if request.method == "POST":        #Only listen to POST
        result = request.form.to_dict()           #Get the data submitted
        print(result)
        email = result["email"]
        print(email)
        password = result["pass"]
        print(password)
        name = result["name"]
        age = result["age"]
        phone = result["phone"]
        try:
            #Try creating the user account using the provided data
            auth.create_user_with_email_and_password(email, password)
            #Login the user
            user = auth.sign_in_with_email_and_password(email, password)
            #Add data to global person
            global person
            person["is_logged_in"] = True
            person["email"] = user["email"]
            person["uid"] = user["localId"]
            person["name"] = name
            person["age"] = age
            person["phone"] = phone
            #Append data to the cloud firestore database
            collection.document(user["email"]).set({  # insert document
                'is_logged_in': True,
                'uid': user["localId"],
                'Name': name,
                'Age': age,
                'Phone': phone,
                'Email': user["email"],
            })
            #Go to welcome page
            return redirect(url_for('welcome'))
        except:
            #If there is any error, redirect to register
            return redirect(url_for('register'))

    else:
        if current_user.is_authenticated:
            return redirect(url_for('welcome'))
        else:
            return redirect(url_for('register'))

if __name__ == "__main__":
    app.run(debug=True)