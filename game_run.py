import copy
import random
from field import FieldStatus, FIELDS
from horns import Horns
from imre import Apothecary, BlackMarket
from items import Item, ItemType
from outcome import ProcessLog, Result
from player import Player, PlayerProcessing, PlayerStatic, PlayerStatus, PlayerChoices, Tuition
from actioninfo import Target
from actions import Action, ActionType, ActionCategory
from statics import FIELDNAMES, NONIMRE_LODGINGS, Background, FieldName, Lodging, Rank, BACKGROUNDS, LODGINGS

import pickle

# idk 
#PLAYERS: "list[Player]" = [] 

distro_shortcut = [
    {
        "player_name": "Kas",
        "player_rpname": "",
        "is_evil": False,
        "background": Background.Yll,
        "inventory": None,
        "lodging": Lodging.Ankers, # idk
        "musical_stat": 1,
        "ep1": [FieldName.RHETORICLOGIC, 3]
     },
    {
        "player_name": "El",
        "player_rpname": "",
        "is_evil": False,
        "background": Background.Ceald,
        "inventory": None,
        "lodging": Lodging.Ankers, # idk
        "musical_stat": 1,
        "ep1": [FieldName.LINGUISTICS, 2]
     },
    {
        "player_name": "Hael",
        "player_rpname": "",
        "is_evil": True,
        "background": Background.Ruh,
        "inventory": "1nahlrout",
        "lodging": Lodging.KingsDrab, # idk
        "musical_stat": 1,
        "ep1": [FieldName.ALCHEMY, 2]
     }
]

class Game:

    def __init__(self, shortcut_distro = False):


        self.num_players = 0
        self.players: list[Player] = []
        self.turns: list[Turn] = []
        self.curr_turn: Turn = None
        # this is where field status init should go

        self.apothecary = Apothecary()
        self.blackmarket = BlackMarket()
        self.fields = FIELDS
        self.player_list = {}
        self.month = 0

        self.curr_gm_input = {}

        if shortcut_distro:
            for p in distro_shortcut:
                self.add_player(p)
            
            self.start_game()

        


    def add_player(self, input):
        #background = BACKGROUNDS[input["background"]]
        p = PlayerStatic(input["player_name"], input["player_rpname"], input["is_evil"], Background(int(input["background"])))
        p.id = self.num_players

        inventory = []
        if input["inventory"] is not None: # is it ever? 
            match input["inventory"]:
                case "1nahlrout":
                    inventory.append(Item.Generate(ItemType.NAHLROUT))
                case "2nahlrout":
                    inventory.append(Item.Generate(ItemType.NAHLROUT))
                    inventory.append(Item.Generate(ItemType.NAHLROUT))
                case "ward":
                    inventory.append(Item.Generate(ItemType.WARD))
                case "tenaculum":
                    inventory.append(Item.Generate(ItemType.TENACULUM))
                case "bloodless":
                    inventory.append(Item.Generate(ItemType.BLOODLESS))
                case "gram":
                    inventory.append(Item.Generate(ItemType.GRAM))
                case "bonetar":
                    inventory.append(Item.Generate(ItemType.BONETAR))
        #lodging = LODGINGS[input["lodging"]]
        ps = PlayerStatus.distro_init(p, input["lodging"], input["musical_stat"], inventory)

        print(ps.inventory)

        player = Player(p, ps)

        if input["ep1"] is not None:
            ep_field = FIELDS[input["ep1"][0]].name
            ep_num = input["ep1"][1]
            player.assign_EP(ep_field, ep_num)
            FIELDS[input["ep1"][0]].add_EP(player, input["ep1"][1])



        self.players.append(player)

        self.player_list[p.name] = player

        self.num_players += 1

        return player

    def start_game(self):
        # for d in distro_inputs:
        #     self.add_player(d) 

        self.curr_turn = Turn({}, 0, self)
        
        with open('gamestart.pickle', 'wb') as f:
            pickle.dump(self, f)
        
        with open('t1players.pickle', 'wb') as f:
            pickle.dump(self.players, f)
        
        with open('gamenow.pickle', 'wb') as f:
            pickle.dump(self, f)


    # ...should this be in Turn? not sure
    def add_action(self, player_id, action):
        p = self.players[player_id]

        if not p.status.can_take_actions:
            print("Player cannot take actions!") # log, and better
        elif action["action_type"].info not in p.status.accessible_abilities:
            # log, not print
            print(f"Player {p.name} cannot take action {action}!")
        # anything else?

        # this bit can probably be much better (get func maybe?)
        t2 = None
        if "target_two" in action:
            t2 = action["target_two"]
        
        a = Action(p, action["action_type"], action["target"], t2)

        p.take_action(a)

    def update_player_choices(self, choice, player):
        c = player

        # term start things
        if "lodging" in choice:
            c.choices.next_lodging = int(choice["lodging"])


        if "imre_next" in choice: c.choices.imre_next = True

        for i in range(6):
            s = "field" + str(i)
            if s in choice and choice[s] is not None:
                print("filing EP #" + str(i) + " in field " + choice[s])
                if choice[s] != "None":
                    c.choices.filing_EP[i] = int(choice[s])

        for i in range(4):
            if ("action" + str(i)) in choice:
                a_info = choice["action"+str(i)]
                # TODO

                self.add_action(c.id, a_info)
        # what about updating an action? do we just clear all actions before this func? 
        
        # todo other choices
            # imre stuff
        
        with open('gamenow.pickle', 'wb') as f:
            pickle.dump(self, f)
    # ! TODO
    # PICKLE THIS
    def update_choices(self, new_choices):
        # erase all prev choices? (for just the player(s) in the list?)
        for choice in new_choices:
            c = self.players[choice["player"]]

            if choice["imre_next"]: c.imre_next = True
            if choice["EP"]:
                # check here?
                c.choices.filing_EP = choice["EP"]
                    
            if choice["actions"]:
                for a in choice["actions"]:

                    self.add_action(c.id, a)
            # what about updating an action? do we just clear all actions before this func? 
            
            # todo other choices
                # imre stuff

    def new_turn(self):


        self.turns.append(self.curr_turn)
        self.month += 1
        self.curr_turn = Turn(self.curr_gm_input, self.month, self)


        self.curr_turn.PROCESS_TURN()

        # TODO: add gm processing manually here

        m = 'turn' + str(self.month) + '.pickle' 

        with open(m, 'wb') as f:
            pickle.dump(self.curr_turn, f)

        with open('gamenow.pickle', 'wb') as f:
            pickle.dump(self, f)
        
        return self.curr_turn.log



