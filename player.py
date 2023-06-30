from enum import IntEnum

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

class Player:
    def __init__(self, name: str):
        self.name: str = name

        self.rank = "Student"

        self.lodging = "On the streets"

        self.expelled: bool = False

        self.EP: Fields = Fields()


        # Stored input list of who they are blocking, as Player references
        self.actions: list[Action] = []

        # Flag for whether they have been successfully blocked.
        self.isBlocked: bool = False

        # Working list of players that blocking them, as Player references
        self.blockedBy: list[Player] = []

        # List of complaints made
        self.complaints: list[Player] = []

        # List of complaints recieved
        self.complaintsReceived: list[Player] = []


        # Total DP
        self.DP: int = 0
        
        # For Masters:
        self.MasterOf: FieldName = None
        self.assignedDP: list[Player] = []

        
    
    def __str__(self) -> str:
        return self.name

    def TakeAction(self, action):
        self.actions.append(action)
        # Do checks to make sure the action is valid?
    
    def BlockAll(self, target):
        self.TakeAction(Action("Mommet", self,"Block All",target))
    
    def BlockOne(self, target, actionType: str):
        self.TakeAction(Action("Tenaculum", self,"Block One", target, actionType=actionType))
    
    def RedirectAction(self, fromTarget, toTarget, actionType: str):
        self.TakeAction(Action("Law of Contraposition", self, "RedirectAction", fromTarget, toTarget, actionType))

    def FindAction(self, type: str):
        for a in self.actions:
            if a.type.find(type) > -1:
                return a
        return None  
    
    def ImportComplaint(self, target):
        self.complaints.append(target)

    def assignDP(self, total = 1, masterOf:FieldName = None):
            if masterOf is not None:
                print(f"Master {masterOf.name} assigning DP to {self.name}, with {self.EP.values[masterOf]} EP in {masterOf.name}")
                self.EP.values[masterOf] -= total
                if self.EP.values[masterOf] < 0:
                    self.DP -= self.EP.values[masterOf]
                    self.EP.values[masterOf] = 0
            else:
                self.DP += total

    def assignEP(self, field, total = 1):
        self.EP.values[field-1] += total
    

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
        return f"{self.player}: {self.name} "
    
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
                self.target.blockedBy.append(self.player)
                # print(f"{self.player} blocks all {self.target}'s actions")
                for a in self.target.actions:
                    a.blockedBy.append(self.player)
                    a.blockedByAction.append(a)
                    # print(f"-- {a.name} blocked.")

            elif self.type == "Block One":
                for a in self.target.actions:
                    if a.type.find(self.targetActionType) >= 0:
                        a.blockedBy.append(self.player)
                        a.blockedByAction.append(a)
                        # print(f"{self.player} blocked {self.target}'s {a.type} action.")
                        return
                # print("No relevant actions found.")


class Fields:
    def __init__(self, linguistics = 0, arithemtics = 0, rhetoric = 0, archives = 0, sympathy = 0, physicking = 0, alchemy = 0, artificery = 0, naming = 0) -> None:
        # self.Linguistics = linguistics
        # self.Arithmetics = arithemtics
        # self.RhetoricAndLogic = rhetoric
        # self.Archives = archives
        # self.Sympathy = sympathy
        # self.Physicking = physicking
        # self.Alchemy = alchemy
        # self.Artificery = artificery
        # self.Naming = naming

        # self.values = [self.Linguistics, self.Arithmetics, self.RhetoricAndLogic, self.Archives, self.Sympathy, self.Physicking, self.Alchemy, self.Artificery, self.Naming]
        self.values = [linguistics, arithemtics, rhetoric, archives, sympathy, physicking, alchemy, artificery, naming]
        
    def __str__(self) -> str:
        out = f"| Lin | Ari | R&L | Arc | Sym | Phy | ALc | Art | Nam |\n|"
        for v in self.values:
            out += f"{v: >3}  |"
        return out
    

