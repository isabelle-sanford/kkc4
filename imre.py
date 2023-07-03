import random
from player import Player, Item

class Imre:
    def  __init__(self, player_list: list[Player]) -> None:
        self.player_list = player_list
        pass

    def Eolian(self):
        for p in self.player_list:
            # Practice
            if p.choice.IMRE_EOLIAN_practice:
                p.status.musical_stat += 0.5
            # Perform
            elif (p.choice.IMRE_EOLIAN_audition 
                    and not p.status.IMRE_EOLIAN_auditioned):
                p.status.IMRE_EOLIAN_auditioned = True
                result = random.randrange(1,20) + p.status.musical_stat
                if result >= 15:
                    p.status.inventory.append(Item("Talent Pipes"))

    def Moneylenders(self):

        pass

    def LoadedDice(self):
        WinningRatios: list[int] = [0, 20, 15, 10, 5, 2]

        for p in self.player_list:
            if p.choice.IMRE_LOADEDDICE_placed_bet:
                dif = p.status.money - p.choice.IMRE_LOADEDDICE_bet_amount
                if dif > 0:
                    p.status.money -= p.choice.IMRE_LOADEDDICE_bet_amount
                else:
                    return # You're broke and bet money you didn't have.
                won = False
                result = random.randrange(1,20)
                for i in p.choice.IMRE_LOADEDDICE_numbers:
                    if i == result:
                        won = True
                if won:
                    p.status.money += p.choice.IMRE_LOADEDDICE_bet_amount * WinningRatios[len(p.choice.IMRE_LOADEDDICE_numbers)]

    def Apocathery(self):
        pass

    def BlackMarket(self):
        pass


