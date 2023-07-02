from test import Test
from player import Player
from block import Block
from horns import Horns
    
allPlayers: list[Player] = Test().StartTest(8)

Block().RunBlocks(allPlayers)
Horns().RunComplaints(allPlayers)
Horns().RunHorns(allPlayers)
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



