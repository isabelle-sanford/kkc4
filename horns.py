from outcome import ProcessLog
from player import Player
from statics import Background, Lodging
from field import FieldStatus
import random


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
    def __init__(self, log: ProcessLog = None, fields: "list[FieldStatus]" = None) -> None:
        Weightings(20,  0,   0,  0,  0, 100)
        Weightings(19,  0,   0,  0, 10,  90)
        Weightings(17,  0,   0,  0, 20,  80)
        Weightings(15,  0,   5,  5, 25,  65)
        Weightings(13,  0,  10, 20, 40,  30)
        Weightings(11,  0,  20, 20, 50,  10)
        Weightings(8,  20,  30, 30, 20,   0)
        Weightings(5,  60,  30, 10,  0,   0)
        Weightings(0,   0,   0,  0,  0,   0)
        
        self.log = log
        self.fields = fields

    # Rolls a d100, finds which tier to compare the result with based on the players DP.
    # The punishment tier arrays has the max roll corresponding to the given punishment of that column.
    # Starting from the smallest column, checks all columns until it finds the appropriate column.
    # Uses the index found to set the result by passing the matching string in outcome as the argument of assign_outcome.
    def determine_punishment(self, target: Player):
        random_result = random.randrange(1, 100)
        self.log.log(
            f"\n{target.info.name} has {target.processing.DP} DP, and got a result of {random_result}.")

        # Checks each tier to find the relevant band for the target's DP
        for t in Weightings.tier_weights:
            if (target.processing.DP >= t.dp_range_minimum):
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
            self.log.log(f"All charges on {target.info.name} were dropped.")
        elif outcome == "Undignified Mischief":
            self.log.log(f"{target.info.name} punished with formal apology.")
        elif outcome == "Reckless Use":
            self.log.log(
                f"{target.info.name} charged with Reckless Use of Sympathy and will be punished with 1 lashing.")
            target.status.last_reckless_use = target.status.month #? off by one?
        elif outcome == "Conduct Unbecoming":
            self.log.log(f"{target.info.name} charged with Conduct Unbecoming a Member of the Arcanum and will be punished with 3 lashings.")
            target.status.last_conduct_unbecoming = target.status.month #?
        elif outcome == "Expulsion":
            target.expel(self.fields)
            self.log.log(
                f"{target.info.name} charged with Conduct Unbecoming a Member of the Arcanum and will be expelled.")
        else:
            self.log.log(f"Error. Outcome provided was '{outcome}'.")

        # return outcome ? 
        
        

### ==== Runtime Code ==== ###


class Horns:
    def __init__(self) -> None:
        pass

    def run_complaints(self, player_list: "list[Player]" = None):
        print("run_complaints()...")
        all_players: list[Player] = []
        if player_list is not None:
            all_players = player_list
        
        # Complaint actions - currently under perform, but idk
        # for p in all_players:
        #     for c in p.choice.actions:
        #         if c.name == "Proficient in Hyperbole" and not c.blocked:
        #             if c.target is not None:
        #                 p.choice.complaints.append(c.target)
        #             if c.target_two is not None:
        #                 p.choice.complaints.append(c.target_two)
        #         elif c.name == "Argumentum Ad Nauseam" and not c.blocked:
        #             c.target.status.complaints_blocked = True
        #         elif c.name == "Persuasive Arguments":
        #             # todo make sure there aren't 2 ppl doing this at once to diff targets 
        #             # Does this require 3 potential targets? - no, can't choose which vote to move
        #             # TODO
        #             pass


        for p in all_players:
            for c in p.processing.processed_complaints:
                # Notify all players of complaints received.
                c.processing.complaints_received.append(p)

        for p in all_players:
            if len(p.processing.complaints_received) > 0:
                out = f"{p.info.name} ({len(p.processing.complaints_received)}): "

                out += ", ".join([c.info.name for c in p.processing.complaints_received])

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

    def run_horns(self, player_list: "list[Player]" = None, field_list: "list[FieldStatus]" = None, log: ProcessLog = None):
        log.log("RunHorns()......")
        all_players: list[Player] = []
        if player_list is not None:
            all_players = player_list
        # else error?
        all_fields: list[FieldStatus] = [] 
        if field_list is not None:
            all_fields = field_list

        complaints: list[Player] = [] # for NPC masters
        at_pony: list[Player] = []

        players_on_the_horns: set[Player] = set()

        for p in all_players:
            # Gets list of any players at the pony
            # Could be imported from elsewhere?
            if p.status.lodging == Lodging.GoldenPony:
                at_pony.append(p)

            for c in p.processing.processed_complaints:
                # generates complaints list for NPC Master DP distribution
                complaints.append(player_list[c]) # hmm # !

                # Notify all players of complaints received.
                if player_list is None:
                    c.processing.complaints_received.append(p)

        # Deal with Golden Pony buff
        for p in at_pony:
            count = complaints.count(p)
            if count > 0:
                complaints.remove(p)
            if count > 1:
                complaints.remove(p)

        # TODO dissolve complaints on masters

        log.log("Complaints handled.")

        # add complaints on players to tuition as inflations
        for c in complaints:
            c.tuition.num_complaints_received += 1

        # By passing assign_DP the field of the Master assigning DP,
        #  it handles offsetting the DP gain with related EP.

        # assign DP from masters (PC and NPC)
        for field in all_fields:
            if field.master is not None: # pc master
                for d in field.master.choices.assigned_DP:
                    d.assign_DP(master_of=field.master.status.master_of)
            else: # npc master
                for count in range(5):
                    if len(complaints) > 0:
                        complaints[random.randrange(0,len(complaints))].assign_DP(master_of=field.name)
        # TODO LOG
        log.log("DP assigned.")

        # Adds DP from complaints
        for p in all_players:
            p.assign_DP(len(p.processing.complaints_received)//2)

            # OnHorns either if recieved any complaint, or PC Master assigned DP to you.
            # why not just check if DP > 0? 
            if (len(p.processing.complaints_received) > 0) or (p.processing.DP > 0):
                players_on_the_horns.add(p)

        log.log("Determining charges...")
        charges = Charges(log, all_fields)
        for p in players_on_the_horns:
            p.tuition.times_on_horns += 1
            charges.determine_punishment(p)

        # for i in Weightings.tier_weights:
        #     print(i)
        log.log("RunHorns()... Done!")
