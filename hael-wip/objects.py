import random
from enum import Enum, IntEnum
from log import Log, LogOutcome



# Could be worth trying this: https://stackoverflow.com/questions/6060635/convert-enum-to-int-in-python
# I.E. use aenum, though does mean using an additional package beyond the stdlib
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


class Background(Enum): 
    Vint = 0, "Vintish Nobleman", 20, 30, [Lodging.HorseAndFour, Lodging.SpindleAndDraft]
    Aturan = 1, "Aturan Nobleman", 13.34, 20, [Lodging.WindyTower, Lodging.HorseAndFour]
    Yll = 2, "Yllish Commoner", 7.49, 11.23, [Lodging.GoldenPony, Lodging.WindyTower]
    Ceald = 3, "Cealdish Commoner", 6.58, 9.87, [Lodging.KingsDrab, Lodging.GoldenPony]
    Ruh = 4, "Edema Ruh", 3.4, 5.67, [Lodging.Ankers, Lodging.KingsDrab]

    def __new__(cls, value, name, initalFunds, stipend, lodging):
        member = object.__new__(cls)
        member._value_ = value
        member.fullname = name
        member.initalFunds = initalFunds
        member.stipend = stipend
        member.lodging = lodging
        return member

    def __int__(self):
        return self.value
    
    def __str__(self) -> str:
        return f"{self.fullname}"


class BaseStat(Enum):
    MUSIC = 1
    ESSAY = 2
    ART = 3


class Rank(Enum):
    NONE = 0
    ELIR = 1
    RELAR = 2
    ELTHE = 3
    MASTER = 4

class FieldName(IntEnum):
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

class ItemType(Enum):
    MOMMET = 1
    TENACULUM = 2
    FIRESTOP = 3
    PLUMBOB = 4
    BONETAR = 5
    WARD = 6
    BLOODLESS = 7
    THIEVESLAMP = 8
    GRAM = 9
    TALENTPIPES = 10
    NAHLROUT = 11
    BODYGUARD = 12

class Item:
    def __init__(self, name, type: ItemType, uses, defense, action, level, target= None) -> None:
        self.type: ItemType = type

        self.name: str = name
        self.uses: int = uses # Can be None
        self.defense: bool = defense
        self.action: bool = action
        self.level: int = level # Can be None
        self.target = target #None except when mommet

    @classmethod
    def Generate(cls, type: ItemType, level: int = 0, target = None):
        if type == ItemType.MOMMET:
            return Item("Mommet", type, 1, False, True, level, target)
        elif type == ItemType.TENACULUM:
            uses = 1
            if level == 4: uses = 2
            return Item("Tenaculum", type, uses, False, True, level)
        elif type == ItemType.FIRESTOP:
            uses = 1
            if level == 4: uses = 2
            return Item("Firestop", type, uses, True, False, level)
        elif type == ItemType.PLUMBOB:
            return Item("Plumbob", type, 1, False, True, level)
        elif type == ItemType.BONETAR:
            return Item("Bonetar", type, 1, False, True, level)
        elif (type == ItemType.WARD or type == ItemType.BLOODLESS 
              or type == ItemType.THIEVESLAMP or type == ItemType.GRAM):
            if level == 2: uses = random.randrange(1,2)
            elif level == 3: uses = 2
            elif level == 4: uses = 3
            else: uses = 1
            if type == ItemType.WARD:
                return Item("Ward", type, uses,True,True,level)
            elif type ==  ItemType.BLOODLESS:
                return Item("Bloodless", type, uses, True, False, level)
            elif type == ItemType.THIEVESLAMP:
                return Item("Thieve's Lamp", type, uses, False, True, level)
            else: # Gram
                return Item("Gram", type, uses, True, False, level) 
        elif type == ItemType.TALENTPIPES:
            return Item("Talent Pipes", type, None, False, False, None)
        elif type == ItemType.NAHLROUT:
            return Item("Nahlrout", type, 1, True, True, None)
        elif type == ItemType.BODYGUARD:
            return Item("Bodyguard", type, 2,True,False,None)

