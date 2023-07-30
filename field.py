
from __future__ import annotations
import random
from typing import TYPE_CHECKING

from statics import FieldName, Rank

if TYPE_CHECKING:
    from player import Player
from enum import Enum, IntEnum
from actioninfo import Target, ActionType

class ActionPeriod(Enum):
    LINGUISTICS = 0
    ARITHMETICS = 1
    RHETORICLOGIC = 2
    ARCHIVES = 3
    SYMPATHY = 4
    PHYSICKING = 5
    
    NAMING = 8
    GENERAL = 9 
    ITEMCREATION = 10
    # any others?



# want to use Ability2 (currently in actioninfo)
class Ability:
    def __init__(
        self,
        ability_name,
        field,
        min_rank: Rank,
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
        abilities: list[ActionType] = [],
        APbylevel = [None, None, None, None]
    ):
        self.name = name
        self.field_id = field
        self.abilities = abilities

        self.APbylevel = APbylevel

class FieldStatus:
    def __init__(self, field: FieldName, info: FieldInfo):
        self.name = field # hmm
        self.info = info
        self.EP = {} # dict player: numEP
        self.master: Player = None
        self.month = 0
        self.elevating: Player = None 
        self.elevatedOnce: list[int] = [] 
        self.elevatedTwice: list[int] = []
        self.elevatedThrice: list[int] = []
        self.next_masters: list[Player] = []
        self.DP = [] # todo
        # todo: prev masters always have highest priority
    
    def add_EP(self, player, num: int = 1):
        if player in self.EP:
            self.EP[player] += num
        else:
            self.EP[player] = num

    def get_EP_list(self):
        # for NPC master choosing
        EP_proportional_list: list[Player] = []
        for p, num in self.EP.items():
            if p.status.is_enrolled: # make sure this is BEFORE term switch
                for n in range(num):
                    EP_proportional_list.append(p) # TODO test pls
        return EP_proportional_list
    
    # todo DESTROY

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


    # death, expulsion, insanity, masters
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
    


linguistics = FieldInfo(
    FieldName.LINGUISTICS,
    "Linguistics",
    [ActionType.HandDelivery,
     ActionType.MysteriousBulletins,
     ActionType.BribeTheMessenger,
     ActionType.LinguisticAnalysis],
    [None,
    ActionPeriod.GENERAL,
    ActionPeriod.GENERAL,
    ActionPeriod.GENERAL],
)

arithmetics = FieldInfo(
    FieldName.ARITHMETICS,
    "Arithmetics",
    [ActionType.ReducedInterest,
     ActionType.GreatDeals,
     ActionType.Pickpocket,
     ActionType.DecreasedTuition],
    [None, None, None, ActionPeriod.GENERAL],
)



rhetoriclogic = FieldInfo(
    FieldName.RHETORICLOGIC,
    "Rhetoric & Logic",
    [ActionType.ArgumentumAdNauseam,
     ActionType.ProficientInHyperbole,
     ActionType.PersuasiveArguments,
     ActionType.LawOfContraposition],
    [None,
    ActionPeriod.RHETORICLOGIC,
    ActionPeriod.RHETORICLOGIC,
    ActionPeriod.RHETORICLOGIC]
)


archives = FieldInfo(
    FieldName.ARCHIVES,
    "Archives",
    [ActionType.OmenRecognition,
     ActionType.SchoolRecords,
     ActionType.BannedBooks,
     ActionType.FaeLore],
    [None,
    ActionPeriod.ARCHIVES,
    ActionPeriod.ARCHIVES,
    ActionPeriod.ARCHIVES],
)

sympathy = FieldInfo(
    FieldName.SYMPATHY,
    "Sympathy",
    [ActionType.MommetMaking,
     ActionType.MalfeasanceProtection],
    [ActionPeriod.SYMPATHY,
    None,
    None,
    ActionPeriod.SYMPATHY],
)

physicking = FieldInfo(
    FieldName.PHYSICKING,
    "Physicking",
    [ActionType.MedicaEmergency,
     ActionType.MedicaDetainment,
     ActionType.PsychologicalCounselling,
     ActionType.CheatingDeath],
     [None, None, None, ActionPeriod.PHYSICKING],
)



alchemy = FieldInfo(
    FieldName.ALCHEMY,
    "Alchemy",
    [ActionType.CreateTenaculum,
     ActionType.CreateFirestop,
     ActionType.CreatePlumbob,
     ActionType.CreateBonetar],
    [ActionPeriod.ITEMCREATION, None, None, None]
)



artificery = FieldInfo(
    FieldName.ARTIFICERY,
    "Artificery",
    [ActionType.CreateWard,
     ActionType.CreateBloodless,
     ActionType.CreateThievesLamp,
     ActionType.CreateGram],
    [ActionPeriod.ITEMCREATION, None, None, None]
)

# Dunno what to do with all the names. Don't seem quite appropriate as abilities? 
# Otherwise, need more ability fields to account for all names
naming = FieldInfo(
    FieldName.NAMING,
    "Naming",
    [ActionType.UseName], # ? 
    [None,
    FieldName.NAMING,
    FieldName.NAMING,
    FieldName.NAMING],
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