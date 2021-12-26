# Shakuhachi Music Maker

Japanilaisen bambuhuilun - shakuhachin - musiikin perinteisen japanilaisen notaation kirjoittamiseen tarkoitettu sovellus.

Sovellus on toteutettu Helsingin Yliopiston Tietojenkäsittelytieteen Ohjelmistotekniikan menetelmät -kurssin kurssityönä.

## Dokumentaatio

- [Vaatimusmäärittely](https://github.com/ElectricShakuhachi/ot-harjoitustyo/blob/master/dokumentaatio/vaatimusmaarittely.md)

- [Arkkitehtuuri](https://github.com/ElectricShakuhachi/ot-harjoitustyo/blob/master/dokumentaatio/arkkitehtuuri.md)

- [Tyoaikakirjanpito](https://github.com/ElectricShakuhachi/ot-harjoitustyo/blob/master/dokumentaatio/tyoaikakirjanpito.md)

- [Testaus](https://github.com/ElectricShakuhachi/ot-harjoitustyo/blob/master/dokumentaatio/testaus.md)

- [Käyttöohje](https://github.com/ElectricShakuhachi/ot-harjoitustyo/blob/master/dokumentaatio/kayttoohje.md)

## Asennus

1. Kloonaa sovellus githubista:

 ```bash
git clone git@github.com:ElectricShakuhachi/ot-harjoitustyo.git shakuhachi_music_maker
```

2. Asenna riippuvuudet komennolla:
 ```bash
poetry install
```

3. Voidaksesi käyttää musiikin toisto-toiminnallisuutta ohjelmassa, asenna fluidsynth.
Asennuksen tapa riippuu käyttöjärjestelmästä:

- Ubuntu tai Debian:
 ```bash
sudo apt-get install fluidsynth
```

- Mac OS X (Homebrew:in avulla):
 ```bash
brew install fluidsynth
```

- Muille käyttöjärjestelmille:
[Lue fluidsynthin dokumentaatiosta](https://github.com/FluidSynth/fluidsynth/wiki/Download)

## Komentorivitoiminnot

Ohjelman käynnistäminen:

 ```bash
poetry run invoke start
```

Testien suorittaminen:

 ```bash
poetry run invoke test
```
Testikattavuusraportin generoiminen hmtlcov -hakemistoon:

 ```bash
poetry run invoke coverage-report
```

## Julkaistut versiot:

- [v0.2.0-alpha](https://github.com/ElectricShakuhachi/ot-harjoitustyo/releases/tag/v0.2.0-alpha)

- [v0.3.0-alpha](https://github.com/ElectricShakuhachi/ot-harjoitustyo/releases/tag/v0.3.0-alpha)