# could put this inside game, idk
class Turn:

    def __init__(self, gm_input, month: int, game: Game):
        self.players = game.players
        self.gm_input = gm_input
        self.month = month
        self.game = game

        self.log = ProcessLog(month)

        self.actions: list[Action] = []
        self.offensive_actions: list[Action] = []

        self.fields = game.fields # hmm, or just directly access game.fields? 
        self.apothecary: Apothecary = game.apothecary # same here
        self.blackmarket: BlackMarket = game.blackmarket

        self.sane_players: list[int] = [] # just ids 
        self.living_players: list[int] = [] # just ids 
        self.imre_players: list[int] = [] # just ids

        for p in self.players:
            if p.status.is_alive:
                self.living_players.append(p.id)

                if p.status.is_sane:
                    self.sane_players.append(p.id)
            
            for a in p.choices.actions:

                self.actions.append(a)
            
            if p.choices.imre_next: # is this good?
                self.imre_players.append(p.id)

            # TUITION FROM CHOICES
            if len(p.choices.filing_EP) > 0:
                p.tuition.times_filed_EP += 1
            # todo imre tuition things (once imre is done)

            

        # other lists? imre? 

        if "complaints" in gm_input and gm_input["complaints"] is not None:
            for v in range(len(gm_input["complaints"])):
                # accessing id here is a little dubious but ok
                self.players[v].choices.complaints = [int(i) for i in gm_input["complaints"][v]] # might need to intify
                if len(gm_input["complaints"][v]) > 0:
                    self.players[v].tuition.times_filed_complaints += 1
        
        # TODO: other tuition stuff from GM input
            # public apology
            # num posts
            # num PMs
            # num quality rp / game-related



    
    def start_term(self):

        self.log.add_section("NEW TERM", "Starting new term.")

        # pay off interest to devi / giles (any further payment is in process_imre)
        self.log.log("Paying off interests to Giles / Devi...")
        # also maybe do this inside player, not here?
        for pid in self.sane_players:
            p = self.players[pid] # idk why I'm even using pid at this point

            if p.status.IMRE_INFO["DEVI_amt_owed"] > 0: # ? and not yet defaulted?
                paying = p.choices.pay_devi 
                owed = p.status.IMRE_INFO["DEVI_amt_owed"]
                arit_reduction = p.levels_in(FieldName.ARITHMETICS) * 10 + 10
                interest_owed = owed * 0.3 * (1 - arit_reduction / 100)

                p.status.IMRE_INFO["DEVI_amt_owed"] += interest_owed

                if paying < interest_owed:
                    # DEFAULT
                    p.IMRE_INFO["DEVI_defaulted"] = True

                    mommet = Item.Generate(ItemType.MOMMET, 1, p)
                    mommet.uses = (owed + interest_owed) // 1

                    self.blackmarket.mommets.append(mommet) # todo need to add its price

                    p.processing.player_message.append("You did not pay Devi enough to cover your interest! You have now defaulted, and she has put a mommet on the Black Market with your name on it.")
                    self.log.log(f"{p.name} defaulted on their loan to Devi.")
                else:
                    p.status.IMRE_INFO["DEVI_amt_owed"] -= interest_owed
                    p.choices.pay_devi -= interest_owed # rest of payment happens later
                    p.processing.player_message.append("You successfully paid off your interest owed to Devi.")

            if p.status.IMRE_INFO["GILES_amt_owed"] > 0:
                paying = p.choices.pay_giles
                owed = p.status.IMRE_INFO["GILES_amt_owed"]
                arit_reduction = p.levels_in(FieldName.ARITHMETICS) * 10 + 10
                interest_owed = owed * 0.15 * (1 - arit_reduction / 100)

                p.status.IMRE_INFO["GILES_amt_owed"] += interest_owed

                if paying < interest_owed:
                    # DEFAULT
                    p.status.IMRE_INFO["GILES_defaulted"] = True
                    # todo blacklist from grey man
                    p.processing.player_message.append("You didn't pay Giles enough to cover your interest! You have now defaulted, and are no longer welcome at the Grey Man.")
                    self.log.log(f"{p.name} defaulted on their loan to Giles.")

                else:
                    p.status.IMRE_INFO["GILES_amt_owed"] -= interest_owed
                    p.choices.pay_giles -= interest_owed # rest of payment happens later
                    p.processing.player_message.append("You successfully paid off your interest owed to Giles.")


        
        
        # GIVE STIPENDS
        for pid in self.sane_players:
            p = self.players[pid]
            # could use p.increase_money() instead ig
            p.status.money += p.initial_status.stipend

            if p.status.has_talent_pipes: # todo make sure this works
                p.status.money += 10


            # DO TUITION STUFF
            # remember to check for masters, social class

            # if currently enrolled, calculate tuition for next term
            # (otherwise keep the value of whatever the previous one was)
            if p.status.is_enrolled and not p.status.is_expelled:
                tuition = p.tuition.calculate_tuition(p.status) 
                p.status.current_tuition = tuition
                p.tuition = Tuition(pid) # new obj for next term

            # if enrolling next term, get tuition and try to pay it
            if p.choices.enroll_next and not p.status.is_expelled:
                tuition = p.status.current_tuition 
                
                if p.status.money >= tuition:
                    # todo check for the preferences thingy
                    p.status.money -= tuition # should really use the reduce_money() func
                    p.status.is_enrolled = True
                else:
                    p.status.is_enrolled = False
                    self.log.log(f"Player {p.name} could not afford their tuition of {tuition} and as such is not enrolling this turn.")


            if p.choices.next_lodging == Lodging.GreyMan and p.status.IMRE_INFO["GILES_defaulted"]:
                p.processing.player_message.append("You tried to stay at the Grey Man, but defaulted on your debt to Giles, so are unable to stay there! You were placed at the King's Drab instead.")
                p.choices.next_lodging = Lodging.KingsDrab


        # DO LODGING STUFF
        # remember to check price for masters, ruh
            # ordering on these?
            lodging_price = p.calc_lodging(p.choices.next_lodging)

            if p.status.money >= lodging_price:
                p.status.money -= lodging_price
                p.status.lodging = p.choices.next_lodging
            else:
                self.log.log(f"Player {p.name} could not afford to stay at {p.choices.next_lodging} after tuition.")
                # TODO imre lodgings
                if p.choices.next_lodging == Lodging.PearlOfImre:
                    new_lodging = Lodging.GreyMan
                    new_lodging_price = p.calc_lodging(Lodging.GreyMan)


                    if p.status.money >= new_lodging_price:
                        p.status.lodging = Lodging.GreyMan
                        p.status.money -= new_lodging_price
                
                if p.choices.next_lodging == Lodging.GreyMan:
                    i = NONIMRE_LODGINGS.index(Lodging.GoldenPony)
                else: 
                # this isn't hacky at all shhh
                    i = NONIMRE_LODGINGS.index(p.choices.next_lodging)
                while p.status.money <= lodging_price:
                    i -= 1
                    new_lodging = NONIMRE_LODGINGS[i]
                    lodging_price = p.calc_lodging(new_lodging)
                
                p.status.money -= lodging_price
                p.status.lodging = new_lodging
                self.log.log(f"They have been moved to {new_lodging}.")
            
            if p.initial_status.lodging == Lodging.WindyTower:
                p.status.available_EP -= 1

            if p.status.lodging == Lodging.WindyTower:
                p.status.available_EP += 1
                # what if master / expelled / whatevs 
            elif p.status.lodging == Lodging.GreyMan or p.status.lodging == Lodging.PearlOfImre:
                p.status.in_Imre = True
            

        # todo make sure expelled students not in mews?


        self.log.log("Stipends, tuition, & lodging processed.")


    

    def preprocess_tenaculum(self):
        for a in self.actions:
            if a.type == ActionType.UseTenaculumAction:
                awry = False
                if a.level == 1: #! LEVEL IS OF USER
                    roll = random.randint(1,100)
                    if roll <= 20:
                        awry = True

                if a.level == 2:
                    roll = random.randint(1,100)
                    if roll <= 10:
                        awry = True
                # DO STUFF
                pass

            if a.type == ActionType.UseTenaculumItem:
                # DO STUFF
                pass

    def preprocessing(self):
        self.log.log("Now preprocessing stuff like whether people being targeted actually can be targeted, and lists of who ppl are targeted by for things like pickpocketing.")

        for a in self.actions:
             # check that target(s) can be targeted 
            if a.type.info.target1 == Target.PLAYER:
                if a.target and not a.target.status.can_be_targeted:
                    a.successful = False 
            if a.type.info.target2 == Target.PLAYER:
                if a.target_two and not a.target_two.status.can_be_targeted:
                    a.successful = False 

            # check that target is valid if action taker is expelled
            # (i.e. target is expelled or in imre)
            if a.player.status.is_expelled:
                if a.type.info.target1 == Target.PLAYER and a.target:
                    if (not a.target.status.is_expelled) and (not a.target.status.in_Imre):
                        a.successful = False 
                if a.type.info.target2 == Target.PLAYER and a.target_two:
                    if (not a.target_two.status.is_expelled) and (not a.target_two.status.in_Imre):
                        a.successful = False 

            # for item steal/destroy, roll for specifics on what happens
            # TODO make this just 'pending' to account for RB cycles
            # sighhhhh
            if a.type == ActionType.UseThievesLamp and a.successful:
                if len(a.target.status.inventory) > 0:
                    if a.target.holds_item(ItemType.BODYGUARD):
                        continue # i guess????
                    else:
                        item_count = len(self.target.status.inventory)
                        items_stolen = []
                        if self.target.holds_item(ItemType.TALENTPIPES):
                            item_count -= 1


                        if item_count == 1:
                            stolen = self.target.get_stolen_from()
                            items_stolen.append(stolen)

                        # this is a little iffy
                        for i in range(item_count // 2):
                            stolen = self.target.get_stolen_from()
                            items_stolen.append(stolen)
                a.info = items_stolen # i guess

            if a.type == ActionType.UseTenaculumItem and a.successful:
                awry = False
                if a.level == 1:
                    roll = random.randint(1,100)
                    if roll <= 20:
                        awry = True

                if a.level == 2:
                    roll = random.randint(1,100)
                    if roll <= 10:
                        awry = True
                
                if awry:
                    # TODO
                    pass # sigh

                destroyed = None

                if a.target_two:
                    if a.target.holds_item(a.target_two):
                        destroyed = self.target.get_items(a.target_two)[0]
                        a.info = destroyed # idk

                
                if destroyed is None:
                    # item unspecified or not specified correctly
                    destroyed = self.target.get_stolen_from() # hm
                    a.info = destroyed



            if a.type == ActionType.UseTenaculumAction and a.successful:
                awry = False
                if a.level == 1:
                    roll = random.randint(1,100)
                    if roll <= 20:
                        awry = True

                if a.level == 2:
                    roll = random.randint(1,100)
                    if roll <= 10:
                        awry = True
                if awry:
                    # goes awry! 
                    change = random.randint(1,4)

                    # todo: no talent pipes
                    target_items = self.target.status.inventory
                    self_items = self.player.status.inventory
                    target_actions = self.target.choices.actions
                    self_actions = self.player.choices.actions

                    options = ["Destroy Target's Item", "Destroy Own Item", "Block Target's Action", "Block Self Action"]

                    if len(target_items) == 0:
                        options.remove("Destroy Target's Item")
                    # ? can tenaculum destroy itself?
                    if len(target_actions) == 0: 
                        options.remove("Block Target's Action")
                        # what if only 1 action, and it's the specified one?
                    if len(self_actions) == 1:
                        options.remove("Block Self Action")
                    
                    choice = random.choice(options)
                        
            self.log.log("Block processing partly done and messy. Sigh.")
        return


    def apply_valid_blocks(self, block_list: "list[Action]", count = 0, process_block_cycles = False):
        state_changed = False

        # Notify all actions of intent to be blocked.
        if not process_block_cycles:
            for a in block_list:
                a.perform(notify_only = True)
        
        to_remove: list[Action] = []
        for action in block_list:
            # Ignoring players who have been blocked, if the player isn't being blocked, apply their blocks.
            if not(action.blocked) or (action.in_block_cycle):
                # Only apply block if not being blocked by something.
                if (len(action.blocked_by) == 0 and not process_block_cycles) or (action.in_block_cycle):
                    action_result = {"success": False, "state_changed": False, "process_block_cycles": process_block_cycles}
                    action.perform(result=action_result)
                    to_remove.append(action)
                    if action_result["state_changed"]:
                        state_changed = True
        
        for action in block_list:
            if action.blocked and action not in to_remove:
                action.clear_block_notification()
                to_remove.append(action)

        # Dunno if this goes before or after the block notification
        for action in to_remove:
            if (action.blocked):
                action.perform()
            block_list.remove(action)

        for a in block_list:
            if a.blocked == False:
                a.clear_block_notification()
        
        if state_changed:
            self.apply_valid_blocks(block_list, count + 1)


    def process_blocks(self, action_list: "list[Action]"):
        # Apply all mommets that definitely are not in loops
        self.apply_valid_blocks(action_list)

        # Identify all loops
        for a in action_list:
            a.perform(notify_only = True)
        for a in action_list:
            a.identify_block_cycle([])

        # Block all loops
        self.apply_valid_blocks(action_list, process_block_cycles=True)

        # Apply any remaining blocks
        self.apply_valid_blocks(action_list)

        print("\n")
        for p in self.players:
            for a in p.choices.actions:
                print(f"{a.player.info.name}'s {a.type} action is blocked = {a.blocked}")

    def preprocessing_standard(self):

        for a in self.actions: 
            # if failed, do whatever to log it

            if a.successful:
                # todo: fix for actions that can but don't require a player target
                # add actions to targeted_by lists for player targets
                if a.type.info.target1 == Target.PLAYER:
                    a.target.processing.targeted_by.append(a)
                if a.type.info.target2 == Target.PLAYER:
                    a.target_two.processing.targeted_by.append(a)     

                # could split by category here but just do at init?            

                a.player.processing.player_message.append(f"Your action to use {a.type.info.name} on {a.target} {f'and {a.target_two} ' if a.target_two else ''} succeeded.") # more here? idk
            
            else:
                a.player.processing.player_message.append(f"Your action to use {a.type.info.name} on {a.target} {f'and {a.target_two} ' if a.target_two else ''} failed.")



    def process_standard_actions(self):
        # todo: check streets pos actions
        for a in self.actions:
            if a.type.category == ActionCategory.OTHER or a.type.category == ActionCategory.CREATEITEM:
                if a.successful:
                    # not sure if these checks are already done in block processing
                    if a.type.t1type == Target.PLAYER:
                        if not a.target.status.can_be_targeted:
                            a.successful = False
                            continue # ??
                    
                    # probs gotta check for target None
                    # bc sometimes player target is optional
                    if a.type.t2type == Target.PLAYER and not a.target_two.status.can_be_targeted:
                        a.successful = False
                        continue

                    # todo more checks probably
                    a.perform(log=self.log)

            elif a.type.category == ActionCategory.OFFENSIVE:
                self.offensive_actions.append(a)
        return


    def do_new_masters(self):
        new_master_candidates = {} # field: [player1, ...]
        new_masters = {} # player: field
        conflicts = {} # player: field1, field2

        for f in self.fields:
            f.update_master_candidates()
            
            # if no PC master, try to elevate someone
            if f.master is None:
                if len(f.next_masters) > 0:
                    new_master_candidates[f] = f.next_masters
                    p = f.next_masters[0]

                    if f.next_masters[0] in new_masters.keys():
                        # conflict exists 
                        conflicts[p] = [f, new_masters[p]]
                        
                    else:
                        new_masters[p] = f
            

        # check just in case someone tries to become master of 2 things simultaneously 
        while len(conflicts.keys()) > 0:
            for player, fields in conflicts.items():
                roll = random.choice(fields)

                new_masters[player] = roll

                fields.remove(roll)

                for f in fields:
                    new_master_candidates[f].remove(player)
                    if len(new_master_candidates[f]) > 0:
                        new_cand = new_master_candidates[f][0]

                        if new_cand in new_masters.keys():
                            # WAIT what if 3 tho >:(
                            conflicts[new_cand] = [f, new_masters[new_cand]]
                        else:
                            new_masters[new_cand] = f
                
                del conflicts[player]
        
        nm_ret = {}
        for nm, f in new_masters.items():
            f.remove_player(nm)
            #f.master = nm # do AFTER elevations
            f.elevating = nm
            f.next_masters.remove(nm) # probably?

            nm.become_master(f) # TODO

            nm_ret[f] = nm # ehhhhh
        
        return nm_ret # i guess
        # todo TEST pls

    def do_elevations(self):
        pcE = [None] * 9 # test 
        npcE = [None] * 9 
        finalE = [None] * 9
        newM = self.do_new_masters().values()

        # preprocessing
        for f in self.fields:
            if f.master is not None:
                if f.master.status.can_elevate: # processing?
                    e = f.master.choices.to_elevate 
                    e = [i for i in e if i not in newM] # test

                    if len(e) > 0:
                        pcE[f.name] = e
            else:
                e = f.get_EP_list() 
                e = [i for i in e if i not in newM]
                npcE[f.name] = e
            
        # PC masters
        print(pcE)

        pc_choices = [None] * 9
        for i,p in enumerate(pcE):
            if p is not None:
                pc_choices[i] = p

        
        #e1 = [i[0] for i in pcE if i is not None] # hmm
        dupes = self.get_dupes(pc_choices) # make sure doesn't find None=None

        for d in dupes:
            p = pc_choices[d[0]]
            i = self.get_max([p.status.EP.vals[f] for f in d])

            for f in d:
                if f != i:
                    pcE[f].remove(p) # should always work
        
        for i, p in enumerate(finalE):
           
            if pc_choices[i] is not None: 
                finalE[i] = pc_choices[i]
        #finalE = e1

        print("finalE after PCs ", finalE)
        print(npcE)

        print(npcE[0])

        npc_choices = [None] * 9
        for idx,f in enumerate(npcE):
            if f is not None:
                # print(f, " not none")
                npcE[idx] = [i for i in f if i not in finalE] # ?
            else:
                # print(f, " was none, now empty")
                npcE[idx] = []
            if len(npcE[idx]) > 0:
                npc_choices[idx] = random.choice(npcE[idx])
        # print(npcE)
        
        # npc_choices = [random.choice(l) for l in npcE if len(l) > 0]
        print("npc choices ", npc_choices)
        # remove anyone a PC already went for 
        for i, p in enumerate(npc_choices):
            if p in finalE:
                npc_choices[i] = None


        dupes = self.get_dupes(npc_choices)
        print("dupes are ", dupes)

        for player, fields in dupes:
            # dupes are {Player: f1, f2}
            
            winner = self.get_max([player.status.EP.vals[f] for f in fields])

            for c in fields:
                if c != winner:
                    npcE[c] = [i for i in npcE[c] if i != p]
                    npc_choices[c] = random.choice(npcE[c])

    
        print("after dupes ", npc_choices)

        print(finalE)

        for i, p in enumerate(finalE):
            # check for conflict w PC? (shouldn't happen)
            if npc_choices[i] is not None: 
                finalE[i] = npc_choices[i]
        
        print("after integration ", finalE)
        
        
        for i, p in enumerate(finalE):
            if p is not None:
                p.elevate_in(FieldName(i)) #?
        
        print(finalE)
        
        self.log.log("Resulting elevations: ")

        for i, p in enumerate(finalE):
            self.log.log(f"{FIELDNAMES[i]}: {p.name if p is not None else 'none'}")


        return finalE

                


    def get_max(self, li: list[int]):
        random.shuffle(li) # for tiebreakers 
        idx = 0
        val = 0

        for i, n in li:
            if n > val:
                idx = i
                val = n
        return idx

    
    def get_dupes(self, li): 
        dupes = {} 

        for i, val in enumerate(li): 
            if li.count(val) > 1 and val is not None:
                if val in dupes: dupes[val].append(i)
                else: dupes[val] = [i]
        return dupes#.values()
    
    # todo TEST elevations2

    # todo somewhere: remember to account for fields being destroyed

    # check this over, hmm
    # also it's 1 IP per FOUR EP
    def offset_IP(self):
        for pid in self.sane_players:
            p = self.players[pid]
            if p.choices.offset_IP > 3:
                offset = p.choices.offset_IP // 4
                if p.processing.insanity_bonus > 0:
                    if p.processing.insanity_bonus < offset:
                        num_EP = offset - p.processing.insanity_bonus
                    else:
                        num_EP = offset 
                
                else: # IB is already 0
                    return

                ep_list = p.status.EP.get_list()
                filing = p.choices.filing_EP

                without_current_filings = []
                for e in ep_list:
                    if e not in filing:
                        without_current_filings.append(e)
                
                if len(without_current_filings) <= num_EP:

                    # remove all EP in other fields
                    for e in without_current_filings:
                        p.status.EP.values[e] -= 1 # SHOULD be fine not to go below 0, buc still check 
                        num_EP -= 1
                        ep_list.remove(e) 
                    
                    for j in range(num_EP):
                        rem = random.choice(ep_list) # remember to check if ep_list is empty
                        ep_list.remove(rem)
                        p.status.EP.values[rem] -= 1
                
                else: # there's enough EP to remove without looking at current fields 

                    for k in range(num_EP):
                        rem = random.choice(without_current_filings) 
                        ep_list.remove(rem)
                        without_current_filings.remove(rem) 
                        p.status.EP.values[rem] -= 1
                        
                # TODO LOG

    # not sure this needs to be a sep func
    def file_EP(self):
        # todo log
        for pid in self.sane_players:
            p = self.players[pid]
            if not p.status.is_expelled and p.processing.can_file_EP:
                # check that they aren't filing more than allowed
                for e in p.choices.filing_EP:
                    if e is not None:
                        p.assign_EP(e)

                        self.fields[e].add_EP(p)


    def process_mechanics(self):
        self.log.add_section("Horns", "Processing Horns...")
        horns = Horns()
        horns.run_horns(self.players, self.fields, self.log)
        # todo NAHLROUT

        # elevations
        self.log.add_section("Elevations", "Processing elevations...")
        self.do_elevations()

        # offset IP
        self.log.add_section("EP", "Processing EP stuff & breakout roll...")
        self.offset_IP()

        # file EP
        self.file_EP()

        # breakout roll
        for p in self.players:
            if not p.initial_status.is_sane and p.initial_status.is_alive:
                roll = random.randint(1,20)
                if len(p.known_names) >= 5:
                    roll = random.randint(1,10)
                
                if roll == 1:
                    print(f"{p.name} broke out !!!")
                    p.status.is_sane = True 
                    # todo break_out() func 

        return

    def process_offensive_actions(self):
        #TODO

        sabotagee = None
        attacks = [] # (attack action, target)
        could_go_insane = []
        protected = []

        for p in self.sane_players:
            if self.players[p].status.lodging == Lodging.Streets:
                roll = random.randint(1,4)

                if roll == 1:
                    # todo probs not this
                    attacks.append(("Streets", self.players[p]))
            
            if self.players[p].processing.insanity_bonus > 0:
                could_go_insane.append(self.players[p])

        for a in self.offensive_actions:
            # check if blocked? 
            # if a.target.status.lodging == Lodging.HorseAndFour:
            #     roll = random.randint(1,2)
            #     if roll == 1:
            #         protected.append(a.target) # hmmm
            #         # TODO fix 
            
            if a.type == ActionType.Sabotage and a.successful:
                # todo if expelled, it's a kill (but blockable)

                # if insane, this is unblockable kill
                if not a.target.status.is_sane:
                    a.successful = True
                    #sabotagee = (a,a.target)
                    attacks.append((a, a.target))

                elif a.target.processing.can_be_targeted:
                    sabotagee = (a,a.target)

                    # checked later
                    # if sabotagee.holds_item(ItemType.BLOODLESS):
                    #     b = sabotagee.get_items(ItemType.BLOODLESS)

                    #     if len(b) > 0: # should always be true
                    #         b[0].use() # todo, probs
                        
                    #         a.successful = True # bc not blocked
                    #         sabotagee = None
                    
            
            if a.type == ActionType.UseAssassin and a.successful:
                if a.target.processing.can_be_targeted:
                    attacks.append((a, a.target))

            
            # todo bonetar 
            if a.type == ActionType.UseBonetar and a.successful:
                lodging_destroyed = a.target
                at_lodging = [id for id in self.living_players if self.players[id].status.lodging == lodging_destroyed] # that might be a bit much but hey it works 
                if a.player.id in at_lodging: at_lodging.remove(a.player.id) # handled separately inside perform()

                results = a.perform(log=self.log, at_lodging=at_lodging)

                for d in results["dead"]:
                    being_attacked.append(d)
                
                # todo put survivors on the streets

            # todo mommet

        dying: set(Player) = set()
        
        for attacked in attacks:
            # TODO change to attacked.attack(attackaction)
            result = attacked[1].get_attacked(attacked[0])

            if result: # person dies
                dying.append(attacked[1])
                self.log.log(f"{attacked[1].name} dying to {attacked[0].name}")
                self.log.results.public_results.append(f"{attacked[1].name} was killed!") # ?add alignment?
            else: # person is protected
                self.log.log(f"{attacked[1].name} was attacked by {attacked[0]} but survived") # due to?
                self.log.results.public_results.append(f"{attacked[1].name} was attacked, but survived!")
        
        if sabotagee is not None: # if sabotage was attack, this is none
            was_sabotaged = sabotagee[1].get_attacked(sabotagee[0])
            if was_sabotaged:
                self.log.log(f"{sabotagee[1]} successfully sabotaged")
                self.log.results.public_results.append(f"{sabotagee[1]} went insane!")
            else:
                self.log.log(f"{sabotagee[1].name} was sabotaged but survived") # due to?
                self.log.results.public_results.append(f"{sabotagee[1].name} was attacked, but survived!")
            # if sabotagee.holds_item(ItemType.GRAM):
            #     g = attacked.get_items(ItemType.GRAM)
            #     if len(g) > 0:
            #         g[0].use()
            #         protected.append(sabotagee)
            # elif sabotagee.holds_item(ItemType.BODYGUARD):
            #     bs = attacked.get_items(ItemType.BODYGUARD)
            #     if len(bs) > 0:
            #         bs[0].use() # SABOTAGE
            #         protected.append(sabotagee)
            # else:
            #     sabotagee.go_insane()
        
        for p in could_go_insane:
            roll = random.randint(1,10)

            if roll + p.processing.insanity_bonus >= 12:
                p.go_insane()
                self.log.log(f"{p.name} went insane normally")
                self.log.results.public_results(f"{p.name} went insane!") # todo: check against already-insane ppl

        # for a in still_attacked:
        #     a.die()

        # TODO LOGGING / RESULTS
        return
    
    def process_imre(self):
        apoth_orders = {
            "nahlrout": [],
            "courier": [],
            "bloodless": [],
            "gram": []
        }

        # pay giles/devi
        # note: interest payoff (if it occurred) will have already happened
        # and what's left in choices.pay_whoever does NOT include the amount already taken out
        # this is kinda pointless / weird tbh 
        for pid in self.sane_players:
            p = self.players[pid]

            if p.choices.pay_giles > 0:
                p.pay_giles()
            
            if p.choices.pay_devi > 0:
                p.pay_devi()

        for pid in self.imre_players:
            p = self.players[pid]
            pchoices = p.choices.IMRE_CHOICES

            # TODO: blocks stuff

            p.visit_eolian()

            p.gamble_loadeddice()

            p.visit_devi()
            p.visit_giles()

            apoth = pchoices["Apothecary"]

            # todo: check this works
            apoth_orders["nahlrout"] += [p] * apoth["nahlrout"]
            apoth_orders["courier"] += [p] * apoth["courier"]
            apoth_orders["bloodless"] += [p] * apoth["bloodless"]
            apoth_orders["gram"] += [p] * apoth["gram"]

            bm = pchoices["Black Market"]
            # todo


        # BLACK MARKET

        # resolve apothecary orders
        # why is this two functions? idk, it probably shouldn't be
        valid_orders = self.apothecary.take_orders(apoth_orders)
        self.apothecary.give_out_sold_items(valid_orders)

        # todo

        return

    def postprocessing(self):
        for pid in self.living_players:
            p = self.players[pid]

            if len(p.processing.items_received) > 0:
                for item in p.processing.items_received:
                    p.status.inventory.append(item)

    def PROCESS_TURN(self):
        # update field statuses to new month (?)

        # setup
        for p in self.players:
            # add processing object for this turn
            p.processing = PlayerProcessing(p.info, p.status, p.choices, self.month)

            # add next_status for next turn (to overwrite status at end of turn processing)
            p.initial_status = p.status
            p.status = p.status.new_turn()
            p.month += 1

        # term beginning -----
        if self.month % 3 == 0 and self.month != 0:
            self.start_term()
        
        # lodging effects / IB
        for pid in self.sane_players:
            p = self.players[pid]
            if p.status.lodging == Lodging.Mews:
                p.processing.insanity_bonus += 2
            elif p.status.lodging == Lodging.SpindleAndDraft:
                p.processing.insanity_bonus -= 2
            


        # set up passive roleblocks
        self.log.add_section("Roleblocks & The Like", "Starting to process roleblocks etc.")
        for pid in self.sane_players:
            p = self.players[pid]
            
            roll = random.randrange(0,100)

            # HOMECOMING
            # add this to results
            if p.info.social_class == Background.Vint and roll < 25:
                p.processing.is_blocked = True
                p.processing.can_be_targeted = False
            elif p.info.social_class == Background.Aturan and roll < 10:
                p.processing.is_blocked = True
                p.processing.can_be_targeted = False
            
            if p.status.lodging == Lodging.Ankers and random.randrange(0,100) < 15:
                # TODO check for in imre
                if len(p.choices.actions) > 0:
                    action_blocked = random.choice(p.choices.actions)
                    action_blocked.blocked = True
                    action_blocked.block_reasoning += "Ankers"
            elif p.status.lodging == Lodging.KingsDrab and random.randrange(0,100) < 5:
                p.get_stolen_from()
                # log? 

            # TODO log
        
        # TODO process if actions by expelled students work
        # can only target expelled ppl or ppl in imre
        self.preprocessing()
        
        self.log.log("Passive roleblocks processed...")

        self.process_blocks(self.actions)

        self.log.log("All blocks processed!")
        success_actions = [a for a in self.actions if a.successful]
        #self.log.log("Actions marked as succeeding: ", [str(a) for a in success_actions])

        self.log.add_section("Standard Actions", "Starting to process standard actions...")
        # preprocessing? 
        self.process_standard_actions()

        self.log.log("Standard actions processed!")

        # TODO imre


        self.log.add_section("Mechanics stuff", "Starting to process mechanics...")
        self.process_mechanics()
        self.log.log("Mechanics processed!")

        self.log.add_section("Offensive Actions", "Processing offensive actions...")
        self.process_offensive_actions()
        self.log.log("Offensive actions processed!")

        # give players any items they received
        self.postprocessing()

        self.log.add_section("Final", "Turn is processed! blah blah blah")

        return self.log.get_log()

        # stuff? 
        # return results, probably
            
            

