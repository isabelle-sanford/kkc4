import copy
import random
from field import FieldStatus, FIELDS
from horns import Horns
from items import Item, ItemType
from outcome import ProcessLog, Result
from player import Player, PlayerProcessing, PlayerStatic, PlayerStatus, PlayerChoices
from actions import Action, ActionType, ActionCategory
from statics import Background, Lodging

# idk 
#PLAYERS: "list[Player]" = [] 

# could put all this in a Game class
def add_player(input, id):
    p = PlayerStatic(input["player_name"], input["player_rpname"], input["is_evil"], input["background"])
    p.id = id

    inventory = []
    if input["inventory"] is not None:
        inventory.append(Item.Generate(input["inventory"])) # does this work or do you need to do something different bc 2 nahlrout? 
    ps = PlayerStatus.distro_init(p, input["lodging"], input["musical_stat"], inventory)

    player = Player(p, ps)
    


    if input["ep1"] is not None:
        player.assign_EP(FIELDS[input["ep1"][0]].name, input["ep1"][1])
        FIELDS[input["ep1"][0]].add_EP(player, input["ep1"][1])

    
    if input["ep2"] is not None:
        player.assign_EP(FIELDS[input["ep2"][0]].name, input["ep2"][1])
        FIELDS[input["ep1"][0]].add_EP(player, input["ep2"][1])

    #choice = PlayerChoices(p)

    return player

def start_game(distro_inputs):
    PLAYERS = []
    i = 0
    for d in distro_inputs:
        # make Player objects for month 0
        p = add_player(d, i) 
        i += 1
        PLAYERS.append(p)
    return PLAYERS

def add_action(PLAYERS, player_id, action_info):
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



def update_choices(PLAYERS, new_choices):

    for choice in new_choices:
        c = PLAYERS[choice["player"]]

        if choice["imre_next"]: c.imre_next = True
        if choice["EP"]:
            # check here?
            c.choices.filing_EP = choice["EP"]
                
        if choice["actions"]:
            for a in choice["actions"]:

                add_action(PLAYERS, c.id, a)
        # what about updating an action? do we just clear all actions before this func? 
        
        # todo other choices
            # imre stuff


