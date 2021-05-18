from flask import Flask, render_template
from post import Post
import requests


posts = requests.get("https://api.npoint.io/e91f0b8b46783302c76c").json()
data = posts['posts']
home_image = posts['home_image']
quote = posts['quote']

post_list = []

for i in data:
    post_instance = Post(i['id'], i['image_url'], i['title'],
                         i['subtitle'], i['body'], i['date'])
    post_list.append(post_instance)

app = Flask("__name__")


@app.route("/")
def home():
    return render_template("index.html", posts=post_list, image_url=home_image, quote=quote)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/post/<int:id>")
def render_post(id):
    required_post = None
    for i in post_list:
        if i.id == id:
            required_post = i
    return render_template("post.html", post=required_post)


if __name__ == "__main__":
    app.run(debug=True)
