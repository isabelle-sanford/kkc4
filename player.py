from enum import Enum, IntEnum
import random

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

class Item:
    def __init__(self) -> None:
        pass


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
    def __init__(self, name:str , rp_name:str, is_evil:bool, social_class:Background):
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


class EP:
    def __init__(self, linguistics = 0, arithemtics = 0, rhetoric = 0, archives = 0, sympathy = 0, physicking = 0, alchemy = 0, artificery = 0, naming = 0) -> None:
        self.values = [linguistics, arithemtics, rhetoric, archives, sympathy, physicking, alchemy, artificery, naming]
        
    def __str__(self) -> str:
        out = f"| Lin | Ari | R&L | Arc | Sym | Phy | ALc | Art | Nam |\n|"
        for v in self.values:
            out += f"{v: >3}  |"
        return out


class PlayerStatus:

    # input from GM distribution 
    def __init__(
        self, player_static, current_lodging, musical_stat, inventory, current_funds
    ):
        self.info = player_static # Do we need this here?
        self.available_EP = 5
        self.rank = Rank.NONE

        self.lodging = current_lodging
        self.money = current_funds 

        self.musical_stat = musical_stat
        self.inventory: list[Item] = [inventory] # questionable

        self.EP: EP = EP() 
        self.elevations = []
        self.MasterOf: FieldName = None # 4th elevation is equivalent I guess?

        self.is_alive = True 
        self.is_sane = True
        self.is_expelled = False 
        self.is_enrolled = True 
        self.in_Imre = False

        self.complaintsBlocked = False # Set when target of Argumentum Ad Nauseam.

        # IMRE
        self.IMRE_EOLIAN_Auditioned: bool = False
        
        self.IMRE_GILES_Defaulted: bool = False
        self.IMRE_GILES_AmountOwed: float = 0.0
        self.IMRE_DEVI_Defaulted: bool = False
        self.IMRE_DEVI_AmountOwed: float = 0.0
        self.IMRE_DEVI_Collateral: list[Item] = []

        self.IMRE_BLACKMARKET_ContractLog: list[Item] = []

        # Working Vars
        # List of complaints recieved
        self.complaintsReceived: list[Player] = []

        # Total DP
        self.DP: int = 0

        # Flag for whether they have been successfully blocked.
        self.isBlocked: bool = False

        # Working list of players that blocking them, as Player references
        self.blockedBy: list[Player] = []



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

        self.assignedDP: list[Player] = []

        # IMRE
        self.IMRE_EOLIAN_Audition: bool = False
        self.IMRE_EOLIAN_Practice: bool = False

        self.IMRE_DEVI_AcquireLoan: bool = False
        self.IMRE_DEVI_GiveCollateral: list[Item] = []
        self.IMRE_DEVI_LoanAmount: float =  0.0
        # Do you actively choose to pay the loan or is it direct debit?

        self.IMRE_GILES_AcquireLoan: bool = False
        self.IMRE_GILES_LoanAmount: float =  0.0

        self.IMRE_LOADEDDICE_PlacedBet: bool = False
        self.IMRE_LOADEDDICE_BetAmount: float = 0.0
        self.IMRE_LOADEDDICE_Numbers: list[int] = []

        self.IMRE_APOTHECARY_Nahlrout: int = 0
        self.IMRE_APOTHECARY_Couriers: list[str] = []
        self.IMRE_APOTHECARY_Bloodless: int = 0
        self.IMRE_APOTHECARY_Gram: int = 0

        self.IMRE_BLACKMARKET_Mommet: list[Player] = [] # or list[Item]
        self.IMRE_BLACKMARKET_Bodyguard: int = 0
        self.IMRE_BLACKMARKET_Assassin: list[Player] = []
        self.IMRE_BLACKMARKET_TakeContract: list[Item] = []
        self.IMRE_BLACKMARKET_PlaceContract: list[Item] = []




        

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
    #     line2 = f"EP filed: {[s.name for s in self.EP_filed]}\n" # ! fix later
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

    def TakeAction(self, action):
        self.choice.actions.append(action)
        # Do checks to make sure the action is valid?
    
    def BlockAll(self, target):
        self.TakeAction(Action("Mommet", self,"Block All",target))
    
    def BlockOne(self, target, actionType: str):
        self.TakeAction(Action("Tenaculum", self,"Block One", target, actionType=actionType))
    
    def RedirectAction(self, fromTarget, toTarget, actionType: str):
        self.TakeAction(Action("Law of Contraposition", self, "RedirectAction", fromTarget, toTarget, actionType))

    def FindAction(self, type: str):
        for a in self.choice.actions:
            if a.type.find(type) > -1:
                return a
        return None  
    
    def ImportComplaint(self, target):
        self.choice.complaints.append(target)

    def assignDP(self, total = 1, masterOf:FieldName = None):
            if masterOf is not None:
                print(f"Master {masterOf.name} assigning DP to {self.info.name}, with {self.status.EP.values[masterOf]} EP in {masterOf.name}")
                self.status.EP.values[masterOf] -= total
                if self.status.EP.values[masterOf] < 0:
                    self.status.DP -= self.status.EP.values[masterOf]
                    self.status.EP.values[masterOf] = 0
            else:
                self.status.DP += total

    def assignEP(self, field, total = 1):
        self.status.EP.values[field-1] += total


# a = Player()

class Action:
    def __init__(self, iName: str, iPlayer: Player, iType, iTarget: Player, iTarget2: Player = None, actionType: str = None):
        self.name: str = iName # Action name
        self.player: Player = iPlayer # Player taking the action
        self.type: str = iType # Type of action: Block, Redirect, Kill, etc.
        self.targetActionType: str = actionType
        self.target: Player = iTarget
        self.target2: Player = iTarget2

        self.blocked: bool = False
        self.redirected: bool = False
        self.redirectTarget: Player

        # Working variables to process cycles and chains
        self.blockedBy: list[Player] = []
        self.blockedByAction: list[Action] = []
        self.inBlockCycle: bool = False
    
    def __str__(self) -> str:
        return f"{self.player.info.name}: {self.name} "
    
    def clearBlockedBy(self):
        self.blockedBy: list[Player] = []
        self.blockedByAction: list[Action] = []
        # clear the blockedBy flag on players?

    def setBlockedBy(self):
        if not self.blocked:    
            if self.type.find("Block") < 0:
                # print("Not a block action.")
                return
            
            # Dunno if we just set the player flag, set the player and all action flags, or just the action flags.
            if self.type == "Block All":
                self.target.status.blockedBy.append(self.player)
                # print(f"{self.player} blocks all {self.target}'s actions")
                for a in self.target.choice.actions:
                    a.blockedBy.append(self.player)
                    a.blockedByAction.append(a)
                    # print(f"-- {a.name} blocked.")

            elif self.type == "Block One":
                for a in self.target.choice.actions:
                    if a.type.find(self.targetActionType) >= 0:
                        a.blockedBy.append(self.player)
                        a.blockedByAction.append(a)
                        # print(f"{self.player} blocked {self.target}'s {a.type} action.")
                        return
                # print("No relevant actions found.")


class PlayerRandom:
    def __init__(self) -> None:
        pass

    def Generate(self, name:str) -> Player:
        static = PlayerStatic(name, name, random.choice([True,False]),random.choice(list(Background)))
        status = PlayerStatus(static,random.choice(list(Lodging)),random.randint(1,20),[],random.random()*20.0)
        choice = PlayerChoices()

        return Player(static,status,choice)