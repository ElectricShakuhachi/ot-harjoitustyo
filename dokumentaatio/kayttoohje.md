# Shakuhachi Music Maker -käyttöohje

Ohjelmiston loppukäyttäjien oletetaan tuntevan shakuhachimusiikkia. Ohjelmistoon muutoin tutustuvalle tarjotaan tässä dokumentin lopussa lyhyt selitys siitä, millaista shakuhachi-musiikki ja sen notaatio on.

## Perusohjeet

Käynnistäessä avautuu automaattisesti muokattavaksi uusi nuottisivu. Nuottiin piirtyy automaattisesti näkyviin ruudukko, jonka ruudut vastaavat tahteja.
Sovelluksen nuottinäkymä on vain esikatselu, tallentaessa tekstien ja nuottien fontti tallentuu kauniimmin.
Valmista nuottia pdf:ksi eksportoitaessa voi valita, haluaako lopulliseen nuottiin tahtiruudukon, vai ei.

## Yhteenveto shakuhachi-musiikkia tuntemattomille

Shakuhachi-musiikin notaatiossa käytetään pääosin japanilaisia katakana-merkkejä, sekä osalti vain notaatioon kehitettyjä merkintöjä, tärkeimpinä näistä tahtia kuvaavat viivoja katakana-merkkien vieressä. Nuotit kirjoitetaan ylhäältä alas, ja rivit oikealta vasemmalle, eli nuotinnus aloitetaan
paperin oikeasta yläreunasta

### Tässä sovelluksessa kirjoitettava nuotinnus voidaan pääosin lukea näiden ohjeiden avulla:

1. Nuotin ruudukon ruutu vastaa yhtä tahtia nuotissa, eli tiettyä kestoa ajassa. Oletuksena tämä kesto on kaksi tyypillisimmän pituista nuottia (ns. neljäsosanuotti), kuten tässä kuvassa:

<img src="https://github.com/ElectricShakuhachi/ot-harjoitustyo/blob/master/dokumentaatio/kuvat/nuotit/1.jpg" width="300">

2. Nuotin pituudet ilmaistaan nuoteissa paitsi niiden etäisyytenä toisistaan pystysuunnassa, myös niiden vasemmalle puolelle piirtyvillä viivoilla.
    - Yksi pystyviiva = neljäsosanuotti
    - Ei lainkaan viivoja = puolinuotti (jonka pituus on kaksinkertainen neljäsosanuottiin verrattuna)
    - Yksi pystyviiva, joka yhdistyy seuraavan nuotin viereiseen pystyviivaan = molemmat nuotit ovat kahdeksasosanuotteja (puolet neljäsosanuotin kestosta)
    - Yksi pystyviiva, jonka lävistää pilkku = Yksinäinen kahdeksasosanuotti
    - Kaksi pystyviivaa = Kuudestoistaosanuotti (neljä kertaa nopeampi kuin neljäsosanuotti)

3. Nuotin sävelkorkeutta ilmaisee kaksi tekijää:
    1. Rekisterimerkintä (merkki, joka piirtyy nuottijonon vierelle ja ilmaisee että siitä lähtien nuotit ovat sitä vastaavassa rekisterissä). Usein käytetään sanaa oktaavit - mutta tämä ei vastaa tarkkaan shakuhachimusiikin rekisterejä.
        - tärkein pointti kuitenkin on siis ymmärtää, että rekisterin valinta siirtää seuraavien nuottien korkeuden merkittävästi ylös- tai alaspäin
    2. Nuottimerkki, joista jokainen viittaa johonkin tiettyyn nuottiin. Alla yksinertainen taulukko merkintöjen sävelkorkeuksien vastaavuudesta länsimaisessa asteikossa:
    <img src="https://github.com/ElectricShakuhachi/ot-harjoitustyo/blob/master/dokumentaatio/kuvat/nuotit/tozan-western.jpg" width="640">

4. Alla esimerkki ohjelmalla toteutettua shakuhachi-nuottia vastaavasta länsimaisesta nuotista:

<img src="https://github.com/ElectricShakuhachi/ot-harjoitustyo/blob/master/dokumentaatio/kuvat/nuotit/2.jpg" width="300">

<img src="https://github.com/ElectricShakuhachi/ot-harjoitustyo/blob/master/dokumentaatio/kuvat/nuotit/2-western.jpg" width="800">

Nuottien kesto merkitään nuottien viereen viiva- ja pistemerkeillä, lisäksi nuottien viereen tai alle voi tulla lisämerkintöjä liittyen erinäisiin nuotin sävelkorkeuteen ja
soittotekniikkaan vaikuttaviin asioihin.

Tässä ohjelmassa on tarjottu toiminnallisuus sekä soolo- että moniäänisten kappaleiden nuotintamiseen. Moniääniset kappaleet ovat yhtyekappaleita, joissa jokaista ääntä soittaa
eri soittaja. Moniäänisten kappaleiden notaatiossa eri äänet merkitään vierekkäin klusterina, joka jatkuu riveittäin, eli kunkin äänen soittaja soittaa siis klusterista omaa linjaansa, ja voi samalla seurata vierestä muiden äänien notaatiota osatakseen ajoittaa soittonsa oikein.

Shakuhachi sinänsä on japanilainen päästä soitettava bambuhuilu. kts. lisää internetistä tarpeen mukaan.
