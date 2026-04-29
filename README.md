# Book Review App

**Book Review App** on Flask-pohjainen web-sovellus, jossa käyttäjät voivat luoda tunnuksen, etsiä ja julkaista kirja-arvosteluja.

##  Sovelluksen toiminnot

* Sovelluksessa käyttäjät voivat jakaa kirja-arvosteluja. Jokaisessa arvostelussa näkyy kirjan nimi, kirjailija ja kuvaus.
* Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
* Käyttäjä pystyy lisäämään arvosteluja sekä muokkaamaan ja poistamaan lisäämiään arvosteluja.
* Käyttäjä näkee sovellukseen lisätyt arvostelut.
* Käyttäjä pystyy etsimään arvosteluja hakusanalla (esim. kirjan nimi tai kirjailija).
* Käyttäjäsivu näyttää, montako arvostelua käyttäjä on lisännyt ja listan käyttäjän lisäämistä arvosteluista.
* Käyttäjä pystyy valitsemaan arvostelulle yhden tai useamman genren (esim. jännitys, romaani, fantasia) sekä arvosanan.
* Käyttäjät voivat kommentoida arvosteluja.
* Käyttäjät saavat ilmoituksen, kun heidän arvosteluihinsa lisätään kommentteja.
* Käyttäjät voivat lisätä profiilikuvan
---

## Asennusohjeet

### 1. Kloonaa projekti
```bash
git clone <repo-url>
cd book-review-app
```

### 2. Luo ja aktivoi virtuaaliympäristö
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Asenna riippuvuudet
```bash
pip install -r requirements.txt
```

### 4. Luo tietokanta ja lisää alkutiedot
```bash
sqlite3 database.db < schema.sql
sqlite3 database.db < init.sql
```

### 5. Käynnistä sovellus
```bash
flask run
```


### 6. Avaa selaimessa
```text
http://127.0.0.1:5000
```
