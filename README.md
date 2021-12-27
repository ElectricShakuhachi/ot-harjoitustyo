# ShakuNotator - Shakuhachi Flute Sheet Music Maker

Japanilaisen bambuhuilun - shakuhachin - musiikin perinteisen japanilaisen notaation kirjoittamiseen tarkoitettu sovellus.

Sovellus on toteutettu Helsingin Yliopiston Tietojenkäsittelytieteen Ohjelmistotekniikan menetelmät -kurssin kurssityönä.

## Dokumentaatio

- [Käyttöohje](https://github.com/ElectricShakuhachi/ot-harjoitustyo/blob/master/dokumentaatio/kayttoohje.md)

- [Vaatimusmäärittely](https://github.com/ElectricShakuhachi/ot-harjoitustyo/blob/master/dokumentaatio/vaatimusmaarittely.md)

- [Arkkitehtuuri](https://github.com/ElectricShakuhachi/ot-harjoitustyo/blob/master/dokumentaatio/arkkitehtuuri.md)

- [Tyoaikakirjanpito](https://github.com/ElectricShakuhachi/ot-harjoitustyo/blob/master/dokumentaatio/tyoaikakirjanpito.md)

- [Testaus](https://github.com/ElectricShakuhachi/ot-harjoitustyo/blob/master/dokumentaatio/testaus.md)

## Asennus

### 1. Kloonaa sovellus githubista:

 ```bash
git clone git@github.com:ElectricShakuhachi/ot-harjoitustyo.git shakunotator
```

### 2. Asenna riippuvuudet komennolla:
 ```bash
poetry install
```

### 3. Voidaksesi käyttää musiikin toisto-toiminnallisuutta ohjelmassa, asenna fluidsynth.
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

### 4. Voidaksesi ladata Shakunotator -ohjelmalla yhteissäveltämiseen tarkoitettuun AWS S3 -etärepositorioon, pyydä kredentiaalit ohjelmiston kehittäjältä. 

Halutessasi voit myös käyttää jotakin muuta AWS S3 -repositoriota muuttamalla konfiguraatiotiedostossa "src/config/shaku_constants.py" vakio AWS_S3_BUCKET osoittamaan haluamasi repositorion (bucket) nimeen
    - AWS S3 -kredentiaalien käyttö vaatii [AWS Cli](https://aws.amazon.com/cli/):n asentamista ja kredentaalien konfigurointia siihen.

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

Pylint

Tiedoston .pylintrc määrittelemät tarkistukset voi suorittaa komennolla:

```bash
poetry run invoke lint
```

## Julkaistut versiot:

- [v.0.2.0-alpha](https://github.com/ElectricShakuhachi/ot-harjoitustyo/releases/tag/v0.2.0-alpha)

- [v.0.3.0-alpha](https://github.com/ElectricShakuhachi/ot-harjoitustyo/releases/tag/v0.3.0-alpha)

- [v.0.5.0-alpha](https://github.com/ElectricShakuhachi/ot-harjoitustyo/releases/tag/v0.5.0-alpha)

- [loppupalautus - v.0.7.0-alpha](https://github.com/ElectricShakuhachi/ot-harjoitustyo/releases/tag/v.0.7.0-alpha)