class ActionType(Enum):
    Complaint = 1
    GainEP = 2
    MysteriousBulletins = 3
    BribeTheMessenger = 4
    LinguisticAnalysis = 5
    Pickpocket = 6
    LawOfContraposition = 7
    ProficientInHyperbole = 8
    ArgumentumAdNauseam = 9
    PersuaisveArguments = 10
    FaeLore = 11
    OmenRecognition = 12
    SchoolRecords = 13
    BannedBooks = 14
    MommetMaking = 15
    MalfeasanceProtection = 16
    MedicaEmergency = 17
    MedicaDetainment = 18
    PsychologicalCounselling = 19
    CheatingDeath = 20
    CreateTenaculum = 21
    CreateFirestop = 22
    CreatePlumbob = 23
    CreateBonetar = 24
    CreateWard = 25
    CreateBloodless = 26
    CreateThievesLamp = 27
    CreateGram = 28
    UseName = 29
    UseMommet = 30
    UseTenaculumItem = 31
    UseTenaculumAction = 32
    UseFirestop = 33
    UsePlumbob = 34
    UseBonetar = 35
    UseWard = 36
    UseThievesLamp = 37
    UseNahlrout = 38
    UseCourier = 39
    UseAssassin = 40

class Action:
    def __init__(self, name: str, player, type: ActionType, target,
                  target_two = None, action_type: str = None):
        self.name: str = name # Action name
        self.player = player # Player taking the action
        self.type: ActionType = type # Type of action: Block, Redirect, Kill, etc.
        self.target_action_type: str = action_type
        self.target = target
        self.target_two = target_two

        self.blocked: bool = False
        self.redirected: bool = False
        self.redirect_target = None

        self.message: str = None

        # Working variables to process cycles and chains
        self.blocked_by = []
        self.blocked_by_action: list[Action] = []
        self.in_block_cycle: bool = False

    def perform(self):
        if self.blocked:
            Log.Action(self, LogOutcome.Blocked)
            return
        player_level = int(self.player.status.rank)
        action_logged = False
        # Item Creation Actions
        # Artificery
        if self.type == ActionType.CreateWard:
            item = Item.Generate(ItemType.WARD,player_level)
            self.player.add_item(item)
        elif self.type == ActionType.CreateBloodless:
            item = Item.Generate(ItemType.BLOODLESS,player_level)
            self.player.add_item(item)
        elif self.type == ActionType.CreateThievesLamp:
            item = Item.Generate(ItemType.THIEVESLAMP,player_level)
            self.player.add_item(item)
        elif self.type == ActionType.CreateGram:
            item = Item.Generate(ItemType.GRAM,player_level)
            self.player.add_item(item)
        # Alchemy
        elif self.type == ActionType.CreateTenaculum:
            item = Item.Generate(ItemType.TENACULUM,player_level)
            self.player.add_item(item)
        elif self.type == ActionType.CreateFirestop:
            item = Item.Generate(ItemType.FIRESTOP,player_level)
            self.player.add_item(item)
        elif self.type == ActionType.CreatePlumbob:
            item = Item.Generate(ItemType.PLUMBOB,player_level)
            self.player.add_item(item)
        elif self.type == ActionType.CreateBonetar:
            item = Item.Generate(ItemType.BONETAR,player_level)
            self.player.add_item(item)

        # Mommet making may need aditional types, to distinguish level 1, 2, 3, 4
        # Needs access to player list for level 1.
        elif self.type == ActionType.MommetMaking: 
            item = Item.Generate(ItemType.MOMMET,player_level, self.target)
            self.player.add_item(item)

        # Linguistics
        elif self.type == ActionType.MysteriousBulletins:
            # Appened string to WriteUp details.
            pass
        elif self.type == ActionType.BribeTheMessenger:
            Log.NotifyGM(f"{self.player.info.name} spies on {self.target}'s PMs.")
            action_logged = True
        elif self.type == ActionType.LinguisticAnalysis:
            Log.NotifyGM() 

        # Arithmetics
        elif self.type == ActionType.Pickpocket:
            if self.player.status.master_of is not FieldName.ARITHMETICS:
                #random Target
                pass
            if self.target.holds_item(ItemType.BODYGUARD):
                Log.Action(self, LogOutcome.Failure)
                action_logged = True
            else:
                money = self.target.status.money
                proportion = 0.1
                if player_level == Rank.RELAR:
                    proportion = 0.2
                elif player_level == Rank.ELTHE:
                    proportion = 0.3
                self.player.increase_money(money*proportion)
                self.target.reduce_money(money*proportion)
        
        # Rhetoric & Logic
        elif self.type == ActionType.LawOfContraposition:
            pass
        elif self.type == ActionType.ProficientInHyperbole:
            if self.target is not None:
                self.player.status.complaints.append(self.target)
            if self.target_two is not None:
                self.player.status.complaints.append(self.target_two)
        elif self.type == ActionType.ArgumentumAdNauseam:
            for complaint in self.target.status.complaints:
                if complaint.target == self.target_two:
                    complaint.blocked = True
                    return
        elif self.type == ActionType.PersuaisveArguments:
            # Do I need 3 targets here?
            pass

        # Archives
        elif self.type == ActionType.FaeLore:
            if self.target.info.is_evil:
                self.target.status.blocked = True
        elif self.type == ActionType.OmenRecognition:
            Log.NotifyGM()
        elif self.type == ActionType.SchoolRecords:
            out = ""
            if self.player.status.is_enrolled:
                count = len(self.target.status.elevations)
                if count >= 1:
                    out += "."
                # Log this
                # Output to Player PM
        elif self.type == ActionType.BannedBooks:
            pass
        
        # Sympathy
        elif self.type == ActionType.MommetMaking:
            pass
        elif self.type == ActionType.MalfeasanceProtection:
            pass

        # Physicking
        elif self.type == ActionType.MedicaEmergency:
            pass
        elif self.type == ActionType.MedicaDetainment:
            pass
        elif self.type == ActionType.PsychologicalCounselling:
            self.target.status.IP -= int(player_level)
            Log.Action()
        elif self.type == ActionType.CheatingDeath:
            pass

        # Naming
        elif self.type == ActionType.UseName:
            # Tell the GMs what names to use.
            Log.NotifyGM()

        
        # Item Usage
        elif self.type == ActionType.UseTenaculumAction:
            pass
        elif self.type == ActionType.UseTenaculumItem:
            pass
        elif self.type == ActionType.UseFirestop:
            pass
        elif self.type == ActionType.UsePlumbob:
            pass
        elif self.type == ActionType.UseBonetar:
            pass

        elif self.type == ActionType.UseWard:
            pass
        elif self.type == ActionType.UseThievesLamp:
            pass

        elif self.type == ActionType.UseMommet:
            pass
        
        elif self.type == ActionType.UseNahlrout:
            pass

        # Other Actions
        # UseAssassin
        # UseCourier
        # GainEP

        # Complaint
        elif self.type == ActionType.Complaint:
            if self.target is not None:
                self.player.status.complaints.append(self.target)
            if self.target_two is not None:
                self.player.status.complaints.append(self.target_two)

        if not action_logged:
            Log.Action(self)
        



    
    def __str__(self) -> str:
        return f"{self.player.info.name}: {self.name} "
    
    def clear_blocked_by(self):
        self.blocked_by = []
        self.blocked_by_action: list[Action] = []
        # clear the blocked_by flag on players?

    def set_blocked_by(self):
        if not self.blocked:    
            if self.type.find("Block") < 0:
                # print("Not a block action.")
                return
            
            # Dunno if we just set the player flag, set the player and
            #  all action flags, or just the action flags.
            if self.type == "Block All":
                self.target.status.blocked_by.append(self.player)
                # print(f"{self.player} blocks all {self.target}'s actions")
                for a in self.target.choice.actions:
                    a.blocked_by.append(self.player)
                    a.blocked_by_action.append(a)
                    # print(f"-- {a.name} blocked.")

            elif self.type == "Block One":
                for a in self.target.choice.actions:
                    if a.type.find(self.target_action_type) >= 0:
                        a.blocked_by.append(self.player)
                        a.blocked_by_action.append(a)
                        # print(f"{self.player} blocked {self.target}'s {a.type} action.")
                        return
                # print("No relevant actions found.")






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
        field: FieldName,
        name: str,
        ability1: Ability,
        ability2: Ability,
        ability3: Ability,
        ability4: Ability,
        level1_AP = None,
        level2_AP = None,
        level3_AP = None,
        master_AP = None
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
    "Hand Delivery", FieldName.LINGUISTICS, Rank.ELIR, True, False, False, False, False
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
    None,
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
    None,
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