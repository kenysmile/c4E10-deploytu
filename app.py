
import os
from flask import *
import mlab
from mongoengine import *
from werkzeug.utils import secure_filename

app = Flask(__name__)

mlab.connect()

app.config["IMG_PATH"] = os.path.join(app.root_path, "static", "images")

class Flower(Document):
    image = StringField()
    title = StringField()
    price = FloatField()

flower1 = Flower(image = "http://media.tiin.vn//archive/images/2017/04/09/152641_4.jpg",
                 title = "Red rose",
                 price = 10000
                 )

flowers = [
    {
        "image": "http://media.tiin.vn//archive/images/2017/04/09/152641_4.jpg",
        "title": "Rainbow",
        "price": 11000
    },
    {
        "image": "https://i.ytimg.com/vi/pOEz5ZlT0kI/sddefault.jpg",
        "title": "Red rose",
        "price": 11000
    },
    {
        "image": "http://kenh14cdn.com/thumb_w/600/2016/1937227-955344701201792-2754518135946920252-n-1453173531333.jpg",
        "title": "violet",
        "price": 12000
    },

]
@app.route('/')
def index():
    # return render_template("index.html",flowers = Flower.objects())
    return "Hi"

@app.route("/images/<image_name>")
def image(image_name):
    return send_from_directory(app.config["IMG_PATH"], image_name)

@app.route('/add_flower', methods=["GET", "POST"])
def add_flower():
    if request.method == "GET": # FORM request
        return render_template("add_flower.html")
    elif request.method == "POST":#User submit form
        #1: Get data(title, image, price)

        form = request.form
        title = form["title"]
        # image = form["image"]
        price = form ["price"]
        image = request.files["images"]

        filename = secure_filename(image.filename)
        image.save(os.path.join(app.config["IMG_PATH"], filename))
        # print(filename)
        # 2: Save data into database
        new_flower = Flower(title = title,
                            image = "/images/{0}".format(filename),
                            price = price)
        new_flower.save()
        return  redirect(url_for("index"))


@app.route("/about:")
def about():
    return "hi, Welcome to C4E. "

@app.route("/users/<username>")
def user(username):
    return"Hello! My name is " + username + ", welcome to page <3"

@app.route("/add/<int:a>/<int:b>")
def add(a,b):
    a = int(a)
    b = int(b)
    return "{0} + {1} = {2}".format(a, b, a + b)

if __name__ == '__main__':
    app.run()
