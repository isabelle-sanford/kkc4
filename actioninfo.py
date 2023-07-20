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
    CREATEITEM = 4 # hmm


class Target(Enum):
    PLAYER = 1
    ACTION = 2
    LOCATION = 3
    ITEM = 4 # maybe distinguish item and itemtype?
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
    #name: str = ""

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



hd_ability = Ability2(FieldName.LINGUISTICS, Rank.ELIR, 1)
hand_delivery = ActionInfo(1, "Hand Delivery", ActionCategory.OTHER, field_ability=hd_ability, is_passive=True)

myst_bulletins = ActionInfo(2, "Mysterious Bulletins", ActionCategory.OTHER, Target.NONE, field_ability=Ability2(FieldName.LINGUISTICS, Rank.RELAR))
bribe_messenger = ActionInfo(3, "Bribe the Messenger", ActionCategory.OTHER, Target.PLAYER, field_ability=Ability2(FieldName.LINGUISTICS, Rank.ELTHE))
linguistic_analysis = ActionInfo(4, "Linguistic Analysis", ActionCategory.OTHER, Target.PLAYER, field_ability=Ability2(FieldName.LINGUISTICS, Rank.MASTER))

reduced_interest = ActionInfo(33, "Reduced Interest", ActionCategory.OTHER, field_ability=Ability2(FieldName.ARITHMETICS, Rank.ELIR,True), is_passive=True)
pickpocket = ActionInfo(5, "Pickpocket", ActionCategory.BLOCKETC, Target.PLAYER, is_negative=True, field_ability=Ability2(FieldName.ARITHMETICS, Rank.ELIR, True)) 
great_deals = ActionInfo(34, "Great Deals", ActionCategory.OTHER, field_ability=Ability2(FieldName.ARITHMETICS, Rank.ELIR, True), is_passive=True)
decreased_tuition = ActionInfo(35, "Decreased Tuition", ActionCategory.OTHER, Target.PLAYER, field_ability=Ability2(FieldName.ARITHMETICS, Rank.ELIR, True), is_passive=True)

argumentum_ad_nauseam = ActionInfo(6, "Argumentum Ad Nauseam", ActionCategory.OTHER, field_ability=Ability2(FieldName.RHETORICLOGIC, Rank.ELIR), is_negative=True) # IS NEGATIVE
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
medica_detainment = ActionInfo(17, "Medica Detainment", ActionCategory.BLOCKETC, Target.PLAYER, is_negative=True, field_ability=Ability2(FieldName.PHYSICKING, Rank.ELIR, True))
psych_counselling = ActionInfo(18, "Psychological Counselling", ActionCategory.OTHER, Target.PLAYER, is_positive=True, field_ability=Ability2(FieldName.PHYSICKING, Rank.ELIR, True))
cheating_death = ActionInfo(19, "Cheating Death", ActionCategory.OTHER, Target.PLAYER, is_positive=True, field_ability=Ability2(FieldName.PHYSICKING,Rank.ELIR, True))

# Alchemy
create_tenaculum = ActionInfo(36, "Create Tenaculum", ActionCategory.CREATEITEM, Target.ITEM, field_ability=Ability2(FieldName.ALCHEMY, Rank.ELIR, True), insanity_bonus=1)
create_firestop = ActionInfo(37, "Create Firestop", ActionCategory.CREATEITEM, Target.ITEM, field_ability=Ability2(FieldName.ALCHEMY, Rank.RELAR, True), insanity_bonus=2)
create_plumbob = ActionInfo(38, "Create Plumbob", ActionCategory.CREATEITEM, Target.ITEM, field_ability=Ability2(FieldName.ALCHEMY, Rank.ELIR, True), insanity_bonus=3)
create_bonetar = ActionInfo(39, "Create Bonetar", ActionCategory.CREATEITEM, Target.ITEM, field_ability=Ability2(FieldName.ALCHEMY, Rank.ELTHE, True), insanity_bonus=3)

# Artificery
create_ward = ActionInfo(40, "Create Ward", ActionCategory.CREATEITEM, Target.ITEM, field_ability=Ability2(FieldName.ARTIFICERY, Rank.ELIR, True), insanity_bonus=1)
create_bloodless = ActionInfo(41, "Create Bloodless", ActionCategory.CREATEITEM, Target.ITEM, field_ability=Ability2(FieldName.ARTIFICERY, Rank.RELAR, True), insanity_bonus=2)
create_thieveslamp = ActionInfo(42, "Create Thieves Lamp", ActionCategory.CREATEITEM, field_ability=Ability2(FieldName.ARTIFICERY, Rank.RELAR, True), insanity_bonus=2)
create_gram = ActionInfo(43, "Create Gram", ActionCategory.CREATEITEM, Target.ITEM, field_ability=Ability2(FieldName.ARTIFICERY, Rank.ELTHE, True), insanity_bonus=3)

