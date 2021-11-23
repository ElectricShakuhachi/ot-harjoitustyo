# Shakuhachi Music Maker

Japanilaisen bambuhuilun - shakuhachin - musiikin perinteisen japanilaisen notaation kirjoittamiseen tarkoitettu sovellus.

Sovellus on toteutettu Helsingin Yliopiston Tietojenkäsittelytieteen Ohjelmistotekniikan menetelmät -kurssin kurssityönä.

## Dokumentaatio

[vaatimusmaarittely.md](https://github.com/ElectricShakuhachi/ot-harjoitustyo/blob/master/dokumentaatio/vaatimusmaarittely.md)

[tyoaikakirjanpito.md](https://github.com/ElectricShakuhachi/ot-harjoitustyo/blob/master/dokumentaatio/tyoaikakirjanpito.md)

## Asennus

 ```bash
poetry install
```

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
