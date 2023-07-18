from __future__ import annotations
from dataclasses import dataclass
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from player import Player
import random
from enum import Enum, IntEnum
from items import Item, ItemType
from statics import FieldName, Rank
from actioninfo import ActionInfo, ActionCategory, ActionType #, Target


class Action:
    def __init__(self, player, type: ActionType, target,
                  target_two = None, level = None, item: Item = None): 
        self.player = player # Player taking the action
        
        self.type: ActionType = type # could use info? idk
        self.category: ActionCategory = type.info.category
        self.target = target
        self.target_two = target_two
        # todo: target types?

        
        self.blocked: bool = False
        self.redirected: bool = False
        self.redirect_target = None # might want original_target

        self.successful: bool = True # result for player

        self.message: str = None

        self.level = level # hmm

        self.item = item # if using or targeting a specific item

        # Working variables to process cycles and chains
        self.blocked_by = []
        self.blocked_by_action: list[Action] = []
        self.in_block_cycle: bool = False
        self.block_reasoning = "" # for GM results

    def __str__(self):
        # assumes action-taker is known 
        # e.g. Law of Contraposition (Hael -> Wilson)
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
        print(out) # maybe return? 

    
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
                # todo remove item
                print(f"{self.player.info.name} succesfully used Mommet")


        match self.type:

            case ActionType.CreateItem:
                # maybe make helper function for this
                art_level = self.player.levels_in(FieldName.ARTIFICERY)
                alc_level = self.player.levels_in(FieldName.ALCHEMY)

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
                        #Log.Action(self, LogOutcome.Failure)
                        action_logged = True
                    else:
                        money = self.target.status.money
                        proportion = 0.1
                        levels = self.player.status.elevations.count(FieldName.ARITHMETICS)
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
                phys_levels = self.player.levels_in(FieldName.PHYSICKING)

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