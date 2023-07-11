from field import FieldStatus
from player import Player
from flask import Flask, render_template

# sql connection goes here

app = Flask(__name__)

# hmm
fields: "list[FieldStatus]" = []
players: "list[Player]" = []

living_players = [] # seems useful, idk

# main public game page
@app.route("/")
def index():
    return render_template('index.html')

# not sure if we do this or just random strings
@app.route("/player")
def player_login():
    return render_template('player_login.html')

# PLAYER PAGES
@app.route("/player/<name>")
def player(name):
    return render_template('player_page.html', player=name)

@app.route("/gm")
def gm():
    return render_template('gm.html')

@app.route("/gm/fields")
def gm_fields():
    return render_template('gm-fields.html', fieldstatus=fields)

@app.route("/gm/players")
def gm_players():
    return render_template('gm-players.html', players=players)

@app.route("/distro")
def distro():
    return render_template('distro.html')

@app.route("/rules")
def distro():
    return render_template('rules.html')

@app.route("/gm/input")
def turn_input():
    return render_template('gm-input.html', players=players, playerlist=living_players)

if __name__ == "__main__":
    app.run(debug=True)