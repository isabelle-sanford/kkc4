from enum import Enum
import random 

from statics import Background, Lodging
from actions import ActionType, Action
from field import Rank, FieldName
from items import ItemType, Item

class BaseStat(Enum):
    MUSIC = 1
    ESSAY = 2
    ART = 3


class PlayerStatic:
    def __init__(self, name:str , rp_name:str, is_evil:bool, 
                 social_class:Background, id:int = -1):
        # ? id?  TODO
        self.id = id
        self.name: str = name 
        self.rp_name: str = rp_name
        self.is_evil: bool = is_evil # or could be skindancer
        self.social_class: Background = social_class
        # ! base stat? 
    
    def __str__(self):
        ret = f"Player: {self.name} ({self.rp_name}) - {self.social_class} - "
        ret += "Skindancer" if self.is_evil else "Student"
        ret += "\n"
        return ret
    
class EP:
    def __init__(self, linguistics = 0, arithemtics = 0, rhetoric = 0, 
                 archives = 0, sympathy = 0, physicking = 0, alchemy = 0,
                   artificery = 0, naming = 0) -> None:
        
       
        self.values = [linguistics, arithemtics, rhetoric, archives, sympathy,
                        physicking, alchemy, artificery, naming]
        # self.linguistics = linguistics
        # self.arithemtics = arithemtics
        # self.rhetoric = rhetoric 
        # self.archives = archives
        # self.sympathy = sympathy
        # self.physicking = physicking
        # self.alchemy = alchemy 
        # self.artificery = artificery
        # self.naming = naming 
        
    def __str__(self) -> str:
        out = f"| Lin | Ari | R&L | Arc | Sym | Phy | Alc | Art | Nam |\n|"
        for v in self.values:
            out += f"{v: >3}  |"
        return out

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
        s.month = 0
        s.available_EP = 5
        s.rank = Rank.NONE

        s.lodging: Lodging = current_lodging
        s.money = player_static.social_class.initial_funds 
        s.stipend = player_static.social_class.stipend
        s.current_tuition = 10

        s.musical_stat = musical_stat
        s.inventory: list[Item] = [inventory] # questionable
        # should bodyguard be in inventory or separate?

        s.EP: EP = EP() 
        s.elevations: list[FieldName] = []
        s.master_of: FieldName = None # 4th elevation is equivalent I guess?

        s.is_alive = True 
        s.is_sane = True
        s.is_expelled = False 
        s.is_enrolled = True 
        s.in_Imre = False

        # things the player knows / happened prev turn
        # so their page can have invalid stuff grayed out or whatever
        s.can_take_actions = True 
        s.can_file_complaints = True 
        s.can_file_EP = True 
        s.can_be_targeted = True # medica emergency (only?)
        # is lashed? 

        s.accessible_abilities: list[ActionType] = []
        s.known_names = [] # ? (for breakout roll)

        # are there any other prev turn effects? 
        # this is the best way I could come up with to have effects into future turns
        s.last_reckless_use = -1 # successful - nahlrout protected doesn't count here
        s.last_conduct_unbecoming = -1
        s.last_volatile_firestop = -1
        s.last_medica_emergency = -1 # 
        s.last_in_medica = -1 # for bonetar ig

        # IMRE
        # hmmmm - could make own class? 
        s.IMRE_INFO = {
            "EOLIAN_auditioned": False,
            "GILES_defaulted": False,
            "GILES_amt_owed": 0.0,
            "DEVI_defaulted": False,
            "DEVI_collateral": [],
            "BLACKMARKET_Contractlog": []
        }

        # s.IMRE_EOLIAN_auditioned: bool = False
        
        # s.IMRE_GILES_defaulted: bool = False
        # s.IMRE_GILES_amount_owed: float = 0.0
        # s.IMRE_DEVI_defaulted: bool = False
        # s.IMRE_DEVI_amount_owed: float = 0.0
        # s.IMRE_DEVI_collateral: list[Item] = []

        # s.IMRE_BLACKMARKET_ContractLog: list[Item] = []

        return s
    
    # TODO string / print func 

    # todo change stipend for vint/aturan


