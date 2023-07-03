from player import Player, PlayerRandom, FieldName

class Test:
    def __init__(self) -> None:
        pass

    def start_test(self, i: int) -> list[Player]:
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

                p1.import_complaint(p2)
                p1.import_complaint(p2)
                p2.import_complaint(p1)
                p2.import_complaint(p4)
                p3.import_complaint(p4)
                p5.import_complaint(p6)
                p6.import_complaint(p4)
                p6.import_complaint(p4)
                p6.import_complaint(p4)
                p6.import_complaint(p4)
                p7.import_complaint(p4)
                p7.import_complaint(p4)
                p8.import_complaint(p4)
                p8.import_complaint(p4)
                p8.status.master_of = FieldName.LINGUISTICS
                p7.status.master_of = FieldName.NAMING

                p4.assign_EP(FieldName.ALCHEMY,3)
                p4.assign_EP(FieldName.NAMING,2) 

                return [p1, p2, p3, p4, p5, p6, p7, p8]
        
        # Block Tests
        elif i == 2:
            p1 = spawner.Generate("A")
            p2 = spawner.Generate("B")
            p3 = spawner.Generate("C")
            p4 = spawner.Generate("D")

            p1.block_one(p2,"Block")
            p2.block_all(p3)
            p3.block_one(p1, "Block")
            p3.block_one(p4, "Block")
            p4.redirect_action(p1,p1,"Redirect")

            return [p1, p2, p3, p4]
        
        elif i == 3:
            p1 = spawner.Generate("A")
            p2 = spawner.Generate("B")
            p3 = spawner.Generate("C")
            p4 = spawner.Generate("D")

            p1.block_one(p2,"Block")
            p2.block_all(p3)
            p3.block_one(p1, "Block")
            p4.block_one(p1, "Block")

            return [p1, p2, p3, p4]
        
        elif i == 4:
            p1 = spawner.Generate("A")
            p2 = spawner.Generate("B")
            p3 = spawner.Generate("C")
            p4 = spawner.Generate("D")

            p1.block_one(p2,"Block")
            p2.block_all(p3)
            p3.block_one(p1, "Block")
            p3.block_one(p4, "Block")
            p4.block_all(p1)

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

            p1.block_one(p2,"Block")
            p1.block_all(p5)
            p2.block_all(p3)
            p3.block_one(p4, "Block")
            p4.block_all(p5)
            p4.block_all(p2)
            p5.block_one(p1, "Block")
            p6.block_one(p7, "Block")
            p7.block_one(p3, "Block")
            p7.block_all(p1)

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

            p1.block_one(p2,"Block")
            p1.block_all(p5)
            p2.block_all(p3)
            p3.block_one(p4, "Block")
            p4.block_all(p5)
            p4.block_all(p2)
            p5.block_one(p1, "Block")
            p6.block_one(p7, "Block")
            p7.block_one(p3, "Block")
            p7.block_all(p1)
            p8.block_one(p6, "Block")

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

            p1.block_one(p2,"Block")
            p1.block_all(p3)
            p2.block_all(p3)
            p3.block_one(p1, "Block")
            p3.block_one(p4, "Block")
            p4.block_all(p1)
            p5.block_one(p2, "Block")
            p6.block_one(p7, "Block")
            p7.block_all(p8)

            return [p1, p2, p3, p4, p5, p6, p7, p8]
        
        else:
            print("Not a valid test!")