---
marp: true
theme: verixcel
size: 16:9
paginate: true
title: Verixcel
description: Prezentacja 8 slajdów / 5 minut
footer: 'Verixcel'
---

<!-- _class: title -->
<!-- _footer: '' -->
<!-- _paginate: false -->

<div class="title-main">
<h1>Verixcel</h1>
<p class="lead">Weryfikacja wyników naukowych bez ujawniania danych źródłowych.s</p>
</div>

<div class="title-bottom">
<p class="author">Imię Nazwisko</p>
</div>

<!--
CEL (0:00–0:25): nazwać projekt i obietnicę, bez technologii.
Zdanie otwarcia: „Verixcel. Dziennik, który nie deklaruje czasu — dowodzi go. I pozwala pokazać wynik, nie oddając danych."
-->

---

<!-- _class: warn -->

<div class="kicker">Problem</div>

## Problem naukowca i grantodawcy

<div class="standoff">
  <div class="side-card">
    <div class="label">Naukowiec</div>
    <p class="voice">Oddam dane i ktoś zabierze mój pomysł</p>
    <p class="still">Dodatkowo czasem danych nie wolno przesłać np. gdy są to dane medyczne.</p>
  </div>
  <div class="side-card">
    <div class="label">Komisja grantowa</div>
    <p class="voice">Muszę sprawdzić, czy wyniki są interesujące</p>
    <p class="still">Bez tego nie przyznam grantu.</p>
  </div>
</div>

<div class="answer">Verixcel daje naukowcowi gwarancję daty (w tym pierwszeństwa), a komisji dowód poprawności, podczas gdy dane pozostają niejawne.</div>

---

## Cztery składniki

<div class="steps4">
  <div class="stepbig">
    <div class="n">01</div>
    <h3>Zapis</h3>
    <p>wyniki badań w arkuszu</p>
  </div>
  <div class="stepbig">
    <div class="n">02</div>
    <h3>Znacznik czasu</h3>
    <p>podpisany czas od Trusted Third Party</p>
  </div>
  <div class="stepbig">
    <div class="n">03</div>
    <h3>Selektywne ujawnianie</h3>
    <p>tylko wynik, nie pomiary</p>
  </div>
  <div class="stepbig">
    <div class="n">04</div>
    <h3>Weryfikacja</h3>
    <p>każdy może sprawdzić wynik i datę uzyskania danych wejściowych</p>
  </div>
</div>

<!--
CEL (1:20–1:55): trzy kroki, zero diagramów.
1. Zapisujesz wpis — commitment wiąże treść, więc każda zmiana zmienia hash.
2. Czas — TSA podpisuje moment, log jest append-only, więc przepisanie historii zostawia ślad.
3. Ujawniasz — dowód inclusion pokazuje, że komórki są częścią wpisu; zk-SNARK dowodzi wyniku formuły bez ujawniania danych.
-->

---
## Jak to działa?

<div class="algo-grid">
  <div class="algo">
    <div class="tag">Czas</div>
    <h3>Guaranteed Time Providers</h3>
    <p>Niezależny podmiot np. OpenTimestamps podpisuje moment zapisu. Podpisu nie da się cofnąć ani podrobić.</p>
    <p class="out">→ dowód, kiedy dane powstały</p>
  </div>
  <div class="algo">
    <div class="tag">Obliczenia</div>
    <h3>zk-SNARK</h3>
    <p>Publikuje wynik funkcji bez odtajniania danych wejściowych i potwierdza, że te dane wejściowe faktycznie istnieją.</p>
    <p class="out">→ wynik dowolnej* funkcji bez oddawania danych</p>
  </div>
  <div class="algo">
    <div class="tag">Historia</div>
    <h3>Łańcuch zmian</h3>
    <p>Każdy wpis wskazuje poprzedni, więc zmiany widać w czasie.</p>
    <p class="out">→ prześledzisz każdą zmianę</p>
  </div>
</div>

<div class="algo-sum">Razem: wynik, czas i historia, a sprawdzić to może każdy, bez ufania naukowcowi.</div>

<p class="footnote">* dowolnej funkcji, którą da się wyrazić przez skończoną liczbę dodawań i możeń</p>

<!--
CEL (2:00–2:50): trzy klocki i to, co daje każdy z osobna.
TTP (RFC 3161) — podpisany czas; odpowiada na pytanie „kiedy to powstało".
zk-SNARK — dowód obliczenia; odpowiada na pytanie „czy wynik jest poprawny" bez pokazywania wejść; potwierdza też, że wejścia istnieją.
Razem: pierwszeństwo + poprawność + poufność. Gwiazdka przy „dowolnej funkcji" jest istotna — circuit trzeba zbudować osobno dla każdej funkcji.
-->



