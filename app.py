from flask import Flask, render_template, redirect, url_for, flash
from flask_login import UserMixin, LoginManager, login_user, login_required, current_user, logout_user
from flask_bcrypt import Bcrypt
from firebase import *
from firebase_admin import auth

app = Flask(__name__)
app.config['SECRET_KEY'] = 'FlaskAuth'
bcrypt = Bcrypt(app)


db = Database.initializedatabase()
collection = db.collection('users')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(email):
    return auth.get_user_by_email(email)


def createUserinDB(email, name, age, phone):
    res = collection.document(email).set({  # insert document
        'Name': name,
        'Age': age,
        'Phone': phone,
        'Email': email,
    })


# user = collection.document("iamrk98@gmail.com").get().to_dict()

def signup(_email, _phone_number, _password, _name, _age):

    new_user = auth.create_user(
        email=_email,
        phone_number=_phone_number,
        password=_password,
        display_name=_name,
    )

    res = createUserinDB(_email, new_user.display_name, _age, new_user.phone_number)


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/dashboard', methods=["GET", "POST"])
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/logout', methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    form = LoginForm()

    auth.sign
        if user:
            auth.
    #             login_user(user)
    #             return redirect(url_for('dashboard'))
    #         else:
    #             flash("Incorrect Password! Please Try again")
    #     else:
    #         flash("This email is not registered. Try Signing Up!")

    return render_template('login.html')

@app.route('/register', methods=["GET", "POST"])
def register():
    # if current_user.is_authenticated:
    #     return redirect(url_for('dashboard'))
    # form = RegistrationForm()
    #
    # if form.validate_on_submit():
    #     hashed_password = bcrypt.generate_password_hash(form.password.data)
    #     new_user = User(username=form.username.data, password=hashed_password)
    #     db.session.add(new_user)
    #     db.session.commit()
    #     return redirect(url_for('login'))

    return render_template('signup.html')

if __name__ == '__main__':
    app.run(debug=True)