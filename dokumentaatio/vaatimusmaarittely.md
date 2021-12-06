# Vaatimusmäärittely

## Sovelluksen tarkoitus

Sovelluksella voi luoda japanilaiselle shakuhachi -bambuhuilulle tarkoitettuja nuotteja, joissa käytetään perinteistä japanilaista nuotinnusta.

## Käyttöliittymäluonnos

Sovelluksesessa on yksi graafisen käyttöliittymän näkymä, jossa olevilla painikkeilla ja tekstikentillä tapahtuvat kaikki käyttäjän ja sovelluksen väliset interaktiot:

<img src="https://github.com/ElectricShakuhachi/ot-harjoitustyo/blob/master/dokumentaatio/kuvat/v-1.jpg" width="420">

## Perusversion tarjoama toiminnallisuus

- Käyttäjä voi nimetä kappaleen ja säveltäjän kirjoittamalla nämä tekstikenttiin, jotka ohjelma piirtää nuottipohjan yläreunoihin
  - TEHTY

- Käyttäjä voi lisätä nuottisivuun nuottimerkkejä painamalla merkkejä vastaavia nappeja
  - TEHTY

- Nuotit ilmestyvät oletusarvoisesti viimeisen nuotissa olevan nuotin jälkeen (eli alle japanilaisten nuottien mukaisesti)
  - TEHTY

- Nuotit jatkuvat seuraavalle riville edellisen vasemmalle puolelle kun tila edelliseltä loppuu
  - TEHTY

- Sivun täytyttyä ohjelma ilmoittaa sivun täyttymisestä, kehoittaa tallentamaan, eikä nuotteja voi enää lisätä
  - TEHTY

- Käyttäjä voi valita nuotissa jo olevan nuotin klikkaamalla sitä, jolloin se indikoidaan nuotin muuttumisella harmaaksi
  - jos jokin nuotti on jo valittuna, se muuttuu takaisin mustaksi, eli valittuna voi olla yksi nuotti kerrallaan

- Mikäli jokin nuotti on valittuna, uuden nuotin lisääminen muuttaa kyseisen nuotin sen sijaan että nuotti ilmestyisi nuotin loppuun

- Käyttäjä voi peruuttaa viimeisimmän muutoksen painamalla ohjelman ui:ssa olevaa peruutusnappia tai ctrl+z (ei koske tallentamista tai tiedoston aukaisemista)

- Käyttäjä voi tallentaa nuotin ohjelman käyttämään tiedostomuotoon

- Käyttäjä voi ladata nuotin ohjelman tallentamasta tiedostosta muokattavaksi

- Käyttäjä voi tallentaa nuotin sekä pdf, että svg -muodossa
    -tallentaessa näihin muotoihin nuottiin tallentuu myös merkintä siitä, että nuotti on generoitu kyseisellä sovelluksella

## Jatkokehitysideoita

Perusversion jälkeen järjestelmää täydennetään ajan salliessa esim. seuraavilla toiminnallisuuksilla:

- Käyttäjä voi konfiguroida haluamansa nuottien koon ja niiden välien pituuden

- Käyttäjän luomat konfiguraatiot tallentuavat erilliselle konfigurointitiedostolle, joka ladataan tämän käyttistäessä ohjelmaa

- Nuottisivun täytyttyä avautuu muokkausnäkymään uusi nuottisivu, ja edelliset sivut tallentuvat välilehdiksi, joiden muokkaukseen voi palata

- Käyttäjä voi vaihtaa nuotinnustyylin eri japanilaisten shakuhachi-koulukuntien nuotinnustyylien välillä

- Käyttäjä voi vaihtaa nuottien fonttia

- Käyttäjä voi tehdä tekstuaalisia merkintöjä nuottiin (kirjoittaa tekstiä, piirtää hiirellä jne)

- Käyttäjä voi muuttaa otsikon ja säveltäjän tekstin fonttia

- Käyttäjä voi luoda shakuhachi-huilulla äänitetyistä äänistä generoidun esikatselun kappaleesta
