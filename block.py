from player import Player, Action

### ==== Functions ==== ###
def generateActionList(playerList: list[Player]) -> list[Action]:
    actionList: list[Action] = []
    for p in playerList:
        for a in p.choice.actions:
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
                print(f"Blocking all {action.target.info.name}'s actions.")
                for a in action.target.choice.actions:
                    if a.blocked == False:
                        a.blocked = True
                        gameStateChanged = True
            elif action.type == "Block One":
                a = action.target.FindAction("Block") # Technically different to how the BlockedBy flag is set by with SetBlockedBy()
                if a is not None:
                    print(f"Blocking {action.target.info.name}'s Block action.")
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
            str += f"{n.player.info.name} -> "
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
                    str += f"{sequence[i].player.info.name} -> "
                print("Iteration terminated (Cycle identified and blocked).")
                print(f"{str} {attack}]")

def processRedirectBlocks(actionList: list[Action]):
    for a in actionList:
        if a.type.find("Redirect") > -1:
            # Do we need to specify Redirect Block specifically?
            for b in a.target.choice.actions:
                if (b.type.find("Block") > -1) and (b.target == a.player):
                        # Redirect the block now.
                        b.redirected = True
                        b.redirectTarget = a.target2
                        # Do we need a "action processed flag"?
            


### ==== Runtime Code ==== ###
# 1. Check for redirects & blocks that target each other and redirect the block.
# 2. Check for redirect/block chains and process from the start of the chain forwards.
# --> Actually, this is still just the recursive unblocked/redirected things triggering in turn. 
# --> Need a check to see if it has a redirect targetting it?
# ----> Needs to both see if the action itself is being redirected, and whether a block/redirect is being move to target it.
# ----> Unless it's redirecting a block that is targetting itself, block 
# 3. Process unblocked/redirected blocks and unblocked/redirected redirects (order should not matter)
# 4. Process block/redirect loops
# 5. Process remaining redirects/blocks (order should not matter)

class Block:
    def __init__(self) -> None:
        pass

    def RunBlocks(self, playerList: list[Player] = None):
        print("RunBlocks()...")
        allPlayers: list[Player] = [] # Test().StartTest(7)
        if playerList is not None:
            allPlayers = playerList
            
        allActions: list[Action] = generateActionList(allPlayers)
        allBlocks: list[Action] = generateBlockList(allActions)

        print(''.join(map(str,allBlocks)))


        # 1. Check for redirects & blocks targetting each other.

        # processRedirectBlocks(allActions)

        # 2. Check for redirect/block chains



        # 3. Process unblocked/redireted blocks and unblocked/redirected redirects


        processUnblocked(allBlocks)


        # 4. Process block/redirect loops

        for a in allBlocks:
            processCyclicalBlock(a,[])

        for a in allActions:
            if a.inBlockCycle:
                a.blocked = True

        # 5. Process remaining redirects/blocks

        processUnblocked(allBlocks)


        for p in allPlayers:
            print(f"{p.info.name}: isBlocked = {p.status.isBlocked}")
            for a in p.choice.actions:
                    print(f" - {a.name}: isBlocked = {a.blocked}")

        print("RunBlocks()... Done!")