# Shakuhachi Music Maker -käyttöohje

Ohjelmiston loppukäyttäjien oletetaan tuntevan shakuhachimusiikkia ja sen notaatiota. Ohjelmistoon muutoin tutustuvalle tarjotaan tämän dokumentin lopussa lyhyt selitys siitä, millaista shakuhachi-musiikki ja sen notaatio on, ja miten se on ohjelmassa toteutettu.

## Perusohjeet

1. Sovelluksen käynnistyminen:

Käynnistäessä avautuu automaattisesti muokattavaksi uusi nuottisivu. Nuottiin piirtyy näkyviin ruudukko, jonka ruudut vastaavat tahteja:

<img src="https://github.com/ElectricShakuhachi/ot-harjoitustyo/blob/master/dokumentaatio/kuvat/start.jpg" width="400">

2. Käyttäjäympäristön osat:

<img src="https://github.com/ElectricShakuhachi/ot-harjoitustyo/blob/master/dokumentaatio/kuvat/parts.jpg" width="600">

    1. Sävellyksen nimen ja säveltäjän asettamisen tekstikentät ja painikkeet
    2. Rekisterin (oktaavin) valinta seuraavaksi kirjoitettaville nuoteille
    3. Nuottinäppäimet - nuottien lisääminen nuottiin
    4. Taukonäppäimet - taukojen lisääminen nuottiin
        - huom, valittu nuotin pituus ei koske taukoja
    5. Pituusnäppäimet - lisättävän nuotin keston valitseminen
    6. Osien lisäys -nappi, sekä osanapit
        - moniäänisten kappaleiden kirjoittamista varten
    7. Eksportointinapit
        - PDF nuotin tulostamista varten
        - SVG, jotta nuottia voisi muokata lisää vektorigrafiikka-ohjelmistoissa
        - MIDI, jotta nuotista voisi tallentaa musiikin soitettavissa olevaan muotoon
            - HUOM vaatii fluidsynth -asennuksen, kts. README
    8. Tallennus, lataus ja upload -etärepositorioon -napit
        - HUOM etärepositorioon lataus vaatii kredentiaalit AWS S3 -repositorioon, kts. README
    9. Play/Stop -nappi sävellyksen esikuunteluun
        - HUOM vaatii fluidsynth -asennuksen, kts. README

3. Sekalaisia ohjeita, jotka kannattaa lukea läpi:

- Moniäänisyydestä:

Yllä olevan käyttöympäristön osien luettelon avulla pääset hyvin alkuun - osat ovat melko helppo ymmärtää suoraan sen avulla.
Moniäänisiin kappaleihin voi lisätä osat joko heti aluksi, tai niitä voi lisätä kesken säveltämisen missä vaiheessa hyvänsä - jo kirjoitetut osat keskittyvät uudelleen nuottiin sen mukaisesti. 

- Yksi sivu kerrallaan:

Huomioi, että jos nuotteja on paperilla jo paljon, ei välttämättä osien lisääminen enää ole mahdollista, koska nuotit eivät mahtuisi paperille. (Tässä sovelluksen versiossa ei ole toteutettu monisivuisten kappaleiden muokkaamista -> mutta se on tulossa tulevaan julkaisuun) Toisin sanoen monisivuiset kappaleet on tässä versiossa luotava sivu kerrallaan.

- Tauot:

Valittu lisättävän nuotin pituus ei koske taukoja, joilla on vakiopituutensa, eli pallon muotoinen tauko kestää neljäsosanuotin verran, pilkun muotoinen kestää kahdeksasosanuotin verran

- Rekisterit:

Valitessasi seuraavaksi kirjoitettaville äänille rekisterin rekisterinapeista, vaihtuu näkymässä automaattisesti lisättävissä olevien äänien lista, sillä jokainen rekisteri ei sisällä tarkalleen samoja mahdollisia nuottimerkintöjä.
- Tallennus ja lataus:

Save- ja Load -napeilla voit tallentaa ja ladata nuotteja .shaku -tiedostomuodossa. Load-nappia painaessa ohjelma tarkastaa ja ilmoittaa sinulle, jos olet tehnyt tallentamattomia muutoksia nuottiin. Voit peruuttaa silloin vielä latauksen menettämättä tietoja. 

HUOM! Ei ole taattua että tämänhetkisen ohjelman version tallentamat .shaku -tiedostot ovat luettavissa tulevilla ohjelman versioilla.

- Tiedoston uploadaaminen etärepositorioon (internettiin)

Painamalla upload-nappia voi ladata muokattavana olevan nuotin AWS S3 -repositorioon. Nuotille tulee olla merkittynä nimi, jotta lataus olisi mahdollista. Lisäksi nuotin pitää olla nimi, joka ei ole toisen nuotin nimenä jo repositoriossa. (Ylikirjoittaminen ei ole mahdollista, mutta ohjelma ei anna ladata nuottia mikäli nimi on kopio, ja siinä tapauksessa nimi on syytä vaihtaa, mikäli haluaa ladata nuotin repositorioon)

Lisäksi etärepositorioon lataus vaatii kredentiaalit AWS S3 -repositorioon, kts. README

- Eksportointi

Käyttämällä eksportointinappeja, voit tallentaa nuotin sisältämät tiedot PDF- tai SVG-muotoon. PDF-muoto on suositeltavampi nuotin tulostamista ym. käyttöä varten, mutta eksportoimalla SVG-muotoon saa tiedoston, jota voi muokata lisää vektorigrafiikkaohjelmistoissa. Lisäksi nuoteista generoidun MIDI-tiedoston voi eksportoida.

