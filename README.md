# Book Review App

**Book Review App** on Flask-pohjainen web-sovellus, jossa käyttäjät voivat luoda tunnuksen, etsiä ja julkaista kirja-arvosteluja.

##  Sovelluksen toiminnot

* Sovelluksessa käyttäjät voivat jakaa kirja-arvosteluja. Jokaisessa kirjassa näkyy kirjan nimi, kirjailija ja kuvaus.
* Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
* Käyttäjä pystyy lisäämään kirjoja sekä muokkaamaan ja poistamaan lisäämiään kirjoja.
* Käyttäjä näkee sovellukseen lisätyt kirjat.
* Käyttäjä pystyy etsimään kirjoja hakusanalla (esim. kirjan nimi tai kirjailija).
* Käyttäjäsivu näyttää, montako kirjaa käyttäjä on lisännyt ja listan käyttäjän lisäämistä kirjoista.
* Käyttäjä pystyy valitsemaan kirjalle yhden tai useamman genren (esim. jännitys, romaani, fantasia).
* Käyttäjät voivat antaa kirjoille arvosteluja, joissa on kommentti ja arvosana. Kirjan sivulla näytetään arvostelut ja keskimääräinen arvosana.

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
