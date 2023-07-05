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
# RunInsanity()
# RunElevations()
# RunEP()

# if(month == 3):
#     RunStipend()
#     RunAdmission()
#     RunLodging()



