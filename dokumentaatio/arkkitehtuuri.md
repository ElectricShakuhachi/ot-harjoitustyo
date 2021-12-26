# Arkkitehtuurikuvaus

## Rakenne

Ohjelman rakenne on MVC-arkkitehtuurin mukainen ja sen pakkausrakenne on seuraava

<img src="https://github.com/ElectricShakuhachi/ot-harjoitustyo/blob/master/dokumentaatio/kuvat/architecture.jpg" width="420">

Pakkausten koodi vastaa seuraavia tarkoituksia:

- controls = käyttäjäkomennot, sekä käyttöliittymän ne osat, joista ei vastaa view-pakkaus
- model = tuotettavan tiedoston mallintaminen käyttäjäkomentojen pohjalta
- view = mallinnuksen kuvaaminen näkymäksi käyttöliittymään
- data = tiedostojen tallentaminen, lataaminen ja käsittely - lukuunottamatta konfiguraatiotiedostoja
- configurations = konfiguraatiotiedostojen tallentamisesta, lataaminen ja käsittelystä

## Käyttöliittymä

Käyttöliittymässä on yksi päänäkymä, joka koostuu sovelluksessa luotavaa nuottia kuvaavasta näkymästä, sekä käyttäjätoimintoja fasilitoivista komentonapeista ja tekstikentistä.

### Varoitusviestit

Päänäkymän lisäksi käyttöliittymään luodaan tarvittaessa varoitusviestejä, jotka sisältävät komentonäppäimiä käyttäjää varten. Varoitusviestejä on kahdenlaisia:

1. Näkymän täyttyessä ilmestyy varoitusviesti, joka ilmoittaa nuotin olevan täynnä ja kehoittaa käyttäjää tallentamaan. Viestin näkymä sisältää lisäksi napin, jolla voi tallentaa sivun ja aloittaa uuden tyhjän sivun muokkauksen

2. Sovellusta sammuttaessa ilmestyy varoitusviesti, joka kysyy, haluaako käyttäjä tallentaa sivun. Viestin näkymä sisältää lisäksi napin, jolla voi tallentaa sivun, minkä jälkeen ohjelma sammuu.

## Sovelluslogiikka

## Sekvenssikaavioita

### Uuden osan luominen nuottiin instrumenttia varten

<img src="https://github.com/ElectricShakuhachi/ot-harjoitustyo/blob/master/dokumentaatio/kuvat/sequence_add_part.jpg" width="820">

## Tietojen pysyväistallennus

data -pakkaus vastaa sovelluksessa tuotetun mallinnuksen tallentamisesta ja lataamisesta. Tieto tallennetaan .shaku -tiedostomuotoon. Tiedostoa ladattaessa käynnissä olevan ohjelman mallinnusta muokataan tiedoston sisältämän datan mukaiseksi.

## Konfiguraatio

configurations -kansion sisään tallentuvan .shakucf -tiedoston sisältö päivittyy sovellusta käyttäessä. Sen tallentamisesta, lataamisesta ja käsittelystä vastaa configurations -pakkaus. Konfiguraatioon tallentuu käyttäjän antama säveltäjän nimi, sekä mahdollisia muita asetuksia, jotka vaikuttavat sovelluslogiikan oletusarvoihin uutta tiedostoa luodessa muun muassa siten, että uudessa tiedostossa on aluksi oletusarvoisesti säveltäjän nimenä käyttäjän aiemmin antama säveltäjänimi
