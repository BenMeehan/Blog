from flask import Flask, render_template, request, redirect, url_for
from post import Post
import smtplib
import requests

from flask_sqlalchemy import SQLAlchemy
from flask_ckeditor import CKEditor

MAIL_NAME = "spacetimebenmeehan@gmail.com"
MAIL_PASSWORD = "aval1234"

post_list = []

app = Flask("__name__")
ckeditor = CKEditor(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class HomeContent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    home_image = db.Column(db.String, nullable=False)
    quote = db.Column(db.String, nullable=False)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_url = db.Column(db.String, nullable=False)
    title = db.Column(db.String, nullable=False, unique=True)
    subtitle = db.Column(db.String, nullable=False)
    body = db.Column(db.String, nullable=False)
    date = db.Column(db.String, nullable=False)


db.create_all()


def get_home():
    result = HomeContent.query.get(1)
    home_image = result.home_image
    quote = result.quote
    return (home_image, quote)


def get_posts():
    global post_list
    post_list = []
    results = db.session.query(Post).all()
    for i in results:
        obj = {
            'id': i.id,
            'image_url': i.image_url,
            'title': i.title,
            'subtitle': i.subtitle,
            'body': i.body,
            'date': i.date
        }
        post_list.append(obj)


@app.route("/")
def home():
    get_posts()
    (home_image, quote) = get_home()
    return render_template("index.html", posts=post_list, image_url=home_image, quote=quote)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/post/<int:id>")
def render_post(id):
    required_post = None
    for i in post_list:
        if i['id'] == id:
            required_post = i
    return render_template("post.html", post=required_post)


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "GET":
        return render_template("contact.html", sent=False)
    if request.method == "POST":
        name = request.form['name']
        mail = request.form['mail']
        message = request.form['message']
        mail_body = f"{name},{mail},{message}"
        with smtplib.SMTP("smtp.gmail.com", port=587) as conn:
            conn.starttls()
            conn.login(user=MAIL_NAME, password=MAIL_PASSWORD)
            conn.sendmail(MAIL_NAME, MAIL_NAME, mail_body)
        return render_template("contact.html", sent=True)


@app.route('/new_home', methods=['GET', 'POST'])
def set_home():
    if request.method == 'GET':
        return render_template("newhome.html")
    elif request.method == 'POST':
        result = db.session.query(HomeContent).all()
        new_home = HomeContent(id=1,
                               home_image=request.form['home_image'], quote=request.form['quote'])
        if(len(result) == 0):
            db.session.add(new_home)
            db.session.commit()
        else:
            old = HomeContent.query.get(1)
            db.session.delete(old)
            db.session.commit()
            db.session.add(new_home)
            db.session.commit()
        return redirect(url_for('home'))


@app.route("/new_post", methods=['GET', 'POST'])
def new_post():
    if request.method == 'GET':
        return render_template("add.html")
    elif request.method == 'POST':
        new_post = Post(image_url=request.form['image_url'], title=request.form['title'],
                        subtitle=request.form['subtitle'], body=request.form['ckeditor'], date=request.form['date'])
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('home'))


@app.route('/edit_post/<int:id>', methods=['GET', 'POST'])
def edit_post(id):
    if request.method == 'GET':
        required_post = None
        for i in post_list:
            if i['id'] == id:
                required_post = i
        return render_template("edit.html", post=required_post)
    elif request.method == 'POST':
        edited = Post.query.get(id)
        edited.image_url = request.form['image_url']
        edited.title = title = request.form['title']
        edited.subtitle = subtitle = request.form['subtitle']
        edited.body = body = request.form['ckeditor']
        edited.date = date = request.form['date']
        db.session.commit()
        return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)
