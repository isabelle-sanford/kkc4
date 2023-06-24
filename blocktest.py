# Player class recieves a list of player references

class Player:
    def __init__(self, name):
        self.name = name

        # Flag for whether they have been successfully blocked.
        self.isBlocked = False

        # Flag to ensure proper blocking behaviour of all identified cycles.
        self.inCycle = False

        # Stored input list of who they are blocking, as Player references
        self.blocking = []

        # Working list of players that blocking them, as Player references
        self.blockedBy = []
        

    def __str__(self):
        return self.name
    
    # Prints Player state. 
    # - Only displays who they attempted to block if not blocked.
    def print(self):
        outstr = self.name
        if self.isBlocked:
            outstr += " is blocked."
        else:
            outstr += " is not blocked."

            # Only displays list of blocking targets if not blocked.
            outstr += "\nBlocking: "
            for n in self.blocking:
                outstr += f"{n} "
        
        outstr += "\nBlocked by: "
        if self.inCycle:
            outstr += "Cycle"
        else:
            for n in self.blockedBy:
                outstr += f"{n} "
        
        print(outstr)
    
    # Updates the "blockedBy" field of any player they are targetting with a block.
    def notifyBlock(self):
        for player in self.blocking:
            if not(self.isBlocked):
                player.blockedBy.append(self)

    # Clears the "blockedBy" list.
    def clearBlockedBy(self):
        self.blockedBy = []

# Functions for each step of the process (see explanations below):

# Note: This function will need the "list" to be the full player list, not just those with block actions.
def processUnblocked(list):
    print("Starting iteration.")

    # If any blocks are processed, we need to rerun the check to see if it results in any new players with no one attempting to block them.
    # If this is True, then this function needs to be called again, otherwise this first step can finish.
    blockWasProcessed = False

    # If this is not the first call of the function, players may have preexisting blocks listed in their "BlockedBy" field. These need to be cleared.
    for player in list:
        player.clearBlockedBy()
    
    # Fill the "blockedBy" list for all players, taking into account the current state of player "isBlocked" flags.
    for player in list:
        player.notifyBlock()

    for player in list:
        # Ignoring players who have been blocked, if the player isn't being blocked, apply their blocks.
        if not(player.isBlocked) and len(player.blockedBy) == 0:
            for target in player.blocking:
                # Sets the "blockWasProcessed" flag to only if the game state was changed (i.e. if their target wasn't already blocked).
                if (target.isBlocked == False):
                    target.isBlocked = True
                    blockWasProcessed = True
                    print(f"{target} was blocked.")
        print(f"{player} was processed.")
    print("Iteration complete.")

    if blockWasProcessed:
        processUnblocked(list)
    
# Note: Don't think the recursion end points are correct yet. 
# --> Want it to recursively call the function until it finds the end of a chain (len(player.blocking) = 0 for player), or finds a duplicate in cyclelist, representing a cycle found.
# --> Need to ensure it does actually run for each element in player.blocking
def processCyclicalBlock(player, inputList):
    print("\nStarting iteration")
    # print(f"inputList: {inputList}")
    print(f"Analysing {player}...")
    # Add self to the list.
    inputList.append(player)

    if len(player.blocking) == 0:
        print("Iteration terminated (End of chain reached).")
        str = "["
        for n in inputList:
            str += f"{n} -> "
        print(f"{str} end]")
    else:
        # Checks everyone the current player is trying to block.
        for target in player.blocking:
            # If target is already blocked, no need to consider it.
            if (target.isBlocked):
                continue
            # If the target hasn't be part of the current recorded cycle yet, recursively call this function with a copy (not reference to) the list of players in the current loop.
            if (target not in inputList):
                processCyclicalBlock(target, inputList.copy())
                print(f"...{player} recursion finished.")
            # Otherwise, the target is already there, so we have a cycle. 
            else:
                # From the first occurence of the duplicate to the end of the list, including self, set the "isBlocked" flag on each participant.
                str = "["
                for i in range(inputList.index(target),len(inputList)):
                    inputList[i].inCycle = True
                    str += f"{inputList[i]} -> "
                print("Iteration terminated (Cycle identified and blocked).")
                print(f"{str} {target}]")
                            
    



