from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:admin@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
app.secret_key = "SuperSecretString"
db = SQLAlchemy(app)

#---Models----------------------------------------------------------------

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(500))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password

#---helper functions-------------------------------------------------------

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

def get_blog_post(id):
  return Blog.query.get(id)

def get_blog_posts():
  return Blog.query.all()

def is_title_blank(title):
    if len(title) == 0:
        return "Please fill out title"
    ""
def is_body_blank(body):
    if len(body) == 0:
        return "Please fill out body"
    ""

#--before request handler------------------------------------------

@app.before_request
def require_login():
    allowed_routes = ['login','signup', 'index', 'list_posts']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')

#---hanlders-------------------------------------------------------

@app.route('/', methods=['GET'])
def index():
    all_users = User.query.all()
    return render_template('index.html',title="blog users", all_users=all_users)

@app.route('/blog')
def list_posts():
    blog_post_id = request.args.get('id')
    user_id = request.args.get('user')
    if blog_post_id:
        new_blog_post = Blog.query.filter_by(id=blog_post_id).first()
        return render_template('display_post.html', new_blog_post=new_blog_post)
    elif user_id:
        owner = User.query.filter_by(id=user_id).first()
        all_user_posts = Blog.query.filter_by(owner=owner).all()
        return render_template('singleUser.html', all_user_posts=all_user_posts, username=owner)
    else:
        blog_posts = Blog.query.all()
        return render_template('post_list.html',title="Blogz", blog_posts=blog_posts)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        username_error = username_error_f(username)
        password_error = password_error_f(password)
        user = User.query.filter_by(username=username).first()

        if is_username_valid(username) is True and is_password_valid(password) is True:
            if user and user.password == password:
                session['username'] = username
                flash('Logged in')
                return redirect('/')
            elif not user:                
                return render_template('login.html', username_error='username does not exist')
            return render_template('login.html', password_error='incorrect password')

        return render_template('login.html', password_error=password_error, username_error=username_error)

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')

    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"] 
        verify_password = request.form["verify-password"]

        username_error = username_error_f(username)
        password_error = password_error_f(password)
        password_verification_error = password_v_error_f(password,verify_password)

        if is_username_valid(username) is True and is_password_valid(password) is True and password == verify_password:
            existing_user = User.query.filter_by(username=username).first()
            if not existing_user:
                session['username']=username
                new_user = User(username,password)
                db.session.add(new_user)
                db.session.commit() 
                flash('Account created')
                return redirect('/')
            return render_template("signup.html", username_error="username already exists")
        else:
            return render_template("signup.html", 
            username_error=username_error, 
            password_error=password_error, 
            password_verification_error=password_verification_error, 
            username=username)

@app.route('/logout')
def logout():
    if 'username' not in session:
        flash('Not logged in')
        return redirect('/login')
    del session['username']
    flash('Logged out')
    return redirect('/')

@app.route('/newpost', methods=['POST', 'GET'])
def create_new_post():

    if request.method == 'GET':
        return render_template('create_post.html')

    if request.method == 'POST':
        owner = User.query.filter_by(username=session['username']).first()
        blog_title = request.form['blog-title']
        blog_content = request.form['blog-body']
    if len(blog_title) != 0 and len(blog_content) != 0:
        new_blog_post = Blog(blog_title,blog_content,owner)
        db.session.add(new_blog_post)
        db.session.commit() 
        return render_template('display_post.html', new_blog_post=new_blog_post)

    if len(blog_title) == 0 or len(blog_content) == 0:
        title_error = is_title_blank(blog_title)
        body_error = is_body_blank(blog_content)
        return render_template('create_post.html', 
        title="Blogz", 
        title_error=title_error, 
        body_error=body_error)
               
    return render_template('post_list.html' ,title="Blogz")

if __name__ == '__main__':
    app.run()