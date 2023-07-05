import random
from player import Player, FieldName, Lodging, Rank
from test import Test

### ==== Classes ==== ###

# Stores the maximum roll for each punishment on the horns, based on player DP
# as a list of Weightings objects as a static class variable.
# The constructor takes the percentages as displayed on the rules doc
# and converts them into "roll this number or less" equivalents
# so that by checking if the rolled result is less than the value, starting
# small, the correct probabilities are applied to each punishment.
class Weightings:
    total_tiers = 0
    tier_weights = []
    outcomes = ["Charges Dropped", "Undignified Mischief",
                "Reckless Use", "Conduct Unbecoming", "Expulsion"]

    def __init__(self, dp_range_minimum, charges_dropped, undignified_mischief, reckless_use, conduct_unbecoming, expulsion) -> None:
        self.tier_level = self.total_tiers
        Weightings.total_tiers += 1

        self.dp_range_minimum = dp_range_minimum

        self.result = [charges_dropped, undignified_mischief,
                       reckless_use, conduct_unbecoming, expulsion]

        # The sum of all percetages is 100, so starting with first 
        # weight and adding the next weight to the previous each time 
        # gives the max value for the range
        for i in range(1, 5):
            self.result[i] = self.result[i-1] + self.result[i]
        Weightings.tier_weights.append(self)

    def __str__(self) -> str:
        if self.tier_level == 0:
            maximum_range = "->"
        else:
            maximum_range = f"{Weightings.tier_weights[self.tier_level-1].dp_range_minimum - 1: <2}"
        val = ""
        for i in range(0, 4):
            val += f"{self.result[i]: >3}, "
        val += f"{self.result[4]: >3}"
        return f"Tier {self.tier_level} ({self.dp_range_minimum: >2}-{maximum_range} DP) [{val}]"


class Charges:
    # Sets up the punishments for the DP ranges
    # First number is the minimum DP for that tier of punishment
    # Other numbers are the percent chance of the different punishments:
    # - Charges Dropped
    # - Undignified Mischief (apology)
    # - Reckless Use of Sympathy (lashing - 1 turn roleblock)
    # - Conduct Unbecoming a Member of the Arcanum (lashing - 3 turn roleblock)
    # - Conduct Unbecoming a Member of the Arcanum (expulsion)
    # What is returned is a 5 element array(list), with the max d100 
    # rolls corresponding to the weights
    def __init__(self) -> None:
        Weightings(20,  0,   0,  0,  0, 100)
        Weightings(19,  0,   0,  0, 10,  90)
        Weightings(17,  0,   0,  0, 20,  80)
        Weightings(15,  0,   5,  5, 25,  65)
        Weightings(13,  0,  10, 20, 40,  30)
        Weightings(11,  0,  20, 20, 50,  10)
        Weightings(8,  20,  30, 30, 20,   0)
        Weightings(5,  60,  30, 10,  0,   0)
        Weightings(0,   0,   0,  0,  0,   0)

    # Rolls a d100, finds which tier to compare the result with based on the players DP.
    # The punishment tier arrays has the max roll corresponding to the given punishment of that column.
    # Starting from the smallest column, checks all columns until it finds the appropriate column.
    # Uses the index found to set the result by passing the matching string in outcome as the argument of assign_outcome.
    def determine_punishment(self, target: Player):
        random_result = random.randrange(1, 100)
        print(
            f"\n{target.info.name} has {target.status.DP} DP, and got a result of {random_result}.")

        # Checks each tier to find the relevant band for the target's DP
        for t in Weightings.tier_weights:
            if (target.status.DP >= t.dp_range_minimum):
                # Checks each possible outcome to find the one corresponding to the rolled result
                for i in range(len(t.result)):
                    if random_result <= t.result[i]:
                        self.assign_outcome(target, Weightings.outcomes[i])
                        return

    # Consequences are not actually implemented yet, but the appropriate if
    #  statements are called based on the DP result.
    # Apply Nahlrout at this point?
    def assign_outcome(self, target: Player, outcome: str):
        if outcome == "Charges Dropped":
            print(f"All charges on {target.info.name} were dropped.")
        elif outcome == "Undignified Mischief":
            print(f"{target.info.name} punished with formal apology.")
        elif outcome == "Reckless Use":
            print(
                f"{target.info.name} charged with Reckless Use of Sympathy and will be punished with 1 lashing.")
        elif outcome == "Conduct Unbecoming":
            print(f"{target.info.name} charged with Conduct Unbecoming a Member of the Arcanum and will be punished with 3 lashings.")
        elif outcome == "Expulsion":
            target.status.is_expelled = True
            print(
                f"{target.info.name} charged with Conduct Unbecoming a Member of the Arcanum and will be expelled.")
        else:
            print(f"Error. Outcome provided was '{outcome}'.")

