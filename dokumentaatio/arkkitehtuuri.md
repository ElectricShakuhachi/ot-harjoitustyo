# Arkkitehtuurikuvaus

## Rakenne

Ohjelman rakenne on löyhästi kolmitasoisen arkkitehtuurimallin mukainen, ja sen rakenne on yksinkertaistetussa muodossa seuraava:

<img src="https://github.com/ElectricShakuhachi/ot-harjoitustyo/blob/master/dokumentaatio/kuvat/architecture.jpg" width="420">

Poiketen tavanomaisesta kolmitasoisesta arkkitehtuurimallista, repositorio-luokkia ei ole toteutettu erillisinä, vaan niiden
toiminnallisuus on toteutettu muiden luokkien toiminnallisuuksissa. Ohjelmiston monenlaisen tiedontallennuksen muodot on toteutettu pääosin palvelu-luokissa ja sen pääasiallisesti käsittelemän datan mallinnus- ja käsittely tapahtuu entiteettiluokkien sisällä hierarkisessa struktuurissa.

Pakkausten koodi vastaa seuraavia tarkoituksia:

- Buttons = Käyttäjäkomentojen välittäminen mallinnus-, käyttöliittymä- ja palveluluokille.
- Music / Part / Note = tuotettavan tiedoston mallintaminen käyttäjäkomentojen pohjalta
- UI = mallinnuksen kuvaaminen näkymäksi käyttöliittymään sekä koko käyttöliittymän hahmotus
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

Mallinnusluokkien lisäksi ohjelmisto sisältää käyttäjärajapinnasta vastaavat luokat UI ja Buttons, joista UI vastaa ShakuMusic-luokan sisältämän tiedon piirtämisestä reaaliaikaiseen näkymään käyttäjälle, ja Buttons-luokka vastaa käyttäjän,mallinnus- ja palveluluokkien interaktion fasilitoimisesta lähinnä erilaisten painikkeiden avulla. 

<img src="https://github.com/ElectricShakuhachi/ot-harjoitustyo/blob/master/dokumentaatio/kuvat/packages.jpg" width="420">

## Sekvenssikaavioita

### Uuden osan luominen nuottiin instrumenttia varten

Oheinen sekvenssikaavio kuvaa 

<img src="https://github.com/ElectricShakuhachi/ot-harjoitustyo/blob/master/dokumentaatio/kuvat/sequence_add_part.jpg" width="820">

## Tietojen pysyväistallennus

FileManager -luokka vastaa tiedostojen avaamisesta ja tallentamisesta. Lisäksi sovellus sisältää useita palveluluokkia, jotka
tarjoavat toiminnallisuuden tiedon muokkaamista eri tallennusmuotoja varten.

Pääasiallinen tallennusmuoto on .shaku -tiedostomuoto, joka on toteutettu JSON -formaatin avulla. Kyseiseen muotoon voi tallentaa ohjelman mallinnusluokkien sisältämän shakuhachi-nuotin mallinnusdatan, ja kyseisestä formaatista voi myös
ladata tiedon sovellukseen.

Lisäksi .shaku -formaatin tiedoston voi myös ladata AWS S3 -repositorioon, joka on konfiguroitavissa, mutta on oletuksena
"shakunotator" -repositorio, johon ohjelman ensisijaisille käyttäjille voidaan tarjota kredentiaalit.

Ohjelmasta voi myös eksportoida nuotin PDF tai SVG -tiedostoiksi, sekä eksportoida MIDI-äänitiedoston joka mallintaa
ohjelmassa kirjoitettua nuottia ääneksi.


## Konfiguraatio

src/config/shaku_constants.py -tiedoston vakio-arvoja muuttamalla voi vaikuttaa monin tavoin sovelluksen konfiguraatioon.

ESIMERKIKSI:

1. Muuttaa käytettävää AWS S3 -repositoriota

2. Muuttaa sovelluksen tallentamien ja soittamien äänitiedostojen tempoa, voluumia, midi-soitinta ym. yksityiskohtia

3. Vaikuttaa nuotin asettelullisiin tekijöihin, kuten muun muassa:
    - Montako riviä nuotteja mahdutetaan nuottiin (nuottilinjojen välien pituus)
    - Rytmiä ilmaisevien piirtojen ja nuottien keskinäinen asettelu ja koko
    - Kuinka isoja nuotit, tekstit ym. ovat ja minkä värisinä / millä fonteilla ne piirretään eksportoituihin nuotteihin
    - Nuotin koko
    - Käyttöliittymän ruudun koko

4. Konfiguroida, mitä kuvia ja fonttia käytetään nuottien piirtämiseen.

5. Vaikuttaa nuottien sävelkorkeuteen

6. Vaihtaa ohjelman virheviestien tekstejä

Konfiguraatiotiedoston puutteellisesta käyttäjäystävällisyydestä johtuen tulevan version on tarkoitus sisältää sovelluksen UI:ssa konfiguraatiota fasilitoivan helposti ymmärrettävän paneelin.

