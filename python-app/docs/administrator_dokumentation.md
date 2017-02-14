---
title: Administrator Dokumentation
author: Siegfried Schwengler
version: 1.0
---

Status: Final

# Benutzer Anleitung Administrator


## Funktionen

### Messwerte und Vergleich

  - Login
  - Wasserwerte Importe
  - Messwerte Anzeigen
  - Orte Anzeigen 
  - Mineralwasser
  - Durchschnittswerte
  - Tägliche Dosis
  
### Administration

  - User Anzeigen
  - User Verwalten
  - Administratoren Verwaltung

##### Login

Mit den default Credentials hier einloggen: 
<: server_name :>/login/admin/

Benutzername:      "**admin**"
Passwort:           "**AdminWasser**"


##### Wasserwerte Importe
Hier ist zu sehen, wie die Syntax für Orte und für Wasserwerte aussieht, die die CSV Dateien haben müssen.
Zuerst muss eine Region angegeben werden, für welche man die Orte/Wasserwerte Importieren möchte.
Darunter gibt es die Option "Choose File" vom Lokalen Rechner.
Nach der Auswahl der gewünschten Jsons, muss rechts auf den Button "Hochladen und Importieren" geklickt werden um den Prozess abzuschließen.



##### Messwerte Anzeigen
Hier ist eine Übersicht der Wasserwerte zu sehen, die in der Datenbank existieren.

##### Orte Anzeigen
Hier eine Übersicht der Orte zu sehen, die in der Datenbank existieren.

##### Mineralwasser
Hier ist eine Übersicht der Mineralwasser zu sehen, die in der Datenbank existieren.
Dieses Wasser sind editierbar mit einem Klick rechts auf den "Edit" Button.

##### Durchschnittswerte
Hier sind die aktuellen Durchschnittswerte für ganz Deutschland zu entnehmen. Diese sind mit einem klicken auf den Button "Wasser Mittelwerte" ganz rechts editierbar. 

##### Tägliche Dosis
Hier ist die tägliche Dosis zu sehen, die empfohlen wird, täglich zu sich zu nehmen.



### Administration

##### User Anzeigen
Hier sind die registrierten Privat User und die registrierten Behördenmitarbeiter zu sehen.
Um einen der User zu löschen, wird ein Klick auf das rote "X" neben des zu löschenden Users benötigt.

##### User Verwalten
Hier ist es möglich Behördenmitarbeiter via CSV Datei zu importieren. Die Syntax ist dabei zu beachten.
Hat man eine CSV Datei mit den gewünschten Kontakten in der richtigen Syntax, wird ein Klick
auf "Choose File" benötigt, um die CSV Datei von seinem lokalen Rechner auszusuchen und rechts mit "Hochladen und Importieren" werden diese Kontakte aus der CSV Datei importiert.

##### Behördenmitarbeiter Verifizieren

Mit dem Klick hier auf "Behördenmitarbeiter verifizieren"
Öffnet sich eine neue Seite, auf der zu sehen ist, welche Behördenmitarbeiter auf eine Verifizierung warten um sich einloggen zu können.

##### Token versenden

Token an alle Gemeinden senden: 
Mit dem Klick auf "Emails senden" werden an alle Behördenmitarbeiter, in der Datenbank gespeicherten Kontakte, ein Token verschickt, der benutzt werden soll um sich auf dem Trinkwasser Tool einzuloggen.

Token an eine oder mehrere Gemeinden senden:
Mit dem Klick auf "Behördenübersicht", öffnet sich eine neue Seite mit allen Behörden Mitarbeiter Kontakten in der Datenbank. Per Checkbox ist es möglich die Kontakte auszusuchen, die einen Token per E-Mail erhalten sollen.

##### Administratoren Verwaltung

Hier sind in aktuellen Administratoren in der oberen Tabelle zu sehen.
Gelöscht werden können diese mit betätigen des roten "X" hinter dem gewünschten Administrator.

Darunter hat der Administrator die Option weitere Administratoren anzulegen.