---

## Przykład: Inhibitor wzrostu siewek

<p class="lead-line">Naukowiec stara się o grant na badanie nowej grupy środków hamujących wzrost siewek.</p>

<div class="tiles4">
  <div class="tile">
    <div class="n">01</div>
    <h3>Pomiary</h3>
    <p>liczba wykiełkowanych siewek, dzień po dniu</p>
  </div>
  <div class="tile">
    <div class="n">02</div>
    <h3>Zapis</h3>
    <p>dane i podpisany znacznik czasu</p>
  </div>
  <div class="tile repeat">
    <div class="n">03</div>
    <h3>Wniosek</h3>
    <p>ujawnia się <em>jedynie</em> wynik np. sumę wykiełkowanych siewek&nbsp;<b>45</b></p>
  </div>
  <div class="tile repeat">
    <div class="n">04</div>
    <h3>Weryfikacja</h3>
    <p>dowolna osoba z dowodem sprawdzi wynik i datę utworzenia danych źródłowych</p>
  </div>
  <p class="tile-note left"><span class="chip muted">×n</span>kolejne wpisy, każdy z datą</p>
  <p class="tile-note accent right"><span class="chip">×n</span>z zapisanych danych można wyciągać wiele wniosków</p>
</div>

<!--
CEL (2:50–3:30): jedna historia, cztery kafelki, żadnych liczb poza 45.
1. Codzienne pomiary — ile siewek wykiełkowało danego dnia.
2. Pomiary są zapisane i opatrzone podpisanym znacznikiem czasu.
3. Wniosek grantowy zawiera wyłącznie wynik: 45. Komisja nie dostaje serii pomiarów.
4. Weryfikacja — komisja sprawdza wynik i datę dowodem, bez dostępu do pomiarów.
Kluczowe: kroki 3 i 4 są powtarzalne. Jeden zapis danych obsługuje wiele wniosków (kolejne granty, kolejne publikacje) i wiele niezależnych weryfikacji — za każdym razem bez oddawania pomiarów.
-->

---

<!-- _class: demo -->

## Jak to wygląda w praktyce?

<div class="demo-grid">
  <div class="demo-col">
    <h3>Wejście — dane badacza</h3>
    <table class="sheet series">
      <tr><th>dzień</th><th>siewki</th></tr>
      <tr><td>1</td><td>8</td></tr>
      <tr><td>2</td><td>6</td></tr>
      <tr><td>3</td><td>5</td></tr>
      <tr><td>4</td><td>7</td></tr>
      <tr><td>5</td><td>3</td></tr>
      <tr><td>6</td><td>4</td></tr>
      <tr><td>7</td><td>6</td></tr>
      <tr><td>8</td><td>2</td></tr>
      <tr><td>9</td><td>4</td></tr>
      <tr class="sum"><td>SUMA</td><td>45</td></tr>
    </table>
    <div class="hint">
      <div class="hint-label">Interfejs</div>
      <p>Zwykły arkusz kalkulacyjny. Wystarczy zaznaczyć zakres komórek i wskazać, które mają zostać zamaskowane.</p>
    </div>
  </div>
  <div class="demo-col">
    <h3>Wyjście — widok komisji</h3>
    <table class="sheet series">
      <tr><th>dzień</th><th>siewki</th></tr>
      <tr><td>1</td><td class="hidden"><span class="mask"></span></td></tr>
      <tr><td>2</td><td class="hidden"><span class="mask"></span></td></tr>
      <tr><td>3</td><td class="hidden"><span class="mask"></span></td></tr>
      <tr><td>4</td><td class="hidden"><span class="mask"></span></td></tr>
      <tr><td>5</td><td class="hidden"><span class="mask"></span></td></tr>
      <tr><td>6</td><td class="hidden"><span class="mask"></span></td></tr>
      <tr><td>7</td><td class="hidden"><span class="mask"></span></td></tr>
      <tr><td>8</td><td class="hidden"><span class="mask"></span></td></tr>
      <tr><td>9</td><td class="hidden"><span class="mask"></span></td></tr>
      <tr class="sum"><td>SUMA</td><td>45</td></tr>
    </table>
    <div class="claim">✓ Twierdzenie z dowodem kryptograficznym</div>
    <div class="verdict">Suma ukrytych danych wynosi 45, a dane te nie zmieniły się od czasu ich stworzenia np. 14 marca</div>
  </div>