# working variables for processing turn
class PlayerProcessing:
    def __init__(self, player_info, player_status, player_choices, month):
        self.info = player_info
        self.starting_status = player_status
        self.month = month
        self.choices = player_choices
        # also want ending_status?

        self.complaints_blocked = False # Set when target of Argumentum Ad Nauseam.
        self.complaints_received: list[Player] = []
        self.processed_complaints = self.choices.complaints # todo should initially set as original complaints
        
        # Total DP
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
        
        self.can_file_complaints: bool = self.starting_status.can_file_complaints # should also reference status
        self.can_file_EP: bool = self.starting_status.can_file_EP
        self.can_be_targeted: bool = self.starting_status.can_be_targeted
        # can_elevate? 

        # should probably instead process protects with kills, so they happen in appropriate order
        self.protected_from_sabotage = 0
        self.protected_from_kill = 0
        self.protects = [] # hmm

        self.items_received: list[Item] = []
        # todo remember to add this ^ to next_status

        self.getting_elevated_in: FieldName = None

        self.insanity_bonus = 0 # might want to take something from prev status?
        # and check mews

class PlayerChoices:
    # basically a record of what things a player wants to do this turn
    # and funcs returning false if the player can't do those things (?)
    # choices are actually processed and integrated to the overall game separately 
    # it's essentially just the info submitted from the player's page

    def __init__(self, playerstatic, month: int = 0):
        self.player_static = playerstatic
        self.month = month
        # maybe also status here? 

        if self.month % 3 == 0:
            self.next_lodging: Lodging = Lodging.Streets

        self.imre_next = False # should check if in imre lodging?
        self.enroll_next = True # check expulsion etc 

        # List of complaints made (NOT including PiH)
        self.complaints: list[Player] = []

        # Stored input list of who they are blocking, as Player references
        self.actions: list[Action] = []

        self.filing_EP: list[FieldName] = []

        # if master 
        self.assigned_DP: list[Player] = []
        self.to_elevate: list[Player] = [] # ordered preference list

        # IMRE (check if player is there?)
        # also again maybe change to dict, this is really messy
        self.IMRE_EOLIAN_audition: bool = False
        self.IMRE_EOLIAN_practice: bool = False

        self.IMRE_DEVI_acquire_loan: bool = False
        self.IMRE_DEVI_give_collateral: list[Item] = []
        self.IMRE_DEVI_loan_amount: float =  0.0
        # Do you actively choose to pay the loan or is it direct debit?

        self.IMRE_GILES_acquire_loan: bool = False
        self.IMRE_GILES_loan_amount: float =  0.0

        self.IMRE_LOADEDDICE_placed_bet: bool = False
        self.IMRE_LOADEDDICE_bet_amount: float = 0.0
        self.IMRE_LOADEDDICE_numbers: list[int] = []

        self.IMRE_APOTHECARY_nahlrout: int = 0
        self.IMRE_APOTHECARY_couriers: list[str] = []
        self.IMRE_APOTHECARY_bloodless: int = 0
        self.IMRE_APOTHECARY_gram: int = 0

        self.IMRE_BLACKMARKET_mommet: list[Item] = []
        self.IMRE_BLACKMARKET_bodyguard: int = 0
        self.IMRE_BLACKMARKET_assassin: list[Player] = []
        self.IMRE_BLACKMARKET_take_contract: list[Item] = []
        self.IMRE_BLACKMARKET_place_contract: list[Item] = []
 
    def __str__(self) -> str:
        # TODO

        ret = f"{self.player_static.name}: complaints {self.complaints}"

        return ret

    # helper function to add multiple maybe? 
    # def file_EP(self, field, slot): 
    #     if slot >= self.player.available_EP: return False 

    #     if field in FieldName: # ? 
    #         self.EP_filed[slot] = field
    
    # def go_to_Imre(self):
    #     # TODO 
    #     self.imre_next = True


    # def set_next_lodging(self, lodging):
    #     if self.month % 3 == 0:
    #         self.next_lodging = lodging
    #     else:
    #         return False 
    
    # def enroll_next(self):
    #     if self.player.is_expelled: # is this enough? 
    #         self.enroll_next_term = True
    #     else:
    #         return False 


    # def __str__(self):
    #     # this is probably not ideal :p
    #     line1 = f"Player: {self.info.name}  Month: {self.month}\n"
    #     line2 = f"ep filed: {[s.name for s in self.EP_filed]}\n" # ! fix later
    #     line3 = f"Going to Imre next month: {self.imre_next}\n"
        
    #     return line1 + line2 + line3

    # todo vote

    # todo imre stuff
        # practice / play @ the eolian (play_pipes, practice_pipes)
        # apothecary (buy_item)
        # buy assassin/bodyguard/sold items (buy_contract)
        # give_contract / take_contract (need a "taken_contracts" attribute probs)
        # loaded dice nums 
        # devi/giles loan 

