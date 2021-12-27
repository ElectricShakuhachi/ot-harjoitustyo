# Testausdokumentti

HUOM - Tämän dokumentin määrittelemästä testauksesta osa toteutetaan vasta (27.12.2021)

Ohjelmaa on testattu automatisoiduin yksikkötestien avulla, sekä manuaalisesti eri käyttöympäristöissä.

## Yksikkötestaus

### Mallinnusluokat

Shakuhachi-musiikkia mallintavat ShakuMusic, ShakuPart, ShakuNote ja ShakuNotation -luokat on testattu kukin omilla testiluokillaan TestShakuMusic, TestShakuPart, TestShakuNote ja TestShakuNotation.

### Ohjausluokat

Käyttäjäkomennoista, sekä palveluluokkien alustamisesta ja yhdistämisestä mallinnusluokkaan vastaava Buttons -luokka on testattu testiluokalla TestButtons.

### Palveluluokat

Palveluluokkia (ImageScaler, MusicConverter, FileManager, ImageCreator, MidiCreator, MidiTrack, MusicPlayer ja SvgCreator) on kutakin testattu niitä vastaavissa testiluokissa:

(TestImageScaler, TestMusicConverter, TestFileManager, TestImageCreator, TestMidiCreator, TestMidiTrack, TestMusicPlayer ja TestSvgCreator)

### Testikattavuus

Käyttöliittymää lukuunottamatta testauksen haarautumakattavuus on

<img src="https://github.com/ElectricShakuhachi/ot-harjoitustyo/blob/master/dokumentaatio/kuvat/coverage.jpg" width="420">

## Järjestelmätestaus

Sovellus on järjestelmätestattu asentamalla se käyttöohjeiden mukaisesti, sekä käymällä läpi toiminnallisuuksien luottelo ja kokeilemalla niistä jokaista usealla eri tavalla, pyrkien koittamaan myös epäoletettavat käyttötavat.

Ko. manuaalinen järjestelmätestaus on toteutettu seuraavilla käyttöjärjestelmillä:

Ubuntu 20.04.3 (Gnome 3.36.8)