class Turn:

    def __init__(self, playerlist: "list[Player]", gm_input, month: int, fields: "list[FieldStatus]"):
        self.players = playerlist
        self.gm_input = gm_input
        self.month = month

        self.log = ProcessLog(month)
        self.results = Result(month)

        self.actions: list[Action] = []
        self.offensive_actions: list[Action] = []

        self.fields = fields

        self.sane_players: list[int] = [] # just ids 
        self.living_players: list[int] = [] # just ids 

        for p in playerlist:
            if p.status.is_alive:
                self.living_players.append(p.id)

                if p.status.is_sane:
                    self.sane_players.append(p.id)
            
            for a in p.choices.actions:

                self.actions.append(a)
        # other lists? imre? 

        if gm_input["complaints"]:
            for v in range(len(gm_input["complaints"])):
                self.players[v].choices.complaints = gm_input["complaints"][v]
    
    def start_term(self):

        self.log.add_section("NEW TERM", "Starting new term.")
        
        # GIVE STIPENDS
        for pid in self.sane_players:
            p = self.players[pid]
            p.status.money += p.initial_status.stipend


        # DO TUITION STUFF
        # remember to check for masters, social class
            if p.choices.enroll_next and not p.status.is_expelled:
                if not p.status.is_enrolled:
                    tuition = p.status.tuition # from last enrollment
                else:
                    tuition = p.calculate_tuition(self.gm_input) # TODO
                
                if p.status.money >= tuition:
                    # todo check for the preferences thingy
                    p.status.money -= tuition
                    p.status.is_enrolled = True
                else:
                    p.status.is_enrolled = False


        # DO LODGING STUFF
        # remember to check price for masters, ruh
            # ordering on these?
            lodging_price = p.choices.next_lodging.price
            if p.info.social_class == Background.Ruh:
                lodging_price /= 2
            
            if p.status.master_of is not None:
                lodging_price *= 0.75
            
            if p.status.money >= lodging_price:
                p.status.money -= lodging_price
                p.status.lodging = p.choices.next_lodging
            else:
                # WHATEVER, TODO
                # LOG
                pass
            
            if p.initial_status.lodging == Lodging.WindyTower:
                p.status.available_EP -= 1

            # TODO lodging effects 
            if p.status.lodging == Lodging.WindyTower:
                p.status.available_EP += 1
                # what if master / expelled / whatevs 
            elif p.status.lodging == Lodging.GreyMan or p.status.lodging == Lodging.PearlOfImre:
                p.status.in_Imre = True
        # todo make sure expelled students not in mews


        self.log.log("Stipends, tuition, & lodging processed.")
    

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

    def preprocessing(self):
        # assigning insanity bonuses

        standard_actions: list[Action] = []

        # mews
        for pid in self.sane_players:
            p = self.players[pid]
            if p.status.lodging == Lodging.Mews:
                p.processing.insanity_bonus += 2
            elif p.status.lodging == Lodging.SpindleAndDraft:
                p.processing.insanity_bonus -= 2
            
        # action IBs
        # tbh just move this stuff under perform() though
        for a in self.actions:
            if a.successful:
                # TODO
                if a.type.category == ActionCategory.CREATEITEM:
                    standard_actions.append(a)
                    # ASSIGN APPROPRIATE IB
                    pass
                elif a.type == ActionType.MalfeasanceProtection:
                    # assign appropriate ib
                    pass 
                elif a.type == ActionType.UseName:
                    # assign appropriate ib
                    pass
                elif a.type == ActionType.UseMommet:
                    # assign ib
                    pass
                else:
                    pass

                if a.type.category == ActionCategory.OTHER:
                    standard_actions.append(a)
        
        return standard_actions
    
    def process_standard_actions(self):

        for a in self.actions:
            if a.category == ActionCategory.OTHER or a.category == ActionCategory.CREATEITEM:
                if a.successful:

                    # todo checks probably
                    a.perform()
            elif a.category == ActionCategory.OFFENSIVE:
                self.offensive_actions.append(a)
        return


    # todo somewhere: remember to account for fields being destroyed
    def do_elevations(self):

        to_elevate: list[Player] = []

        for f in self.fields:
            if f.master is not None: # PC master
                m = f.master

                if len(m.choices.to_elevate) > 0:
                    if m.processing.can_elevate:
                        to_elevate.append(m.choices.to_elevate[0])
                        f.elevating = m.choices.to_elevate[0]
                # else add tuition inflation 
            
            else: # NPC
                elevation_candidates: list[Player] = f.get_EP_list()
                self.log.log(f"NPC master {f.name} picking who to elevate among: {elevation_candidates}")

                if len(elevation_candidates) > 0:
                    npc_choice = random.choice(elevation_candidates)
                    to_elevate.append(npc_choice)
                    f.elevating = npc_choice
        


        # todo: recurse until duplicates are gone
        for f in self.fields:
            if f.elevating is not None:
                self.log.log(f"Player {f.elevating.name} elevated in {f.name}")

                f.elevate_player(f.elevating)
                f.elevating.elevate_in(f.name)

                

        # todo LOG

    # check this over, hmm
    def offset_IP(self):
        for pid in self.sane_players:
            p = self.players[pid]
            if p.choices.offset_IP > 0:
                offset = p.choices.offset_IP
                if p.insanity_bonus > 0:
                    if p.insanity_bonus < offset:
                        num_EP = offset - p.insanity_bonus
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
                    p.assign_EP(e)

                    self.fields[e].add_EP(p)


    def process_mechanics(self):

        horns = Horns()
        horns.run_horns(self.players, self.fields, self.log)
        # todo NAHLROUT

        # elevations
        # TODO master-level elevations
        self.do_elevations()

        # offset IP
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
        being_attacked = [] # maybe include reason? 
        could_go_insane = []
        protected = []

        for p in self.sane_players:
            if self.players[p].status.lodging == Lodging.Streets:
                roll = random.randint(1,4)

                if roll == 1:
                    being_attacked.append(self.players[p])
            
            if self.players[p].processing.insanity_bonus > 0:
                could_go_insane.append(self.players[p])

        for a in self.offensive_actions:
            # check if blocked? 
            if a.target.status.lodging == Lodging.HorseAndFour:
                roll = random.randint(1,2)
                if roll == 1:
                    protected.append(a.target) # hmmm
                    # TODO fix 
            
            if a.type == ActionType.Sabotage and a.successful:
                # TODO remember that if insane, this is unblockable kill
                # if expelled, it's a kill (but blockable)
                if a.target.processing.can_be_targeted:
                    sabotagee = a.target

                    if sabotagee.holds_item(ItemType.BLOODLESS):
                        b = sabotagee.get_items(ItemType.BLOODLESS)

                        if len(b) > 0: # should always be true
                            b[0].use() # todo, probs
                        
                            a.successful = True # bc not blocked
                            sabotagee = None
                    
            
            if a.type == ActionType.UseAssassin and a.successful:
                if a.target.processing.can_be_targeted:
                    being_attacked.append(a.target)

            
            # todo bonetar 

            # todo mommet

        still_attacked = []
        
        for attacked in being_attacked:
            if attacked.holds_item(ItemType.GRAM):
                g = attacked.get_items(ItemType.GRAM)
                if len(g) > 0:
                    g[0].use()
                    protected.append(attacked)
            
            elif attacked.holds_item(ItemType.BODYGUARD):
                bs = attacked.get_items(ItemType.BODYGUARD)
                if len(bs) > 0:
                    bs[0].use() # KILL
                    protected.append(attacked)
            
            else:
                still_attacked.append(attacked)
        
        if sabotagee is not None:
            if sabotagee.holds_item(ItemType.GRAM):
                g = attacked.get_items(ItemType.GRAM)
                if len(g) > 0:
                    g[0].use()
                    protected.append(sabotagee)
            elif sabotagee.holds_item(ItemType.BODYGUARD):
                bs = attacked.get_items(ItemType.BODYGUARD)
                if len(bs) > 0:
                    bs[0].use() # SABOTAGE
                    protected.append(sabotagee)
            else:
                sabotagee.go_insane()
        
        for p in could_go_insane:
            roll = random.randint(1,10)

            if roll + p.processing.insanity_bonus >= 12:
                p.go_insane()

        for a in still_attacked:
            a.die()

        # TODO LOGGING / RESULTS
        return

    def PROCESS_TURN(self):
        # update field statuses to new month (?)

        # setup
        for p in self.players:
            # add processing object for this turn
            p.processing = PlayerProcessing(p.info, p.status, p.choices, self.month)

            # add actions to actions_list
            #self.actions.append(p.choices.actions)


            # add next_status for next turn (to overwrite status at end of turn processing)
            p.initial_status = p.status
            p.status = p.status.new_turn()
            p.month += 1

        # term beginning -----
        if self.month % 3 == 0 and self.month != 0:
            self.start_term()
        
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
                action_blocked = random.choice(p.choices.actions)
                action_blocked.blocked = True
                action_blocked.block_reasoning += "Ankers"
            # TODO log
        
        self.log.log("Passive roleblocks processed...")

        self.process_blocks(self.actions)

        self.log.log("All blocks processed!")

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

        self.log.add_section("Final", "Turn is processed! blah blah blah")

        return self.log.get_log()

        # stuff? 
        # return results, probably
            
            

