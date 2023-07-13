from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from player import Player
import random
from enum import Enum
from items import Item, ItemType
from field import Rank, FieldName

class ActionType(Enum):
    Complaint = 1 # player
    GainEP = 2 # ? 
    MysteriousBulletins = 3 # none
    BribeTheMessenger = 4  # player
    LinguisticAnalysis = 5  # player
    Pickpocket = 6 # none or player (if master)
    LawOfContraposition = 7 # 2 players
    ProficientInHyperbole = 8 # none / 2 players
    ArgumentumAdNauseam = 9 # player 
    PersuasiveArguments = 10 # 2 players 
    FaeLore = 11 # player
    OmenRecognition = 12 # event (???)
    SchoolRecords = 13 # player 
    BannedBooks = 14 # field. target_2 ability
    MommetMaking = 15 # player
    MalfeasanceProtection = 16 # 
    MedicaEmergency = 17
    MedicaDetainment = 18
    PsychologicalCounselling = 19
    CheatingDeath = 20

    # what if single CreateItem action type, target is item
    CreateTenaculum = 21 # none
    CreateFirestop = 22 # none
    CreatePlumbob = 23 # none
    CreateBonetar = 24 # none
    CreateWard = 25 # none
    CreateBloodless = 26 # none
    CreateThievesLamp = 27 # none
    CreateGram = 28 # none
    
    UseName = 29 # any 

    # what if UseItem type
    UseMommet = 30
    UseTenaculumItem = 31
    UseTenaculumAction = 32
    UseFirestop = 33
    UsePlumbob = 34 # player
    UseBonetar = 35 # location
    UseWard = 36
    UseThievesLamp = 37
    UseNahlrout = 38
    UseCourier = 39 # player
    UseAssassin = 40 # player
    Sabotage = 41 # player

    CreateItem = 42
    CreateHalfItem = 43
# todo maybe - add what target type these have
    # player, action, location, none, field ? 

class ActionCategory(Enum):
    ACTIONAFFECTING = 1
    OFFENSIVE = 2
    OTHER = 3

class TargetType(Enum):
    PLAYER = 1
    ACTION = 2
    LOCATION = 3
    ITEM = 4
    EVENT = 5 # for Omen Recognition and mommet lvl 3
    OTHER = 6 # bool for master bonetar
    FIELD = 7 # banned books
    ABILITY = 8 # banned books