## Yhteenveto shakuhachi-musiikkia tuntemattomille

Shakuhachi-musiikin notaatiossa käytetään pääosin japanilaisia *katakana*-merkkejä, sekä osalti vain notaatioon kehitettyjä merkintöjä, tärkeimpinä näistä tahtia kuvaavat viivoja *katakana*-merkkien vieressä. Nuotit kirjoitetaan ylhäältä alas, ja rivit oikealta vasemmalle, eli nuotinnus aloitetaan
paperin oikeasta yläreunasta

### Tässä sovelluksessa kirjoitettava nuotinnus voidaan pääosin lukea näiden ohjeiden avulla:

1. Shakuhachi-nuotteja kirjoitetaan ylhäältä alas jonona japanilaisia merkkejä. Rivit vaihtuvat oikealta vasemmalle. 

2. Shakuhachi-nuotissa voi olla tahtiruudukko tai ei (ohjelmassa ruudukko on aina läsnä käyttöympäristössä, mutta nuotin voi eksportoida joko ruudukon kanssa tai ilman. Nuotin ruudukon ruutu vastaa yhtä tahtia nuotissa, eli tiettyä kestoa ajassa. Oletuksena tämä kesto on kaksi tyypillisimmän pituista nuottia (ns. neljäsosanuotti), kuten tässä kuvassa:

<img src="https://github.com/ElectricShakuhachi/ot-harjoitustyo/blob/master/dokumentaatio/kuvat/nuotit/1.jpg" width="300">

3. Nuotin pituudet ilmaistaan nuoteissa paitsi niiden etäisyytenä toisistaan pystysuunnassa, myös niiden vasemmalle puolelle piirtyvillä viivoilla.
    - Yksi pystyviiva = neljäsosanuotti
    - Ei lainkaan viivoja = puolinuotti (jonka pituus on kaksinkertainen neljäsosanuottiin verrattuna)
    - Yksi pystyviiva, joka yhdistyy seuraavan nuotin viereiseen pystyviivaan = molemmat nuotit ovat kahdeksasosanuotteja (puolet neljäsosanuotin kestosta)
    - Yksi pystyviiva, jonka lävistää pilkku = Yksinäinen kahdeksasosanuotti
    - Kaksi pystyviivaa = Kuudestoistaosanuotti (neljä kertaa nopeampi kuin neljäsosanuotti)

4. Taukojen pituutta ei merkitä erikseen. Pallolta näyttävä tauko merkitsee neljäsosanuotin pituista taukoa, pilkulta näyttävä tauko merkitsee kahdeksasosanuotin pituista taukoa

5. Nuotin sävelkorkeutta ilmaisee kaksi tekijää:
    1. Rekisterimerkintä (merkki, joka piirtyy nuottijonon vierelle ja ilmaisee että siitä lähtien nuotit ovat sitä vastaavassa rekisterissä). Usein käytetään sanaa oktaavit - mutta tämä ei vastaa tarkkaan shakuhachimusiikin rekisterejä.
        - tärkein asia rekisteristä on ymmärtää, että rekisterin valinta siirtää seuraavien nuottien korkeuden merkittävästi ylös- tai alaspäin
    2. Nuottimerkki, joista jokainen viittaa johonkin tiettyyn nuottiin. Alla yksinertainen taulukko merkintöjen sävelkorkeuksien vastaavuudesta länsimaisessa asteikossa:
    <img src="https://github.com/ElectricShakuhachi/ot-harjoitustyo/blob/master/dokumentaatio/kuvat/nuotit/tozan-western.jpg" width="640">

6. Alla esimerkki ohjelmalla toteutettua shakuhachi-nuottia vastaavasta länsimaisesta nuotista:

<img src="https://github.com/ElectricShakuhachi/ot-harjoitustyo/blob/master/dokumentaatio/kuvat/nuotit/2.jpg" width="300">

<img src="https://github.com/ElectricShakuhachi/ot-harjoitustyo/blob/master/dokumentaatio/kuvat/nuotit/2-western.jpg" width="800">

Tässä ohjelmassa on tarjottu toiminnallisuus sekä soolo- että moniäänisten kappaleiden nuotintamiseen. Moniääniset kappaleet ovat yhtyekappaleita, joissa jokaista ääntä soittaa
eri soittaja. Moniäänisten kappaleiden notaatiossa eri äänet merkitään vierekkäin klusterina, joka jatkuu riveittäin, eli kunkin äänen soittaja soittaa siis klusterista omaa linjaansa, ja voi samalla seurata vierestä muiden äänien notaatiota osatakseen ajoittaa soittonsa oikein.

7. Esimerkki yhtyekappaleesta ja sitä vastaavasta länsimaisesta nuotista:

<img src="https://github.com/ElectricShakuhachi/ot-harjoitustyo/blob/master/dokumentaatio/kuvat/nuotit/3.jpg" width="400">

<img src="https://github.com/ElectricShakuhachi/ot-harjoitustyo/blob/master/dokumentaatio/kuvat/nuotit/3-western.jpg" width="700">

8. Logo:

<img src="https://github.com/ElectricShakuhachi/ot-harjoitustyo/blob/master/src/graphics/shakuicon.png" width="90">

Shakunotator -ohjelmiston logo viittaa shakuhachin historiaan liittyneiden [komuso-munkkien](https://en.wikipedia.org/wiki/Komus%C5%8D) päähineeseen.