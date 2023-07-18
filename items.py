from enum import Enum
import random


class ItemType(Enum):
    MOMMET = 1
    TENACULUM = 2
    FIRESTOP = 3
    PLUMBOB = 4
    BONETAR = 5
    WARD = 6
    BLOODLESS = 7
    THIEVESLAMP = 8
    GRAM = 9
    TALENTPIPES = 10
    NAHLROUT = 11
    BODYGUARD = 12 # hmm
    MOMMET_3rd = 13


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
    def Generate(cls, type: ItemType, level: int = 0, target = None, half = False):
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
            return Item("Bodyguard", type, 2,True,False,None)
    
    def use(self):
        # TODO 

        if self.uses > 1:
            self.uses -= 1

        return
    
    def __str__(self):
        ret = f"{self.name}"
        if self.target is not None:
            # mommet only
            ret += f" on {self.target} "
        if self.uses > 1:
            ret += f" ({self.uses} use(s))"
        
