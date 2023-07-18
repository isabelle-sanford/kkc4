
from __future__ import annotations
import random
from typing import TYPE_CHECKING

from statics import FieldName, Rank

if TYPE_CHECKING:
    from player import Player
from enum import Enum, IntEnum
from actioninfo import Target

# want to use Ability2 (currently in actioninfo)
class Ability:
    def __init__(
        self,
        ability_name,
        field,
        min_rank: Rank,
        #is_passive,
        #is_negative,
        has_level_effects: bool,
        target1: Target, # TYPE
        target2 = Target.NONE,
        is_positive: bool = False,
        is_negative: bool = False,
        is_passive: bool = False
        # could add insanity bonus
        # todo: add category, probably - or just actiontype? 
    ):
        self.name = ability_name
        self.field = field
        self.min_rank = min_rank
        self.is_passive = is_passive
        self.target1 = target1
        self.target2 = target2
        self.has_level_effects = has_level_effects
        self.is_negative = is_negative
        self.is_positive = is_positive

class FieldInfo:
    def __init__(
        self,
        field: FieldName,
        name: str,
        # these should just be a list[Ability]
        abilities: list[Ability] = [],
        level1_AP = None,
        level2_AP = None,
        level3_AP = None,
        master_AP = None
    ):
        self.name = name
        self.field_id = field
        self.abilities = abilities

        self.level1_AP = level1_AP
        self.level2_AP = level2_AP
        self.level3_AP = level3_AP
        self.master_AP = master_AP

class FieldStatus:
    def __init__(self, field: FieldName, info: FieldInfo):
        self.name = field # hmm
        self.info = info
        self.EP = {} # dict player: numEP
        self.master: Player = None
        self.month = 0
        self.elevating: Player = None 
        self.elevatedOnce: list[int] = [] # since it's not actually rank? 
        self.elevatedTwice: list[int] = []
        self.elevatedThrice: list[int] = []
        self.next_masters: list[Player] = []
        self.DP = [] # todo
    
    def add_EP(self, player, num: int = 1):
        if player in self.EP:
            self.EP[player] += num
        else:
            self.EP[player] = num

    def get_EP_list(self):
        # for NPC master choosing
        EP_proportional_list: list[Player] = []
        for p, num in self.EP.items():
            for n in range(num):
                EP_proportional_list.append(p) # TODO test pls
        return EP_proportional_list
    
    # todo DESTROY
# ! need some way to record master's prev EP in case they destroy the field 
    def update_master_candidates(self):
        # remove ineligible candidates

        for candidate in self.next_masters:
            if self.EP[p] >= 15 and p.status.can_be_elevated:
                continue
            else:
                self.next_masters.remove(candidate) # is this ok?

        # add new potential candidates for master
        new_candidates = []
        for p, num in self.EP.items():
            if num >= 15:
                if p.status.rank == Rank.ELTHE and p.status.can_be_elevated:
                    new_candidates.append(p)
        
        random.shuffle(new_candidates)

        for n in new_candidates:
            if n not in self.next_masters:
                self.next_masters.append(n)

        if self.master is not None:
            return
        
        if len(self.next_masters) < 1:
            # no masters available
            return
        
        return self.next_masters


    # death, expulsion, insanity
    def remove_player(self, player):
        if player in self.EP:
            del self.EP[player]
        if player == self.master:
            self.master = None
            # TODO get new master 
        if player.id in self.elevatedOnce:
            self.elevatedOnce.remove(player.id)
        if player.id in self.elevatedTwice:
            self.elevatedTwice.remove(player.id)
        if player.id in self.elevatedThrice:
            self.elevatedThrice.remove(player.id)

    def elevate_player(self, player):
        n = self.EP[player]
        if n > 5:
            self.EP[player] -= 5
        else:
            self.EP[player] = 0
        
        if player.id in self.elevatedOnce:
            self.elevatedOnce.remove(player.id)
            self.elevatedTwice.append(player.id)
        elif player.id in self.elevatedTwice:
            self.elevatedTwice.remove(player.id)
            self.elevatedThrice.append(player.id)
        elif player.id in self.elevatedThrice:
            self.elevatedThrice.remove(player.id)
            self.master = player # more checks here? 
        else:
            self.elevatedOnce.append(player.id)
        
        if player.status.rank == Rank.ELTHE:
            # could do the remove_player here
            self.master = player # more stuff? idk
    


