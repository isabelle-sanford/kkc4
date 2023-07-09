from player import Player
from statics import Lodging
from field import FieldName, Rank, FieldStatus
import random

class Horns:
    def __init__(self) -> None:
        pass

    def run_complaints(self, player_list: "list[Player]" = None):
        print("run_complaints()...")
        all_players: list[Player] = []
        if player_list is not None:
            all_players = player_list
        
        # TODO public vote count (probably)

        # Complaint actions 
        for p in all_players:
            for c in p.choice.actions:
                if c.name == "Proficient in Hyperbole" and not c.blocked:
                    if c.target is not None:
                        p.choice.complaints.append(c.target)
                    if c.target_two is not None:
                        p.choice.complaints.append(c.target_two)
                elif c.name == "Argumentum Ad Nauseam" and not c.blocked:
                    c.target.status.complaints_blocked = True
                elif c.name == "Persuasive Arguments":
                    # Does this require 3 potential targets?
                    # TODO
                    pass

        for p in all_players:
            for c in p.choice.complaints:
                # Notify all players of complaints received.
                c.status.complaints_received.append(p)

        for p in all_players:
            if len(p.status.complaints_received) > 0:
                out = f"{p.info.name} ({len(p.status.complaints_received)}): "

                out += ", ".join([c.info.name for c in p.status.complaints_received])

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

    def run_horns(self, player_list: "list[Player]" = None, field_list: "list[FieldStatus]" = None):
        print("RunHorns()...")
        all_players: list[Player] = []
        if player_list is not None:
            all_players = player_list
        all_fields: list[FieldStatus] = [] 
        if field_list is not None:
            all_fields = field_list

        complaints: list[Player] = [] # for NPC masters
        pc_masters: list[Player] = []
        at_pony: list[Player] = []

        players_on_the_horns: set[Player] = set()

        for p in all_players:
            # Gets list of any players at the pony
            # Could be imported from elsewhere?
            if p.status.lodging == Lodging.GoldenPony:
                at_pony.append(p)

            # # Gets list of Masters
            # # Could be imported from elsewhere?
            # if p.status.rank == Rank.MASTER:
            #     pc_masters.append(p)

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

        # assign DP from masters (PC and NPC)
        for field in all_fields:
            if field.master is not None: # pc master
                for d in field.master.choice.assigned_DP:
                    # todo understand
                    d.assign_DP(master_of=field.master.status.master_of)
            else: # npc master
                for count in range(5):
                    if len(complaints) > 0:
                        complaints[random.randrange(len(complaints))].assign_DP(master_of=field.name)


        # Adds DP from complaints
        for p in all_players:
            p.assign_DP(len(p.status.complaints_received)//2)

            # OnHorns either if recieved any complaint, or PC Master assigned DP to you.
            # todo check abt public vote manip
            if (len(p.status.complaints_received) > 0) or (p.status.DP > 0):
                players_on_the_horns.add(p)
