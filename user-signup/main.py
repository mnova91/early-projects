from flask import Flask, request, redirect, render_template
import cgi
import os
import jinja2

template_dir = os.path.join(os.path.dirname(__file__),'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

app = Flask(__name__)
app.config['DEBUG']=True

def is_username_valid(username):
    if len(username) >= 3 and len(username) <= 20:
        if " " not in username:
            return True
        False
    False

def is_password_valid(password):
    if len(password) >= 3 and len(password) <= 20:
        if " " not in password:
            return True
        False
    False

def is_email_valid(email):
    if len(email) == 0:
        return True
    elif len(email) >= 3 and len(email) <= 20:
        if "@" and "." in email:
            return True
        False
    False

def username_error_f(username):
    if is_username_valid(username):
        return ""
    return "That's not a valid username"

def password_error_f(password):
    if is_password_valid(password):
        return ""
    return "That's not a valid password"

def password_v_error_f(password, verify_password):
    if is_password_valid(verify_password):
        if password == verify_password:
            return ""
        return "Passwords don't match"
    return "That's not a valid password"

def email_error_f(email):
    if email == "":
        return ""
    elif is_email_valid(email):
        return ""
    return "That's not a valid email"

@app.route("/")
def index():
    return render_template("login_form.html")

@app.route("/login", methods=["POST"])
def validate():
    
    username = request.form["username"]
    password = request.form["password"] 
    verify_password = request.form["verify-password"]
    email = request.form["email"]

    username_error = username_error_f(username)
    password_error = password_error_f(password)
    password_verification_error = password_v_error_f(password,verify_password)
    email_error = email_error_f(email)

    if is_username_valid(username) is True and is_password_valid(password) is True and password == verify_password and is_email_valid(email) is True:
        return render_template("login_greeting.html", 
        username=request.form["username"])
    else:
        return render_template("login_form.html", 
        username_error=username_error, 
        password_error=password_error, 
        password_verification_error=password_verification_error, 
        email_error=email_error,
        email=email, 
        username=username)

app.run()