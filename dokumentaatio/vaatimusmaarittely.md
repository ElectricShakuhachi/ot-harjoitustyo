# Vaatimusmäärittely

## Sovelluksen tarkoitus

Sovelluksella voi luoda japanilaiselle shakuhachi -bambuhuilulle tarkoitettuja nuotteja, joissa käytetään perinteistä japanilaista nuotinnusta.

## Käyttöliittymäluonnos

Sovelluksesessa on yksi graafisen käyttöliittymän näkymä, jossa olevilla painikkeilla ja tekstikentillä tapahtuvat kaikki käyttäjän ja sovelluksen väliset interaktiot:

<img src="https://github.com/ElectricShakuhachi/ot-harjoitustyo/blob/master/dokumentaatio/kuvat/v-1.jpg" width="420">

## Perusversion tarjoama toiminnallisuus

- Käyttäjä voi nimetä kappaleen ja säveltäjän kirjoittamalla nämä tekstikenttiin, jotka ohjelma piirtää nuottipohjan yläreunoihin
    TEHTY

- Käyttäjä voi lisätä nuottisivuun nuottimerkkejä painamalla merkkejä vastaavia nappeja
    TEHTY

- Nuotit ilmestyvät oletusarvoisesti viimeisen nuotissa olevan nuotin jälkeen (eli alle japanilaisten nuottien mukaisesti)
    TEHTY

- Nuotit jatkuvat seuraavalle riville edellisen vasemmalle puolelle kun tila edelliseltä loppuu
    TEHTY

- Sivun täytyttyä ohjelma ilmoittaa sivun täyttymisestä, kehoittaa tallentamaan, eikä nuotteja voi enää lisätä
    TEHTY

- Käyttäjä voi kirjoittaa yksiäänisten kappaleiden lisäksi myös moniäänisiä kappaleita, kirjoitettavana olevan äänen voi vaihtaa napeista
    TEHTY

- Käyttäjä voi lisätä moniääniseen kappaleeseen ääniä maksimissaan 4 erityisellä napilla, jolla voi lisätä ääniä, äänien napit (Part1, Part2) jne ilmestyvät vasta äänen lisäyksen tapahduttua
    TEHTY

- Uutta ääntä luodessa ohjelma siirtää jo kirjoitettuja ääniä ja leventää pystyviivojen välejä siten, että äänien määrästä huolimatta ne on keskitetty tasaisesti pystyviivojen väliin
    TEHTY

- Käyttäjä voi tallentaa nuotin ohjelman käyttämään .shaku tiedostomuotoon (johon tieto tallentuu json-muotoisena)
    TEHTY

- Käyttäjä voi ladata nuotin ohjelman .shaku -tiedostosta muokattavaksi
    TEHTY

- Käyttäjä voi lisätä nuottiin myös taukoja

- Ladatessa tiedostoa ohjelma varoittaa, että kannattaa tallentaa, jos näkymällä on jo tehty muokkauksia nuottiin. Latauksen tekeminen tyhjentää vanhat tiedot nuotilta

- Käyttäjä voi eksportata nuotin tulostettavissa olevaksi tiedostoksi (pdf / png tms.)
    TEHTY

- Käyttäjä voi kuunnella / tallentaa nuotista MIDI-muotoisena tuotetun ääniraidan esikuuntelua varten
    TEHTY (tarvitsee vielä debuggausta segmentaatiovirheen takia)

- Käyttäjä voi valita nuotissa jo olevan nuotin klikkaamalla sitä, jolloin se indikoidaan nuotin muuttumisella harmaaksi
  - jos jokin nuotti on jo valittuna, se muuttuu takaisin mustaksi, eli valittuna voi olla yksi nuotti kerrallaan

- Mikäli jokin nuotti on valittuna, uuden nuotin lisääminen muuttaa kyseisen nuotin sen sijaan että nuotti ilmestyisi nuotin loppuun.

- Käyttäjä voi tallentaa nuotin svg-muotoon jatkomuokkausta varten muissa ohjelmistoissa

## Jatkokehitysideoita

Perusversion jälkeen järjestelmää täydennetään ajan salliessa esim. seuraavilla toiminnallisuuksilla:

- Napit on järjestelty paremmin niin että UI ei täyty napeista, eli dropdown -menuilla ym.

- Käyttäjä voi avata uuteen ikkunaan ohjesivun, jossa löytyy sormitusten ja länsimaisen asteikon äänten vastaavuudet shakuhachin ääniin

- Käyttäjä voi vaihtaa shakuhachi-notaatiojärjestelmien välillä, jolloin jo kirjoitettu notaatio, sekä käytettävissä olevat napit muuttuvat valitun notaatiojärjestelmän mukaiseksi

- Käyttäjä voi konvertoida jollakin muulla avoimen lähdekoodin ohjelmistolla tuotettua länsimaista notaatiota ohjelmaan shakuhachinotaatioksi

- Käyttäjä voi konfiguroida haluamansa nuottien koon, fontin ja niiden välien pituuden

- Käyttäjän luomat konfiguraatiot tallentuavat erilliselle konfigurointitiedostolle, joka ladataan tämän käyttistäessä ohjelmaa

- Nuottisivun täytyttyä avautuu muokkausnäkymään uusi nuottisivu, ja edelliset sivut tallentuvat välilehdiksi, joiden muokkaukseen voi palata

- Käyttäjä voi tehdä tekstuaalisia merkintöjä nuottiin (kirjoittaa tekstiä, piirtää hiirellä jne)

- Käyttäjä voi muuttaa otsikon ja säveltäjän tekstin fonttia

- MIDI-ääniraidan generointi ottaa huomioon äänenkorkeuksien ja -pituuksien lisäksi shakuhachille tyypilliset soittotekniikat kuten mikrointervallit, vibraaton, crescendon, hälyäänet ja muita dynaamisia yksityiskohtia

- Käyttäjä voi peruuttaa viimeisimmän muutoksen painamalla ohjelman ui:ssa olevaa peruutusnappia tai ctrl+z (ei koske tallentamista tai tiedoston aukaisemista)

- Käyttäjä voi sovelluksen UI:ssa suoraan konfiguroida ohjelmaan käytettäväksi uudenlaisia nuotteja (koska shakuhachi-nuotinnusjärjestelmiä on olemassa monia, voi olla tarve nuottimerkinnälle, jota ohjelma ei tarjoa)