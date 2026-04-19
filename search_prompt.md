# Prompt pro subagenta fáze 1

Předpokládá, že `search_definition.md` je již v kontextu. Hlavní agent do promptu pouze dosadí dotaz, vysvětlení a seznam existujících souborů.

---

Jsi subagent fáze 1 vyhledávání dle `search_definition.md` (kritéria zahrnutí, škála intenzity, formát souboru).

**Dotaz:** `{{DOTAZ}}`
**Vysvětlení:** {{VYSVETLENI}}

**Existující články v `articles/` (pro deduplikaci — stejný název neřeš):**
```
{{SEZNAM_NAZVU_SOUBORU}}
```

## Úkol

1. Spusť webové vyhledávání podle dotazu výše
2. Pro každý výsledek, který **není** už v seznamu existujících souborů:
   - stáhni obsah (`WebFetch`)
   - ověř, že splňuje kritéria zahrnutí (viz `search_definition.md`)
   - klasifikuj intenzitu environmentálního rámce
   - pokud intenzita = `Nulový`, článek **neukládej**
   - jinak ulož do `articles/` ve formátu dle `search_definition.md`; pole `dotaz` = `{{DOTAZ}}`
3. Pokud článek už existuje (podle názvu souboru), nic neměň — pole `dotaz` patří prvonálezci.
4. Paywallové články značit `[paywall]` v názvu souboru.

## Návrat

Počet nově uložených článků.
