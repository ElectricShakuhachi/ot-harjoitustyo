# Arkkitehtuurikuvaus

## Rakenne

Ohjelman rakenne on löyhästi MVC arkkitehtuurimallin mukainen, ja sen rakenne on yksinkertaistetussa muodossa seuraava:

<img src="https://github.com/ElectricShakuhachi/ot-harjoitustyo/blob/master/dokumentaatio/kuvat/architecture.jpg" width="420">

Tästä yksinkertaistetusta rakennekuvasta poiketen käyttäjärajapinnan luokat ovat suorassa yhteydessä palveluluokkiin, ja tarjoavat initialisoimansa ja konfiguroimansa yhteyden niihin Music-luokalle

Pakkausten koodi vastaa seuraavia tarkoituksia:

- Buttons = käyttäjäkomennot, sekä käyttöliittymän ne osat, joista ei vastaa UI-pakkaus
- Music / Part / Note = tuotettavan tiedoston mallintaminen käyttäjäkomentojen pohjalta
- UI = mallinnuksen kuvaaminen näkymäksi käyttöliittymään
- services = Useita luokkia, jotka vastaavat tiedon konvertoinnista, tallentamisesta ja lataamisesta 

Lisäksi kaikki luokat hakevat konfiguraatiotietoja vakioita sisältävästä shaku_constants.py -tiedostosta

## Käyttöliittymä

Käyttöliittymässä on yksi päänäkymä, joka koostuu sovelluksessa luotavaa nuottia kuvaavasta näkymästä, sekä käyttäjätoimintoja fasilitoivista komentonapeista ja tekstikentistä. 

### Varoitusviestit

Päänäkymän lisäksi käyttöliittymään luodaan tarvittaessa varoitusviestejä, esimerkiksi jotta käyttäjä huomioisi tallentamattoman tiedon menetyksen ladatessaan ohjelmaan toista tiedostoa.

## Sovelluslogiikka

Sovelluslogiikan keskiössä on shakuhachi-soittimen notaatiota mallintavat ShakuMusic, ShakuPart ja ShakuNote -luokat.
ShakuMusic -luokan instanssi on pääasiallinen mallinnussäilö, jonka päätehtävänä on pitää kirjaa, kontrolloida ja muokata
notaatiodataa, jonka yksityiskohdat mallinnetaan alemman tason Part ja Note -luokkiin.
  ShakuPart -luokan kukin instanssi vastaa yhtä soitinta yksi- tai moniäänisessä shakuhachi-nuotissa. Tämän luokan päätehtävät
ovat yksittäisten nuottien tietoja mallintavien Note -luokkien säilytys ja manipuolointi. Lisäksi ShakuPart -instanssi pitää
kirjaa muista merkinnöistä, joita nuottiin voi lisätä (nykyisessä sovellusversiossa tämä tarkoittaa vain oktaavialaa, eli 
suhteellista sävelkorkeutta ilmaisevia merkintöjä). Nämä lisämerkinnät tallennetaan ShakuPart -luokkaan ShakuNotation -instansseina.

Mallinnusluokkien lisäksi ohjelmisto sisältää käyttäjärajapinnasta vastaavat luokat UI ja Buttons, joista UI vastaa ShakuMusic-luokan sisältämän tiedon piirtämisestä reaaliaikaiseen näkymään käyttäjälle, ja Buttons-luokka vastaa käyttäjän ja mallinnusluokkien interaktion fasilitoimisesta lähinnä erilaisten painikkeiden avulla. 

Käyttäjärajapinnan luokat kommunikoivat myös 

## Sekvenssikaavioita

### Uuden osan luominen nuottiin instrumenttia varten

<img src="https://github.com/ElectricShakuhachi/ot-harjoitustyo/blob/master/dokumentaatio/kuvat/sequence_add_part.jpg" width="820">

## Tietojen pysyväistallennus

data -pakkaus vastaa sovelluksessa tuotetun mallinnuksen tallentamisesta ja lataamisesta. Tieto tallennetaan .shaku -tiedostomuotoon. Tiedostoa ladattaessa käynnissä olevan ohjelman mallinnusta muokataan tiedoston sisältämän datan mukaiseksi.

## Konfiguraatio

configurations -kansion sisään tallentuvan .shakucf -tiedoston sisältö päivittyy sovellusta käyttäessä. Sen tallentamisesta, lataamisesta ja käsittelystä vastaa configurations -pakkaus. Konfiguraatioon tallentuu käyttäjän antama säveltäjän nimi, sekä mahdollisia muita asetuksia, jotka vaikuttavat sovelluslogiikan oletusarvoihin uutta tiedostoa luodessa muun muassa siten, että uudessa tiedostossa on aluksi oletusarvoisesti säveltäjän nimenä käyttäjän aiemmin antama säveltäjänimi
