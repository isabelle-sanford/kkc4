class Lodging:
    # could add description / effect
    def __init__(self, name, cost):
        self.name = name
        self.cost = cost


streets = Lodging("the streets", 0)
underthing = Lodging("The Underthing", 0)
mews = Lodging("Mews", 1)
ankers = Lodging("Ankers", 4)
kingsdrab = Lodging("The King's Drab", 6)
greyman = Lodging("The Grey Man", 7)
goldenpony = Lodging("The Golden Pony", 8)
windytower = Lodging("The Windy Tower", 9)
horseandfour = Lodging("The Horse and Four", 10)
pearlofimre = Lodging("The Pearl of Imre", 11)
spindleanddraft = Lodging("The Spindle and Draft", 12)

lodgings = [
    streets,
    underthing,
    mews,
    ankers,
    kingsdrab,
    greyman,
    goldenpony,
    windytower,
    horseandfour,
    pearlofimre,
    spindleanddraft,
]


class SocialClass:
    # could add effect
    def __init__(self, name, gamestart, stipend, startlodgings):
        self.name = name
        self.gamestart = gamestart
        self.stipend = stipend
        self.startlodgings = startlodgings


vint = SocialClass("Vintish Nobleman", 20, 30, [horseandfour, spindleanddraft])
aturan = SocialClass("Aturan Nobleman", 13.34, 20, [windytower, horseandfour])
yllish = SocialClass("Yllish Commoner", 7.49, 11.23, [goldenpony, windytower])
cealdish = SocialClass("Cealdish Commoner", 6.58, 9.87, [kingsdrab, goldenpony])
ruh = SocialClass("Edema Ruh", 3.4, 5.67, [ankers, kingsdrab])

social_classes = [vint, aturan, yllish, cealdish, ruh]


import random

from enum import Enum


class BaseStat(Enum):
    MUSIC = 1
    ESSAY = 2
    ART = 3


class Rank(Enum):
    ELIR = 1
    RELAR = 2
    ELTHE = 3
    MASTER = 4
    # NONE = 0 #?


class PlayerStart:
    def __init__(
        self, name, is_evil, social_class, base_stat_choice, base_stat_score, ep_choice
    ):
        self.name = name
        self.is_evil = is_evil
        self.social_class = social_class
        self.available_ep = 5

        # absolutely no idea if this works
        self.starting_lodging = random.choice(social_class.startlodgings)

        # TODO roll base stat stuff
        # if base_stat_choice == BaseStat.MUSIC:

        # if base_stat_choice == BaseStat.ESSAY:
        # (else roll starting EP)

        # if base_stat_choice == BaseStat.ART


class PlayerStatus:
    # note: WORK IN PROGRESS
    # this class is for keeping track of a player's status in a particular turn

    # vars: rank, lodging, enrolled, inImre, expelled, roleblocked(?), elev1field, elev2field, elev3field, elev4field, items, ...

    # put prev playerstatus in as arg?
    def __init__(self, player_prev, month):
        self.name = player_prev.name
        self.month = month  # or do month += 1


class PlayerChoices:
    def __init__(self, player_status):
        self.player = player_status

    # def takeAction

    # def fileEP

    # if term end, nextLodging() and enrollNext()


class FieldName(Enum):
    LINGUISTICS = 1
    ARITHMETICS = 2
    RHETORICLOGIC = 3
    ARCHIVES = 4
    SYMPATHY = 5
    PHYSICKING = 6
    ALCHEMY = 7
    ARTIFICERY = 8
    NAMING = 9
    GENERAL = 10  # ?


class Ability:
    def __init__(
        self,
        ability_name,
        field,
        min_rank,
        is_passive,
        is_negative,
        has_level_effects,
        requires_target,
        requires_second_target,
    ):
        self.name = ability_name
        self.field = field
        self.min_rank = min_rank
        self.is_passive = is_passive
        self.requires_target = requires_target
        self.requires_second_target = requires_second_target
        self.has_level_effects = has_level_effects
        self.is_negative = is_negative


# enum for fields (+ general as 0?)


class FieldInfo:
    def __init__(
        self,
        field,
        name,
        ability1,
        ability2,
        ability3,
        ability4,
        level1_AP,
        level2_AP,
        level3_AP,
        master_AP,
    ):
        self.name = name
        self.field_id = field
        self.ability1 = ability1
        self.ability2 = ability2
        self.ability3 = ability3
        self.ability4 = ability4

        self.level1_AP = level1_AP
        self.level2_AP = level2_AP
        self.level3_AP = level3_AP
        self.master_AP = master_AP


