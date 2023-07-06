from test import Test
from player import Player
from block import Block
from horns import Horns
from imre import Imre

all_players: list[Player] = Test().start_test(10)

Block().run_blocks(all_players)
Horns().run_complaints(all_players)
Horns().run_horns(all_players)
# RunStandardActions()
Imre().run_Imre(all_players)
# RunAttacks()
# # RunInsanity()
# for p in all_players:
#     result = random.randrange(1,10)
#     if result + p.status.IP > 12:
#         p.status.is_sane = False
# RunElevations()
# RunEP()

# if(month == 3):
#     RunStipend()
#     RunAdmission()
#     RunLodging()

def run_standard_actions(player_list):
    player_list = player_list

    # Linguistics:
    # Mysterious Bulletins -> str output to GM messages. Something in the log?
    # Hand Delivery: Lookup in Bribe the Messenger
    # Bribe the Messenger: Flag the GMs via the log
    # Linguistic Analysis: Flag the GMs via the log

    # Arithmetics:
    # Reduced Interest: Lookup as part of Imre.MoneyLenders
    # Pickpocket:


    # Great Deals: Look up as part of Imre.Apocathery
    # Decreased Tuition: Look up as part of Tuition()


    # Rhetoric & Logic
    # Law of Contraposition: Happens as part of block.py, but also flag the GMs via the log
    # Proficient in Hyperbole: Looked up as part of Horns.
    # Argumentum Ad Nauseam: Part of Horns? Needs to happen prior to it anyway.
    # Persuasive Arguments: Part of Horns? Needs to happen prior to it anyway.

    # Archives:
    # Fae Lore: Part of block.
    # Omen Recognition: Flag the GMS via the log
    # School Records:


    # Banned Books:



    # Sympathy:
    # Mommet-making:


    # Malfeasance Protection?



    # Physicking:
    # Medica Emergency:


    # Medica Detainment: Part of Block
    # Psychological Counselling: Can happen now, or as a check in Insanity()
    # Cheating Death: Can happen now, or when kill/sabotage happens

    # Alchemy:
    # Tenaculum:
    

    # Firestop:


    # Plumbob:

    # Bone-tar


    # Artificery:
    # Ward:

    # Bloodless: 

    # Thieves Lamp: 

    # Gram: 

    # Naming
    # ??????

    # Item Actions: 
    # 

