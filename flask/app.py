from flask import Flask, render_template

# sql connection goes here

app = Flask(__name__)

# main public game page
@app.route("/")
def index():
    return render_template('index.html')

@app.route("/player")
def player_login():
    return render_template('player_login.html')

# PLAYER PAGES
@app.route("/player/p1")
def player_p1():
    return render_template('player_page.html')

@app.route("/gm")
def gm():
    return render_template('gm.html')

@app.route("/distro")
def distro():
    return render_template('distro.html')


if __name__ == "__main__":
    app.run(debug=True)