### ==== Runtime Code ==== ###


class Horns:
    def __init__(self) -> None:
        pass

    def run_complaints(self, player_list: list[Player] = None):
        print("run_complaints()...")
        all_players: list[Player] = []
        if player_list is not None:
            all_players = player_list

        # Extra complaints lodged, and complaint manipulation needs to be processed somewhere.

        # Extra complaints (means if blocked, don't have to remove them.)
        for p in all_players:
            for c in p.choice.actions:
                if c.type == "complaint" and not c.blocked:
                    if c.name == "Proficient in Hyperbole":
                        if c.target is not None:
                            p.choice.complaints.append(c.target)
                        if c.target_two is not None:
                            p.choice.complaints.append(c.target_two)
                    elif c.name == "Argumentum Ad Nauseam":
                        c.target.status.complaints_blocked = True
                    elif c.name == "Persuasive Arguments":
                        # Does this require 3 potential targets?
                        pass

        for p in all_players:
            for c in p.choice.complaints:
                # Notify all players of complaints received.
                c.status.complaints_received.append(p)

        for p in all_players:
            if len(p.status.complaints_received) > 0:
                out = f"{p.info.name} ({len(p.status.complaints_received)}): "
                for c in p.status.complaints_received:
                    out += f"{c.info.name}, "
                out = out[:-2]
                print(out)

        # What do complaints do? 
        # Horns already takes the votes placed and notifies all players of who 
        # voted on them, which can be used in the tuition step. 
        # Extra votes should have been pulled from db. 
        # Blocks needs to run at some point to ensure blocks are removed.
        #    Possibly this class generates the vote counts?
        # Could move the notification of votes to this class. 
        #   This class would need to happen after blocks though.
        print("run_complaints()... Done!")

    def run_horns(self, player_list: list[Player] = None):
        print("RunHorns()...")
        all_players: list[Player] = []
        if player_list is not None:
            all_players = player_list

        complaints: list[Player] = []
        pc_masters: list[Player] = []
        at_pony: list[Player] = []

        players_on_the_horns: set[Player] = set()

        for p in all_players:
            # Gets list of any players at the pony
            # Could be imported from elsewhere?
            if p.status.lodging == Lodging.GoldenPony:
                at_pony.append(p)

            # Gets list of Masters
            # Could be imported from elsewhere?
            if p.status.rank == Rank.MASTER:
                pc_masters.append(p)

            for c in p.choice.complaints:
                # generates complaints list for NPC Master DP distribution
                complaints.append(c)

                # Notify all players of complaints received.
                if player_list is None:
                    c.status.complaints_received.append(p)

        # Deal with Golden Pony buff
        for p in at_pony:
            count = complaints.count(p)
            if count > 0:
                complaints.remove(p)
            if count > 1:
                complaints.remove(p)

        # By passing assign_DP the field of the Master assigning DP,
        #  it handles offsetting the DP gain with related EP.
        
        # For PC masters
        for m in pc_masters:
            for d in m.choice.assigned_DP:
                d.assign_DP(master_of=m.status.master_of)   

        # For all NPC masters
        npc_master_fields = []
        for i in range(1, 9):
            npc_master_fields.append(FieldName(i))
        for p in pc_masters:
            npc_master_fields.pop(p.status.master_of)

        for f in npc_master_fields:
            for count in range(5):
                if (len(complaints) > 0):
                    complaints[random.randrange(
                        len(complaints))].assign_DP(master_of=f)

        # Adds DP from complaints
        for p in all_players:
            p.assign_DP(len(p.status.complaints_received)//2)

            # OnHorns either if recieved any complaint, or PC Master assigned DP to you.
            if (len(p.status.complaints_received) > 0) or (p.status.DP > 0):
                players_on_the_horns.add(p)

        charges = Charges()
        for p in players_on_the_horns:
            charges.determine_punishment(p)

        # for i in Weightings.tier_weights:
        #     print(i)
        print("RunHorns()... Done!")