# p1 = Player("Kasimir")
# p2 = Player("Elbereth")
# p3 = Player("Stink")
# p4 = Player("Burnt")
# p5 = Player("Wilson")

p1 = Player("A")
p2 = Player("B")
p3 = Player("C")
p4 = Player("D")
p5 = Player("E")
p6 = Player("F")
p7 = Player("G")
p8 = Player("H")

# I = Simple loop
# p1.blocking.append(p2)
# p2.blocking.append(p3)
# p3.blocking.append(p1)
# p3.blocking.append(p4)

# III = Seems like loop but actually chain
# p1.blocking.append(p2)
# p2.blocking.append(p3)
# p3.blocking.append(p1)
# p4.blocking.append(p1)

# IV = Multiple loops
# p1.blocking.append(p2)
# p2.blocking.append(p3)
# p3.blocking.append(p1)
# p3.blocking.append(p4)
# p4.blocking.append(p1)

# V = Lots more nested loops
# p1.blocking.append(p2)
# p1.blocking.append(p5)
# p2.blocking.append(p3)
# p3.blocking.append(p4)
# p4.blocking.append(p5)
# p4.blocking.append(p2)
# p5.blocking.append(p6)
# p5.blocking.append(p1)
# p6.blocking.append(p7)
# p7.blocking.append(p3)
# p7.blocking.append(p1)

# VI = V, but external successful block on F.
# p1.blocking.append(p2)
# p1.blocking.append(p5)
# p2.blocking.append(p3)
# p3.blocking.append(p4)
# p4.blocking.append(p5)
# p4.blocking.append(p2)
# p5.blocking.append(p6)
# p5.blocking.append(p1)
# p6.blocking.append(p7)
# p7.blocking.append(p3)
# p7.blocking.append(p1)
# p8.blocking.append(p6)

# VII = IV but with E breaking one of the loops, while A also forms secondary loop through C, plus an extra chain.
p1.blocking.append(p2)
p1.blocking.append(p3)
p2.blocking.append(p3)
p3.blocking.append(p1)
p3.blocking.append(p4)
p4.blocking.append(p1)
p5.blocking.append(p2)
p6.blocking.append(p7)
p7.blocking.append(p8)



playerlist = [p1, p2, p3, p4, p5, p6, p7, p8]

# First, process any blocks that are uncontested.
# -> Any player who is not a target of a block, who has their own block action will succeed in taking the block action, so can be processed (taking into account protects).
# -> The blocks already processed may mean that other players will now no longer be targetted by a block, so the process can happen iteratively.
# -> Do this by each time populating each player with a list of anyone targetting them with a block, and then applying the blocks of any player with an empty "blockedBy" list. 
# --> On subsequent passes, players already blocked (isBlocked = True) will not have their block targets added to "blockedBy" lists.
print("Applying initial unblocked chains...")
processUnblocked(playerlist)
print("...Done.\n")


# Next, what is left over should be made up of paths that terminate, or cycles that loop back on themselves. 
# -> Any cycle will result in any participants having all actions blocked.
# -> If we identify any cycles and apply blocks to all participants, the only remaining block actions will be easy to process chains.
# -> Identify cycles by starting with a player, checking their block targets to see who their block targets are, and so on, keeping track of each player considered.
# --> If a duplicate is ever added, you have found a cycle - starting from the first occurence of the duplicate, set the "isBlocked" flag for all players in loop.
# --> Call the same function iteratively for each element in "blocking" list. 
# ---> Will result in applying the "isBlocked" flag multiple times, but should be exhausive, ensure all loops are found if there are multiple loops.
# ---> Be careful of how the list of players in consideration is passed - has to be a copy of the list, not a reference to the list - each new call should have a new copy of the list with its own name added.

# Sets a "inCycle" flag for any node in a cycle.
print("Starting search for cycles...")
for player in playerlist:
    processCyclicalBlock(player, [])

# Converts all "inCycle" flags to "isBlocked" being set True.
for player in playerlist:
    if player.inCycle:
        player.isBlocked = True
print("Search complete.\n")

# Finally, need to find the start of any chains: these will be the remaining instances of players with empty "blockedBy" lists after resolving any chains.
processUnblocked(playerlist)
# -> Don't forget to consider redirects...


# Output the results
for a in playerlist:
    a.print()
    print()