class Action:
    def __init__(self, player, type: ActionType, target,
                  target_two = None, action_type: ActionType = None): # action_type ??
        self.player = player # Player taking the action
        self.type: ActionType = type 
        # todo: make ActionCategory (Action-Affecting, Offensive, Other)
        self.target_action_type: ActionType = action_type # ? what's this for?
        self.target: Player = target
        # maybe something indicating what kind of object the target will be?
        self.target_two = target_two

        # todo 
        self.category: ActionCategory = ActionCategory.OTHER

        self.blocked: bool = False
        self.redirected: bool = False
        self.redirect_target = None # might want original_target

        self.successful: bool = True # result for player

        self.message: str = None

        # could have ActionType be more specific instead of this
        # probs should be an argument though
        self.level = None # hmm

        # month?

        # IS POSITIVE (for streets purposes)
        # is negative (for malfeasance protection and maybe other stuff)

        # Working variables to process cycles and chains
        self.blocked_by = []
        self.blocked_by_action: list[Action] = []
        self.in_block_cycle: bool = False
        self.block_reasoning = "" # for GM results

    # only handling OTHER-category actions atm
    def perform(self, **kwargs):
        if self.blocked:
            # log it
            print("blocked")
            return
        
        # todo everywhere: check that target can be targeted
        # also for target types being correct

        action_logged = False

        # match self.type:

        #     case ActionType.CreateItem:
        #         # maybe make helper function for this
        #         art_level = self.player.status.elevations.count(FieldName.ARTIFICERY)
        #         alc_level = self.player.status.elevations.count(FieldName.ALCHEMY)

        #         match self.target:
                    
        #             # Artificery
        #             case ItemType.WARD:
        #                 # todo: check that first half is already made
        #                 item = Item.Generate(ItemType.WARD, art_level)
        #                 self.player.processing.insanity_bonus += 1
        #             case ItemType.BLOODLESS:
        #                 item = Item.Generate(ItemType.BLOODLESS, art_level)
        #                 self.player.processing.insanity_bonus += 2
        #             case ItemType.THIEVESLAMP:
        #                 item = Item.Generate(ItemType.THIEVESLAMP, art_level)
        #                 self.player.processing.insanity_bonus += 2
        #             case ItemType.GRAM:
        #                 item = Item.Generate(ItemType.GRAM, art_level)
        #                 self.player.processing.insanity_bonus += 3
                    
        #             # Alchemy
        #             case ItemType.TENACULUM:
        #                 item = Item.Generate(ItemType.TENACULUM, alc_level)
        #                 self.player.processing.insanity_bonus += 1
        #             case ItemType.FIRESTOP:
        #                 item = Item.Generate(ItemType.FIRESTOP, alc_level)
        #                 self.player.processing.insanity_bonus += 2
        #             case ItemType.PLUMBOB:
        #                 item = Item.Generate(ItemType.PLUMBOB, alc_level)
        #                 self.player.processing.insanity_bonus += 3
        #             case ItemType.BONETAR:
        #                 item = Item.Generate(ItemType.PLUMBOB, alc_level)
        #                 self.player.processing.insanity_bonus += 3
                    
        #             # TODO mommet making 
        #             case ItemType.MOMMET:
        #                 # TODO 
        #                 print("todo")
        #             case ItemType.MOMMET_3rd:
        #                 # TODO
        #                 print("todo")
        #             case _:
        #                 print("idk")

        #         self.player.add_item(item)
            
        #     # field abilities

        #     # LINGUISTICS
        #     case ActionType.MysteriousBulletins:
        #         # append string to writeup results
        #         # todo 
        #         pass 
        #     case ActionType.BribeTheMessenger:
        #         # notify GM abt it
        #         # todo 
        #         pass #?
        #     case ActionType.LinguisticAnalysis:
        #         # notify GM to say what result is
        #         pass

        #     # ARITHMETICS (pickpocket)
        #     case ActionType.Pickpocket:
        #         if self.player.status.master_of is not FieldName.ARITHMETICS:
        #             if "player_list" in kwargs:
        #                 # TODO
        #                 pass
        #             #random Target
        #             pass
        #         else:
        #             if self.target.holds_item(ItemType.BODYGUARD):
        #                 Log.Action(self, LogOutcome.Failure)
        #                 action_logged = True
        #             else:
        #                 money = self.target.status.money
        #                 proportion = 0.1
        #                 levels = player.status.elevations.count(FieldName.ARITHMETICS)
        #                 if levels == 2:
        #                     proportion = 0.2
        #                 elif levels == 3:
        #                     proportion = 0.3
        #                 self.player.increase_money(money*proportion)
        #                 self.target.reduce_money(money*proportion)
            
        #     # RHETORIC AND LOGIC
        #     # TODO law of contraposition
        #     # TODO proficient in hyperbole
        #     case ActionType.ArgumentumAdNauseam:
        #         self.target.processing.complaints_blocked = True
        #         self.target.processing.processed_complaints = []
        #     case ActionType.PersuasiveArguments:
        #         complaints = self.target.processing.processed_complaints
        #         if len(complaints) == 1:
        #             self.target.processing.processed_complaints = [self.target_two]
        #         elif len(complaints) == 2:
        #             pick = random.randint(0,1)
        #             self.target.processing.processed_complaints[pick] = self.target_two
            
        #     # ARCHIVES
        #     # TODO FAE LORE
        #     case ActionType.OmenRecognition:
        #         print("omen recog")
        #         # notify GM
        #     case ActionType.SchoolRecords:
        #         if self.player.status.is_enrolled:
        #             elevs = self.target.status.elevations
        #             self.message = elevs # ig, idk
        #             # log 
        #     case ActionType.BannedBooks:
        #         # TODO
        #         pass

        #     # SYMPATHY
        #     # mommet-making handled above
        #     # TODO malfeasance protection (sigh)
        #     # don't forget insanity bonuses

        #     # PHYSICKING
        #     case ActionType.MedicaEmergency:
        #         self.player.status.last_medica_emergency = self.player.status.month # i guess? 

        #     # TODO medica detainment
        #     case ActionType.PsychologicalCounselling:
        #         phys_levels = self.player.status.elevations.count(FieldName.PHYSICKING)
        #         if self.player.master_of == FieldName.PHYSICKING:
        #             phys_levels = 4

        #         self.target.processing.insanity_bonus -= phys_levels
        #     # TODO cheating death

        #     # NAMING
        #     case ActionType.UseName:
        #         # TODO 
        #         # log 
        #         # remember insanity bonuses
        #         pass


        #     # USE ITEMS
        #     # remember to remove / decrease a use from the item

        #     # Alchemy
        #     case ActionType.UseTenaculumAction:
        #         # AA
        #         pass
        #     case ActionType.UseTenaculumItem:
        #         # AA
        #         pass

        #     case ActionType.UsePlumbob:
        #         alc_levels = self.player.status.elevations.count(FieldName.ALCHEMY)
        #         print(f"{alc_levels} level plum bob used by {self.player} on {self.target}")
        #         pass
        #     case ActionType.UseBonetar:
        #         # OFFENSIVE
        #         # need to get list of players at target location
        #         alc_levels = self.player.levels_in(FieldName.ALCHEMY)
        #         roll = random.randint(1,100) # maybe just make a func for this tbh
        #         goes_volatile = False

        #         if alc_levels < 2 and roll <= 50:
        #             goes_volatile = True
        #         elif alc_levels == 2 and roll <= 25:
        #             goes_volatile = True
        #         elif alc_levels == 3 and roll <= 10:
        #             goes_volatile = True 
        #         elif alc_levels == 4:
        #             if self.target_two == True: # choose to go volatile
        #                 goes_volatile = True
        #         else:
        #             # error check
        #             pass
                
        #         if not goes_volatile:
        #             print("destroy ", self.target)
                
        #         else:
        #             # choose players to kill
        #             if alc_levels == 3:
        #                 self.status.last_in_medica = self.status.month + 1
        #             elif alc_levels == 4:
        #                 roll = random.randint(1,100)
        #                 if roll <= 10:
        #                     self.status.last_in_medica = self.status.month + 1
        #             else:
        #                 # you have as much chance of dying as everyone else
        #                 # todo
        #                 pass

        #     case ActionType.UseWard:
        #         # need to get list of actions on the person
        #         pass
        #     case ActionType.UseThievesLamp:
        #         if self.target.holds_item(ItemType.BODYGUARD):
        #             # action fails
        #             pass 
        #         else:
        #             money = self.target.status.money * .3
        #             item_count = len(self.target.status.inventory)

        #             # this is a little iffy
        #             for i in range(item_count // 2):
        #                 stolen = random.choice(self.target.status.inventory)
        #                 self.player.processing.items_received.append(stolen)
        #                 self.target.status.inventory.remove(stolen)




        #     case ActionType.UseMommet:
        #         # remember insanity bonuses
        #         pass
            
        #     case ActionType.UseNahlrout:
        #         # AA
        #         pass
            
        #     case ActionType.Sabotage:
        #         # todo
        #         pass



                    



