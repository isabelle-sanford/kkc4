from player import Player, PlayerRandom, FieldName

class Test:
    def __init__(self) -> None:
        pass

    def StartTest(self, i: int) -> list[Player]:
        spawner = PlayerRandom()

        # Complaint/DP Test
        if i == 1: 
                p1 = spawner.Generate("A")
                p2 = spawner.Generate("B")
                p3 = spawner.Generate("C")
                p4 = spawner.Generate("D")
                p5 = spawner.Generate("E")
                p6 = spawner.Generate("F")
                p7 = spawner.Generate("G")
                p8 = spawner.Generate("H")

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
                p8.status.MasterOf = FieldName.LINGUISTICS
                p7.status.MasterOf = FieldName.NAMING

                p4.assignEP(FieldName.ALCHEMY,3)
                p4.assignEP(FieldName.NAMING,2) 

                return [p1, p2, p3, p4, p5, p6, p7, p8]
        
        # Block Tests
        elif i == 2:
            p1 = spawner.Generate("A")
            p2 = spawner.Generate("B")
            p3 = spawner.Generate("C")
            p4 = spawner.Generate("D")

            p1.BlockOne(p2,"Block")
            p2.BlockAll(p3)
            p3.BlockOne(p1, "Block")
            p3.BlockOne(p4, "Block")
            p4.RedirectAction(p1,p1,"Redirect")

            return [p1, p2, p3, p4]
        
        elif i == 3:
            p1 = spawner.Generate("A")
            p2 = spawner.Generate("B")
            p3 = spawner.Generate("C")
            p4 = spawner.Generate("D")

            p1.BlockOne(p2,"Block")
            p2.BlockAll(p3)
            p3.BlockOne(p1, "Block")
            p4.BlockOne(p1, "Block")

            return [p1, p2, p3, p4]
        
        elif i == 4:
            p1 = spawner.Generate("A")
            p2 = spawner.Generate("B")
            p3 = spawner.Generate("C")
            p4 = spawner.Generate("D")

            p1.BlockOne(p2,"Block")
            p2.BlockAll(p3)
            p3.BlockOne(p1, "Block")
            p3.BlockOne(p4, "Block")
            p4.BlockAll(p1)

            return [p1, p2, p3, p4]
        
        elif i == 5:
            p1 = spawner.Generate("A")
            p2 = spawner.Generate("B")
            p3 = spawner.Generate("C")
            p4 = spawner.Generate("D")
            p5 = spawner.Generate("E")
            p6 = spawner.Generate("F")
            p7 = spawner.Generate("G")
            p8 = spawner.Generate("H")

            p1.BlockOne(p2,"Block")
            p1.BlockAll(p5)
            p2.BlockAll(p3)
            p3.BlockOne(p4, "Block")
            p4.BlockAll(p5)
            p4.BlockAll(p2)
            p5.BlockOne(p1, "Block")
            p6.BlockOne(p7, "Block")
            p7.BlockOne(p3, "Block")
            p7.BlockAll(p1)

            return [p1, p2, p3, p4, p5, p6, p7, p8]
        
        elif i == 6:
            p1 = spawner.Generate("A")
            p2 = spawner.Generate("B")
            p3 = spawner.Generate("C")
            p4 = spawner.Generate("D")
            p5 = spawner.Generate("E")
            p6 = spawner.Generate("F")
            p7 = spawner.Generate("G")
            p8 = spawner.Generate("H")

            p1.BlockOne(p2,"Block")
            p1.BlockAll(p5)
            p2.BlockAll(p3)
            p3.BlockOne(p4, "Block")
            p4.BlockAll(p5)
            p4.BlockAll(p2)
            p5.BlockOne(p1, "Block")
            p6.BlockOne(p7, "Block")
            p7.BlockOne(p3, "Block")
            p7.BlockAll(p1)
            p8.BlockOne(p6, "Block")

            return [p1, p2, p3, p4, p5, p6, p7, p8]
        
        elif i == 7:
            p1 = spawner.Generate("A")
            p2 = spawner.Generate("B")
            p3 = spawner.Generate("C")
            p4 = spawner.Generate("D")
            p5 = spawner.Generate("E")
            p6 = spawner.Generate("F")
            p7 = spawner.Generate("G")
            p8 = spawner.Generate("H")

            p1.BlockOne(p2,"Block")
            p1.BlockAll(p3)
            p2.BlockAll(p3)
            p3.BlockOne(p1, "Block")
            p3.BlockOne(p4, "Block")
            p4.BlockAll(p1)
            p5.BlockOne(p2, "Block")
            p6.BlockOne(p7, "Block")
            p7.BlockAll(p8)

            return [p1, p2, p3, p4, p5, p6, p7, p8]
        
        else:
            print("Not a valid test!")