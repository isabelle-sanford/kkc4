from player import Player, FieldName

class Test:
    def __init__(self) -> None:
        pass

    def StartTest(self, i: int) -> list[Player]:
        if i == 1:
                p1 = Player("A")
                p2 = Player("B")
                p3 = Player("C")
                p4 = Player("D")
                p5 = Player("E")
                p6 = Player("F")
                p7 = Player("G")
                p8 = Player("H")

                p1.ImportComplaint(p2)
                p1.ImportComplaint(p2)
                p2.ImportComplaint(p1)
                p2.ImportComplaint(p4)
                p3.ImportComplaint(p4)
                p5.ImportComplaint(p6)
                p6.ImportComplaint(p4)
                p6.ImportComplaint(p4)
                p6.ImportComplaint(p4)
                p6.ImportComplaint(p4)
                p7.ImportComplaint(p4)
                p7.ImportComplaint(p4)
                p8.ImportComplaint(p4)
                p8.ImportComplaint(p4)
                p8.MasterOf = FieldName.LINGUISTICS
                p7.MasterOf = FieldName.NAMING

                p4.assignEP(FieldName.ALCHEMY,3)
                p4.assignEP(FieldName.NAMING,2) 

                return [p1, p2, p3, p4, p5, p6, p7, p8]


class Complaints:
    def __init__(self) -> None:
        pass

    def RunComplaints(self, playerList: list[Player] = None):
        allPlayers: list[Player] = Test().StartTest(1)
        if playerList is not None:
             allPlayers = playerList

        for p in allPlayers:
            for c in p.complaints:
                # Notify all players of complaints received.
                c.complaintsReceived.append(p)

        for p in allPlayers:
            if len(p.complaints) > 0:
                out = f"{p.name} ({len(p.complaints)}): "
                for c in p.complaints:
                    out += f"{c.name}, "
                out = out[:-2]
                print(out)
                

        # What do complaints do? Horns already takes the votes placed and notifies all players of who voted on them, which can be used in the tuition step. Extra votes should have been pulled from db. Blocks needs to run at some point to ensure blocks are removed. 
        # Possibly this class generates the vote counts?
        # Could move the notification of votes to this class. This class would need to happen after blocks though.
             
