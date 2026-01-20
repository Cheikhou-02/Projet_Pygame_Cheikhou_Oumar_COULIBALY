dd = int(input("Veiller saisir le jours:"))
mm = int(input("Veiller saisir le mois correspondant : "))
annee = (input("Veiller saisir l'annee correspondant: "))
c = int(annee [0:2])
y = int(annee [2:4])
w = (dd + (13 * (mm + 1)//5) + y + (y//4) + (c//4) - 2*c) % 7

print(w)
match w :
    case 0:
        print("Samedi")
    case 1:
        print("Dimanche")
    case 2:
        print("Lundi")
    case 3:
        print("Mardi")
    case 4:
        print("Mercredi")
    case 5:
        print("Jeudi")
    case 6:
        print("Vendredi")
        

