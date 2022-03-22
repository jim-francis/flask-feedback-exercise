from flask import Flask, render_template, redirect, session, flash
from models import connect_db, db, User
from forms import RegisterForm, LoginForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///flask-feedback"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "NGE4ev"

connect_db(app)

@app.route('/')
def home_page():
    return redirect('/register')

@app.route('/register', methods=["GET", "POST"])
def register_form():
    form = RegisterForm()
    
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        
        user = User.register(username, password, email, first_name, last_name)
        
        db.session.commit()
        session['username'] = user.username
        
        return redirect('/secret')
    
    return render_template('register.html', form=form)

@app.route('/login', methods=["GET", "POST"])
def login_form():
    form = LoginForm()
    
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        user = User.authenticate(username, password)
        if user:
            session['username'] = user.username
            return redirect('/secret')
        else:
            form.username.errors = ["Invalid username/passord."]
            return redirect('/login', form=form)
        
    return render_template('login.html', form=form)

@app.route('/secret')
def secret_page():
    return "You made it!"