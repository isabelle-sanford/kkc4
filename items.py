from enum import Enum
import random
from actioninfo import ActionType

class ItemType(Enum):

    MOMMET = 1, ActionType.UseMommet, "Mommet"
    TENACULUM = 2, ActionType.UseTenaculumAction, "Tenaculum" # hmm
    FIRESTOP = 3, None, "Firestop" # passive
    PLUMBOB = 4, ActionType.UsePlumbob, "Plum Bob"
    BONETAR = 5, ActionType.UseBonetar, "Bone-tar"
    WARD = 6, ActionType.UseWard, "Ward"
    BLOODLESS = 7, None, "Bloodless" # passive
    THIEVESLAMP = 8, ActionType.UseThievesLamp, "Thieves' Lamp"
    GRAM = 9, None, "Gram" # passive
    TALENTPIPES = 10, None, "Talent Pipes" # passive # maybe remove
    NAHLROUT = 11, ActionType.UseNahlrout, "Nahlrout"
    BODYGUARD = 12, None, "--" # passive # maybe remove? (can't be given or stolen)
    # MOMMET_3rd = 13, ActionType.UseMommet, "--" # ???

    def __new__(cls, value, using_action, fullname):
        member = object.__new__(cls)
        member._value_ = value
        member.using_action = using_action
        member.item_name = fullname

        return member

    def __int__(self):
        return self.value

    
    def __str__(self):
        return self.fullname



class Item:
    ITEM_COUNT = 0

    def __init__(self, name, type: ItemType, uses, defense, action, level, target= None, half = False) -> None:
        self.type: ItemType = type

        self.name: str = name # ??
        self.uses: int = uses # Can be None
        self.defense: bool = defense
        self.action: bool = action
        self.level: int = level # Can be None
        self.target = target #None except when mommet

        self.half_made: bool = half

        self.id = Item.ITEM_COUNT
        Item.ITEM_COUNT += 1

    @classmethod
    def Generate(cls, type: ItemType, level: int = 0, target = None, half = False): # todo add half to below stuff
        if type == ItemType.MOMMET: # add sep 3rd level?
            return Item("Mommet", type, 1, False, True, level, target)
        elif type == ItemType.TENACULUM:
            uses = 1
            if level == 4: uses = 2
            return Item("Tenaculum", type, uses, False, True, level)
        elif type == ItemType.FIRESTOP:
            uses = 1
            if level == 4: uses = 2
            return Item("Firestop", type, uses, True, False, level)
        elif type == ItemType.PLUMBOB:
            return Item("Plumbob", type, 1, False, True, level)
        elif type == ItemType.BONETAR:
            return Item("Bonetar", type, 1, False, True, level)
        elif (type == ItemType.WARD or type == ItemType.BLOODLESS 
              or type == ItemType.THIEVESLAMP or type == ItemType.GRAM):
            if level == 2: uses = random.randrange(1,2)
            elif level == 3: uses = 2
            elif level == 4: uses = 3
            else: uses = 1
            if type == ItemType.WARD:
                return Item("Ward", type, uses,True,True,level)
            elif type ==  ItemType.BLOODLESS:
                return Item("Bloodless", type, uses, True, False, level)
            elif type == ItemType.THIEVESLAMP:
                return Item("Thieve's Lamp", type, uses, False, True, level)
            else: # Gram
                return Item("Gram", type, uses, True, False, level) 
        elif type == ItemType.TALENTPIPES:
            return Item("Talent Pipes", type, None, False, False, None)
        elif type == ItemType.NAHLROUT:
            return Item("Nahlrout", type, 1, True, True, None)
        elif type == ItemType.BODYGUARD:
            i = Item("Bodyguard", type, 2,True,False,None)
            i.sabotages = 0
            i.attacks = 0
            return i
    
    def use(self, info=None):
        # TODO 

        if self.type == ItemType.BODYGUARD:
            if info == ActionType.Sabotage:
                self.sabotages += 1
            else: # any other attack ig 
                self.attacks += 1
                # return false? 

        if self.uses > 1:
            self.uses -= 1

        return # maybe bool of whether still exists? 
    
    def __str__(self):
        ret = f"{self.name}"
        if self.target is not None:
            # mommet only
            ret += f" on {self.target} "
        if self.uses > 1:
            ret += f" ({self.uses} use(s))"
        
        return ret
    
    def __repr__(self):
        ret = f"{self.name}"

        if self.target is not None:
            # mommet only
            ret += f" on {self.target} "
        if self.uses > 1:
            ret += f" ({self.uses} use(s))"
        
        return ret
        
