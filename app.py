
from statics import FIELDNAMES, RANKNAMES
from field import ActionPeriod, FieldStatus
from game_run import Game, Turn
from items import ItemType
from player import Player
from flask import Flask, render_template, request, url_for, flash, redirect
from actioninfo import ActionType
import pickle
from custom_players import PLAYERLIST

# sql connection goes here

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

# hmm
fields: "list[FieldStatus]" = []
players: "list[Player]" = []

living_players = [] # seems useful, idk

curr_input = {}

g: Game = None
with open('t5withchoices.pickle', 'rb') as f:
    g = pickle.load(f)

with open('gamenow.pickle', 'wb') as f:
    pickle.dump(g, f)


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

        inventory = request.form['inventory']



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
@app.route("/player/<name>", methods=['GET', 'POST'])
def player(name):
    with open('gamenow.pickle', 'rb') as f:
        curr_game = pickle.load(f)
    
    if request.method == 'POST':
        print(request.form)
        curr_game.update_player_choices(request.form, curr_game.player_list[name])

        flash('Success!')
        #return redirect(url_for('player'))
    # todo POST method for choice submissions
    player = curr_game.player_list[name]
    action_periods={i:a.name for i, a in enumerate(player.status.action_periods)}
    #print("action periods: ", action_periods)
    return render_template('player_page.html', player=player, playerlist=curr_game.players, actions=ActionType, items=ItemType, fieldnames=FIELDNAMES, ranknames=RANKNAMES, action_periods=action_periods)

@app.route("/gm/start")
def start_game():
    g.start_game()
    print(g.players)
    # does this stay like this once start_game is done? 
    return render_template('gm-start.html')

@app.route("/gm/fields")
def gm_fields():
    #print("fields: ", g.fields)
    return render_template('gm-fields.html', fields=g.fields)

@app.route("/gm/players")
def gm_players():
    print(g.players)
    with open('gamenow.pickle', 'rb') as f:
        curr_game = pickle.load(f)
    return render_template('gm-players.html', players=curr_game.players)

@app.route("/gm/imre")
def gm_imre():
    return render_template('gm-imre.html', imre_players=[g.curr_turn.players[id] for id in g.curr_turn.imre_players]) # TODO

@app.route("/gm/playerchoices")
def playerchoices():
    with open('gamenow.pickle', 'rb') as f:
        curr_game = pickle.load(f)
    return render_template('gm-choices.html', g=curr_game) # TODO


@app.route("/gm/processturn")
def process_turn():
    with open('t5wchoices.pickle', 'rb') as f:
        curr_game = pickle.load(f)

        print(curr_game.curr_gm_input)
        # TODO gm inputs for RP etc
        process_log = curr_game.new_turn()


    return render_template('gm-processing.html', game=curr_game, actions=curr_game.curr_turn.actions, log=process_log)
# TODO: page post-processing to reset 'g' to new thingy

@app.route("/rules/game-basics")
def rules_game_basics():
    return render_template('rules-game-basics.html')

@app.route("/rules/uni-basics")
def rules_uni_basics():
    return render_template('rules-university-basics.html')

@app.route("/rules/arcanum-basics")
def rules_arcanum_basics():
    return render_template('rules-arcanum-basics.html')

@app.route("/rules/arcanum-fields")
def rules_arcanum_fields():
    return render_template('rules-arcanum-fields.html')

@app.route("/rules/imre")
def rules_imre():
    return render_template('rules-imre.html')


@app.route("/gm/input", methods=['GET', 'POST'])
def turn_input():
    with open('gamenow.pickle', 'rb') as f:
        curr_game = pickle.load(f)
    if request.method == 'POST':
        print(request.form)
        curr_input = request.form

        complaints = [[] for i in range(len(curr_game.players))] # ???
        PMs = [0 for i in range(len(curr_game.players))]
        posts = [0 for i in range(len(curr_game.players))]
        qrp = [0 for i in range(len(curr_game.players))]
        qpostwc = [0 for i in range(len(curr_game.players))]
        for p in curr_game.players:
            s = "p" + str(p.id)
            #print("looking for complaints from player ", p.id)
            if curr_input["complaint0p" + str(p.id)] != "None":
                #print("player ", str(p.id), " complained on player ", curr_input["complaint0p"+str(p.id)])
                complaints[p.id].append(curr_input["complaint0p" + str(p.id)])
            if curr_input["complaint1p" + str(p.id)] != "None":
                complaints[p.id].append(curr_input["complaint1p" + str(p.id)])
            if curr_input["complaint2p" + str(p.id)] != "None":
                complaints[p.id].append(curr_input["complaint2p" + str(p.id)])
            if curr_input["complaint3p" + str(p.id)] != "None":
                complaints[p.id].append(curr_input["complaint3p" + str(p.id)])
            p.choices.complaints = [int(i) for i in complaints[p.id]]
            #print("got complaints: ", complaints[p.id])

            if curr_input[s + "PostCount"] != "None":
                posts[p.id] = curr_input[s + "PostCount"]
            if curr_input[s + "PMInput"] != "None":
                PMs[p.id] = curr_input[s + "PMInput"]
            if curr_input[s + "QRP"] != "None":
                qrp[p.id] = curr_input[s + "QRP"]
            if curr_input[s + "QPostWC"] != "None":
                qpostwc[p.id] = curr_input[s + "QPostWC"]




        

        
        curr_game.curr_gm_input = {}
        curr_game.curr_gm_input["complaints"] = complaints
        curr_game.curr_gm_input["posts"] = posts
        curr_game.curr_gm_input["PMs"] = PMs
        curr_game.curr_gm_input["QRP"] = qrp
        curr_game.curr_gm_input["qpostwc"] = qpostwc
        
                
        print(complaints)
        # todo pickle/load
        
        with open('gamenow.pickle', 'wb') as f:
            pickle.dump(curr_game, f)
    return render_template('gm-input.html', players=curr_game.players, previnput=curr_game.curr_gm_input)

if __name__ == "__main__":
    app.run(debug=True)