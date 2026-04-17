# Procedura vyhledávání — technický postup pro agenta

Navazuje na `search_definition.md` (metodologie — **co a proč**). Tento soubor popisuje **jak** agent provede fáze 1 a 2.

## Struktura souborů

```
/
├── search_definition.md
├── search_procedure.md
├── search_queries.md             # log vyhledávacích dotazů
└── articles/
    └── *datum* - *zdroj* - *intenzita* - *název*.md
```

## Formát `search_queries.md`

Append-only log. Agent přidává řádky a mění stav, nikdy nemaže.

```markdown
# Vyhledávací dotazy

| Dotaz | Vysvětlení | Stav | Nových článků |
|-------|------------|------|---------------|
| veganství klima média | překryv enviro + veganství v mediálním jazyce | hotovo | 4 |
| rostlinná strava uhlíková stopa | test mediální enviro terminologie | čeká | — |
```

Stav: `čeká` nebo `hotovo`.
**Nových článků** = počet článků nově uložených právě tímto dotazem (duplicity s předchozími dotazy se nepočítají).

## Fáze 1 — vyhledávání

**Vstup:** `search_queries.md` s alespoň jedním řádkem ve stavu `čeká`.

### 1.1 Paralelní subagenti

Pro každý čekající dotaz spustit jednoho subagenta typu `general-purpose` paralelně (více `Agent` volání v jednom tool-use bloku).

**Prompt subagenta obsahuje:**

1. Přesný dotaz a jeho vysvětlení
2. `search_definition.md` (kritéria zahrnutí)
3. Seznam **názvů** existujících souborů v `articles/` (pro deduplikaci)
4. Pokyn: pro každý nový článek splňující kritéria (intenzita ≠ `Nulový`) — stáhnout (`WebFetch`), klasifikovat intenzitu, uložit do `articles/` ve formátu dle `search_definition.md`, včetně pole „vyhledávací dotaz" = aktuální dotaz.
5. Pokud článek už existuje, **nic neměnit** — pole „vyhledávací dotaz" zůstává s prvním dotazem, který ho našel.
6. Vrátit: počet nově uložených článků.

### 1.2 Aktualizace logu

Po dokončení všech subagentů hlavní agent změní stav dotazů na `hotovo` a doplní **Nových článků**.

### 1.3 Konec iterace

Jedna věta shrnutí (počet nových, zdroje) a požádat o `/clear`.

## Fáze 2 — brainstorming nových dotazů

**Vstup:** čistý kontext.

### 2.1 Načtení kontextu

Agent načte:

- `search_definition.md`
- `search_queries.md`
- **Plné obsahy článků z poslední iterace** (podle `Nových článků` u dotazů se stavem `hotovo`, který právě přibyl — tj. články, které hlavní agent ještě neviděl). Pro starší články stačí názvy.

Obsah nových článků je klíčový pro to, kam dál mířit — mediální jazyk, argumenty, zdroje, slepá místa.

### 2.2 Návrh nových dotazů

Podle fáze 2 ze `search_definition.md`:

- **podobné články** — z terminologie nových článků
- **slepá místa** — kategorie z analytických rámců bez pokrytí (např. žádný článek o rybolovu)
- `site:zdroj.cz` — kde má zdroj víc článků, ověřit další
- `-site:zdroj.cz` — pokud vzorek dominuje jeden zdroj

Každý dotaz s krátkým vysvětlením.

### 2.3 Zápis

Nové dotazy přidat do `search_queries.md` se stavem `čeká`.

### 2.4 Konec iterace

Oznámit počet nových dotazů a požádat o `/clear`.

## Smyčka

```
opakuj:
    [čistý kontext] fáze 1
    /clear
    [čistý kontext] fáze 2
    /clear
dokud fáze 2 nepřidá žádný nový dotaz  (saturace)
```

## Doporučení pro výkon a cenu

- **Subagenti fáze 1 paralelně** — izolují kontext hlavního vlákna. Latence = nejpomalejší subagent. Praktické maximum ~5–10 paralelně.
- **Haiku pro subagenty fáze 1** (mechanická práce: search + fetch + save) → 3–5× levnější než Sonnet. **Sonnet pro hlavní vlákno a fázi 2** (syntéza, klasifikace rámce).
- **`/clear` mezi fázemi je povinný** — bez něj kontext roste a prompt cache se rozpadá.
- **Prompt caching**: `search_definition.md` + `search_queries.md` držet na začátku promptu subagenta, během iterace je neměnit (log se aktualizuje až po dokončení všech subagentů).
- **Deduplikace přes název souboru** — subagent dostane seznam existujících názvů, ušetří `WebFetch`.
- **Jedna iterace = jeden git commit** — rollback, diff mezi iteracemi, stabilní cache.
- **Ruční stop při 2 prázdných iteracích po sobě** — saturaci poznáš dřív, než smyčka sama.
- **Paywall** — v názvu souboru značit `[paywall]`, ať je jasné, co dodělat ručně s předplatným.

## Na co pamatovat

- `search_queries.md` je append-only. Stav se mění, obsah ne.
- Pokud subagent selže (timeout, nedostupný web), dotaz zůstává `čeká` — příští iterace zopakuje.
- Klasifikaci intenzity rámce dělá subagent, který článek čte. Hlavní agent ji nerevizuje bez důvodu.
- Pole „vyhledávací dotaz" u článku je **prvonalezení**, ne seznam.
