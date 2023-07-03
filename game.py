from test import Test
from player import Player
from block import Block
from horns import Horns
    
all_players: list[Player] = Test().start_test(1)

Block().run_blocks(all_players)
Horns().run_complaints(all_players)
Horns().run_horns(all_players)
# RunStandardActions()
# RunImre()
# RunAttacks()
# RunInsanity()
# RunElevations()
# RunEP()

# if(month == 3):
#     RunStipend()
#     RunAdmission()
#     RunLodging()



