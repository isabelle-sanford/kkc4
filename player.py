import copy
from dataclasses import dataclass
from enum import Enum
import random
from actioninfo import ActionInfo 

from statics import Background, Lodging, FieldName, Rank
from actions import ActionType, Action
from field import FieldStatus
from items import ItemType, Item

class BaseStat(Enum):
    MUSIC = 1
    ESSAY = 2
    ART = 3


class PlayerStatic:
    def __init__(self, name:str , rp_name:str, is_evil:bool, 
                 social_class:Background, id:int = -1):
        self.id = id
        self.name: str = name 
        self.rp_name: str = rp_name
        self.is_evil: bool = is_evil # or could be skindancer
        self.social_class: Background = social_class
    
    def __str__(self):
        ret = f"Player: {self.name} ({self.rp_name}) - {self.social_class} - "
        ret += "Skindancer" if self.is_evil else "Student"
        ret += "\n"
        return ret

@dataclass
class EP:
    # TODO figure out what's going on here
    vals = {
            FieldName.LINGUISTICS: 0, 
            FieldName.ARITHMETICS: 0, 
            FieldName.RHETORICLOGIC: 0,
            FieldName.ARCHIVES: 0, 
            FieldName.SYMPATHY: 0,
            FieldName.PHYSICKING: 0,
            FieldName.ALCHEMY: 0,
            FieldName.ARTIFICERY: 0,
            FieldName.NAMING: 0
            }
    
    def get_list(self): # [rhet, rhet, ling, ling, ling, ...]
        all_EP: list[FieldName] = []
        for i in self.vals.keys(): # ?
            for j in range(self.vals[i]):
                all_EP.append(FieldName(i))
    
        return all_EP
    
    def __str__(self) -> str:
        ret = ""
       
        for k in self.vals.keys():
            if self.vals[k] > 0:
                ret += f"({k}: {self.vals[k]}) "
            
        return ret

class PlayerStatus:

    def __init__(self, player_static):
        self.info = player_static


    # input from GM distribution 
    @classmethod
    def distro_init(
        cls, player_static, current_lodging, musical_stat, inventory
        #current_funds
    ):
        s = PlayerStatus(player_static)
        s.month =  -1 #??
        s.available_EP = 5
        s.rank = Rank.NONE

        s.lodging: Lodging = current_lodging
        s.money = player_static.social_class.initial_funds 
        s.stipend = player_static.social_class.stipend
        s.current_tuition = 10

        s.musical_stat = musical_stat
        s.inventory: list[Item] = inventory # questionable
        # should bodyguard be in inventory or separate?

        s.EP: EP = EP() 
        s.elevations: list[FieldName] = []
        s.master_of: FieldName = None # 4th elevation is equivalent I guess?

        s.is_alive = True 
        s.is_sane = True
        s.is_expelled = False 
        s.is_enrolled = True 
        s.in_Imre = False
        s.broke_out = False # for underthing

        # things the player knows / happened prev turn
        # so their page can have invalid stuff grayed out or whatever
        s.can_take_actions = True # why is this blue
        s.can_file_complaints = True 
        s.can_file_EP = True 
        s.can_be_targeted = True # medica emergency, vint/aturan
        s.can_elevate = True
        s.can_be_elevated = True
        # is lashed? 

        s.accessible_abilities: list[ActionInfo] = [] # TODO
        if player_static.is_evil:
            s.accessible_abilities.append(ActionType.Sabotage.info)
        s.known_names = [] # ? (for breakout roll)

        # are there any other prev turn effects? 
        # this is the best way I could come up with to have effects into future turns
        s.last_reckless_use = -2 # successful - nahlrout protected doesn't count here
        s.last_conduct_unbecoming = -2
        s.last_volatile_firestop = -2
        s.last_medica_emergency = -2 # 
        s.last_in_medica = -2 # for bonetar ig

        # IMRE
        # hmmmm - could make own class? 
        s.IMRE_INFO = {
            "EOLIAN_auditioned": False,
            "GILES_defaulted": False,
            "GILES_amt_owed": 0.0,
            "DEVI_defaulted": False,
            "DEVI_amt_owed": 0.0,
            "DEVI_collateral": [],
            "BLACKMARKET_Contractlog": []
            # TODO blacklistings probs
        }
        s.has_talent_pipes = True # todo

        return s
    
    def new_turn(self):
        newstatus = copy.deepcopy(self)

        newstatus.month += 1

        # change up being in Imre or not
        if newstatus.lodging == Lodging.GreyMan or newstatus.lodging == Lodging.PearlOfImre:
            newstatus.in_Imre = True
        else:
            # updated later when processing choices, if person wants to go
            newstatus.in_Imre = False

        # if roleblocked or no 
        # !! idk what I'm doing sigh
        blocked_by_anything = False
        if newstatus.last_reckless_use == newstatus.month - 1:
            blocked_by_anything = True
        if newstatus.last_conduct_unbecoming > newstatus.month - 3:
            blocked_by_anything = True
        if newstatus.last_volatile_firestop == newstatus.month - 1:
            blocked_by_anything = True
            newstatus.can_file_EP = False
            newstatus.can_file_complaints = False
        if newstatus.last_medica_emergency == newstatus.month - 1:
            blocked_by_anything = True
            newstatus.can_be_targeted = False
            # gotta check physicker level here sigh

        # I guess???
        if blocked_by_anything:
            self.can_take_actions = False

        return newstatus
    
    # TODO string / print func 

    # yes this is redundant no I am not happy about it
    def levels_in(self, field: FieldName):
        # error check?
        count = self.status.elevations.count(field)
        if self.status.master_of == field:
            count = 4
        return count
    
    
    def short_status(self):
        ret = "" 
        ret += "Alive" if self.is_alive else "Dead"
        ret += ", "
        ret += "Sane" if self.is_sane else "Insane"
        ret += " (Expelled)" if self.is_expelled else ""

        return ret


    
