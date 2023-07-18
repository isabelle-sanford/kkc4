from dataclasses import dataclass
from enum import Enum
from statics import FieldName, Rank

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from field import Rank

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
    min_rank: Rank = Rank.ELIR
    has_level_effects: bool = False

@dataclass
class ActionInfo:
    id: int
    name: str
    category: ActionCategory
    # type? 
    target1: Target = Target.NONE
    target2: Target = Target.NONE
    is_positive: bool = False
    is_negative: bool = False
    insanity_bonus: int = 0
    field_ability: Ability2 = None
    is_passive: bool = False # only for field abilities tbh


hand_delivery = ActionInfo(1, "Hand Delivery", ActionCategory.OTHER, field_ability=Ability2(FieldName.LINGUISTICS, Rank.ELIR), is_passive=True)
myst_bulletins = ActionInfo(2, "Mysterious Bulletins", ActionCategory.OTHER, Target.NONE, field_ability=Ability2(FieldName.LINGUISTICS, Rank.RELAR))
bribe_messenger = ActionInfo(3, "Bribe the Messenger", ActionCategory.OTHER, Target.PLAYER, field_ability=Ability2(FieldName.LINGUISTICS, Rank.ELTHE))
linguistic_analysis = ActionInfo(4, "Linguistic Analysis", ActionCategory.OTHER, Target.PLAYER, field_ability=Ability2(FieldName.LINGUISTICS, Rank.MASTER))

reduced_interest = ActionInfo(33, "Reduced Interest", ActionCategory.OTHER, field_ability=Ability2(FieldName.ARITHMETICS, Rank.ELIR,True), is_passive=True)
pickpocket = ActionInfo(5, "Pickpocket", ActionCategory.BLOCKETC, Target.PLAYER, is_negative=True, field_ability=Ability2(FieldName.ARITHMETICS, Rank.ELIR, True)) 
great_deals = ActionInfo(34, "Great Deals", ActionCategory.OTHER, field_ability=Ability2(FieldName.ARITHMETICS, Rank.ELIR, True), is_passive=True)
decreased_tuition = ActionInfo(35, "Decreased Tuition", ActionCategory.OTHER, Target.PLAYER, field_ability=Ability2(FieldName.ARITHMETICS, Rank.ELIR, True), is_passive=True)

argumentum_ad_nauseam = ActionInfo(6, "Argumentum Ad Nauseam", ActionCategory.OTHER, field_ability=Ability2(FieldName.RHETORICLOGIC, Rank.ELIR))
proficient_in_hyperbole = ActionInfo(7, "Proficient In Hyperbole", ActionCategory.OTHER, Target.PLAYER, Target.PLAYER, field_ability=Ability2(FieldName.RHETORICLOGIC, Rank.RELAR))
persuasive_arguments = ActionInfo(8, "Persuasive Arguments", ActionCategory.OTHER, Target.PLAYER, Target.PLAYER, field_ability=Ability2(FieldName.RHETORICLOGIC, Rank.ELTHE))
law_of_contraposition = ActionInfo(9, "Law of Contraposition", ActionCategory.OTHER, Target.PLAYER, Target.PLAYER, field_ability=Ability2(FieldName.RHETORICLOGIC, Rank.MASTER))

omen_recognition = ActionInfo(19, "Omen Recognition", ActionCategory.OTHER, Target.EVENT, field_ability=Ability2(FieldName.ARCHIVES, Rank.ELIR))
school_records = ActionInfo(11, "School Records", ActionCategory.OTHER, Target.PLAYER, field_ability=Ability2(FieldName.ARCHIVES, Rank.RELAR))
banned_books = ActionInfo(12, "Banned Books", ActionCategory.OTHER, Target.FIELD, field_ability=Ability2(FieldName.ARCHIVES, Rank.ELTHE, True))
fae_lore = ActionInfo(13, "Fae Lore", ActionCategory.BLOCKETC, Target.PLAYER, field_ability=Ability2(FieldName.ARCHIVES, Rank.MASTER))

mommet_making = ActionInfo(14, "Mommet Making", ActionCategory.CREATEITEM, Target.PLAYER, field_ability=Ability2(FieldName.SYMPATHY, Rank.ELIR, True)) # IB per level
malfeasance_protection = ActionInfo(15, "Mommet Protection", ActionCategory.CREATEITEM, Target.PLAYER, field_ability=Ability2(FieldName.SYMPATHY, Rank.ELIR, True)) # SOMETIMES negative; IB is per level


medica_emergency = ActionInfo(16, "Medica Emergency", ActionCategory.OTHER, field_ability=Ability2(FieldName.PHYSICKING, Rank.ELIR, True))
medica_detainment = ActionInfo(16, "Medica Detainment", ActionCategory.BLOCKETC, Target.PLAYER, is_negative=True, field_ability=Ability2(FieldName.PHYSICKING, Rank.ELIR, True))
psych_counselling = ActionInfo(17, "")
# TODO




sabotage = ActionInfo(41, "Sabotage", ActionCategory.OFFENSIVE, Target.PLAYER, is_negative=True)

# TODO 
class ActionType(Enum):
    # isn't there a way to generate enums instead of having to have them all here like this? 
    HandDelivery = 1, hand_delivery
    MysteriousBulletins = 2, myst_bulletins
    BribeTheMessenger = 3, bribe_messenger
    LinguisticAnalysis = 4, linguistic_analysis
    Pickpocket = 5,
    ArgumentumAdNauseam = 6, 
    ProficientInHyperbole = 7, 
    PersuasiveArguments = 8, 
    LawOfContraposition = 9, 
    OmenRecognition = 10, 
    SchoolRecords = 11,
    BannedBooks = 12
    FaeLore = 13,
    MommetMaking = 14
    MalfeasanceProtection = 15,
    MedicaEmergency = 16
    MedicaDetainment = 17, 
    PsychologicalCounselling = 18
    CheatingDeath = 19

    # what if single CreateItem action type, target is item
    CreateItem = 20
    CreateHalfItem = 21
    # CreateTenaculum = 20
    # CreateFirestop = 21
    # CreatePlumbob = 22
    # CreateBonetar = 23
    # CreateWard = 24
    # CreateBloodless = 25
    # CreateThievesLamp = 27
    # CreateGram = 28
    
    UseName = 22

    # what if UseItem type
    UseMommet = 23 , 
    UseTenaculumItem = 24
    UseTenaculumAction = 25 
    UsePlumbob = 26, 
    UseBonetar = 35,
    UseWard = 27,
    UseThievesLamp = 28 , 
    UseNahlrout = 29 , 
    UseCourier = 30, 

    # ! maybe don't include this at all tbh? 
    #UseAssassin = 40, ActionCategory.OFFENSIVE, Target.PLAYER, Target.NONE # player # note - does not take an action period / can't be blocked

    Sabotage = 31, sabotage

    GiveItem = 32

    # PASSIVE, maybe shouldn't be here 
    ReducedInterest = 33, reduced_interest
    GreatDeals = 34, great_deals
    DecreasedTuition = 35, decreased_tuition


    def __new__(cls, value, info):
        member = object.__new__(cls)
        member._value_ = value
        member.info = info
        return member

    def __int__(self):
        return self.value
    
    def __str__(self):
        return f"{self.info} ({self.value})"