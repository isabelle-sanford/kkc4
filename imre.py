import random
from player import Player, Item, ItemType

class Imre:
    player_list = []
    def  __init__(self) -> None:
        pass

    def Eolian(self):
        print(f"\nEolian started...")
        
        for p in Imre.player_list:
            # Practice
            # Is there a limit on this, or can you practice for ever?
            if p.choice.IMRE_EOLIAN_practice:
                str = p.status.musical_stat
                p.status.musical_stat += 0.5
                print(f"{p.info.name} practiced. [{str} became {p.status.musical_stat}]")
            # Perform
            elif (p.choice.IMRE_EOLIAN_audition 
                    and not p.status.IMRE_EOLIAN_auditioned):
                
                p.status.IMRE_EOLIAN_auditioned = True
                result = random.randrange(1,20) + p.status.musical_stat
                print(f"{p.info.name} auditioned. [Result: {result-p.status.musical_stat}+{p.status.musical_stat}={result}]")
                if result >= 15:
                    p.status.inventory.append(Item.Generate(ItemType.TALENTPIPES))
                    print(f"{p.info.name} got their talent pipes!")
                

    def Moneylenders(self):
        print(f"\nMoney Lenders started...")
        pass

    # Doesn't enforce bet limits yet.
    def LoadedDice(self):
        # While this shouldn't be called if there's no bets placed
        # more convenient to have index 1 be for betting on 1 number
        # therefore including the odds of winning when betting no numbers
        WinningRatios: list[int] = [0, 20, 15, 10, 5, 2]
        print(f"\nLoaded Dice started...")
        print(Imre.player_list)
        print(len(Imre.player_list))

        for p in Imre.player_list:
            print(f"{p.info.name}: Placed Bet = {p.choice.IMRE_LOADEDDICE_placed_bet}")
            if p.choice.IMRE_LOADEDDICE_placed_bet:
                dif = p.status.money - p.choice.IMRE_LOADEDDICE_bet_amount
                if dif > 0:
                    p.status.money -= p.choice.IMRE_LOADEDDICE_bet_amount
                else:
                    pass # You're broke and bet money you didn't have.
                won = False
                result = random.randrange(1,20)
                for i in p.choice.IMRE_LOADEDDICE_numbers:
                    if i == result:
                        won = True
                winnings = 0
                if won:
                    winnings = (p.choice.IMRE_LOADEDDICE_bet_amount 
                                       * WinningRatios[len(p.choice.IMRE_LOADEDDICE_numbers)])
                    p.status.money += winnings
                print(f"{p.info.name} bet {p.choice.IMRE_LOADEDDICE_bet_amount} on {str(p.choice.IMRE_LOADEDDICE_numbers)[1:-1]} and rolled a {result} (Winnings = {winnings})")
    

    # Doesn't consistently check for if people have the money for things. 
    def Apocathery(self):
        print(f"\nApocathery started...")
        def ApocatheryRunProcess(item: dict, buyers: list[Player], 
                                 units_requested: list[Player]):
            # If there are enough for all purchase request, just hand them out.
            if len(units_requested) < item["supply"]:
                print(f"{item['type']}: supply > demand")
                for p in units_requested:
                    if p.status.money > item["cost"]:
                        p.status.money -= item["cost"]
                        item["supply"] -= 1
                        p.status.inventory.append(Item.Generate(item["type"]))
                        print(f"{p.info.name} purchased {item['type']} ({p.status.money} talents left)")
                    else:
                        print(f"{p.info.name} has run out of money...")
            else: 
                # Otherwise, if all buyers can get at least one unit, hand out one each.
                # ITEM_units_requested lists the total number of item requests, 
                # ITEM_buyers lists the players who are in the buying pool.
                print(f"{item['type']}: demand < supply")
                while len(buyers) < item["supply"]:
                    for p in buyers:
                        if p.status.money > item["cost"]:
                            p.status.money -= item["cost"]
                            item["supply"] -= 1
                            p.status.inventory.append(Item.Generate(item["type"]))
                            units_requested.remove(p)
                            print(f"{p.info.name} purchased {item['type']} ({p.status.money} talents left)")
                        
                        # Once a players has received all they asked for or runs out of money
                        # remove them from the list of active buyers.
                        if (units_requested.count(p) == 0 
                            or p.status.money < item["cost"]):
                            buyers.pop(p)
                            print(f"{p.info.name} ({p.status.money} talents) removed from buyers.")
                
                # Check that everyone left asking can afford all their requests.
                for p in buyers:
                    if p.status.money  < item["cost"] * units_requested.count(p):
                        # Remove entries in list until only requesting the amount they can afford
                        pass
                
                # Hand out the remaining unites
                for p in range(item["supply"]):
                    result = random.randrange(0,len(buyers))
                    units_requested[result].status.inventory.append(Item.Generate(item["type"]))
                    units_requested[result].status.money -= item["cost"]
                    print(f"{units_requested[result].info.name} purchased {item['type']} ({units_requested[result].status.money} talents left)")
                    units_requested.pop(result)
                    

        nahlrout = {"type": ItemType.NAHLROUT, "cost": 1, "supply": 12}
        bloodless = {"type": ItemType.BLOODLESS, "cost": 10, "supply": 4}
        gram = {"type": ItemType.GRAM, "cost": 20, "supply": 1}

        nahlrout_buyers: list[Player] = []
        nahlrout_units_requested: list[Player] = []
        bloodless_buyers: list[Player] = []
        bloodless_units_requested: list[Player] = []
        gram_buyers: list[Player] = []
        gram_units_requested: list[Player] = []

        
        for p in Imre.player_list:
            if p.choice.IMRE_APOTHECARY_nahlrout > 0:
                nahlrout_buyers.append(p)
                for i in range(p.choice.IMRE_APOTHECARY_nahlrout):
                    nahlrout_units_requested.append(p)
            if p.choice.IMRE_APOTHECARY_bloodless > 0:
                bloodless_buyers.append(p)
                for i in range(p.choice.IMRE_APOTHECARY_bloodless):
                    bloodless_units_requested.append(p)
            if p.choice.IMRE_APOTHECARY_gram > 0:
                gram_buyers.append(p)
                for i in range(p.choice.IMRE_APOTHECARY_gram):
                    gram_units_requested.append(p)
        
        ApocatheryRunProcess(nahlrout, nahlrout_buyers, nahlrout_units_requested)
        ApocatheryRunProcess(bloodless, bloodless_buyers, bloodless_units_requested)
        ApocatheryRunProcess(gram, gram_buyers, gram_units_requested)
    

    def BlackMarket(self):
        print(f"\nBlack Market started...")
        pass

    def run_Imre(self,player_list: list[Player]):
        Imre.player_list = player_list
        self.Apocathery()
        self.Eolian()
        self.LoadedDice()
        self.BlackMarket()
        self.Moneylenders()