# working variables for processing turn
class PlayerProcessing:
    def __init__(self, player_info, player_status, player_choices, month):
        self.info = player_info
        self.starting_status = player_status
        self.month = month
        self.choices = player_choices
        # also want ending_status?

        self.complaints_blocked = False # Set when target of Argumentum Ad Nauseam.
        self.complaints_received: list[Player] = [] # this is POST processing
        self.processed_complaints = self.choices.complaints 
        
        # Total DP on the player
        self.DP: int = 0

        # Flag for whether they have been successfully blocked.
        self.is_blocked: bool = self.starting_status.can_take_actions
        self.is_lashed: bool = False

        # Working list of players that blocking them, as Player references
        self.blocked_by: list[Player] = []

        self.targeted_by: list[Player] = [] # for ward, pickpocket, ?

        # malfeasance protection things
        self.transfer_neg_actions_to = None # master 
        self.split_neg_actions_between = None # 3rd level
        self.all_actions_also_affect = None # 1-2
        
        self.can_file_complaints: bool = self.starting_status.can_file_complaints 
        self.can_file_EP: bool = self.starting_status.can_file_EP
        self.can_be_targeted: bool = self.starting_status.can_be_targeted
        self.can_elevate = self.starting_status.can_elevate
        # can file DP?

        # protect / attack info, maybe? 

        self.items_received: list[Item] = []
        # todo remember to add this ^ to next_status (AFTER everything else is processed)

        self.getting_elevated_in: FieldName = None

        self.insanity_bonus = 0 # might want to take something from prev status?
        # and check mews / spindle & draft


    def print_money(self):
        # this can probs be better / nicer 
        m = self.money # 3.14
        m *= 100 # 314
        m = str(m) # "314"
        ret = f"{m[0]} talent(s), {m[1]} jot(s), and {m[2]} drab(s)" 

        return ret


