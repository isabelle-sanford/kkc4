
from player import PlayerStatic, PlayerStatus, PlayerChoices
from statics import Background, Lodging
from field import FieldName
from items import ItemType, Item
from actions import ActionType, Action

# Player Initialization

# todo get inputs from html page 

input0 = {
    "player_name": "Kas",
    "player_rpname": "Khas",
    "is_evil": False,
    "background": Background.Vint,
    "lodging": Lodging.HorseAndFour,
    "musical_stat": 12,
    "ep1": (FieldName.RHETORICLOGIC, 7),
    "ep2": None,
    "inventory": None
}

input1 = {
    "player_name": "El",
    "player_rpname": "Elle",
    "is_evil": True,
    "background": Background.Ruh,
    "lodging": Lodging.Ankers,
    "musical_stat": 8,
    "ep1": (FieldName.RHETORICLOGIC, 1),
    "ep2": (FieldName.LINGUISTICS, 1),
    "inventory": None
}

input2 = {
    "player_name": "Haelbarde",
    "player_rpname": "Halle",
    "is_evil": True,
    "background": Background.Aturan,
    "lodging": Lodging.WindyTower,
    "musical_stat": 5,
    "ep1": (FieldName.NAMING, 2),
    "ep2": None,
    "inventory": None
}

input3 = {
    "player_name": "Wilson",
    "player_rpname": "Will",
    "is_evil": False,
    "background": Background.Ceald,
    "lodging": Lodging.KingsDrab,
    "musical_stat": 7,
    "ep1": (FieldName.ALCHEMY, 1),
    "ep2": (FieldName.ARTIFICERY, 1),
    "inventory": ItemType.NAHLROUT
}

input4 = {
    "player_name": "Devotary",
    "player_rpname": "devdev",
    "is_evil": False,
    "background": Background.Yll,
    "lodging": Lodging.GoldenPony,
    "musical_stat": 8,
    "ep1": (FieldName.SYMPATHY, 1),
    "ep2": (FieldName.PHYSICKING, 1),
    "inventory": ItemType.BLOODLESS
}

INPUTS = [input0, input1, input2, input3, input4]
PLAYERSTATICS = []
PLAYERSTATUSES = []
# 0 Kas, 1 El, 2 Hael, 3 Wilson, 4 Devo

for i in INPUTS:
    p = PlayerStatic(i.player_name, i.player_rpname, i.is_evil, i.background)
    PLAYERSTATICS.append(p)

    inventory = []
    if i.inventory is not None:
        inventory.append(Item.Generate(i.inventory)) # does this work or do you need to do something different bc 2 nahlrout? 
    ps = PlayerStatus(p, i.lodging, i.musical_stat, inventory)

    ps.EP.values[i.ep1[0]] += i.ep1[1]
    if i.ep2 is not None:
        ps.EP.values[i.ep2[0]] += i.ep2[1]
    
    PLAYERSTATUSES.append(ps)

# todo create player webpages, GM pages, etc 

# Month 1 - players make choices, complaints

# create choice objects
CHOICESM1 = []
for player in PLAYERSTATICS:
    choice = PlayerChoices(player)
    CHOICESM1.append(choice)

# todo get choices from player webpages 

choices0 = {
    "player": 0, # id, for now just list index 
    "imre_next": False,
    #"complaints": [3, 3],
    "actions": None, # or []?
    "EP": [FieldName.RHETORICLOGIC, FieldName.RHETORICLOGIC, FieldName.RHETORICLOGIC, FieldName.RHETORICLOGIC, FieldName.RHETORICLOGIC] # todo check appropriate amt somewhere
}

choices1 = {
    "player": 1,
    "imre_next": False,
    #"complaints": [3, 2],
    "actions": [{
        "action_type": ActionType.Sabotage,
        "target": 4, # is index ok even tho ref varies?
        "target2": None
    }],
    "EP": [FieldName.ALCHEMY, FieldName.ALCHEMY, FieldName.SYMPATHY, FieldName.SYMPATHY, FieldName.ALCHEMY]
}

choices2 = {
    "player": 2,
    "imre_next": True,
    #"complaints": [0, 3],
    "actions": None,
    "EP": [FieldName.LINGUISTICS, FieldName.LINGUISTICS, FieldName.LINGUISTICS, FieldName.LINGUISTICS, FieldName.LINGUISTICS]
}

choices3 = {
    "player": 3,
    "imre_next": True,
    #"complaints": [2, 2],
    "actions": None,
    "EP": [FieldName.NAMING, FieldName.NAMING, FieldName.NAMING, FieldName.NAMING, FieldName.NAMING]
}

choices4 = {
    "player": 4,
    "imre_next": False,
    #"complaints": [0, 2],
    "actions": None,
    "EP": [FieldName.ALCHEMY, FieldName.ALCHEMY, FieldName.ALCHEMY, FieldName.ALCHEMY, FieldName.ALCHEMY]
}

CHOICESM1INPUT = [choices0, choices1, choices2, choices3, choices4]


# fill in choice objects
for c in CHOICESM1INPUT:
    curr = CHOICESM1[c.player]
    curr.imre_next = c.imre_next 
    curr.EP_filed = c.EP

    if c.actions is not None:
        for a in c.actions:
            act = Action("name??", c.player, a.action_type, a.target, a.target2)
            curr.actions.append(act)

# todo get complaints

complaints = [
    [3,3],
    [3,2],
    [0,3],
    [2,2],
    [0,2]
]

# add complaints into choices
for voter in range(len(complaints)): # i guess
    choice = CHOICESM1[voter]
    voter.complaints = complaints[voter]