create_item = ActionInfo(20, "Create Item", ActionCategory.CREATEITEM, Target.ITEM)
create_half_item = ActionInfo(21, "Create Half Item", ActionCategory.CREATEITEM, Target.ITEM)

use_name = ActionInfo(22, "Use Name", ActionCategory.OTHER, field_ability=Ability2(FieldName.NAMING))

use_mommet = ActionInfo(23, "Use Mommet", ActionCategory.BLOCKETC, is_negative=True) # IB 
use_tenaculum_item = ActionInfo(24, "Use Tenaculum (Item)", ActionCategory.BLOCKETC, Target.ITEM, is_negative=True)
use_tenaculum_action = ActionInfo(25, "Use Tenaculum (Action)", ActionCategory.BLOCKETC, Target.ACTION, is_negative=True)
use_plumbob = ActionInfo(26, "Use Plum Bob", ActionCategory.OTHER, Target.PLAYER, is_negative=True) # neg?
use_bonetar = ActionInfo(27, "Use Bonetar", ActionCategory.OFFENSIVE, Target.LOCATION, is_negative=True)
use_ward = ActionInfo(28, "Use Ward", ActionCategory.OTHER)
use_thieveslamp = ActionInfo(29, "Use Thieves Lamp", ActionCategory.BLOCKETC, Target.PLAYER, is_negative=True)
use_nahlrout = ActionInfo(30, "Use Nahlrout", ActionCategory.BLOCKETC, Target.PLAYER, is_negative=True)

sabotage = ActionInfo(31, "Sabotage", ActionCategory.OFFENSIVE, Target.PLAYER, is_negative=True)

give_item = ActionInfo(32, "Give Item", ActionCategory.OTHER, Target.PLAYER, Target.ITEM, is_positive=True)

# TODO 
class ActionType(Enum):
    # isn't there a way to generate enums instead of having to have them all here like this? 
    HandDelivery = 1, hand_delivery
    MysteriousBulletins = 2, myst_bulletins
    BribeTheMessenger = 3, bribe_messenger
    LinguisticAnalysis = 4, linguistic_analysis
    Pickpocket = 5, pickpocket
    ArgumentumAdNauseam = 6, argumentum_ad_nauseam
    ProficientInHyperbole = 7, proficient_in_hyperbole
    PersuasiveArguments = 8, persuasive_arguments
    LawOfContraposition = 9, law_of_contraposition
    OmenRecognition = 10, omen_recognition
    SchoolRecords = 11, school_records
    BannedBooks = 12, banned_books
    FaeLore = 13, fae_lore
    MommetMaking = 14, mommet_making
    MalfeasanceProtection = 15, malfeasance_protection
    MedicaEmergency = 16, medica_emergency
    MedicaDetainment = 17, medica_detainment
    PsychologicalCounselling = 18, psych_counselling
    CheatingDeath = 19, cheating_death

    # what if single CreateItem action type, target is item
    CreateItem = 20, create_item
    CreateHalfItem = 21, create_half_item
    
    UseName = 22, use_name

    # what if UseItem type - no, too many targets then
    UseMommet = 23 , use_mommet
    UseTenaculumItem = 24, use_tenaculum_item
    UseTenaculumAction = 25, use_tenaculum_action
    UsePlumbob = 26, use_plumbob
    UseBonetar = 27, use_bonetar
    UseWard = 28, use_ward
    UseThievesLamp = 29, use_thieveslamp
    UseNahlrout = 30, use_nahlrout

    Sabotage = 31, sabotage

    GiveItem = 32, give_item

    # PASSIVE, maybe shouldn't be here 
    ReducedInterest = 33, reduced_interest
    GreatDeals = 34, great_deals
    DecreasedTuition = 35, decreased_tuition

    # kinda need for accessible abilities stuff
    CreateTenaculum = 36
    CreateFirestop = 37
    CreatePlumbob = 38
    CreateBonetar = 39
    CreateWard = 40
    CreateBloodless = 41
    CreateThievesLamp = 42
    CreateGram = 43


    def __new__(cls, value, info):
        member = object.__new__(cls)
        member._value_ = value
        member.info = info
        return member

    def __int__(self):
        return self.value
    
    def __str__(self):
        return f"{self.info} ({self.value})"