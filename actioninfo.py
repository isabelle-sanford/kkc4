from dataclasses import dataclass
from enum import Enum

from field import Ability, FieldName, Rank


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
class Ability2():
    field: FieldName
    min_rank: Rank
    has_level_effects: bool = False

@dataclass
class ActionInfo:
    id: int
    name: str
    category: ActionCategory
    target1: Target = Target.NONE
    target2: Target = Target.NONE
    is_positive: bool = False
    is_negative: bool = False
    insanity_bonus: int = 0
    field_ability: Ability2 = None
    is_passive: bool = False # only for field abilities tbh


hand_delivery = ActionInfo(1, "Hand Delivery", ActionCategory.OTHER, field_ability=Ability2(FieldName.LINGUISTICS), is_passive=True)
myst_bulletins = ActionInfo(2, "Mysterious Bulletins", ActionCategory.OTHER, Target.NONE, field_ability=Ability2(FieldName.LINGUISTICS, Rank.RELAR))
bribe_messenger = ActionInfo(3, "Bribe the Messenger", ActionCategory.OTHER, Target.PLAYER, field_ability=Ability2(FieldName.LINGUISTICS, Rank.ELTHE))
linguistic_analysis = ActionInfo(4, "Linguistic Analysis", ActionCategory.OTHER, Target.PLAYER, field_ability=Ability2(FieldName.LINGUISTICS, Rank.MASTER))

reduced_interest = ActionInfo(5, "Reduced Interest", ActionCategory.OTHER, field_ability=Ability2(FieldName.ARITHMETICS, Rank.ELIR,True), is_passive=True)
pickpocket = ActionInfo(6, "Pickpocket", ActionCategory.BLOCKETC, Target.PLAYER, is_negative=True, field_ability=Ability2(FieldName.ARITHMETICS, Rank.ELIR, True)) 
great_deals = ActionInfo(7, "Great Deals", ActionCategory.OTHER, field_ability=Ability2(FieldName.ARITHMETICS, Rank.ELIR, True), is_passive=True)
decreased_tution = ActionInfo(8, "Decreased Tuition", ActionCategory.OTHER, Target.PLAYER, field_ability=Ability2(FieldName.ARITHMETICS, Rank.ELIR, True), is_passive=True)

argumentum_ad_nauseam = ActionInfo(9, "Argumentum Ad Nauseam", ActionCategory.OTHER, field_ability=Ability2(FieldName.RHETORICLOGIC, Rank.ELIR))
proficient_in_hyperbole = ActionInfo(9, "Proficient In Hyperbole", ActionCategory.OTHER, Target.PLAYER, Target.PLAYER, field_ability=Ability2(FieldName.RHETORICLOGIC, Rank.RELAR))
persuasive_arguments = ActionInfo(10, "Persuasive Arguments", ActionCategory.OTHER, Target.PLAYER, Target.PLAYER, field_ability=Ability2(FieldName.RHETORICLOGIC, Rank.ELTHE))
law_of_contraposition = ActionInfo(11, "Law of Contraposition", ActionCategory.OTHER, Target.PLAYER, Target.PLAYER, field_ability=Ability2(FieldName.RHETORICLOGIC, Rank.MASTER))

omen_recognition = ActionInfo(12, "Omen Recognition", ActionCategory.OTHER, Target.EVENT, field_ability=Ability2(FieldName.ARCHIVES, Rank.ELIR))
school_records = ActionInfo(13, "School Records", ActionCategory.OTHER, Target.PLAYER, field_ability=Ability2(FieldName.ARCHIVES, Rank.RELAR))
# TODO

# TODO 
class ActionType(Enum):
    # isn't there a way to generate enums instead of having to have them all here like this? 
    HandDelivery = 1, hand_delivery
    MysteriousBulletins = 2, myst_bulletins
    BribeTheMessenger = 3, bribe_messenger
    LinguisticAnalysis = 4, linguistic_analysis
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