# might want to do the is_passive=True, etc stuff
mysterious_bulletins = Ability(
    "Hand Delivery", FieldName.LINGUISTICS, Rank.ELIR, True, False, False, False
)
hand_delivery = Ability(
    "Hand Delivery",
    FieldName.LINGUISTICS,
    Rank.RELAR,
    False,
    False,
    False,
    False,
    False,
)
bribe_messenger = Ability(
    "Bribe Messenger",
    FieldName.LINGUISTICS,
    Rank.ELTHE,
    False,
    True,
    False,
    True,
    False,
)
linguistic_analysis = Ability(
    "Linguistic Analysis",
    FieldName.LINGUISTICS,
    Rank.MASTER,
    False,
    True,
    False,
    True,
    False,
)


linguistics = FieldInfo(
    FieldName.LINGUISTICS,
    "Linguistics",
    mysterious_bulletins,
    hand_delivery,
    bribe_messenger,
    linguistic_analysis,
    False,
    FieldName.GENERAL,
    FieldName.GENERAL,
    FieldName.GENERAL,
)

reduced_interest = Ability(
    "Reduced Interest",
    FieldName.ARITHMETICS,
    Rank.ELIR,
    True,
    False,
    True,
    False,
    False,
)
pickpocket = Ability(
    "Pickpocket", FieldName.ARITHMETICS, Rank.ELIR, False, True, True, True, False
)  # only requires target at master level
great_deals = Ability(
    "Great Deals", FieldName.ARITHMETICS, Rank.ELIR, True, False, True, False, False
)
decreased_tuition = Ability(
    "Decreased Tuition",
    FieldName.ARITHMETICS,
    Rank.ELIR,
    True,
    False,
    True,
    False,
    False,
)

arithmetics = FieldInfo(
    FieldName.ARITHMETICS,
    "Arithmetics",
    reduced_interest,
    pickpocket,
    great_deals,
    decreased_tuition,
    master_AP=FieldName.ARITHMETICS,
)

law_of_contraposition = Ability(
    "Law of Contraposition",
    FieldName.RHETORICLOGIC,
    Rank.MASTER,
    False,
    False, #Redirect is not attack/roleblock
    False,
    True,
    True,
)
proficient_in_hyperbole = Ability(
    "Proficient in Hyperbole",
    FieldName.RHETORICLOGIC,
    Rank.RELAR,
    False,
    False,
    False,
    True,
    True, #Not specified in player actions, but is technically up to two targets?
)
argumentum_ad_nauseam = Ability(
    "Argumentum Ad Nauseam",
    FieldName.RHETORICLOGIC,
    Rank.ELIR,
    False,
    False, #Blocking a complaint isn't an action roleblock?
    False,
    True,
    False,
)
persuasive_arguments = Ability(
    "Persuasive Arguments",
    FieldName.RHETORICLOGIC,
    Rank.ELTHE,
    False,
    False, #Redirect, and of complaints not actions.
    False,
    True,
    True
)

rhetoriclogic = FieldInfo(
    FieldName.RHETORICLOGIC,
    "Rhetoric & Logic",
    law_of_contraposition,
    proficient_in_hyperbole,
    argumentum_ad_nauseam,
    persuasive_arguments,
    False,
    FieldName.RHETORICLOGIC,
    FieldName.RHETORICLOGIC,
    FieldName.RHETORICLOGIC,
)

fae_lore = Ability(
    "Fae Lore",
    FieldName.ARCHIVES,
    Rank.MASTER,
    False, # ?? It's sorta passive in that it is an additional effect on a different action?
    True, # Roleblock action (for Fae)
    False,
    False, # This doesn't so much target a player as enhance another action/inherit the target from the other action? 
    False,
)
omen_recognition = Ability(
    "Omen Recognition",
    FieldName.ARCHIVES,
    Rank.ELIR,
    False,
    False,
    False,
    True, # Doesn't target a player so much?
    False,
)
school_records = Ability( #Requires being at Uni
    "School Records",
    FieldName.ARCHIVES,
    Rank.RELAR,
    False,
    False, 
    False,
    True,
    False,
)
banned_books = Ability(
    "Banned Books",
    FieldName.ARCHIVES,
    Rank.ELTHE,
    False,
    False,
    True, # Does this need to be given more info? Masters don't get caught
    True, # Targets a field?
    False,
)

