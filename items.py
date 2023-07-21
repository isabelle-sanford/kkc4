from enum import Enum
import random


class ItemType(Enum):
    MOMMET = 1, "Mommet"
    TENACULUM = 2, "Tenaculum"
    FIRESTOP = 3, "Firestop"
    PLUMBOB = 4, "Plum Bob"
    BONETAR = 5, "Bonetar"
    WARD = 6, "Ward"
    BLOODLESS = 7, "Bloodless"
    THIEVESLAMP = 8, "Thieves Lamp"
    GRAM = 9, "Gram"
    TALENTPIPES = 10, "Talent Pipes"
    NAHLROUT = 11, "Nahlrout"
    BODYGUARD = 12, "Bodyguard" # hmm
    MOMMET_3rd = 13, "Mommet (3rd level)"

    def __new__(cls, value, name, ):
        member = object.__new__(cls)
        member._value_ = value
        member.fullname = name
        return member

    def __int__(self):
        return self.value
    
    def __str__(self):
        return self.fullname


class Item:
    ITEM_COUNT = 0

    def __init__(self, name, type: ItemType, uses, defense, action, level, id, target= None, half = False) -> None:
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
    def Generate(cls, type: ItemType, level: int = 0, target = None, id = 0, half = False):
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
        
