#---setup

from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:admin@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

#---Blog Model-------------------------------------------------------

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(500))

    def __init__(self, title, body):
        self.title = title
        self.body = body

#---helper functions-------------------------------------------------------

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

#---hanlders-------------------------------------------------------

@app.route('/', methods=['GET'])
def index():

    blog_posts = Blog.query.all()

    return render_template('post_list.html',title="Build-a-blog", blog_posts=blog_posts)

@app.route('/blog', methods=['GET'])
def list_post():

    if request.method == 'GET':
        blog_post_id = request.args.get('id')
        new_blog_post = Blog.query.filter_by(id=blog_post_id).first()
        return render_template('display_post.html', new_blog_post=new_blog_post)

@app.route('/newpost', methods=['POST', 'GET'])
def create_new_post():

    if request.method == 'GET':
        return render_template('create_post.html')

    if request.method == 'POST':
        blog_title = request.form['blog-title']
        blog_content = request.form['blog-body']
    if len(blog_title) != 0 and len(blog_content) != 0:
        new_blog_post = Blog(blog_title,blog_content)
        db.session.add(new_blog_post)
        db.session.commit() 
        return redirect(f'/blog?id={new_blog_post.id}')

    if len(blog_title) == 0 or len(blog_content) == 0:
        title_error = is_title_blank(blog_title)
        body_error = is_body_blank(blog_content)
        return render_template('create_post.html', 
        title="Build-a-blog", 
        title_error=title_error, 
        body_error=body_error)
               
    return render_template('post_list.html' ,title="Build-a-blog")

if __name__ == '__main__':
    app.run()