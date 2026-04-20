# Prompt pro subagenta fáze 1

Předpokládá, že `search_definition.md` je již v kontextu.

---

Jsi subagent fáze 1 vyhledávání dle `search_definition.md` (kritéria zahrnutí, škála intenzity, formát souboru).

**Dotaz:** `{{DOTAZ}}`
**Vysvětlení:** {{VYSVETLENI}}

## Úkol

1. Spusť webové vyhledávání podle dotazu výše
2. Pro každý výsledek zkontroluj URL skriptem:
   ```
   python check_url.py <url>
   ```
   - vypíše `new` → URL je nová, pokračuj na WebFetch
   - vypíše `exists` → URL již byla zpracována, přeskoč ji
3. Pro nové URL:
   - stáhni obsah (`WebFetch`)
   - klasifikuj intenzitu **veganského rámce** (škála dle `search_definition.md`); pokud = `Nulový`, **přeskoč**
   - klasifikuj intenzitu **environmentálního rámce** (škála dle `search_definition.md`); pokud = `Nulový`, **přeskoč**
   - splňuje-li oba rámce nenulovou intenzitu, ulož do `articles/` ve formátu dle `search_definition.md`
4. Paywallové články značit `[paywall]` v názvu souboru.

## Návrat

Počet nově uložených článků.