mysterious_bulletins = Ability(
    "Mysterious Bulletins", FieldName.LINGUISTICS, Rank.RELAR, False, Target.NONE)
hand_delivery = Ability(
    "Hand Delivery",
    FieldName.LINGUISTICS,
    Rank.ELIR,
    False,
    Target.NONE,
    is_passive=True
)
bribe_messenger = Ability(
    "Bribe Messenger",
    FieldName.LINGUISTICS,
    Rank.ELTHE,
    False, Target.PLAYER,
    is_negative=True # ??
)
linguistic_analysis = Ability(
    "Linguistic Analysis",
    FieldName.LINGUISTICS,
    Rank.MASTER,
    False,
    Target.PLAYER,
    is_negative=True #??
)

linguistics = FieldInfo(
    FieldName.LINGUISTICS,
    "Linguistics",
    [mysterious_bulletins,
    hand_delivery,
    bribe_messenger,
    linguistic_analysis],
    None,
    FieldName.GENERAL,
    FieldName.GENERAL,
    FieldName.GENERAL,
)

reduced_interest = Ability(
    "Reduced Interest",
    FieldName.ARITHMETICS,
    Rank.ELIR,
    True,
    Target.NONE,
    is_passive=True
)
pickpocket = Ability(
    "Pickpocket", FieldName.ARITHMETICS, Rank.ELIR, True, Target.PLAYER,
    is_negative=True
)  # only requires target at master level
great_deals = Ability(
    "Great Deals", FieldName.ARITHMETICS, Rank.ELIR, 
    True, 
    Target.NONE,
    is_passive=True
)
decreased_tuition = Ability(
    "Decreased Tuition",
    FieldName.ARITHMETICS,
    Rank.ELIR,
    True,
    Target.NONE,
    is_passive=True
)

arithmetics = FieldInfo(
    FieldName.ARITHMETICS,
    "Arithmetics",
    [reduced_interest,
    pickpocket,
    great_deals,
    decreased_tuition],
    master_AP=FieldName.ARITHMETICS,
)

law_of_contraposition = Ability(
    "Law of Contraposition",
    FieldName.RHETORICLOGIC,
    Rank.MASTER,
    False,
    Target.ACTION,
    target2=Target.PLAYER,
    # is_negative?
)
proficient_in_hyperbole = Ability(
    "Proficient in Hyperbole",
    FieldName.RHETORICLOGIC,
    Rank.RELAR,
    False,
    Target.PLAYER,
    Target.PLAYER
)
argumentum_ad_nauseam = Ability(
    "Argumentum Ad Nauseam",
    FieldName.RHETORICLOGIC,
    Rank.ELIR,
    False,
    Target.PLAYER
    # is_negative? 
)
persuasive_arguments = Ability(
    "Persuasive Arguments",
    FieldName.RHETORICLOGIC,
    Rank.ELTHE,
    False,
    Target.PLAYER,
    Target.PLAYER,
    # is_negative?
)

rhetoriclogic = FieldInfo(
    FieldName.RHETORICLOGIC,
    "Rhetoric & Logic",
    [law_of_contraposition,
    proficient_in_hyperbole,
    argumentum_ad_nauseam,
    persuasive_arguments],
    None,
    FieldName.RHETORICLOGIC,
    FieldName.RHETORICLOGIC,
    FieldName.RHETORICLOGIC,
)

fae_lore = Ability(
    "Fae Lore",
    FieldName.ARCHIVES,
    Rank.MASTER,
    False,
    Target.PLAYER, # ?
    is_negative=True
)
omen_recognition = Ability(
    "Omen Recognition",
    FieldName.ARCHIVES,
    Rank.ELIR,
    False,
    Target.EVENT
)
school_records = Ability( #Requires being at Uni
    "School Records",
    FieldName.ARCHIVES,
    Rank.RELAR,
    False,
    Target.PLAYER
)
banned_books = Ability(
    "Banned Books",
    FieldName.ARCHIVES,
    Rank.ELTHE,
    True, # not caught if master
    Target.FIELD,
    Target.ABILITY, # if field known

)

archives = FieldInfo(
    FieldName.ARCHIVES,
    "Archives",
    [fae_lore,
    omen_recognition,
    school_records,
    banned_books],
    None,
    FieldName.ARCHIVES,
    FieldName.ARCHIVES,
    FieldName.ARCHIVES,
)

