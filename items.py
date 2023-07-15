from enum import Enum
import random

# untouched since haelbarde, seems fine

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

    def __init__(self, name, type: ItemType, uses, defense, action, level, id, target= None) -> None:
        self.type: ItemType = type

        self.name: str = name # ??
        self.uses: int = uses # Can be None
        self.defense: bool = defense
        self.action: bool = action
        self.level: int = level # Can be None
        self.target = target #None except when mommet

        self.half_made: bool = False

        self.id = id

    @classmethod
    def Generate(cls, type: ItemType, level: int = 0, target = None, id = 0):
        # TODO make incrementing ids
        if type == ItemType.MOMMET: # add sep 3rd level?
            return Item("Mommet", type, 1, False, True, level, id, target)
        elif type == ItemType.TENACULUM:
            uses = 1
            if level == 4: uses = 2
            return Item("Tenaculum", type, uses, False, True, level, id)
        elif type == ItemType.FIRESTOP:
            uses = 1
            if level == 4: uses = 2
            return Item("Firestop", type, uses, True, False, level, id)
        elif type == ItemType.PLUMBOB:
            return Item("Plumbob", type, 1, False, True, level, id)
        elif type == ItemType.BONETAR:
            return Item("Bonetar", type, 1, False, True, level, id)
        elif (type == ItemType.WARD or type == ItemType.BLOODLESS 
              or type == ItemType.THIEVESLAMP or type == ItemType.GRAM):
            if level == 2: uses = random.randrange(1,2)
            elif level == 3: uses = 2
            elif level == 4: uses = 3
            else: uses = 1
            if type == ItemType.WARD:
                return Item("Ward", type, uses,True,True,level, id)
            elif type ==  ItemType.BLOODLESS:
                return Item("Bloodless", type, uses, True, False, level, id)
            elif type == ItemType.THIEVESLAMP:
                return Item("Thieve's Lamp", type, uses, False, True, level, id)
            else: # Gram
                return Item("Gram", type, uses, True, False, level, id) 
        elif type == ItemType.TALENTPIPES:
            return Item("Talent Pipes", type, None, False, False, None, id)
        elif type == ItemType.NAHLROUT:
            return Item("Nahlrout", type, 1, True, True, None, id)
        elif type == ItemType.BODYGUARD:
            return Item("Bodyguard", type, 2,True,False,None, id)
    
    def use(self):
        # TODO 

        if self.uses > 1:
            self.uses -= 1

        return
