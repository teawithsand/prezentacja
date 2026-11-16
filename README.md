# Verixcel — prezentacja 8 slajdów / 5 minut

Verixcel to dziennik badawczy z dowodem pierwszeństwa i selektywnym ujawnianiem.
Deck jest w Marp (Markdown), z notatkami mówcy i pięcioma artefaktami demo. Format 16:9 (1280×720).

## Szybki start

```bash
nix run .                      # wszystko: demo + PDF + PPTX + podglądy PNG
```

Albo klasycznie:

```bash
nix-shell                      # node, chromium, python + openpyxl, IBM Plex, poppler
npm install                    # @marp-team/marp-cli
./build.sh                     # demo + PDF + PPTX + podglądy PNG
```

Pojedyncze komendy:

```bash
npx marp deck.md --html --theme-set theme.css --pdf  -o out/verixcel.pdf
npx marp deck.md --html --theme-set theme.css --pptx -o out/verixcel.pptx
python3 scripts/build_demo.py && python3 scripts/verify_demo.py
```

## Co jest gotowe

| Plik | Rola |
|---|---|
| `deck.md` | 8 slajdów + notatki mówcy (komentarze HTML) |
| `theme.css` | motyw Marp: kolory, typografia, siatka, stopka |
| `out/verixcel.pdf` | backup do prezentacji, fonty osadzone, 8 stron 960×540 pt |
| `out/verixcel.pptx` | PPTX ze slajdami jako obrazami i notatkami w panelu mówcy |
| `out/preview/verixcel.001–008.png` | podgląd każdego slajdu |
| `demo/source.xlsx` | pełny arkusz: kolumna dni i 9 pomiarów, SUMA = 45 |
| `demo/redacted.xlsx` | 9 z 9 pomiarów ukrytych; widoczna tylko SUMA |
| `demo/proof.json` | format dowodu: commitment, TSA, Merkle, zk, public inputs |
| `demo/verify_output.txt` | wynik weryfikatora: PASS (demo scope) |
| `demo/redacted.pdf` | awaryjny podgląd arkusza |
| `scripts/build_demo.py` | generuje xlsx, proof.json, HTML do PDF |
| `scripts/verify_demo.py` | sprawdza hashe, inclusion i zaciemnienie |
| `shell.nix` | środowisko Nix |

## Struktura decku

| # | Slajd | Czas |
|---|---|---|
| 1 | Verixcel + obietnica | 0:00–0:25 |
| 2 | Problem naukowca i grantodawcy | 0:25–1:20 |
| 3 | Cztery składniki: zapis, czas, selektywne ujawnianie, weryfikacja | 1:20–2:00 |
| 4 | Jak to działa: TTP, zk-SNARK, łańcuch zmian | 2:00–2:50 |
| 5 | Przypadek: cztery kafelki naukowca i grantu | 2:50–3:20 |
| 6 | Przykład: wejście badacza vs wyjście komisji | 3:20–4:10 |
| 7 | Każda komórka ma swoją datę: liczby, daty, widok komisji | 4:10–4:40 |
| 8 | Dziękuję za uwagę | 4:40–5:00 |

Świadomie bez statystyk problemu: publiczność zna temat, a slajdy mają zostać proste.
Dlatego nie ma liczb, wykresów ani rankingu problemów, jest tylko napięcie: naukowiec nie odda danych, prawo nie pozwala ich przesłać, komisja nie da grantu bez sprawdzenia.

## Slajd 5 — co pokazuje

- **Lewa kolumna (wejście):** seria pomiarów, dzień 1–9, suma 45.
- **Prawa kolumna (wyjście):** te same dni, wszystkie pomiary zasłonięte, ta sama suma 45,
  etykieta „twierdzenie z dowodem kryptograficznym" i jedno zdanie werdyktu.
- Na slajdzie nie ma ani hasha, ani struktury drzewa Merkle — celowo.

## Demo — co jest prawdziwe, a co jest placeholderem

To jest **demo formatu**, nie działający system kryptograficzny.

- **Prawdziwe:** SHA-256 commitujący komórki, drzewo Merkle, ścieżki inclusion, hash pliku, sprawdzenie, że ukryte komórki są puste.
- **Placeholder:** token RFC 3161 (`tsa_token.kind = demo-placeholder`) i dowód Groth16 (`zk_proof.kind = demo-placeholder`). Nie zostały wygenerowane ani zweryfikowane.
- `verify_output.txt` kończy się `PASS (demo scope)` i wprost wypisuje, że TSA oraz zk nie były walidowane.
- Daty w artefaktach (14 marca 2026) są ilustracją narracji, nie rzeczywistym podpisem czasu.