mommet_making = Ability(
    "Mommet-making",
    FieldName.SYMPATHY,
    Rank.ELIR,
    True,
    Target.PLAYER, # DEAD player, only if 3rd level
    # is_negative?
)
malfeasance_protection = Ability(
    "Malfeasance Protection",
    FieldName.SYMPATHY,
    Rank.ELIR,
    True,
    Target.PLAYER,
    is_positive=True, # IF 3rd level though. oof.
    is_negative=True, # if not third level
)

sympathy = FieldInfo(
    FieldName.SYMPATHY,
    "Sympathy",
    [mommet_making,
    malfeasance_protection],
    FieldName.SYMPATHY,
    False,
    False,
    FieldName.SYMPATHY,
)

medica_emergency = Ability(
    "Medica Emergency",
    FieldName.PHYSICKING,
    Rank.ELIR,
    True,
    Target.NONE
)
medica_detainment = Ability(
    "Medica Detainment",
    FieldName.PHYSICKING,
    Rank.ELIR,
    True,
    Target.PLAYER,
    is_negative=True
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
    True,
    Target.PLAYER,
    is_positive=True
)

physicking = FieldInfo(
    FieldName.PHYSICKING,
    "Physicking",
    [medica_emergency,
    medica_detainment,
    psychological_counselling,
    cheating_death],
    master_AP=FieldName.PHYSICKING
)

tenaculum_creation = Ability(
    "Tenaculum",
    FieldName.ALCHEMY,
    Rank.ELIR,
    False,
    Target.ITEM, # kinda
)
firestop_creation = Ability(
    "Firestop",
    FieldName.ALCHEMY,
    Rank.RELAR,
    False,
    Target.ITEM, # kinda
)
plum_bob_creation = Ability(
    "Plum bob",
    FieldName.ALCHEMY,
    Rank.ELTHE,
    False,
    Target.ITEM, # kinda
)
bone_tar_creation = Ability(
    "Bone-tar",
    FieldName.ALCHEMY,
    Rank.ELTHE,
    False,
    Target.ITEM, # kinda
)

alchemy = FieldInfo(
    FieldName.ALCHEMY,
    "Alchemy",
    [tenaculum_creation,
    firestop_creation,
    plum_bob_creation,
    bone_tar_creation],
    False, # item creation period
    False,
    False,
    False,
)

ward_creation = Ability(
    "Ward",
    FieldName.ARTIFICERY,
    Rank.ELIR,
    True,
    Target.ITEM
)
bloodless_creation = Ability(
    "Bloodless",
    FieldName.ARTIFICERY,
    Rank.RELAR,
    True,
    Target.ITEM
)
thieves_lamp_creation = Ability(
    "Thieves Lamp",
    FieldName.ARTIFICERY,
    Rank.RELAR,
    True,
    Target.ITEM
)
gram_creation = Ability(
    "Gram",
    FieldName.ARTIFICERY,
    Rank.ELTHE,
    True,
    Target.ITEM
)

artificery = FieldInfo(
    FieldName.ARTIFICERY,
    "Artificery",
    [ward_creation,
    bloodless_creation,
    thieves_lamp_creation,
    gram_creation],
    FieldName.ARTIFICERY, # hm
    False,
    False,
    False,
)

# Dunno what to do with all the names. Don't seem quite appropriate as abilities? 
# Otherwise, need more ability fields to account for all names
naming = FieldInfo(
    FieldName.NAMING,
    "Naming",
    [], # ? 
    False,
    FieldName.NAMING,
    FieldName.NAMING,
    FieldName.NAMING,
)

# not sure where this should go (or if fieldInfo should even be separate)
ling_status = FieldStatus(FieldName.LINGUISTICS, linguistics)
arith_status = FieldStatus(FieldName.ARITHMETICS, arithmetics)
rl_status = FieldStatus(FieldName.RHETORICLOGIC, rhetoriclogic)
archive_status = FieldStatus(FieldName.ARCHIVES, archives)
sympathy_status = FieldStatus(FieldName.SYMPATHY, sympathy)
phys_status = FieldStatus(FieldName.SYMPATHY, sympathy)
alch_status = FieldStatus(FieldName.ALCHEMY, alchemy)
artificery_status = FieldStatus(FieldName.ARTIFICERY, artificery)
naming_status = FieldStatus(FieldName.NAMING, naming)

FIELDS = [ling_status, arith_status, rl_status, archive_status, sympathy_status, phys_status, alch_status, artificery_status, naming_status]