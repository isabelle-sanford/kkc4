### ==== Classes ==== ###
class Player:
    def __init__(self, name: str):
        self.name: str = name

        # Stored input list of who they are blocking, as Player references
        self.actions: list[Action] = []

        # Flag for whether they have been successfully blocked.
        self.isBlocked: bool = False

        # Working list of players that blocking them, as Player references
        self.blockedBy: list[Player] = []
    
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


class Test:
    def __init__(self) -> None:
        pass
    def StartTest(self, i: int) -> list[Player]:
        if i == 1:
            p1 = Player("A")
            p2 = Player("B")
            p3 = Player("C")
            p4 = Player("D")

            p1.BlockOne(p2,"Block")
            p2.BlockAll(p3)
            p3.BlockOne(p1, "Block")
            p3.BlockOne(p4, "Block")
            p4.RedirectAction(p1,p1,"Redirect")

            return [p1, p2, p3, p4]
        # elif i == 2:
        #     p1 = Player("A")
        #     p2 = Player("B")
        #     p3 = Player("C")
        #     p4 = Player("D")
        #     p5 = Player("E")
        #     p6 = Player("F")
        #     p7 = Player("G")
        #     p8 = Player("H")

        #     p1.BlockOne(p2,"Block")
        #     p2.BlockAll(p3)
        #     p3.BlockOne(p1, "Block")
        #     p3.BlockOne(p4, "Block")

        #     return [p1, p2, p3, p4, p5, p6, p7, p8]
        elif i == 3:
            p1 = Player("A")
            p2 = Player("B")
            p3 = Player("C")
            p4 = Player("D")

            p1.BlockOne(p2,"Block")
            p2.BlockAll(p3)
            p3.BlockOne(p1, "Block")
            p4.BlockOne(p1, "Block")

            return [p1, p2, p3, p4]
        elif i == 4:
            p1 = Player("A")
            p2 = Player("B")
            p3 = Player("C")
            p4 = Player("D")

            p1.BlockOne(p2,"Block")
            p2.BlockAll(p3)
            p3.BlockOne(p1, "Block")
            p3.BlockOne(p4, "Block")
            p4.BlockAll(p1)

            return [p1, p2, p3, p4]
        elif i == 5:
            p1 = Player("A")
            p2 = Player("B")
            p3 = Player("C")
            p4 = Player("D")
            p5 = Player("E")
            p6 = Player("F")
            p7 = Player("G")
            p8 = Player("H")

            p1.BlockOne(p2,"Block")
            p1.BlockAll(p5)
            p2.BlockAll(p3)
            p3.BlockOne(p4, "Block")
            p4.BlockAll(p5)
            p4.BlockAll(p2)
            p5.BlockOne(p1, "Block")
            p6.BlockOne(p7, "Block")
            p7.BlockOne(p3, "Block")
            p7.BlockAll(p1)

            return [p1, p2, p3, p4, p5, p6, p7, p8]
        elif i == 6:
            p1 = Player("A")
            p2 = Player("B")
            p3 = Player("C")
            p4 = Player("D")
            p5 = Player("E")
            p6 = Player("F")
            p7 = Player("G")
            p8 = Player("H")

            p1.BlockOne(p2,"Block")
            p1.BlockAll(p5)
            p2.BlockAll(p3)
            p3.BlockOne(p4, "Block")
            p4.BlockAll(p5)
            p4.BlockAll(p2)
            p5.BlockOne(p1, "Block")
            p6.BlockOne(p7, "Block")
            p7.BlockOne(p3, "Block")
            p7.BlockAll(p1)
            p8.BlockOne(p6, "Block")

            return [p1, p2, p3, p4, p5, p6, p7, p8]
        elif i == 7:
            p1 = Player("A")
            p2 = Player("B")
            p3 = Player("C")
            p4 = Player("D")
            p5 = Player("E")
            p6 = Player("F")
            p7 = Player("G")
            p8 = Player("H")

            p1.BlockOne(p2,"Block")
            p1.BlockAll(p3)
            p2.BlockAll(p3)
            p3.BlockOne(p1, "Block")
            p3.BlockOne(p4, "Block")
            p4.BlockAll(p1)
            p5.BlockOne(p2, "Block")
            p6.BlockOne(p7, "Block")
            p7.BlockAll(p8)

            return [p1, p2, p3, p4, p5, p6, p7, p8]
        else:
            print("Not a valid test!")

### ==== Functions ==== ###
def generateActionList(playerList: list[Player]) -> list[Action]:
    actionList: list[Action] = []
    for p in playerList:
        for a in p.actions:
            actionList.append(a)
    return actionList

def generateBlockList(actionList: list[Action]):
    blockList = []
    for a in actionList:
        if a.type.find("Block") > -1:
            blockList.append(a)
    return blockList

# Recursive function
def processUnblocked(blockList: list[Action], count = 0):
    print(f"\nInteration {count} starting...")
    gameStateChanged = False
    
    for action in blockList:
        action.clearBlockedBy()

    for action in blockList:
        action.setBlockedBy()

    for action in blockList:
        # Ignoring players who have been blocked, if the player isn't being blocked, apply their blocks.
        if not(action.blocked) and len(action.blockedBy) == 0:
            if action.type == "Block All":
                print(f"Blocking all {action.target}'s actions.")
                for a in action.target.actions:
                    if a.blocked == False:
                        a.blocked = True
                        gameStateChanged = True
            elif action.type == "Block One":
                a = action.target.FindAction("Block") # Technically different to how the BlockedBy flag is set by with SetBlockedBy()
                if a is not None:
                    print(f"Blocking {action.target}'s Block action.")
                    if a.blocked == False:
                        a.blocked = True
                        a.blockedBy = action.player # Don't know if this will have been already set...
                        gameStateChanged = True

    if gameStateChanged:
        processUnblocked(blockList, count + 1)
    print(f"... Iteration {count} finished!\n")

def processCyclicalBlock(action: Action, sequence: list[Action]):
    sequence.append(action)

    if len(action.blockedBy) == 0:
        print("[End of Chain]")
        str = "["
        for n in sequence:
            str += f"{n.player} -> "
        print(f"{str} end]")
    else:
        for attack in action.blockedByAction:
            # Dunno if this makes sense going backwards?
            if attack.blocked:
                continue
            if attack not in sequence:
                processCyclicalBlock(attack, sequence.copy())
            else:
                # From the first occurence of the duplicate to the end of the list, including self, set the "isBlocked" flag on each participant.
                str = "["
                for i in range(sequence.index(attack),len(sequence)):
                    sequence[i].inBlockCycle = True
                    str += f"{sequence[i]} -> "
                print("Iteration terminated (Cycle identified and blocked).")
                print(f"{str} {attack}]")




### ==== Runtime Code ==== ###
allPlayers: list[Player] = Test().StartTest(7)
allActions: list[Action] = generateActionList(allPlayers)
allBlocks: list[Action] = generateBlockList(allActions)

print(''.join(map(str,allBlocks)))

processUnblocked(allBlocks)

for a in allBlocks:
    processCyclicalBlock(a,[])

for a in allActions:
    if a.inBlockCycle:
        a.blocked = True

processUnblocked(allBlocks)


for p in allPlayers:
    print(f"{p.name}: isBlocked = {p.isBlocked}")
    for a in p.actions:
            print(f" - {a.name}: isBlocked = {a.blocked}")