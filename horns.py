from player import Player, Action
import random

### ==== Classes ==== ###       
class Weightings:
    def __init__(self, minDPRange, chargesDropped, undignifiedMischief, recklessUse, conductUnbecoming, expulsion) -> None:
        self.minDP = minDPRange

        self.result = [chargesDropped, undignifiedMischief, recklessUse, conductUnbecoming, expulsion]
        for i in range(1, 5):
            self.result[i] = self.result[i] + self.result[i-1]

        self.outcome = ["Charges Dropped", "Undignified Mischief", "Reckless Use", "Conduct Unbecoming", "Expulsion"]
        # self.MaxDPRange = minDPRange
        # self.ChargesDropped = chargesDropped
        # self.UndignifiedMischief = undignifiedMischief
        # self.RecklessUse = recklessUse
        # self.ConductUnbecoming = conductUnbecoming
        # self.Expulsion = expulsion

        # out = ""
        # for i in self.result:
        #     out += f"{i}, "
        # print(out)

    def __str__(self) -> str:
        out = ""
        out.join(map(str,self.result))
        return out

class Charges:
    # Sets up the punishments for the DP ranges
    # First number is the minimum DP for that tier of punishment
    # Other numbers are the percent chance of the different punishments:
    # - Charges Dropped
    # - Undignified Mischief (apology)
    # - Reckless Use of Sympathy (lashing - 1 turn roleblock)
    # - Conduct Unbecoming a Member of the Arcanum (lashing - 3 turn roleblock)
    # - Conduct Unbecoming a Member of the Arcanum (expulsion)
    # What is returned is a 5 element array(list), with the max d100 rolls corresponding to the weights
    def __init__(self) -> None:
        self.PunishmentTiers: list[Weightings] =  []
        self.PunishmentTiers.append(Weightings(20,  0,   0,  0,  0, 100))
        self.PunishmentTiers.append(Weightings(19,  0,   0,  0, 10,  90))
        self.PunishmentTiers.append(Weightings(17,  0,   0,  0, 20,  80))
        self.PunishmentTiers.append(Weightings(15,  0,   5,  5, 25,  65))
        self.PunishmentTiers.append(Weightings(13,  0,  10, 20, 40,  30))
        self.PunishmentTiers.append(Weightings(11,  0,  20, 20, 50,  10))
        self.PunishmentTiers.append(Weightings(8,  20,  30, 30,  0,   0))       
        self.PunishmentTiers.append(Weightings(5,  60,  30, 10,  0,   0))
        self.PunishmentTiers.append(Weightings(0,   0,   0,  0,  0,   0))
    
    # Rolls a d100, finds which tier to compare the result with based on the players DP.
    # The punishment tier arrays has the max roll corresponding to the given punishment of that column.
    # Starting from the smallest column, checks all columns until it finds the appropriate column.
    # Uses the index found to set the result by passing the matching string in outcome as the argument of assignOutcome.
    def determinePunishment(self, target: Player):
        randomResult = random.randrange(1, 100)
        print(f"\n{target} has {target.DP} DP, and got a result of {randomResult}.")

        # Checks each tier to find the relevant band for the target's DP
        for t in self.PunishmentTiers:
            if (p.DP >= t.minDP):
                # Checks each possible outcome to find the one corresponding to the rolled result
                for i in range(len(t.result)):
                    if randomResult <= t.result[i]:
                        self.assignOutcome(p,t.outcome[i])
                        return

    # Consequences are not actually implemented yet, but the appropriate if statements are called based on the DP result.                    
    def assignOutcome(self, target: Player, outcome: str):
        if outcome == "Charges Dropped":
            print(f"All charges on {target} were dropped.")
        elif outcome == "Undignified Mischief":
            print(f"{target} punished with formal apology.")
        elif outcome == "Reckless Use":
            print(f"{target} charged with Reckless Use of Sympathy and will be punished with 1 lashing.")
        elif outcome == "Conduct Unbecoming":
            print(f"{target} charged with Conduct Unbecoming a Member of the Arcanum and will be punished with 3 lashings.")
        elif outcome == "Expulsion":
            target.expelled = True
            print(f"{target} charged with Conduct Unbecoming a Member of the Arcanum and will be expelled.")
        else:
            print(f"Error. Outcome provided was '{outcome}'.")

class Test:
    def __init__(self) -> None:
        pass

    def StartTest(self, i: int) -> list[Player]:
        if i == 1:
                p1 = Player("A")
                p2 = Player("B")
                p3 = Player("C")
                p4 = Player("D")
                p5 = Player("E")
                p6 = Player("F")
                p7 = Player("G")
                p8 = Player("H")

                p1.ImportComplaint(p2)
                p1.ImportComplaint(p2)
                p2.ImportComplaint(p1)
                p2.ImportComplaint(p4)
                p3.ImportComplaint(p4)
                p5.ImportComplaint(p6)

                return [p1, p2, p3, p4, p5, p6, p7, p8]


### ==== Runtime Code ==== ###
allPlayers: list[Player] = Test().StartTest(1)

complaints: list[Player] = []
pcMaster: list[Player] = []
atPony: list[Player] = []

onHorns: set[Player] = set()


for p in allPlayers:
    # Gets list of any players at the pony
    # Could be imported from elsewhere?
    if p.lodging == "The Golden Pony":
        atPony.append(p)

    # Gets list of Masters
    # Could be imported from elsewhere?
    if p.rank == "Master":
        pcMaster.append(p)

    for c in p.complaints:
        # generates complaints list for NPC Master DP distribution
        complaints.append(c)

        # Notify all players of complaints received.
        c.complaintsReceived.append(p)

# For PC masters
for m in pcMaster:
    for d in m.assignedDP:
        d.assignDP()

# Deal with Golden Pony buff
for p in atPony:
    count =complaints.count(p)
    if count > 0:
        complaints.remove(p)
    if count > 1:
        complaints.remove(p)

# For all NPC masters
for i in range(9 - len(pcMaster)):
    for count in range(5):
        complaints[random.randrange(len(complaints))].assignDP()

# Adds DP from complaints
for p in allPlayers:
    p.assignDP(len(p.complaintsReceived)//2)
    
    # OnHorns either if recieved any complaint, or PC Master assigned DP to you.
    if (len(p.complaintsReceived) > 0) or (p.DP > 0):
        onHorns.add(p)

charges = Charges()
for p in onHorns:
    charges.determinePunishment(p)
