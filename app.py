from field import FieldStatus
from game_run import Game
from player import Player
from flask import Flask, render_template, request, url_for, flash, redirect

# sql connection goes here

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

# hmm
fields: "list[FieldStatus]" = []
players: "list[Player]" = []

living_players = [] # seems useful, idk

g = Game()

# main public game page
@app.route("/")
def index():
    return render_template('index.html')

@app.route("/distro", methods=['GET', 'POST'])
def distro():
    if request.method == 'POST':
        playername = request.form['playername']
        RPname = request.form['RPname']
        skindancer = request.form['alignment']
        socialclass = request.form['socialclass']
        lodging = request.form['lodging']
        musical = request.form['musical']
        ep1 = request.form['ep1']
        fieldep1 = request.form['field1']
        ep2 = request.form['ep2']
        fieldep2 = request.form['field2']
        inventory = request.form['inventory']

        if ep2 == "":
            ep2 = 0

        alignment = True if skindancer == "skindancer" else False

        player_info = {
            "player_name": playername,
            "player_rpname": RPname,
            "is_evil": alignment, # i guess?
            "background": socialclass,
            "inventory": inventory,
            "lodging": lodging,
            "musical_stat": musical,
            "ep1": [int(fieldep1), int(ep1)],
            "ep2": [int(fieldep2), int(ep2)]
        }

        # TODO error check for missing info

        g.add_player(player_info)
        return redirect(url_for('distro'))

    print(g.num_players)
    return render_template('distro.html', g=g)


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
    #print("fields: ", g.fields)
    return render_template('gm-fields.html', fields=g.fields)

@app.route("/gm/players")
def gm_players():
    print(g.players)
    return render_template('gm-players.html', players=g.players)


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