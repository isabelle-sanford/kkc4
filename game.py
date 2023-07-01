from test import Test
from player import Player
from block import Block
from complaints import Complaints
from horns import Horns
    
allPlayers: list[Player] = Test().StartTest(1)

Block().RunBlocks()
Complaints().RunComplaints(allPlayers)
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