class PlayerChoices:
    # basically a record of what things a player wants to do this turn
    # and funcs returning false if the player can't do those things (?)
    # choices are actually processed and integrated to the overall game separately 
    # it's essentially just the info submitted from the player's page

    def __init__(self, playerstatic, month: int = 0):
        self.player_static = playerstatic
        self.month = month
        # maybe also status here? 

        if self.month % 3 == 2: # make lodging choice in month BEFORE term start
            self.next_lodging: Lodging = Lodging.Streets

        self.imre_next = False # should check if in imre lodging
        self.enroll_next = True # check expulsion etc 

        # List of complaints made (NOT including PiH)
        # remember cannot vote if expelled
        self.complaints: list[Player] = []

        self.actions: list[Action] = []

        self.filing_EP: list[FieldName] = []

        # if master 
        self.assigned_DP: list[Player] = []
        self.to_elevate: list[Player] = [] # ordered preference list

        # IMRE (check if player is there?)
        self.IMRE_CHOICES = {
            "Eolian": {
                "audition": False,
                "practice": False
            },
            "Devi": {
                "acquire_loan": False,
                "give_collateral": [], # item list
                "loan_amount": 0.0
            }, "Giles": {
                "acquire_loan": False,
                "loan_amount": 0.0
            }, "Loaded Dice": {
                "place_bet": False,
                "bet_amt": 0.0,
                "numbers": []
            }, "Apothecary": {
                "nahlrout": 0,
                "courier": 0, # does this need target?
                "bloodless": 0,
                "gram": 0
            }, "Black Market": {
                "mommet": [], # items
                "bodyguard": [], # player targets
                "assassin": [], # player targets
                "take_contract": [], # contract ids
                "place_contract": [] # contract info
            }
        }

        # probably automatically have interest here, if start of term + relevant? 
        self.pay_giles = 0
        self.pay_devi = 0

        self.offset_IP = 0
 
    def __str__(self) -> str:
        # TODO

        ret = f"{self.player_static.name}: complaints {self.complaints}"

        return ret


    # def __str__(self):
    #     # this is probably not ideal :p
    #     line1 = f"Player: {self.info.name}  Month: {self.month}\n"
    #     line2 = f"ep filed: {[s.name for s in self.EP_filed]}\n" # ! fix later
    #     line3 = f"Going to Imre next month: {self.imre_next}\n"
        
    #     return line1 + line2 + line3

@dataclass
class Tuition:
    pid: int
    quality_thread = 0.0 # 0.1 per post, ish
    quality_rp = 0 # 0.5 per post
    times_filed_EP = 0 # .5 per turn # done
    times_filed_complaints = 0 # 0.3 per turn
    items_sold = 0 # 0.05 per item
    apothecary_items = [] # depends on item 
    contracts_placed = [] # depends on contract amt
    tried_for_pipes: bool = False
    filled_contracts = 0.0 # .5 per contract
    num_posts_m1 = 0
    num_pms_m1 = 0
    num_posts_m2 = 0
    num_pms_m2 = 0
    num_posts_m3 = 0
    num_pms_m3 = 0
    num_complaints_received = 0 # post manip
    times_on_horns = 0
    no_public_apology = 0
    master_didnt_elevate = 0 # per turn
    master_didnt_act: bool = False # todo

    def calc_tuition(self, player: PlayerStatus):
        t = 5 if player.rank == Rank.MASTER else 10
        
        reductions = self.quality_thread + self.quality_rp * 0.5 # should already be calculated on entry
        reductions += self.times_filed_EP * 0.5
        reductions += self.times_filed_complaints * 0.3
        reductions += self.items_sold * 0.05
        # todo apoth items and contracts
        reductions += self.filled_contracts * 0.5
        reductions += 1 if self.tried_for_pipes else 0
         
        if self.num_posts_m1 > 0:
            reductions += 0.5
        if self.num_posts_m2 > 0:
            reductions += 0.5
        if self.num_posts_m3 > 0:
            reductions += 0.5
        
        if self.num_pms_m1 > 0:
            reductions += 0.3
        if self.num_pms_m2 > 0:
            reductions += 0.3
        if self.num_pms_m3 > 0:
            reductions += 0.3
        
        inflations = 0
        # todo: care div by 0 probably
        m1_ratio = self.num_pms_m1 / (self.num_pms_m1 + self.num_posts_m1)
        m2_ratio = self.num_pms_m2 / (self.num_pms_m2 + self.num_posts_m2)
        m3_ratio = self.num_pms_m3 / (self.num_pms_m3 + self.num_posts_m3)
        for ratio in [m1_ratio, m2_ratio, m3_ratio]:
            if ratio >= 0.75:
                inflations += 1
            if ratio > 0.85:
                inflations += 1
            if ratio > 0.9:
                inflations += 1
            if ratio > 0.95:
                inflations += 1
        
        inflations += self.num_complaints_received * 0.1
        inflations += self.times_on_horns * 2
        inflations += self.no_public_apology * 2
        inflations += 0.5 if player.rank == Rank.RELAR else 0
        inflations += 1 if player.rank == Rank.ELTHE else 0

        if player.rank == Rank.MASTER:
            if self.num_posts_m1 == 0:
                inflations += 3
            if self.num_posts_m2 == 0:
                inflations += 3
            if self.num_posts_m3 == 0:
                inflations += 3
            
            inflations += self.master_didnt_elevate * 1

            if self.master_didnt_act:
                inflations += 4

        # log total inflation / reduction

        t = t + inflations - reductions

        if player.info.social_class == Background.Vint:
            t *= 1.33
        
        arit_levels = player.levels_in(FieldName.ARITHMETICS)

        if arit_levels > 0:
            decrease = 0.05 * arit_levels
            t = t - t * decrease
        
        return t
        
    # todo reset_tuition thingy probably?



