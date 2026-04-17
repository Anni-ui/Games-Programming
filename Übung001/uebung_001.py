#Variablen deklariert
Ergebnis = 437
Ende = 32483
Wert1 = 3.1
Wert2 = 5.4

total = sum(range(Ergebnis, Ende))
print(total)

#for Schleife für die Zahlen von 437 bis 32483
for Ergebnis in range(Ende):
    Ergebnis = Ergebnis + Ergebnis + 1

print(Ergebnis)

if Wert1 > Wert2: 
   result = Wert2 / Wert1 
   print(result)
elif Wert1 < Wert2:
    result = Wert1 / Wert2
    print(result)   
else :
    result = 1
    print(result)

    