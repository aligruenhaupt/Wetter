## Wetter Application using the API of the DWD "Deutscher Wetterdienst Offenbach am Main"

>Die Idee hinter dieser Anwendung ist, zu lernen und meine Fähigkeiten zu zeigen. Sie soll eine Datenpipeline von
den rohen Daten des deutschen Wetterdienstes bilden und die Daten in eine für den Nutzer einfach zu verstehende Form bringen.
>
>Das Ganze ist ja auch logisch. Keiner braucht eine weitere Wetteranwendung. Vor allem nicht auf dem Desktop. 


Die Anwendung soll alle aktiven Wetterstationen auflisten. 
Der Nutzer sucht sich eine Station aus und dann werden ihm 
die Daten angezeigt, die er will. 

Aktuell stelle ich mir folgende Funktionen vor:
- Die Temperatur für die nächsten Tage in 3h Abschnitten
- Regenwahrscheinlichkeit (optional)
- Wetterzustand

TODO:
Alle Stationen reinnehmen und dann alle Stationen 
deren Ende Datum vor aktuellerMonat/aktuellesJahr ist 
entfernen

--> es sind 1365 Lines aber nur um die 570 sind aktiv.

vielleicht auch fürs erste, dass man seine stadt anfangsbuchstabe angibt und so viele städte angezeigt werden.