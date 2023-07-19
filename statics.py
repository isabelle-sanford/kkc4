from enum import Enum, IntEnum

class FieldName(Enum):
    LINGUISTICS = 0, "Linguistics"
    ARITHMETICS = 1, "Arithmetics"
    RHETORICLOGIC = 2, "Rhetoric & Logic"
    ARCHIVES = 3, "Archives"
    SYMPATHY = 4, "Sympathy"
    PHYSICKING = 5, "Physicking"
    ALCHEMY = 6, "Alchemy"
    ARTIFICERY = 7, "Artificery"
    NAMING = 8, "Naming"
    GENERAL = 9, "GENERAL"  # ? # gotta remember this when iterating thru

    def __new__(cls, value, name, ):
        member = object.__new__(cls)
        member._value_ = value
        member.fullname = name
        return member

    def __int__(self):
        return self.value
    
    def __str__(self):
        return self.fullname


# maybe separate out action periods, bc Item Creation and all



class Rank(Enum):
    NONE = 0
    ELIR = 1
    RELAR = 2
    ELTHE = 3
    MASTER = 4

    # todo probably not this 
    def get_next(self):
        if self.NONE:
            return self.ELIR
        if self.ELIR:
            return self.RELAR
        if self.RELAR:
            return self.ELTHE
        if self.ELTHE:
            return self.MASTER




class Lodging(Enum):
    Streets = 0, "The Streets", 0
    Underthing = 1, "The Underthing", 0
    Mews = 2, "Mews", 1 # +2 IP
    Ankers = 3, "Ankers", 4 # 15% 1 action cancelled
    KingsDrab = 4, "The King's Drab", 6 # ?% stolen item
    GreyMan = 5, "The Grey Man", 7 # Giles, Imre
    GoldenPony = 6, "The Golden Pony", 8 # -2 complaints
    WindyTower = 7, "The Windy Tower", 9 # +1 EP to file
    HorseAndFour = 8, "The Horse and Four", 10 # 50% kill/sab fail
    PearlOfImre = 9, "The Pearl of Imre", 11 # imre, cheaper contracts
    SpindleAndDraft = 10, "The Spindle and Draft", 12 # -2 IP

    # add a destroyed flag? and maybe method? 

    def __new__(cls, value, name, cost):
        member = object.__new__(cls)
        member._value_ = value
        member.fullname = name
        member.price = cost
        return member

    def __int__(self):
        return self.value
    
    def __str__(self):
        return f"{self.fullname} ({self.price} talents)"

LODGINGS = {
    # todo add non-starting lodgings
    "Anker's": Lodging.Ankers,
    "King's-Drab": Lodging.KingsDrab,
    "Golden-Pony": Lodging.GoldenPony,
    "Windy-Tower": Lodging.WindyTower,
    "Horse-and-Four": Lodging.HorseAndFour,
    "Spindle-and-Draft": Lodging.SpindleAndDraft
}


class Background(Enum): 
    Vint = 0, "Vintish Nobleman", 20, 30, [Lodging.HorseAndFour, Lodging.SpindleAndDraft]
    Aturan = 1, "Aturan Nobleman", 13.34, 20, [Lodging.WindyTower, Lodging.HorseAndFour]
    Yll = 2, "Yllish Commoner", 7.49, 11.23, [Lodging.GoldenPony, Lodging.WindyTower]
    Ceald = 3, "Cealdish Commoner", 6.58, 9.87, [Lodging.KingsDrab, Lodging.GoldenPony]
    Ruh = 4, "Edema Ruh", 3.4, 5.67, [Lodging.Ankers, Lodging.KingsDrab]

    def __new__(cls, value, name, initial_funds, stipend, lodging):
        member = object.__new__(cls)
        member._value_ = value
        member.fullname = name
        member.initial_funds = initial_funds
        member.stipend = stipend
        member.lodging = lodging
        return member

    def __int__(self):
        return self.value
    
    def __str__(self) -> str:
        return f"{self.fullname}"

# for conversion from distro page
BACKGROUNDS = {
    "Vintish-Nobleman": Background.Vint,
    "Aturan-Nobleman": Background.Aturan,
    "Yllish-Commoner": Background.Yll,
    "Cealdish-Commoner": Background.Ceald,
    "Edema-Ruh": Background.Ruh
}