from flask import Flask, render_template
import eval

app = Flask(__name__)

@app.route("/")
def main():

    return render_template("index.html", title="Test Falsk")

@app.route("/output")
def output():
    eval.run()
    return render_template("index.html", title="Test Falsk")

if __name__ == "__main__":
    app.run(debug=True, port=5000)