class Player:

    # start of game constructor 
    def __init__(self, player_static: PlayerStatic, player_status: PlayerStatus, player_choices: PlayerChoices = None, player_process: PlayerProcessing = None):
        self.initial_status: PlayerStatus = player_status
        self.info: PlayerStatic = player_static 

        if player_choices is None:
            player_choices = PlayerChoices(player_static, 0)
        self.choices: PlayerChoices = player_choices # renamed this, hopefully it stuck

        # self.past_statuses = [] ? 
        
        # sort of irregularly used, but maybe more helpful than passing full Player instances around everywhere
        self.id: int = player_static.id 
        self.name: str = player_static.name
        self.month = 0 # hmm

        # need to remember to make new processing objects per turn
        if player_process is None:
            player_process = PlayerProcessing(player_static, player_status, player_choices, self.month)
        self.status: PlayerProcessing = player_process

    def levels_in(self, field: FieldName):
        # error check?
        count = self.status.elevations.count(field)
        if self.status.master_of == field:
            count = 4
        return count

    def elevate_in(self, field: FieldName):
        self.status.elevations.append(field)
        num_EP = self.status.EP.values[field]
        if num_EP < 5:
            self.status.EP.values[field] = 0
        else:
            self.status.EP.values[field] -= 5
        
        #self.status.rank = self.status.rank.next() # todo test 
        self.status.available_EP -= 1

        # anything else here? 
    # todo go_insane()
    # todo break_out()
    # todo calculate_tuition(gm_input)
        # remember to check masters, social class, arithmetics
        # probs have Tuition object that can be updated over turns?

# everything below here untouched since haelbarde branch (except assign_DP)
    def take_action(self, action: Action):

        self.choices.actions.append(action)
        self.status.rank
        # Do checks to make sure the action is valid?
        # maybe do this in choices?
    
    def add_item(self, item: Item):
        self.status.inventory.append(Item)

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
                print(f"Master {master_of.name} assigning DP to {self.info.name}, with {self.status.EP.values[master_of]} ep in {master_of.name}")
                
                num_EP = self.status.ep.values[master_of]
                
                if num_EP > 0:
                    diff = num_EP - total
                    if diff >= 0: # at least as much EP as DP
                        self.status.EP.values[master_of.name] -= total # or = diff
                        total = 0
                    else:
                        total -= num_EP # or = -diff
                        self.status.EP.values[master_of] = 0
                
                self.status.DP += total
                
            else:
                self.status.DP += total

    def assign_EP(self, field, total = 1):
        self.status.EP.values[field-1] += total

class PlayerRandom:
    def __init__(self) -> None:
        pass

    def Generate(self, name:str) -> Player:
        static = PlayerStatic(name, name, random.choice([True,False]),random.choice(list(Background)))
        status = PlayerStatus(static,random.choice(list(Lodging)),random.randint(1,20),[],round(random.random()*20.0,2))
        choice = PlayerChoices()

        return Player(static,status,choice)