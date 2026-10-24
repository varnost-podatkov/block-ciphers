# Bločne šifre

Laboratorijska vaja pri predmetu Varnost podatkov je namenjena sprotnemu
tedenskemu delu in učenju. Spoznali boste kriptografsko varne generatorje
naključnih vrednosti, uporabo knjižnice `cryptography`, načina AES-CTR in
AES-CBC, gnetljivost tajnopisa ter v nalogi 5 še napad na šifriran seznam ocen.
Za izris javnega frekvenčnega diagrama v nalogi 5 potrebujete tudi `matplotlib`.

## Priprava okolja

Potrebujete sodobni Python (priporočeno 3.12 ali novejši) in pakete
`cryptography`, `jupyterlab` ter `matplotlib`. Namestite jih z:

```sh
pip install -r requirements.txt
```

Če uporabljate Nix, lahko okolje pripravite z:

```sh
nix develop
```

Nato iz korena repozitorija odprite zvezek:

```sh
jupyter lab assignments.ipynb
```

## Delo z nalogo

- Navodila in prostor za rešitve so v **`assignments.ipynb`**.
- Podatkovna datoteka je v **`data/ic-za-narodov-blagor.txt`**. Imenik `data/`
  ohranite poleg zvezka, saj zvezek uporablja relativne poti do nje.
- Datoteki **`pb.py`** in **`pb_solved.py`** prikazujeta telefonski imenik pred
  šifriranjem in po njem. Uporabite ju kot pomoč pri nalogi 2.
- Dopolnite celice z oznako `# VAŠA REŠITEV`. Ohranite podpise funkcij, navodila,
  priložene teste in metapodatke celic.
- Rešitve preverjajte s priloženimi testi. `NotImplementedError` v nedopolnjeni
  funkciji pomeni, da jo morate še napisati.
- Pri delu s funkcijami, ki pišejo v datoteke, se v `data/` ustvari datoteka s
  končnico `.enc`; ta je lokalni izdelek in ni del oddaje.
- Po potrebi dodajte svoje celice za poskuse in izpis vmesnih rezultatov. Pred
  oddajo znova zaženite jedro in izvedite vse celice po vrsti od začetka do
  konca, da preverite, ali zvezek pravilno deluje tudi ob svežem zagonu.

Oddajte samo izpolnjeni **`assignments.ipynb`**. Podatkovnih datotek in
razvojnega okolja ni treba oddajati.
