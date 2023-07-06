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
        # Imre Tests
        elif i == 8: #Eolian 
            p1 = spawner.Generate("A")
            p2 = spawner.Generate("B")
            p3 = spawner.Generate("C")
            p4 = spawner.Generate("D")
            p5 = spawner.Generate("E")
            p6 = spawner.Generate("F")
            p7 = spawner.Generate("G")
            p8 = spawner.Generate("H")
            
            p1.status.in_Imre = True
            p1.choice.IMRE_EOLIAN_practice = True


            p2.status.in_Imre = True
            p2.choice.IMRE_EOLIAN_audition = True
            p2.choice.IMRE_EOLIAN_practice = True

            p3.status.in_Imre = True
            p3.status.musical_stat = 15
            p3.choice.IMRE_EOLIAN_audition = True

            p4.status.in_Imre = True
            p4.status.musical_stat = -10
            p4.choice.IMRE_EOLIAN_audition = True

            p5.choice.IMRE_EOLIAN_audition = True

            p6.status.in_Imre = True
            p6.status.IMRE_EOLIAN_auditioned = True
            p6.choice.IMRE_EOLIAN_audition = True

            p7.status.in_Imre = True
            p7.status.IMRE_EOLIAN_auditioned = True
            p7.choice.IMRE_EOLIAN_practice = True

            return [p1, p2, p3, p4, p5, p6, p7, p8]

        elif i == 9: #Apocathery
            p1 = spawner.Generate("A")
            p2 = spawner.Generate("B")
            p3 = spawner.Generate("C")
            p4 = spawner.Generate("D")
            p5 = spawner.Generate("E")
            p6 = spawner.Generate("F")
            p7 = spawner.Generate("G")
            p8 = spawner.Generate("H")
            p1.status.in_Imre = True
            p2.status.in_Imre = True
            p3.status.in_Imre = True
            p4.status.in_Imre = True
            p5.status.in_Imre = True
            p6.status.in_Imre = True
            p7.status.in_Imre = True
            p8.status.in_Imre = True

            # Nahlrout supply: 12
            # Bloodless supply: 4
            # Gram supply: 1
            p1.choice.IMRE_APOTHECARY_gram = 1
            p1.status.money += 25

            p2.choice.IMRE_APOTHECARY_bloodless = 1
            p2.status.money += 10
            p3.choice.IMRE_APOTHECARY_bloodless = 2
            p3.status.money += 20
            p4.choice.IMRE_APOTHECARY_bloodless = 1
            p4.status.money = 4
            p5.choice.IMRE_APOTHECARY_bloodless = 2
            p5.status.money = 15

            p6.choice.IMRE_APOTHECARY_nahlrout = 3
            p7.choice.IMRE_APOTHECARY_nahlrout = 1

            return [p1, p2, p3, p4, p5, p6, p7, p8]
        
        elif i == 10: # LoadedDice
            p1 = spawner.Generate("A")
            p2 = spawner.Generate("B")
            p3 = spawner.Generate("C")
            p4 = spawner.Generate("D")
            p5 = spawner.Generate("E")
            p6 = spawner.Generate("F")
            p7 = spawner.Generate("G")
            p8 = spawner.Generate("H")

            p1.status.in_Imre = True
            p2.status.in_Imre = True
            p3.status.in_Imre = True
            p4.status.in_Imre = True
            p5.status.in_Imre = True
            p6.status.in_Imre = True
            p7.status.in_Imre = True
            p8.status.in_Imre = True

            p1.choice.IMRE_LOADEDDICE_placed_bet = True
            p1.choice.IMRE_LOADEDDICE_bet_amount = 1
            p1.choice.IMRE_LOADEDDICE_numbers = [13, 7]
            p1.status.money = 1
            
            p2.choice.IMRE_LOADEDDICE_placed_bet = True
            p2.choice.IMRE_LOADEDDICE_bet_amount = 4
            p2.choice.IMRE_LOADEDDICE_numbers = [2, 3, 1]
            p2.status.money = 6

            p3.choice.IMRE_LOADEDDICE_placed_bet = True
            p3.choice.IMRE_LOADEDDICE_bet_amount = 0.5
            p3.choice.IMRE_LOADEDDICE_numbers = [1]
            p3.status.money = 0.1

            return [p1, p2, p3, p4, p5, p6, p7, p8]

        else:
            print("Not a valid test!")