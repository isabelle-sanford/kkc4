from __future__ import annotations
from dataclasses import dataclass
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from player import Player
import random
from enum import Enum
from items import Item, ItemType
from field import Rank, FieldName

class ActionCategory(Enum):
    BLOCKETC = 1
    OFFENSIVE = 2
    OTHER = 3
    CREATEITEM = 4


class Target(Enum):
    PLAYER = 1
    ACTION = 2
    LOCATION = 3
    ITEM = 4
    EVENT = 5 # for Omen Recognition and mommet lvl 3
    OTHER = 6 # bool for master bonetar
    FIELD = 7 # banned books
    ABILITY = 8 # banned books
    NONE = 9 # includes self-targets

@dataclass
class ActionInfo:
    id: int
    name: str
    category: ActionCategory
    target1: Target
    target2: Target = Target.NONE
    is_positive: bool = False
    is_negative: bool = False
    insanity_bonus: int = 0

class ActionType(Enum):
    # isn't there a way to generate enums instead of having to have them all here like this? 
    MysteriousBulletins = 1, ActionCategory.OTHER, Target.NONE, Target.NONE
    BribeTheMessenger = 2, ActionCategory.OTHER, Target.PLAYER, Target.NONE 
    LinguisticAnalysis = 3, ActionCategory.OTHER, Target.PLAYER, Target.NONE
    Pickpocket = 4, ActionCategory.BLOCKETC, Target.PLAYER, Target.NONE # or none + none if not master
    LawOfContraposition = 5, ActionCategory.BLOCKETC, Target.ACTION, Target.PLAYER
    ProficientInHyperbole = 6, ActionCategory.OTHER, Target.PLAYER, Target.PLAYER 
    ArgumentumAdNauseam = 7, ActionCategory.OTHER, Target.PLAYER, Target.NONE 
    PersuasiveArguments = 8, ActionCategory.OTHER, Target.PLAYER, Target.PLAYER 
    FaeLore = 9, ActionCategory.BLOCKETC, Target.PLAYER, Target.NONE # right?
    OmenRecognition = 12, ActionCategory.OTHER, Target.EVENT, Target.NONE
    SchoolRecords = 13, ActionCategory.OTHER, Target.PLAYER, Target.NONE
    BannedBooks = 14, ActionCategory.OTHER, Target.FIELD, Target.ABILITY
    MommetMaking = 15, ActionCategory.OTHER, Target.PLAYER, Target.NONE
    MalfeasanceProtection = 16, ActionCategory.BLOCKETC, Target.PLAYER, Target.NONE
    MedicaEmergency = 17, ActionCategory.OTHER, Target.NONE, Target.NONE
    MedicaDetainment = 18, ActionCategory.BLOCKETC, Target.PLAYER, Target.NONE
    PsychologicalCounselling = 19, ActionCategory.OTHER, Target.PLAYER, Target.NONE
    CheatingDeath = 20, ActionCategory.OTHER, Target.PLAYER, Target.NONE

    # what if single CreateItem action type, target is item
    CreateTenaculum = 21, ActionCategory.CREATEITEM, Target.ITEM, Target.NONE
    CreateFirestop = 22, ActionCategory.CREATEITEM, Target.ITEM, Target.NONE
    CreatePlumbob = 23, ActionCategory.CREATEITEM, Target.ITEM, Target.NONE
    CreateBonetar = 24, ActionCategory.CREATEITEM, Target.ITEM, Target.NONE
    CreateWard = 25, ActionCategory.CREATEITEM, Target.ITEM, Target.NONE
    CreateBloodless = 26, ActionCategory.CREATEITEM, Target.ITEM, Target.NONE
    CreateThievesLamp = 27, ActionCategory.CREATEITEM, Target.ITEM, Target.NONE
    CreateGram = 28, ActionCategory.CREATEITEM, Target.ITEM, Target.NONE
    
    UseName = 29, ActionCategory.OTHER, Target.OTHER, Target.OTHER # !!

    # what if UseItem type
    UseMommet = 30, ActionCategory.BLOCKETC, Target.PLAYER, Target.NONE
    UseTenaculumItem = 31, ActionCategory.BLOCKETC, Target.PLAYER, Target.ITEM
    UseTenaculumAction = 32, ActionCategory.BLOCKETC, Target.PLAYER, Target.ACTION
    UsePlumbob = 34, ActionCategory.OTHER, Target.PLAYER, Target.NONE
    UseBonetar = 35, ActionCategory.OFFENSIVE, Target.LOCATION, Target.OTHER
    UseWard = 36, ActionCategory.OTHER, Target.NONE, Target.NONE
    UseThievesLamp = 37, ActionCategory.BLOCKETC, Target.NONE, Target.NONE
    UseNahlrout = 38, ActionCategory.BLOCKETC, Target.PLAYER, Target.NONE
    UseCourier = 39, ActionCategory.OTHER, Target.PLAYER, Target.NONE 

    # ! maybe don't include this at all tbh? 
    #UseAssassin = 40, ActionCategory.OFFENSIVE, Target.PLAYER, Target.NONE # player # note - does not take an action period / can't be blocked

    Sabotage = 41, ActionCategory.OFFENSIVE, Target.PLAYER, Target.NONE # player

    CreateItem = 42, ActionCategory.CREATEITEM, Target.ITEM, Target.NONE
    CreateHalfItem = 43, ActionCategory.CREATEITEM, Target.ITEM, Target.NONE

    def __new__(cls, value, category, t1type, t2type):
        member = object.__new__(cls)
        member._value_ = value
        member.category = category
        member.t1type = t1type
        member.t2type = t2type
        return member

    def __int__(self):
        return self.value
    
    def __str__(self) -> str:
        return f"---"




