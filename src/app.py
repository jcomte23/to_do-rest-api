from flask import Flask, render_template

from routes.todo import todo


app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

app.register_blueprint(todo, url_prefix="/to-do")

if __name__ == "__main__":
    app.run(debug=True)