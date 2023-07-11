from enum import Enum, IntEnum



class Lodging(Enum):
    Streets = 0, "The Streets", 0
    Underthing = 1, "The Underthing", 0
    Mews = 2, "Mews", 1
    Ankers = 3, "Ankers", 4
    KingsDrab = 4, "The King's Drab", 6
    GreyMan = 5, "The Grey Man", 7
    GoldenPony = 6, "The Golden Pony", 8
    WindyTower = 7, "The Windy Tower", 9
    HorseAndFour = 8, "The Horse and Four", 10
    PearlOfImre = 9, "The Pearl of Imre", 11
    SpindleAndDraft = 10, "The Spindle and Draft", 12

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

# TODO some way to account for stipend change for vint/aturan
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
