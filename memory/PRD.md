# Sonel MPI-530 Interaktywna Instrukcja - PRD

## Problem Statement
Interactive guide application for the Sonel MPI-530 electrical measurement meter. Supports three languages: Polish (PL), English (EN), German (DE). Provides step-by-step instructions, tools, calculators, protocol generation, and professional features.

## Architecture
- **Frontend**: React + Tailwind CSS + Shadcn/UI + i18n (custom LanguageProvider)
- **Backend**: FastAPI (all data hardcoded in server.py + translations.py)
- **Database**: None (all data mocked/hardcoded)

## Implemented Features

### Multi-language Support (PL/EN/DE)
- Language switcher in header (globe icon + dropdown)
- Language persists via localStorage
- Backend endpoints accept `?lang=pl|en|de` parameter
- All content fully translated: functions, steps, FAQ, quiz, error codes, checklists

### Core (10 measurement functions)
1. Test Wyłączników Różnicowoprądowych (RCD)
2. Impedancja Pętli Zwarciowej
3. Rezystancja Izolacji
4. Rezystancja Uziemienia
5. Pomiar Napięcia
6. Ciągłość Przewodów Ochronnych
7. Kolejność Faz
8. Kierunek Obrotów Silnika
9. Pomiar Natężenia Oświetlenia
10. Uziemienie Metodą Cęgową

### Tools (9 tabs)
1. Kalkulator Zs → Ik
2. Kalkulator doboru przewodów
3. Tabele norm PN-HD 60364
4. Kody błędów (12)
5. Schematy podłączeń (8)
6. Checklista bezpieczeństwa (6)
7. Generator protokołu PDF
8. Quiz z certyfikatem (15 pytań)
9. Notatki i historia (localStorage)

### Protocols, FAQ, PDF Export
- 4 instrukcje Sonel Reports Plus
- 5 szablonów + 5 przykładowych protokołów
- 13 pytań FAQ
- Statyczny PDF eksport (34 strony)

## Key Files
- `/app/backend/server.py` - Backend logic and Polish data
- `/app/backend/translations.py` - EN and DE translations
- `/app/frontend/src/App.js` - Main component
- `/app/frontend/src/i18n/` - Language context and JSON files (pl/en/de)
- `/app/frontend/src/components/ToolsComponents.js` - Professional tools

## Testing
- Iteration 3: Backend 28/28, Frontend 100% (core features)
- Iteration 4: Backend 21/21, Frontend 100% (i18n feature)

## Status: COMPLETE
