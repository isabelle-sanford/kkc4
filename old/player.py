import random, math
from enum import Enum, IntEnum

class Rank(IntEnum):
    NONE = 0 #?
    ELIR = 1
    RELAR = 2
    ELTHE = 3
    MASTER = 4

class FieldName(IntEnum):
    LINGUISTICS = 1
    ARITHMETICS = 2
    RHETORICLOGIC = 3
    ARCHIVES = 4
    SYMPATHY = 5
    PHYSICKING = 6
    ALCHEMY = 7
    ARTIFICERY = 8
    NAMING = 9
    GENERAL = 10  # ? 0? 

class ItemType(Enum):
    MOMMET = 1
    TENACULUM = 2
    FIRESTOP = 3
    PLUMBOB = 4
    BONETAR = 5
    WARD = 6
    BLOODLESS = 7
    THIEVESLAMP = 8
    GRAM = 9
    TALENTPIPES = 10
    NAHLROUT = 11
    BODYGUARD = 12



class Item:
    def __init__(self, name, type: ItemType, uses, defense, action, level, target= None) -> None:
        self.type: ItemType = type

        self.name: str = name
        self.uses: int = uses # Can be None
        self.defense: bool = defense
        self.action: bool = action
        self.level: int = level # Can be None
        self.target: Player = target #None except when mommet

    @classmethod
    def Generate(cls, type: ItemType, level: int = 0, target = None):
        if type == ItemType.MOMMET:
            return Item("Mommet", type, 1, False, True, level, target)
        elif type == ItemType.TENACULUM:
            uses = 1
            if level == 4: uses = 2
            return Item("Tenaculum", type, uses, False, True, level)
        elif type == ItemType.FIRESTOP:
            uses = 1
            if level == 4: uses = 2
            return Item("Firestop", type, uses, True, False, level)
        elif type == ItemType.PLUMBOB:
            return Item("Plumbob", type, 1, False, True, level)
        elif type == ItemType.BONETAR:
            return Item("Bonetar", type, 1, False, True, level)
        elif (type == ItemType.WARD or type == ItemType.BLOODLESS 
              or type == ItemType.THIEVESLAMP or type == ItemType.GRAM):
            if level == 2: uses = random.randrange(1,2)
            elif level == 3: uses = 2
            elif level == 4: uses = 3
            else: uses = 1
            if type == ItemType.WARD:
                return Item("Ward", type, uses,True,True,level)
            elif type ==  ItemType.BLOODLESS:
                return Item("Bloodless", type, uses, True, False, level)
            elif type == ItemType.THIEVESLAMP:
                return Item("Thieve's Lamp", type, uses, False, True, level)
            else: # Gram
                return Item("Gram", type, uses, True, False, level) 
        elif type == ItemType.TALENTPIPES:
            return Item("Talent Pipes", type, None, False, False, None)
        elif type == ItemType.NAHLROUT:
            return Item("Nahlrout", type, 1, True, True, None)
        elif type == ItemType.BODYGUARD:
            return Item("Bodyguard", type, 2,True,False,None)
        


    


# Could be worth trying this: https://stackoverflow.com/questions/6060635/convert-enum-to-int-in-python
# I.E. use aenum, though does mean using an additional package beyond the stdlib
class Lodging(Enum):
    Streets = 0, "The Streets", 0
    Underthing = 1, "The Underthing", 0
    Mews = 2, "Mews", 1
    Ankers = 3, "Ankers", 4
    KingsDrab = 4, "The King's Drab", 6
    GreyMan = 5, "The Grey Man", 7
    GoldenPony = 6, "The Golden Pony", 8
    WindyTower = 7, "The Windy Tower", 9
    HorseAndFour = 8, "The Horse and Four", 10
    PearlOfImre = 9, "The Pearl of Imre", 11
    SpindleAndDraft = 10, "The Spindle and Draft", 12

    def __new__(cls, value, name, cost):
        member = object.__new__(cls)
        member._value_ = value
        member.fullname = name
        member.price = cost
        return member

    def __int__(self):
        return self.value
    
    def __str__(self):
        return f"{self.fullname} ({self.price} talents)"



class Background(Enum): 
    Vint = 0, "Vintish Nobleman", 20, 30, [Lodging.HorseAndFour, Lodging.SpindleAndDraft]
    Aturan = 1, "Aturan Nobleman", 13.34, 20, [Lodging.WindyTower, Lodging.HorseAndFour]
    Yll = 2, "Yllish Commoner", 7.49, 11.23, [Lodging.GoldenPony, Lodging.WindyTower]
    Ceald = 3, "Cealdish Commoner", 6.58, 9.87, [Lodging.KingsDrab, Lodging.GoldenPony]
    Ruh = 4, "Edema Ruh", 3.4, 5.67, [Lodging.Ankers, Lodging.KingsDrab]

    def __new__(cls, value, name, initalFunds, stipend, lodging):
        member = object.__new__(cls)
        member._value_ = value
        member.fullname = name
        member.initalFunds = initalFunds
        member.stipend = stipend
        member.lodging = lodging
        return member

    def __int__(self):
        return self.value
    
    def __str__(self) -> str:
        return f"{self.fullname}"



class PlayerStatic:
    def __init__(self, name:str , rp_name:str, is_evil:bool, 
                 social_class:Background):
        # ? id? 
        self.name: str = name 
        self.rp_name: str = rp_name
        self.is_evil: bool = is_evil # or could be skindancer
        self.social_class: Background = social_class
    
    def __str__(self):
        ret = f"Player: {self.name} ({self.rp_name}) - {self.social_class} - "
        ret += "Skindancer" if self.is_evil else "Student"
        ret += "\n"
        return ret


