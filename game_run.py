


import random
from outcome import ProcessLog, Result
from player import Player, PlayerStatic, PlayerStatus, PlayerChoices
from actions import Action, ActionType
from statics import Background, Lodging

PLAYERS: list[Player] = [] 

def add_player(input, id):
    p = PlayerStatic(input.player_name, input.player_rpname, input.is_evil, input.background)
    p.id = id

    inventory = []
    if input.inventory is not None:
        inventory.append(Item.Generate(input.inventory)) # does this work or do you need to do something different bc 2 nahlrout? 
    ps = PlayerStatus(p, input.lodging, input.musical_stat, inventory)

    choice = PlayerChoices(p)

    player = Player(p, ps, choice)

    return player

def start_game(distro_inputs):
    i = 0
    for d in distro_inputs:
        # make Player objects for month 0
        p = add_player(d, i) 
        i += 1
        PLAYERS.append(p)
    return PLAYERS

def add_action(player_id, action_info):
    p = PLAYERS[player_id]

    if not p.status.can_take_actions:
        print("Player cannot take actions!") # log, and better
    elif action_info["action_type"] not in p.status.accessible_abilities:
        # log, not print
        print("Player cannot take this action!")
    # anything else?

    # this bit can probably be much better (get func maybe?)
    t2 = None
    if "target_two" in action_info:
        t2 = action_info["target_two"]
    
    a = Action(p, action_info["action_type"], action_info["target"], t2)

    p.take_action(a)



def update_choices(new_choices):
    c = PLAYERS[new_choices["player"]]

    if new_choices["imre_next"]: c.imre_next = True
    if new_choices["add_action"]:
        add_action(c.id, new_choices["add_action"])
    # what about updating an action? do we just clear all actions before this func? 
    
    # todo other choices


def process_turn(PLAYERS, gm_input, month):
    process = ProcessLog(month)
    results = Result(month) 

    ACTION_LIST: list[Action] = []
    sane_players: list[int] = [] # just ids 
    living_players: list[int] = [] # just ids 

    # update field statuses to new month (?)

    for p in PLAYERS:
        # add processing object for this turn
        proc = p.PlayerProcessing(p, month)

        # make sane_players and living_players lists
        if p.status.is_sane:
            sane_players.append(p.id)
        if p.status.is_alive:
            living_players.append(p.id)
        # maybe other lists? imre? 

        # add actions to actions_list
        ACTION_LIST.append(p.choices.actions)


        # add next_status for next turn (to overwrite status at end of turn processing)
        p.next_status = p.status.deepcopy()
        # todo: change things like can_take_actions back where needed

    if month % 3 == 0:
        # for p in sane_players, probs
        
        # GIVE STIPENDS
        for pid in sane_players:
            p = PLAYERS[pid]
            p.next_status.money += p.status.stipend

        # DO TUITION STUFF
        # remember to check for masters, social class
            if p.choices.enroll_next and not p.status.is_expelled:
                if not p.status.is_enrolled:
                    tuition = p.status.tuition # from last enrollment
                else:
                    tuition = p.calculate_tuition() # TODO
                
                if p.next_status.money >= tuition:
                    # todo check for the preferences thingy
                    p.next_status.money -= tuition
                    p.next_status.is_enrolled = True
                else:
                    p.next_status.is_enrolled = False


        # DO LODGING STUFF
        # remember to check price for masters, ruh
            # ordering on these?
            lodging_price = p.choices.next_lodging.price
            if p.info.social_class == Background.Ruh:
                lodging_price /= 2
            
            if p.status.master_of is not None:
                lodging_price *= 0.75
            
            if p.next_status.money >= lodging_price:
                p.next_status.money -= lodging_price
                p.next_status.lodging = p.choices.next_lodging
            else:
                # WHATEVER, TODO
                # LOG
                pass


    # set up passive roleblocks
    for pid in sane_players:
        p = PLAYERS[pid]
        
        roll = random.randrange(0,100)

        # HOMECOMING
        # add this to results
        if p.info.social_class == Background.Vint and roll < 25:
            p.processing.is_blocked = True
            p.processing.can_be_targeted = False
        elif p.info.social_class == Background.Aturan and roll < 10:
            p.processing.is_blocked = True
            p.processing.can_be_targeted = False
        
        if p.next_status.lodging == Lodging.Ankers and random.randrange(0,100) < 15:
            action_blocked = random.choice(p.choice.actions)
            action_blocked.blocked = True
            action_blocked.block_reasoning += "Ankers"
        
    # TODO
    # maybe split action_list into categories first? 
    # pass in logger, too? or just make a Turn class tbh
    process_meta_actions(PLAYERS, ACTION_LIST)

    process_standard_actions(PLAYERS, ACTION_LIST)

    process_mechanics(PLAYERS, ACTION_LIST)

    process_offensive_actions(PLAYERS, ACTION_LIST)

    # output results and stuff




def process_meta_actions(players, actions):
    # TODO
    return # actions? maybe? 

def process_standard_actions(players, actions):
    #TODO 
    return

def process_mechanics(players, actions):
    #TODO
    # horns

    # elevations

    # offset IP

    # file EP

    # # breakout roll
    return

def process_offensive_actions(players, actions):
    #TODO



    return
        
    
