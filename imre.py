import random
from player import Player, Item

class Imre:
    def  __init__(self, playerList: list[Player]) -> None:
        self.PlayerList = playerList
        pass

    def Eolian(self):
        for p in self.PlayerList:
            # Practice
            if p.choice.IMRE_EOLIAN_Practice:
                p.status.musical_stat += 0.5
            # Perform
            elif p.choice.IMRE_EOLIAN_Audition and not p.status.IMRE_EOLIAN_Auditioned:
                p.status.IMRE_EOLIAN_Auditioned = True
                result = random.randrange(1,20) + p.status.musical_stat
                if result >= 15:
                    p.status.inventory.append(Item("Talent Pipes"))

    def Moneylenders(self):

        pass

    def LoadedDice(self):
        WinningRatios: list[int] = [0, 20, 15, 10, 5, 2]

        for p in self.PlayerList:
            if p.choice.IMRE_LOADEDDICE_PlacedBet:
                dif = p.status.money - p.choice.IMRE_LOADEDDICE_BetAmount
                if dif > 0:
                    p.status.money -= p.choice.IMRE_LOADEDDICE_BetAmount
                else:
                    return # You're broke and bet money you didn't have.
                won = False
                result = random.randrange(1,20)
                for i in p.choice.IMRE_LOADEDDICE_Numbers:
                    if i == result:
                        won = True
                if won:
                    p.status.money += p.choice.IMRE_LOADEDDICE_BetAmount * WinningRatios[len(p.choice.IMRE_LOADEDDICE_Numbers)]

    def Apocathery(self):
        pass

    def BlackMarket(self):
        pass