# todo maybe - add what target type these have
    # player, action, location, none, field ? 

HAS_IB = [ # hmm
    ActionType.MalfeasanceProtection,
    ActionType.CreateTenaculum,
    ActionType.CreateFirestop,
    ActionType.CreatePlumbob,
    ActionType.CreateBonetar,
    ActionType.CreateWard,
    ActionType.CreateBloodless,
    ActionType.CreateThievesLamp,
    ActionType.CreateGram,
    ActionType.UseName,
    ActionType.UseMommet,
    ActionType.CreateItem #
]

class Action:
    # maybe ActionInfo instead of type? not sure
    def __init__(self, player, type: ActionType, target,
                  target_two = None, level = None, item: Item = None): # action_type ??
        self.player = player # Player taking the action
        
        self.type: ActionType = type 
        self.category: ActionCategory = type.category
        self.target = target
        self.target_two = target_two
        # todo: target types?

        
        self.blocked: bool = False
        self.redirected: bool = False
        self.redirect_target = None # might want original_target

        self.successful: bool = True # result for player

        self.message: str = None

        # could have ActionType be more specific instead of this
        # probs should be an argument though
        self.level = level # hmm

        self.item = item

        # month?

        # IS POSITIVE (for streets purposes)
        # is negative (for malfeasance protection and maybe other stuff)

        # Working variables to process cycles and chains
        self.blocked_by = []
        self.blocked_by_action: list[Action] = []
        self.in_block_cycle: bool = False
        self.block_reasoning = "" # for GM results

    def __str__(self):
        # assumes action-taker is known 
        ret = self.type.name # ! gotta be info 
        if self.target is not None:
            ret += f"({self.target}"
            if self.target_two is not None:
                ret += f"-> {self.target_two})"
            ret += ")"
        
        return ret

    # todo more detailed str


    def print_block_details(self):
        out = f"Action: {self}\n"
        out += f"Player: {self.player.info.name} Target: {self.target.info.name} Target_Two: {self.target_two}\n"
        out += f"In_Block_cycle: {self.in_block_cycle}, Blocked: {self.blocked}, Blocked_By: [{', '.join([p.info.name for p in self.blocked_by])}]\n"
        print(out)

    
    def perform(self, **kwargs):
        if self.blocked and not self.in_block_cycle:
            # log it
            out_one = ", ".join(p.info.name for p in self.blocked_by)
            out_two = ", ".join(a.type.name for a in self.blocked_by_action)
            print(f"{self.player.info.name}'s {self.type.name} blocked by [{out_one}] using [{out_two}]")
            self.successful = False
            return
        
        # todo everywhere: check that target can be targeted
        # also for target types being correct

        action_logged = False

        # todo: insanity bonus
        if self.type == ActionType.UseMommet:
            # Dunno if this can be cleaned up a bit
            notify_only = False
            if "notify_only" in kwargs:
                notify_only = kwargs["notify_only"]
            if "result" in kwargs:    
                result = kwargs["result"]
            else:
                result = {"process_block_cycles": False}
            
            self.block_one(notify_only, result)
            if result["success"]:
                self.in_block_cycle = False
                # Remove item
                # Would be nice to have the item have a reference to the action.
                print(f"{self.player.info.name} succesfully used Mommet")


        match self.type:

            case ActionType.CreateItem:
                # maybe make helper function for this
                art_level = self.player.status.elevations.count(FieldName.ARTIFICERY)
                alc_level = self.player.status.elevations.count(FieldName.ALCHEMY)

                match self.target:
                    
                    # Artificery
                    case ItemType.WARD:
                        # todo: check that first half is already made
                        item = Item.Generate(ItemType.WARD, art_level)
                        self.player.processing.insanity_bonus += 1
                    case ItemType.BLOODLESS:
                        item = Item.Generate(ItemType.BLOODLESS, art_level)
                        self.player.processing.insanity_bonus += 2
                    case ItemType.THIEVESLAMP:
                        item = Item.Generate(ItemType.THIEVESLAMP, art_level)
                        self.player.processing.insanity_bonus += 2
                    case ItemType.GRAM:
                        item = Item.Generate(ItemType.GRAM, art_level)
                        self.player.processing.insanity_bonus += 3
                    
                    # Alchemy
                    case ItemType.TENACULUM:
                        item = Item.Generate(ItemType.TENACULUM, alc_level)
                        self.player.processing.insanity_bonus += 1
                    case ItemType.FIRESTOP:
                        item = Item.Generate(ItemType.FIRESTOP, alc_level)
                        self.player.processing.insanity_bonus += 2
                    case ItemType.PLUMBOB:
                        item = Item.Generate(ItemType.PLUMBOB, alc_level)
                        self.player.processing.insanity_bonus += 3
                    case ItemType.BONETAR:
                        item = Item.Generate(ItemType.PLUMBOB, alc_level)
                        self.player.processing.insanity_bonus += 3
                    
                    # TODO mommet making 
                    case ItemType.MOMMET:
                        # TODO 
                        print("todo")
                    case ItemType.MOMMET_3rd:
                        # TODO
                        print("todo")
                    case _:
                        print("idk")

                self.player.add_item(item)
            
            # field abilities

            # LINGUISTICS
            case ActionType.MysteriousBulletins:
                # append string to writeup results
                # todo 
                pass 
            case ActionType.BribeTheMessenger:
                # notify GM abt it
                # todo 
                pass #?
            case ActionType.LinguisticAnalysis:
                # notify GM to say what result is
                pass

            # ARITHMETICS (pickpocket)
            case ActionType.Pickpocket:
                if self.player.status.master_of is not FieldName.ARITHMETICS:
                    if "player_list" in kwargs:
                        # TODO
                        pass
                    #random Target
                    pass
                else:
                    if self.target.holds_item(ItemType.BODYGUARD):
                        Log.Action(self, LogOutcome.Failure)
                        action_logged = True
                    else:
                        money = self.target.status.money
                        proportion = 0.1
                        levels = player.status.elevations.count(FieldName.ARITHMETICS)
                        if levels == 2:
                            proportion = 0.2
                        elif levels == 3:
                            proportion = 0.3
                        self.player.increase_money(money*proportion)
                        self.target.reduce_money(money*proportion)
            
            # RHETORIC AND LOGIC
            # TODO law of contraposition
            # TODO proficient in hyperbole
            case ActionType.ArgumentumAdNauseam:
                self.target.processing.complaints_blocked = True
                self.target.processing.processed_complaints = []
            case ActionType.PersuasiveArguments:
                complaints = self.target.processing.processed_complaints
                if len(complaints) == 1:
                    self.target.processing.processed_complaints = [self.target_two]
                elif len(complaints) == 2:
                    pick = random.randint(0,1)
                    self.target.processing.processed_complaints[pick] = self.target_two
            
            # ARCHIVES
            # TODO FAE LORE
            case ActionType.OmenRecognition:
                print("omen recog")
                # notify GM
            case ActionType.SchoolRecords:
                if self.player.status.is_enrolled:
                    elevs = self.target.status.elevations
                    self.message = elevs # ig, idk
                    # log 
            case ActionType.BannedBooks:
                # TODO
                pass

            # SYMPATHY
            # mommet-making handled above
            # TODO malfeasance protection (sigh)
            # don't forget insanity bonuses

            # PHYSICKING
            case ActionType.MedicaEmergency:
                self.player.status.last_medica_emergency = self.player.status.month # i guess? 

            # TODO medica detainment
            case ActionType.PsychologicalCounselling:
                phys_levels = self.player.status.elevations.count(FieldName.PHYSICKING)
                if self.player.master_of == FieldName.PHYSICKING:
                    phys_levels = 4

                self.target.processing.insanity_bonus -= phys_levels
            # TODO cheating death

            # NAMING
            case ActionType.UseName:
                # TODO 
                # log 
                # remember insanity bonuses
                pass


            # USE ITEMS
            # remember to remove / decrease a use from the item

            # Alchemy
            case ActionType.UseTenaculumAction:
                # AA
                pass
            case ActionType.UseTenaculumItem:
                # AA
                pass

            case ActionType.UsePlumbob:
                alc_levels = self.player.status.elevations.count(FieldName.ALCHEMY)
                print(f"{alc_levels} level plum bob used by {self.player} on {self.target}")
                pass
            case ActionType.UseBonetar:
                # OFFENSIVE
                # need to get list of players at target location
                alc_levels = self.player.levels_in(FieldName.ALCHEMY)
                roll = random.randint(1,100) # maybe just make a func for this tbh
                goes_volatile = False

                if alc_levels < 2 and roll <= 50:
                    goes_volatile = True
                elif alc_levels == 2 and roll <= 25:
                    goes_volatile = True
                elif alc_levels == 3 and roll <= 10:
                    goes_volatile = True 
                elif alc_levels == 4:
                    if self.target_two == True: # choose to go volatile
                        goes_volatile = True
                else:
                    # error check
                    pass
                
                if not goes_volatile:
                    print("destroy ", self.target)
                
                else:
                    # choose players to kill
                    if alc_levels == 3:
                        self.status.last_in_medica = self.status.month + 1
                    elif alc_levels == 4:
                        roll = random.randint(1,100)
                        if roll <= 10:
                            self.status.last_in_medica = self.status.month + 1
                    else:
                        # you have as much chance of dying as everyone else
                        # todo
                        pass

            case ActionType.UseWard:
                # need to get list of actions on the person
                pass
            case ActionType.UseThievesLamp:
                if self.target.holds_item(ItemType.BODYGUARD):
                    # action fails
                    pass 
                else:
                    money = self.target.status.money * .3
                    item_count = len(self.target.status.inventory)

                    # this is a little iffy
                    for i in range(item_count // 2):
                        stolen = random.choice(self.target.status.inventory)
                        self.player.processing.items_received.append(stolen)
                        self.target.status.inventory.remove(stolen)




            case ActionType.UseMommet:
                # remember insanity bonuses
                pass
            
            case ActionType.UseNahlrout:
                # AA
                pass
            
            case ActionType.Sabotage:
                # todo
                pass



                    



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
                    print(f"    Cycle found: [{'<-'.join([actions_in_cycle.target.info.name for actions_in_cycle in sequence_cycle])}<-{a.target.info.name}]")
                else:
                    a.identify_block_cycle(sequence.copy())
        else:
            print(f"    Start of sequence found: [{'<-'.join([action.player.info.name for action in sequence])}]")

    def block_one(self, notify_only, result: dict):
        # Blocks are normally random targets, and target_two is blank
        # Tenaculum can specify a type of action, passing ActionType to target_two
        # Otherwise, to only roll once, once random action chosen, stored in target_two

        # If target action not already fixed - NOTE: THIS MUST BE ABLE TO DEAL WITH IMRE LOCATIONS.
        if not isinstance(self.target_two, Action):
            action_list = self.target.choices.actions
            if len(action_list) > 0:
                target_action = random.choice(action_list)
                # If target was specified
                if isinstance(self.target_two, ActionType):
                    targetted_actions = [a for a in action_list if a.type == self.target_action_type]
                    # If there was only one candidate 
                    if len(targetted_actions) > 0:
                        target_action = random.choice(targetted_actions)
                self.target_two = target_action
            else:
                # No possible actions
                self.target_two = None

        # when dealing with block cycles, don't need to do the notify step
        # Otherwise notify target actions of intent to block
        if notify_only:
            if self.target_two is not None:
                self.target_two.blocked_by.append(self.player)# Possibly unnecessary?
                self.target_two.blocked_by_action.append(self)
            result["success"] = False
        # If actually apply block
        else: 
            if self.target_two is not None:
                if self.target_two.blocked == False:
                    self.target_two.blocked = True
                    result["state_changed"] = True
            result["success"] = True


    # Probably needs something to handle if target has no actions (equivalent of self.target_two is not None checks above)
    def block_all(self, notify_only, result: dict):
        if not result["process_block_cycles"]:       
            self.target.status.blocked_by.append(self.player)
        if not notify_only:
            if self.target.status.is_blocked == False: # Only sets flags if not already blocked.
                self.target.status.is_blocked = True
                result["state_changed"] = True
            result["success"] = True
        else:
            result["success"] = False
        
        for a in self.target.choices.actions:
            if not result["process_block_cycles"]:  
                a.blocked_by.append(self.player)
                a.blocked_by_action.append(self)
            if not notify_only:
                if a.blocked == False: # Only sets flags if not already blocked.
                    a.blocked = True
                    result["state_changed"] = True
                result["success"] = True
            else:
                result["success"] = False
            

    def clear_block_notification(self):
        # If block was single target
        if isinstance(self.target_two, Action):
            self.target_two.blocked_by.remove(self.player)
            self.target_two.blocked_by_action.remove(self)
        # If blocked all? 
        elif self.target_two is not None:
            self.target.status.blocked_by.remove(self.player)
            for a in self.target.choices.actions:
                a.blocked_by.remove(self.player)
                a.blocked_by_action.remove(self)