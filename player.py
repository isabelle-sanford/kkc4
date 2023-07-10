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
                 social_class:Background, id:int = 0):
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
        
        # todo: figure out where this is used and remove, probably?
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

        s.musical_stat = musical_stat
        s.inventory: list[Item] = [inventory] # questionable

        s.EP: EP = EP() 
        s.elevations: list[FieldName] = []
        s.master_of: FieldName = None # 4th elevation is equivalent I guess?

        s.is_alive = True 
        s.is_sane = True
        s.is_expelled = False 
        s.is_enrolled = True 
        s.in_Imre = False

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

    def __copy__(self):
        next = PlayerStatus(self.info)
        next.month = self.month + 1
        next.available_EP = self.available_EP
        next.rank = self.rank 
        next.lodging = self.lodging 
        next.money = self.money
        next.stipend = self.stipend
        next.musical_stat = self.musical_stat
        next.inventory = self.inventory
        next.EP = self.EP
        next.elevations = self.elevations
        next.master_of = self.master_of
        next.is_alive = self.is_alive
        next.is_sane = self.is_sane 
        next.is_expelled = self.is_expelled
        next.is_enrolled = self.is_enrolled
        next.in_Imre = self.in_Imre

        next.IMRE_INFO = self.IMRE_INFO

# working variables for processing turn
class PlayerProcessing:
    def __init__(self, player_static, month):
        self.info = player_static
        self.month = month

        self.complaints_blocked = False # Set when target of Argumentum Ad Nauseam.
        self.complaints_received: list[Player] = []
        
        # Total DP
        self.DP: int = 0

        # Flag for whether they have been successfully blocked.
        self.is_blocked: bool = False

        # Working list of players that blocking them, as Player references
        self.blocked_by: list[Player] = []

        self.transfer_neg_actions_to = None
        

        self.can_file_complaints: bool = True

        self.can_be_targeted: bool = True

        self.protected_from_sabotage = 0
        self.protected_from_kill = 0
        self.protects = [] # hmm

class PlayerChoices:
    # basically a record of what things a player wants to do this turn
    # and funcs returning false if the player can't do those things
    # choices are actually processed and integrated to the overall game separately 
    
    def __init__(self, playerstatic, month: int = 0):
        self.player_static = playerstatic
        self.month = month
        # if self.player.available_EP > 0:
        #     self.EP_filed = [FieldName.GENERAL] * self.player.available_EP # ?? ew
        
        # if self.month % 3 == 0:
        #     self.next_lodging = streets # ! change to enum val probs

        self.imre_next = False # should check if in imre lodging 

        # List of complaints made (NOT including PiH)
        self.complaints: list[Player] = []

        # Stored input list of who they are blocking, as Player references
        self.actions: list[Action] = []

        # if master 
        self.assigned_DP: list[Player] = []

        # IMRE
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

    # def take_action

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

    def __init__(self, player_static: PlayerStatic, player_status: PlayerStatus, player_choices: PlayerChoices = None, player_process: PlayerProcessing = None):
        self.status: PlayerStatus = player_status
        self.info: PlayerStatic = player_static 
        self.choice: PlayerChoices = player_choices
        self.id: int = player_static.id
        self.name: str = player_static.name
        self.month = player_status.month # hmm

        if player_process is None:
            player_process = PlayerProcessing(player_static, self.month)
        self.processing: PlayerProcessing = player_process

    def take_action(self, action: Action):

        self.choice.actions.append(action)
        self.status.rank
        # Do checks to make sure the action is valid?
    
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
        for a in self.choice.actions:
            if a.type.find(type) > -1:
                return a
        return None  
    
    def import_complaint(self, target):
        self.choice.complaints.append(target)

    def assign_DP(self, total = 1, master_of:FieldName = None):
            if master_of is not None:
                print(f"Master {master_of.name} assigning DP to {self.info.name}, with {self.status.EP.values[master_of]} ep in {master_of.name}")
                self.status.EP.values[master_of] -= total
                if self.status.EP.values[master_of] < 0:
                    self.status.DP -= self.status.EP.values[master_of]
                    self.status.EP.values[master_of] = 0
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