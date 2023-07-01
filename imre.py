import random

class Item:
    def __init__(self) -> None:
        pass

class Apocathery:
    def __init__(self) -> None:
        self.nahlrout: int = 0
        self.couriers: list[str] = []
        self.bloodless: int = 0
        self.gram: int = 0

class Eolian:
    def __init__(self) -> None:
        self.pratice: bool = False
        self.takeExam: bool = False
        self.attemptedExam: bool = False

class Giles:
    def __init__(self) -> None:
        self.defaulted: bool = False
        self.amountOwed: float = 0.0

class Devi:
    def __init__(self) -> None:
        self.defaulted: bool = False
        self.collateral: list[Item] = []
        self.amountOwed: float = 0.0

class LoadedDice:
    WinningRatios: list[int] = [0, 20, 15, 10, 5, 2]
    def __init__(self) -> None:
        self.numbers: list[int] = []
        self.bet: float = 0.0

class BlackMarket:
    def __init__(self) -> None:
        self.mommets: list[Player] = [] # Dunno what this is yet.
        self.bodyguard: int  = 0 # Can you purchase multiple Bodyguards?
        self.assassin: list[Player] = []
        self.takeContracts: list[str] = []
        self.placeContracts: list[str] = []
        self.contractLog: list[Item] = []

class Player:
    def __init__(self) -> None:
        self.items: list[Item] = []
        self.money: float = 0.0
        self.eolianBaseStat: float = 0.0
        
        # Eolian
        self.eolian = Eolian()

        # Moneylenders
        self.giles = Giles()
        self.devi = Devi()

        # Loaded Dice
        self.loadedDice = LoadedDice()

        # Apocathery
        self.apocathery = Apocathery()

        # Black Market
        self.blackMarket = BlackMarket()


class Imre:

    def  __init__(self, playerList: list[Player]) -> None:
        self.PlayerList = playerList
        pass

    def Eolian(self):
        for p in self.PlayerList:
            # Practice
            if p.eolian.pratice:
                p.eolianBaseStat += 0.5
            # Perform
            elif p.eolian.takeExam and not p.eolian.attemptedExam:
                p.eolian.attemptedExam = True
                result = random.randrange(1,20) + p.eolianBaseStat
                if result >= 15:
                    p.items.append(Item("Talent Pipes"))

    def Moneylenders(self):

        pass

    def LoadedDice(self):
        for p in self.PlayerList:
            if len(p.loadedDice.numbers) > 0:
                dif = p.money - p.loadedDice.bet
                if dif > 0:
                    p.money -= p.loadedDice.bet
                else:
                    return # You're broke and bet money you didn't have.
                won = False
                result = random.randrange(1,20)
                for i in p.loadedDice.numbers:
                    if i == result:
                        won = True
                if won:
                    p.money += p.loadedDice.bet * LoadedDice().WinningRatios[len(p.loadedDice.numbers)]

    def Apocathery(self):
        pass

    def BlackMarket(self):
        pass