class Player:
    # start of game constructor 
    def __init__(self, player_static: PlayerStatic, player_status: PlayerStatus, player_choices: PlayerChoices = None, player_process: PlayerProcessing = None):
        self.initial_status: PlayerStatus = player_status
        self.status: PlayerStatus = player_status
        self.info: PlayerStatic = player_static 

        if player_choices is None:
            player_choices = PlayerChoices(player_static, 0)
        self.choices: PlayerChoices = player_choices 

        # self.past_statuses = [] ? 
        
        # sort of irregularly used, but maybe more helpful than passing full Player instances around everywhere
        self.id: int = player_static.id 
        self.name: str = player_static.name
        self.month = -1 # hmm

        # need to remember to make new processing objects per turn
        if player_process is None:
            player_process = PlayerProcessing(player_static, player_status, player_choices, self.month)
        self.processing: PlayerProcessing = player_process

        self.tuition = Tuition(self.id)

    def __str__(self):

        ret = f"{self.info}{self.status.EP}\n"

        return ret
    
    def __repr__(self):
        # todo not this
        ret = f"{self.info.name} ({self.info.social_class} "
        ret += "Skindancer" if self.info.is_evil else "Student"
        ret += f" {self.status.rank})"
        return ret

    # todo become_master(field)

    # todo action period stuff (sigh)

    def levels_in(self, field: FieldName):
        # error check?
        count = self.status.elevations.count(field)
        if self.status.master_of == field:
            count = 4
        return count

    def elevate_in(self, field: FieldName):
        self.status.elevations.append(field)
        num_EP = self.status.EP.vals[field]
        if num_EP < 5:
            self.status.EP.vals[field] = 0
        else:
            self.status.EP.vals[field] -= 5
        
        self.status.rank = self.status.rank.get_next()
        self.status.available_EP -= 1

        # TODO if elthe + only studied in one field, add 5 EP

        # anything else here? 
        # TODO more stuff if master (probs)

        # TODO add new accessible abilities

        # todo aturan chance of backing out of arcane fields


    def go_insane(self, fields: "list[FieldStatus]"):
        # TODO
        self.status.is_sane = False 
        self.status.can_be_elevated = False

        for f in fields:
            f.remove_player(self)
        self.status.EP = None

        # ... other stuff? 
        return 

    def break_out(self):
        # TODO
        self.status.is_sane = True
        self.status.broke_out = True
        # rank stuff, accessible abilities, ...
        return 
    
    def die(self, fields: "list[FieldStatus]"):
        self.status.is_alive = False
        self.status.can_take_actions = False
        self.status.can_be_targeted = False #no
        self.status.can_be_elevated = False 
        self.status.is_enrolled = False
        self.status.can_file_complaints = False
        self.status.can_file_EP = False


        for f in fields:
            f.remove_player(self)
        self.status.EP = None
        
        # TODO ??
    
        return

    def take_action(self, action: Action):

        self.choices.actions.append(action)
        self.status.rank
        # Do checks to make sure the action is valid?
        # maybe do this in choices?
    
    def expel(self, fields):
        self.status.is_expelled = True
        self.status.can_file_EP = True
        self.status.can_be_elevated = False

        for f in fields:
            f.remove_player(self)
        
        if self.info.social_class == Background.Vint:
            self.status.stipend = 20
        
        # anything else? 


    def add_item(self, item: Item):
        self.processing.items_received.append(item)

    def holds_item(self, item_type: ItemType) -> bool:
        count = 0
        for item in self.status.inventory:
            if item.type == item_type:
                count += 1
        if count > 0:
            return True
        else:
            return False
    
    def item_count(self, item_type: ItemType) -> int:
        count = 0
        for item in self.status.inventory:
            if item.type == item_type:
                count += 1
        return count
    
    def get_items(self, item_type: ItemType) -> "list[Item]":
        list = []
        if self.holds(item_type) > 0:
            for item in self.status.inventory:
                if item.type == item_type:
                    list.append(item)
        return list

    # not sure if to do imre stuff here or in process_imre tbh
    def visit_eolian(self):
        if self.status.IMRE_INFO["EOLIAN_auditioned"]:
            # cannot re-audition
            return
        
        if self.choices.IMRE_CHOICES["Eolian"]["practice"]:
            self.status.musical_stat += 0.5
            return 
        
        if self.choices.IMRE_CHOICES["Eolian"]["audition"]:
            mstat = self.status.musical_stat
            pipes = False
            # TODO

            if pipes:
                self.status.inventory.append(Item.Generate(ItemType.TALENTPIPES))
                self.status.has_talent_pipes = True
            
            return

    def gamble_loadeddice(self):
        # todo check blacklisting
        if not self.choices.IMRE_CHOICES["Loaded Dice"]["place_bet"]:
            return
        houseroll = random.randint(1,20)
        if self.info.social_class == Background.Ceald:
            houseroll = random.randint(1, 6)
        elif self.info.social_class == Background.Ruh:
            houseroll = random.randint(1,12)
        
        nums = self.choices.IMRE_CHOICES["Loaded Dice"]["numbers"]
        bet_amt = self.choices.IMRE_CHOICES["Loaded Dice"]["bet_amt"] 

        if houseroll in nums: # win! 
            
            numlen = len(nums)

            if numlen == 1:
                multiplier = 20
            elif numlen == 2:
                multiplier = 15
            elif numlen == 3:
                multiplier = 10
            elif numlen == 4:
                multiplier = 5
            elif numlen == 5:
                multiplier = 2
            else: 
                # error
                print(" uh oh")
            
            winnings = bet_amt * multiplier

            self.increase_money(winnings)
        
        else: # lost
            self.reduce_money(bet_amt)
    
    def visit_devi(self):
        if self.status.IMRE_INFO["DEVI_defaulted"]:
            return 
        # maybe check for prev loan too? 

        d = self.choices.IMRE_CHOICES["Devi"]

        if not d["acquire_loan"]:
            return
        
        if d["loan_amount"] < 4:
            # minimum is 4 talents 
            # should also have this check on webpage
            return

        income = 0
        if self.holds_item(ItemType.TALENTPIPES):
            # ! this talent pipes check should be post stealing stuff
            # (which i thiiiink it is?)
            income += 10
        income += self.status.stipend

        # TODO collateral 

        if d["loan_amount"] > income / 2:
            # loan must be no more than half your income
            # (plus collateral)
            # return or just do highest you can afford? 
            return

        # if you get the loan:

        self.increase_money(d["loan_amount"])
        # todo take collateral
        self.status.IMRE_INFO["DEVI_amt_owed"] = d["loan_amount"]

    def visit_giles(self):
        if self.status.IMRE_INFO["GILES_defaulted"]:
            return 
        # maybe check for prev loan too? 



        d = self.choices.IMRE_CHOICES["Giles"]

        if not d["acquire_loan"]:
            return
        
        if self.status.lodging != Lodging.GreyMan and self.info.social_class != Background.Ceald:
            # must be a ceald or at the grey man
            # should also be checked on webpage
            return

        if d["loan_amount"] > 2:
            # maximum is 2 talents 
            # should also have this on webpage
            return


        # if you get the loan:

        self.increase_money(d["loan_amount"])
        self.status.IMRE_INFO["GILES_amt_owed"] = d["loan_amount"]

    def pay_devi(self):
        owed = self.status.IMRE_INFO["DEVI_amt_owed"]
        paying = self.choices.pay_devi
        if owed <= 0:
            return 
        
        if self.status.IMRE_INFO["DEVI_defaulted"]:
            # you defaulted, you can't do anything now
            return
        
        if paying <= 0:
            return
        
        if paying > owed:
            paying = owed

        self.status.IMRE_INFO["DEVI_amt_owed"] -= paying
        self.reduce_money(paying)

        # return collateral if loan is entirely paid off
        if self.status.IMRE_INFO["DEVI_amt_owed"] <= 0:
            for item in self.status.IMRE_INFO["DEVI_collateral"]:
                self.add_item(item)
        
    def pay_giles(self):
        owed = self.status.IMRE_INFO["GILES_amt_owed"]
        paying = paying
        if owed <= 0:
            return 
        
        if self.status.IMRE_INFO["GILES_defaulted"]:
            # you defaulted, you can't do anything now
            return
        
        if paying <= 0:
            return
        
        if paying > owed:
            paying = owed 

        self.status.IMRE_INFO["GILES_amt_owed"] -= paying
        self.reduce_money(paying)

    def apoth_orders(self):
        # check in imre or whatever
        o = self.choices.IMRE_CHOICES["Apothecary"]

    # todo place_contract? (to remove the thing that's the reward)
    
    # todo use_item()

    def increase_money(self, amount: float):
        self.status.money += amount

    def reduce_money(self, amount: float):
        self.status.money -= amount

    def block_all(self, target):
        self.take_action(Action("Mommet", self,"Block All",target))
    
    def block_one(self, target, action_type: str):
        self.take_action(Action("Tenaculum", self,"Block One", target, action_type=action_type))
    
    def redirect_action(self, from_target, to_target, action_type: str):
        self.take_action(Action("Law of Contraposition", self, "redirect_action", from_target, to_target, action_type))

    def find_action(self, type: str):
        for a in self.choices.actions:
            if a.type.find(type) > -1:
                return a
        return None  
    
    def import_complaint(self, target): #?
        self.choices.complaints.append(target)

    # changed this slightly bc I wasn't clear what it was doing / if it was right
    def assign_DP(self, total = 1, master_of:FieldName = None):
        if master_of is not None:
            #print(f"Master {master_of.name} assigning DP to {self.info.name}, with {self.status.EP.vals[master_of]} ep in {master_of.name}")
            
            num_EP = self.status.EP.vals[master_of]
            
            if num_EP > 0:
                diff = num_EP - total
                if diff >= 0: # at least as much EP as DP
                    self.status.EP.vals[master_of] -= total # or = diff
                    total = 0
                else:
                    total -= num_EP # or = -diff
                    self.status.EP.vals[master_of] = 0
            
            self.processing.DP += total
            
        else:
            self.processing.DP += total

    def assign_EP(self, field: FieldName, total = 1):
        # todo add to field's ep listing? 
        self.status.EP.vals[field] += total


# maybe put this elsewhere - a test.py file? 
class PlayerRandom:
    def __init__(self) -> None:
        pass

    def Generate(self, name:str) -> Player:
        static = PlayerStatic(name, name, random.choice([True,False]),random.choice(list(Background)))
        status = PlayerStatus(static,random.choice(list(Lodging)),random.randint(1,20),[],round(random.random()*20.0,2))
        choice = PlayerChoices()

        return Player(static,status,choice)