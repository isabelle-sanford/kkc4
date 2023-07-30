import copy
from dataclasses import dataclass
from enum import Enum
import random
from actioninfo import ActionInfo 

from statics import Background, Lodging, FieldName, Rank
from actions import ActionType, Action
from field import FieldStatus, FIELDS
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

class EP:
    def __init__(self):

        self.vals = {
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

        self.accessible_actions: set[ActionType] = set() 
        if player_static.is_evil:
            self.accessible_actions.add(ActionType.Sabotage)
        self.month =  -1 #??
        self.rank = Rank.NONE
        self.money = player_static.social_class.initial_funds 
        self.stipend = player_static.social_class.stipend
        self.current_tuition = 10
        
        self.EP: EP = EP() 
        self.elevations: list[FieldName] = []
        self.master_of: FieldName = None # 4th elevation is equivalent I guess?
        self.is_alive = True 
        self.is_sane = True
        self.is_expelled = False 
        self.is_enrolled = True 
        self.in_Imre = False
        self.broke_out = False # for underthing
        

        # things the player knows / happened prev turn
        # so their page can have invalid stuff grayed out or whatever
        self.can_take_actions = True
        self.can_file_complaints = True 
        self.can_file_EP = True 
        self.can_be_targeted = True # medica emergency, vint/aturan
        self.can_elevate = True # eh, maybe do this in become_master()
        self.can_be_elevated = True
        # is lashed? 

        self.known_names = [] 

        # are there any other prev turn effects? 
        # this is the best way I could come up with to have effects into future turns
        self.last_reckless_use = -2 # successful - nahlrout protected doesn't count here
        self.last_conduct_unbecoming = -2
        self.last_volatile_firestop = -2
        self.last_medica_emergency = -2 # 
        self.last_in_medica = -2 # for bonetar ig

        # IMRE
        # hmmmm - could make own class? 
        self.IMRE_INFO = {
            "EOLIAN_auditioned": False,
            "GILES_defaulted": False,
            "GILES_amt_owed": 0.0,
            "DEVI_defaulted": False,
            "DEVI_amt_owed": 0.0,
            "DEVI_collateral": [],
            "BLACKMARKET_Contractlog": [],
            "LOADEDDICE_lastwon": -1,
            "LOADEDDICE_blacklistedtil": -1
        }
        self.has_talent_pipes = False # todo

        self.action_periods = [FieldName.GENERAL] # this is when NOT in imre


    # input from GM distribution 
    @classmethod
    def distro_init(
        cls, player_static, current_lodging, musical_stat, inventory
        #current_funds
    ):
        s = PlayerStatus(player_static)
        s.available_EP = 5 # check windy tower?

        s.lodging: Lodging = current_lodging

        s.musical_stat = musical_stat
        s.inventory: list[Item] = [inventory] # questionable
        # should bodyguard be in inventory or separate?
        

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
    
    def print_money(self):
        # this can probs be better / nicer 
        m = self.money # 30.14
        ret = f"{int(m // 1)} talent(s), {int((m * 10) // 1) % 10} jot(s), and {int(m * 100) % 10} drab(s)" 

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

        self.targeted_by: list[Action] = [] # for ward, pickpocket, ?

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

        self.getting_elevated_in: FieldName = None

        self.insanity_bonus = 0 # might want to take something from prev status?
        # and check mews / spindle & draft (currently in PROCESS_TURN)


        self.player_message = [] # todo fancy this probs

    def short_status(self):
        # maybe add this to playerstatus / just straight player
        ret = "" 
        ret += "Alive" if self.is_alive else "Dead"
        ret += ", "
        ret += "Sane" if self.is_sane else "Insane"
        ret += " (Expelled)" if self.is_expelled else ""





class PlayerChoices:
    # basically a record of what things a player wants to do this turn
    # and funcs returning false if the player can't do those things (?)
    # choices are actually processed and integrated to the overall game separately 
    # it's essentially just the info submitted from the player's page

    def __init__(self, playerstatic, month: int = 0, status: PlayerStatus = None):
        self.player_static = playerstatic
        self.month = month
        self.status = status
        # maybe also status here? 

        
        self.pay_giles = 0
        self.pay_devi = 0

        if self.month % 3 == 2: # make lodging choice in month BEFORE term start
            self.next_lodging: Lodging = Lodging.Streets
            if not self.status.is_expelled:
                self.enroll_next = True # check expulsion etc 
            
            if self.status.IMRE_INFO["DEVI_amt_owed"] > 0:
                arit_reduction = self.status.levels_in(FieldName.ARITHMETICS) * 10 + 10
                interest_owed = self.status.IMRE_INFO["DEVI_amt_owed"] * 0.3 * (1 - arit_reduction / 100)

                self.pay_devi = interest_owed
            
            if self.status.IMRE_INFO["GILES_amt_owed"] > 0:
                arit_reduction = self.status.levels_in(FieldName.ARITHMETICS) * 10 + 10
                interest_owed = self.status.IMRE_INFO["GILES_amt_owed"] * 0.15 * (1 - arit_reduction / 100)
                
                self.pay_giles = interest_owed




        # change up being in Imre or not
        if self.status.lodging == Lodging.GreyMan or self.status.lodging == Lodging.PearlOfImre:
            self.imre_next = True
        else:
            # updated later when processing choices, if person wants to go
            self.imre_next = False


        # List of complaints made (NOT including PiH)
        # remember cannot vote if expelled
        self.complaints: list[Player] = []

        self.actions: list[Action] = []

        self.filing_EP: list[FieldName] = []

        # if master 
        if self.status.master_of is not None:
            self.assigned_DP: list[Player] = []
            self.to_elevate: list[Player] = [] # ordered preference list

        # IMRE (check if player is there?)
        if self.status.in_Imre:
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


        self.offset_IP = 0
 
    def __str__(self) -> str:
        # TODO

        ret = f"{self.player_static.name}: complaints {self.complaints}"

        return ret


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
        




class Player:
    # start of game constructor 
    def __init__(self, player_static: PlayerStatic, player_status: PlayerStatus, player_choices: PlayerChoices = None, player_process: PlayerProcessing = None):
        self.initial_status: PlayerStatus = player_status
        self.status: PlayerStatus = player_status
        self.info: PlayerStatic = player_static 

        if player_choices is None:
            player_choices = PlayerChoices(player_static, 0)
        self.choices: PlayerChoices = player_choices 
        
        # sort of irregularly used, but maybe more helpful than passing full Player instances around everywhere
        self.id: int = player_static.id 
        self.name: str = player_static.name
        self.month = -1 # hmm

        # need to remember to make new processing objects per turn
        if player_process is None:
            player_process = PlayerProcessing(player_static, player_status, player_choices, self.month)
        self.processing: PlayerProcessing = player_process

        self.tuition = Tuition(self.id)

        self.history = [] # [(status m0, choices, processing), (status m1, choices, processing), ...]

    def __str__(self):

        ret = f"{self.info.name}\n"

        return ret
    
    def __repr__(self):
        # todo not this
        ret = f"{self.info.name} ({self.info.social_class} "
        ret += "Skindancer" if self.info.is_evil else "Student"
        ret += f" {self.status.rank})"
        return ret
    
    # i.e. process an attack on you
    def get_attacked(self, attack: Action):
        # sabotage, bonetar, assassin, mommet, ??
        if self.processing.can_be_targeted == False: 
            attack.successful = False
            print(f"Attack by f{attack.player} of {attack.type.info.name} on {self.name} was attempted, but {self.name} could not be targeted so it failed.")
            # todo log properly
            return False # idk, maybe string?
        
        if self.status.lodging == Lodging.HorseAndFour:
            roll = random.randint(1,2)
            if roll == 2:
                self.processing.player_message.append("You were attacked[], but protected!")
                return False 
        
        if attack.type == ActionType.Sabotage:
            if self.holds_item(ItemType.BLOODLESS):
                item = self.get_items(ItemType.BLOODLESS)[0]
                self.use_item(item)

                self.processing.player_message.append("You used your Bloodless to protect you from an attack!") # ig? 
                return False

        if self.holds_item(ItemType.GRAM):
            item = self.get_items(ItemType.GRAM)[0]
            self.use_item(item) 

            self.processing.player_message.append("You used your Bloodless to protect you from an attack!") # ig? 
            return False
        
        if self.holds_item(ItemType.BODYGUARD):
            item = self.get_items(ItemType.BODYGUARD)[0]
            self.use_item(item, info=attack.type) 

            self.processing.player_message.append("Your Bodyguard protected you from an attack!") # ig?
            return False 
        
        # TODO firestop
        
        # maybe return result for logging? 
        # die? / go insane?

        return True

    def get_stolen_from(self):
        
        updated_inventory = []
        for item in self.status.inventory:
            if item.type == ItemType.TALENTPIPES:
                continue
            if item.type == ItemType.BODYGUARD:
                continue # todo not if kingsdrab is blocked by bodyguards
            updated_inventory.append(item)
        
        if len(updated_inventory) == 0:
            return None

        choice = random.choice(updated_inventory)

        # probably actually take item later, for processing purposes
        # self.status.inventory.remove(choice)
        # self.processing.player_message.append("You misplaced the item ", choice)
        return choice

        

    def use_item(self, item, info=None):
        # TODO ?

        still_exists = item.use(info)

        if not still_exists:
            self.status.inventory.remove(item) # ig?

            if not self.holds_item(item.type):
                if item.type.using_action is not None:
                    self.status.accessible_actions.discard(item.type.using_action)

                    if item.type == ItemType.TENACULUM:
                        self.status.accessible_actions.discard(ActionType.UseTenaculumItem)

        return

    def levels_in(self, field: FieldName):
        # error check?
        count = self.status.elevations.count(field)
        if self.status.master_of == field:
            count = 4
        return count

    def elevate_in(self, field: FieldName):
        # if becoming a master, use become_master and NOT this

        self.status.elevations.append(field)
        num_EP = self.status.EP.vals[field]
        if num_EP < 5:
            self.status.EP.vals[field] = 0
        else:
            self.status.EP.vals[field] -= 5

        if self.info.social_class == Background.Aturan:
            if field == FieldName.SYMPATHY or field == FieldName.ALCHEMY or field == FieldName.ARTIFICERY or field == FieldName.NAMING:
                roll = random.randint(1,4)

                if roll == 1:
                    print(f"{self.name} backed out of {field}")
                    return
        
        self.status.rank = self.status.rank.get_next()
        self.status.available_EP -= 1

        curr_rank = self.status.rank

        # if you only study in one rank, get an extra 5 ep when reaching elthe
        if curr_rank == Rank.ELTHE and self.levels_in(field) == 3:
            self.status.EP.vals[field] += 5

        # add relevant ability/abilities (assumming not master, that's later)
        if field == FieldName.LINGUISTICS or field == FieldName.RHETORICLOGIC or field == FieldName.ARCHIVES:
            # need to add just the ability at that elevation level
            for ability in FIELDS[field].info.abilities:
                if ability.field_ability.min_rank == curr_rank:
                    self.status.accessible_actions.add(ability)
        elif field == FieldName.ARITHMETICS or field == FieldName.SYMPATHY or field == FieldName.PHYSICKING:
            # all ranks have access to all abilities 
            # maybe don't add passive arithmetics abilities?
            for ability in FIELDS[field].info.abilities:
                self.status.accessible_actions.add(ability)


        # if know any alchemy, add any new alchemy abilities
        if FieldName.ALCHEMY in self.status.elevations:
            for ability in FIELDS[FieldName.ALCHEMY].info.abilities:
                if ability.info.field_ability.min_rank <= self.status.rank:
                     self.status.accessible_actions.add(ability)
        # same for artificery
        if FieldName.ARTIFICERY in self.status.elevations:
            for ability in FIELDS[FieldName.ARTIFICERY].info.abilities:
                if ability.info.field_ability.min_rank <= self.status.rank:
                    self.status.accessible_actions.add(ability)

        if field == FieldName.NAMING:
             self.status.accessible_actions.add(ActionType.UseName)
        
        # if get an action period at that level, add it
        num_elevs = self.levels_in(field) 
        if FIELDS[field].info[num_elevs - 1] is not None:
            self.status.action_periods.append(FIELDS[field].info[num_elevs - 1])


        # anything else? 



    def become_master(self, field: FieldName):
        # checks (like already master? idk)

        self.status.master_of = field

        fieldinfo = FIELDS[field].info

        # add all abilities
        for ability in fieldinfo.abilities:
            self.status.accessible_actions.add(ability)
        
        for i, elev in self.status.elevations:
            if elev != field:
                # add the AP from that elevation, if relevant
                #? had i+1 here but I don't think that's right
                if fieldinfo.APbylevel[i] is not None:
                    self.status.action_periods.append(fieldinfo.APbylevel[i])
        
        # add master AP
        self.status.elevations.append(field)
        if fieldinfo.APbylevel[3] is not None:
            self.status.action_periods.append(fieldinfo.APbylevel[3])

        
        self.status.rank = Rank.MASTER 
        # do stuff with EP? 

    # maybe go_on_horns() for nahlrout?         

    def go_insane(self, fields: "list[FieldStatus]"):
        # TODO
        self.status.is_sane = False 
        self.status.can_be_elevated = False

        for f in fields:
            f.remove_player(self)
        # self.status.EP = None # hm # still useful for DP / IP? 

        # ... other stuff? 
        self.processing.player_message.append("You went insane!")
        return 

    def break_out(self):
        # TODO
        self.status.is_sane = True
        self.status.broke_out = True
        self.processing.player_message.append("You broke out of the Crockery!!")

        # todo lodging 

        if self.status.rank is not Rank.NONE:
            self.status.rank -=1
        
            abilities_to_lose = [a for a in self.status.accessible_abilities if a.info.field_ability is not None]
            if len(abilities_to_lose) > 0:
                lost = random.choice(abilities_to_lose)
                self.processing.player_message.append(f"You lost a rank and access to the ability {lost.info.name}.")
            
                self.status.accessible_abilities.discard(lost)

        
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

        self.processing.player_message("Sorry, you died!") # todo: add dead doc link
        
        # TODO ??
    
        return

    def take_action(self, action: Action):

        self.choices.actions.append(action)
        #self.status.rank
        # Do checks to make sure the action is valid?
        # maybe do this in choices?
    
    def expel(self, fields):
        self.status.is_expelled = True
        self.status.can_file_EP = True
        self.status.can_be_elevated = False
        self.status.can_file_complaints = False

        for f in fields:
            f.remove_player(self)
        
        if self.info.social_class == Background.Vint:
            self.status.stipend = 20
        
        # anything else? 

    def add_item(self, item: Item):
        self.processing.items_received.append(item)
        if item.type.using_action is not None:
            self.status.accessible_actions.add(item.type.using_action)
        if item.type == ItemType.TENACULUM:
            self.status.accessible_actions.add(ActionType.UseTenaculumItem) # hacky but works
        
        self.status.accessible_actions.add(ActionType.GiveItem)

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
    # todo somewhere - Imre roleblock locations
    def visit_eolian(self):
        if self.status.IMRE_INFO["EOLIAN_auditioned"]:
            # cannot re-audition
            return
        
        if self.choices.IMRE_CHOICES["Eolian"]["practice"]:
            self.status.musical_stat += 0.5
            self.processing.player_message.append("You practiced for your Pipes, and improved your musical skill slightly.")
            return 
        
        if self.choices.IMRE_CHOICES["Eolian"]["audition"]:
            mstat = self.status.musical_stat

            roll = random.randint(1,10)
            pipes = False
            if roll + mstat >= 12:
                pipes = True

            if pipes:
                self.status.inventory.append(Item.Generate(ItemType.TALENTPIPES))
                self.status.has_talent_pipes = True

                self.processing.player_message.append("You won your Talent Pipes!")
            else:
                self.processing.player_message.append("You tried for your Talent Pipes, but didn't get them.")
            
            self.status.IMRE_INFO["EOLIAN_auditioned"] = True
            
            # todo log for GM
            return

    def gamble_loadeddice(self):
        if not self.choices.IMRE_CHOICES["Loaded Dice"]["place_bet"]:
            return
    
        if self.status.IMRE_INFO["LOADEDDICE_blacklistedtil"] > self.month:
            # todo log 
            print("Can't go to loaded dice yet!")
            return 
        if self.status.IMRE_INFO["LOADEDDICE_lastwon"] + 3 <= self.month:
            print("Can't go to loaded dice yet!")
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

            if self.status.IMRE_INFO["LOADEDDICE_lastwon"] + 6 <= self.month:
                self.status.IMRE_INFO["LOADEDDICE_blacklistedtil"] = self.month + 12
                # TODO log this
                
            self.processing.player_message.append(f"You went to the Loaded Dice and won! You received {winnings} talents for your gamble.") # should be in talents/etc but whatevs
        else: # lost
            self.reduce_money(bet_amt)
            self.processing.player_message.append(f"You went to the Loaded Dice and lost everything you bet.") 
    
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
        if self.holds_item(ItemType.TALENTPIPES): # ?or self.status.has_pipes
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

        self.processing.player_message.append(f"You took out a loan from Devi for {d['loan_amount']}!")

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

        self.processing.player_message.append(f"You took out a loan from Giles for {d['loan_amount']}!")

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

        self.processing.player_message.append(f"You paid Devi back {paying} and now owe her {self.status.IMRE_INFO['DEVI_amt_owed']}.")

        # return collateral if loan is entirely paid off
        if self.status.IMRE_INFO["DEVI_amt_owed"] <= 0:
            for item in self.status.IMRE_INFO["DEVI_collateral"]:
                self.add_item(item)
            
            self.processing.player_message.append(f"Since your loan has been fully paid back, she has also returned any items you gave her as collateral.")
                    
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

        self.processing.player_message.append(f"You paid Giles back {paying} and now owe her {self.status.IMRE_INFO['GILES_amt_owed']}.")

    def apoth_orders(self):
        # check in imre or whatever
        o = self.choices.IMRE_CHOICES["Apothecary"]
        # todo

    # todo place_contract? (to remove the thing that's the reward)

    def increase_money(self, amount: float):
        self.status.money += amount

    def reduce_money(self, amount: float):
        self.status.money -= amount
        if self.status.money < 0:
            print("Uh oh! I've got less than no money!")
            # todo log proper lol

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
        # todo add to field's ep listing? curr done in Turn file_EP
        self.status.EP.vals[field] += total


