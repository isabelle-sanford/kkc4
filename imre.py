


# The Eolian
from dataclasses import dataclass
import random


class Apothecary:

    def __init__(self):
        self.num_nahlrout = 5
        self.num_grams = 5
        self.num_bloodless = 5
        # couriers is infinite
    
    def restock(self):
        self.num_nahlrout = 5
        self.num_grams = 5
        self.num_bloodless = 5
    
    def take_orders(self, orders):
        # orders = {nahlrout: pids, grams: pids, etc}

        if len(orders["nahlrout"]) > self.num_nahlrout:
            too_many = len(orders["nahlrout"]) - self.num_nahlrout
            for i in range(too_many):
                to_remove = random.choice(orders["nahlrout"])
                orders["nahlrout"].remove(to_remove)
        
        if len(orders["bloodless"]) > self.num_bloodless:
            too_many = len(orders["bloodless"]) - self.num_bloodless
            for i in range(too_many):
                to_remove = random.choice(orders["bloodless"])
                orders["bloodless"].remove(to_remove)

        if len(orders["grams"]) > self.num_grams:
            too_many = len(orders["grams"]) - self.num_grams
            for i in range(too_many):
                to_remove = random.choice(orders["grams"])
                orders["grams"].remove(to_remove)
        
        return orders # I guess??
        
        


# The Loaded Dice


# Devi

# Giles


# Apothecary



# Black Market


@dataclass
class Contract:
    id: int
    name: str
    placer: int # pid
    contract_text: str 
    prize_str: str
    turn_placed: int
    prize_int: int = None # if it's actually money
    current_taker: int = -1
    prev_takers: list[int] = []
    # anything else?

    # funcs for taking, completing? 


class BlackMarket:

    def __init__(self):
        # todo actual numbers here
        self.num_assassins = 30 # todo
        self.assassin_price = 30 
        self.num_bodyguards = 20 
        self.bodyguard_price = 100
        self.contracts: list[Contract] = []

    def restock(self):
        self.num_assassins += 1 # idk
        # TODO
    
    def take_orders(self, orders): 
        # TODO
        pass

    # I mean that's not really necessary is it
    def add_contract(self, contract: Contract):
        self.contracts.append(contract)

    # other stuff?




