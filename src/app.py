import os
from dotenv import load_dotenv
from flask import Flask, render_template

from config.mongodb import mongo
from routes.todo import todo

load_dotenv()

app = Flask(__name__)
app.config['MONGO_URI'] = os.getenv('CONNECTION_STRING')
mongo.init_app(app)

@app.route("/")
def index():
    return render_template("index.html")

app.register_blueprint(todo, url_prefix="/to-do")

if __name__ == "__main__":
    app.run(debug=True)