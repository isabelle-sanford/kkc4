from field import FieldStatus
from game_run import Game
from player import Player
from flask import Flask, render_template

# sql connection goes here

app = Flask(__name__)

# hmm
fields: "list[FieldStatus]" = []
players: "list[Player]" = []

living_players = [] # seems useful, idk

g = Game()

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
    # need to actually get PLAYER object
    return render_template('player_page.html', player=name)

@app.route("/gm")
def gm():
    return render_template('gm.html')

@app.route("/gm/fields")
def gm_fields():
    return render_template('gm-fields.html', fields=g.fields)

@app.route("/gm/players")
def gm_players():
    return render_template('gm-players.html', players=players)

@app.route("/distro")
def distro():
    return render_template('distro.html', g=g)

@app.route("/rules-game-basics")
def rules_game_basics():
    return render_template('rules-game-basics.html')

@app.route("/rules-uni-basics")
def rules_uni_basics():
    return render_template('rules-university-basics.html')

@app.route("/rules-arcanum-basics")
def rules_arcanum_basics():
    return render_template('rules-arcanum-basics.html')

@app.route("/rules-arcanum-fields")
def rules_arcanum_fields():
    return render_template('rules-arcanum-fields.html')

@app.route("/rules-imre")
def rules_imre():
    return render_template('rules-imre.html')




@app.route("/gm/input")
def turn_input():
    return render_template('gm-input.html', players=g.players)

if __name__ == "__main__":
    app.run(debug=True)