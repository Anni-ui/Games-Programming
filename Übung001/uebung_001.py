#Variablen deklariert
Summe = 0
#Variable Ende ist 1 mehr als die letzte Zahl die wir brauchen, da diese vom Code nicht mitgezählt wird.
Ende = 32483
Wert1 = 3.1
Wert2 = 5.4

#for Schleife, die alle Zahlen von 437 bis 32482 zusammen rechnet.
for i in range(437, Ende):
    Summe = Summe + i
#print gibt die Summe der Zahlen von 437 bis 32482 in der Konsole aus. 
print(Summe)    

# if fragt ab, ob der erste Wert größer ist als der zweite. 
if Wert1 > Wert2: 
  # falls das im mit if abgefragte zutrifft wird der zweite Wert durch den ersten geteilt.
   result = Wert2 / Wert1 
   #print gibt das Ergebnis der Variable result in der Konsole aus.
   print(result)
#elif wird aktiviert, falls das if nicht zutrifft (if = false). Elif fragt ab, ob der erste Wert kleiner ist als der zweite.
elif Wert1 < Wert2:
    #falls das im elif abgefragte zutrifft wird der erste Wert durch den zweiten geteilt.
    result = Wert1 / Wert2
    #print gibt das Ergebnis der Variable result in der Konsole aus.
    print(result)   
#else wird aktiviert falls das if und das elif nicht zutreffen (beide false sind). 
else :
    #dann wird die Variable result auf 1 gesetzt.
    result = 1
    #print gibt das Ergebnis der Variable result in der Konsole aus.
    print(result)

    