class Player:
    def __init__(self, name: str):
        self.name: str = name

        self.rank = "Student"

        self.lodging = "On the streets"

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
        self.assignedDP: list[Player] = []

        self.expelled: bool = False


    
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

    def assignDP(self, total = 1):
            self.DP += total


    

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