class ep:
    def __init__(self, linguistics = 0, arithemtics = 0, rhetoric = 0, 
                 archives = 0, sympathy = 0, physicking = 0, alchemy = 0,
                   artificery = 0, naming = 0) -> None:
        self.values = [linguistics, arithemtics, rhetoric, archives, sympathy,
                        physicking, alchemy, artificery, naming]
        
    def __str__(self) -> str:
        out = f"| Lin | Ari | R&L | Arc | Sym | Phy | ALc | Art | Nam |\n|"
        for v in self.values:
            out += f"{v: >3}  |"
        return out


class PlayerStatus:

    # input from GM distribution 
    def __init__(
        self, player_static, current_lodging, musical_stat, inventory, 
        current_funds
    ):
        self.info = player_static # Do we need this here?
        self.available_EP = 5
        self.rank = Rank.NONE

        self.lodging = current_lodging
        self.money = current_funds 

        self.musical_stat = musical_stat
        self.inventory: list[Item] = [inventory] # questionable

        self.EP: ep = ep() 
        self.elevations = []
        self.master_of: FieldName = None # 4th elevation is equivalent I guess?

        self.is_alive = True 
        self.is_sane = True
        self.is_expelled = False 
        self.is_enrolled = True 
        self.in_Imre = False

        self.complaints_blocked = False # Set when target of Argumentum Ad Nauseam.

        # IMRE
        self.IMRE_EOLIAN_auditioned: bool = False
        
        self.IMRE_GILES_defaulted: bool = False
        self.IMRE_GILES_amount_owed: float = 0.0
        self.IMRE_DEVI_defaulted: bool = False
        self.IMRE_DEVI_amount_owed: float = 0.0
        self.IMRE_DEVI_collateral: list[Item] = []

        self.IMRE_BLACKMARKET_ContractLog: list[Item] = []

        # Working Vars
        # List of complaints recieved
        self.complaints_received: list[Player] = []

        # Total DP
        self.DP: int = 0

        # Flag for whether they have been successfully blocked.
        self.is_blocked: bool = False

        # Working list of players that blocking them, as Player references
        self.blocked_by: list[Player] = []



class PlayerChoices:
    # basically a record of what things a player wants to do this turn
    # and funcs returning false if the player can't do those things
    # choices are actually processed and integrated to the overall game separately 
    
    def __init__(self):

        # if self.player.available_EP > 0:
        #     self.EP_filed = [FieldName.GENERAL] * self.player.available_EP # ?? ew
        
        # if self.month % 3 == 0:
        #     self.next_lodging = streets # ! change to enum val probs

        self.imre_next = False # should check if in imre lodging 

        # List of complaints made
        self.complaints: list[Player] = []

        # Stored input list of who they are blocking, as Player references
        self.actions: list[Action] = []

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

    def __init__(self, player_static: PlayerStatic, player_status: PlayerStatus, player_choices: PlayerChoices):
        self.status: PlayerStatus = player_status
        self.info: PlayerStatic = player_static 
        self.choice: PlayerChoices = player_choices

    def take_action(self, action):
        self.choice.actions.append(action)
        # Do checks to make sure the action is valid?
    
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


# a = Player()

class Action:
    def __init__(self, name: str, player: Player, type, target: Player,
                  target_two: Player = None, action_type: str = None):
        self.name: str = name # Action name
        self.player: Player = player # Player taking the action
        self.type: str = type # Type of action: Block, Redirect, Kill, etc.
        self.target_action_type: str = action_type
        self.target: Player = target
        self.target_two: Player = target_two

        self.blocked: bool = False
        self.redirected: bool = False
        self.redirect_target: Player

        # Working variables to process cycles and chains
        self.blocked_by: list[Player] = []
        self.blocked_by_action: list[Action] = []
        self.in_block_cycle: bool = False
    
    def __str__(self) -> str:
        return f"{self.player.info.name}: {self.name} "
    
    def clear_blocked_by(self):
        self.blocked_by: list[Player] = []
        self.blocked_by_action: list[Action] = []
        # clear the blocked_by flag on players?

    def set_blocked_by(self):
        if not self.blocked:    
            if self.type.find("Block") < 0:
                # print("Not a block action.")
                return
            
            # Dunno if we just set the player flag, set the player and
            #  all action flags, or just the action flags.
            if self.type == "Block All":
                self.target.status.blocked_by.append(self.player)
                # print(f"{self.player} blocks all {self.target}'s actions")
                for a in self.target.choice.actions:
                    a.blocked_by.append(self.player)
                    a.blocked_by_action.append(a)
                    # print(f"-- {a.name} blocked.")

            elif self.type == "Block One":
                for a in self.target.choice.actions:
                    if a.type.find(self.target_action_type) >= 0:
                        a.blocked_by.append(self.player)
                        a.blocked_by_action.append(a)
                        # print(f"{self.player} blocked {self.target}'s {a.type} action.")
                        return
                # print("No relevant actions found.")


class PlayerRandom:
    def __init__(self) -> None:
        pass

    def Generate(self, name:str) -> Player:
        static = PlayerStatic(name, name, random.choice([True,False]),random.choice(list(Background)))
        status = PlayerStatus(static,random.choice(list(Lodging)),random.randint(1,20),[],round(random.random()*20.0,2))
        choice = PlayerChoices()

        return Player(static,status,choice)