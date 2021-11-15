# Vaatimusmäärittely

## Sovelluksen tarkoitus

Sovelluksella voi luoda japanilaiselle shakuhachi -bambuhuilulle tarkoitettuja nuotteja, joissa käytetään perinteistä japanilaista nuotinnusta.

## Käyttöliittymäluonnos

Sovelluksesessa on yksi graafisen käyttöliittymän näkymä, jossa olevilla painikkeilla tapahtuvat kaikki käyttäjän ja sovelluksen väliset interaktiot:

<img src="https://github.com/ElectricShakuhachi/ot-harjoitustyo/blob/master/dokumentaatio/kuvat/v-1.jpg" width="750">

## Perusversion tarjoama toiminnallisuus

- Käyttäjä voi nimetä kappaleen ja säveltäjän kirjoittamalla nämä tekstikenttiin, ohjelma keskittää nimen nuottiin sopivaan kohtaan

- Käyttäjä voi lisätä nuottisivuun nuottimerkkejä painamalla merkkejä vastaavia nappeja

- Nuotit ilmestyvät oletusarvoisesti viimeisen nuotissa olevan nuotin jälkeen
   - nuoteissa merkit alkavat yläoikealta, rivit kirjoittuvat alaspäin ja seuraava rivi on edellisen vasemmalla puolella

- Käyttäjä voi valita nuotissa jo olevan nuotin klikkaamalla sitä, jolloin se indikoidaan nuotin muuttumisella harmaaksi
   - jos jokin nuotti on jo valittuna, se muuttuu takaisin mustaksi, eli valittuna voi olla yksi nuotti kerrallaan

- Mikäli jokin nuotti on valittuna, uuden nuotin lisääminen muuttaa kyseisen nuotin sen sijaan että nuotti ilmestyisi nuotin loppuun

- Käyttäjä voi peruuttaa viimeisimmän muutoksen painamalla ctrl+z (ei koske tallentamista tai tiedoston aukaisemista)

- Käyttäjä voi tallentaa nuotin ohjelman käyttämään tiedostomuotoon

- Käyttäjä voi ladata nuotin ohjelman tallentamasta tiedostosta muokattavaksi

- Käyttäjä voi tallentaa nuotin sekä pdf, että svg -muodossa
    -tallentaessa näihin muotoihin nuottiin tallentuu myös merkintä siitä, että nuotti on generoitu kyseisellä sovelluksella

## Jatkokehitysideoita

Perusversion jälkeen järjestelmää täydennetään ajan salliessa esim. seuraavilla toiminnallisuuksilla:

- Käyttäjä voi vaihtaa nuotinnustyylin eri japanilaisten shakuhachi-koulukuntien nuotinnustyylien välillä

- Käyttäjä voi vaihtaa nuottien fonttia tietokoneen sisältämien fonttien tarjoamissa rajoissa

- Käyttäjä voi tehdä tekstuaalisia merkintöjä nuottiin (kirjoittaa tekstiä, piirtää hiirellä jne)

- Käyttäjä voi luoda shakuhachi-huilulla äänitetyistä äänistä generoidun esikatselun kappaleesta