archives = FieldInfo(
    FieldName.ARCHIVES,
    "Archives",
    fae_lore,
    omen_recognition,
    school_records,
    banned_books,
    False,
    FieldName.ARCHIVES,
    FieldName.ARCHIVES,
    FieldName.ARCHIVES,
)

mommet_making = Ability(
    "Mommet-making",
    FieldName.SYMPATHY,
    Rank.ELIR,
    False,
    False, #Making the Mommet isn't an attack, rather using is.
    True,
    False,
    False,
)
malfeasance_protection = Ability(
    "Malfeasance Protection",
    FieldName.SYMPATHY,
    Rank.ELIR,
    False,
    True,
    True,
    True,
    False,
)

sympathy = FieldInfo(
    FieldName.SYMPATHY,
    "Sympathy",
    mommet_making,
    malfeasance_protection,
    False,
    False,
    FieldName.SYMPATHY,
    False,
    False,
    FieldName.SYMPATHY,
)

medica_emergency = Ability(
    "Medica Emergency",
    FieldName.PHYSICKING,
    Rank.ELIR,
    False,
    False, #Roleblocks yourself? Sorta?
    True,
    False,
    False,
)
medica_detainment = Ability(
    "Medica Detainment",
    FieldName.PHYSICKING,
    Rank.ELIR,
    False,
    True, 
    True,
    True,
    False,
)
psychological_counselling = Ability(
    "Psychological Counselling",
    FieldName.PHYSICKING,
    Rank.ELIR,
    False,
    False,
    True,
    True,
    False,
)
cheating_death = Ability(
    "Cheating Death",
    FieldName.PHYSICKING,
    Rank.ELIR,
    False,
    False,
    True,
    True,
    False,
)

physicking = FieldInfo(
    FieldName.PHYSICKING,
    "Physicking",
    medica_emergency,
    medica_detainment,
    psychological_counselling,
    cheating_death,
    master_AP=FieldName.PHYSICKING
)

tenaculum = Ability(
    "Tenaculum",
    FieldName.ALCHEMY,
    Rank.ELIR,
    False,
    False,
    True,
    False,
    False,
)
firestop = Ability(
    "Firestop",
    FieldName.ALCHEMY,
    Rank.RELAR,
    False,
    False,
    True,
    False,
    False,
)
plum_bob = Ability(
    "Plum bob",
    FieldName.ALCHEMY,
    Rank.ELTHE,
    False,
    False,
    True,
    False,
    False,
)
bone_tar = Ability(
    "Bone-tar",
    FieldName.ALCHEMY,
    Rank.ELTHE,
    False,
    False,
    True,
    False,
    False,
)

alchemy = FieldInfo(
    FieldName.ALCHEMY,
    "Alchemy",
    tenaculum,
    firestop,
    plum_bob,
    bone_tar,
    False,
    False,
    False,
    False,
)

ward = Ability(
    "Ward",
    FieldName.ARTIFICERY,
    Rank.ELIR,
    False,
    False,
    False,
    False,
    False,
)
bloodless = Ability(
    "Bloodless",
    FieldName.ARTIFICERY,
    Rank.RELAR,
    False,
    False,
    False,
    False,
    False,
)
thieves_lamp = Ability(
    "Thieves Lamp",
    FieldName.ARTIFICERY,
    Rank.RELAR,
    False,
    False,
    False,
    False,
    False,
)
gram = Ability(
    "Gram",
    FieldName.ARTIFICERY,
    Rank.ELTHE,
    False,
    False,
    False,
    False,
    False,
)

artificery = FieldInfo(
    FieldName.ARTIFICERY,
    "Artificery",
    ward,
    bloodless,
    thieves_lamp,
    gram,
    FieldName.ARTIFICERY,
    False,
    False,
    False,
)

# Dunno what to do with all the names. Don't seem quite appropriate as abilities? 
# Otherwise, need more ability fields to account for all names
naming = FieldInfo(
    FieldName.NAMING,
    "Naming",
    False,
    False,
    False,
    False,
    False,
    FieldName.NAMING,
    FieldName.NAMING,
    FieldName.NAMING,
)