# Everything after this point is untouched from haelbarde branch
# could be out of date, not sure
    # def perform_old(self):
    #     if self.blocked:
    #         Log.Action(self, LogOutcome.Blocked)
    #         return
    #     player_level = int(self.player.status.rank)
    #     action_logged = False



    #     # Item Creation Actions
    #     # Artificery
    #     if self.type == ActionType.CreateWard:
    #         item = Item.Generate(ItemType.WARD,player_level)
    #         self.player.add_item(item)
    #     elif self.type == ActionType.CreateBloodless:
    #         item = Item.Generate(ItemType.BLOODLESS,player_level)
    #         self.player.add_item(item)
    #     elif self.type == ActionType.CreateThievesLamp:
    #         item = Item.Generate(ItemType.THIEVESLAMP,player_level)
    #         self.player.add_item(item)
    #     elif self.type == ActionType.CreateGram:
    #         item = Item.Generate(ItemType.GRAM,player_level)
    #         self.player.add_item(item)
    #     # Alchemy
    #     elif self.type == ActionType.CreateTenaculum:
    #         item = Item.Generate(ItemType.TENACULUM,player_level)
    #         self.player.add_item(item)
    #     elif self.type == ActionType.CreateFirestop:
    #         item = Item.Generate(ItemType.FIRESTOP,player_level)
    #         self.player.add_item(item)
    #     elif self.type == ActionType.CreatePlumbob:
    #         item = Item.Generate(ItemType.PLUMBOB,player_level)
    #         self.player.add_item(item)
    #     elif self.type == ActionType.CreateBonetar:
    #         item = Item.Generate(ItemType.BONETAR,player_level)
    #         self.player.add_item(item)

    #     # Mommet making may need aditional types, to distinguish level 1, 2, 3, 4
    #     # Needs access to player list for level 1.
    #     elif self.type == ActionType.MommetMaking: 
    #         item = Item.Generate(ItemType.MOMMET,player_level, self.target)
    #         self.player.add_item(item)

    #     # Linguistics
    #     elif self.type == ActionType.MysteriousBulletins:
    #         # Appened string to WriteUp details.
    #         pass
    #     elif self.type == ActionType.BribeTheMessenger:
    #         Log.NotifyGM(f"{self.player.info.name} spies on {self.target}'s PMs.")
    #         action_logged = True
    #     elif self.type == ActionType.LinguisticAnalysis:
    #         Log.NotifyGM() 

    #     # Arithmetics
    #     elif self.type == ActionType.Pickpocket:
    #         if self.player.status.master_of is not FieldName.ARITHMETICS:
    #             #random Target
    #             pass
    #         if self.target.holds_item(ItemType.BODYGUARD):
    #             Log.Action(self, LogOutcome.Failure)
    #             action_logged = True
    #         else:
    #             money = self.target.status.money
    #             proportion = 0.1
    #             if player_level == Rank.RELAR:
    #                 proportion = 0.2
    #             elif player_level == Rank.ELTHE:
    #                 proportion = 0.3
    #             self.player.increase_money(money*proportion)
    #             self.target.reduce_money(money*proportion)
        
    #     # Rhetoric & Logic
    #     elif self.type == ActionType.LawOfContraposition:
    #         pass
    #     elif self.type == ActionType.ProficientInHyperbole:
    #         if self.target is not None:
    #             self.player.status.complaints.append(self.target)
    #         if self.target_two is not None:
    #             self.player.status.complaints.append(self.target_two)
    #     elif self.type == ActionType.ArgumentumAdNauseam:
    #         for complaint in self.target.status.complaints:
    #             if complaint.target == self.target_two:
    #                 complaint.blocked = True
    #                 return
    #     elif self.type == ActionType.PersuasiveArguments:
    #         # Do I need 3 targets here?
    #         pass

    #     # Archives
    #     elif self.type == ActionType.FaeLore:
    #         if self.target.info.is_evil:
    #             self.target.status.blocked = True
    #     elif self.type == ActionType.OmenRecognition:
    #         Log.NotifyGM()
    #     elif self.type == ActionType.SchoolRecords:
    #         out = ""
    #         if self.player.status.is_enrolled:
    #             count = len(self.target.status.elevations)
    #             if count >= 1:
    #                 out += "."
    #             # Log this
    #             # Output to Player PM
    #     elif self.type == ActionType.BannedBooks:
    #         pass
        
    #     # Sympathy
    #     elif self.type == ActionType.MommetMaking:
    #         pass
    #     elif self.type == ActionType.MalfeasanceProtection:
    #         pass

    #     # Physicking
    #     elif self.type == ActionType.MedicaEmergency:
    #         pass
    #     elif self.type == ActionType.MedicaDetainment:
    #         pass
    #     elif self.type == ActionType.PsychologicalCounselling:
    #         self.target.status.IP -= int(player_level)
    #         Log.Action()
    #     elif self.type == ActionType.CheatingDeath:
    #         pass

    #     # Naming
    #     elif self.type == ActionType.UseName:
    #         # Tell the GMs what names to use.
    #         Log.NotifyGM()

        
    #     # Item Usage
    #     elif self.type == ActionType.UseTenaculumAction:
    #         pass
    #     elif self.type == ActionType.UseTenaculumItem:
    #         pass
    #     elif self.type == ActionType.UseFirestop:
    #         pass
    #     elif self.type == ActionType.UsePlumbob:
    #         pass
    #     elif self.type == ActionType.UseBonetar:
    #         pass

    #     elif self.type == ActionType.UseWard:
    #         pass
    #     elif self.type == ActionType.UseThievesLamp:
    #         pass

    #     elif self.type == ActionType.UseMommet:
    #         pass
        
    #     elif self.type == ActionType.UseNahlrout:
    #         pass

    #     # Other Actions
    #     # UseAssassin
    #     # UseCourier
    #     # GainEP

    #     # Complaint
    #     elif self.type == ActionType.Complaint:
    #         if self.target is not None:
    #             self.player.status.complaints.append(self.target)
    #         if self.target_two is not None:
    #             self.player.status.complaints.append(self.target_two)

    #     if not action_logged:
    #         Log.Action(self)
        



    
    def __str__(self) -> str:
        return f"{self.player.info.name}: {self.type} "
    
    def clear_blocked_by(self):
        self.blocked_by = []
        self.blocked_by_action: list[Action] = []
        # clear the blocked_by flag on players?

    # Called by block actions, determines if there is a valid target action, 
    # and notifies the action/player that there is an intention to blocked.
    def set_blocked_by(self):
        # Duplicated in notify_is_blocked. Probably should be handled with categories
        
        block_one = [ActionType.UseTenaculumAction, ActionType.UseNahlrout]
        block_all = [ActionType.FaeLore, ActionType.MedicaDetainment, ActionType.UseMommet]
        block_actions = block_one + block_all
        if (not self.blocked) and (self.type in block_actions):
            
            # Dunno if we just set the player flag, set the player and
            #  all action flags, or just the action flags.
            if self.type in block_all:
                # print("In Block All")
                # print(f"Target Status Blocked By{self.target.status.blocked_by}")
                self.target.status.blocked_by.append(self.player)
                # print(f"Target Status Blocked By{self.target.status.blocked_by}")
                # print(f"Num actions: {len(self.target.choices.actions)}")
                for a in self.target.choices.actions:
                    # print(f"Action Blocked By: {a.blocked_by}")
                    # print(f"Action Blocked By Action: {a.blocked_by_action}")
                    a.blocked_by.append(self.player)
                    a.blocked_by_action.append(self)
                    # print(f"Action Blocked By: {a.blocked_by}")
                    # print(f"Action Blocked By Action: {a.blocked_by_action}")

            elif self.type in block_one:
                # print("In Block One")
                # Random action chosen
                action_list = self.target.choices.actions

                # Unless there is a single valid target specified.
                if len(action_list) > 0:
                    target_action = random.choice(action_list)
                    # If target was specified
                    if self.target_action_type is not None:
                        targetted_actions = [a for a in action_list if a.type == self.target_action_type]
                        # If there was only one candidate 
                        if len(targetted_actions) > 0:
                            target_action = random.choice(targetted_actions)

                    # Notifies the action of the intent to block
                    target_action.blocked_by.append(self.player) # Possibly unnecessary?
                    target_action.blocked_by_action.append(self)
  
    
    # Actions are set up to be similar to doubly linked lists - 
    # they know what actions they are blocking and which actions are blocking them.
    # To determine a circular list, start with an action and work backwards through
    # all blocks targetting it, creating a running list of actions in a sequence.
    # If you ever arrive back at an action you've already considered, 
    # you've found a (sub)loop.
    def identify_block_cycle(self, sequence: list[Action]):
        sequence.append(self)

        if len(self.blocked_by) > 0:
            for a in self.blocked_by_action:
                # Can remove if blocked actions already removed 
                # from action.blocked_by_action lists
                if a.blocked:
                    continue
                
                if (a in sequence):
                    sequence_cycle = sequence[sequence.index(a):]
                    for cycle_action in sequence_cycle:
                        cycle_action.in_block_cycle = True
                    print(f"Cycle found: [{'->'.join([actions_in_cycle.target.info.name for actions_in_cycle in sequence_cycle])}]")
                else:
                    a.identify_block_cycle(sequence.copy())
        else:
            print(f"Start of sequence found: [{'->'.join([action.player.info.name for action in sequence])}]")

