from enum import Enum, IntEnum


class FieldName(IntEnum):
    LINGUISTICS = 0
    ARITHMETICS = 1
    RHETORICLOGIC = 2
    ARCHIVES = 3
    SYMPATHY = 4
    PHYSICKING = 5
    ALCHEMY = 6
    ARTIFICERY = 7
    NAMING = 8
    GENERAL = 9  # ? # gotta remember this when iterating thru
FIELDNAMES = ["Linguistics", "Arithmetics", "Rhetoric & Logic", "Archives", "Sympathy", "Physicking", "Alchemy", "Artificery", "Naming"]

class Rank(IntEnum):
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
    Ankers = 3, "Anker's", 4 # 15% 1 action cancelled
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
    "Anker's": Lodging.Ankers,
    "King's-Drab": Lodging.KingsDrab,
    "Golden-Pony": Lodging.GoldenPony,
    "Windy-Tower": Lodging.WindyTower,
    "Horse-and-Four": Lodging.HorseAndFour,
    "Spindle-and-Draft": Lodging.SpindleAndDraft,
    "Streets": Lodging.Streets,
    "Underthing": Lodging.Underthing,
    "Mews": Lodging.Mews,
    "Grey-Man": Lodging.GreyMan,
    "Pearl-of-Imre": Lodging.PearlOfImre
}
# for going to the next cheapest lodging if you can't afford current
NONIMRE_LODGINGS = [Lodging.Streets, Lodging.Mews, Lodging.Ankers, Lodging.KingsDrab, Lodging.GoldenPony, Lodging.WindyTower, Lodging.HorseAndFour, Lodging.SpindleAndDraft]


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