</div>

<!--
CEL (3:20–4:10): pokazać, że komisja widzi wynik, a nie pomiary.
Interfejs: zwykły arkusz kalkulacyjny, zaznacza się zakres komórek do zamaskowania i nic więcej.
Po lewej to, co ma naukowiec: dziewięć pomiarów i suma. Po prawej to, co dostaje komisja: te same dni, zasłonięte pomiary, ta sama suma.
Werdykt: formuła dała 45 na ukrytych danych, które nie zmieniły się od 14 marca.
Uczciwie: w tym demo realne są commitment, drzewo Merkle i ścieżki inclusion; TSA i zk-SNARK to warstwa demonstracyjna (stopka).
-->

---

## Każda komórka ma swoją historię

<p class="lead-line">Dzięki temu, że trzymamy historię zmian, możemy wskazać, kiedy dana komórka została zmieniona.</p>

<div class="sheets3">
  <div class="sheetcol">
    <h3>Liczby</h3>
    <table class="sheet mini">
      <tr><th class="rn">dzień</th><th>siewki</th></tr>
      <tr><th class="rn">1</th><td>8</td></tr>
      <tr><th class="rn">2</th><td>6</td></tr>
      <tr><th class="rn">3</th><td class="changed">5</td></tr>
      <tr><th class="rn">4</th><td>7</td></tr>
      <tr><th class="rn">5</th><td>3</td></tr>
      <tr><th class="rn">6</th><td class="changed">4</td></tr>
      <tr><th class="rn">7</th><td>6</td></tr>
      <tr><th class="rn">8</th><td>2</td></tr>
      <tr><th class="rn">9</th><td class="changed">4</td></tr>
    </table>
  </div>
  <div class="sheetcol">
    <h3>Dziennik</h3>
    <table class="sheet mini">
      <tr><th class="rn">dzień</th><th>data zmiany</th></tr>
      <tr><th class="rn">1</th><td>02.03</td></tr>
      <tr><th class="rn">2</th><td>03.03</td></tr>
      <tr><th class="rn">3</th><td class="changed">09.03</td></tr>
      <tr><th class="rn">4</th><td>05.03</td></tr>
      <tr><th class="rn">5</th><td>06.03</td></tr>
      <tr><th class="rn">6</th><td class="changed">11.03</td></tr>
      <tr><th class="rn">7</th><td>08.03</td></tr>
      <tr><th class="rn">8</th><td>09.03</td></tr>
      <tr><th class="rn">9</th><td class="changed">12.03</td></tr>
    </table>
  </div>
  <div class="sheetcol wide">
    <h3>Widok komisji</h3>
    <table class="sheet mini">
      <tr><th class="rn">dzień</th><th>siewki</th><th>data zmiany</th></tr>
      <tr><th class="rn">1</th><td class="blur"><span class="mask"></span></td><td>02.03</td></tr>
      <tr><th class="rn">2</th><td class="blur"><span class="mask"></span></td><td>03.03</td></tr>
      <tr><th class="rn">3</th><td class="blur"><span class="mask on"></span></td><td class="changed">09.03</td></tr>
      <tr><th class="rn">4</th><td class="blur"><span class="mask"></span></td><td>05.03</td></tr>
      <tr><th class="rn">5</th><td class="blur"><span class="mask"></span></td><td>06.03</td></tr>
      <tr><th class="rn">6</th><td class="blur"><span class="mask on"></span></td><td class="changed">11.03</td></tr>
      <tr><th class="rn">7</th><td class="blur"><span class="mask"></span></td><td>08.03</td></tr>
      <tr><th class="rn">8</th><td class="blur"><span class="mask"></span></td><td>09.03</td></tr>
      <tr><th class="rn">9</th><td class="blur"><span class="mask on"></span></td><td class="changed">12.03</td></tr>
    </table>
  </div>
</div>

<!--
CEL (4:10–4:40): dziennik prowadzi datę każdej zmiany, nie tylko datę pliku.
Trzy arkusze to ten sam fragment danych: wartości, daty ostatniej zmiany każdej wartości, oraz widok komisji, gdzie wartości są zasłonięte, a daty zostają jawne.
Daty biegną od 02.03 do 12.03, czyli kończą się przed certyfikacją 14.03, więc nie kłócą się ze slajdem 6 („dane nie zmieniły się od 14 marca").
Podświetlone są trzy komórki poprawiane po pomiarze: dzień 3, 6 i 9.
-->

---

<!-- _class: end -->

<div class="thanks">
  <h2>Dziękuję za uwagę.</h2>
</div>