Jeśli publiczność zapyta „pokaż proof" — trzeba powiedzieć, że to format i warstwa demo, a nie produkcyjny dowód. Podmiana na realny TSA i realny circuit to osobny krok.

## Źródła techniczne

| Element | Źródło |
|---|---|
| Trusted timestamping | RFC 3161 (2001) |
| Łańcuch haszy jako dowód istnienia | Haber & Stornetta, *Journal of Cryptology* 3(2), 99–111 (1991) |
| Interaktywne dowody z zerową wiedzą | Goldwasser, Micali, Rackoff (STOC 1985; *SIAM J. Comput.* 1989) |
| PCP theorem | Arora–Safra (1998); ALMSS (1998) |
| zk-SNARK, Groth16 | Groth, EUROCRYPT 2016 |
| PLONK | Gabizon, Williamson, Ciobotaru (2019) |
| Kotwica publiczna | OpenTimestamps; Bitcoin |

## Decyzje projektowe

1. **Nazwa Verixcel** — w tytule, stopce, metadanych i artefaktach demo.
2. **Bez statystyk problemu** — na slajdach nie ma żadnych danych o skali zjawiska.
3. **Seria 9 dni** — pomiary 8, 6, 5, 7, 3, 4, 6, 2, 4, suma 45; te same liczby w demo/source.xlsx i na slajdzie.
4. **Wszystkie pomiary ukryte** w redacted.xlsx; widoczne są tylko numery dni i suma.
5. **Bez hasha na slajdzie** — commitment jest w proof.json, nie w decku.
6. **Autor** — na slajdzie tytułowym jest miejsce na nazwisko: placeholder „Imię Nazwisko” w deck.md.

## Limity i sprawdzenia

- 8 slajdów, 16:9, marginesy 80 px, stała siatka i wspólna linia bazowa.
- Typografia: IBM Plex Sans + IBM Plex Mono; fonty osadzone w PDF.
- Kolory: problem = amber #D97706 (slajd 2), rozwiązanie = teal #0F766E (reszta), tekst #1A1A1A, tło #FAFAFA, szary #6B7280.
- Slajd 4: trzy karty algorytmów, każda z własnym „co daje".
- Slajd 7: zdanie „Dziennik: każda zmiana ma datę." i trzy arkusze tego samego fragmentu (liczby, dziennik z datami, widok komisji), daty 02.03 do 12.03, czyli przed certyfikacją 14.03; podświetlone trzy komórki poprawiane po pomiarze.
- Slajd 5: cztery kafelki (pomiary, zapis, wniosek, weryfikacja); kroki 1–2 podpisane ×1, kroki 3–4 wyróżnione tłem i plakietką ×n, bo są powtarzalne.
- Slajd 6: dwie tabele o identycznym rytmie wierszy; stopka przypomina, że TSA i zk są warstwą demo.
- Slajd 8: jedno zdanie, wyśrodkowane w pionie.
- Notatki mówcy są w deck.md i w PPTX (Panel notes).

## Backup na pytania (skrót)

- **Zenodo/OSF/DOI vs Verixcel:** repozytorium daje trwały identyfikator i dostęp; Verixcel dokłada dowód czasu i selektywne ujawnianie. Nie zastępuje repozytorium — może je uzupełniać.
- **RODO/IRB:** selektywne ujawnianie nie zwalnia z compliance; dziennik może zawierać dane wrażliwe, więc potrzebna jest polityka retencji i podstawa prawna.
- **Koszty:** proving jest drogi, verification tani; TSA i anchoring to koszt per wpis/okres. W pilocie: batchowanie i jedna kotwica na dobę.
- **Adopcja:** eksport z Excela, integracja z ELN/Git, brak vendor lock-in; kluczowy jest jeden klik i brak zmiany sposobu pracy.
- **Zagrożenia:** backdating → log + TSA; kradzież → commitment + pierwszeństwo; nieuprawniony dostęp → selektywne ujawnianie; cenzura TTP → wielu TTP + anchoring.

## Regeneracja

```bash
nix run .                 # wszystko
nix-shell --run './build.sh'
```

Po edycji demo:

```bash
nix-shell --run 'python3 scripts/build_demo.py && python3 scripts/verify_demo.py'
nix-shell --run 'chromium --headless --no-sandbox --disable-gpu --no-pdf-header-footer --print-to-pdf=demo/redacted.pdf file://$PWD/out/redacted.html'
```# prezentacja
# prezentacja
