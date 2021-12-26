# Vaatimusmäärittely

## Sovelluksen tarkoitus

Sovelluksella voi luoda japanilaiselle shakuhachi -bambuhuilulle tarkoitettuja nuotteja, joissa käytetään perinteistä japanilaista nuotinnusta. Lisäksi sovelluks mahdollistaa nuottien jakamisen ja yhdessä editoinnin pilvipalveluun tallentamisen
avulla.

## Käyttöliittymäluonnos

Sovelluksesessa on yksi graafisen käyttöliittymän näkymä, jossa olevilla painikkeilla ja tekstikentillä tapahtuvat kaikki käyttäjän ja sovelluksen väliset interaktiot (lukuunottamatta erillisenä avautuvia viestejä ja tiedostojen tallentamiseen ja lataamiseen liittyviä ikkunoita)

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

- Käyttäjä voi eksportata nuotin pdf-muotoon
    TEHTY

- Käyttäjä voi eskportata nuotin svg-muotoon
    TEHTY

- Jos käyttäjä on asentanut tietokoneelleen AWS Cli:n ja konfiguroinut siihen Shakunotator -bucket:ia (ohjelman yhteiskäyttöä varten luotu s3 -säilö) varten tarvittavat kredentiaalit, hän voi uploadata nuotin s3:seen
    TEHTY

- Jos käyttäjällä ei ole tarvittavaa AWS Cli -konfiguraatiota, upload-napin painallus aiheuttaa ilmoituksen, että sen käyttö vaatii AWS-kredentiaaleja
    TEHTY

- Käyttäjä voi tallentaa nuotista MIDI-ääniraidan sellaisenaan, tai wav-muotoon konvertoituna
    TEHTY

- Käyttäjä voi soittaa ohjelmassa luomassaan kappaleesta esikuuntelun
    TEHTY

- Käyttäjä voi pysäyttää kuuntelun
    TEHTY

- Käyttäjä voi lisätä nuottiin myös taukoja
    TEHTY

- Ladatessa tiedostoa ohjelma varoittaa, että kannattaa tallentaa, jos näkymällä on jo tehty muokkauksia nuottiin.
    TEHTY

## Jatkokehitysideoita

Perusversion jälkeen järjestelmää täydennetään ajan salliessa esim. seuraavilla toiminnallisuuksilla:

- Nuottisivun täytyttyä avautuu muokkausnäkymään uusi nuottisivu, ja edelliset sivut tallentuvat välilehdiksi, joiden muokkaukseen voi palata. Tämän toiminallisuuden myötä poistuu tarve estää lisäämästä kappaleeseen osia, jos sivulle ei mahdu,
vaan osia jatketaan automaattisesti uusille sivuille.

- Käyttäjä voi poistaa nuotista osan ja nuottien välit konfiguroituvat jälleen lähemmäs toisiaan

- Käyttäjä voi valita nuotissa jo olevan nuotin klikkaamalla sitä, jolloin se indikoidaan nuotin muuttumisella harmaaksi
  - jos jokin nuotti on jo valittuna, se muuttuu takaisin mustaksi, eli valittuna voi olla yksi nuotti kerrallaan

- Mikäli jokin nuotti on valittuna, uuden nuotin lisääminen muuttaa kyseisen nuotin sen sijaan että nuotti ilmestyisi nuotin loppuun.

- Mikäli jokin nuotti on valittuna ja klikkaa oktaavi-nappia, muuttuu oktaavi kyseisen nuotin osalta ja tarvittavat oktaavimerkit piirtyvät

- Käyttäjä voi eksportata nuotin MusicXML -muotoon

- Käyttäjä voi importata MusicXML -tiedoston joka konvertoituu shakuhachinotaatioksi

- Napit on järjestelty paremmin niin että UI ei täyty napeista, eli dropdown -menuilla ym.

- Käyttäjä voi avata uuteen ikkunaan ohjesivun, jossa löytyy sormitusten ja länsimaisen asteikon äänten vastaavuudet shakuhachin ääniin

- Käyttäjä voi vaihtaa shakuhachi-notaatiojärjestelmien välillä, jolloin jo kirjoitettu notaatio, sekä käytettävissä olevat napit muuttuvat valitun notaatiojärjestelmän mukaiseksi

- Käyttäjä voi konfiguroida haluamansa nuottien koon, fontin ja niiden välien pituuden

- Käyttäjän luomat konfiguraatiot tallentuavat erilliselle konfigurointitiedostolle, joka ladataan tämän käyttistäessä ohjelmaa

- Käyttäjä voi tehdä tekstuaalisia merkintöjä nuottiin (kirjoittaa tekstiä, piirtää hiirellä jne)

- Käyttäjä voi muuttaa otsikon ja säveltäjän tekstin fonttia

- MIDI-ääniraidan generointi ottaa huomioon äänenkorkeuksien ja -pituuksien lisäksi shakuhachille tyypilliset soittotekniikat kuten mikrointervallit, vibraaton, crescendon, hälyäänet ja muita dynaamisia yksityiskohtia

- Käyttäjä voi peruuttaa viimeisimmän muutoksen painamalla ohjelman ui:ssa olevaa peruutusnappia tai ctrl+z (ei koske tallentamista tai tiedoston aukaisemista)

- Käyttäjä voi sovelluksen UI:ssa suoraan konfiguroida ohjelmaan käytettäväksi uudenlaisia nuotteja (koska shakuhachi-nuotinnusjärjestelmiä on olemassa monia, voi olla tarve nuottimerkinnälle, jota ohjelma ei tarjoa)

- Käyttäjä voi poistaa osan, jolloin siihen kirjoitetut nuotit häviävät ja muut osat keskitetään uudelleen.

- Käyttäjä voi luoda nuotin joko pysty- tai vaaka-asennossa (portrait / landscape)

- Käyttäjä voi vaihtaa ui:n kielen ainakin joko suomeksi, englanniksi tai japaniksi

- Ohjelmisto tunnistaa tietokoneen oletuskielen ja näyttää ui:n oletuksena sillä kielellä, mikäli kieli on ohjelmassa saatavilla

- Käyttäjä voi määrittää jokaiselle osalle eri äänialaisen shakuhachin
