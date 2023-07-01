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